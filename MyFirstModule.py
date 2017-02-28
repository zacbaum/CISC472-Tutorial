# Importing all the necessary Slicer APIs and goodies.
import os
import unittest
import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *
import logging

# Initialization of the module -- Also holds the help text and contributor information.
class MyFirstModule(ScriptedLoadableModule):

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "MyFirstModule"
    self.parent.categories = ["Examples"]
    self.parent.dependencies = []
    self.parent.contributors = ["Csaba Pinter, Zachary Baum, Vinyas Harish -- Laboratory for Percutaneous Surgery, Queen's University"]
    self.parent.helpText = """
    Used to find the center of mass of two label maps.
    Will place a fiducial marker in the calculated point.
    """
    self.parent.acknowledgementText = """
    """

# This part of the code will produce the Graphical User Interface (GUI) for the module.
class MyFirstModuleWidget(ScriptedLoadableModuleWidget):

  def setup(self):
    ScriptedLoadableModuleWidget.setup(self)

    # Creates the Parameters Dropdown widget.
    parametersCollapsibleButton = ctk.ctkCollapsibleButton()
    parametersCollapsibleButton.text = "Parameters"
    self.layout.addWidget(parametersCollapsibleButton)
    parametersFormLayout = qt.QFormLayout(parametersCollapsibleButton)

    # Input Volume 1 Selector.
    # Defines the selector as a "Combobox"
    self.inputSelector = slicer.qMRMLNodeComboBox()

    # This sets the node type that can be selected as a Label Map Volume Node.
    self.inputSelector.nodeTypes = ( ("vtkMRMLLabelMapVolumeNode"), "" )
    self.inputSelector.selectNodeUponCreation = False
    self.inputSelector.addEnabled = False
    self.inputSelector.removeEnabled = False
    self.inputSelector.noneEnabled = False
    self.inputSelector.showHidden = False
    self.inputSelector.showChildNodeTypes = False
    self.inputSelector.setMRMLScene( slicer.mrmlScene )

    # Tooltips and the label for the combobox.
    self.inputSelector.setToolTip( "Pick the first input to the algorithm." )
    parametersFormLayout.addRow("Input Volume 1: ", self.inputSelector)

    # Input Volume 2 Selector. 
    self.input2Selector = slicer.qMRMLNodeComboBox()
    self.input2Selector.nodeTypes = ( ("vtkMRMLLabelMapVolumeNode"), "" )
    self.input2Selector.selectNodeUponCreation = False
    self.input2Selector.addEnabled = False
    self.input2Selector.removeEnabled = False
    self.input2Selector.noneEnabled = False
    self.input2Selector.showHidden = False
    self.input2Selector.showChildNodeTypes = False
    self.input2Selector.setMRMLScene( slicer.mrmlScene )
    self.input2Selector.setToolTip( "Pick the second input to the algorithm." )
    parametersFormLayout.addRow("Input Volume 2: ", self.input2Selector)

    # Apply Button
    # Defines the button and sets it to be unclickable (for now...)
    self.applyButton = qt.QPushButton("Apply")
    self.applyButton.toolTip = "Run the algorithm."
    self.applyButton.enabled = False
    parametersFormLayout.addRow(self.applyButton)

    # Text Field
    # Provides the output space for the Center of Mass of the two objects.
    self.outputLabel = qt.QLabel()
    parametersFormLayout.addRow(self.outputLabel) 

    # When the apply button is clicked, it says it's clicked,
    # When the selectors have a node selected, they are marked as filled.
    self.applyButton.connect('clicked(bool)', self.onApplyButton)
    self.inputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.input2Selector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)

    # Add vertical spacer
    self.layout.addStretch(1)

    # Refresh Apply button state
    self.onSelect()

  # Does nothing for this module. Can be used to clear out selectors once run if you wanted to.
  def cleanup(self):
    pass

  # When the node selectors both contain valid nodes (they can be the same node),
  # the apply button becomes clickable!
  def onSelect(self):
    self.applyButton.enabled = self.inputSelector.currentNode() and self.input2Selector.currentNode()

  # When the apply button is clicked, a new instance of the logic is created,
  # and the algorithm is run using the inputted nodes from the selectors.
  # The output label text is also updated with the coordinates of the Center of Mass.
  def onApplyButton(self):
    logic = MyFirstModuleLogic()
    logic.run(self.inputSelector.currentNode(), self.input2Selector.currentNode())
    self.outputLabel.setText('(' + repr(logic.translation[0]) + ', ' + repr(logic.translation[1]) + ', ' + repr(logic.translation[2]) + ')') 

# The logic for the Module.
class MyFirstModuleLogic(ScriptedLoadableModuleLogic):

  # This function gets the center of mass of a given volume node.
  def getCenterOfMass(self, volumeNode):

    # Define some necessary variables for later.
    centerOfMass = [0,0,0]
    numberOfStructureVoxels = 0
    sumX = sumY = sumZ = 0

    # Gets the image data for the current node.
    volume = volumeNode.GetImageData()

    # Uses the extent of the image to get the range for the loops,
    # Then if the value of the given voxel is > zero we add the 
    # value of the voxel coordinate to the running sums, and the
    # count of voxels is incremented.
    for z in xrange(volume.GetExtent()[4], volume.GetExtent()[5] + 1, 2):
      for y in xrange(volume.GetExtent()[2], volume.GetExtent()[3] + 1, 2):
        for x in xrange(volume.GetExtent()[0], volume.GetExtent()[1] + 1, 2):
          voxelValue = volume.GetScalarComponentAsDouble(x,y,z,0)
          if voxelValue > 0:
            numberOfStructureVoxels = numberOfStructureVoxels + 1
            sumX = sumX + x
            sumY = sumY + y
            sumZ = sumZ + z

    # When the loop terminates, if we had any voxels, we calculate
    # the Center of Mass by dividing the sums by the number of voxels
    # in total.
    if numberOfStructureVoxels > 0:
      centerOfMass[0] = sumX / numberOfStructureVoxels
      centerOfMass[1] = sumY / numberOfStructureVoxels
      centerOfMass[2] = sumZ / numberOfStructureVoxels

    # Return the point that contains the center of mass location.
    return centerOfMass 

  def run(self,inputVolume,input2Volume):

    # Get the transformation matrix from the Image Volume coordinate system
    # into RAS coordinates.
    ijk2ras4x4 = vtk.vtkMatrix4x4()
    inputVolume.GetIJKToRASMatrix(ijk2ras4x4)

    # Get the center of mass of the first volume, then turn it into a 4D
    # point, so the matrix multiplication works. Then do the multiplication,
    # and output the center of mass to the console.
    center1 = self.getCenterOfMass(inputVolume)
    center1.append(1)
    center1 = ijk2ras4x4.MultiplyPoint(center1)
    print('Center of mass for \'' + inputVolume.GetName() + '\': ' + repr(center1))

    # Same as above, with the second input volume.
    center2 = self.getCenterOfMass(input2Volume)
    center2.append(1)
    center2 = ijk2ras4x4.MultiplyPoint(center2)
    print('Center of mass for \'' + input2Volume.GetName() + '\': ' + repr(center2))

    # Get the average of the two Centers of Mass to give the center of the
    # two objects.
    self.translation = []
    for i in [0,1,2]:
      self.translation.append((center2[i] + center1[i])/2)

    # Set the scale, color, location and label of the COM fiducial node.
    slicer.modules.markups.logic().SetDefaultMarkupsDisplayNodeGlyphScale(5.0)
    slicer.modules.markups.logic().SetDefaultMarkupsDisplayNodeTextScale(5.0)
    slicer.modules.markups.logic().SetDefaultMarkupsDisplayNodeColor(0.0, 0.0, 0.0)
    slicer.modules.markups.logic().SetDefaultMarkupsDisplayNodeSelectedColor(0.0, 0.0, 0.0)
    slicer.modules.markups.logic().AddNewFiducialNode()
    slicer.modules.markups.logic().AddFiducial(self.translation[0],self.translation[1],self.translation[2])
    fidList = slicer.util.getNode('F')
    numFids = fidList.GetNumberOfFiducials()
    fidStr = "COM: " + inputVolume.GetName() + ", " + input2Volume.GetName()
    for n in range(numFids):
      fidList.SetNthFiducialLabel(n, fidStr)

    # Return true to indicate success!
    return True