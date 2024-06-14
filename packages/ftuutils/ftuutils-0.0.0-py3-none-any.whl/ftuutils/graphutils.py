"""Logic for creating FTU graphs based on known motifs, like 2d Lattice"""
import numpy as np
import networkx as nx
import copy


from ftuutils.base import FTUGraph

#2D lattice FTU graph methods
class Lattice2D(FTUGraph):
    """
        Class to construct a 2D lattice, suitable for simulating 2D electrical/chemical wave propogation.
        ...
        Attributes
        ----------
        rows : int
            Number of rows in the lattice
        cols : int
            Number of columns in the lattice
        defaultphs : str
            The default PHS class assigned to the cells/nodes in the lattice
    """
    def __init__(self,rows,cols,defaultphs=None) -> None:
        super().__init__()
        self.row_size = rows
        self.col_size = cols
        self.active_cells = np.ones((rows,cols),dtype=np.bool_)
        self.sheet_conductivity = {1:1.0}
        self.fibre_conductivity = {1:1.0}
        self.connections = self._initConnections()
        #Get boundary nodes
        # In case setDefects is not called
        self.bottomNodes = self.getCellIndex([[-1,self.row_size],[0,self.col_size]])[self.active_cells].flatten()
        self.leftNodes = self.getCellIndex([[0,self.row_size],[0,0]])[self.active_cells].flatten()
        self.rightNodes = self.getCellIndex([[0,self.row_size],[-1,self.col_size]])[self.active_cells].flatten()
        self.topNodes = self.getCellIndex([[0,0],[0,self.col_size]])[self.active_cells].flatten()
        self.num_active_cells = rows*cols      
        self.blocks = []
        self.stimulusBlocks = dict()
        self.defaultphs = defaultphs

    def setStimulationBlock(self,bname,blk):
        """Setup a stimulus block for the given graph
    
        Identify a block of cells within the lattice and setup networks and input nodes

        Args:
            bname (str): Name for the block
            blk (array): Array of size num active cells with 'True' for cells within the block
        """
        bl = self.getCellIndex(blk)[self.active_cells].flatten()
        self.stimulusBlocks[bname] = bl
                
    def setDefects(self,blocks) -> None:
        """Setup defective regions within the lattice identified by blocks

        Args:
            blocks (array of arrays): Array of 2D coordinates  of the form [[x_start,x_end],[y_start,y_end]]
        """
        self.blocks = blocks
        self.active_cells.fill(True)
        for bl in blocks:
            x,xe = bl[0][0],bl[0][1]+1
            y,ye = bl[1][0],bl[1][1]+1
            if x < 0:
                x = self.row_size + x
            if x > self.row_size:
                x = self.row_size
            if y < 0:
                y = self.col_size + y
            if y > self.col_size:
                y = self.col_size
            if bl[0][1] < 0:
                xe = self.row_size + bl[0][1]
            if xe < x:
                xe = x+1
            if xe > self.row_size:
                xe = self.row_size
            if bl[1][1] < 0:
                ye = self.col_size + bl[1][1]            
            if ye < y:
                ye = y+1
            if ye > self.col_size:
                ye = self.col_size 
                
            self.active_cells[x:xe, y:ye] = False
        self.num_active_cells = np.sum(self.active_cells.flatten())   
        
        #Get boundary nodes
        #
        self.bottomNodes = self.getCellIndex([[-1,self.row_size],[0,self.col_size]])[self.active_cells].flatten()
        self.leftNodes = self.getCellIndex([[0,self.row_size],[0,0]])[self.active_cells].flatten()
        self.rightNodes = self.getCellIndex([[0,self.row_size],[-1,self.col_size]])[self.active_cells].flatten()
        self.topNodes = self.getCellIndex([[0,0],[0,self.col_size]])[self.active_cells].flatten()       
              
    def setFibreConductivity(self,cond,network=1) -> None:
        """Set the conductivity values along the horizontal axis

        Args:
            cond (float): Conductivity values
            network (int, optional): Network on which the weights are assigned. Defaults to 1.
        """
        self.fibre_conductivity[network] = cond

    def setSheetConductivity(self,cond,network=1) -> None:
        """Set the conductivity values along the vertical axis

        Args:
            cond (float): Conductivity values
            network (int, optional): Network on which the weights are assigned. Defaults to 1.
        """        
        self.sheet_conductivity[network] = cond
        
    def _initConnections(self) -> np.array:
        """
        Simplified implementation of connections, defects need not be take into consideration
        as they are handled at the time of generating the graph
        However, the graph generation code only handles 8 neighbors
        For complex conditions, update the code appropriately
        Returns:
            np.array: Connections between nodes
        """
        connections = np.ones((self.row_size,self.col_size,8))
        #Connections - 0 Top, 1 Top-Right, 2 Right, 3 Bottom-Right, 4 Bottom
        # 5 Bottom-Left, 6 Left, 7 Top-Left         
        connections[:, :, 0] = 2
        connections[:, :, 2] = 1
        connections[:, :, 6] = 1
        connections[:, :, 4] = 2
        
               
        connections[:, :, 1] = 0.0
        connections[:, :, 3] = 0.0
        connections[:, :, 5] = 0.0
        connections[:, :, 7] = 0.0
        return connections    
       
    def _generateGraph(self,active_cells) -> nx.Graph:
        """ Logic to generate a 2D lattice given the weights and active cells

        Args:
            active_cells (array): Array of boolean values that indicate which cells are active within the lattice

        Returns:
            nx.Graph: networkx Graph
        """
        G = nx.MultiGraph()
        rows = range(self.row_size)
        cols = range(self.col_size)
        nix = dict()
        nodeid = 1
        for i in rows:
            for j in cols:
                if active_cells[i,j]:
                  nix[(i,j)] = nodeid
                  nodeid +=1  
        #Create non defect nodes
        G.add_nodes_from(list(nix.values()))
        ii = (i for i in cols for j in rows)
        jj = (j for i in cols for j in rows)
        #Set fibre direction along x axis and sheet along y axis, with origin at top left like in numpy 2d array
        pos = dict()
        celltype = dict()
        nodetype = dict()
        for i, j in zip(ii, jj):
            if (i, j) in nix:
                pos[nix[(i, j)]] = (j, self.row_size - i) 
                celltype[nix[(i, j)]] = self.defaultphs if nix[(i, j)] not in self.celltypes else self.celltypes[nix[(i, j)]]
                nodetype[nix[(i, j)]] = 'in'

        
        nx.set_node_attributes(G, pos, "pos")
        nx.set_node_attributes(G, celltype,"phs")
        nx.set_node_attributes(G, nodetype,"type")
                           
        for i in range(self.connections.shape[0]):
            for j in range(self.connections.shape[1]):
                if (i,j) in nix:
                    #Connections - 0 Top, 1 Top-Right, 2 Right, 3 Bottom-Right, 4 Bottom
                    # 5 Bottom-Left, 6 Left, 7 Top-Left 
                    ixs = [(i-1,j),(i-1,j+1),(i,j+1),(i+1,j+1),(i+1,j),(i+1,j-1),(i,j-1),(i-1,j-1)]

                    for k in range(self.connections.shape[2]):
                        if(self.connections[i,j,k]!=0.0):
                            if ixs[k] in nix:
                                contype = self.connections[i,j,k] #1 Fiber connectivity, 2 Sheet connectivity
                                weight = {}
                                if contype==1:
                                    weight = copy.deepcopy(self.fibre_conductivity)
                                elif contype==2:
                                    weight = copy.deepcopy(self.sheet_conductivity)
                                G.add_edges_from([(nix[(i,j)],nix[ixs[k]],weight)])
                                
        return G
    
    def getStimulusBlockNodes(self,bname):
        """Get the list of nodes that fall within the stimulation block

        Args:
            bname (str): Name of the block

        Returns:
            np.array: List of nodes that fall within the blk, [] if block is not found
        """
        if bname in self.stimulusBlocks:
            nix = np.arange(1,self.num_active_cells+1)
            return nix[self.stimulusBlocks[bname]]
        return []    
    
    def getNodes(self,blk):
        """
            Get the list of node ids that fall within the blk
        Args:
            blk (list): [[x0,x1],[y0,y1]]
        """
        simb = self.getCellIndex(blk)[self.active_cells].flatten()
        nix = np.arange(1,self.num_active_cells+1)
        return nix[simb]
         
    def getCellIndex(self,block) -> np.array:
        """
        Boolean index of cells  into a (num_active_cells,:) array representative of the state vector

        Args:
            block (np.array): a selection block of the format [[x0,x1], [y0,y1]]

        Returns:
            np.array: (num_active_cells,1) boolean array, selected elements will be True
        """        
        selectedCells = np.copy(self.active_cells)
        selectedCells.fill(False)
        x,xe = block[0][0],block[0][1]+1
        y,ye = block[1][0],block[1][1]+1
        if x < 0:
            x = self.row_size + x
        if x > self.row_size:
            x = self.row_size
        if y < 0:
            y = self.col_size + y
        if y > self.col_size:
            y = self.col_size
        if block[0][1] < 0:
            xe = self.row_size + block[0][1]
        if xe < x:
            xe = x+1
        if xe > self.row_size:
            xe = self.row_size
        if block[1][1] < 0:
            ye = self.col_size + block[1][1]            
        if ye < y:
            ye = y+1
        if ye > self.col_size:
            ye = self.col_size 
            
        selectedCells[x:xe, y:ye] = True
        return np.logical_and(selectedCells, self.active_cells)
        
    def getSubGraph(self,block) -> nx.Graph:
        """Get the subgraph that includes cells within the block

        Args:
            block (array): [[x0,x1],[y0,y1]]

        Returns:
            nx.Graph: networkx Graph
        """
        subset = self.getCellIndex(block)
        return self._generateGraph(subset)        
    
    def getGraph(self) -> nx.Graph:
        """Get the FTU graph corresponding to the Lattice for set parameters

        Returns:
            nx.Graph: networkx Graph
        """
        return self._generateGraph(self.active_cells)
    
    def getPositionFromIndex(self,index):
        """Get the x,y coordinates for a cell with an index 

        Args:
            index (int): cell index

        Returns:
            list : x,y coordinates for the cell at index
        """
        i = index//self.row_size
        j = index%self.col_size
        return (i+1, j+1) 

    def convertStateVecTo2D(self,array,fill_defect=0.0) -> np.array:
        """
        Utility function to convert a (num_active_cells,:) array  
        to an array of shape (row_size,col_size,:)
        The graphs
        Args:
            array (float): State vector array of shape (num_active_cells,:)

        Returns:
            np.array: Array of shape (row_size,col_size,:)
        """
        assert( array.shape[0]==self.num_active_cells ), "First dim of state vector's size does not match the graph's dimension {self.num_active_cells}"
        
        result = np.zeros((self.row_size,self.col_size,array.shape[-1]),dtype=array.dtype)
        result.fill(fill_defect)
        result[self.active_cells,:] = array
        return result