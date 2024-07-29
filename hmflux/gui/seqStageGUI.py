'''
class for tracking of plasmon peaks
'''
#%%
from pathlib import Path
import numpy as np
import time

from viscope.gui.baseGUI import BaseGUI
from magicgui import magicgui
from viscope.gui.napariGUI import NapariGUI

class SeqStageGUI(BaseGUI):
    ''' main class to save image'''

    DEFAULT = {'nameGUI': 'Seq Stage',
               }

    def __init__(self, viscope, **kwargs):
        ''' initialise the class '''
        super().__init__(viscope, **kwargs)

        self.viewer = None

        # prepare the gui of the class
        SeqStageGUI.__setWidget(self) 

    def __setWidget(self):
        ''' prepare the gui '''

        @magicgui(filePath={"label": "Saving main Path:","mode":'d'},
                  fileName={"label": "Saving folder name:"},
                            fileIdx = {"label": "File Index"},
                stepX={'min':-10,'max':10},
                stepY={'min':-10,'max':10})
        def seqGui(filePath= Path(self.viscope.dataFolder),
                   fileName:str = 'dataset',
                   fileIdx=0,
                   idxIncrement = True,
                   numberOfImage: int = 10,
                   stepX: float = 0.1,
                   stepY: float = 0):
            
            if idxIncrement:
                self.device.dataFolder = str(filePath /(fileName + f'_{fileIdx:03d}'))
                seqGui.fileIdx.value += 1
            else:
                self.device.dataFolder = str(filePath /fileName)
            
            self.device.numberOfImage = numberOfImage
            self.device.shiftVector = np.array([stepX,stepY,0])

            # create napari viewer if not existing
            if self.viewer is None:
                _vWindow = self.viscope.addViewerWindow()
                newGUI  = NapariGUI(viscope=self.viscope,vWindow=_vWindow)
                self.viewer = newGUI.viewer
                # set napari layer
                self.dataLayer = self.viewer.add_image(np.ones((2,2)),
                                rgb=False, colormap="gray",
                                name='data',  blending='additive')
            
            # pause camera threading if exist
            if self.device.camera.worker is not None:
                self.device.camera.worker.pause()
                while not self.device.camera.worker.is_running:
                    time.sleep(.1)

            # create thread for the sequencer
            self.device.setParameter('threading', True)
            # connect signals
            self.device.worker.yielded.connect(self.guiUpdateTimed)
            self.device.worker.finished.connect(self.afterProcess)

            # start the sequencer
            self.device.worker.start()

        # add widgets 
        self.seqGui = seqGui
        self.vWindow.addParameterGui(self.seqGui,name=self.DEFAULT['nameGUI'])
 
    def setDevice(self,device):
        super().setDevice(device)
        self.seqGui.filePath.value = Path(self.device.dataFolder).parent
        self.seqGui.fileName.value = str(Path(self.device.dataFolder).stem)

    def updateGui(self):
        ''' update the data in gui '''
        self.dataLayer.data = self.device.image

    def afterProcess(self):
        ''' steps to do after the sequencer has finished'''

        # show the whole data
        self.dataLayer.data = self.device.imageSet

        # resume working camera thread
        if self.device.camera.worker is not None:
                self.device.camera.worker.resume()    
        




if __name__ == "__main__":
    pass


