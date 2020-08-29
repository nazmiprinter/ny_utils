from maya import cmds

def cp_vertex_normal():
    """
    Select your source vertex normal and destination, then run the script.
    """
    vsel = cmds.ls(sl=True, fl=True)
    src = vsel[0]
    dest = vsel[1]
    srcNorm = cmds.polyNormalPerVertex(vsel[0], q=True, xyz=True)
    cmds.polyNormalPerVertex(dest, xyz=(srcNorm[0], srcNorm[1], srcNorm[2]), edit=True)
    
cp_vertex_normal()