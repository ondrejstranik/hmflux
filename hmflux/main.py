'''
main class for holo min flux
'''
#%%

from viscope.main import viscope
from viscope.gui.allDeviceGUI import AllDeviceGUI 

from hmflux.instrument.camera.andorCamera.andorCamera import AndorCamera

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
        camera = AndorCamera(name='AndorCamera')
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

    HMFlux.run()


