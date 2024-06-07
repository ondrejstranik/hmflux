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
