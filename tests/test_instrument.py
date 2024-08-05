''' camera unitest '''

import pytest

@pytest.mark.GUI
def test_AndorCamera():
    ''' check if andor camera work'''
    from hmflux.instrument.camera.andorCamera.andorCamera  import AndorCamera

    cam = AndorCamera(name='AndorCamera')
    cam.connect()
    cam.setParameter('exposureTime',300)
    cam.setParameter('nFrames', 1)

    cam._displayStreamOfImages()
    cam.disconnect()

def test_AVCamera():
    ''' check if andor camera work'''
    from hmflux.instrument.camera.avCamera.avCamera import AVCamera

    cam = AVCamera(name='AVCamera')
    cam.connect()
    cam.setParameter('exposureTime',10)
    cam.setParameter('nFrames', 3)

    cam._displayStreamOfImages()
    cam.disconnect()

def test_AVCameraGui():
    from viscope.main import viscope
    from viscope.gui.allDeviceGUI import AllDeviceGUI
    from hmflux.instrument.camera.avCamera.avCamera import AVCamera

    camera = AVCamera()
    camera.connect()
    camera.setParameter('exposureTime',300)
    camera.setParameter('nFrame', 1)
    camera.setParameter('threadingNow',True)

    # add gui
    viewer  = AllDeviceGUI(viscope)
    viewer.setDevice(camera)

    # main event loop
    viscope.run()

    camera.disconnect()


def test_CoboltLaser():
    from hmflux.instrument.laser.coboltLaser import CoboltLaser

    laser = CoboltLaser()
    laser.connect()
    laser.setParameter('keySwitch',True)
    print('set power to 1 mW')
    laser.setParameter('power', 1)
    time.sleep(10)
    print('set power to 3 mW')
    laser.setParameter('power', 3)
    time.sleep(10)
    laser.disconnect()    

def test_CoboltLaserGui():
    from hmflux.instrument.laser.coboltLaser import CoboltLaser
    from viscope.main import viscope
    from viscope.gui.allDeviceGUI import AllDeviceGUI

    laser = CoboltLaser()
    laser.connect()

    # add gui
    adGui  = AllDeviceGUI(viscope)
    adGui.setDevice(laser)
    # main event loop
    viscope.run()

    laser.disconnect()



@pytest.mark.GUI
def test_screenSLM():
    ''' check if slm works'''
    from hmflux.instrument.slm.screenSlm.screenSLM import ScreenSLM
    import time
    import numpy as np

    slm = ScreenSLM()
    slm.connect()

    X,Y = np.meshgrid(np.linspace(0,slm.sizeX,slm.sizeX),np.linspace(0,slm.sizeY,slm.sizeY))
    for i in range(10):
        testIMG = np.round((2**8-1)*(0.5+0.5*np.sin(2*np.pi*X/50+1.0*i/10*np.pi))).astype('uint8')
        slm.setImage(testIMG)
        time.sleep(0.05)

    slm.disconnect()

def test_smarACTStage():
    ''' check if smarACT stage works'''
    from hmflux.instrument.stage.smarACT.smarACTStage import SmarACTStage
    import time
    import numpy as np

    stage = SmarACTStage()
    stage.connect()

    mP = stage.getParameter('position')
    print(f'position = {mP}')
    stage.setParameter('position', mP+1)

    mP = stage.getParameter('position')
    print(f'new position = {mP}')

    stage.disconnect()

@pytest.mark.GUI
def test_smarACTStage_2():
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

def test_stageSequencer():
    from hmflux.instrument.stageSequencer import StageSequencer
    from viscope.instrument.virtual.virtualCamera import VirtualCamera
    from viscope.instrument.virtual.virtualSLM import VirtualSLM
    from viscope.instrument.virtual.virtualStage import VirtualStage

    #camera
    camera = VirtualCamera(name='VirtualCamera')
    camera.connect()
    camera.setParameter('exposureTime', 300)
    camera.setParameter('nFrame', 1)

    # slm
    slm = VirtualSLM()
    slm.connect()

    # stage
    stage = VirtualStage('stage')
    stage.connect()

    seq = StageSequencer()
    seq.connect(camera=camera, stage=stage,slm=slm)

    for _ in seq.loop():
        pass

    camera.disconnect()
    slm.disconnect()
    stage.disconnect()

def test_hmfluxProcessor():
    from viscope.instrument.virtual.virtualCamera import VirtualCamera
    from hmflux.instrument.hmfluxProcessor import HMFluxProcessor
    import time

    #camera
    camera = VirtualCamera(name='VirtualCamera')
    camera.connect()
    camera.setParameter('exposureTime', 300)
    camera.setParameter('nFrame', 1)
    camera.setParameter('threadingNow', True)

    hmfluxPro = HMFluxProcessor()
    hmfluxPro.connect(camera=camera)
    hmfluxPro.setParameter('threadingNow', True)

    print('waiting ')
    time.sleep(3)

    _sig, _time = hmfluxPro.emitterData.getData()

    print(f'time:\n {_time}')
    print(f'signal:\n {_sig}')
    
    hmfluxPro.disconnect()
    camera.disconnect()

@pytest.mark.GUI
def test_thorlabSwitch():
    ''' check if thorlab switch in gui works'''
    from hmflux.instrument.switch.throlabSwitch import ThrolabSwitch

    from viscope.main import viscope
    from viscope.gui.allDeviceGUI import AllDeviceGUI

    switch = ThrolabSwitch()
    switch.connect(port='COM3')
    switch.positionList = ['OD1','OD2','OD3','OD4']

    # add gui
    viewer  = AllDeviceGUI(viscope)
    viewer.setDevice(switch)

    # main event loop
    viscope.run()

    stage.disconnect()


