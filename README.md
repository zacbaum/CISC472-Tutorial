# CISC472 Programming Tutorial
Friday March 3rd, 2017

## Purpose:
This tutorial is meant to help you learn to find relevant documentation, pull code from existing sources, and implement code in 3DSlicer.

## Installation:
Clone or Fork this repository locally, then add the directory ```src``` to your list of modules in 3DSlicer so that it will be loaded when 3DSlicer starts up.

## What We're Going To Do:
We're going to create a module that takes two Label Maps, and finds the center of mass between them. It will output each Label Map's center of mass to the python console, and it will output the center of mass between the two in the module in a QLabel on the module's GUI.

To do this, we're going to need to add a few things to the module we've given you:

### First:
Let's load ```MyFirstModule.py``` that we've placed in the repository here for you.

### Next:
Follow the comments in the code to see what we need to do as we work our way through what happens.
- We'll start with the GUI and the connections for all our buttons,
- Then we'll move into the algorithm for finding the center of mass of a labelmap,
- Then we're going to handle the output of our program:
  1. Printing to the Python Console,
  2. Filling in a QLabel in the GUI,
  3. Drawing a labelled fiducial marker in the COM on the 3D Viewer.

## Helpful Links:
[QT](http://doc.qt.io/qt-4.8/classes.html) - QT GUI code documentation.
- Here we're going to look specifically at QLabel & QPushButton.

[VTK](http://www.vtk.org/doc/release/6.2/html/classes.html) - Visualization Toolkit documentation.
- Here we're going to want to look at the vtkMatrix4x4.

[MRML / Slicer](https://www.slicer.org/doc/html/classes.html) - Slicer Documentation.
- Here we're going to look at the vtkMRMLLabelMapVolumeNode & qMRMLNodeComboBox.
