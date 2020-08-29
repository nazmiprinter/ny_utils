from maya import cmds, OpenMaya

def delete_unused_dagpose_nodes():
    """
    Clears out the unused dagpose nodes in the scene.
    """
    dels = []
    dagposes = cmds.ls(type='dagPose')
    for dpn in dagposes:
        outs = cmds.listConnections(dpn + '.message', d=True)
        if outs:
            pass
        else:
            dels.append(dpn)
    if dels:
        cmds.delete(dels)
        OpenMaya.MGlobal.displayInfo('DELETED DAGPOSE NODES:{}'.format(dels))
    else:
        OpenMaya.MGlobal.displayInfo('NO DAGPOSE NODE DELETED')
        
delete_unused_dagpose_nodes()