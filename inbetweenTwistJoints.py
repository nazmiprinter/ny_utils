def inbetween_twist_joints(primaryAxis, name, number):
    """
    Arguments are self explanatory.
    Use lowercase for axis: x+, z-
    Select parent and child joints, then run the script.
    """
    #JOINT SETUP
    jnts = cmds.ls(sl=True)
    first = jnts[0]
    second = jnts[1]

    length = cmds.getAttr("{}.t{}".format(second, primaryAxis[0]))
    div = length / (float(number) + 1.0)
    
    cmds.select(cl=True)
    startJN = cmds.joint(n=name + "_start_JNT")
    cmds.matchTransform(startJN, first)
    cmds.makeIdentity(r=True, a=True)
    cmds.select(cl=True)
    endJN = cmds.joint(n=name + "_end_JNT")
    cmds.matchTransform(endJN, second)
    cmds.makeIdentity(r=True, a=True)
    
    cmds.select(startJN)
    for btw in range(int(number)):
        cmds.insertJoint()
        insjt = cmds.rename(name + "_twist_{}_JNT".format(btw))
        cmds.setAttr(insjt + ".t{}".format(primaryAxis[0]), div)
    
    cmds.parent(endJN, insjt)
    
    #HANDLE AND TWIST
    ikHDL = cmds.ikHandle(sol="ikSplineSolver", ccv=True, scv=True, roc=True, n=name + "_twist_HDL", sj=startJN, ee=endJN)
    ikEFF = cmds.rename(ikHDL[1], name + "_twist_EFF")
    ikCRV = cmds.rename(ikHDL[2], name + "_twist_CRV")
    
    if primaryAxis[1] == "+":
        cmds.connectAttr(second + ".r{}".format(primaryAxis[0]), ikHDL[0] + ".twist")
    else:
        twistAbar = cmds.createNode("animBlendNodeAdditiveRotation", n=name + "_twist_ABAR")
        cmds.connectAttr(second + ".r{}".format(primaryAxis[0]), twistAbar + ".inputAX")
        cmds.setAttr(twistAbar + ".weightA", -1)
        cmds.connectAttr(twistAbar + ".outputX", ikHDL[0] + ".twist")
        
    #CLEANUP
    cmds.setAttr(ikCRV + ".v", 0)
    cmds.setAttr(ikHDL[0] + ".v", 0)
    cmds.parent(ikCRV, first)
    cmds.parent(ikHDL[0], first)
    cmds.parent(startJN, first)
    
inbetween_twist_joints("x+", "test", "5")