import torch
import numpy as np
from tqdm import tqdm
import os, json, argparse
from torch.utils.data import Dataset
from torch.utils.data import DataLoader


uset2 = False
class __HamiltonianToStateMapDataset__(Dataset):
    
    def __init__(self,datadir,ztol=1e-14) -> None:
        self.statename = "__STATENAME__"
        self.indexs =  __STATEINDEXS__
        
        """Load the experiment data files from the data folder and
        create inputs for PySR based symbolic regression using
        cell hamiltonian at time t, and state vector at time t -1 as input vector
        to predict the state vector at time t
        ztol (float, optional): Values below this tolerance are set to zero. Defaults to 1e-14.
        """
        data_files = []
        u0 = []
        state0 = []
        testcases = []
        with open(os.path.join(datadir,"runresults.json"),"r") as rf:
            resultsfile = json.load(rf)
            
        for k,v in resultsfile.items():
            if v["success"]:
                testcases.append(f"{k}.npy")
                
        for f in os.listdir(datadir):
            if f.endswith("npy") and f in testcases:
                with open(os.path.join(datadir,f),"rb") as df:
                    data_files.append(os.path.join(datadir,f))
                    np.load(df) #times
                    # tranpose to get it in states x time
                    states = np.load(df) #states
                    np.load(df) #rates
                    u = np.load(df) #Hamiltonians
                    u0.append(u)
                    state0.append(states)
        #Time shifted indexes should be performed for each datase
        #Created the shifted arrays here before stacking
        #Input is made of u at t and state at t-1
        # uf,ff are in states x time, 
        # Stack all the states per time and then horizontall stack the resulting arrays
        uonestep = []
        stateOneStep = []
        stateStep = []
        stateBackStep = []
        for ix,uf in enumerate(u0):
            usingle = uf[:,          2:].T.reshape((-1,1))  #Ham at t 
            ss =  state0[ix][self.indexs,2:].T.reshape((-1,1))  #state at t            
            ssingle = state0[ix][self.indexs,1:-1].T.reshape((-1,1)) #state at t-1
            sb =  state0[ix][self.indexs,:-2].T.reshape((-1,1)) #state at t-2
            uonestep.append(usingle)
            stateStep.append(ss)
            stateOneStep.append(ssingle)
            stateBackStep.append(sb)
        
        #Stack along time dimension, and remove zero (abs value < 1e-10) columns
        uonefull = np.vstack(uonestep).squeeze()
        stateOnefull = np.vstack(stateOneStep).squeeze()
        stateful     = np.vstack(stateStep).squeeze()
        stateBackful    = np.vstack(stateBackStep).squeeze()
        
        uoneidx = np.argwhere(np.abs(uonefull) < ztol)
        stateoneidx = np.argwhere(np.abs(stateOnefull) < ztol)
        idx = np.intersect1d(uoneidx,stateoneidx)
        if idx.shape[0] > 2:
            ilen = int(idx.shape[0]*0.01) #Leave 1% of zeros in
            uf = np.delete(uonefull,idx[:ilen])
            stateof = np.delete(stateOnefull,idx[:ilen])
            statef = np.delete(stateful,idx[:ilen])
            statebf = np.delete(stateBackful,idx[:ilen])
        else:
            uf = uonefull
            stateof = stateOnefull
            statef = stateful
            statebf = stateBackful
        # #Hamiltonian energy should be positive, some symbolic expressions may not have the constant coefficient
        # # So we offset it
        # umin = uf.min()
        # if umin < 0:
        #     uf = uf - umin
        
        self.state0 = torch.from_numpy(np.expand_dims(statef,axis=-1)).type(torch.float)
        self.stateof = torch.from_numpy(np.expand_dims(stateof,axis=-1)).type(torch.float)
        self.uf = torch.from_numpy(np.expand_dims(uf,axis=-1)).type(torch.float)
        self.statebf = torch.from_numpy(np.expand_dims(statebf,axis=-1)).type(torch.float)

        self.num_items = self.state0.shape[0] #Reflect the number of samples
           
    def __len__(self):
        return self.num_items
    
    def __getitem__(self, idx):
        if uset2:
            #State value at t, Hamiltonian at t, State value at t-1, State value at t-2
            return self.state0[idx], torch.hstack((self.uf[idx],self.stateof[idx],self.statebf[idx]))        
        else:
            #State value at t, Hamiltonian at t, State value at t-1
            return self.state0[idx], torch.hstack((self.uf[idx],self.stateof[idx]))
        
class NonlinearOp(torch.nn.Module):
    """Logic to implement NeuralNet to capture nonlinear energy dissipation characteristics
       The hamiltonian at time t-1 and total input energy at time t are inputs
       the hamiltonian at time t is predicted
       User is expected to provide the depth and hidden dimension of the sequence 
    """
    
    def __init__(self, dim, depth,*args, **kwargs) -> None:
        """Setup the NonlinearFlux operator

        Args:
            dim (int): Hidden dimension
            depth (int): Depth of the Neural Net i.e layers
        """
        super().__init__(*args, **kwargs)
        layers = []
        if uset2:
            layers.append(torch.nn.Linear(3,dim))
        else:
            layers.append(torch.nn.Linear(2,dim))
        for h in range(depth-1):
            layers.append(torch.nn.ReLU())
            layers.append(torch.nn.Linear(dim, dim))

        layers.append(torch.nn.ReLU())
        layers.append(torch.nn.Linear(dim, 1))            
        self.sequence = torch.nn.Sequential(*layers)
                
    def forward(self,input):
        """Compute the hamiltonian at t for given input and parameter configuration

        Args:
            input (torch.Tensor): ham at t-1, total energy input at t

        Returns:
            torch.Tensor: ham at t
        """
        return self.sequence(input)

def computeGradientsForParameterUpdate(d,u0:torch.Tensor,f0:torch.Tensor,lossfn):
    """Logic for computing gradients for parameters

    Args:
        d (Operator): NonlinearOp instance
        u0 (torch.Tensor): Ham at t (to predict)
        f0 (torch.Tensor): Ham at t-1, total input energy at t
    Returns:
        (float): Loss
    """
    dres = d(f0)
    loss = lossfn(dres, u0)
    #loss = torch.linalg.norm(dres - u0,axis=-1).sum()
    # backward pass for computing the gradients of the loss w.r.t to learnable parameters
    loss.backward()

    return loss.item()

def train_one_epoch(d,training_loader,optimizer, epoch_index, lossfn, erf, pbar=None, tb_writer=None):
    running_loss = 0.
    last_loss = 0.

    # Here, we use enumerate(training_loader) instead of
    # iter(training_loader) so that we can track the batch
    # index and do some intra-epoch reporting
    batchCount = 0
    for i, data in enumerate(training_loader):
        # Every data instance is an input + label pair
        u0i, f0i = data
        
        # Zero your gradients for every batch!
        optimizer.zero_grad()

        # Make predictions for this batch
        
        loss = computeGradientsForParameterUpdate(d,u0i,f0i,lossfn)
        running_loss += loss
        # Adjust learning weights
        optimizer.step()
        batchCount += 1
        # Gather data and report
        if i>0 and i % erf == 0:
            last_loss = running_loss 
            if pbar is not None:
                pbar.set_postfix({f'batch {(i + 1):2d} MSE Train loss': last_loss})
            tb_x = epoch_index * len(training_loader) + i + 1
            if tb_writer:
                tb_writer.add_scalar('Loss/train', last_loss, tb_x)
            running_loss = 0.0
            batchCount = 0

    return running_loss

os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
    
if __name__ == "__main__":
    BATCH_SIZE = 100
    EPOCHS = 50
    parser = argparse.ArgumentParser()
    parser.add_argument("--plot", help="Show truth vs prediction plot", action="store_true")
    parser.add_argument("--device", type=str,help="Training architecture cuda:x or cpu", default="cuda:0")
    parser.add_argument("--epochs", type=int,help="Maximum EPOCHS to train", default=400)
    parser.add_argument("--batchsize", type=int,help="Batch size for training", default=100)
    parser.add_argument("--ut2", help="Use state value at t-2", action="store_true")
    parser.add_argument("--modelpath", help="Location to save model", default=r"__MODEL_PATHNAME__")
    parser.add_argument("--datadir", help="Location to data", default=r"__DATADIRECTORY__")
    parms = {}
    #args = parser.parse_args()
    args, unknown = parser.parse_known_args()
    if args.ut2:
        uset2 = True
    if args.epochs:
        EPOCHS = args.epochs
    if args.batchsize:
        BATCH_SIZE = args.batchsize
        
    datadir = args.datadir
    modelsavepath = args.modelpath
    
    if args.device.startswith('cuda'):
        device = torch.device(args.device if torch.cuda.is_available() else 'cpu')
    torch.manual_seed(0)
    
    training_data = __HamiltonianToStateMapDataset__(datadir)    
    train_dataloader = DataLoader(training_data, batch_size=BATCH_SIZE, shuffle=True)
    validation_loader = DataLoader(training_data, batch_size=BATCH_SIZE, shuffle=True)
    output_loader = DataLoader(training_data, batch_size=len(training_data), shuffle=False)
    nonlinearOp = NonlinearOp(5, 1)
    nonlinearOp.train(True)   
                            
    optimizer = torch.optim.Adam(nonlinearOp.parameters())
    EPOCH_REPORT_FREQ = int(np.floor(np.sqrt(len(train_dataloader))))
    best_vloss = 1_000_000.
    avg_loss = best_vloss
    avg_vloss= best_vloss
    loss_fn = torch.nn.MSELoss()
    with tqdm(range(EPOCHS)) as pbar:
        for epoch in pbar:
            pbar.set_description(f'EPOCH {(epoch + 1):4d} : MSE Validation Loss {avg_vloss:.4f}')
            
            # Make sure gradient tracking is on, and do a pass over the data
            nonlinearOp.train(True)
            avg_loss = train_one_epoch(nonlinearOp,train_dataloader,optimizer,epoch,loss_fn,EPOCH_REPORT_FREQ,pbar)

            running_vloss = 0.0
            # Set the model to evaluation mode, disabling dropout and using population
            # statistics for batch normalization.
            nonlinearOp.eval()

            # Disable gradient computation and reduce memory consumption.
            with torch.no_grad():
                for i, vdata in enumerate(validation_loader):
                    uov, fov = vdata
                    voutputs = nonlinearOp(fov)
                    vloss = loss_fn(voutputs, uov)
                    running_vloss += vloss

            avg_vloss = running_vloss / (i + 1)
            # Track best performance, and save the model's state
            if avg_vloss < best_vloss:
                best_vloss = avg_vloss
                bestmodel = nonlinearOp.state_dict()

    checkpoint = {
        'model': nonlinearOp,
        'state_dict': bestmodel,
        'optimizer' : optimizer.state_dict()
    }

    torch.save(checkpoint, modelsavepath)

    if args.plot:
        from matplotlib import pyplot as plt
        for data in output_loader:
            y,X = data
            y = y.cpu().detach().numpy()
            nonlinearOp.load_state_dict(bestmodel)
            pred = nonlinearOp(X).cpu().detach().numpy()
            _, axs = plt.subplots(1, 2, layout='constrained')
            axs[0].scatter(y, pred,s=0.1)
            axs[0].set_xlabel('Truth')
            axs[0].set_ylabel('Prediction')
            axs[0].set_title('ElementWise')
            axs[1].scatter(range(y.shape[0]),y,label ='Truth',s=1,marker='^')
            axs[1].scatter(range(pred.shape[0]),pred,label ='Prediction',s=1,marker='v')
            axs[1].set_xlabel('Time')
            axs[1].set_ylabel('Hamiltonian')
            axs[1].set_title('Continous')
            axs[1].legend(loc="upper right")
            plt.show()