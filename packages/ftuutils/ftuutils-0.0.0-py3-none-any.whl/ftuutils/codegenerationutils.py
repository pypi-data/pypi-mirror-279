"""Logic for generating pythonic code from FTU composition"""

import sympy
from sympy import Matrix
import re, os, json
from collections import OrderedDict

def _stringsubs(target, mapping):
    """Substitute mapping into target string

    Args:
        target (string): Target string
        mapping (dict): Key value pairs for replacement

    Returns:
        string: replaced string
    """
    for k, v in mapping.items():
        if not v.startswith("\\"):
            target = re.sub(re.escape(k), v, target)
        else:
            target = re.sub(re.escape(k), f"\\{v}", target)
    return target

def exportAsPython(composer):
    """Export the FTU description in the composer as python code

    Args:
        composer (compositionutils.Composer): Composer instance that has the resolved FTU 
    """
    numconstants,constantsubs,nonlinearrhsterms,inputs,arrayedinputs,arraymapping,uCapterms,ucapdescriptive,nonlineararrayedrhsterms,nonlinearrhstermsdescriptive,arrayedrhs,invarraymapping,rhs,ubaridxmap,cleaninputs = composer.generatePythonIntermediates()
    stateVec = Matrix(composer.stateVec)
    # Generate metedata
    variabledescription = 'VOI_INFO = {"name": "t", "units": "second", "component": "main", "type": VariableType.VARIABLE_OF_INTEGRATION}\n'
    variabledescription += "STATE_INFO = [\n"
    for k, v in composer.statevalues.items():
        variabledescription += f'\t{{"name": "{k}", "units": "{v["units"]}", "component": "main", "type": VariableType.STATE}},\n'
    variabledescription += "]\n\nVARIABLE_INFO = [\n"
    # Maintain this order when creating variables
    # Do constant subs, constant subs will have multiple values for the same constant due to precision
    definedNames = []
    for k, v in constantsubs.items():
        if v not in definedNames:
            if not v.name.startswith("-"):
                variabledescription += f'\t{{"name": "{v}", "units": "dimensionless", "component": "main", "type": VariableType.CONSTANT}},\n'
                definedNames.append(v)

    # TODO compute the units of calculated terms
    # Do uCap terms
    for v in stateVec:
        variabledescription += f'\t{{"name": "u_{v}", "units": "dimensionless", "component": "main", "type": VariableType.INTERNAL_INPUT}},\n'
    for s in composer.uVecSymbols:
        variabledescription += f'\t{{"name": "{s}", "units": "dimensionless", "component": "main", "type": VariableType.EXTERNAL_INPUT}},\n'

    # Do nonlinear terms
    for k, v in nonlinearrhsterms.items():
        variabledescription += f'\t{{"name": "{k}", "units": "dimensionless", "component": "main", "type": VariableType.ALGEBRAIC}},\n'
    variabledescription += "]\n"

    # ucap and nonlinearrhs terms go into def compute_variables(voi, states, rates, variables)
    # nonlineararrayedrhsterms go into compute_rates(voi, states, rates, variables)
    # def compute_computed_constants(variables) is ucap and nonlinearrhs
    # def initialise_variables(states, variables) contains initialisations

    pycode = f"""
# The content of this file was generated using the FTUWeaver

from enum import Enum
import numpy as np


__version__ = "0.0.1"

STATE_COUNT = {len(composer.stateVec)}
VARIABLE_COUNT = {numconstants}


class VariableType(Enum):
    VARIABLE_OF_INTEGRATION = 0
    STATE = 1
    CONSTANT = 2
    COMPUTED_CONSTANT = 3
    ALGEBRAIC = 4
    INTERNAL_INPUT = 5
    EXTERNAL_INPUT = 6

{variabledescription}

def create_states_array():
    return np.zeros(STATE_COUNT)

def create_variables_array():
    return np.zeros(VARIABLE_COUNT)
        
def initialise_variables(states, variables):\n"""
    # Do states first
    for k, v in composer.statevalues.items():
        try:
            stmt = f"\t{arraymapping[k.name]} = {float(v['value']):6f}  #{k}\n"
        except:
            stmt = f"\t{arraymapping[k.name]} = {v['value']}  #{k}\n"
        pycode += stmt

    # Do constant subs
    definedVariables = []
    for k, v in constantsubs.items():
        if v not in definedVariables:
            if v.name in arraymapping:
                try:
                    stmt = f"\t{arraymapping[v.name]} = {float(k):6f}  #{v}\n"
                except:
                    stmt = f"\t{arraymapping[v.name]} = {k}  #{v}\n"
                pycode += stmt
                definedVariables.append(v)
    pycode += "\ndef compute_computed_constants(variables):\n\tpass\n\n"
    pycode += "def compute_variables(voi, states, rates, variables):\n\tt=voi #mapping to t\n"
    # Do uCap terms
    for k, v in uCapterms.items():
        pycode += f"\t#{ucapdescriptive[k]}\n"
        pycode += f"\t{k} = {v}\n"

    # Do rhs
    pycode += "\ndef compute_rates(voi, states, rates, variables):\n\tt=voi #mapping to t\n"
    # Do nonlinear terms - these depend on state values and therefore step size, os here instead of compute variables
    for k, v in nonlineararrayedrhsterms.items():
        pycode += f"\t#{nonlinearrhstermsdescriptive[k]}\n"
        pycode += f"\t{k} = {v}\n"
    for i, v in enumerate(arrayedrhs):
        pycode += fr"\t#\dot{{{composer.stateVec[i]}}} = {_stringsubs(str(v),invarraymapping)} # {sympy.simplify(rhs[i,0])}\n"
        pycode += fr"\trates[{i}] = {v}\n"

    # Do inputs
    pycode += "\ndef compute_inputs(voi,inputs,states,variables):\n"
    for i, v in enumerate(arrayedinputs):
        pycode += f"\t# cell[{i}] = {cleaninputs[i]}\n"
        pycode += f"\tinputs[{i}] = {v}\n"
    # Provide external input variable names in comment to help support
    ubarcomment = ""
    for k, v in ubaridxmap.items():
        ubarcomment += f"    #\t{k} -> {v}\n"
    pycode += f'''
from math import exp

def Heaviside(x):
    if x > 0:
        return 1.0
    return 0.0

def process_time_sensitive_events(voi, states, rates, variables):
    """Method to process events such as (re)setting inputs, updating switches etc
        Unline process_events, this method is called in rhs calculation
        Useful to ensure that time sensitive inputs are set espcially if ode integrator timestep spans over the 
        input time. Note that this should be re-entrant i.e. not modify states, else this will
        lead to solver dependent behaviour, esp. solvers that use multiple steps
        The method is called before each rhs evelauation
    Args:
        voi (int) : Current value of the variable of integration (time)
        states (np.array): A vectors of model states
        variables (_type_): A vector of model variables
    """
    #External input variables - listed to help code event processing logic
{ubarcomment}
    #Comment the line below (and uncomment the line after) to solve the model without event processing!    
    #raise("Process time sensitive events not implemented")
    #pass
    variables[0] = 0.0
    if voi > 100 and voi < 110:
        variables[0] = 0.5
    #Following needs to be performed to set internal inputs from current state values
    compute_variables(voi,states,rates,variables)    
    
def process_events(voi, states,variables):
    """Method to process events such as (re)setting inputs, updating switches etc
        The method is called after each successful ode step
    Args:
        voi (int) : Current value of the variable of integration (time)
        states (np.array): A vectors of model states
        variables (_type_): A vector of model variables
    """
    #External input variables - listed to help code event processing logic
{ubarcomment}

    #Comment the line below (and uncomment the line after) to solve the model without event processing!    
    #raise("Process events not implemented")

    pass

rates = np.zeros(STATE_COUNT)

def rhs(voi, states, variables):
    #Perform (re)setting of inputs, time sensitive event processing etc
    process_time_sensitive_events(voi,states,rates,variables)    
    #Compute rates
    compute_rates(voi,states,rates,variables)
    return rates

def solve_model(starttime=0,stoptime=300,steps=300):
    """Solve model with ODE solver"""
    from scipy.integrate import ode
    import numpy as np
    # Initialise constants and state variables
    states = create_states_array()
    variables = create_variables_array()
    initialise_variables(states,variables)
    # Set timespan to solve over
    voi = np.linspace(starttime, stoptime, steps)
    print(f" c0 {{variables[44]}}")
    print(f" ct {{variables[27]}}")
    print(f" sigma {{variables[136]}}")
    print(f" sqpi {{variables[135]}}")

    # Construct ODE object to solve
    r = ode(rhs)
    r.set_integrator('vode', method='bdf', atol=1e-06, rtol=1e-06, max_step=1)
    r.set_initial_value(states, voi[0])
    r.set_f_params(variables)

    # Solve model
    result = np.zeros((STATE_COUNT,steps))
    result[:,0] = states    
    for (i,t) in enumerate(voi[1:]):
        if r.successful():
            r.integrate(t)
            result[:,i+1] = r.y
            states = r.y
            #Perform event processing etc
            process_events(t,states,variables)
        else:
            break

    return (voi, result, variables)

import matplotlib.pyplot as plt
if __name__ == '__main__':
    t,r,v = solve_model()
    grid = plt.GridSpec({(len(composer.inodeIndexes)+1)//3}, 3, wspace=0.2, hspace=0.5)

    ix = 0
    for i in range({(len(composer.inodeIndexes)+1)//3}):
        for j in range(3):
            ax = plt.subplot(grid[i, j])
            ax.plot(r[ix,:])
            ax.title.set_text(f'{{ix//{(len(composer.stateVec)//len(composer.inodeIndexes))}+1}}')
            ix += {(len(composer.stateVec)//len(composer.inodeIndexes))}
            if ix+{(len(composer.stateVec)//len(composer.inodeIndexes))} > result.shape[0]:
                break
    plt.subplots_adjust(hspace=0.3)
    plt.subplots_adjust(wspace=0.3)
    plt.show() 
'''
    return pycode.replace("1**2*", "").replace("-1.0*","-")

def exportAsODEStepper(composer,modelName):
    r"""Generate numerically solvable PHS
        d/dx (Ex) = (J-R) Q x - \hat{B}\hat{C}\hat{B}^T \hat{u} + \bar{B} \bar{u}
        \hat{y} = \hat{B}^T Q x
        \bar{y} = \bar{B}^T Q x
    
        Setup the code as a Python class, with the ability to step through time and
        set inputs
    """
    numconstants,constantsubs,nonlinearrhsterms,inputs,arrayedinputs,arraymapping,uCapterms,ucapdescriptive,nonlineararrayedrhsterms,nonlinearrhstermsdescriptive,arrayedrhs,invarraymapping,rhs_,ubaridxmap,cleaninputs = composer.generatePythonIntermediates()

    #Also handle constant subs
    revconstantsubs = dict()
    for k,v in constantsubs.items():
        revconstantsubs[v] = k
    nonlinearrhstermssub = dict()
    for k,v in nonlinearrhsterms.items():
        nonlinearrhstermssub[k] = sympy.simplify(v.xreplace(revconstantsubs))

    rhs = composer.raw_rhs.xreplace(nonlinearrhstermssub)
    
    #Replace all symbolic parameters in hamiltonian with their values from composer.compositeparameters and constants
    parvals_ = dict()
    for k,v in composer.compositeparameters.items():
        parvals_[k] = v['value'].xreplace(nonlinearrhstermssub)
    #some composite parameters also use symbols listed in composite parameters
    parvals = dict()
    for k,v in parvals_.items():
        parvals[k] = v.xreplace(parvals_)
    
    #Subtitute in cellHamiltonians - requires symbols
    arraymappingsym = {sympy.Symbol(k):sympy.Symbol(v) for k,v in arraymapping.items()}
    cellhams = OrderedDict()
    externalInputEnergy = OrderedDict()
    totalInputEnergy = OrderedDict()
    ubaridxmapsym = {sympy.Symbol(k):sympy.Symbol(v) for k,v in ubaridxmap.items()}
    #For setting up energy calculations
    supportEnergyCalculations = OrderedDict()
    
    #Used for calculating total input energy contribution, sets all internal inputs to zero
    ubaridxmapzero = {sympy.Symbol(f"u_{s}"):0 for s in composer.stateVec}
    inputStateSymbolMap = {sympy.Symbol(f"u_{k}"):v for k,v in arraymapping.items()}
    
    inputsidx = 0
    #Determine the hamiltonian without exterior inputs - compare this with one having the
    #external inputs included to determing the energetic contribution from the external inputs
    noisubs = dict()
    for uin in composer.uVecSymbols:
        noisubs[uin] = 0
    cix = 0
    for k,v in composer.cellHamiltonians.items():
        cham = v.hamiltonian
        #Subtitute for inputs
        isubs = dict()
        istatemap = dict() #input variable to stateVec Index
        rhsidxmap = []
        for ui in v.u:
            if inputs[inputsidx]!=0:
                isubs[ui] = inputs[inputsidx]
                istatemap[ui] = inputsidx
            rhsidxmap.append(inputsidx)
            inputsidx +=1     
        cham = cham.xreplace(isubs) #isubs expands all internal inputs          
        noicham = cham.xreplace(noisubs) #Calculate hamiltonian without external inputs            
        notcham = noicham.xreplace(ubaridxmapzero) #Calculate the hamiltonian without any internal and external input contributions
        cdiff = sympy.simplify(cham - noicham)
        tdiff = sympy.simplify(cham - notcham)
        if cdiff != 0.0: #Store internal input data
            #isubs has all input related information
            cinps = {}
            csyms = []
            for k1,v1 in isubs.items():
                cexpr = v1.xreplace(noisubs)
                sv = composer.stateVec[istatemap[k1]]
                #Get the index into the state array, the expression
                cinps[sv] = [int(arraymapping[sv].replace("states[","").replace("]","")), cexpr] #noisubs remove external inputs
                csyms.extend(list(cexpr.free_symbols))
            csyms = list(set(csyms))
            csym_map = {}
            for kc in csyms:
                csym_map[kc]=int(inputStateSymbolMap[kc].replace("states[","").replace("]",""))
            #Map node label to input symbols and expressions - using subs as xreplace doesnt seem to handle **
            subbedHam = sympy.simplify(cham.xreplace(parvals).xreplace(revconstantsubs))
            supportEnergyCalculations[k] = {'cmap':csym_map,'expr':cinps,'ham':str(subbedHam),'rhsix':rhsidxmap,'cix':cix}
             
        cellhams[k] = cham.xreplace(arraymappingsym).xreplace(ubaridxmapsym) 
        externalInputEnergy[k] = cdiff.xreplace(arraymappingsym).xreplace(ubaridxmapsym) 
        totalInputEnergy[k] = tdiff.xreplace(arraymappingsym).xreplace(ubaridxmapsym) 
        cix +=1
    
    # Provide hook for inputs
    inputhook = dict()
    for k, v in ubaridxmap.items():
        #input name will be suffixed by the network id through which it communicates
        ik = '_'.join(k.split('_')[:-1])
        inputhook[ik] = v    
    inputhookcode = f'class {modelName}Hooks():\n    #PHS Input name and variable entry\n'
    inputhookcode += "    inputhooks={"
    for k,v in inputhook.items():
        inputhookcode += f"\n        '{k}':'{v}',"
    inputhookcode += "\n        }\n    #Node name and state array entries for each associated state variable\n    statehooks={"   
    
    stateNameToVectorIndexMap = dict()
    
    for k,ph in composer.nodePHSData.items():
        statemap = dict()
        statelist = list(map(str,ph.states))
        #Find PH name prefix - if it exists
        commonprefix = os.path.commonprefix(statelist)

        cix = len(commonprefix)
        for six,st in enumerate(statelist):
            stt = st.split('_')[:-1]
            if cix > 0:
                stn = '_'.join(stt[1:])
            else:
                stn = '_'.join(stt)
            #Store the statename to solution array index for PySR fitting
            if stn not in stateNameToVectorIndexMap:
                stateNameToVectorIndexMap[stn] = []
            stateNameToVectorIndexMap[stn].append(int(f"{arraymappingsym[ph.states[six]]}".replace("states[","").replace("]","")))
                
            statemap[stn]= str(arraymappingsym[ph.states[six]])
        inputhookcode += f"\n        '{k}':{json.dumps(statemap)},"
    inputhookcode += "\n        }\n    #State name and solution vector indexes for each associated PHS state variable\n    statenamehooks={"               
    for k1,v1 in stateNameToVectorIndexMap.items():
        inputhookcode += f"\n        '{k1}':[{','.join(map(str,v1))}],"    
    inputhookcode += "\n    }\n"  
    
    phsIndexMap = dict()
    #Node ordering is in composer.inodeIndexes
    for si, k in enumerate(composer.inodeIndexes):
        v = composer.cellTypePHS[k]
        if v not in phsIndexMap:
            phsIndexMap[v] = []
        phsIndexMap[v].append(si) #si is the index into the cell Hamiltonian vector
        
    inputhookcode += "    #PHS name and hamiltonian solution vector indexes \n    phsnamehooks={"
    for k,v in phsIndexMap.items():
        inputhookcode += f"\n        '{k}':[{','.join(map(str,v))}],"
    inputhookcode += "\n        }\n\n"

    inputsymbols = []
    for sm in composer.uVecSymbols:
        inputsymbols.append(f"'{sm}'")

    inputhookcode += f'class {modelName}Inputs():\n    #Input Node mappings \n'
    inputhookcode += "    nodes=[\n"
    for k,v in supportEnergyCalculations.items():
        svmap = v['cmap']
        inexpr = v['expr']
        sorder = dict()
        si = 0
        for w,va in composer.nodePHSData[k].statevalues.items():
            sorder[str(w)] = {'value':f"{va['value']:.5f}",'order':si}
            si +=1
        
        inputhookcode += f"            {{\n                'nodelabel':{k},\n"
        inputhookcode += f"                'hamiltonianIndex':{v['cix']},\n"
        inputhookcode += f"                'hamiltonian':'{v['ham']}',\n"
        inputhookcode += f"                'states':{json.dumps(sorder)},\n"
        inputhookcode += f"                'inputs':[{','.join(inputsymbols)}],\n"
        inputhookcode += f"                'rhs':[\n"
        for v1 in v['rhsix']:
            inputhookcode += f"                    '{sympy.simplify(rhs[v1])}',\n"
        inputhookcode += f"                ],\n"
        inputhookcode += f"                'statevarmap':{{\n"
        for k1,v1 in svmap.items():
            inputhookcode += f"                        '{k1}':{v1},\n"
        inputhookcode += f"                }},\n"  
        inputhookcode += f"                'inputExpressions':{{\n"          
        for k1,v1 in inexpr.items():
            inputhookcode += f"                        '{k1}':{{'statevecindex':{v1[0]},'expr':'{v1[1]}'}},\n"
        inputhookcode += f"                }}\n            }},\n"              
    inputhookcode += "        ]"
    
    pycode = f"""
# The content of this file was generated using the FTUWeaver

import numpy as np
from numpy import exp
from scipy.integrate import ode

def Heaviside(x):
    if x > 0:
        return 1.0
    return 0.0

__version__ = "0.0.1"

{inputhookcode}

class {modelName}():
    STATE_COUNT = {len(composer.stateVec)}
    VARIABLE_COUNT = {numconstants}
    CELL_COUNT  = {len(composer.inodeIndexes)}

    stateIndexes = {json.dumps(stateNameToVectorIndexMap)}

    def __init__(self):
        self.states = np.zeros(self.STATE_COUNT)
        self.rates = np.zeros(self.STATE_COUNT)
        self.variables = np.zeros(self.VARIABLE_COUNT)
        self.time = 0.0
        self.odeintegrator = ode(lambda t,x : self.rhs(t,x))
        self.odeintegrator.set_integrator('vode', method='bdf', atol=1e-06, rtol=1e-06, max_step=1)
        self.odeintegrator.set_initial_value(self.states, self.time)       
        #Initialize variables
        states, variables = self.states, self.variables
"""
    # Do states first
    for k, v in composer.statevalues.items():
        try:
            stmt = f"        {arraymapping[k.name]} = {float(v['value']):6f}  #{k}\n"
        except:
            stmt = f"        {arraymapping[k.name]} = {v['value']}  #{k}\n"
        pycode += stmt

    # Do constant subs
    definedVariables = []
    for k, v in constantsubs.items():
        if v not in definedVariables:
            if v.name in arraymapping:
                try:
                    stmt = f"        {arraymapping[v.name]} = {float(k):6f}  #{v}\n"
                except:
                    stmt = f"        {arraymapping[v.name]} = {k}  #{v}\n"
                pycode += stmt
                definedVariables.append(v)

    pycode += "\n    def compute_variables(self,voi):\n        t=voi #mapping to t\n        states, rates, variables = self.states,self.rates,self.variables\n"
    # Do uCap terms
    for k, v in uCapterms.items():
        pycode += f"        #{ucapdescriptive[k]}\n"
        pycode += f"        {k} = {v}\n"

    # Do rhs
    pycode += "\n    def compute_rates(self,voi):\n        t=voi #mapping to t\n        states, rates, variables = self.states,self.rates,self.variables\n"
    # Do nonlinear terms - these depend on state values and therefore step size, os here instead of compute variables
    for k, v in nonlineararrayedrhsterms.items():
        pycode += f"        #{nonlinearrhstermsdescriptive[k]}\n"
        pycode += f"        {k} = {v}\n"
    for i, v in enumerate(arrayedrhs):
        pycode += f"        #\\dot{{{composer.stateVec[i]}}} = {_stringsubs(str(v),invarraymapping)} # {sympy.simplify(rhs[i,0])}\n"
        pycode += f"        rates[{i}] = {v}\n"

    # Do inputs
    pycode += f"\n    def compute_inputs(self,voi,inputs):\n        t,states,variables=voi,self.states,self.variables\n        #inputs size {len(composer.stateVec)}\n"
    for i, v in enumerate(arrayedinputs):
        pycode += f"        # forstate[{i}] = {cleaninputs[i]}\n"
        pycode += f"        inputs[{i}] = {v}\n"

    # Compute Hamiltonian's for each cells
    pycode += f"\n    def compute_hamiltonian(self,cellHam):\n        t,states,variables=self.time,self.states,self.variables\n        #cellHam = np.zeros({len(composer.inodeIndexes)})\n"
    cix = 0
    for k,v in cellhams.items():
        pycode += f"        cellHam[{cix}] = {v}\n"
        cix +=1
    pycode += f"\n        return cellHam\n"

    # Compute energy input from external inputs
    pycode += f"\n    def compute_external_energy(self,inputEnergy):\n        t,states,variables=self.time,self.states,self.variables\n        #inputEnergy = np.zeros({len(composer.inodeIndexes)})\n"
    cix = 0
    for k,v in externalInputEnergy.items():
        pycode += f"        inputEnergy[{cix}] = {v}\n"
        cix +=1
    pycode += f"\n        return inputEnergy\n"

    # Compute energy input from internal and external inputs
    pycode += f"\n    def compute_total_input_energy(self,totalInputEnergy):\n        t,states,variables=self.time,self.states,self.variables\n        #totalInputEnergy = np.zeros({len(composer.inodeIndexes)})\n"
    cix = 0
    for k,v in totalInputEnergy.items():
        pycode += f"        totalInputEnergy[{cix}] = {v}\n"
        cix +=1
    pycode += f"\n        return totalInputEnergy\n"
            
    # Provide external input variable names in comment to help support
    ubarcomment = ""
    for k, v in ubaridxmap.items():
        ubarcomment += f"        #\t{k} -> {v}\n"

    pycode += f'''
    def process_time_sensitive_events(self,voi):
        """Method to process events such as (re)setting inputs, updating switches etc
        Unline process_events, this method is called in rhs calculation
        Useful to ensure that time sensitive inputs are set espcially if ode integrator timestep spans over the 
        input time. Note that this should be re-entrant i.e. not modify states, else this will
        lead to solver dependent behaviour, esp. solvers that use multiple steps
        The method is called before each rhs evelauation
        Args:
            voi (int) : Current value of the variable of integration (time)
            states (np.array): A vectors of model states
            variables (_type_): A vector of model variables
        """
        states, rates, variables = self.states,self.rates,self.variables
        #External input variables - listed to help code event processing logic
{ubarcomment}
        #Comment the line below (and uncomment the line after) to solve the model without event processing!    
        #raise("Process time sensitive events not implemented")
        variables[0] = 0.0
        if voi > 100 and voi < 110:
            variables[0] = 0.5        
        #Following needs to be performed to set internal inputs from current state values
        self.compute_variables(voi)    
            
    def process_events(self,voi):
        """Method to process events such as (re)setting inputs, updating switches etc
        The method is called after each successful ode step
        Args:
            voi (int) : Current value of the variable of integration (time)
        """
        #External input variables - listed to help code event processing logic
        states, rates, variables = self.states,self.rates,self.variables
{ubarcomment}
        #Comment the line below (and uncomment the line after) to solve the model without event processing!    
        #raise("Process events not implemented")

    def getStateValues(self,statename):
        return self.states[self.stateIndexes[statename]]

    def setStateValues(self,statename,values):
        self.states[self.stateIndexes[statename]] = values

    def rhs(self, voi, states):
        self.states = states    
        #Perform (re)setting of inputs, time sensitive event processing etc
        self.process_time_sensitive_events(voi)    
        #Compute rates
        self.compute_rates(voi)
        return self.rates

    def step(self,step=1.0):
        if self.odeintegrator.successful():
            self.odeintegrator.integrate(step)
            self.time = self.odeintegrator.t
            self.states = self.odeintegrator.y
            #Perform event processing etc
            self.process_events(self.time)
        else:
            raise Exception("ODE integrator in failed state!")

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    starttime=0
    stoptime=300
    steps=300
    finst = FTUStepper()
    voi = np.linspace(starttime, stoptime, steps)
    result = np.zeros((finst.STATE_COUNT,steps))
    result[:,0] = finst.states    
    for (i,t) in enumerate(voi[1:]):
        finst.step(t)
        result[:,i+1] = finst.states      
    fig = plt.figure(figsize=(50, 50))
    grid = plt.GridSpec({(len(composer.inodeIndexes)+1)//3}, 3, wspace=0.2, hspace=0.5)

    ix = 0
    for i in range({(len(composer.inodeIndexes)+1)//3}):
        for j in range(3):
            ax = plt.subplot(grid[i, j])
            ax.plot(result[ix,:])
            ax.title.set_text(f'{{ix//{(len(composer.stateVec)//len(composer.inodeIndexes))}+1}}')
            ix += {(len(composer.stateVec)//len(composer.inodeIndexes))}
            if ix+{(len(composer.stateVec)//len(composer.inodeIndexes))} > result.shape[0]:
                break
    plt.subplots_adjust(hspace=0.3)
    plt.subplots_adjust(wspace=0.3)
    fig.savefig(f"FTUStepper_results.png",dpi=300)
    plt.show()         
'''


    return pycode.replace("1**2*", "").replace("-1.0*","-")
