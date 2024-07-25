
#%%
import os
from pathlib import Path

from hmflux.instrument.camera.andorCamera.andorCamera import AndorCamera
from hmflux.instrument.camera.teledyneCamera.teledyneCamera import TeledyneCamera   
from hmflux.instrument.slm.screenSlm.screenSLM import ScreenSLM
from hmflux.instrument.stage.smarACT.smarACTStage import SmarACTStage
from hmflux.algorithm.imageSLM import ImageSLM
import numpy as np

import keyboard
import time


class AutoSave():
    def __init__(self):
        
        #camera
        self.camera = TeledyneCamera(name='TeledyneCamera')
        self.camera.connect()
        self.camera.stopAcquisition()
        self.camera.setParameter('exposureTime', 300)
        self.camera.setParameter('nFrame', 1)
        #self.camera.setParameter('threadingNow',True)


        # slm
        self.slm = ScreenSLM('slm')
        self.slm.connect()

        # stage
        self.stage = SmarACTStage('stage')
        self.stage.connect()

        #all parameters
        self.folderName = '20240725-104'
        self.dataFolder = r'E:\ZihaoData\DATA\PrimeBSI'
        # self.dataFolder = r'.\hmflux\DATA'
        self.path = self.dataFolder+'./'+self.folderName

        self.pathBinary = Path(self.path+'./'+'Binary')
        self.pathBox = Path(self.path+'./'+'Box')
        self.pathDark = Path(self.path+'./'+'Dark')
        self.fileName = 'Image'
        self.mkdir()

        #stage parameter
        self.stageX = -0.02
        self.stageY = 0
        self.stageZ = 0

        #slm parameter
        self.imageSLM = ImageSLM()
        self.imageSLM.setSizeSLM(self.slm.sizeX,self.slm.sizeY)

        self.constantValue = 0
        self.binaryAxis = 0
        self.binaryValue0 = 0
        self.binaryValue1 = 134
        self.boxAxis = 0
        self.boxPosition = 333
        self.boxValue0 = 0
        self.boxValue1 = 104
        self.boxHalfwidth = 3
        self.bcgImage = None

        self.numberOfImage = 250

        print('Press q if stage is stuck')

    def mkdir(self):
        folder = os.path.exists(self.path)
        if not folder:
                os.makedirs(self.path)
                os.makedirs(self.path+'./'+'Binary')
                os.makedirs(self.path+'./'+'Box')
                os.makedirs(self.path+'./'+'Dark')
     
        else:
            while folder:
                tail = '-1'
                self.path = self.path + tail
                folder = os.path.exists(self.path)
            os.makedirs(self.path)
            os.makedirs(self.path+'./'+'Binary')
            os.makedirs(self.path+'./'+'Box')
            os.makedirs(self.path+'./'+'Dark')
            self.pathBinary = Path(self.path+'./'+'Binary')
            self.pathBox = Path(self.path+'./'+'Box')
            self.pathDark = Path(self.path+'./'+'Dark')
            
    def getStagePosition(self):
        ax1 = self.stage.getPosition('X')
        ax2 = self.stage.getPosition('Y')
        ax3 = self.stage.getPosition('Z')
        self.position = np.array((ax1,ax2,ax3))
        return self.position


    def record(self):
        slmImageBi = self.imageSLM.generateConstant(self.constantValue)
        slmImageBi += self.imageSLM.generateBinaryGrating(self.binaryAxis,self.binaryValue0,self.binaryValue1)

        slmImageBox = self.imageSLM.generateConstant(self.constantValue)
        slmImageBox += self.imageSLM.generateBinaryGrating(1-self.boxAxis,self.binaryValue0,self.binaryValue1)
        slmImageBox = self.imageSLM.generateBox1(axis=self.boxAxis,
                                            position=self.boxPosition,
                                            val0=self.boxValue0,
                                            val1=self.boxValue1,
                                            halfwidth=self.boxHalfwidth,
                                            bcgImage=slmImageBox)
        
        slmImageDark = self.imageSLM.generateConstant(self.constantValue)
        slmImageDark += self.imageSLM.generateBinaryGrating(1-self.binaryAxis,self.binaryValue0,self.binaryValue1)

        stagePosition = np.zeros([self.numberOfImage,3])
        for ii in range(self.numberOfImage):
            stagePosition[ii,:] = self.getStagePosition()
            print(f'recording {ii} image')
            #binary
            # self.slm.setImage(slmImageBi)
            # # time.sleep(0.3)
            # # TODO: try this
            # self.camera.startAcquisition()
            # self.rawBinary = self.camera.getLastImage()
            # self.camera.stopAcquisition()
            # np.save(str(self.pathBinary / self.fileName) + f'_{ii:03d}',self.rawBinary)

            #box1
            self.slm.setImage(slmImageBox)
            # time.sleep(0.3)
            # TODO: try this
            self.camera.startAcquisition()
            self.rawBox = self.camera.getLastImage()
            self.camera.stopAcquisition()
            np.save(str(self.pathBox/ self.fileName) + f'_{ii:03d}',self.rawBox)

            #dark
            # self.slm.setImage(slmImageDark)
            # self.camera.startAcquisition()
            # self.rawDark = self.camera.getLastImage()
            # self.camera.stopAcquisition()
            # np.save(str(self.pathDark/ self.fileName) + f'_{ii:03d}',self.rawDark)

            if self.stageX != 0:
                self.stage.move(self.stageX,'X')
            elif self.stageY != 0:
                self.stage.move(self.stageY,'Y')
            elif self.stageZ != 0:
                self.stage.move(self.stageZ,'Z')

            
            if keyboard.is_pressed('q'):
                print("Loop terminated")
                break
        np.savetxt(self.path+'./'+'stageShiftInfo.txt', stagePosition)

#%%

if __name__ == '__main__':
    import napari

    autoSave = AutoSave()
    autoSave.record()
    print('record done')
    # autoSave.save()
    # print('save done')


    autoSave.camera.disconnect()
    autoSave.stage.disconnect()
    autoSave.slm.disconnect()    

    # viewer = napari.Viewer()
    # viewer.add_image(np.array(autoSave.binaryImage),name='binary')
    # viewer.add_image(np.array(autoSave.boxImage),name='box')
    # napari.run()


#%%

