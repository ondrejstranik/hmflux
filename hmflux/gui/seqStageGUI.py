'''
class for tracking of plasmon peaks
'''
#%%
from pathlib import Path
import numpy as np

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

        @magicgui(filePath={"label": "Saving file Path:","mode":'d'},
                )
        def seqGui(filePath= Path(self.viscope.dataFolder),
                   numberOfImage: int = 10):
            self.device.dataFolder = str(filePath)
            self.device.numberOfImage = numberOfImage

            # create napari viewer
            newGUI  = NapariGUI(self.viscope)
            self.viewer = newGUI.viewer

            # set new napari layer
            self.dataLayer = self.viewer.add_image(np.ones((2,2)),
                            rgb=False, colormap="gray",
                            name='data',  blending='additive')
            
            # run the sequencer
            self.device.worker.start()

        # add widgets 
        self.seqGui = seqGui
        self.vWindow.addParameterGui(self.seqGui,name=self.DEFAULT['nameGUI'])
 
    def setDevice(self,device):
        super().setDevice(device)

        # connect signals
        self.device.worker.yielded.connect(self.guiUpdateTimed)

    def updateGui(self):
        ''' update the data in gui '''
        self.dataLayer = self.device.image


if __name__ == "__main__":
    pass


