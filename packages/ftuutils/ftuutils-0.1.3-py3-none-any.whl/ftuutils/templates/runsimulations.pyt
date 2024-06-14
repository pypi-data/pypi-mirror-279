import json, argparse, os
from multiprocessing import Pool
from functools import partial

import importlib.util

def runExperiment(pmodule,datadir):
    mname = os.path.splitext(os.path.basename(pmodule))[0]
    try:
        spec = importlib.util.spec_from_file_location(mname, pmodule)
        xmodule = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(xmodule)
        ftu_class = getattr(xmodule, mname) #Main class has the samename as filename
        ftu = ftu_class()
        ftu.run()
        ftu.save(os.path.join(datadir,f"{mname}.npy"))
    except Exception as ex:
        return {"success":False,"msg":str(ex),"module":mname}
    return {"success":True,"module":mname}

class ExperimentRunner():
    
    def __init__(self,experimentDir) -> None:
        self.experimentDir = experimentDir
        #Find experiment design file
        dirfiles = os.listdir(experimentDir)
        expdesign = None
        experiments = None
        experimentcodes = []

        for f in dirfiles:
            if f.endswith(".json"):
                with open(os.path.join(experimentDir,f),'r') as js:
                    jexp = json.load(js)
                    if "provenance" in jexp and "datadirectory" in jexp:
                        experiments = jexp
                        experimentcodes = []
                        for exp,v in experiments.items():    
                            if not exp in ["provenance","sourcemodel","datadirectory"]:
                                experimentcodes.append(v["code"])        
                        if len(experimentcodes)>0:                        
                            expdesign = f
                            break
                        
        if expdesign==None:
            raise Exception(f"{experimentDir} does not contains experiment design file!")
        self.experiments = experiments
        self.experimentcodes = experimentcodes
        self.datadir = experiments["datadirectory"]
        self.numprocesses = 4
        
    def setMaxProcesses(self,numProcs):
        self.numprocesses = numProcs
        
    def setDataDirectory(self,datadir):
        self.datadir = datadir
        
    def run(self):
        result = dict()
        psize = min(len(self.experimentcodes),self.numprocesses)
        print(f"Spawning {psize} simulations")
        with Pool(psize) as pool:
            N = pool.map_async(partial(runExperiment, datadir=self.datadir), self.experimentcodes)
            #N.wait()
            pool.close() #Wait for all processes to complete
            pool.join()
            for res in N.get():
                result[res["module"]] = res
        resfile = os.path.join(self.datadir,"runresults.json")
        with open(resfile,'w') as rr:
            json.dump(result,fp=rr)
        print(f"Completed all simulations, see {resfile} for details.")
            
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-j","--processes", type=int,default=4,
                        help="Maximum number of processes to spawn")
    parser.add_argument("-o", "--outputdir", 
                        help="directory in which simulation results are to be stored")
    args = parser.parse_args()
    
    runner = ExperimentRunner(os.path.dirname(os.path.realpath(__file__)))
    if args.processes:
        runner.setMaxProcesses(args.processes)
    if args.outputdir:
        os.makedirs(args.outputdir,exist_ok=True)
        runner.setDataDirectory(args.outputdir)
    
    runner.run()

