import argparse, os, json
import torch
import numpy as np
from tqdm import tqdm
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
    
class NonlinearPotentialOp(torch.nn.Module):
    """Logic to implement NeuralNet to capture nonlinear Potential characteristics
       The input and output dimension of the net is same
       User is expected to provide the depth of the sequence 
    """
    
    def __init__(self, dim, depth,*args, **kwargs) -> None:
        """Setup the NonlinearFlux operator

        Args:
            dim (int): Number of flux components
            depth (int): Depth of the Neural Net i.e layers
        """
        super().__init__(*args, **kwargs)
        sequence = []
        self.depth = depth
        scale = 2
        sequence.append(torch.nn.Linear(dim,scale*dim))
        for i in range(depth-1):
            sequence.append(torch.nn.ReLU())
            sequence.append(torch.nn.Linear(scale*dim,scale*dim))
        sequence.append(torch.nn.ReLU())
        sequence.append(torch.nn.Linear(scale*dim,dim))
        
        self.operator = torch.nn.Sequential(*sequence)
        self.sequence = sequence
    
    @torch.no_grad
    def exportToNumpy(self):
        """Export the linear operators in the sequence as 
            numpy Matrices and Vectors for reconstruction in python
            Assumes that the activation function is fixed and know (ReLU)
        Returns:
            (list[numpy.array],list[numpy.array]): _description_
        """
        Amats = []
        Bvecs = []
        Amats.append(self.sequence[0].weight.cpu().numpy())
        Bvecs.append(self.sequence[0].bias.cpu().numpy())
        ix = 1
        for i in range(self.depth-1):
            Amats.append(self.sequence[ix+1].weight.cpu().numpy())
            Bvecs.append(self.sequence[ix+1].bias.cpu().numpy())            
            ix+=2
        Amats.append(self.sequence[-1].weight.cpu().numpy())
        Bvecs.append(self.sequence[-1].bias.cpu().numpy())   
        
        return Amats,Bvecs         
        
    def forward(self,input):
        """Compute the flux for given input and parameter configuration

        Args:
            input (torch.Tensor): node potentials

        Returns:
            torch.Tensor: Node fluxes
        """
        return self.operator(input)
 
class NodeFluxDataSet(Dataset):
    def __init__(self,datadir,ztol=1e-14):    
        self.data_files = []
        u0 = []
        f0 = []
        testcases = []
        with open(os.path.join(datadir,"runresults.json"),"r") as rf:
            resultsfile = json.load(rf)
            
        for k,v in resultsfile.items():
            if v["success"]:
                testcases.append(f"{k}.npy")
                
        for f in os.listdir(datadir):
            if f.endswith("npy") and f in testcases:
               with open(os.path.join(datadir,f),"rb") as df:
                    self.data_files.append(os.path.join(datadir,f))
                    np.load(df) #times
                    # tranpose to get it in states x time
                    np.load(df) #states
                    np.load(df) #rates
                    u = np.load(df) #Hamiltonians
                    np.load(df) #External Energy inputs
                    f = np.load(df) #Total Energy inputs
                    u0.append(u)
                    f0.append(f)

        #Time shifted indexes should be performed for each dataset
        #Created the shifted arrays here before stacking
        #Input is made of u at t and state at t-1
        # uf,ff are in states x time, 
        # Stack all the states per time and then horizontall stack the resulting arrays
        uonestep = []  # u at t
        ustep = []     # u at t-1
        ubackstep = [] # u at t-2
        fstep = []
        for ix,uf in enumerate(u0):
            u = uf[:,          2:]  #Ham at t 
            fs =  f0[ix][:,2:]      #f0 at t  
            usingle = uf[:,1:-1]    #Ham at t-1           
            ubstep = uf[:,:-2]      #Ham at t-2           
            ustep.append(u)
            fstep.append(fs)
            uonestep.append(usingle)
            ubackstep.append(ubstep)
        
        #Stack along time dimension, and remove zero (abs value < 1e-10) columns
        ufull = np.hstack(ustep).squeeze()
        ffull = np.hstack(fstep).squeeze()
        usful = np.hstack(uonestep).squeeze()
        ubful = np.hstack(ubackstep).squeeze()
        
        uoneidx = np.argwhere(np.all(np.abs(ufull[..., :]) < 1e-10, axis=0))
        foneidx = np.argwhere(np.all(np.abs(ffull[..., :]) < 1e-10, axis=0))
        idx = np.intersect1d(uoneidx,foneidx)
        if idx.shape[0] > 2:
            ilen = int(idx.shape[0]*0.01) #Leave 1% of zeros in
            uf = np.delete(ufull,idx[:ilen],axis=1)
            ff = np.delete(ffull,idx[:ilen],axis=1)
            usf = np.delete(usful,idx[:ilen],axis=1)
            ubf = np.delete(ubful,idx[:ilen],axis=1)
        else:
            uf = ufull
            ff = ffull
            usf = usful
            ubf = ubful
 
        #Check if hamiltonian value at t-2 is also provided
        #X format is batch x [input(t),ham(t-1),ham(t-2)]

        #setup for batching
        self.u0 = torch.from_numpy(np.expand_dims(uf,axis=-1)).type(torch.float)
        self.ff = torch.from_numpy(np.expand_dims(ff,axis=-1)).type(torch.float)
        self.usf = torch.from_numpy(np.expand_dims(usf,axis=-1)).type(torch.float)

        self.num_items = self.u0.shape[1] #Reflect the number of samples
        print(f"Dataset of size {uf.shape} loaded.")

    def __len__(self):
        return self.num_items
    
    def __getitem__(self, idx):
        return self.u0[:,idx], self.ff[:,idx], self.usf[:,idx]
    
class LinearForwardOp(torch.nn.Module):
    
    def __init__(self,boundaryOperator,weights=None,*args,**kwargs) -> None:
        """Create an Operator to predict node values from boundary fluxes

        Args:
            boundaryOperator (np.array): Boundary operator of the 1-form
            weights (np.array): Initial edge weights for the network, default None - uses random values 
        """
        super().__init__(*args, **kwargs)
        self.boundaryOperator = boundaryOperator
        self.coBoundaryOperator = np.transpose(boundaryOperator)
        r,c = boundaryOperator.shape
        self.B2dim = c
        self.B1dim = r
        self.D2dim = c
        self.D1dim = r        
        
        self.Rdim  = r
        self.numnodes = c #Number of nodes in the complex
        self.numcomponents = r #Number of flux vector components
        self.co = torch.from_numpy(self.coBoundaryOperator).type(torch.float)
        self.bo = torch.from_numpy(self.boundaryOperator).type(torch.float)
        if weights is None:
            self.R = torch.nn.Parameter(torch.randn(self.Rdim))    
        else:
            if weights.shape[0] == self.Rdim:
                self.R = torch.nn.Parameter(torch.from_numpy(weights).type(torch.float))
            else:
                raise Exception(f"Weights array dimension ({weights.shape}) does not match the boundary operator dimensions {r}")    

        self.B2 = torch.nn.Parameter(torch.abs(torch.randn(self.B2dim)))
        self.B1inv = torch.nn.Parameter(torch.abs(torch.randn(self.B1dim)))
        self.D2 = torch.nn.Parameter(torch.abs(torch.randn(self.D2dim)))
        self.D1iv = torch.nn.Parameter(torch.abs(torch.randn(self.D1dim)))

        #Allocate space        
        self.costar = torch.matmul(torch.diag(self.R),self.bo)
        self.DIV_h = torch.matmul(torch.matmul(torch.diag(self.B2),self.co),torch.diag(self.B1inv))
        self.GRADstar_h = -torch.matmul(torch.matmul(torch.diag(self.D1iv),self.costar),torch.diag(self.D2))
        #This is the adjoint (div = -grad*), so negative
        print(f"Operator setup with {self.numnodes} node potentials, and {self.numcomponents} fluxes")
                    

    @torch.no_grad
    def setInitialResistanceParameters(self,r:torch.Tensor):
        if r.shape[0] == self.R.shape[0] and r.shape[1] == self.R.shape[1]:
            self.R.data = r.data
        else:
            raise Exception(f"Input tensor dimension of {r.shape} does not match with problem resistance {self.R.shape}")
    
    @torch.no_grad
    def getOperator(self):
        """Get the operator and coefficient of integration for current fitting parameters
        Returns:
            (np.array,float): Tuple with operator B (u0 = B f0 + c) and coefficient of integration c
        """
        self.costar = torch.matmul(torch.diag(self.R),self.bo)
        self.DIV_h = torch.matmul(torch.matmul(torch.diag(self.B2),self.co),torch.diag(self.B1inv))
        self.GRADstar_h= -torch.matmul(torch.matmul(torch.diag(self.D1iv),self.costar),torch.diag(self.D2))
        op = torch.matmul(self.DIV_h,self.GRADstar_h)
        return op.cpu().detach().numpy()
    
    def forward(self,input):
        """Compute fluxes for given potentials

        Args:
            input (torch.Tensor): numcomponents x [tensor of fluxes, tensor of node potentials at t-1]
        """
        costar = torch.matmul(torch.diag(self.R),self.bo)
        DIV_h = torch.matmul(torch.matmul(torch.diag(self.B2),self.co),torch.diag(self.B1inv))
        GRADstar_h= -torch.matmul(torch.matmul(torch.diag(self.D1iv),costar),torch.diag(self.D2))
        #return f0 - Delta u = f0        
        return torch.matmul(DIV_h,torch.matmul(GRADstar_h,input))      

class NonlinearOp(torch.nn.Module):
    
    def __init__(self,grad, div, depth=1, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.grad = grad.clone().detach()
        self.div = div.clone().detach()
        gradT = torch.t(grad)
        divT  = torch.t(div)
        self.invLinO = torch.matmul(gradT,divT).clone().detach()
        self.NN = NonlinearPotentialOp(self.div.shape[0],depth)
        
    @torch.no_grad
    def exportToNumpy(self):
        """Export the operators are numpy matrices 
           to reconstruct the model in python without torch dependencies
        Returns:
            (np.array,np.array,list(np.array),list(np.array)): Grad, Div, NN linear opertors weight matrices, bias vectors (in the order of their application)
        """
        mats,bias = self.NN.exportToNumpy()
        return self.grad.cpu().numpy(),self.div.cpu().numpy(),mats,bias

        
    def forward(self,input):
        u = input[:,:,:,1] #Node potential at time t-1
        f = input[:,:,:,0] #External flux  at time t
        linrev = torch.matmul(self.invLinO,f)
        internalflux = torch.matmul(self.div,torch.matmul(self.grad,u))
        nnflux = self.NN(internalflux.squeeze()).unsqueeze(axis=-1) + f

        return linrev + nnflux 
                
def computeGradientsForLinOpParameterUpdate(d:LinearForwardOp,u0:torch.Tensor,f0:torch.Tensor):
    """Logic for computing gradients for parameters

    Args:
        d (Operator): AdjointOfLaplacianOperator instance
        u0 (torch.Tensor): Node potentials
        f0 (torch.Tensor): Node fluxes (potential at t-2 if used for pysr fitting)
    Returns:
        (float): Loss
    """
    dres = d(u0)
    loss = torch.mean(((dres-f0))**2)
    #loss = (((dres-f0))**2).sum()
    #loss = torch.linalg.norm(dres - f0,axis=-1).sum()
    # backward pass for computing the gradients of the loss w.r.t to learnable parameters
    loss.backward()

    return loss.item()

def train_one_epoch_for_linop(d,training_loader,optimizer, epoch_index, batchsize, erf, pbar=None, tb_writer=None):
    running_loss = 0.
    last_loss = 0.

    # Here, we use enumerate(training_loader) instead of
    # iter(training_loader) so that we can track the batch
    # index and do some intra-epoch reporting
    batchCount = 0
    for i, data in enumerate(training_loader):
        # Every data instance is an input + label pair
        u0i, f0i, _ = data
        
        # Zero your gradients for every batch!
        optimizer.zero_grad()

        # Make predictions for this batch

        loss = computeGradientsForLinOpParameterUpdate(d,u0i,f0i)
        running_loss += loss
        # Adjust learning weights
        optimizer.step()
        batchCount += 1
        # Gather data and report
        if i>0 and i % erf == 0:
            last_loss = running_loss  # loss per erf iteration
            #print(f'\tbatch {i + 1}\tMSE loss: {last_loss}')
            if pbar is not None:
                pbar.set_postfix({f'batch {(i + 1):2d} MSE loss': last_loss})
            tb_x = epoch_index * len(training_loader) + i + 1
            if tb_writer:
                tb_writer.add_scalar('Loss/train', last_loss, tb_x)
            running_loss = 0.0
            batchCount = 0

    return max(running_loss,last_loss)

def computeGradientsForNonLinOpParameterUpdate(d:NonlinearOp,u0:torch.Tensor,f0:torch.Tensor,u1:torch.Tensor):
    """Logic for computing gradients for parameters

    Args:
        d (Operator): AdjointOfLaplacianOperator instance
        u0 (torch.Tensor): Node potentials
        f0 (torch.Tensor): Node fluxes 
        u1 (torch.Tensor): Node potentials at t-1
    Returns:
        (float): Loss
    """
    dres = d(torch.stack((f0,u1),axis=-1))
    #loss = torch.mean(((dres-u0))**2)
    loss = (((dres-u0))**2).sum()
    #loss = torch.linalg.norm(dres - u0,axis=-1).sum()
    # backward pass for computing the gradients of the loss w.r.t to learnable parameters
    loss.backward()

    return loss.item()

def train_one_epoch_for_nonlinop(d,training_loader,optimizer, epoch_index, erf, pbar=None, tb_writer=None):
    running_loss = 0.
    last_loss = 0.

    # Here, we use enumerate(training_loader) instead of
    # iter(training_loader) so that we can track the batch
    # index and do some intra-epoch reporting
    batchCount = 0
    for i, data in enumerate(training_loader):
        # Every data instance is an input + label pair
        u0i, f0i, u1 = data
        
        # Zero your gradients for every batch!
        optimizer.zero_grad()

        # Make predictions for this batch

        loss = computeGradientsForNonLinOpParameterUpdate(d,u0i,f0i,u1)
        running_loss += loss
        # Adjust learning weights
        optimizer.step()
        batchCount += 1
        # Gather data and report
        if i>0 and i % erf == 0:
            last_loss = running_loss  # loss per erf iteration
            #print(f'\tbatch {i + 1}\tMSE loss: {last_loss}')
            if pbar is not None:
                pbar.set_postfix({f'batch {(i + 1):2d} MSE loss': last_loss})
            tb_x = epoch_index * len(training_loader) + i + 1
            if tb_writer:
                tb_writer.add_scalar('Loss/train', last_loss, tb_x)
            running_loss = 0.0
            batchCount = 0

    return max(running_loss,last_loss)

def parse_args():
    parser = argparse.ArgumentParser(
        description='Neumann to Dirchlet map operator deduction')
    parser.add_argument("--datadir", default=r"__DATADIRECTORY__",help="directory in which results are to be stored")
    parser.add_argument("--outputdir", default=r"__MODEL_OUPUT__", help="directory in which results are to be stored")
    parser.add_argument("-ot","--operatortemplate", default=r"__OPERATOR_TEMPLATE__", help="path to boundary operator template")
    parser.add_argument("-od","--operatordepth", default=5, type=int, help="Depth of NonlinearOp NN")
    
    parser.add_argument(
        '--device', type=str, default='cuda', help='CPU/CUDA device option')
    parser.add_argument(
        '--batchsize',type=int,default=50,help='batch size.')
    parser.add_argument(
        '--epochs',type=int,default=2000,help='number of epochs.')
    parser.add_argument(
        '--savetraining',action='store_true',help='Save training metadata')  
    parser.add_argument(
        '--plot',action='store_true',help='Save training metadata')
      
    args, unknown = parser.parse_known_args()
    return args

os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

if __name__ == '__main__':
    torch.manual_seed(0)
       
    args = parse_args()
    targetDevice = 'cpu'
    if args.device:
        if args.device.startswith('cuda'):
            if torch.cuda.is_available():
                targetDevice = args.device
    
    device = torch.device(targetDevice)
    datadirectory = args.datadir
    BATCH_SIZE = 50
    if args.batchsize:
        BATCH_SIZE = args.batchsize
    EPOCHS = 300
    if args.epochs:
        EPOCHS = args.epochs
    saveTrainingMetadata = False
    if args.savetraining:
        saveTrainingMetadata = True
    opdepth = 5
    if args.operatordepth:
        opdepth=args.operatordepth
    operatortemplatefile = args.operatortemplate
    
    training_data = NodeFluxDataSet(datadirectory)
    
    train_dataloader = DataLoader(training_data, batch_size=BATCH_SIZE, shuffle=True)
    validation_loader = DataLoader(training_data, batch_size=BATCH_SIZE, shuffle=True)
    output_loader = DataLoader(training_data, batch_size=len(training_data), shuffle=False)
    savefile = os.path.join(os.path.dirname(os.path.abspath(operatortemplatefile)),"n2dmap.npy")
    adjmodel = None
    model = None #NonlinearModel
    bestmodel = None
    best_vloss = 1_000_000.
    EPOCH_REPORT_FREQ = int(np.floor(np.sqrt(len(train_dataloader))))
    
    if not (args.plot and os.path.exists(savefile)):
        print("Finding Linear Operator")
        with open(operatortemplatefile,'rb') as ops:
            boundaryOp = np.load(ops)
            edgeWeights = np.load(ops)
            _ = np.load(ops) #weighted divergence
        
        adjmodel = LinearForwardOp(boundaryOp,edgeWeights)
        adjmodel.train(True)   
                                
        optimizer = torch.optim.Adam(adjmodel.parameters())

        writer = None
        if saveTrainingMetadata:
            from torch.utils.tensorboard import SummaryWriter
            from datetime import datetime    
            
            # Initializing in a separate cell so we can easily add more epochs to the same run
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            writer = SummaryWriter('runs/neuman2dirchletlinop_trainer_{}'.format(timestamp))
        
        
        avg_loss = best_vloss
        loss_fn = torch.nn.MSELoss()
        with tqdm(range(EPOCHS)) as pbar:
            for epoch in pbar:
                pbar.set_description(f'EPOCH {(epoch + 1):4d} : MSE Loss {avg_loss:.5f}')
                
                # Make sure gradient tracking is on, and do a pass over the data
                adjmodel.train(True)
                avg_loss = train_one_epoch_for_linop(adjmodel,train_dataloader,optimizer,epoch,BATCH_SIZE,EPOCH_REPORT_FREQ,pbar)

                running_vloss = 0.0
                # Set the model to evaluation mode, disabling dropout and using population
                # statistics for batch normalization.
                adjmodel.eval()

                # Disable gradient computation and reduce memory consumption.
                with torch.no_grad():
                    for i, vdata in enumerate(validation_loader):
                        uov, fov, _ = vdata
                        voutputs = adjmodel(fov)
                        vloss = loss_fn(voutputs, uov)
                        running_vloss += vloss

                avg_vloss = running_vloss / (i + 1)
                pbar.set_description(f'EPOCH {epoch + 1} : MSE Train Loss {avg_loss:.5f} Valid Loss {avg_vloss.item():.5f}')

                if saveTrainingMetadata:
                    # Log the running loss averaged per batch
                    # for both training and validation
                    writer.add_scalars('Training vs. Validation Loss',
                                    { 'Training' : avg_loss, 'Validation' : avg_vloss },
                                    epoch + 1)
                    writer.flush()

                # Track best performance, and save the model's state
                if avg_vloss < best_vloss:
                    best_vloss = avg_vloss
                    bestmodel = adjmodel.state_dict() #adjmodel.getOperator()
    

        if bestmodel is None:
            bestmodel = adjmodel.state_dict() #adjmodel.getOperator()
        
        os.makedirs(args.outputdir,exist_ok=True)
        savefile = os.path.join(args.outputdir,"linOpn2dmap.npy")
        
        torch.save(bestmodel,savefile)

        print(f"Completed linop runs, saved operator to file {savefile}. Operator MSE Loss: {best_vloss}")    
    
    #Train nonlinearop
    best_vloss = 1_000_000.
    bestnonlinop = None
    if not (args.plot and os.path.exists(savefile)):
        print("Finding NonLinear Operator")
        if adjmodel is None:
            with open(operatortemplatefile,'rb') as ops:
                boundaryOp = np.load(ops)
                edgeWeights = np.load(ops)
                _ = np.load(ops) #weighted divergence
            
            adjmodel = LinearForwardOp(boundaryOp,edgeWeights)
            linopfile = os.path.join(args.outputdir,"linOpn2dmap.npy")
            adjmodel.load_state_dict(torch.load(linopfile))
            
        model = NonlinearOp(adjmodel.GRADstar_h,adjmodel.DIV_h,depth=opdepth)
        model.train(True)   
                                
        optimizer = torch.optim.Adam(model.parameters())

        writer = None
        if saveTrainingMetadata:
            from torch.utils.tensorboard import SummaryWriter
            from datetime import datetime    
            
            # Initializing in a separate cell so we can easily add more epochs to the same run
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            writer = SummaryWriter('runs/neuman2dirchletop_trainer_{}'.format(timestamp))
        
        avg_loss = best_vloss
        loss_fn = torch.nn.MSELoss()
        with tqdm(range(EPOCHS)) as pbar:
            for epoch in pbar:
                pbar.set_description(f'EPOCH {(epoch + 1):4d} : MSE Loss {avg_loss:.5f}')
                
                # Make sure gradient tracking is on, and do a pass over the data
                model.train(True)
                avg_loss = train_one_epoch_for_nonlinop(model,train_dataloader,optimizer,epoch,EPOCH_REPORT_FREQ,pbar)

                running_vloss = 0.0
                # Set the model to evaluation mode, disabling dropout and using population
                # statistics for batch normalization.
                model.eval()

                # Disable gradient computation and reduce memory consumption.
                with torch.no_grad():
                    for i, vdata in enumerate(validation_loader):
                        uov, fov, u1v = vdata
                        voutputs = model(torch.stack((fov,u1v),axis=-1))
                        vloss = loss_fn(voutputs, uov)
                        running_vloss += vloss

                avg_vloss = running_vloss / (i + 1)
                #print(f'MSE LOSS train {avg_loss} valid {avg_vloss}')
                pbar.set_description(f'EPOCH {epoch + 1} : MSE Train Loss {avg_loss:.5f} Valid Loss {avg_vloss.item():.4f}')
                #pbar.set_postfix({'MSE Loss valid ': avg_vloss.item()})

                if saveTrainingMetadata:
                    # Log the running loss averaged per batch
                    # for both training and validation
                    writer.add_scalars('Training vs. Validation Loss',
                                    { 'Training' : avg_loss, 'Validation' : avg_vloss },
                                    epoch + 1)
                    writer.flush()

                # Track best performance, and save the model's state
                if avg_vloss < best_vloss:
                    best_vloss = avg_vloss
                    bestnonlinop = model.state_dict()


        os.makedirs(args.outputdir,exist_ok=True)
        savefile = os.path.join(args.outputdir,"n2dmap.npy")
        torch.save(bestnonlinop,savefile)
        #Save the best model operator for reconstruction
        model.load_state_dict(bestnonlinop)
        res = model.exportToNumpy()
        nonlinopsavefile = os.path.join(args.outputdir,"numpynonlinearoperator.npy")
        with open(nonlinopsavefile,'wb') as nsf:
            #Since array elements shapes are different, save seperately
            np.save(nsf,len(res[3])) #Store the number of Amats and Bvecs
            np.save(nsf,res[0])
            np.save(nsf,res[1])
            for A in res[2]:
                np.save(nsf,A)            
            for b in res[3]:
                np.save(nsf,b)
        
        print(f"Completed runs, saved operator to file {savefile}. Operator MSE Loss: {best_vloss}")    
    
    
    if model is None and adjmodel is None:
        with open(operatortemplatefile,'rb') as ops:
            boundaryOp = np.load(ops)
            edgeWeights = np.load(ops)
            _ = np.load(ops) #weighted divergence
        
        adjmodel = LinearForwardOp(boundaryOp,edgeWeights)
        linopfile = os.path.join(args.outputdir,"linOpn2dmap.npy")
        adjmodel.load_state_dict(torch.load(linopfile))
    
        model = NonlinearOp(adjmodel.GRADstar_h,adjmodel.DIV_h,depth=opdepth)        
        nonlinopfile = os.path.join(args.outputdir,"n2dmap.npy")
        model.load_state_dict(torch.load(nonlinopfile))
        
    from matplotlib import pyplot as plt
    for ui,fi,u1 in output_loader:

        pred = model(torch.stack((fi,u1),axis=-1)).cpu().detach().numpy().flatten()
        uif = ui.cpu().detach().numpy().flatten()
        err = np.mean((uif-pred)**2)
        _, axs = plt.subplots(1, 2, layout='constrained')
        axs[0].scatter(uif, pred,s=0.1)
        axs[0].set_xlabel('Truth')
        axs[0].set_ylabel('Prediction')
        axs[0].set_title('ElementWise')
        axs[1].scatter(range(uif.shape[0]),uif,label ='Truth',s=1,marker='^')
        axs[1].scatter(range(pred.shape[0]),pred,label ='Prediction',s=1,marker='v')
        axs[1].set_xlabel('Time')
        axs[1].set_ylabel('Hamiltonian')
        axs[1].set_title('Continous')
        axs[1].legend(loc="upper right")
        plt.suptitle(f"Operator performance loss {err:.4f}")
        resultfile = os.path.join(args.outputdir,"n2d_mlp_mapperformance.png")
        plt.savefig(resultfile,dpi=300, bbox_inches='tight')
        if args.plot:
            plt.show()