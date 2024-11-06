'''
class for live viewing spectral images
'''
#%%
from viscope.gui.baseGUI import BaseGUI
from hmflux.gui.slmViewer import SLMViewer
from magicgui import magicgui
import numpy as np

class SLMGUI(BaseGUI):
    ''' main class to show control SLM'''

    DEFAULT = {'nameGUI': 'slm'}

    def __init__(self, viscope, **kwargs):
        ''' initialise the class '''
        super().__init__(viscope, **kwargs)

        self.liveUpdate = False

        # prepare the gui of the class
        SLMGUI.__setWidget(self) 

    def _liveUpdate(self):
        ''' internal use. set the image on the slm 
        and update the slm preview'''
        self.device.setImage(self.slmViewer.imageSLM.image)
        self.onDeviceImageLayer.data = self.device.image


    def __setWidget(self):
        ''' prepare the gui '''

        @magicgui()
        def parameterSLMGUI(liveUpdate = self.liveUpdate):
            
            self.liveUpdate = liveUpdate 
            self._liveUpdate()

        # add widget parameterCameraGui 
        self.parameterSLMGUI = parameterSLMGUI
        self.dw =self.vWindow.addParameterGui(self.parameterSLMGUI,name=self.DEFAULT['nameGUI'])

        # add widget slmviewer 
        self.slmViewer = SLMViewer(show=False)
        self.viewer = self.slmViewer.viewer
        self.vWindow.addMainGUI(self.viewer.window._qt_window, name=self.DEFAULT['nameGUI'])

        # add new layer
        self.onDeviceImageLayer = self.viewer.add_image(
            np.zeros((2,2)), name='onDeviceImage', colormap='green',
            contrast_limits= (0,255), opacity=0.5)
     
        # connect signal from slmviewer for liveupdate
        self.slmViewer.sinWaveGui.changed.connect(
            lambda: self._liveUpdate() if self.liveUpdate else None)
        self.slmViewer.slanted3Gui.changed.connect(
            lambda: self._liveUpdate() if self.liveUpdate else None)
        self.slmViewer.slantedGui.changed.connect(
            lambda: self._liveUpdate() if self.liveUpdate else None)
        self.slmViewer.slanted8Gui.changed.connect(
            lambda: self._liveUpdate() if self.liveUpdate else None)
        self.slmViewer.binaryGui.changed.connect(
            lambda: self._liveUpdate() if self.liveUpdate else None)
        self.slmViewer.choiceGui.changed.connect(
            lambda: self._liveUpdate() if self.liveUpdate else None)
        self.slmViewer.constGui.changed.connect(
            lambda: self._liveUpdate() if self.liveUpdate else None)
        self.slmViewer.box1Gui.changed.connect(
            lambda: self._liveUpdate() if self.liveUpdate else None)
        self.slmViewer.box2Gui.changed.connect(
            lambda: self._liveUpdate() if self.liveUpdate else None)
        


    def setDevice(self,device):
        super().setDevice(device)
        
        self.slmViewer.imageSLM.setSizeSLM(sizeX =self.device.sizeX,sizeY = self.device.sizeY)
        
        self.onDeviceImageLayer.data = self.device.image



if __name__ == "__main__":
    pass

