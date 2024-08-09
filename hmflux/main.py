'''
main class for holo min flux
'''
#%%

from viscope.main import viscope
from viscope.gui.allDeviceGUI import AllDeviceGUI    
from viscope.gui.cameraGUI import CameraGUI
from viscope.gui.cameraViewGUI import CameraViewGUI
from viscope.gui.saveImageGUI import SaveImageGUI
from hmflux.gui.slmGUI import SLMGUI
from hmflux.gui.seqStageGUI import SeqStageGUI
from hmflux.gui.emitterDataGUI import EmitterDataGUI

from hmflux.PRIVATE.seqCameraGUI import SeqCameraGUI
from hmflux.PRIVATE.seqSlmGUI import SeqSlmGUI

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
        from hmflux.instrument.stageSequencer import StageSequencer
        from hmflux.instrument.hmfluxProcessor import HMFluxProcessor
        from hmflux.instrument.switch.throlabSwitch import ThrolabSwitch
        from hmflux.instrument.laser.coboltLaser import CoboltLaser

        from hmflux.PRIVATE.cameraSequencer import CameraSequencer
        from hmflux.PRIVATE.slmSequencerBi import SlmSequencerBi

        # some global settings
        # viscope.dataFolder = str(Path(__file__).parent.joinpath('DATA'))
        viscope.dataFolder = str(Path(r'E:\ZihaoData\DATA\PrimeBSI'))

        # stage
        # stage = SmarACTStage('stage')
        # stage.connect()

        # #camera
        # camera = AndorCamera(name='AndorCamera')
        # camera.connect()
        # camera.setParameter('exposureTime', 300)
        # camera.setParameter('nFrame', 1)
        # camera.setParameter('threadingNow',True)

        #camera
        # camera = TeledyneCamera(name='TeledyneCamera')
        # camera.connect()
        # camera.setParameter('exposureTime', 300)
        # camera.setParameter('nFrame', 1)
        # camera.setParameter('threadingNow',True)

        #camera 2
        camera2 = AVCamera(name='AVCamera')
        camera2.connect()
        camera2.setParameter('exposureTime', 50)
        camera2.setParameter('nFrame', 1)
        camera2.setParameter('threadingNow',True)

        # slm
        slm = ScreenSLM('slm')
        slm.connect()

        # switch
        switch = ThrolabSwitch('switch')
        switch.connect(port='COM6')
        switch.positionList = ['OD1','OD2','OD3','OD4','OD5','OD6']

        #laser
        laser = CoboltLaser()
        laser.connect()

        # stage Sequencer
        # seq = StageSequencer()
        # seq.connect(camera=camera2, stage=stage,slm=slm,laser=laser)
        seq = SlmSequencerBi()
        seq.connect(camera=camera2,slm=slm,laser=laser)

        # processor
        # hmfluxPro = HMFluxProcessor()
        # hmfluxPro.connect(camera=camera)
        # hmfluxPro.setParameter('threadingNow', True)

        hmfluxPro = HMFluxProcessor()
        hmfluxPro.connect(camera=camera2)
        hmfluxPro.setParameter('threadingNow', True)

        
        # set GUIs
        # adGui = AllDeviceGUI(viscope)
        # adGui.setDevice([stage,camera2,switch,laser])
        adGui = AllDeviceGUI(viscope)
        #adGui.setDevice([camera2,switch,laser])
        adGui.setDevice([switch,laser])
        # siGui = SaveImageGUI(viscope)
        # siGui.setDevice(camera)
        siGui2 = SaveImageGUI(viscope,name='2Save')
        siGui2.setDevice(camera2)

        # cGui = CameraGUI(viscope,vWindow='new')
        # cGui.setDevice(camera)
        # cvGui = CameraViewGUI(viscope,vWindow=cGui.vWindow)
        # cvGui.setDevice(camera)
        cGui = CameraGUI(viscope,vWindow='new')
        cGui.setDevice(camera2)
        cvGui = CameraViewGUI(viscope,vWindow=cGui.vWindow)
        cvGui.setDevice(camera2)
        slmGui = SLMGUI(viscope,vWindow='new')
        slmGui.setDevice(slm)
        edGui  = EmitterDataGUI(viscope,vWindow='new')
        edGui.setDevice(hmfluxPro)
        edGui.interconnectGui(cameraViewGUI=cvGui)
    
        # ssGui  = SeqStageGUI(viscope)
        # ssGui.setDevice(seq)
        # ssGui.interconnectGui(emitterDataGUI=edGui,cameraViewGUI=cvGui)
        ssGui  = SeqSlmGUI(viscope)
        ssGui.setDevice(seq)
        ssGui.interconnectGui(emitterDataGUI=edGui,cameraViewGUI=cvGui)

        # main event loop
        viscope.run()

        # camera.disconnect()
        # stage.disconnect()
        camera2.disconnect()
        slm.disconnect()        
        laser.disconnect()    
        switch.disconnect()


    @classmethod
    def runVirtual(cls):
        '''  set the all the parameter and then run the GUI'''
        from viscope.instrument.virtual.virtualCamera import VirtualCamera
        from viscope.instrument.virtual.virtualSLM import VirtualSLM
        from viscope.instrument.virtual.virtualStage import VirtualStage
        from viscope.instrument.virtual.virtualSwitch import VirtualSwitch
        from viscope.instrument.virtual.virtualLaser import VirtualLaser
        from hmflux.instrument.stageSequencer import StageSequencer
        from hmflux.instrument.hmfluxProcessor import HMFluxProcessor

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

        #switch
        switch = VirtualSwitch('switch')
        switch.connect()
        switch.positionList = ['OD1','OD2','OD3','OD4']

        #laser
        laser = VirtualLaser('laser')
        laser.connect()

        # stage Sequencer
        seq = StageSequencer()
        seq.connect(camera=camera, stage=stage,slm=slm, laser=laser)

        # processor
        hmfluxPro = HMFluxProcessor()
        hmfluxPro.connect(camera=camera)
        hmfluxPro.setParameter('threadingNow', True)


        # set GUIs
        adGui = AllDeviceGUI(viscope)
        adGui.setDevice([stage,switch,laser])
        siGui = SaveImageGUI(viscope)
        siGui.setDevice(camera)

        cGui = CameraGUI(viscope,vWindow='new')
        cGui.setDevice(camera)
        cvGui = CameraViewGUI(viscope,vWindow=cGui.vWindow)
        cvGui.setDevice(camera)
        slmGui = SLMGUI(viscope,vWindow='new')
        slmGui.setDevice(slm)
        edGui  = EmitterDataGUI(viscope,vWindow='new')
        edGui.setDevice(hmfluxPro)
        edGui.interconnectGui(cameraViewGUI=cvGui)
    
        ssGui  = SeqStageGUI(viscope)
        ssGui.setDevice(seq)
        ssGui.interconnectGui(emitterDataGUI=edGui,cameraViewGUI=cvGui)

        # main event loop
        viscope.run()

        hmfluxPro.disconnect()
        seq.disconnect()
        camera.disconnect()
        stage.disconnect()
        slm.disconnect()


if __name__ == "__main__":

    HMFlux.runReal()
    # HMFlux.runVirtual()

#%%
