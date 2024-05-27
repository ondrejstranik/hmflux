''' camera unitest '''

import pytest

@pytest.mark.GUI
def test_saveImageGUI():
    ''' testing the viewer with webcam'''

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
