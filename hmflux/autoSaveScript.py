
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
        self.camera.setParameter('exposureTime', 500)
        self.camera.setParameter('nFrame', 1)
        #self.camera.setParameter('threadingNow',True)

        # slm
        self.slm = ScreenSLM('slm')
        self.slm.connect()

        # stage
        self.stage = SmarACTStage('stage')
        self.stage.connect()
        #all parameters
        self.folderName = '20240624-half2'
        self.dataFolder = r'.\hmflux\DATA'
        self.path = self.dataFolder+'./'+self.folderName

        #stage parameter
        self.stageX = 0.02
        self.stageY = 0
        self.stageZ = 0
        # self.stageMove = np.array((self.stageX,self.stageY,self.stageZ))
        # self.axis = ['X', 'Y', 'Z']

        #camera image
        self.constantImage = []
        self.boxImage = []


        #slm parameter
        self.imageSLM = ImageSLM()
        self.imageSLM.setSizeSLM(self.slm.sizeX,self.slm.sizeY)

        self.constantValue = 0
        self.binaryValue0 = 0
        self.binaryValue1 = 133
        self.boxAxis = 0
        self.boxPosition = 187
        self.boxValue0 = 3
        self.boxValue1 = 86
        self.boxHalfwidth = 2
        self.bcgImage = None

        print('Press q if stage is stuck')

        self.mkdir()

    def mkdir(self):
        folder = os.path.exists(self.path)
        if not folder:
            os.makedirs(self.path)
            os.makedirs(self.path+'./'+'Constant')
            os.makedirs(self.path+'./'+'Box')
                        
        else:
            print('please create a new folder')

    def save(self):
        for i in range(len(self.constantImage)):
            pathConstant = Path(self.path+'./'+'Constant')
            pathBox = Path(self.path+'./'+'Box')
            fileName = 'Image'
            np.save(str(pathConstant / fileName) + f'_{i}',self.constantImage[i])
            np.save(str(pathBox/ fileName) + f'_{i}',self.boxImage[i])


    def record(self,numberOfImage):
        for i in range(numberOfImage):
            #constant
            # slmImage = np.zeros([self.sizeX,self.sizeY])
            print(f'recording {i} image')
            slmImage = self.imageSLM.generateConstant(self.constantValue)
            self.slm.setImage(slmImage)
            self.rawConstant = self.camera.getLastImage()
            self.constantImage.append(self.rawConstant)
            
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
    numberOfImage = 200
    autoSave.record(numberOfImage)
    print('record done')
    autoSave.save()
    print('save done')


    autoSave.camera.disconnect()
    autoSave.stage.disconnect()
    autoSave.slm.disconnect()    

    viewer = napari.Viewer()
    viewer.add_image(np.array(autoSave.constantImage))
    viewer.add_image(np.array(autoSave.boxImage))
    napari.run()


#%%

