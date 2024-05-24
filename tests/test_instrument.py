''' camera unitest '''

import pytest

@pytest.mark.GUI
def test_camera():
    ''' check if web camera work'''
    from spectralCamera.instrument.camera.webCamera.webCamera import WebCamera

    cam = WebCamera(name='WebCamera',filterType='RGGB')
    cam.connect()
    cam.setParameter('exposureTime',300)
    cam.setParameter('nFrames', 5)

    cam._displayStreamOfImages()
    cam.disconnect()

