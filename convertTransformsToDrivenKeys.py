from maya import cmds

def convert_transforms_to_drivenkeys():
    """
    Select the nodes you want to convert,
    then node with the driver attribute,
    then select the attribute from the channelbox,
    and run the script.
    Driver attribute should be at it's maximum value.
    Default value of driver attribute will be used for "off" state.
    Script will create offset group nodes and create
    driven keys on transforms that are keyable and
    have non-zero values.
    """
    seleks = cmds.ls(sl=True)
    nodes = seleks[0:-1]
    driver = seleks[-1]
    attribute = cmds.channelBox("mainChannelBox", q=True, sma=True)[0]
    attrf = "{}.{}".format(driver, attribute)
    attrv = cmds.getAttr(attrf)
    attrd = cmds.attributeQuery(attribute, node=driver, ld=True)[0]
    
    for drvn in nodes:
        keyables = cmds.listAttr(drvn, se=True, sn=True, k=True)
        uds = cmds.listAttr(drvn, ud=True, se=True, sn=True, k=True)
        if "v" in keyables:
            keyables.remove("v")
        if uds:
            for x in uds:
                if x in keyables:
                    keyables.remove(x)

        dictvals = {}
        for dc in keyables:
            dictvals["{}".format(dc)] = cmds.getAttr("{}.{}".format(drvn, dc))

        cmds.select(cl=True)
        grp = cmds.group(em=True, n=drvn + "_driven")
        cmds.matchTransform(grp, drvn)
        parent = cmds.listRelatives(drvn, f=True, p =True, s=False)
        child = cmds.listRelatives(parent, c=True, f=True, s=False)

        if parent:
            cmds.parent(grp, parent)
            if child:
                for ch in child:
                    cmds.parent(ch, grp)
        else:
            cmds.parent(drvn, grp)

        for key, val in dictvals.items():
            cmds.setAttr("{}.{}".format(grp, key), val)
            cmds.setDrivenKeyframe(grp, currentDriver=attrf, driverValue=attrv, attribute=key, value=val)
            trdv = cmds.attributeQuery(key, node=grp, ld=True)[0]
            cmds.setDrivenKeyframe(grp, currentDriver=attrf, driverValue=attrd, attribute=key, value=trdv)

        conns = cmds.listConnections(grp, s=True)
        for clnup in conns:
            animvals = cmds.keyframe(clnup, vc=True, q=True)
            if animvals[0] == animvals[1]:
                cmds.delete(clnup)

convert_transforms_to_drivenkeys()
