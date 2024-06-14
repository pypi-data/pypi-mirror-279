"""Logic to setup experiments based on generate FTU pythonic code"""
import ast
import os, datetime, json
import importlib.resources

class ExtractFTUDefinition(ast.NodeTransformer):
    """Extact FTU definition from generated pythonic code"""
    def visit_ClassDef(self, node):
        #Remove classes that end with name Hooks or Inputs
        if node.name.endswith("Hooks") or node.name.endswith("Inputs"):
            return None
        return node
    
    def visit_If(self, node):
        #Remove main
        if node.test.left.id == "__name__" and len(node.test.comparators)==1 and node.test.comparators[0].s == '__main__':
            return None
        return node

class Refactor(ast.NodeTransformer):
    """Pythonic code variable name replacement"""
    def __init__(self,varmap) -> None:
        super().__init__()
        self.variableNameMap = varmap 
    
    def visit_arg(self, node):
        if node.arg in self.variableNameMap: 
            return ast.arg(**{**node.__dict__, 'arg':self.variableNameMap[node.arg]})
        else:
            return node

    def visit_Attribute(self, node):
        #node.attr - statename
        #node.value.slice.value = node number
        #node.value.value.name.id = 'node'
        if node.value.value.id =='node':
            nname = f"node[{node.value.slice.value}].{node.attr}"
            if nname in self.variableNameMap: 
                svar = self.variableNameMap[nname]
                svi = svar.index('[')
                if svi>0:
                    sve = svar.index(']')
                    return ast.Subscript(
                        value=ast.Name(id=svar[:svi], ctx=ast.Load()),
                        slice=ast.Constant(value=int(svar[svi+1:sve])),
                        ctx=node.ctx
                    )
        
        return node

    def visit_Name(self, node):
        if node.id in self.variableNameMap: 
            return ast.Name(**{**node.__dict__, 'id':self.variableNameMap[node.id]})
        else:
            return node

def loadTemplateFile(filename):
    """Load template files stored as resources within ftuutils package"""
    resourcefiles = importlib.resources.files("ftuutils")
    with open(os.path.join(resourcefiles,"templates",filename),'r') as tf:
        return tf.read()
        
class SimulationExperiment():
    """Main logic class to load generated pythonic code and create experiments by 
       defining the inputs that each experiment elicits.
       Requires a resolved FTU through the composistionutils.Composer class instance
    """
    def __init__(self,composer) -> None:
        if isinstance(composer,str):
            self.composer = None
            ftucode = composer            
        else:
            self.composer = composer
            ftucode = composer.exportAsODEStepper()
        self.inputhook = None
        self.hamletcode = None
        self.experiments = dict()            
        self.ftusrccode = ftucode
        code = ast.parse(ftucode)
        for node in code.body:
            if isinstance(node, ast.ClassDef):
                if node.name.endswith("Hooks"):
                    self.inputhook = ast.unparse(node)
                    self.modelname = node.name[:-5]
                elif node.name.endswith("Inputs"):
                    self.hamletcode = ast.unparse(node)
                elif self.inputhook is not None and self.hamletcode is not None:
                    break
                
        self.ftulogic = ast.unparse(ExtractFTUDefinition().visit(code))
        
        #load classes
        code = f"{self.inputhook}\nself.inputhookInstance={self.modelname}Hooks()\n"
        exec(compile(code,'','exec'))
        
        code = f"{self.hamletcode}\nself.hamletNodes={self.modelname}Inputs.nodes\n"
        exec(compile(code,'','exec'))

        for k,v in self.inputhookInstance.statehooks.items():
            for sn,sm in v.items():
                self.inputhookInstance.inputhooks[f"node[{k}].{sn}"] = sm
        self.variablemap = self.inputhookInstance.inputhooks
        
        self.statenamehooks = self.inputhookInstance.statenamehooks
        self.phsnamehooks = self.inputhookInstance.phsnamehooks

    def addExperiment(self,name,time,inputblock,preamble=""):
        """Add an experiment for simulation

        Args:
            name (string): Name of the experiment
            time (list): Simulation time block associated with the experiment [start,end, [numsteps]]
            inputblock (string): Python code that will be executed to generate input signals for FTU simulation
            preamble (str, optional): Any preamble python code that will be added to start of the generated code; ideally used to import packages that are used by the input block. Defaults to "".

        Raises:
            Exception: time or inputblock do not conform to requirements
        """
        if len(time) < 2:
            raise Exception(f"experiment times should have a start and stop, given {time}")
        isplit = inputblock.strip().split('\n')
        if "return " in isplit[-1]:
            raise Exception(f"inputblock code should not return, rather assign to input variables!")
        
        self.experiments[name] = {'time':time,'process_time_sensitive_events':inputblock,'preamble':preamble}

    def generate(self,targetDir,provenance={},defaultnetworkid=1):
        """Generate code for the experiments and store them in the target directory
           Use the provenance information to decorate the code and results
        Args:
            targetDir (str): Target location for saving generated experimental code
            provenance (dict, optional): Provenace information like author, project etc to be saved with the experiment metadata. Defaults to {}.
            defaultnetworkid (int, optional): Network based on which Discrete Exterior Calculus operators should be generated. Defaults to 1.
        """
        os.makedirs(targetDir,exist_ok=True)
        #Create Data directory
        os.makedirs(os.path.join(targetDir,"data"),exist_ok=True)
        refactor = Refactor(self.variablemap)
        provenanceBlock = dict()
        if len(provenance)>0:
            provenanceBlock["provenance"] = provenance
        else:
            provenanceBlock["provenance"] = {"Project":targetDir,"Author":"FTU Simulation utils"}
        provenanceBlock["provenance"]["Timestamp"] = datetime.datetime.now().isoformat(sep=" ", timespec="minutes")
        provenanceBlock["datadirectory"] = os.path.join(targetDir,"data")
        provenanceBlock["sourcemodel"] = self.modelname
        for k,v in self.experiments.items():
            #Process time block- start, end [numsteps/stepsize]
            tblock = v['time']
            tstart = tblock[0]
            tend = tblock[1]
            numsteps = int(tend-tstart)
            if len(tblock)>2:
                stepsize = tblock[2]
                if stepsize < 1.0:
                    numsteps = int(numsteps/stepsize)
                else:
                    numsteps = stepsize
            
            #Process the input code block to 
            eventCodex = ast.unparse(refactor.visit(ast.parse(v['process_time_sensitive_events']))).strip()            
            cx = eventCodex.split('\n')
            #Indentation should match that of 'process_time_sensitive_events' function def
            indent = "        "
            if eventCodex.startswith("def"):
               cx = cx[1:]
               indent = "    "
            eventCode = "" 
            for c in cx:
                eventCode += f"{indent}{c}\n"
                
            code = v['preamble']
            if len(code)>0:
                code +='\n'
            code += "import time\n"
            code += f"{self.ftulogic}\n"
            code += f'''
class {self.modelname}_{k}({self.modelname}):
    """
    Machine generated code for running experiment {k} with 
    time {v['time']}
    and inputcode block
    {v['process_time_sensitive_events']}
    """
    def __init__(self) -> None:
        super().__init__()
        self.cellHam = np.zeros(self.CELL_COUNT)
        self.energyInputs = np.zeros(self.CELL_COUNT)
        self.totalEnergyInputs = np.zeros(self.CELL_COUNT)
        self.inputs = np.zeros(self.STATE_COUNT)
        self.times     = []
        self.allstates = []
        self.allrates  = []
        self.allhamiltonians = []
        self.allenergyinputs = []
        self.alltotalenergyinputs = []                
        self.allinputs = []


    def process_time_sensitive_events(self,voi):
        t = voi
        states, rates, variables = self.states,self.rates,self.variables
        #Refactored code to match variable to array maps
{eventCode}
        #End of refactored code
        self.compute_variables(voi)
        
    def process_events(self,voi):
        self.times.append(self.time)
        self.allstates.append(np.copy(self.states))
        self.allrates.append(np.copy(self.rates))
        self.compute_hamiltonian(self.cellHam)
        self.allhamiltonians.append(np.copy(self.cellHam))
        self.compute_external_energy(self.energyInputs)
        self.allenergyinputs.append(np.copy(self.energyInputs))
        self.compute_total_input_energy(self.totalEnergyInputs)
        self.alltotalenergyinputs.append(np.copy(self.totalEnergyInputs))
        self.compute_inputs(self.time,self.inputs)
        self.allinputs.append(np.copy(self.inputs))
                
    def run(self):
        try:
            print(f"Starting experiment {self.modelname} {k} - time steps {tstart},{tend},{numsteps}")
            voi = np.linspace({tstart},{tend},{numsteps})
            if self.time>{tstart}:
                self.time = {tstart}
                self.odeintegrator.set_initial_value(self.states, self.time)
            tic = time.time()
            for t in voi[1:]:
                self.step(t)
            toc = time.time()
            print(f"Completed experiment {self.modelname} {k} in {{(toc-tic):4f}} seconds")
        except Exception as ex:
            print(f"Failed experiment {self.modelname} {k} with {{ex}}")
            
    def save(self,filename):
        with open(filename,'wb+') as sv:
            np.save(sv,np.array(self.times))
            # tranpose to get it in states x time
            np.save(sv,np.array(self.allstates).T) 
            np.save(sv,np.array(self.allrates).T)
            np.save(sv,np.array(self.allhamiltonians).T)
            np.save(sv,np.array(self.allenergyinputs).T)
            np.save(sv,np.array(self.alltotalenergyinputs).T)
            np.save(sv,np.array(self.allinputs).T)
            
if __name__ == '__main__':            
    fstep = {self.modelname}_{k}()
    fstep.run()
    import matplotlib.pyplot as plt

    t = np.array(fstep.times)
    states = np.array(fstep.allstates)
    fig = plt.figure(figsize=(50, 50))
    grid = plt.GridSpec((fstep.CELL_COUNT+1)//3, 3, wspace=0.2, hspace=0.5)

    ix = 0
    numstates = len(fstep.stateIndexes)
    for i in range((fstep.CELL_COUNT+1)//3):
        for j in range(3):
            ax = plt.subplot(grid[i, j])
            ax.plot(t,states[:,ix+2])
            ax.title.set_text(f'{{ix//numstates+1}}')
            ix += numstates
            if ix+numstates > states.shape[1]:
                break
    plt.subplots_adjust(hspace=0.3)
    plt.subplots_adjust(wspace=0.3)
    fig.savefig(f"{self.modelname}_{k}_results.png",dpi=300)
    plt.show()             
'''
            with open(os.path.join(targetDir,f"{self.modelname}_{k}.py"),'w') as spy:
                print(code,file=spy)            
            provenanceBlock[k] = {"simulationtimeblock":v['time'],
                                  "processeventsblock":v['process_time_sensitive_events'],
                                  "code":os.path.join(targetDir,f"{self.modelname}_{k}.py"),
                                  "codepreamble": v['preamble']
                                  }
            
        with open(os.path.join(targetDir,f"experimentdesign.json"),'w') as jpy:
            json.dump(provenanceBlock,fp=jpy)
            
        with open(os.path.join(targetDir,f"{self.modelname}.py"),'w') as cpy:
            print(self.ftusrccode,file=cpy)
            
        #Create runners
        pysrdir = os.path.join(targetDir,"pysrcodes")
        os.makedirs(pysrdir,exist_ok=True)
        torchcodedir = os.path.join(targetDir,"pytorchcodes")
        os.makedirs(torchcodedir,exist_ok=True)
        modelzoodir = os.path.join(targetDir,"modelzoo")
        os.makedirs(modelzoodir,exist_ok=True)
        
        
        try:
            #Load and store the simrunner
            simr = loadTemplateFile('runsimulations.pyt')
            with open(os.path.join(targetDir,f"runsimulations.py"),'w') as sim:
                print(simr,file=sim)
            #Genarate Hamlets for the nodes
            hamlet = loadTemplateFile('hamlettemplate.pyt')
            statevectorsize = 0
            for v in self.statenamehooks.values():
                statevectorsize += len(v)
            for innode in self.hamletNodes:
                numstates = len(innode['states'])
                statenames = [None]*numstates
                stateiv = [None]*numstates
                for k,v in innode['states'].items():
                    statenames[v['order']] = k
                    stateiv[v['order']] = v['value']
                statenameString = ','.join([f'"{sn}"' for sn in statenames])
                stateinitcode   = ','.join(stateiv)
                 
                varmapcode = ','.join(statenames)+'= self.states\n'
                if len(innode['inputs'])>1:
                    varmapcode += '        '+','.join(innode['inputs'])+' = self.inputs\n'
                elif len(innode['inputs'])==1:
                    varmapcode += '        '+innode['inputs'][0]+' = self.inputs[0]\n'
                for k,v in innode['statevarmap'].items():
                    varmapcode += '        '+k+' = self.fomstates['+str(v)+']\n'
                hamcalccode = varmapcode+'\n        return '+innode['hamiltonian']
                e4extinpcode = varmapcode+'\n        totE = '+innode['hamiltonian']
                if len(innode['inputs'])>1:
                    zos = ','.join(["0.0"]*len(innode['inputs']))
                    e4extinpcode += '\n        '+','.join(innode['inputs'])+' = '+zos
                else:
                    e4extinpcode += '\n        '+innode['inputs'][0]+' = 0.0'
                e4extinpcode += '\n        E = '+innode['hamiltonian']
                e4extinpcode += '\n        return totE - E\n'
                computerhsode = varmapcode+'\n        self.rates = ['+',\n            '.join(innode['rhs'])+']'
                computerhsode +='\n        return self.rates\n'
                
                hamc = hamlet.replace('__Hamlet__',f"HamletForBoundaryNode{innode['nodelabel']}")
                hamc = hamc.replace('__NUM_STATES__',str(numstates)).replace('__TOTAL_STATES__',str(statevectorsize))
                hamc = hamc.replace('__CIX__',str(innode['hamiltonianIndex']))
                hamc = hamc.replace('__STATE_NAMES__',statenameString)
                hamc = hamc.replace('__INIT_STATES__',stateinitcode)
                hamc = hamc.replace('__GET_HAMILTONIAN__',hamcalccode)
                hamc = hamc.replace('__GET__ENERGYFROMEXTERNALINPUTS__',e4extinpcode)
                hamc = hamc.replace('__COMPUTE_RHS__',computerhsode)
                
                with open(os.path.join(modelzoodir,f"Hamlet4BN{innode['nodelabel']}.py"),"w") as hc:
                    print(hamc,file=hc)
                
            #TODO Move the following to databaseddiscoveryutils
            #Create and store state to hamiltonian map expression determination codes            
            smap = loadTemplateFile('state2hamiltoniansrmap.pyt')
            mlpsmap = loadTemplateFile('state2hamiltonianmlpmap.pyt')
            for k,v in self.statenamehooks.items():
                sfilename = f"FindHamiltonianTo_{k}_Map.py"
                #PySR
                kk = smap.replace("__HamiltonianToStateMap__",f"HamiltonianTo_{k}_Map").replace("__STATENAME__",k)
                kk = kk.replace("__STATEINDEXS__",f"np.array([{','.join(map(str,v))}])")
                kk = kk.replace("__DATADIRECTORY__",os.path.join(targetDir,"data")).replace("__MODEL_FILENAME__",os.path.join(modelzoodir,f"pysr{k}map.pkl"))
                with open(os.path.join(pysrdir,sfilename),'w') as smf:
                    print(kk,file=smf)
                # #MLP 
                mlpkk = mlpsmap.replace("__HamiltonianToStateMapDataset__",f"HamiltonianTo_{k}_MapDatasetLoader").replace("__STATENAME__",k)
                mlpkk = mlpkk.replace("__STATEINDEXS__",f"np.array([{','.join(map(str,v))}])")
                mlpkk = mlpkk.replace("__DATADIRECTORY__",os.path.join(targetDir,"data")).replace("__MODEL_PATHNAME__",os.path.join(modelzoodir,f"pytorch{k}map"))
                with open(os.path.join(torchcodedir,sfilename),'w') as mlsmf:
                    print(mlpkk,file=mlsmf)
                    
                    
            #Create the map for infering the relationship between states at t, t-1, inputenergy
            #Do for each PHS type
            hamfilemap = dict()
            hamfilemap["expressions"] = []
            for k,v in self.phsnamehooks.items():
                hmapfile = os.path.join(modelzoodir,f"pysr_ham_map_{k}.pkl")
                hmap = loadTemplateFile('hamsrexpression.pyt')
                hk = hmap.replace("__HamiltonianExpression__",f"HamiltonianExpressionForPHS_{k}")
                hk = hk.replace("__PHS_NAME__",k).replace("__PHS_INDEX__",','.join(map(str,v)))
                hk = hk.replace("__DATADIRECTORY__",os.path.join(targetDir,"data")).replace("__MODEL_FILENAME__",hmapfile)
                with open(os.path.join(pysrdir,f"FindExpressionFor_PHS_{k}_Hamiltonian.py"),'w') as hmf:
                    print(hk,file=hmf)
                
                hamfilemap["expressions"].append({"index":v,"file":hmapfile})
            
            with open(os.path.join(modelzoodir,"pysr_ham_map.json"),"w") as srm:
                json.dump(hamfilemap,srm)

            #Store DDECOpertor inference code
            #PySR
            ddecsr = loadTemplateFile('Neuman2DirichletSRDDEC.pyt')
            ddecsr = ddecsr.replace("__DATADIRECTORY__",os.path.join(targetDir,"data")).replace("__MODEL_OUPUT__",os.path.join(modelzoodir,"DDECSR"))
            ddecsr = ddecsr.replace("__PYSRMAP__",os.path.join(modelzoodir,"pysr_ham_map.json"))
            ddecsr = ddecsr.replace("__OPERATOR_TEMPLATE__",os.path.join(targetDir,"operators.npy"))
            with open(os.path.join(pysrdir,f"Neuman2DirichletOp.py"),'w') as dec:
                print(ddecsr,file=dec)  
            #MLP
            ddecmlp = loadTemplateFile('Neuman2DirichletMLPDDEC.pyt')
            ddecmlp = ddecmlp.replace("__DATADIRECTORY__",os.path.join(targetDir,"data")).replace("__MODEL_OUPUT__",os.path.join(modelzoodir,"DDECMLP"))
            ddecmlp = ddecmlp.replace("__OPERATOR_TEMPLATE__",os.path.join(targetDir,"operators.npy"))
            with open(os.path.join(torchcodedir,f"Neuman2DirichletOp.py"),'w') as dec:
                print(ddecmlp,file=dec)                  

            nonmlp = loadTemplateFile('NeuralOp.pyt')
            nonmlp = nonmlp.replace("__OPERATOR_FILE__",os.path.join(modelzoodir,"DDECMLP","numpynonlinearoperator.npy"))
            with open(os.path.join(torchcodedir,f"NeuralOp.py"),'w') as dec:
                print(nonmlp,file=dec)                  
         
        except Exception as ex:
            print("Package must be installed for importlib.resources to work, try pip install -e .")
            raise ex        

        #Generate the operators
        if self.composer is not None:
            self.composer.saveDiscreteExteriorCalculusOperators(os.path.join(targetDir,f"operators.npy"),defaultnetworkid)
