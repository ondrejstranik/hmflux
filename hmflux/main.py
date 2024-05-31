'''
main class for holo min flux
'''
#%%

from viscope.main import viscope
from viscope.gui.allDeviceGUI import AllDeviceGUI    
from hmflux.gui.saveImageGUI import SaveImageGUI
from hmflux.gui.slmGUI import SLMGUI

from pathlib import Path

class HMFlux():
    ''' base top class for control'''

    DEFAULT = {}

    @classmethod
    def runReal(cls):
        '''  set the all the parameter and then run the GUI'''

        from hmflux.instrument.camera.andorCamera.andorCamera import AndorCamera
        from hmflux.instrument.slm.screenSlm.screenSLM import ScreenSLM


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
        newGUI  = SaveImageGUI(viscope)
        newGUI.setDevice(camera)

        # main event loop
        viscope.run()

        camera.disconnect()


    @classmethod
    def runVirtual(cls):
        '''  set the all the parameter and then run the GUI'''
        from viscope.instrument.virtual.virtualCamera import VirtualCamera
        from viscope.instrument.virtual.virtualSLM import VirtualSLM
        from viscope.instrument.virtual.virtualStage import VirtualStage

        # some global settings
        viscope.dataFolder = str(Path(__file__).parent.joinpath('DATA'))

        #camera
        camera = VirtualCamera(name='VirtualCamera')
        camera.connect()
        camera.setParameter('exposureTime', 300)
        camera.setParameter('nFrame', 1)
        camera.setParameter('threadingNow',True)

        # slm
        slm = VirtualSLM()
        slm.connect()

        # stage
        stage = VirtualStage('stage')
        stage.connect()

        # set GUIs
        newGUI = AllDeviceGUI(viscope)
        newGUI.setDevice([camera,stage])
        newGUI = SLMGUI(viscope)
        newGUI.setDevice(slm)
        newGUI = SaveImageGUI(viscope)
        newGUI.setDevice(camera)


        # main event loop
        viscope.run()

        camera.disconnect()
        stage.disconnect()
        slm.disconnect()


if __name__ == "__main__":

    HMFlux.runVirtual()


