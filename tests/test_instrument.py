''' camera unitest '''

import pytest

@pytest.mark.GUI
def test_camera():
    ''' check if andor camera work'''
    from hmflux.instrument.camera.andorCamera.andorCamera  import AndorCamera

    cam = AndorCamera(name='AndorCamera')
    cam.connect()
    #cam.setParameter('exposureTime',300)
    cam.setParameter('nFrames', 1)

    cam._displayStreamOfImages()
    cam.disconnect()

