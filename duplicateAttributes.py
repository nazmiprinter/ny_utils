from maya import cmds

def dup_attrs():
    """
    Duplicate attribute command is buggy in Maya 2017/2018 so i decided to write my own.
    Select your transforms that you want to duplicate to first,
    lastly select the source transform with attributes you want to duplicate and run the script.
    """

    attSel = cmds.ls(sl=True)
    destObj = attSel[0:-1]
    sourceObj = attSel[-1]
    selAttr = cmds.channelBox('mainChannelBox', q=True, sma=True)

    for x in selAttr:    
        attType = cmds.attributeQuery(x, node=sourceObj, attributeType=True)
        keyable = cmds.getAttr(sourceObj + '.' + x, k=True)
        lock = cmds.getAttr(sourceObj + '.' + x, l=True)
        getVal = cmds.getAttr(sourceObj + '.' + x)

        if attType == 'bool':
            cmds.addAttr(destObj, sn=x, at=attType, keyable=keyable)

        elif attType == 'enum':
            enumNames = cmds.attributeQuery(x, node=sourceObj, listEnum=True)
            cmds.addAttr(destObj, en = enumNames[0], sn=x, at = attType, keyable = keyable)

        else:
            dv = cmds.attributeQuery(x, node=sourceObj, ld=True)[0]
            rangeCheck = cmds.attributeQuery(x, node=sourceObj, re=True)
            if rangeCheck:
                min = cmds.attributeQuery(x, node=sourceObj, min=True)[0]
                max = cmds.attributeQuery(x, node=sourceObj, max=True)[0]
                cmds.addAttr(destObj, sn=x, at=attType, keyable=keyable, dv=dv, max=max, min=min)
            else:
                minCheck = cmds.attributeQuery(x, node = sourceObj, mne = True)
                maxCheck = cmds.attributeQuery(x, node = sourceObj, mxe = True)
                if minCheck is False and maxCheck is False:
                    cmds.addAttr(destObj, sn=x, at=attType, keyable=keyable, dv=dv)
                if minCheck is True and maxCheck is False:
                    min = cmds.attributeQuery(x, node=sourceObj, min=True)[0]
                    cmds.addAttr(destObj, sn=x, at=attType, keyable=keyable, dv = dv, min = min)
                if minCheck is False and maxCheck is True:
                    max = cmds.attributeQuery(x, node=sourceObj, max=True)[0]
                    cmds.addAttr(destObj, sn=x, at=attType, keyable=keyable, dv = dv, max = max)
                
        for y in destObj:    
            newAttr = y + '.' + x
            cmds.setAttr(newAttr, getVal)
            if lock:
                cmds.setAttr(newAttr, lock=True)
		
dup_attrs()