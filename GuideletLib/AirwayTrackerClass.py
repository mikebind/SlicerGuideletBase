""" Modeled on UltraSound.py in GuideletLib """

import os
from __main__ import vtk, qt, ctk, slicer
import logging
import time

class AirwayTrackerClass(object):
  #DEFAULT_IMAGE_SIZE = [800, 600, 1]

  def __init__(self, guideletParent):
    self.guideletParent = guideletParent # this will be ExampleGuidelet?
    self.captureDeviceName = self.guideletParent.parameterNode.GetParameter('PLUSCaptureDeviceName')
    self.referenceToRas = None

    try:
      slicer.modules.plusremote
    except:
      raise Exception('Error: Could not find Plus Remote module. Please install the SlicerOpenIGTLink extension')
      return

    self.plusRemoteLogic = slicer.modules.plusremote.logic()
    self.plusRemoteNode = None

    fileDir = os.path.dirname(__file__)
    iconPathRecord = os.path.join(fileDir, 'Resources', 'Icons', 'icon_Record.png') 
    iconPathStop = os.path.join(fileDir, 'Resources', 'Icons', 'icon_Stop.png')

    if os.path.isfile(iconPathRecord):
      self.recordIcon = qt.QIcon(iconPathRecord)
    if os.path.isfile(iconPathStop):
      self.stopIcon = qt.QIcon(iconPathStop)



  


  # NOTE: UNUSED CURRENTLY 
  def setupResliceDriver(self):
    layoutManager = slicer.app.layoutManager()
    # Show ultrasound in red view.
    redSlice = layoutManager.sliceWidget('Red')
    redSliceLogic = redSlice.sliceLogic()
    redSliceLogic.GetSliceCompositeNode().SetBackgroundVolumeID(self.liveUltrasoundNode_Reference.GetID())
    # Set up volume reslice driver.
    resliceLogic = slicer.modules.volumereslicedriver.logic()
    if resliceLogic:
      redNode = slicer.mrmlScene.GetNodeByID('vtkMRMLSliceNodeRed')
      # Typically the image is zoomed in, therefore it is faster if the original resolution is used
      # on the 3D slice (and also we can show the full image and not the shape and size of the 2D view)
      redNode.SetSliceResolutionMode(slicer.vtkMRMLSliceNode.SliceResolutionMatchVolumes)
      resliceLogic.SetDriverForSlice(self.liveUltrasoundNode_Reference.GetID(), redNode)
      resliceLogic.SetModeForSlice(6, redNode) # Transverse mode, default for PLUS ultrasound.
      resliceLogic.SetFlipForSlice(False, redNode)
      resliceLogic.SetRotationForSlice(180, redNode)
      redSliceLogic.FitSliceToAll()
    else:
      logging.warning('Logic not found for Volume Reslice Driver')

    self.liveUltrasoundNode_Reference.SetAndObserveTransformNodeID(self.referenceToRas.GetID())

