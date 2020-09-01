from maya import cmds, OpenMaya

class PFRivet():
    """
    This script doesn't use the nodes that prevents the mesh to evaluate in Parallel(GPU). 
    Select 2 edges on a mesh and run the script.
    Name your rivet and it's done.
    """
    
    def __init__(self):
        if len(cmds.ls(sl=True, fl=True)) != 2:
            OpenMaya.MGlobal.displayWarning('Please select only 2 edges')
        else:
            promptu = cmds.promptDialog(title='Rivet name', message='Please name your rivet:', button=['OK', 'Cancel'],
          defaultButton='OK', cancelButton='Cancel', dismissString='Cancel')
            if promptu == 'OK':
                self.name = cmds.promptDialog(q=True, text=True)
            else:
                self.name = 'rivet'
            self.get_data()
            self.create_nodes()
            self.make_connections()
            OpenMaya.MGlobal.displayInfo('Job Done!')
            cmds.select(self.rivloc)
   
    def get_data(self):
        edges = cmds.ls(sl=True, fl=True)
        self.edge1Id = float(edges[0][edges[0].find('[')+1:edges[0].find(']')])
        self.edge2Id = float(edges[1][edges[1].find('[')+1:edges[1].find(']')])
        dag = edges[0].split('.')[0]
        cmds.select(dag)
        cmds.pickWalk(d='down')
        self.shape = cmds.ls(sl=True)[0]
        self.maxedge = cmds.polyEvaluate(self.shape, e=True)
    
    def create_nodes(self):
        self.rivloc = cmds.spaceLocator(n=self.name + '_LOC')[0]
        self.rivgrp = cmds.group(n=self.name + '_offset')
        cmds.addAttr(self.rivloc, ln='U',k=True, at='float', min=0, max=1, dv=0.5)
        cmds.addAttr(self.rivloc, ln='V',k=True, at='float', min=0, max=1, dv=0.5)
        cmds.addAttr(self.rivloc, ln='edge1Index', k=True, at='long', min=0, max=self.maxedge, dv=self.edge1Id)
        cmds.addAttr(self.rivloc, ln='edge2Index', k=True, at='long', min=0, max=self.maxedge, dv=self.edge2Id)
        self.cfme1 = cmds.createNode('curveFromMeshEdge', n=self.name + '_CFME1')
        self.cfme2 = cmds.createNode('curveFromMeshEdge', n=self.name + '_CFME2')
        self.loft = cmds.createNode('loft', n=self.name + '_LOFT')
        cmds.setAttr(self.loft + '.degree', 1)
        self.posi = cmds.createNode('pointOnSurfaceInfo', n=self.name + '_POSI')
        cmds.setAttr(self.posi + '.turnOnPercentage', 1)
        self.fbfm = cmds.createNode('fourByFourMatrix', n=self.name  + '_FBFM')
        self.dcm = cmds.createNode('decomposeMatrix', n=self.name + '_DCM')
       
    def make_connections(self):
        cmds.connectAttr(self.shape + '.worldMesh[0]', self.cfme1 + '.inputMesh')
        cmds.connectAttr(self.shape + '.worldMesh[0]', self.cfme2 + '.inputMesh')
        cmds.connectAttr(self.rivloc + '.edge1Index', self.cfme1 + '.edgeIndex[0]')
        cmds.connectAttr(self.rivloc + '.edge2Index', self.cfme2 + '.edgeIndex[0]')
        cmds.connectAttr(self.cfme1 + '.outputCurve', self.loft + '.inputCurve[0]')
        cmds.connectAttr(self.cfme2 + '.outputCurve', self.loft + '.inputCurve[1]')
        cmds.connectAttr(self.loft + '.outputSurface', self.posi + '.inputSurface')
        cmds.connectAttr(self.rivloc + '.U', self.posi + '.parameterU')
        cmds.connectAttr(self.rivloc + '.V', self.posi + '.parameterV')
        cmds.connectAttr(self.posi + '.positionX', self.fbfm + '.in30')
        cmds.connectAttr(self.posi + '.positionY', self.fbfm + '.in31')
        cmds.connectAttr(self.posi + '.positionZ', self.fbfm + '.in32')
        cmds.connectAttr(self.posi + '.normalX', self.fbfm + '.in00')
        cmds.connectAttr(self.posi + '.normalY', self.fbfm + '.in01')
        cmds.connectAttr(self.posi + '.normalZ', self.fbfm + '.in02')
        cmds.connectAttr(self.posi + '.tangentUx', self.fbfm + '.in10')
        cmds.connectAttr(self.posi + '.tangentUy', self.fbfm + '.in11')
        cmds.connectAttr(self.posi + '.tangentUz', self.fbfm + '.in12')
        cmds.connectAttr(self.posi + '.tangentVx', self.fbfm + '.in20')
        cmds.connectAttr(self.posi + '.tangentVy', self.fbfm + '.in21')
        cmds.connectAttr(self.posi + '.tangentVz', self.fbfm + '.in22')
        cmds.connectAttr(self.fbfm + '.output', self.dcm + '.inputMatrix')
        cmds.connectAttr(self.dcm + '.outputRotateX', self.rivgrp + '.rotateX')
        cmds.connectAttr(self.dcm + '.outputRotateY', self.rivgrp + '.rotateY')
        cmds.connectAttr(self.dcm + '.outputRotateZ', self.rivgrp + '.rotateZ')
        cmds.connectAttr(self.dcm + '.outputTranslateX', self.rivgrp + '.translateX')
        cmds.connectAttr(self.dcm + '.outputTranslateY', self.rivgrp + '.translateY')
        cmds.connectAttr(self.dcm + '.outputTranslateZ', self.rivgrp + '.translateZ')

insR = PFRivet()