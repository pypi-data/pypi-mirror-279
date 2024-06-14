"""Logic to compose FTU from topology, PHS type and network connection information"""

import numpy as np
import sympy
from sympy import Expr, Matrix
import networkx as nx
import json
from collections import OrderedDict

from copy import deepcopy


composerSerializationEnabled = True
try:
    import cloudpickle
except:
    composerSerializationEnabled = False

from ftuutils import codegenerationutils
from ftuutils import latexgenerationutils

class SymbolicPHS:
    """
    Symbolic Port Hamiltonian representation
    """

    def __init__(
        self,
        J: Matrix,
        R: Matrix,
        B: Matrix,
        Bhat: Matrix,
        Q: Matrix,
        E: Matrix,
        C: Matrix,
        ham: Expr,
        s: Matrix,
        u: Matrix,
        usplit: Matrix,
        vars: set,
        parameters: dict,
        statevalues: dict,
    ) -> None:
        self.J = J
        self.R = R
        self.B = B  # If Bhat is non-zero then this is Bbar
        self.Bhat = Bhat
        self.Q = Q
        self.E = E
        self.C = C
        self.hamiltonian = ham
        self.states = s
        if isinstance(u, sympy.Matrix):
            self.u = u
        elif isinstance(u, sympy.Symbol):
            self.u = Matrix([[u]])
        elif isinstance(u, list):
            self.u = Matrix([u])
        else:
            raise (f"Type of input u for creating PHS instance not supported!")
        self.usplit = usplit
        self.variables = vars
        self.parameters = parameters
        self.statevalues = statevalues

    def getCopy(self, id: int):
        """Get a copy of the PHS instance with the symbol ids suffixed with id

        Args:
            id (int): Suffix id for PHS instance symbols

        Returns:
            SymbolicPHS: copy of instance
        """
        nvars = dict()

        for v in self.variables:
            nv = sympy.Symbol(f"{v.name}_{id}")
            nvars[v] = nv
        variables = set(nvars.values())
        parameters = dict()
        for k, v in self.parameters:
            parameters[k.xreplace(nvars)]["value"] = v["value"].xreplace(nvars)
        statevalues = dict()
        for k, v in self.statevalues:
            statevalues[k.xreplace(nvars)] = v["value"].xreplace(nvars)

        J = self.J.xreplace(nvars)
        R = self.R.xreplace(nvars)
        B = self.B.xreplace(nvars)

        Bhat = self.Bhat
        if self.Bhat is not None:
            Bhat = self.Bhat.xreplace(nvars)
        Q = self.Q.xreplace(nvars)
        E = self.E.xreplace(nvars)
        s = self.states.xreplace(nvars)
        u = self.u.xreplace(nvars)
        C = self.C
        if self.C is not None:
            C = self.C.xreplace(nvars)
        ham = self.hamiltonian.xreplace(nvars)

        return SymbolicPHS(
            J,
            R,
            B,
            Bhat,
            Q,
            E,
            C,
            ham,
            s,
            u,
            deepcopy(self.usplit),
            variables,
            parameters,
            statevalues,
        )

    def split(self, iosplit):
        """Split B matrix to suit the interior vs exterior IO elements
           The Bcap,Bbar entries are set to zero as the u's need to be weighted zero
           The row,column corresponding split(value True) dimensions are set to zero in Bcap (viceversa in Bbar)
        Args:
            iosplit (list): boolean array of dim u, bbar elements are true

        Returns:
            list: Bcap and Bbar/Bdash matrices
        """
        Bcap = deepcopy(self.B)
        Bbar = deepcopy(self.B)
        for i, v in enumerate(iosplit):
            if v:
                Bcap[i, :] *= 0
                Bcap[:, i] *= 0
            else:
                Bbar[i, :] *= 0
                Bbar[:, i] *= 0

        return [Bcap, Bbar]

    @staticmethod
    def getMatrix(mjson: dict) -> Matrix:
        """Get Sympy matrix from json description

        Args:
            mjson (dict): Matrix/Vector described as dictionary

        Returns:
            Matrix: Sympy Matrix
        """
        nrows = mjson["rows"]
        ncols = mjson["cols"]
        return Matrix(list(map(sympy.parse_expr, mjson["elements"]))).reshape(
            nrows, ncols
        )

    @staticmethod
    def getJSONForMatrix(matrix) -> dict:
        """Convert Sympy Matrix to json

        Args:
            matrix (Sympy.Matrix): Sympy Matrix for conversion

        Returns:
            dict: Jsonable representation of sympy matrix
        """
        rows = matrix.rows
        cols = matrix.cols
        elements = []
        for i in range(rows):
            for j in range(cols):
                elements.append(sympy.latex(matrix[i, j]))
        mjson = dict()
        mjson["rows"] = rows
        mjson["cols"] = cols
        mjson["elements"] = elements
        return mjson

    @staticmethod
    def getVariables(elem: list) -> set:
        """Convert from string to sympy varibales

        Args:
            elem (list): List of variables/expressions from which symbolic variable names need to be extracted 

        Raises:
            Exception: When a list element cannot be parsed

        Returns:
            set: Set of variables extracted from the input list
        """
        if type(elem) is list:
            exps = list(map(sympy.parse_expr, elem))
            res = set()
            for e in exps:
                res = res.union(e.free_symbols)
            return res
        elif type(elem) is str:
            ee = sympy.parse_expr(elem)
            return ee.free_symbols
        else:
            raise Exception(f"Input of Type {type(elem)} not supported by getVariables")

    @staticmethod
    def savePHSDefinition(phs):
        """Serialize the phs into json format

        Args:
            phs (SymbolicPHS): Target PHS object to be serialised

        Returns:
            dict: JSONable dict of the input PHS
        """
        states = {"rows": len(phs.states), "cols": "1", "elements": phs.states}
        hamexp = sympy.latex(phs.hamiltonian)
        hamitonian = sympy.pretty(phs.hamiltonian)
        matJ = SymbolicPHS.getJSONForMatrix(phs.J)
        matR = SymbolicPHS.getJSONForMatrix(phs.R)
        matB = SymbolicPHS.getJSONForMatrix(phs.B)
        matBhat = {"rows": 0, "cols": 0, "elements": []}
        if phs.Bhat is not None:
            matBhat = SymbolicPHS.getJSONForMatrix(phs.Bhat)
        matE = SymbolicPHS.getJSONForMatrix(phs.E)
        matQ = SymbolicPHS.getJSONForMatrix(phs.Q)
        matC = {"rows": 0, "cols": 0, "elements": []}
        if phs.C is not None:
            matC = SymbolicPHS.getJSONForMatrix(phs.C)

        uvec = SymbolicPHS.getJSONForMatrix(phs.u)
        usplit = SymbolicPHS.getJSONForMatrix(phs.usplit)
        uspx = usplit["elements"]
        for ix, y in enumerate(uspx):
            if y == "0":
                usplit["elements"][ix] = False
            else:
                usplit["elements"][ix] = True

        parameters = dict()
        for k, v in phs.parameters.items():
            parameters[sympy.pretty(k)] = {
                "value": sympy.pretty(v["value"]),
                "units": v["units"],
            }
        statevalues = dict()
        for k, v in phs.statevalues.items():
            statevalues[sympy.pretty(k)] = {
                "value": sympy.pretty(v["value"]),
                "units": v["units"],
            }

        result = dict()
        result["stateVector"] = states
        result["state_values"] = statevalues
        result["Hderivatives"] = {"rows": 0, "cols": 0, "elements": []}
        result["hamiltonianLatex"] = hamexp
        result["hamiltonian"] = hamitonian.replace("**", "^")
        phsm = dict()
        phsm["matR"] = matR
        phsm["matJ"] = matJ
        phsm["matB"] = matB
        phsm["matQ"] = matQ
        phsm["matE"] = matE
        phsm["matBhat"] = matBhat
        phsm["matC"] = matC
        phsm["u"] = uvec
        phsm["u_split"] = usplit
        result["portHamiltonianMatrices"] = phsm
        result["parameter_values"] = parameters

        return result

    @staticmethod
    def loadPHSDefinition(phs,prefix=""):
        """
        Load a PHS definition (json format)
        """
        states = phs["stateVector"]
        # hamexp = phs["hamiltonianLatex"]
        hamexp = phs["hamiltonian"]
        pmat = phs["portHamiltonianMatrices"]
        matR = pmat["matR"]
        matJ = pmat["matJ"]
        matB = pmat["matB"]
        matQ = pmat["matQ"]
        matE = pmat["matE"]
        uvec = pmat["u"]
        usplit = pmat["u_split"]
        if "matBhat" in pmat:
            matBhat = pmat["matBhat"]
        else:
            matBhat = {"cols": 0, "elements": [], "rows": 2}
        if "matC" in pmat:
            matC = pmat["matC"]
        else:
            matC = {"cols": 0, "elements": [], "rows": 2}

        # Get all variables for renaming
        variables = set()
        variables = variables.union(
            SymbolicPHS.getVariables(states["elements"]))
        variables = variables.union(SymbolicPHS.getVariables(hamexp))
        variables = variables.union(SymbolicPHS.getVariables(matR["elements"]))
        variables = variables.union(SymbolicPHS.getVariables(matJ["elements"]))
        variables = variables.union(SymbolicPHS.getVariables(matB["elements"]))
        variables = variables.union(SymbolicPHS.getVariables(matQ["elements"]))
        variables = variables.union(SymbolicPHS.getVariables(matE["elements"]))
        variables = variables.union(SymbolicPHS.getVariables(uvec["elements"]))
        variables = variables.union(
            SymbolicPHS.getVariables(matBhat["elements"]))
        variables = variables.union(SymbolicPHS.getVariables(matC["elements"]))
        #Get in the parameter names as well, some of them will be parameters to operators
        pset = []
        for k in phs["parameter_values"]:
            pset.append(sympy.Symbol(k))
        variables = variables.union(set(pset))
        if prefix=="":
            params = dict()
            for k, v in phs["parameter_values"].items():
                params[sympy.Symbol(k)] = {
                    "value": sympy.sympify(v["value"]),
                    "units": v["units"],
                }

            statevalues = dict()
            for k, v in phs["state_values"].items():
                statevalues[sympy.Symbol(k)] = {
                    "value": sympy.sympify(v["value"]),
                    "units": v["units"],
                }

            J = SymbolicPHS.getMatrix(matJ)
            R = SymbolicPHS.getMatrix(matR)
            B = SymbolicPHS.getMatrix(matB)

            if J.rows != B.rows:
                raise Exception(
                    "B does not have the same dimensions as the J matrix!!")

            Q = SymbolicPHS.getMatrix(matQ)
            E = SymbolicPHS.getMatrix(matE)
            u = SymbolicPHS.getMatrix(uvec)
            # if all elements are integers somethings break
            usp = usplit["elements"]
            for uix in range(len(usp)):
                if usp[uix] is None:
                    usp[uix] = 0
            us = Matrix(list(map(int, usp))).reshape(
                int(usplit["rows"]), int(usplit["cols"])
            )
            Bhat = SymbolicPHS.getMatrix(matBhat)
            C = SymbolicPHS.getMatrix(matC)
            s = SymbolicPHS.getMatrix(states)
            ham = sympy.parse_expr(hamexp)
        else:
            varsub = dict()
            for v in variables:
                varsub[v] = sympy.Symbol(f"{prefix}_{v}")            
            params = dict()
            for k, v in phs["parameter_values"].items():
                params[sympy.Symbol(f"{prefix}_{k}")] = {
                    "value": sympy.sympify(v["value"]).xreplace(varsub), #Make sure operators are updated as well
                    "units": v["units"],
                }

            statevalues = dict()
            for k, v in phs["state_values"].items():
                statevalues[sympy.Symbol(f"{prefix}_{k}")] = {
                    "value": sympy.sympify(v["value"]).xreplace(varsub), #Make sure operators are updated as well
                    "units": v["units"],
                }

            
            J = SymbolicPHS.getMatrix(matJ).xreplace(varsub)
            R = SymbolicPHS.getMatrix(matR).xreplace(varsub)
            B = SymbolicPHS.getMatrix(matB).xreplace(varsub)

            if J.rows != B.rows:
                raise Exception(
                    "B does not have the same dimensions as the J matrix!!")

            Q = SymbolicPHS.getMatrix(matQ).xreplace(varsub)
            E = SymbolicPHS.getMatrix(matE).xreplace(varsub)
            u = SymbolicPHS.getMatrix(uvec).xreplace(varsub)
            # if all elements are integers somethings break
            usp = usplit["elements"]
            for uix in range(len(usp)):
                if usp[uix] is None:
                    usp[uix] = 0
            us = Matrix(list(map(int, usp))).reshape(
                int(usplit["rows"]), int(usplit["cols"])
            )
            Bhat = SymbolicPHS.getMatrix(matBhat).xreplace(varsub)
            C = SymbolicPHS.getMatrix(matC)
            s = SymbolicPHS.getMatrix(states).xreplace(varsub)
            ham = sympy.parse_expr(hamexp).xreplace(varsub)
            variables = set(varsub.values())
            
        return SymbolicPHS(
            J, R, B, Bhat, Q, E, C, ham, s, u, us, variables, params, statevalues
        )

    def instantiatePHS(self, postfix, substituteParameters=False):
        """Create a PHS with given postfix for its symbols
           If substituteParameters is True, then symbols and expressions are evaluated with the cooresponding 
           numerical values and simplified.
        Args:
            postfix (string): Postfix for symbols
            substituteParameters (bool, optional): Substitute numerical values in experessions and simplify. Defaults to False.

        Returns:
            SymbolicPHS: Instance with new postfix and substituted expressions if requested.
        """
        vsubs = dict()
        definedSymbols = []
        for v in self.variables:
            vsubs[v] = sympy.Symbol(str(v) + "_" + postfix)
            definedSymbols.append(sympy.Symbol(str(v) + "_" + postfix))

        J = deepcopy(self.J).xreplace(vsubs)
        R = deepcopy(self.R).xreplace(vsubs)
        B = deepcopy(self.B).xreplace(vsubs)
        if self.Bhat is not None:
            Bhat = deepcopy(self.Bhat).xreplace(vsubs)
        else:
            Bhat = sympy.zeros(0, 0)

        Q = deepcopy(self.Q).xreplace(vsubs)
        E = deepcopy(self.E).xreplace(vsubs)
        if self.C is not None:
            C = deepcopy(self.C).xreplace(vsubs)
        else:
            C = sympy.zeros(0, 0)

        u = deepcopy(self.u).xreplace(vsubs)
        s = deepcopy(self.states).xreplace(vsubs)
        parms = dict()
        for k, v in self.parameters.items():
            nk = k.xreplace(vsubs)
            parms[nk] = deepcopy(v)
            parms[nk]["value"] = v["value"].xreplace(vsubs)
        statevalues = dict()
        for k, v in self.statevalues.items():
            nk = k.xreplace(vsubs)
            statevalues[nk] = deepcopy(v)
            statevalues[nk]["value"] = v["value"].xreplace(vsubs)

        us = deepcopy(self.usplit)
        ham = deepcopy(self.hamiltonian).xreplace(vsubs)
        if substituteParameters:
            subs = dict()
            for (k, v) in parms.items():
                if not v["value"].free_symbols:  # expression is numeric
                    subs[k] = v["value"]

            J = J.xreplace(subs)
            R = R.xreplace(subs)
            B = B.xreplace(subs)
            Bhat = Bhat.xreplace(subs)
            Q = Q.xreplace(subs)
            E = E.xreplace(subs)
            C = C.xreplace(subs)
            ham = ham.xreplace(subs)

        return SymbolicPHS(
            J, R, B, Bhat, Q, E, C, ham, s, u, us, definedSymbols, parms, statevalues
        )

    def __str__(self):
        """ Convert to string"""
        bbars = ""
        if self.Bhat.shape[0] > 0:
            bbars = f"Bhat Matrix\n {sympy.pretty(self.Bhat)}"
        cmats = ""
        if self.C.shape[0] > 0:
            cmats = f"Bhat Matrix\n {sympy.pretty(self.C)}"

        res = f""" Hamiltonian:\n {sympy.pretty(self.hamiltonian)}
State variables:\n {sympy.pretty(self.states)}\n
J Matrix\n {sympy.pretty(self.J)}
R Matrix\n {sympy.pretty(self.R)}
B Matrix\n {sympy.pretty(self.B)}
{bbars}
Q Matrix\n {sympy.pretty(self.Q)}
E Matrix\n {sympy.pretty(self.E)}
{cmats}
U Vector\n {sympy.pretty(self.u)}\n
Free variables : {sympy.pretty(self.variables)}
        """
        return res


class Composer:
    """
    Logic to compose a composite PHS, given the FTU graph, PHS information etc.
    """

    def __init__(self) -> None:
        self.nodeIndex = dict()
        self.nodeName = dict()
        self.nodeData = dict()
        self.phsInstances = dict()
        self.networkGraphs = dict()
        self.dissipativeNets = dict()
        self.boundaryinputs = dict()
        self.nodeNetworks = dict()
        self.networkNodes = dict()
        self.networkGraphs = dict()
        self.cellType = dict()
        self.cellTypePHS = dict()
        self.cellTypeUSplit = dict()

        self.boundaryInputSelection = []
        self.inodeIndexes = []

        self.compositeJ: Matrix = None
        self.compositeQ: Matrix = None
        self.compositeR: Matrix = None
        self.compositeE: Matrix = None
        self.compositeB: Matrix = None

        self.uyConnectionMatrix: Matrix = None
        self.uyConnectionMatrixComputed = (
            False  # Will be set to true if it was computed by compose
        )
        self.composition = None #Store composition information if used to construct the composer

    def setConnectivityGraph(self,graph:nx.Graph):
        """Set the base ftugraph from which the composition was created

        Args:
            graph (FTUGraph): Graph that stores the connectivity and edge
        """
        self.ftugraph = graph
        
    @staticmethod
    def getMatrix(mjson: dict) -> Matrix:
        """Get Sympy matrix from json description"""
        return SymbolicPHS.getMatrix(mjson)

    @staticmethod
    def getVariables(elem: list) -> set:
        """Convert from string to sympy varibales"""
        return SymbolicPHS.getVariables(elem)

    @staticmethod
    def _elementwiseDiv(A: Matrix, B: Matrix):
        """Perform elementwise division of sympy given matrices"""
        if A.shape[0] == B.shape[0] and A.shape[1] == B.shape[1]:
            C = deepcopy(A)
            for i in range(A.rows):
                for j in range(B.rows):
                    C[i, j] = sympy.simplify(A[i, j] / B[i, j])
            return C
        else:
            raise ("Matrix dimensions do not match!")

    @staticmethod
    def save(composition, filename):
        """Save the given composition as a pickle

        Args:
            composition (Composer): The composer instance to be saved
            filename (string): Path of the pickle file
        """
        if composerSerializationEnabled:
            with open(filename, "wb") as ser:
                cloudpickle.dump(composition, ser)
        else:
            raise (
                "Serialization not supported on this platform. Failed to load module cloudpickle!"
            )

    @staticmethod
    def load(filename):
        """Load the composition in a pickle

        Args:
            filename (string): Path of the pickle file
        """
        if composerSerializationEnabled:
            with open(filename, "rb") as ser:
                composition = cloudpickle.load(ser)
                return composition
        else:
            raise (
                "Serialization not supported on this platform. Failed to load module cloudpickle!"
            )

    def loadPHSDefinition(self, mapid, phs,useprefix):
        """
        Load a PHS definition (json format)
        The PHS object is assigned the id `mapid` to be used by mapid based composition
        """
        if useprefix:
            self.phsInstances[mapid] = SymbolicPHS.loadPHSDefinition(phs,mapid)
        else:
            self.phsInstances[mapid] = SymbolicPHS.loadPHSDefinition(phs)

    def loadComposition(self, composition: dict):
        """Load the FTU composition encoded in jsonable dict

        Args:
            composition (dict): FTU composition description
        """
        self.inodeIndexes = []
        self.nodeData = dict()
        self.phsInstances = dict()
        self.cellType = dict()
        self.cellTypePHS = dict()
        self.boundaryinputs = dict()
        self.compositeparameters = dict()

        # Load phs data
        phsdata = composition["graph"]["phsdata"]
        useprefixforPHS = len(phsdata) > 1
        for k, v in phsdata.items():
            self.loadPHSDefinition(k, v["phs"]["phs"],useprefixforPHS)

        # Create a graph
        gnodes = composition["graph"]["graph"]["nodes"]
        # Edges use node id's which is different from node labels
        # node labels may not be contigous, so iterate and find max node
        labelmapid = dict()
        # Structures to map inputs
        nodeNetworks = dict()
        networkNodes = (
            dict()
        )  # Will link both src and target nodes,one of which will be on the boundary

        maxlabel = 0
        labelnodeindex = dict()
        for nix, g in enumerate(gnodes):
            id = int(f"{g['id']}")
            label = int(f'{g["value"]["label"]}')

            if maxlabel < label:
                maxlabel = label

            labelmapid[id] = label
            if "phs" in g["value"]:
                self.cellTypePHS[label] = g["value"]["phs"]

            # Interior or boundary node
            if g["value"]["type"] == "in":
                self.cellType[label] = 1
                self.inodeIndexes.append(label)
            else:
                self.cellType[label] = 0
            labelnodeindex[label] = nix

        self.inodeIndexes.sort()
        # Load network data to help setup laplacian
        dissipativeNets = dict()

        networkDataS = composition["graph"]["networkdata"]
        networkkeys = []
        networkData = dict()
        for k in networkDataS.keys():
            networkkeys.append(int(k))
            networkData[int(k)] = networkDataS[k]

        networkkeys.sort()
        networkkeys.reverse()

        for k, v in networkData.items():
            dissipativeNets[k] = False
            if type(v) is str:
                vj = json.loads(v)
                if "isdissipative" in vj:
                    dissipativeNets[k] = vj["isdissipative"]
            else:
                if "isdissipative" in v:
                    dissipativeNets[k] = v["isdissipative"]

        gedges = composition["graph"]["graph"]["edges"]
        # For each network create a graph
        networkGraphs = dict()
        for networkNames, v in networkData.items():
            networkName = int(f"{networkNames}")
            ngraph = nx.DiGraph()
            ngraph.add_nodes_from(list(range(maxlabel)))
            networkNodes[networkName] = []
            for g in gedges:
                src = int(f"{g['source']}")
                trg = int(f"{g['target']}")
                weight = g["value"]["weight"]
                for ks, vw in weight.items():
                    k = int(
                        f"{ks}"
                    )  # Done this way as json serialisation changes keys to string
                    if k == networkName:
                        if src in nodeNetworks:
                            nodeNetworks[src][networkName] = vw
                        else:
                            nodeNetworks[src] = {networkName: vw}

                        if trg in nodeNetworks:
                            nodeNetworks[trg][networkName] = vw
                        else:
                            nodeNetworks[trg] = {networkName: vw}

                        networkNodes[networkName].append(src)
                        networkNodes[networkName].append(trg)

                        uniquenetworkNodes = set(networkNodes[networkName])
                        networkNodes[networkName] = list(uniquenetworkNodes)

                        if networkName in dissipativeNets:
                            if dissipativeNets[
                                networkName
                            ]:  # If dissipative add edge to compute laplacian
                                ngraph.add_edge(src, trg, weight=vw)

            networkGraphs[networkName] = ngraph

        networkBoundaryNodeMap = dict()
        for l, v in self.cellType.items():
            if v == 0:
                nts = list(nodeNetworks[l].keys())
                if len(nts) == 1:
                    networkBoundaryNodeMap[nts[0]] = l
                else:
                    raise (
                        f"Boundary node {l} has been assigned more than one networks - {nts}!"
                    )

        uVec = []
        for k in networkkeys:
            net = networkData[k]
            if net["type"] == "boundary":  # Should use boundary property
                nname = k
                if "input" in net:
                    input = net["input"]
                    phsc = self.phsInstances[input["phsclass"]]
                    comps = []
                    cindx = []
                    dindx = []
                    for i, v in enumerate(input["components"]):
                        if v:
                            # Encode the node from which input will be obtained. Note that laplacian and adjacency matrix will use different numbers than node label
                            # so map into labelnodeindex
                            # f"{phsc.u[i]}_{labelnodeindex[networkBoundaryNodeMap[f'{k}']]}" #f"{phsc.u[i]}{-k}" if k < 0 else f"{phsc.u[i]}{k}"
                            usym = f"{phsc.u[i]}_{k if k>0 else -k}"
                            uVec.append(Matrix([usym, i]))
                            comps.append(sympy.Symbol(usym))
                            cindx.append(i)
                            dindx.append(dissipativeNets[nname])

                    for nds in networkNodes[nname]:
                        if not nds in self.boundaryinputs:
                            self.boundaryinputs[nds] = [[], [], []]
                        self.boundaryinputs[nds][0].extend(comps)
                        self.boundaryinputs[nds][1].extend(cindx)
                        self.boundaryinputs[nds][2].extend(dindx)
                        uix = [
                            self.boundaryinputs[nds][0].index(x)
                            for x in set(self.boundaryinputs[nds][0])
                        ]
                        ncmps = [self.boundaryinputs[nds][0][ix] for ix in uix]
                        ncidx = [self.boundaryinputs[nds][1][ix] for ix in uix]
                        ndidx = [self.boundaryinputs[nds][2][ix] for ix in uix]
                        self.boundaryinputs[nds][0] = ncmps
                        self.boundaryinputs[nds][1] = ncidx
                        self.boundaryinputs[nds][2] = ndidx

        # Load Bcap information
        bcapdata = composition["composition"]["Bcap"]
        for k, v in bcapdata.items():
            nl = int(k)
            # Contains, bsplit, bbarcontrib, boundary nodes if any
            self.nodeData[nl] = v

        self.dissipativeNets = dissipativeNets
        self.nodeNetworks = nodeNetworks
        self.networkNodes = networkNodes
        self.networkGraphs = networkGraphs
        self.uVec = (
            Matrix(uVec).reshape(len(uVec), 2).T
        )  # Row 1 are input symbols, row 2 are column indexes into B matrix
        self.uyConnectionMatrixComputed = False
        self.composition = composition

    def getSourceComposition(self):
        """
            Return the source composition json that was used to defined the composer
            Returns None if json was not used
        """
        return self.composition

    def compose(self, substituteParameters=True):
        """
        Create the composite PHS matrices for compostion description that has been loaded
        Requires the phs for the different cell types to be loaded see loadPHSDefinition, loadCellTypePHSMap
        Requires the phs interconnection to be loaded see loadCompositionFile
        Ideally all interconnection u's and y's to be of the same size, if some phs have more u's,
        then select the ones that need to be used in the interconnection see setCellTypeUSplit
        """
        # calculate matrix dimensions
        jmat = []
        qmat = []
        emat = []
        rmat = []
        bcapmat = []
        nbcapmat = []
        lashmat = []
        bdasmat = []
        lashzeroflag = []
        jrsize = 0
        jcsize = 0
        brsize = 0
        bcsize = 0
        networkLap = dict()
        networkAdj = dict()
        for n, g in self.networkGraphs.items():
            networkLap[n] = nx.laplacian_matrix(g.to_undirected()).todense()
            # Construct node connectivity matrix, should be consistent with KCL
            nadj = np.zeros((g.number_of_nodes(), g.number_of_nodes()))
            for nd, nbrdict in g.adjacency():
                nadj[
                    nd, nd
                ] = (
                    -1
                )  # -len(nbrdict) # src (-1) -> target (+1) , not using in-degree as src is associated with a quantity
                for ni, wtd in nbrdict.items():
                    nadj[nd, ni] = +1
            networkAdj[n] = nadj

        hamiltonian = None
        ucapVec = []
        ycapVec = []
        ucapVectm1 = []  # At t-1
        ycapVectm1 = []  # At t-1
        stateVec = []
        rhsvec = []
        nodePHS = dict()
        statevalues = dict()

        self.cellHamiltonians = OrderedDict() #Ensure insertion order is maintained
        self.nodePHSData = dict()
        for k in self.inodeIndexes:
            v = self.nodeData[k]
            phs = self.phsInstances[self.cellTypePHS[k]].instantiatePHS(
                f"{k}", substituteParameters
            )
            self.nodePHSData[k] = phs #Used for generating input hooks
            statevalues.update(phs.statevalues)
            nodePHS[k] = phs
            self.compositeparameters.update(phs.parameters)
            r, c = phs.J.shape
            jrsize += r
            jcsize += c
            r, c = phs.B.shape
            brsize += r
            bcsize += c
            if hamiltonian is not None:
                hamiltonian = sympy.Add(hamiltonian, phs.hamiltonian)
            else:
                hamiltonian = phs.hamiltonian
            self.cellHamiltonians[k] = phs
            
            jmat.append(phs.J)
            qmat.append(phs.Q)
            emat.append(phs.E)
            rmat.append(phs.R)
            for i in range(phs.u.rows):
                stateVec.append(f"{phs.states[i,0]}")
                # k in encoded in phs states
                rhsvec.append(f"Del(H_{phs.states[i,0]})")
                if not v["bsplit"][i]:
                    # k in encoded in u during instantiation
                    usym = f"{phs.u[i,0]}_{i}"
                    ysym = "y" + usym[1:]

                    ucapVec.append(sympy.Symbol(usym))
                    ycapVec.append(sympy.Symbol(ysym))
                    ucapVectm1.append(sympy.sympify(usym + "(t-1)"))
                    ycapVectm1.append(sympy.sympify(ysym + "(t-1)"))
                else:
                    ucapVec.append(sympy.Symbol("0"))
                    ycapVec.append(sympy.Symbol("0"))
                    ucapVectm1.append(sympy.Symbol("0"))
                    ycapVectm1.append(sympy.Symbol("0"))

            bcap, bdas = phs.split(v["bsplit"])
            # Unlike the paper, C matrix is a real matrix and not connectivity matrix, therefore 
            # Metric contributions from bcap is determined by C matrix
            # Only active/inactive contribution from component 
            # information is necessary - set all non zero entries in Bcap to 1
            for ix in range(bcap.shape[0]):
                for iy in range(bcap.shape[1]):
                    if bcap[ix, iy] != 0:
                        bcap[ix, iy] = 1  # sympy.Symbol("1")

            # Include composite's Bhat to bcap
            if (
                phs.Bhat.shape[0] == bcap.shape[0]
                and phs.Bhat.shape[1] == bcap.shape[1]
            ):
                # Set the Bhat's nonzeros to bcap
                for i in range(phs.Bhat.shape[0]):
                    for j in range(phs.Bhat.shape[1]):
                        if not sympy.is_zero(phs.Bhat[i, j]):
                            bcap[i, j] = phs.Bhat[i, j]
            elif phs.Bhat.shape[0] != 0 and phs.Bhat.shape[1] != 0:
                raise ("Composite PHS Bhat and Bcap are not of the same shape!")

            bcapmat.append(
                bcap
            )  # Since C is scaled by E, Bcap does not need to be scaled interior u = B C B^T Q x
            nbcapmat.append((-bcap).T)
            # The dimensions need to match the JMatrix as Bdash*udash is summed with (J-R) Q x
            bash = sympy.zeros(phs.B.shape[0], self.uVec.shape[1])
            lash = sympy.zeros(phs.B.shape[0], self.uVec.shape[1])  # laplacian

            # boundaryinputs has the inputs that the nodes receives
            # boundaryinputs[k][0] - component names
            # boundaryinputs[k][1] - name index into u vector
            # boundaryinputs[k][2] - network is dissipative or not

            lashupdated = False
            if k in self.boundaryinputs:
                for (i, uin) in enumerate(self.boundaryinputs[k][0]):
                    comp = self.boundaryinputs[k][1][i]
                    # Subscript of uin contains the node to which k is connected
                    # prefix is given by phs.u[comp]
                    # if dissipative get the laplacian weight using k, uin_subscript
                    # us = Symbolics.variable(uin)
                    uix = -1
                    u_ix = -1  # Get the index in uVec
                    for j in range(self.uVec[0, :].cols):
                        if self.uVec[0, j] == uin:
                            uix = self.uVec[1, j]
                            u_ix = j
                            break
                    # uVec[1,:] has the names, uVec[2,:] has the component indexes

                    if self.boundaryinputs[k][2][i] == False:
                        bash[uix, u_ix] = phs.B[comp, comp]
                    else:
                        nid = f"{phs.usplit[comp]}"
                        if nid in self.dissipativeNets:  # If dissipative
                            # uin is the node that provides the input - the suffix provides the node id and the index into the lapacian/adjacency matrix
                            ulc = phs.u[comp]
                            ulc = str(phs.u[comp]).find("_")
                            suffix = int(str(uin)[ulc + 1:])
                            wt = networkLap[nid][k, suffix]
                            lash[comp, u_ix] = wt
                            lashupdated = True
                        else:  # Has input in bash
                            # Check uix and comp
                            bash[uix, u_ix] = phs.B[comp, comp]

            bdasmat.append(bash)
            lashmat.append(lash)
            lashzeroflag.append(lashupdated)
        # Set the vector elements in the correct order
        if self.uVec.cols > 1:
            self.uVecSymbols = self.uVec[0, self.uVec[1, :]]
        else:
            # When there is a single input symbol
            self.uVecSymbols = Matrix([self.uVec[0]])
        self.stateVec = stateVec
        self.statevalues = statevalues
        self.rhsVec = rhsvec
        self.xVec = Matrix.vstack(
            Matrix(stateVec), Matrix(ucapVec), Matrix(ycapVec))
        self.rVec = Matrix.vstack(
            Matrix(rhsvec), Matrix(ucapVectm1), Matrix(ycapVectm1)
        )
        self.hamiltonian = hamiltonian
        """
            Create full connection matrix - get the asymmetric part for C and the other for R

            Dissipative networks are expected to solve Reaction diffusion equations of the form

            dx/dt = phs(x) + ∇x , where ∇x is the diffusive contributions computed from the weighted graph laplacian

            When the PHS is of the form

            E dx/dt = (J-R)Qx + Bu then the above equation requires a scaling factor for the ∇x term

            E dx/dt = phs(x) + E ∇x

            all terms of the lapacian matrix for the component are scaled by E
        """
        Cx = sympy.zeros(brsize, bcsize)
        roffset = 0
        for (i, b) in enumerate(self.inodeIndexes):
            # phs = self.phsInstances[self.cellTypePHS[b]]
            phs = nodePHS[b]
            # Emat = phs.E
            usplit = phs.usplit
            if phs.C.shape[0] != 0 and phs.C.shape[1] != 0:
                # Scaling by compostite's E done at the time of construction
                Cx[
                    roffset: roffset + phs.C.shape[0],
                    coffset: coffset + phs.C.shape[1],
                ] = phs.C

            for (j, n) in enumerate(usplit):
                nid = n
                if (
                    nid in networkAdj
                ):  # if u has zeros, networks for them will not be present
                    lap = networkAdj[nid]
                    if self.dissipativeNets[nid]:
                        lap = networkLap[nid]
                    coffset = 0
                    for (k, x) in enumerate(self.inodeIndexes):
                        phsx = nodePHS[x]
                        lc = phsx.B.shape[1]
                        if self.dissipativeNets[nid]:
                            try:
                                Cx[roffset + j, coffset + j] = lap[b, x]
                            except:  # DomainError
                                continue
                        else:
                            # Setting up a symmetrix matrix for connection
                            if k > i:
                                try:
                                    Cx[roffset + j, coffset + j] = lap[b, x]
                                    Cx[coffset + j, roffset + j] = -lap[b, x]
                                except:  # DomainError
                                    continue
                            elif k == i:
                                try:
                                    Cx[roffset + j, coffset + j] = lap[b, x]
                                except:  # DomainError
                                    continue
                        coffset += lc
            roffset += phs.B.shape[0]

        self.uyConnectionMatrix = Cx

        sym = (Cx + Cx.T) / 2
        skewsym = (Cx - Cx.T) / -2  # We need -C
        self.uyConnectionMatrixComputed = True

        # calculate the full matrix size
        jr = 2 * jrsize + skewsym.shape[0]
        jc = 2 * jcsize + skewsym.shape[1]

        self.Jcap = sympy.zeros(jrsize, jcsize)
        self.Rcap = sympy.zeros(jrsize, jcsize)
        self.Ecap = sympy.zeros(jrsize, jcsize)
        self.Qcap = sympy.zeros(jrsize, jcsize)
        self.Bcap = sympy.zeros(jrsize, jcsize)
        self.nBcapT = sympy.zeros(jrsize, jcsize)
        self.Bdas = sympy.zeros(jrsize, self.uVec.shape[1])
        self.Cmatrix = skewsym
        self.Lmatrix = sym

        jr, jc = 0, 0
        for (i, jx) in enumerate(jmat):
            self.Jcap[jr: jr + jx.shape[0], jc: jc + jx.shape[1]] = jx
            self.Rcap[jr: jr + jx.shape[0], jc: jc + jx.shape[1]] = rmat[i]
            self.Ecap[jr: jr + jx.shape[0], jc: jc + jx.shape[1]] = emat[i]
            self.Qcap[jr: jr + jx.shape[0], jc: jc + jx.shape[1]] = qmat[i]
            self.Bcap[jr: jr + jx.shape[0], jc: jc + jx.shape[1]] = bcapmat[i]
            self.nBcapT[jr: jr + jx.shape[0],
                        jc: jc + jx.shape[1]] = nbcapmat[i]
            # if laplacian is nonzero then Bdas should be lashmat
            if not lashzeroflag[i]:
                self.Bdas[jr: jr + bdasmat[i].shape[0], :] = bdasmat[i]
            else:
                self.Bdas[jr: jr + bdasmat[i].shape[0], :] = lashmat[i]

            jr += jx.shape[0]
            jc += jx.shape[1]

        freevars = self.Jcap.free_symbols
        freevars = freevars.union(self.Rcap.free_symbols)
        freevars = freevars.union(self.Bcap.free_symbols)
        freevars = freevars.union(self.Bdas.free_symbols)
        freevars = freevars.union(self.Qcap.free_symbols)
        freevars = freevars.union(self.hamiltonian.free_symbols)
        freevars = freevars.union(self.uVecSymbols.free_symbols)

        for k, v in self.compositeparameters.items():
            freevars = freevars.union(k.free_symbols)
            freevars = freevars.union(v["value"].free_symbols)

        self.compositePHS = SymbolicPHS(
            self.Jcap,
            self.Rcap,
            self.Bcap,
            self.Bdas,
            self.Qcap,
            self.Ecap,
            self.uyConnectionMatrix,
            self.hamiltonian,
            stateVec,
            self.uVecSymbols,
            sympy.zeros(self.uVec.shape[0], 1),
            freevars,
            self.compositeparameters,
            self.statevalues,
        )

    def generateLatexReport(self):
        """Generate the latex describing the composite PHS

        Returns:
            string: HTML + Latex sting
        """
        if len(self.stateVec) < 11:
            return latexgenerationutils.generateLatex(self)
        else:
            return latexgenerationutils.generateImage(self)

    def generatePythonIntermediates(self):
        r"""Generate numerically solvable PHS
            d/dx (Ex) = (J-R) Q x - \hat{B}\hat{C}\hat{B}^T \hat{u} + \bar{B} \bar{u}
            \hat{y} = \hat{B}^T Q x
            \bar{y} = \bar{B}^T Q x
        """
        stateVec = Matrix(self.stateVec)
        ucapVec = Matrix([f"u_{s}" for s in self.stateVec])
        Ccap = self.uyConnectionMatrix
        Delx = self.Qcap * stateVec  # Potential
        # Since E^-1 can be expensive, we will scale by the rate diagonal value of E for that component
        Einv = sympy.eye(self.Ecap.shape[0])
        for i in range(self.Ecap.shape[0]):
            Einv[i, i] = 1 / self.Ecap[i, i]
        JRQx = (self.Jcap - self.Rcap) * Delx
        interioru = self.Bcap * Ccap * (self.Bcap.T) * ucapVec
        exterioru = self.Bdas * Matrix(self.uVecSymbols).T
        rhs = sympy.SparseMatrix(Einv * (JRQx - interioru + exterioru))
        inputs = sympy.SparseMatrix(Einv * (-interioru + exterioru))
        rhsfreesymbols = rhs.free_symbols
        rhsnumericconstants = []
        self.raw_rhs = deepcopy(rhs)
        for elem in rhs:
            if isinstance(elem, sympy.Expr):
                for tm in elem.args:
                    rhsnumericconstants.extend(
                        [
                            term
                            for term in tm.args
                            if term not in rhsfreesymbols
                            and isinstance(term, sympy.Number)
                            and np.fabs(float(term)) != 1.0
                        ]
                    )
            elif isinstance(elem, sympy.Number):
                if np.fabs(float(elem)) != 1.0:
                    rhsnumericconstants.append(elem)
        # Constants in uCapVec
        for i, s in enumerate(self.stateVec):
            elem = interioru[i]
            if isinstance(elem, sympy.Expr):
                for tm in elem.args:
                    rhsnumericconstants.extend(
                        [
                            term
                            for term in tm.args
                            if term not in rhsfreesymbols
                            and isinstance(term, sympy.Number)
                            and np.fabs(float(term)) != 1.0
                        ]
                    )
            elif isinstance(elem, sympy.Number):
                if np.fabs(float(elem)) != 1.0:
                    rhsnumericconstants.append(elem)

        constantsubs = dict()
        constCtr = 1
        for c in set(rhsnumericconstants):
            constantsubs[np.abs(c)] = f"c_{constCtr}"
            constCtr += 1

        # Remove constant entries that are same to given precision
        constCtr = 1
        constantstoprecision = dict()
        newkeys = dict()
        for k, v in constantsubs.items():
            pk = f"{float(k):6f}"
            if pk not in constantstoprecision:
                constantstoprecision[pk] = sympy.Symbol(f"c_{constCtr}")
                constCtr += 1
            newkeys[k] = constantstoprecision[pk]

        for k, v in newkeys.items():
            constantsubs[k] = v

        # Xreplace is faster than subs - no deep mathematical reasoning, ok for constant replacement
        cleanrhs = rhs.xreplace(constantsubs)
        cleaninputs = inputs.xreplace(constantsubs)

        # Generate python
        # Constants are contained in constantsubs, map and add all constants in compositeparameters that are used by functions in the composite parameters
        nonlinearrhsterms = dict()
        for c, t in self.compositeparameters.items():
            fs = t["value"].free_symbols
            cvdict = dict()
            if len(fs) > 0:
                # Load the values of composite parameter parameters
                for f in fs:
                    if f in self.compositeparameters:
                        if self.compositeparameters[f]["value"] in constantsubs:
                            cvdict[f] = constantsubs[
                                self.compositeparameters[f]["value"]
                            ]
                        elif (
                            np.fabs(
                                float(self.compositeparameters[f]["value"])) != 1.0
                        ):
                            cvdict[f] = sympy.Symbol(f"c_{constCtr}")
                            constantsubs[self.compositeparameters[f]["value"]] = cvdict[
                                f
                            ]
                            constCtr += 1
                nonlinearrhsterms[c] = t["value"].xreplace(cvdict)

        # Find all symbolic constants in nonlinearrhsterms
        for k, v in nonlinearrhsterms.items():
            fs = v.free_symbols
            cvdict = dict()
            for f in fs:
                if f in self.compositeparameters:
                    if self.compositeparameters[f]["value"] in constantsubs:
                        cvdict[f] = constantsubs[self.compositeparameters[f]["value"]]
                    elif np.fabs(float(self.compositeparameters[f]["value"])) != 1.0:
                        cvdict[f] = sympy.Symbol(f"c_{constCtr}")
                        constantsubs[self.compositeparameters[f]
                                     ["value"]] = cvdict[f]
                        constCtr += 1
            if len(cvdict) > 0:
                v = v.xreplace(cvdict)
            # Store all numeric ones inside constantsubs
            if isinstance(v, sympy.Expr):
                for tm in v.args:
                    xtn = [
                        term
                        for term in tm.args
                        if term not in fs and isinstance(term, sympy.Number)
                    ]
                    for c in xtn:
                        if np.abs(c) not in constantsubs and np.fabs(float(c)) != 1.0:
                            constantsubs[np.abs(c)] = sympy.Symbol(
                                f"c_{constCtr}")
                            constCtr += 1
            elif isinstance(v, sympy.Number):
                if np.abs(v) not in constantsubs and np.fabs(float(v)) != 1.0:
                    constantsubs[np.abs(v)] = f"c_{constCtr}"
                    constCtr += 1

        # Remove constant entries that are same to given precision
        constCtr = 1
        constantstoprecision = dict()
        newkeys = dict()
        skippedkeys = dict()
        for k, v in constantsubs.items():
            pk = f"{float(k):6f}"
            if pk not in constantstoprecision:
                constantstoprecision[pk] = sympy.Symbol(f"c_{constCtr}")
                constCtr += 1
            if v != constantstoprecision[pk]:
                skippedkeys[v] = constantstoprecision[pk]
            newkeys[k] = constantstoprecision[pk]

        for k, v in newkeys.items():
            constantsubs[k] = v

        # Handle elements that are functions, the multiplication operation with a state should be composition
        cleanedrhs = []

        for elem in cleanrhs:
            newelem = 0
            # Logic works for Add expression
            if not isinstance(elem, sympy.Add):
                fs = elem.free_symbols
                nterm = None
                state = None
                for f in fs:
                    if f in nonlinearrhsterms:
                        nterm = nonlinearrhsterms[f]
                        break
                if nterm is not None:
                    # #Get the current state for the term
                    states = []
                    for f in fs:
                        if f in stateVec.free_symbols:
                            states.append(f)
                    # If the state in term appears in nterm, divide
                    for st in states:
                        if st in nterm.free_symbols:
                            state = st
                            # handles just one!
                            break
                if nterm is not None and state is not None:
                    newelem = elem / state
                else:
                    newelem = term
                cleanedrhs.append(sympy.simplify(newelem))
            else:
                for term in elem.args:
                    fs = term.free_symbols
                    nterm = None
                    state = None
                    for f in fs:
                        if f in nonlinearrhsterms:
                            nterm = nonlinearrhsterms[f]
                            break
                    if nterm is not None:
                        # #Get the current state for the term
                        states = []
                        for f in fs:
                            if f in stateVec.free_symbols:
                                states.append(f)
                        #         break
                        # If the state in term appears in nterm, divide
                        for st in states:
                            if st in nterm.free_symbols:
                                state = st
                                # handles just one!
                                break
                    if nterm is not None and state is not None:
                        nterm = term / state
                        newelem += nterm
                    else:
                        newelem += term
                cleanedrhs.append(sympy.simplify(newelem))

        # Constants also contain u vector, however they are updated after each step
        # Do the update in compute_variables method, and initialise them in initialise_variables method
        # Compute rhs contains, nonlinearrhsterms and cleanedrhs
        # All parameters are in compositeparameters
        # Translate to use constants and states arrays
        arraymapping = OrderedDict()
        invarraymapping = OrderedDict()
        arraysubs = dict()
        for i, s in enumerate(self.stateVec):
            arraysubs[sympy.Symbol(s)] = sympy.Symbol(f"states[{i}]")
            arraymapping[s] = f"states[{i}]"
            invarraymapping[f"states[{i}]"] = s

        numconstants = 0
        # Do ubar first as numconstants change due to precision selection
        # ubar entries
        ubaridxmap = dict()
        for s in self.uVecSymbols:
            arraysubs[s] = sympy.Symbol(f"variables[{numconstants}]")
            arraymapping[s.name] = f"variables[{numconstants}]"
            invarraymapping[f"variables[{numconstants}]"] = s.name
            ubaridxmap[s.name] = f"variables[{numconstants}]"
            numconstants += 1

        # Multiple k's will have same v due to defined precision
        definedConstants = []
        for k, v in constantsubs.items():
            if v not in definedConstants:
                arraysubs[v] = sympy.Symbol(f"variables[{numconstants}]")
                arraymapping[str(v)] = f"variables[{numconstants}]"
                invarraymapping[f"variables[{numconstants}]"] = str(v)
                numconstants += 1
                definedConstants.append(v)

        # uCap entries
        for s in self.stateVec:
            arraysubs[sympy.Symbol(f"u_{s}")] = sympy.Symbol(
                f"variables[{numconstants}]"
            )
            arraymapping[f"u_{s}"] = f"variables[{numconstants}]"
            invarraymapping[f"variables[{numconstants}]"] = fr"\hat{{u}}_{s}"
            numconstants += 1

        # Non linear rhs terms
        for s, v in nonlinearrhsterms.items():
            arraysubs[s] = sympy.Symbol(f"variables[{numconstants}]")
            arraymapping[s.name] = f"variables[{numconstants}]"
            invarraymapping[f"variables[{numconstants}]"] = s.name
            numconstants += 1

        uCapterms = dict()
        ucapdescriptive = dict()
        for i, s in enumerate(self.stateVec):
            consu = Delx[i].xreplace(skippedkeys).xreplace(constantsubs)
            res = consu.xreplace(arraysubs)
            uCapterms[arraymapping[f"u_{s}"]] = res
            # Done this was as sympy printing changes the order of printed expr
            ucapdescriptive[
                arraymapping[f"u_{s}"]
            ] = fr"\hat{{u}}_{s} = {codegenerationutils._stringsubs(res.__str__(),invarraymapping)}"

        nonlineararrayedrhsterms = dict()
        nonlinearrhstermsdescriptive = dict()

        for s, v in nonlinearrhsterms.items():
            consv = v.xreplace(skippedkeys).xreplace(constantsubs)
            res = consv.xreplace(arraysubs)
            nonlineararrayedrhsterms[arraymapping[s.name]] = res
            # Done this was as sympy printing changes the order of printed expr
            nonlinearrhstermsdescriptive[
                arraymapping[s.name]
            ] = f"{s} = {codegenerationutils._stringsubs(res.__str__(),invarraymapping)}"

        arrayedrhs = []
        arrayedinputs = []
        # Use cleanedrhs and not cleanrhs - nonlinear terms with functions are transformed to compositions and not multiplication
        for elem in cleanedrhs:
            arrayedrhs.append(elem.xreplace(arraysubs))
        for elem in cleaninputs:
            arrayedinputs.append(elem.xreplace(arraysubs))
        
        return numconstants,constantsubs,nonlinearrhsterms,inputs,arrayedinputs,arraymapping,uCapterms,ucapdescriptive,nonlineararrayedrhsterms,nonlinearrhstermsdescriptive,arrayedrhs,invarraymapping,rhs,ubaridxmap,cleaninputs
    
    def exportAsPython(self):
        """Export composed FTU as python code similar to OpenCOR export"""
        return codegenerationutils.exportAsPython(self)
    
    def exportAsODEStepper(self,modelName="FTUStepper"):
        r"""Generate numerically solvable PHS
            d/dx (Ex) = (J-R) Q x - \hat{B}\hat{C}\hat{B}^T \hat{u} + \bar{B} \bar{u}
            \hat{y} = \hat{B}^T Q x
            \bar{y} = \bar{B}^T Q x
        
            Setup the code as a Python class, with the ability to step through time and
            set inputs
        """
        return codegenerationutils.exportAsODEStepper(self,modelName)
    
    def boundaryOperator(self):
        """Determine the boundary operator for the input graph

        Returns:
            numpy.array : 2D numpy array of size |internal E|x|internal V|
        """
        graph = self.ftugraph.to_undirected()
        #Handle boundary nodes seperately - encoded in node type attribute
        # Discrete operator requires a node for each potential - in case of FTU's
        # the boundary node provides fluxes, therefore create a node for each connection
        # set the nodes's potential to be that of head node + flux
        ntype = nx.get_node_attributes(graph,'type')     
        nodes = [n for n in graph.nodes() if ntype[n] == "in" ]
        edges = [ed for ed in graph.edges() if ed[0] in nodes and ed[1] in nodes]
        boundaryedges = [ed for ed in graph.edges() if ed[0] not in edges]
        nodes.sort() #Ensure consistancy
        boundaryedges.sort()
        nidx = dict() #Node label to incidence matrix index map
        nid = 0
        for nd in nodes:
            nidx[nd] = nid
            nid +=1
        
        numEdges = len(edges)
        adm = np.zeros((numEdges,len(nodes)))
        #Edge Ordering could be handled
        for ei,ed in enumerate(edges):
            adm[ei,nidx[ed[0]]] = -1
            adm[ei,nidx[ed[1]]] = +1
                        
        return adm

    def ddecSetupOperators(self,weight='weight'):
        """
           These operators are used to setup training data for DDEC operators   

           Steps to use:
            Given Node potentials (u0) and energy that is input at each node (f), where |u0| = |f| (as done by exported python code for simulating FTU)       
            Find f0 from u0
            
            Since f0 - weighted Grad(u0) = 0; 
            f0 is determined as
            f0 = weighted Grad (u0)
            
            the rhs f vector is obtained as 
            
            f1 = rhs_f_vector_map*f
            
            Then the problem for DDEC can be setup as
            
                    -Gradstarh*u^f_0 +       f0 = 0
                                       Div_h*f0 = f1
            
        Args:
            weight (string): Name of edge weight that will be used. default = 'weight'
           
        Returns:
            numpy.array : Weighted Gradient Operator 2D numpy array of size |all edges| x |V|
        """
        graph = self.ftugraph.to_undirected()
        #Handle boundary nodes seperately - encoded in node type attribute
        # Discrete operator requires a node for each potential - in case of FTU's
        # the boundary node provides fluxes, therefore create a node for each connection
        # set the nodes's potential to be that of head node + flux
        ntype = nx.get_node_attributes(graph,'type')     
        nodes = [n for n in graph.nodes() if ntype[n] == "in" ]
        edges = [ed for ed in graph.edges() if ed[0] in nodes and ed[1] in nodes]
        boundaryedges = [ed for ed in graph.edges() if ed[0] not in edges]
        nodes.sort() #Ensure consistancy
        boundaryedges.sort()
        nidx = dict() #Node label to incidence matrix index map
        nid = 0
        for nd in nodes:
            nidx[nd] = nid
            nid +=1
        
        numNodes = len(nodes)
        numEdges = len(edges)
        adm = np.zeros((numEdges,numNodes))
        edgeWeights = []
        #Edge Ordering could be handled
        #When loading from a composition Graph is a multigraph - data is stored as dict of dicts
        if isinstance(self.ftugraph,nx.MultiGraph):
            for ei,ed in enumerate(edges):
                ews = self.ftugraph.get_edge_data(ed[0],ed[1])
                ew = 1.0
                for k1,v1 in ews.items():
                    if weight in v1:
                        ew = v1[weight]
                        break
                    edgeWeights.append(ew)
                sew = np.sqrt(ew)
                adm[ei,nidx[ed[0]]] = -sew
                adm[ei,nidx[ed[1]]] = +sew           
        else:
            for ei,ed in enumerate(edges):
                ew = 1.0     
                ews = self.ftugraph.get_edge_data(ed[0],ed[1])
                if weight in ews:
                    ew = ews[weight]
                edgeWeights.append(ew)
                sew = np.sqrt(ew)                  

                adm[ei,nidx[ed[0]]] = -sew
                adm[ei,nidx[ed[1]]] = +sew

        return adm,edgeWeights

    def saveDiscreteExteriorCalculusOperators(self,filename,weight='weight'):
        """Save the boundary, edgeWeight and weighted gradient operators to file 
            Note that diag(sqrt(edgeWeight))* boudary = weighted gradient
            
        Args:
            filename (string): Absolute path of the destination numpy file to store the operators
            weight (str, optional): The FTUgraph edge attribute that defines the weight of connections. Defaults to 'weight'.

        Raises:
            Exception: If the source ftugraph is not bound to the composer, exception is raised
        """
        if self.ftugraph is not None:
            boundaryOp    = self.boundaryOperator()
            adm,edgeWeights  = self.ddecSetupOperators(weight)
            with open(filename,'wb') as ops:
                np.save(ops,boundaryOp)
                np.save(ops,edgeWeights)
                np.save(ops,adm)
        else:
            raise Exception("Connectivity graph not available!!")