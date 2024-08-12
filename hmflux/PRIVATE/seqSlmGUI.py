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



class SeqSlmGUI(BaseGUI):
    ''' main class to save image'''

    DEFAULT = {'nameGUI': 'Seq SLM',
               }

    def __init__(self, viscope, **kwargs):
        ''' initialise the class '''
        super().__init__(viscope, **kwargs)

        self.viewer = None
        self.emitterDataGUI=None
        self.cameraViewGUI=None

        # prepare the gui of the class
        SeqSlmGUI.__setWidget(self) 

    def __setWidget(self):
        ''' prepare the gui '''

        @magicgui(filePath={"label": "Saving main Path:","mode":'d'},
                  fileName={"label": "Saving folder name:"},
                            fileIdx = {"label": "File Index"},
                val0={'min':0,'max':255},
                val1={'min':0,'max':255},
                initialDifference={'min':1,'max':255},
                axis={'min':0,'max':1},
                constantVal={'min':0,'max':255},
                laserPower = {'max':240})
        def seqGui(filePath= Path(self.viscope.dataFolder),
                   fileName:str = 'dataset',
                   fileIdx=0,
                   val0: int = 0,
                   val1: int = 255,
                   initialDifference: int = 1,
                   endDifference: int = 255,
                   axis: int = 0,
                   constantVal: int = 0,
                   laserPower: float = 10,
                   idxIncrement = True):
            
            if idxIncrement:
                self.device.dataFolder = str(filePath /(fileName + f'_{fileIdx:03d}'))
                seqGui.fileIdx.value += 1
            else:
                self.device.dataFolder = str(filePath /fileName)
            
            self.device.valMin = val0
            self.device.valMax = val1
            self.device.constantVal = constantVal
            self.device.initialDifference = initialDifference
            self.device.endDifference = endDifference
            self.device.binaryAxis = axis
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


