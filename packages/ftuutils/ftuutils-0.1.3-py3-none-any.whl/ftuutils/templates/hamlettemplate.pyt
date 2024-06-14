import numpy as np
from numpy import exp

def Heaviside(x):
    if x > 0:
        return 1.0
    return 0.0


class __Hamlet__():
    
    def __init__(self,
                 states=np.zeros(__NUM_STATES__),
                 rates=np.zeros(__NUM_STATES__),
                 fomstates=np.zeros(__TOTAL_STATES__),
                 inputs=np.zeros(__NUM_STATES__)) -> None:
        self.cellIndex = __CIX__
        self.statenames = [__STATE_NAMES__]
        self.states = states
        self.rates = rates
        self.fomstates = fomstates
        self.inputs = inputs        
        self.states = __INIT_STATES__

    def getHamiltonian(self):
        __GET_HAMILTONIAN__
        
    def getEnergyFromExternalInputs(self):
        __GET__ENERGYFROMEXTERNALINPUTS__
        
    def computeRHS(self,t):
        __COMPUTE_RHS__
        
if __name__ == '__main__':
    hm = __Hamlet__()
    hm.getHamiltonian()
    hm.computeRHS(0.0)