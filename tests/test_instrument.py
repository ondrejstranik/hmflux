''' camera unitest '''

import pytest

@pytest.mark.GUI
def test_camera():
    ''' check if andor camera work'''
    from hmflux.instrument.camera.andorCamera.andorCamera  import AndorCamera

    cam = AndorCamera(name='AndorCamera')
    cam.connect()
    cam.setParameter('exposureTime',300)
    cam.setParameter('nFrames', 1)

    cam._displayStreamOfImages()
    cam.disconnect()

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

