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
    #from hmflux.instrument.slm.screenSlm.screenSLM import ScreenSLM
    from viscope.instrument.virtual.virtualSLM import VirtualSLM
    
    from hmflux.gui.slmGUI import SLMGUI

    #slm = ScreenSLM()
    slm = VirtualSLM()
    slm.connect()

    # add gui
    newGUI  = SLMGUI(viscope)
    newGUI.setDevice(slm)

    # main event loop
    viscope.run()

    slm.disconnect()




def test_SLMViewer():
    ''' testing the slm viewer'''
    from hmflux.gui.slmViewer import SLMViewer

    sv = SLMViewer()
    sv.run()