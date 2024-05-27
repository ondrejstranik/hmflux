''' camera unitest '''

def test_camera():
    ''' check if andor camera work'''
    from hmflux.instrument.camera.andorCamera.andorCamera  import AndorCamera

    cam = AndorCamera(name='AndorCamera')
    cam.connect()
    cam.setParameter('exposureTime',300)
    cam.setParameter('nFrames', 1)

    cam._displayStreamOfImages()
    cam.disconnect()


def test_smartACT():
    from hmflux.instrument.stage.smarACT.smarACTStage import SmarACTStage

    stage = SmarACTStage(name='SmarACT')
    stage.connect()
    myPosition =stage.getParameter('position')
    print(f'myPosition ={myPosition}')

    print(f'myPosition ={myPosition}')

    stage.disconnect()

#test_camera()
test_smartACT()