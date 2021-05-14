from maya import cmds

def convert_animkeys_to_drivenkeys(driver, driverMin, driverMax):
    """
    Make sure to set the playback range according to your animation.
    Select the attributes you want to convert from channel box,
    then run the script.
    driver: Full name of the driver attribute(string)
    driverMin: Starting value of the driver attribute(int/float)
    driverMax: Ending value of the driver attribute(int/float)
    """
    oldPlugs = []
    oldKeys = []
    newKeys = []
    timeMin = int(cmds.playbackOptions(min=True, q=True))
    timeMax = int(cmds.playbackOptions(max=True, q=True))
    cmds.currentTime(timeMin)
    cmds.setAttr(driver, driverMin)
    cmds.setKeyframe(driver)
    cmds.currentTime(timeMax)
    cmds.setAttr(driver, driverMax)
    cmds.setKeyframe(driver)
    node = cmds.ls(sl=True)[0]
    selAttr = cmds.channelBox("mainChannelBox", q=True, sma=True)
    duplicate = cmds.duplicate(node)[0]

    for oldKey in selAttr:
        oldKeys.append(cmds.listConnections("{}.{}".format(node, oldKey), p=False, d=False, s=True)[0])

    for oldPlug in selAttr:
        oldPlugs.append("{}.{}".format(node, oldPlug))

    for fra in range(timeMin, timeMax+1):
        cmds.currentTime(fra)
        for attr in selAttr:
            cmds.setDrivenKeyframe(duplicate,
                                    currentDriver=driver,
                                    attribute=attr,
                                    driverValue=cmds.getAttr(driver),
                                    value=cmds.getAttr("{}.{}".format(node, attr)))

    for new in selAttr:
        newKeys.append(cmds.listConnections("{}.{}".format(duplicate, new), p=False, d=False, s=True)[0])

    for old, new in zip(oldPlugs, newKeys):
        cmds.connectAttr(new + ".output", old, f=True)

    #CLEANUP
    cmds.delete(duplicate)
    cmds.delete(oldKeys)
    cmds.delete(cmds.listConnections(driver, p=False, d=False, s=True))
    for ren, org in zip(newKeys, oldKeys):
        cmds.rename(ren, org)
    cmds.currentTime(timeMin)
    cmds.setAttr(driver, driverMin)

convert_animkeys_to_drivenkeys("dummy_LOC.custom", 0, 10)