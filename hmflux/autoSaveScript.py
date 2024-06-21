
#%%
import os
from pathlib import Path

from hmflux.instrument.camera.andorCamera.andorCamera import AndorCamera
from hmflux.instrument.camera.avCamera.avCamera import AVCamera        
from hmflux.instrument.slm.screenSlm.screenSLM import ScreenSLM
from hmflux.instrument.stage.smarACT.smarACTStage import SmarACTStage
from hmflux.algorithm.imageSLM import ImageSLM
import numpy as np

import keyboard


'''don t forget check the save folder!!!!! data will be overlap!!!'''

class AutoSave():
    def __init__(self):
        #camera
        self.camera = AndorCamera(name='AndorCamera')
        self.camera.connect()
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
        self.folderName = '20240624-1-half3'
        self.dataFolder = r'.\hmflux\DATA'
        self.path = self.dataFolder+'./'+self.folderName

        #stage parameter
        self.stageX = -0.02
        self.stageY = 0
        self.stageZ = 0
        # self.stageMove = np.array((self.stageX,self.stageY,self.stageZ))
        # self.axis = ['X', 'Y', 'Z']

        #camera image
        self.binaryImage = []
        self.boxImage = []


        #slm parameter
        self.imageSLM = ImageSLM()
        self.imageSLM.setSizeSLM(self.slm.sizeX,self.slm.sizeY)

        self.constantValue = 0
        self.binaryAxis = 0
        self.binaryValue0 = 0
        self.binaryValue1 = 134
        self.boxAxis = 0
        self.boxPosition = 281
        self.boxValue0 = 0
        self.boxValue1 = 99
        self.boxHalfwidth = 3
        self.bcgImage = None

        print('Press q if stage is stuck')

        self.mkdir()

    def mkdir(self):
        folder = os.path.exists(self.path)
        if not folder:
            os.makedirs(self.path)
            os.makedirs(self.path+'./'+'Binary')
            os.makedirs(self.path+'./'+'Box')
                        
        else:
            print('please create a new folder')

    def save(self):
        for ii in range(len(self.binaryImage)):
            pathBinary = Path(self.path+'./'+'Binary')
            pathBox = Path(self.path+'./'+'Box')
            fileName = 'Image'
            np.save(str(pathBinary / fileName) + f'_{ii}',self.binaryImage[ii])
            np.save(str(pathBox/ fileName) + f'_{ii}',self.boxImage[ii])


    def record(self,numberOfImage):
        for i in range(numberOfImage):
            #binary
            # slmImage = np.zeros([self.sizeX,self.sizeY])
            print(f'recording {i} image')
            slmImage = self.imageSLM.generateConstant(self.constantValue)
            slmImage += self.imageSLM.generateBinaryGrating(self.binaryAxis,self.binaryValue0,self.binaryValue1)
            self.slm.setImage(slmImage)
            self.rawBinary = self.camera.getLastImage()
            self.binaryImage.append(self.rawBinary)
            
            #box1
            slmImage = self.imageSLM.generateConstant(self.constantValue)
            slmImage += self.imageSLM.generateBinaryGrating(1-self.boxAxis,self.binaryValue0,self.binaryValue1)
            slmImage += self.imageSLM.generateBox1(axis=self.boxAxis,
                                            position=self.boxPosition,
                                            val0=self.boxValue0,
                                            val1=self.boxValue1,
                                            halfwidth=self.boxHalfwidth,
                                            bcgImage=slmImage)
            self.slm.setImage(slmImage)
            self.rawBox = self.camera.getLastImage()
            self.boxImage.append(self.rawBox)

            if self.stageX != 0:
                self.stage.move(self.stageX,'X')
            elif self.stageY != 0:
                self.stage.move(self.stageY,'Y')
            elif self.stageZ != 0:
                self.stage.move(self.stageZ,'Z')


            if keyboard.is_pressed('p'):
                print("Loop terminated")
                break

#%%

if __name__ == '__main__':
    import napari

    autoSave = AutoSave()
    numberOfImage = 300
    autoSave.record(numberOfImage)
    print('record done')
    autoSave.save()
    print('save done')


    autoSave.camera.disconnect()
    autoSave.stage.disconnect()
    autoSave.slm.disconnect()    

    viewer = napari.Viewer()
    viewer.add_image(np.array(autoSave.binaryImage),name='binary')
    viewer.add_image(np.array(autoSave.boxImage),name='box')
    napari.run()


#%%

