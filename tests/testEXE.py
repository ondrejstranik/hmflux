''' camera unitest '''

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

test_SLMGUI()