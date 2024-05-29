''' class for setting and viewing slm images'''

import napari

from magicgui import magicgui

from hmflux.algorithm.imageSLM import ImageSLM
import numpy as np

class SLMViewer():
    ''' main class to define and view SLM images'''

    def __init__(self,sizeX=200,sizeY=100, **kwargs):
        ''' initialise the class '''

        # data parameter
        self.imageSLM = ImageSLM()
        self.imageSLM.setSizeSLM(sizeX,sizeY)

        # initiate napari
        if 'show' in kwargs:
            self.viewer = napari.Viewer(show=kwargs['show'])
        else:
            self.viewer = napari.Viewer()
        self.imageLayer = self.viewer.add_image(self.imageSLM.image, name='setting Image')
        self.dockWidgetParameter = None


        # set gui of this class
        SLMViewer._setWidget(self)


    def _setWidget(self):
        ''' prepare the qui '''

        # set pyqt
        @magicgui(auto_call= 'True')
        def sinWaveGui(stepIdx = 0, nStep = 10):
            im = self.imageSLM.generateSinGrating(stepIdx,nStep)
            self.imageLayer.data = im

        @magicgui(auto_call= 'True')
        def binaryGui(axis = 0):
            im = self.imageSLM.generateBinaryGrating(axis=axis)
            self.imageLayer.data = im

        self.sinWaveGui = sinWaveGui
        self.binaryGui = binaryGui

        # add widget 
        dw = self.viewer.window.add_dock_widget(self.sinWaveGui, name ='sin', area='bottom')
        if self.dockWidgetParameter is not None:
            self.viewer.window._qt_window.tabifyDockWidget(self.dockWidgetParameter,dw)
        self.dockWidgetParameter = dw

        dw = self.viewer.window.add_dock_widget(self.binaryGui, name ='binary', area='bottom')
        self.viewer.window._qt_window.tabifyDockWidget(self.dockWidgetParameter,dw)
        self.dockWidgetParameter = dw


    def run(self):
        ''' start napari engine '''
        napari.run()

if __name__ == '__main__':
    pass

    
