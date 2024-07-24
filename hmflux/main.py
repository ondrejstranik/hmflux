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
        from hmflux.instrument.camera.teledyneCamera.teledyneCamera import TeledyneCamera
        from hmflux.instrument.camera.avCamera.avCamera import AVCamera        
        from hmflux.instrument.slm.screenSlm.screenSLM import ScreenSLM
        from hmflux.instrument.stage.smarACT.smarACTStage import SmarACTStage


        # some global settings
        viscope.dataFolder = str(Path(__file__).parent.joinpath('DATA'))

        # #camera
        # camera = AndorCamera(name='AndorCamera')
        # camera.connect()
        # camera.setParameter('exposureTime', 300)
        # camera.setParameter('nFrame', 1)
        # camera.setParameter('threadingNow',True)

        #camera
        camera = TeledyneCamera(name='TeledyneCamera')
        camera.connect()
        camera.setParameter('exposureTime', 300)
        camera.setParameter('nFrame', 1)
        camera.setParameter('threadingNow',True)

        #camera 2
        camera2 = AVCamera(name='AVCamera')
        camera2.connect()
        camera2.setParameter('exposureTime', 50)
        camera2.setParameter('nFrame', 1)
        camera2.setParameter('threadingNow',True)

        # slm
        slm = ScreenSLM('slm')
        slm.connect()

        # stage
        stage = SmarACTStage('stage')
        stage.connect()



        # set GUIs
        viewer  = AllDeviceGUI(viscope)
        viewer.setDevice([stage,camera,camera2])
        newGUI = SLMGUI(viscope)
        newGUI.setDevice(slm)
        newGUI  = SaveImageGUI(viscope)
        newGUI.setDevice(camera)

        # main event loop
        viscope.run()

        camera.disconnect()
        stage.disconnect()
        slm.disconnect()        


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

    HMFlux.runReal()

#%%
