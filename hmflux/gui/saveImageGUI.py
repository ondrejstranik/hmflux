'''
class for tracking of plasmon peaks
'''
#%%
from pathlib import Path
import numpy as np

from viscope.gui.baseGUI import BaseGUI
from magicgui import magicgui

# from hmflux.instrument.stage.smarACT.smarACTStage import SmarACTStage
# from hmflux.gui.slmViewer import SLMViewer

class SaveImageGUI(BaseGUI):
    ''' main class to save image'''

    DEFAULT = {'nameGUI': 'Save Image',
               'autoGUI': 'Auto Save'
               }

    def __init__(self, viscope, **kwargs):
        ''' initialise the class '''
        super().__init__(viscope, **kwargs)

        # self.smartInstance = SmarACTStage()
        # self.slmInstance = SLMViewer(show=False)


        # prepare the gui of the class
        SaveImageGUI.__setWidget(self) 

    def __setWidget(self):
        ''' prepare the gui '''

        @magicgui(filePath={"label": "Saving file Path:","mode":'d'},
                fileName={"label": "Saving file Name:"},
                fileIdx = {"label": "File Index:"})
        def saveGui(filePath= Path(self.viscope.dataFolder), fileName: str = 'Image', fileIdx=0,idxIncrement=True):

            np.save(str(filePath / fileName) + f'_{fileIdx:03d}',self.device.rawImage)            

            if idxIncrement:
                saveGui.fileIdx.value = saveGui.fileIdx.value + 1 


        # add widgets 
        self.saveGui = saveGui
        self.vWindow.addParameterGui(self.saveGui,name=self.DEFAULT['nameGUI'])
        # self.autoSaveGui = autoSaveGui
        # self.vWindow.addParameterGui(self.autoSaveGui,name=self.DEFAULT['autoGUI'])


 

if __name__ == "__main__":
    pass


