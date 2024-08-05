'''
class for viewing emitter
'''
import napari
import pyqtgraph as pg
from PyQt5.QtGui import QColor, QPen
from qtpy.QtWidgets import QLabel, QSizePolicy
from qtpy.QtCore import Qt
from hmflux.algorithm.emitterImage import EmitterImage

import numpy as np


class EmitterImageViewer():
    ''' main class for viewing emitter Images'''
    #TODO: finish the class

    def __init__(self,emitterImage:EmitterImage=None, **kwargs):
        ''' initialise the class '''
    
        # data parameter
        self.emitterImage=emitterImage  # spectral 3D image

        # gui parameter
        self.signalGraph = None
        self.signalLine = None
        self.vLine = None

        # napari
        if 'show' in kwargs:
            self.viewer = napari.Viewer(show=kwargs['show'])
        else:
            self.viewer = napari.Viewer()


        # set this qui of this class
        EmitterImageViewer._setWidget(self)

    def _setWidget(self):
        ''' prepare the gui '''

        # add image layer
        self.dataLayer = self.viewer.add_image(np.zeros((2,2)), rgb=False, colormap="gray", 
                                            name='Data', blending='additive')
  
        # add widget spectraGraph
        self.signalGraph = pg.plot()
        self.signalGraph.setTitle(f'Signal')
        #styles = {'color':'r', 'font-size':'20px'}
        self.signalGraph.setLabel('left', 'Intensity', units='a.u.')
        self.signalGraph.setLabel('bottom', 'Index ', units= 'a.u.')
        
        self.signalLine = self.signalGraph.plot()
        self.vLine = pg.InfiniteLine(movable=False)
        self.signalGraph.addItem(self.vLine)
        
        dw = self.viewer.window.add_dock_widget(self.signalGraph, name = 'signal')

        self.updateViewer()
        # connect events in napari
        # connect changes of the slicer in the viewer
        self.viewer.dims.events.current_step.connect(self.updateVLine)


    def updateViewer(self):
        ''' draw lines in the signalGraph and the imageSet in the viewer'''
        
        if self.emitterImage is not None:
            self.signalLine.setData(self.emitterImage.getSignal())
            self.dataLayer.data = self.emitterImage.getImageSet()
        

    def updateVLine(self):
        ''' update vertical line '''
        self.vLine.setPos(int(self.viewer.dims.point[0]))

    def setEmitterImage(self,emitterImage:EmitterImage):
        self.emitterImage = emitterImage
        self.updateViewer()

    def run(self):
        ''' start napari engine '''
        napari.run()

if __name__ == "__main__":
    pass

        














