"""
Logic to determine the coefficients of the adjoint of the weighted lapacian operator
that maps flux inputs at FTU nodes to the hamiltonian/potential values of all FTU nodes

This is the inverse of the classic Possion problem on graphs \Delta H = f, \partial H = f0 on boundary

The problem has multiple solutions each differ by the constant of integration

The logic proceeds in two stages
1. Determine the parameters of the adjoint of the laplacian for which H = \Delta * f
2. Using this adjoint determine a Neural Network to determine the coefficient of integration

Note that in some problems the coefficients of the laplacian are known (when the FTU is constructed and the interconnecting network is the dominant dof through which energy is exchanged)
In such case these coefficents are set as the initial value and the parameter search is performed.

"""
from pysr import PySRRegressor #Import this before torch as pysr uses juliacall
import argparse, os, json
import torch
import numpy as np
from tqdm import tqdm
from torch.utils.data import Dataset
from torch.utils.data import DataLoader


"""
Import/Define functions that were passed in the unary_operator
block of pysr discovery process, if the function is used in the 
model expression and not defined lamdafication of the pysr expression will fail
Imports and definitions should be torch compatible (for instance 
import from numpy will fail with
RuntimeError: Can't call numpy() on Tensor that requires grad.
) detching break automatic differentiation
"""
#exp is an unary_operator and may be used in the expression
from torch import exp 


class PySRM():
    """
    Load pysr expressions and setup appropriate lambda expressions for evaluations
    """    
    def __init__(self, pysrexp) -> None:
        self.pystexp = []
        self.expressions = []
        self.uselagged = False
        for beq in pysrexp:
            if '#' in beq:
                beq = beq.split('#')[0]
            if 'x2' in beq:
                self.uselagged = True
                break
        
        for beq in pysrexp:
            if '#' in beq:
                beq = beq.split('#')[0]
            if 'x2' in beq:
                psm = lambda x0, x1, x2 : eval(beq)   
            else:
                if self.uselagged: #pass summy
                    psm = lambda x0, x1, _ : eval(beq)   
                else:
                    psm = lambda x0, x1 : eval(beq)  
            self.expressions.append(beq) 
            self.pystexp.append(psm)        
        
        sameExp = len(set(self.expressions))==1
        #If all expressions are same, calling lamda on the batch is more efficient
        if sameExp:
            if self.uselagged:
                self.apply = self.apply3All
            else:
                self.apply = self.apply2All            
        else:
            if self.uselagged:
                self.apply = self.apply3
            else:
                self.apply = self.apply2
    
    def getExpressions(self):
        return self.expressions
    
    def apply2(self,in1,in2):
        xu = torch.unbind(in1, dim=1) #Dim 1 is batch
        fu = torch.unbind(in2, dim=1) #Dim 1 is batch
        res = []
        for i in range(in1.shape[1]):
            res.append(self.pystexp[i](xu[i],fu[i]))
        return torch.stack(res,axis=1)

    def apply3(self,in1,in2,in3):
        xu = torch.unbind(in1, dim=1) #Dim 1 is batch
        fu = torch.unbind(in2, dim=1) #Dim 1 is batch
        xb = torch.unbind(in3, dim=1) #Dim 1 is batch
        res = []
        for i in range(input.shape[1]):
            res.append(self.pystexp[i](xu[i],fu[i],xb[i]))
        return torch.stack(res)

    def apply2All(self,in1,in2):
        return self.pystexp[0](in1,in2)

    def apply3All(self,in1,in2,in3):
        return self.pystexp[0](in1,in2,in3)

 
    @staticmethod
    def loadPySRMap(file): 
        pysrmap = []
        with open(file,'r') as srm:
            pm = json.load(srm)   
            expmap = dict()
            numdims = 0
            for ex in pm["expressions"]:
                if os.path.exists(ex["file"]):
                    fullPySRModel = PySRRegressor.from_file(ex["file"])
                    beq = fullPySRModel.get_best()
                    expmap[beq.equation] = ex["index"]
                    numdims += len(ex["index"])
                else:
                    raise FileNotFoundError(f"{ex['file']} not found!!")
            pysrmap = [None]*numdims
            for e,ix in expmap.items():
                for k in ix:
                    pysrmap[k] = e
            return pysrmap
    
class NodeFluxDataSet(Dataset):
    def __init__(self,datadir,uset2=False):    
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
        #Hamiltonian energy should be positive, some symbolic expressions may not have the constant coefficient
        # So we offset it
        # umin = np.min([uf.min(),usf.min(),ubf.min()])
        # if umin < 0:
        #     uf = uf - umin
        #     usf = usf - umin
        #     ubf = ubf - umin
        
        #Input is made of u at t and input at t, u at t-2 is also provided and can be added through pysr
        # uf,ff are in hams x time, energy x time, 
  
  
        #Check if hamiltonian value at t-2 is also provided
        #X format is batch x [input(t),ham(t-1),ham(t-2)]

        #setup for batching
        self.u0 = torch.from_numpy(np.expand_dims(uf,axis=-1)).type(torch.float)
        self.ff = torch.from_numpy(np.expand_dims(ff,axis=-1)).type(torch.float)
        self.usf = torch.from_numpy(np.expand_dims(usf,axis=-1)).type(torch.float)
        self.ubf = torch.from_numpy(np.expand_dims(ubf,axis=-1)).type(torch.float)

        self.num_items = self.u0.shape[1] #Reflect the number of samples
        print(f"Dataset of size {uf.shape} loaded.")

    def to_csv(self,filename):
        with open(filename,'w') as csv:
                print("Ham(t),TotalEnergy(t),Ham(t-1),Ham(t-2)",file=csv)
                for idx in range(self.num_items):
                    ds = torch.stack((self.u0[:,idx],self.ff[:,idx],self.usf[:,idx],self.ubf[:,idx]),axis=1).squeeze()        
                    for row in ds:
                        print(','.join(map(str,row.numpy())),file=csv)

    def __len__(self):
        return self.num_items
    
    def __getitem__(self, idx):
        return self.u0[:,idx], torch.stack((self.ff[:,idx],self.usf[:,idx],self.ubf[:,idx]),axis=1)        
    
class Neuman2DirechletOperator(torch.nn.Module):
    
    def __init__(self,boundaryOperator,pysrmodel, weights=None, *args,**kwargs) -> None:
        """Create an Operator to predict node values from boundary fluxes

        Args:
            boundaryOperator (np.array): Boundary operator of the 1-form
            weights (np.array): Initial edge weights for the network, default None - uses random values 
        """
        super().__init__(*args, **kwargs)
        self.pysrhamiltonianModel = pysrmodel
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

        
        self.coeffOfIntegration = torch.nn.Parameter(torch.randn(1).reshape((-1,1)))

        #Allocate space        
        self.costar = torch.matmul(torch.diag(self.R),self.bo)
        self.DIV_hT = torch.matmul(torch.matmul(torch.diag(self.B2),self.co),torch.diag(self.B1inv))
        self.GRADstar_hT= -torch.matmul(torch.matmul(torch.diag(self.D1iv),self.costar),torch.diag(self.D2))
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
        self.DIV_hT = torch.matmul(torch.matmul(torch.diag(self.B2),self.co),torch.diag(self.B1inv))
        self.GRADstar_hT= -torch.matmul(torch.matmul(torch.diag(self.D1iv),self.costar),torch.diag(self.D2))        
        #op = torch.matmul(self.GRADstar_hT,self.DIV_hT)
        op = torch.matmul(self.DIV_hT,self.GRADstar_hT)
        hamop = self.pysrhamiltonianModel.getExpressions()
        return op.cpu().detach().numpy(), self.coeffOfIntegration.cpu().detach().numpy()[0], hamop
    
    def forward(self,input):
        """Compute fluxes for given potentials

        Args:
            input (torch.Tensor): numcomponents x [tensor of fluxes, tensor of node potentials at t-1]
        """

        fx = input[:,:,0]
        u_1 = input[:,:,1]
        costar = -torch.matmul(torch.diag(self.R),self.bo)
        DIV_h = torch.matmul(torch.matmul(torch.diag(self.B2),self.co),torch.diag(self.B1inv))
        GRADstar_h= torch.matmul(torch.matmul(torch.diag(self.D1iv),costar),torch.diag(self.D2))
        
        lapterm = torch.matmul(DIV_h,torch.matmul(GRADstar_h,u_1))
        #Expression requires ham(t-1), input(t) and ham(t-2) if x2 is present
        if not self.pysrhamiltonianModel.uselagged:
            u0 = self.pysrhamiltonianModel.apply(u_1,lapterm+fx) + self.coeffOfIntegration
        else:
            u0 = self.pysrhamiltonianModel.apply(u_1,lapterm+fx, input[:,:,2]) + self.coeffOfIntegration
            
        return u0
        
def computeGradientsForParameterUpdate(d:Neuman2DirechletOperator,u0:torch.Tensor,f0:torch.Tensor):
    """Logic for computing gradients for parameters

    Args:
        d (Operator): AdjointOfLaplacianOperator instance
        u0 (torch.Tensor): Node potentials
        f0 (torch.Tensor): Node fluxes (potential at t-2 if used for pysr fitting)
    Returns:
        (float): Loss
    """
    dres = d(f0)
    #loss = torch.mean(((dres-u0))**2)
    loss = (((dres-u0))**2).sum()
    #loss = torch.linalg.norm(dres - u0,axis=-1).sum()
    # backward pass for computing the gradients of the loss w.r.t to learnable parameters
    loss.backward()

    return loss.item()

def train_one_epoch(d,training_loader,optimizer, epoch_index, batchsize, erf, pbar=None, tb_writer=None):
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

        loss = computeGradientsForParameterUpdate(d,u0i,f0i)
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
    parser.add_argument("--datadir", default=r"__DATADIRECTORY__",help="directory in which simulation results are stored")
    parser.add_argument("--outputdir", default=r"__MODEL_OUPUT__", help="directory in which results are to be stored")
    parser.add_argument("--pysrmap", default=r"__PYSRMAP__", help="path to pysr state map description")
    parser.add_argument("-ot","--operatortemplate", default=r"__OPERATOR_TEMPLATE__", help="path to boundary operator template")
    
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
    

    pysrmap = PySRM.loadPySRMap(args.pysrmap)
    
    operatortemplatefile = args.operatortemplate
    
    training_data = NodeFluxDataSet(datadirectory)
    
    train_dataloader = DataLoader(training_data, batch_size=BATCH_SIZE, shuffle=True)
    validation_loader = DataLoader(training_data, batch_size=BATCH_SIZE, shuffle=True)
    output_loader = DataLoader(training_data, batch_size=len(training_data), shuffle=False)
    savefile = os.path.join(os.path.dirname(os.path.abspath(operatortemplatefile)),"n2dmap.npy")
    bestmodel = None
    best_vloss = 1_000_000.
    if not (args.plot and os.path.exists(savefile)):
        pysrhamiltonianModel = PySRM(pysrmap)
        
        EPOCH_REPORT_FREQ = int(np.floor(np.sqrt(len(train_dataloader))))

        with open(operatortemplatefile,'rb') as ops:
            boundaryOp = np.load(ops)
            edgeWeights = np.load(ops)
            _ = np.load(ops) #weighted divergence
        
        adjmodel = Neuman2DirechletOperator(boundaryOp,pysrhamiltonianModel,edgeWeights)
        adjmodel.train(True)   
                                
        optimizer = torch.optim.Adam(adjmodel.parameters())

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
                pbar.set_description(f'EPOCH {(epoch + 1):4d} : MSE Loss {avg_loss:.4f}')
                
                # Make sure gradient tracking is on, and do a pass over the data
                adjmodel.train(True)
                avg_loss = train_one_epoch(adjmodel,train_dataloader,optimizer,epoch,BATCH_SIZE,EPOCH_REPORT_FREQ,pbar)

                running_vloss = 0.0
                # Set the model to evaluation mode, disabling dropout and using population
                # statistics for batch normalization.
                adjmodel.eval()

                # Disable gradient computation and reduce memory consumption.
                with torch.no_grad():
                    for i, vdata in enumerate(validation_loader):
                        uov, fov = vdata
                        voutputs = adjmodel(fov)
                        vloss = loss_fn(voutputs, uov)
                        running_vloss += vloss

                avg_vloss = running_vloss / (i + 1)
                #print(f'MSE LOSS train {avg_loss} valid {avg_vloss}')
                pbar.set_description(f'EPOCH {epoch + 1} : MSE Train Loss {avg_loss:.4f} Valid Loss {avg_vloss.item():.4f}')
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
                    bestmodel = adjmodel.getOperator()
    

        if bestmodel is None:
            bestmodel = adjmodel.getOperator()
        
        os.makedirs(args.outputdir,exist_ok=True)
        savefile = os.path.join(args.outputdir,"n2dmap.npy")
        
        with open(savefile,"wb") as n2d:
            np.save(n2d,bestmodel[0])
            np.save(n2d,bestmodel[1])
            np.save(n2d,bestmodel[2]) #This is a list of strings
            np.save(n2d,best_vloss)

        print(f"Completed runs, saved operator to file {savefile}. Operator MSE Loss: {best_vloss}")    

    if bestmodel is None:
        with open(savefile,"rb") as n2d:
            op1 = np.load(n2d)
            op2 = np.load(n2d)
            op3 = np.load(n2d) #This is a list of strings
            best_vloss = np.load(n2d)
        bestmodel = [op1,op2,op3,best_vloss]
        pysrhamiltonianModel = PySRM(op3)
  
    from matplotlib import pyplot as plt
    for ui,fi in output_loader:
        totalEnergy = np.matmul(bestmodel[0],ui) + fi[:,:,0]
        #pysrhamiltonianModel will use torch compatible unary ops
        pred = pysrhamiltonianModel.apply(fi[:,:,1],totalEnergy) + bestmodel[1]
        uif = ui.flatten()
        pred = pred.flatten()
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
        plt.suptitle(f"Operator performance loss {best_vloss:.4f}")
        resultfile = os.path.join(args.outputdir,"n2d_sr_mapperformance.png")
        plt.savefig(resultfile,dpi=300, bbox_inches='tight')
        if args.plot:
            plt.show()

