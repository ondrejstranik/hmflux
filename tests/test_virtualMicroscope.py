''' camera unitest '''

import pytest

@pytest.mark.GUI
def test_simpleSpectralMicroscope():
    ''' check if virtual microscope works - show raw data'''
    from viscope.instrument.virtual.virtualCamera import VirtualCamera
    from viscope.main import Viscope
    from viscope.gui.allDeviceGUI import AllDeviceGUI
    from spectralCamera.virtualSystem.simpleSpectralMicroscope import SimpleSpectralMicroscope

    camera1 = VirtualCamera()
    camera1.connect()
    camera1.setParameter('threadingNow',True)

    vM = SimpleSpectralMicroscope()
    vM.setVirtualDevice(camera1)
    vM.connect()

    viscope = Viscope()
    viewer  = AllDeviceGUI(viscope)
    viewer.setDevice([camera1])
    
    viscope.run()

    camera1.disconnect()
    vM.disconnect()
