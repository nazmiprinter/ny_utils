import maya.api.OpenMaya as om

def softselection2_cluster():
    """
    Make sure soft select mode is on.
    Run the script and name your cluster.
    """
    promptu = cmds.promptDialog(title='Cluster name', message='Please name your cluster:', button=['OK', 'Cancel'],
                                defaultButton='OK', cancelButton='Cancel', dismissString='Cancel')
    if promptu == 'OK':
        clsName = cmds.promptDialog(q=True, text=True)
    else:
        clsName = 'ss_cluster'
    selection = om.MGlobal.getRichSelection()
    softSel = om.MRichSelection(selection)
    selList = softSel.getSelection()

    component = selList.getComponent(0)
    componentIndex = om.MFnSingleIndexedComponent(component[1])
    vertexList = componentIndex.getElements()

    weightList = {}
    for loop in range (len(vertexList)):
        weight = componentIndex.weight(loop)
        influence = weight.influence
        weightList.setdefault(vertexList[loop], influence)
        
    rangeVertices = selList.getSelectionStrings()
    newcluster = cmds.cluster(rangeVertices, n=clsName)

    for eachWeight in weightList:
        currentVertex = eachWeight
        currentWeight = weightList[eachWeight]
        cmds.setAttr('{}.weightList[0].w[{}]'.format(newcluster[0], currentVertex), currentWeight)
        
softselection2_cluster()