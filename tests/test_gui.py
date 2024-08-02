''' camera unitest '''

import pytest

@pytest.mark.GUI
def test_saveImageGUI():
    ''' testing the viewer with virtual camera'''

    from viscope.main import viscope
    from viscope.gui.allDeviceGUI import AllDeviceGUI
    from viscope.instrument.virtual.virtualCamera import VirtualCamera
    from hmflux.gui.saveImageGUI import SaveImageGUI

    camera = VirtualCamera()
    camera.connect()
    camera.setParameter('exposureTime',300)
    camera.setParameter('nFrame', 1)
    camera.setParameter('threadingNow',True)

    # add gui
    viewer  = AllDeviceGUI(viscope)
    viewer.setDevice(camera)
    newGUI  = SaveImageGUI(viscope,vWindow=viscope.vWindow)
    newGUI.setDevice(camera)

    # main event loop
    viscope.run()

    camera.disconnect()


@pytest.mark.GUI
def test_SLMGUI():
    ''' testing the slmgui'''

    from viscope.main import viscope
    from hmflux.instrument.slm.screenSlm.screenSLM import ScreenSLM
    #from viscope.instrument.virtual.virtualSLM import VirtualSLM
    
    from hmflux.gui.slmGUI import SLMGUI

    slm = ScreenSLM()
    #slm = VirtualSLM()
    slm.connect()

    # add gui
    newGUI  = SLMGUI(viscope)
    newGUI.setDevice(slm)

    # main event loop
    viscope.run()

    slm.disconnect()

@pytest.mark.GUI
def test_smarACTStage():
    ''' check if smarACT stage in gui works'''
    from hmflux.instrument.stage.smarACT.smarACTStage import SmarACTStage

    from viscope.main import viscope
    from viscope.gui.allDeviceGUI import AllDeviceGUI

    stage = SmarACTStage()
    stage.connect()

    # add gui
    viewer  = AllDeviceGUI(viscope)
    viewer.setDevice(stage)

    # main event loop
    viscope.run()

    stage.disconnect()

@pytest.mark.GUI
def test_SLMViewer():
    ''' testing the slm viewer'''
    from hmflux.gui.slmViewer import SLMViewer

    sv = SLMViewer()
    sv.run()

@pytest.mark.GUI
def test_seqStageGUI():
    ''' test if seqStageGUI works'''
    from hmflux.instrument.stageSequencer import StageSequencer
    from viscope.instrument.virtual.virtualCamera import VirtualCamera
    from viscope.instrument.virtual.virtualSLM import VirtualSLM
    from viscope.instrument.virtual.virtualStage import VirtualStage

    from viscope.main import viscope
    from hmflux.gui.seqStageGUI import SeqStageGUI

    #camera
    camera = VirtualCamera(name='VirtualCamera')
    camera.connect()
    camera.setParameter('exposureTime', 300)
    camera.setParameter('nFrame', 1)
    # slm
    slm = VirtualSLM(name='Virtual SLM')
    slm.connect()
    # stage
    stage = VirtualStage(name='virtual Stage')
    stage.connect()
    # stage Sequencer
    seq = StageSequencer()
    seq.connect(camera=camera, stage=stage,slm=slm)
    
    # add gui
    newGUI  = SeqStageGUI(viscope)
    newGUI.setDevice(seq)
    

    # main event loop
    viscope.run()

    seq.disconnect()
    camera.disconnect()
    slm.disconnect()
    stage.disconnect()

@pytest.mark.GUI
def test_emitterDataGUI():
    ''' test if emitterDataGUI works'''
    from viscope.instrument.virtual.virtualCamera import VirtualCamera
    from hmflux.instrument.hmfluxProcessor import HMFluxProcessor

    from viscope.main import viscope
    from hmflux.gui.emitterDataGUI import EmitterDataGUI

    #camera
    camera = VirtualCamera(name='VirtualCamera')
    camera.connect()
    camera.setParameter('exposureTime', 300)
    camera.setParameter('nFrame', 1)
    camera.setParameter('threadingNow', True)

    # processor
    hmfluxPro = HMFluxProcessor()
    hmfluxPro.connect(camera=camera)
    hmfluxPro.setParameter('threadingNow', True)

    # add gui
    newGUI  = EmitterDataGUI(viscope)
    newGUI.setDevice(hmfluxPro)
    
    # main event loop
    viscope.run()

    hmfluxPro.disconnect()
    camera.disconnect()

@pytest.mark.GUI
def test_emitterImageViewer():
    from hmflux.gui.emitterImageViewer import EmitterImageViewer
    from hmflux.algorithm.emitterImage import EmitterImage
    import numpy as np

    ei = EmitterImage(imageSet= np.random.rand(10,5,20))
    
    eiViewer = EmitterImageViewer()
    eiViewer.setEmitterImage(ei)

    eiViewer.run()


@pytest.mark.GUI
def test_emitterImageGUI():
    from hmflux.gui.emitterImageGUI import EmitterImageGUI
    from hmflux.algorithm.emitterImage import EmitterImage
    from viscope.main import viscope
    import numpy as np

    ei = EmitterImage(imageSet= np.random.rand(10,5,20))

    eiGui = EmitterImageGUI(viscope=viscope)
    eiGui.setData(ei)

    viscope.run()

