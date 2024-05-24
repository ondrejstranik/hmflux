'''
class for live viewing spectral images
'''
#%%

from viscope.main import viscope
from viscope.gui.allDeviceGUI import AllDeviceGUI 
from plim.gui.plasmonViewerGUI import PlasmonViewerGUI
from plim.gui.positionTrackGUI import PositionTrackGUI
from viscope.gui.cameraGUI import CameraGUI
from viscope.gui.cameraViewGUI import CameraViewGUI
from plim.gui.saveDataGUI import SaveDataGUI

from viscope.instrument.virtual.virtualCamera import VirtualCamera
from spectralCamera.algorithm.calibrateIFImage import CalibrateIFImage
from spectralCamera.instrument.sCamera.sCamera import SCamera
from viscope.instrument.virtual.virtualStage import VirtualStage
from viscope.instrument.virtual.virtualPump import VirtualPump
from plim.instrument.plasmonProcessor import PlasmonProcessor

from plim.virtualSystem.plimMicroscope import PlimMicroscope

import numpy as np
from pathlib import Path

class HMFlux():
    ''' base top class for control'''

    DEFAULT = {}

    @classmethod
    def run(cls):
        '''  set the all the parameter and then run the GUI'''

        # some global settings
        viscope.dataFolder = str(Path(__file__).parent.joinpath('DATA'))

        #camera
        camera = VirtualCamera(name='BWCamera')
        camera.connect()
        camera.setParameter('exposureTime', 300)
        camera.setParameter('nFrame', 1)
        camera.setParameter('threadingNow',True)

        # set GUIs
        viewer  = AllDeviceGUI(viscope)
        viewer.setDevice([camera])

        # main event loop
        viscope.run()

        camera.disconnect()


if __name__ == "__main__":

    Plim.run()


