from maya import cmds

#Setting keyable attributes of selected nodes to their default value.
#It's extremely handy to use it on "CTRL+SHIFT+R" shortcut

seleks = cmds.ls(sl=True)
for node in seleks:
	kbls = cmds.listAttr(node, k=True, se=True)
	for dv in kbls:
		ld = cmds.attributeQuery(dv, node=node, ld=True)[0]
		try:
			cmds.setAttr('{}.{}'.format(node, dv), ld)
		except RuntimeError:
			pass
