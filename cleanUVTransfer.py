from maya import cmds

def clean_uv_transfer():
    """
    It's a script to copy the uv from one mesh to a another skinned mesh
    Select the mesh you want to copy from, then skinned mesh and run the script.
    """

    selList = cmds.ls(sl=True, ap=True, long=True)
    #ERROR CHECK
    if len(selList) != 2:
        cmds.warning('Please select your source AND target object only')
    else:
        #GETTING TRANSFORM OF TGT AND SHAPE OF DEST NODE
        source, target = selList[0], selList[1]
        tgtList = cmds.listRelatives(target, s=True)
        tgtInd = [i for i, elem in enumerate(tgtList) if 'Orig' in elem]
        tgtOrig = target + '|' + tgtList[tgtInd[0]]
        #GETTING ACCESS TO ORIG NODE AND EXECUTION
        cmds.setAttr('{}.intermediateObject'.format(tgtOrig), 0)
        cmds.select(cl=True)
        cmds.select(source)
        cmds.select(tgtOrig, add=True)
        cmds.transferAttributes(pos=0, nml=0, uvs=2, col=2, spa=4, suv='map1', tuv='map1', sm=3, fuv=0, clb=1)
        cmds.delete(tgtOrig,  ch=True)
        cmds.setAttr(tgtOrig + '.intermediateObject', 1)
        
clean_uv_transfer()