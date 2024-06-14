"""Helper routines to create PHS descriptions"""
def setPHSComponentNetwork(phs,component,netid):
    """Associated the PHS state/input-output vector component to the network with id netid

    Args:
        phs (dict): Datastructure that stores PHS related data
        component (string): Identity of the PHS state/input-output vector
        netid (int): Id for FTU network

    Returns:
        dict: Updated input datastructure that stores PHS related data
    """
    if 'u_split' in phs['portHamiltonianMatrices']:
        phs['portHamiltonianMatrices']['u_split']['elements'][component] = netid
    else:
        ups = phs['portHamiltonianMatrices']['u']
        for x in range(ups['rows']):
            ups['elements'][x] = ''
        ups['elements'][component] = netid
        phs['portHamiltonianMatrices']['u_split'] = ups
    return phs


def connect(phsconnections,phs1,phs1comp,network):
    """Connect a PHS instance's state/input-output vector component to a FTU network

    Args:
        phsconnections (dict): Datastructure to store the connection information
        phs1 (string): Name of the PHS class
        phs1comp (string): state/input-output vector component's name
        network (int): Network id of the FTU network

    Returns:
        dict: Updated datastructure that stores the connection information
    """
    if "connections" not in  phsconnections:
        phsconnections["connections"] = dict()
        
    if phs1 not in phsconnections["connections"]:
        phsconnections["connections"][phs1] = dict()
    phsconnections["connections"][phs1][phs1comp] = network
    return phsconnections
    
def connectToBoundary(phsconnections,phs1,phs1comp,network):
    """Connect a PHS instance's state/input-output vector component to a FTU boundary network

    Args:
        phsconnections (dict): Datastructure to store the connection information
        phs1 (string): Name of the PHS class
        phs1comp (string): state/input-output vector component's name
        network (int): Network id of the FTU boundary network

    Returns:
        dict: Updated datastructure that stores the connection information
    """
    
    if "bdryconnections" not in  phsconnections:
        phsconnections["bdryconnections"] = dict()
    
    if phs1 not in phsconnections["bdryconnections"]:
        phsconnections["bdryconnections"][phs1] = dict()
    phsconnections["bdryconnections"][phs1][phs1comp] = network
    return phsconnections

def addExternalInput(phsconnections,node,component,network=-1):
    """Connect a node as the provide of external input/output to a FTU network

    Args:
        phsconnections (dict): Datastructure to store the connection information
        node (string): Label of graph node that provides the external interface
        component (string): state/input-output vector component's name to which the input/output is provided
        network (int): Network id of the FTU network

    Returns:
        dict: Updated datastructure that stores the connection information
    """
    if "externalinputs" not in  phsconnections:
        phsconnections["externalinputs"] = dict()
    
    if node not in phsconnections["externalinputs"]:
        phsconnections["externalinputs"][node] = []
        
    phsconnections["externalinputs"][node].append([component,network])
    return phsconnections