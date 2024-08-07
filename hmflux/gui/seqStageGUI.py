'''
class for tracking of plasmon peaks
'''
#%%
from pathlib import Path
import numpy as np
import time

from viscope.gui.baseGUI import BaseGUI

from magicgui import magicgui
from hmflux.algorithm.emitterImage import EmitterImage
from hmflux.gui.emitterImageGUI import EmitterImageGUI



class SeqStageGUI(BaseGUI):
    ''' main class to save image'''

    DEFAULT = {'nameGUI': 'Seq Stage',
               }

    def __init__(self, viscope, **kwargs):
        ''' initialise the class '''
        super().__init__(viscope, **kwargs)

        self.viewer = None
        self.emitterDataGUI=None
        self.cameraViewGUI=None

        # prepare the gui of the class
        SeqStageGUI.__setWidget(self) 

    def __setWidget(self):
        ''' prepare the gui '''

        @magicgui(filePath={"label": "Saving main Path:","mode":'d'},
                  fileName={"label": "Saving folder name:"},
                            fileIdx = {"label": "File Index"},
                stepX={'min':-10,'max':10},
                stepY={'min':-10,'max':10},
                laserPower = {'max':240})
        def seqGui(filePath= Path(self.viscope.dataFolder),
                   fileName:str = 'dataset',
                   fileIdx=0,
                   idxIncrement = True,
                   numberOfImage: int = 10,
                   stepX: float = 0.1,
                   stepY: float = 0,
                   laserPower: float = 10):
            
            if idxIncrement:
                self.device.dataFolder = str(filePath /(fileName + f'_{fileIdx:03d}'))
                seqGui.fileIdx.value += 1
            else:
                self.device.dataFolder = str(filePath /fileName)
            
            self.device.numberOfImage = numberOfImage
            self.device.shiftVector = np.array([stepX,stepY,0])
            self.device.laserPower = laserPower

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

            # set roi if processor exist
            if self.emitterDataGUI is not None and self.emitterDataGUI.device is not None:
                self.device.roi = [self.emitterDataGUI.device.xPos,
                                   self.emitterDataGUI.device.yPos,
                                   self.emitterDataGUI.device.deltaX,
                                   self.emitterDataGUI.device.deltaY]

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
        # update other gui as well
        if self.emitterDataGUI is not None and self.emitterDataGUI.device is not None:
            self.emitterDataGUI.device.flagToProcess.set()
        if self.cameraViewGUI is not None:
            self.cameraViewGUI.updateGui()

    def interconnectGui(self,emitterDataGUI=None,cameraViewGUI=None):
        ''' interconnect action with other GUI'''
        self.emitterDataGUI = emitterDataGUI
        self.cameraViewGUI = cameraViewGUI

    def afterProcess(self):
        ''' steps to do after the sequencer has finished'''

        # show the whole data
        eiGui = EmitterImageGUI(viscope=self.viscope,vWindow='new')
        eiGui.setData(EmitterImage(self.device.imageSet))

        # resume working camera thread
        if self.device.camera.worker is not None:
                self.device.camera.worker.resume()        


if __name__ == "__main__":
    pass


