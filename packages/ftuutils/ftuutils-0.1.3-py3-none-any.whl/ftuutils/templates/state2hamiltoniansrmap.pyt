import numpy as np
from pysr import PySRRegressor
import os, json, shutil, argparse


class __HamiltonianToStateMap__():
    
    def __init__(self,datadir,ztol=1e-14,ust2=False) -> None:
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
                    data_files.append(os.path.join(datadir,f))
                    np.load(df) #times
                    # tranpose to get it in states x time
                    states = np.load(df) #states
                    np.load(df) #rates
                    u = np.load(df) #Hamiltonians
                    u0.append(u)
                    f0.append(states)
        #Time shifted indexes should be performed for each datase
        #Created the shifted arrays here before stacking
        #Input is made of u at t and state at t-1
        # uf,ff are in states x time, 
        # Stack all the states per time and then horizontall stack the resulting arrays
        uonestep = []
        fonestep = []
        fstep = []
        fbackstep = []
        for ix,uf in enumerate(u0):
            usingle = uf[:,          2:].T.reshape((-1,1))  #Ham at t 
            fs =  f0[ix][self.indexs,2:].T.reshape((-1,1))  #state at t            
            fsingle = f0[ix][self.indexs,1:-1].T.reshape((-1,1)) #state at t-1
            fb =  f0[ix][self.indexs,:-2].T.reshape((-1,1)) #state at t-2
            uonestep.append(usingle)
            fstep.append(fs)
            fonestep.append(fsingle)
            fbackstep.append(fb)
        
        #Stack along time dimension, and remove zero (abs value < 1e-10) columns
        uonefull = np.vstack(uonestep).squeeze()
        fonefull = np.vstack(fonestep).squeeze()
        fful     = np.vstack(fstep).squeeze()
        fbful    = np.vstack(fbackstep).squeeze()
        
        uoneidx = np.argwhere(np.abs(uonefull) < ztol)
        foneidx = np.argwhere(np.abs(fonefull) < ztol)
        idx = np.intersect1d(uoneidx,foneidx)
        if idx.shape[0] > 2:
            ilen = int(idx.shape[0]*0.01) #Leave 1% of zeros in
            uf = np.delete(uonefull,idx[:ilen])
            ff = np.delete(fonefull,idx[:ilen])
            ffu = np.delete(fful,idx[:ilen])
            fbf = np.delete(fbful,idx[:ilen])
        else:
            uf = uonefull
            ff = fonefull
            ffu = fful
            fbf = fbful
        #Hamiltonian energy should be positive, some symbolic expressions may not have the constant coefficient
        # So we offset it
        # umin = uf.min()
        # if umin < 0:
        #     uf = uf - umin
        
        #Input is made of u at t and state at t-1, state at t-2 is also provided and can be added through pysr
        # uf,ff are in states x time, 
        # Stack all the states per time and then horizontall stack the resulting arrays
        if ust2:
            self.X = np.c_[uf,ff,fbf]
        else:
            self.X = np.c_[uf,ff]
        #State at time t
        self.y = ffu 

    def fit(self,**kwargs):
            
        params = {
            "procs":2,
            "populations":2,    
            "niterations":400,  # < Increase me for better results
            "binary_operators":["+", "*", "-", "/"],
            "unary_operators":[
                "exp",
                #"inv(x) = 1/x",
                # ^ Custom operator (julia syntax)
            ],
            # Any functions/operators added to unary_operators should be imported/defined
            # in the mapped python code or the expression evaluation will fail
            "complexity_of_constants":2,
            # ^ Punish constants more than variables
            "select_k_features":2,
            # ^ Train on only the first 2 features, for all three make this 3
            "progress":False,
            "model_selection":"best",
            #model_selection= "accuracy",
            #extra_sympy_mappings={"inv": lambda x: 1 / x},
            # ^ Define operator for SymPy as well, loss penalises negative predictions as all Hamiltonians are positive or zero
            #elementwise_loss="loss(prediction, target) = (prediction - target)^2 + 1e3*(sign(prediction) - sign(target))^2",
            "elementwise_loss":"loss(prediction, target) = abs((prediction - target)/(target+1e-10)) + 1e3*(sign(prediction) - sign(target))^2",
            # ^ Custom loss function (julia syntax)
        }
        #Set batching if dataset size > 10000
        if self.y.shape[0] > 10000:
            params["batching"] = True
            bsr = self.y.shape[0]//10000
            params["batch_size"] = self.y.shape[0]//(bsr+1)
        params.update(kwargs)
        model = PySRRegressor(**params)
        model.fit(self.X,self.y)
        print(model)
        self.model = model

    def save(self,filename):
        basename = os.path.basename(os.path.abspath(self.model.equation_file_))
        basedir = os.path.dirname(os.path.abspath(self.model.equation_file_))
        pklfile = f"{os.path.join(basedir,os.path.splitext(basename)[0])}.pkl"
        if os.path.exists(pklfile):
            shutil.move(pklfile,filename)

    def cleanUp(self):
        """
            Remove temporary files created by PySR
        """
        basename = os.path.basename(os.path.abspath(self.model.equation_file_))
        fileprefix = os.path.splitext(basename)[0]
        basedir = os.path.dirname(os.path.abspath(self.model.equation_file_))
        for f in os.listdir(basedir):
            if f.startswith(fileprefix):
                os.remove(os.path.join(basedir,f))
        
    def plot(self):
        from matplotlib import pyplot as plt
        pred = self.model.predict(self.X)
        plt.scatter(self.y, pred)
        plt.xlabel('Truth')
        plt.ylabel('Prediction')
        plt.show()
        
        
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbosity", help="increase output verbosity", action="store_true")
    parser.add_argument("--plot", help="Show truth vs prediction plot", action="store_true")
    parser.add_argument("--numprocs", type=int,help="Number of processors to use", default=2)
    parser.add_argument("--numpops", type=int,help="Number of populations to use", default=2)
    parser.add_argument("--ztol", type=float,help="Zero tolerance, input values less than this are eliminated", default=1e-14)
    parser.add_argument("--maxiter", type=int,help="Maximum number of iterations to use", default=400)
    parser.add_argument("--maxconstants", type=int,help="Maximum number of constants in expressions", default=2)
    parser.add_argument("--modelselection", choices=['accuracy', 'score', 'best'], const='best',nargs='?', help="Maximum number of constants in expressions", default="best")
    parser.add_argument("--ut2", help="Use state value at t-2", action="store_true")
    parser.add_argument("--modelfile", help="Location to save model file", default=r"__MODEL_FILENAME__")
    parser.add_argument("--datadir", help="Location to data", default=r"__DATADIRECTORY__")
    parms = {}
    #args = parser.parse_args()
    args, unknown = parser.parse_known_args()
    if args.verbosity:
        parms["progress"] = True
    if args.maxiter:
        parms["niterations"] = args.maxiter
    if args.maxconstants:
        parms["complexity_of_constants"] = args.maxconstants
    if args.modelselection:
        parms["model_selection"] = args.modelselection
    if args.numprocs:
        parms["procs"] = args.numprocs
    if args.numpops:
        parms["populations"] = args.numpops
    ust2 = False
    if args.ut2:
        ust2 = True
        parms["select_k_features"] = 3
    ztol = 1.0e-14
    if args.ztol:
        ztol = args.ztol
    datadir = args.datadir
    savepkl = args.modelfile

    if os.path.exists(datadir):
        state2ham = __HamiltonianToStateMap__(datadir,ztol,ust2)    
        state2ham.fit(**parms)
        if args.plot:
            state2ham.plot()
        state2ham.save(savepkl)
        state2ham.cleanUp()
        print(f"PySR Model saved to {savepkl}")
    else:
        print(f"{datadir} does not exist!")