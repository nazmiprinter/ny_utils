from maya import cmds

def select_deformers():
    sel0 = cmds.ls(sl=True)
    coll0 = cmds.skinCluster(sel0, q=True, influence=True)
    cmds.select(coll0)
    
def remove_unused_influences():
    inflist = cmds.skinCluster(q=True, inf=True)
    wilist = cmds.skinCluster(q=True, wi=True)
    zerolist = list(set(inflist).difference(set(wilist)))
    for rem in zerolist:
        cmds.skinCluster(e=True, ri=rem)
    
def copy_paste_weights():
    """	
    Directly copy skinCluster with correct influences from one mesh to another.
    Also removes influences with 0 weight so it might come handy to use on bandwrists, clothes etc..
    First select the source mesh, then destination mesh and run the script.
    """
    
    skinlist = cmds.ls(sl=True)
    src = skinlist[0]
    dest = skinlist[1]
    cmds.select(cl=True)
    cmds.select(src)
    select_deformers()
    cmds.select(dest, add=True)
    cmds.skinCluster(bm=0, tsb=True, nw=1, dr=4.0)
    cmds.select(cl=True)
    cmds.select(src)
    cmds.select(dest, add=True)
    cmds.copySkinWeights(sa='closestPoint', nm=True)
    cmds.select(dest)
    remove_unused_influences()
    
copy_paste_weights()