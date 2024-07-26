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


        # @magicgui(filePath={"label": "Saving file Path:","mode":'d'},
        #         fileName={"label": "Saving file Name:"},
        #         fileIdx = {"label": "File Index:"},
        #         stageX = {"widget_type": "FloatSpinBox","value":0,"step":0.01},
        #         stageY = {"widget_type": "FloatSpinBox","value":0,"step":0.01},
        #         stageZ = {"widget_type": "FloatSpinBox","value":0,"step":0.01},
        #         imageAmount = {"widget_type":"SpinBox","value":1})
        # def autoSaveGui(filePath= Path(self.viscope.dataFolder), fileName: str = 'Image', fileIdx=0,idxIncrement=True,slmX=0,slmY=0,slmZ=0,imageAmount=1):
        #     constantImage = []
        #     sinusImage = []

        #     for i in range(imageAmount-1):
        #         # self.slmInstance.choiceGui('constant')
        #         constantImage.append(self.device.rawImage)
        #         # choiceGui('sinus')
        #         sinusImage.append(self.device.rawImage)
        #         if stageX != 0:
        #             move(slmX,'X')
        #         elif stageY != 0 :
        #             move(slmY,'Y')
        #         elif stageZ != 0:
        #             move(slmZ,'Z')

                
                        
        #     np.save(str(filePath / fileName) + f'_{fileIdx}',self.device.rawImage) 
        #     if idxIncrement:
        #         autoSaveGui.fileIdx.value = saveGui.fileIdx.value + 1


        # add widgets 
        self.saveGui = saveGui
        self.vWindow.addParameterGui(self.saveGui,name=self.DEFAULT['nameGUI'])
        # self.autoSaveGui = autoSaveGui
        # self.vWindow.addParameterGui(self.autoSaveGui,name=self.DEFAULT['autoGUI'])


 

if __name__ == "__main__":
    pass


