'''
class for live viewing spectral images
'''
#%%
from viscope.gui.baseGUI import BaseGUI
from hmflux.gui.slmViewer import SLMViewer
from magicgui import magicgui
import numpy as np

class SLMGui(BaseGUI):
    ''' main class to show control SLM'''

    DEFAULT = {'nameGUI': 'slm'}

    def __init__(self, viscope, **kwargs):
        ''' initialise the class '''
        super().__init__(viscope, **kwargs)

        self.liveUpdate = False

        # prepare the gui of the class
        SLMGui.__setWidget(self) 

    def _liveUpdate(self):
        ''' internal use. set the image on the slm 
        and update the slm preview'''
        self.device.setImage(self.slmViewer.imageSLM.image)
        self.onDeviceImageLayer.data = self.device.image


    def __setWidget(self):
        ''' prepare the gui '''

        @magicgui()
        def parameterSLMGui(liveUpdate = self.liveUpdate):
            
            self.liveUpdate = liveUpdate 
            self._liveUpdate()

        # add widget parameterCameraGui 
        self.parameterSLMGui = parameterSLMGui
        self.dw =self.vWindow.addParameterGui(self.parameterSLMGui,name=self.DEFAULT['nameGUI'])

        # add widget slmviewer 
        self.slmViewer = SLMViewer(show=False)
        self.viewer = self.slmViewer.viewer
        self.vWindow.addMainGUI(self.viewer.window._qt_window, name=self.DEFAULT['nameGUI'])

        # add new layer
        self.onDeviceImageLayer = self.viewer.add_image(np.zeros((2,2)), name='onDeviceImage')
     
        # connect signal from slmviewer for liveupdate
        self.slmViewer.sinWaveGui.changed.connect(
            lambda: self._liveUpdate() if self.liveUpdate else None
            )
        self.slmViewer.binaryGui.changed.connect(
            lambda: self._liveUpdate() if self.liveUpdate else None
            )

    def setDevice(self,device):
        super().setDevice(device)
        
        self.slmViewer.imageSLM.setSizeSLM(sizeX =self.device.sizeX,sizeY = self.device.sizeY)
        
        self.onDeviceImageLayer.data = self.device.image



if __name__ == "__main__":
    pass

