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
    self.inputSelector.setMRMLScene(slicer.mrmlScene)

    # Tooltips and the label for the combobox.
    self.inputSelector.setToolTip( "Pick the first input to the algorithm." )
    parametersFormLayout.addRow("Input Volume 1: ", self.inputSelector)

    ######################################################################################
    # STEP 1
    # Create an additional input volume selector named 'input2Selector', and give it the 
    # same parameters and attributes as the first input selector.
    ######################################################################################

    # Apply Button
    # Defines the button and sets it to be unclickable (for now...)
    self.applyButton = qt.QPushButton("Apply")
    self.applyButton.toolTip = "Run the algorithm."
    self.applyButton.enabled = False
    parametersFormLayout.addRow(self.applyButton)

    # QLabel Text Field
    ######################################################################################
    # STEP 2
    # Create a QLabel called 'outputLabel' and add it to the module's layout. This will
    # display the Center of Mass to the GUI after running the main logic of the module.
    ######################################################################################
    

    # Connections
    self.applyButton.connect('clicked(bool)', self.onApplyButton)
    ######################################################################################
    # STEP 3
    # Create the connections for the input selectors to the the onSelect function to make
    # sure that the apply button is only selectable when both are picked.
    ######################################################################################

    # Add vertical spacer
    self.layout.addStretch(1)

    # Refresh Apply button state
    self.onSelect()

  # We don't need this for this module
  def cleanup(self):
    pass

  # When the node selectors both contain valid nodes (they can be the same node - we want the
  # center of just one point), the apply button becomes clickable!
  def onSelect(self):
    self.applyButton.enabled = self.inputSelector.currentNode() and self.input2Selector.currentNode()

  # When the apply button is clicked, a new instance of the logic is created,
  # and the algorithm is run using the inputted nodes from the selectors.
  # The output label text is also updated with the coordinates of the Center of Mass.
  def onApplyButton(self):
    logic = MyFirstModuleLogic()
    logic.run(self.inputSelector.currentNode(), self.input2Selector.currentNode())
    ######################################################################################
    # STEP 12
    # Set the output label text to display the string representation of each value in the
    # comVector vector.
    ######################################################################################
    
# The logic for the Module.
class MyFirstModuleLogic(ScriptedLoadableModuleLogic):

  # This function gets the center of mass of a given volume node.
  def getCenterOfMass(self, volumeNode):

    # Define some necessary variables for later.
    centerOfMass = [0,0,0]
    numberOfStructureVoxels = 0
    sumX = sumY = sumZ = 0

    ######################################################################################
    # STEP 5
    # Get the image data from the volume node so that we can find the center of mass.
    ######################################################################################

    # Uses the extent of the image to get the range for the loops,
    # Then if the value of the given voxel is > zero we add the 
    # value of the voxel coordinate to the running sums, and the
    # count of voxels is incremented.

    ######################################################################################
    # STEP 6
    # Loop through the Z, Y and then X direction by using the extent of the image volumes.
    # The extent of the X direction will be in indices 0 and 1 of the extent, Y direction
    # will be 2 and 3, Z will be 4 and 5. To make things a bit faster, have your loops go 
    # up by 2 each iteration.
    ######################################################################################
    '''
    for z ...
      for y ...
        for x ...
          voxelValue = volume.GetScalarComponentAsDouble(x, y, z, 0)
          if voxelValue > 0:
            numberOfStructureVoxels = numberOfStructureVoxels + 1
            sumX = sumX + x
            sumY = sumY + y
            sumZ = sumZ + z
	'''
    # When the loop terminates, if we had any voxels, we calculate
    # the Center of Mass by dividing the sums by the number of voxels
    # in total.
    if numberOfStructureVoxels > 0:
      pass
      ######################################################################################
      # STEP 7
      # Compute the center of mass for each of the X Y Z directions and do this by dividing
      # the summed values by the number of voxels that were used.
      ######################################################################################

    # Return the point that contains the center of mass location.
    return centerOfMass 

  def run(self, inputVolume, input2Volume):

    # Get the transformation matrix from the Image Volume coordinate system
    # into RAS coordinates.
    ijk2ras4x4 = vtk.vtkMatrix4x4()
    ######################################################################################
    # STEP 4
    # Get the IJKToRAS Matrix for the first input volume.
    ######################################################################################

    ######################################################################################
    # STEP 8
    # Get the center of mass of the first input volume and store that in a variable called
    # 'center1'. Append a 1 to the end so we may multiply by a 4x4 matrix, and then mult.
    # the center1 point by the IJKToRAS Matrix.
    ######################################################################################
    print('Center of mass for \'' + inputVolume.GetName() + '\': ' + repr(center1))

    ######################################################################################
    # STEP 9
    # Same as above, with the second input volume and center2.
    ######################################################################################
    print('Center of mass for \'' + input2Volume.GetName() + '\': ' + repr(center2))

    # Get the average of the two Centers of Mass to give the center of the
    # two objects.
    self.comVector = []
    for i in [0, 1, 2]:
      self.comVector.append((center2[i] + center1[i]) / 2)

    # Sets the scale, color, location and label of the COM fiducial node.
    markupsLogic = slicer.modules.markups.logic()
    markupsLogic.SetDefaultMarkupsDisplayNodeGlyphScale(5.0)
    markupsLogic.SetDefaultMarkupsDisplayNodeTextScale(5.0)
    markupsLogic.SetDefaultMarkupsDisplayNodeColor(0.0, 0.0, 0.0)
    markupsLogic.SetDefaultMarkupsDisplayNodeSelectedColor(0.0, 0.0, 0.0)
    markupsLogic.AddNewFiducialNode()
    ######################################################################################
    # STEP 10
    # Add the fiducial that has the values of the comVector.
    ######################################################################################
    fidList = slicer.util.getNode('F')
    numFids = fidList.GetNumberOfFiducials()
    ######################################################################################
    # STEP 11
    # Create the 'fidStr' which will display the names of the input volumes as the name
    # of the fiducial.
    ######################################################################################
    for n in range(numFids):
      fidList.SetNthFiducialLabel(n, fidStr)

    # Return true to indicate success.
    return True
