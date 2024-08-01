'''
class for viewing emitter
'''
import napari
import pyqtgraph as pg
from PyQt5.QtGui import QColor, QPen
from qtpy.QtWidgets import QLabel, QSizePolicy
from qtpy.QtCore import Qt

import numpy as np


class EmitterImageViewer():
    ''' main class for viewing emitter Images'''
    #TODO: finish the class

    def __init__(self,emitterImage, **kwargs):
        ''' initialise the class '''
    
        # data parameter
        self.emitterImage=emitterImage  # spectral 3D image

        self.viewer = None
        self.signalGraph = None

        # set this qui of this class
        EmitterImageViewer._setWidget(self)

    def _setWidget(self):
        ''' prepare the gui '''

        self.viewer = napari.Viewer()

        # add image layer
        self.dataLayer = self.viewer.add_image(self.emitterImage.getImageSet(), rgb=False, colormap="gray", 
                                            name='Data', blending='additive')
  
        # add widget spectraGraph
        self.signalGraph = pg.plot()
        self.signalGraph.setTitle(f'Signal')
        styles = {'color':'r', 'font-size':'20px'}
        self.signalGraph.setLabel('left', 'Intensity', units='a.u.')
        self.signalGraph.setLabel('bottom', 'Index ', units= 'a.u.')
        dw = self.viewer.window.add_dock_widget(self.signalGraph, name = 'signal')

        self.drawSignal()

        # connect events in napari
        # connect changes of the slicer in the viewer
        self.viewer.dims.events.current_step.connect(self.updateLine)


    def drawSignal(self):
        ''' draw lines in the signalGraph '''
        # remove all lines
        self.signalGraph.clear()
        lineplot = self.spectraGraph.plot()
        lineplot.setData(self.emitterImage.getSignal())

    def updateLine(self):
        ''' update vertial line '''
        pass

    def run(self):
        ''' start napari engine '''
        napari.run()

if __name__ == "__main__":
    import pytest
    #retcode = pytest.main(['tests/test_spectralViewer.py::test_XYWViewer'])

        














