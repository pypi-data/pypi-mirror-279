import numpy as np

class NumpyNonlinearPotentialOp():
    """ Numpy based reconstruction of a NN sequence
    made of Linear transforms and ReLU activations
    the weight and bias vectors for each linear transform is provided in the
    Amats and Bvecs list
    """
    def __init__(self,Amats,Bvecs) -> None:
        self.Amats = Amats
        self.Bvecs = Bvecs
        
    def __call__(self, input):
        r1 = np.matmul(self.Amats[0],input) + self.Bvecs[0]
        for i in range(1,len(self.Amats)-1):
            act = np.maximum(0,r1) #ReLU
            r1 = np.matmul(self.Amats[i],act) + self.Bvecs[i]
        act = np.maximum(0,r1) #ReLU
        return np.matmul(self.Amats[-1],act) + self.Bvecs[-1]



class NumpyNonlinearOp():
    
    def __init__(self, grad, div, Amats, Bvecs) -> None:
        """Create operator to predict node potentials at time t, 
        given potentials at t-1 and node fluxes at time t

        Args:
            grad (np.array): Weighted Gradient operator for node potentials describing internal energy flows
            div (np.array): Weighted Divergence operator for node fluxes describing internal energy flows
            Amats (list[np.array]): Weights associated with the neural net to predict the nonlinear fluxes in the system
            Bvecs (list[np.array]): Bias vectors associated with the neural net to predict the nonlinear fluxes in the system
        """
        self.grad = grad
        self.div = div
        gradT = np.transpose(grad)
        divT  = np.transpose(div)
        self.invLinO = np.matmul(gradT,divT)
        self.NN = NumpyNonlinearPotentialOp(Amats,Bvecs)
        
    def __call__(self,f,u):
        """Apply operator to input node fluxes at t and node potentials at t-1

        Args:
            f (np.array): node fluxes/energy input at t
            u (np.array): node potentials/energy at time t-1

        Returns:
            np.array: node potentials/energy at time t
        """
        linrev = np.matmul(self.invLinO,f)
        internalflux = np.matmul(self.div,np.matmul(self.grad,u))
        nnflux = self.NN(internalflux) + f

        return linrev + nnflux 
    
    @staticmethod
    def fromFile(filename):
        """Construct the operator from file

        Args:
            filename (str): Location of operator

        Returns:
            NumpyNonlinearOp: Operator to predict node potentials
        """
        with open(filename,'rb') as fs:
            depth = np.load(fs) #The number of Amats and Bvecs
            r1 = np.load(fs)
            r2 = np.load(fs)
            r3 = []
            for i in range(depth):
                r3.append(np.load(fs)) #Load Amats
            r4 = []
            for i in range(depth):
                r4.append(np.load(fs)) #Load Bvecs
            nop = NumpyNonlinearOp(r1,r2,r3,r4)
            return nop        


#Helper function
def getOperator(filename=r"__OPERATOR_FILE__"):
    return NumpyNonlinearOp.fromFile(filename)