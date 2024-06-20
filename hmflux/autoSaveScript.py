import os

from hmflux.instrument.camera.andorCamera.andorCamera import AndorCamera
from hmflux.instrument.camera.avCamera.avCamera import AVCamera        
from hmflux.instrument.slm.screenSlm.screenSLM import ScreenSLM
from hmflux.instrument.stage.smarACT.smarACTStage import SmarACTStage
from hmflux.algorithm.imageSLM import ImageSLM
import numpy as np

import keyboard

class AutoSave():
    def __init__(self):
        #camera
        self.camera = AndorCamera(name='AndorCamera')
        self.camera.connect()
        self.camera.setParameter('exposureTime', 300)
        self.camera.setParameter('nFrame', 1)
        self.camera.setParameter('threadingNow',True)

        # slm
        self.slm = ScreenSLM('slm')
        self.slm.connect()

        # stage
        self.stage = SmarACTStage('stage')
        self.stage.connect()
        #all parameters
        self.folderName = '20062024-1'
        self.dataFolder = r'.\DATA'
        self.path = self.dataFolder+'./'+self.folderName

        #stage parameter
        self.stageX = 0
        self.stageY = 0
        self.stageZ = 0
        self.stageMove = np.array((self.stageX,self.stageY,self.stageZ))
        self.axis = ['X', 'Y', 'Z']

        #camera image
        self.constantImage = []
        self.boxImage = []
        self.numberOfImage = 10

        #slm parameter
        sizeX = 200
        sizeY = 100
        self.imageSLM = ImageSLM()
        self.imageSLM.setSizeSLM(sizeX,sizeY)

        self.constantValue = 0
        self.binaryValue0 = 0
        self.binaryValue1 = 255
        self.boxAxis = 0
        self.boxPosition = 0
        self.boxValue0 = 0
        self.boxValue1 = 255
        self.boxHalfwidth = 6
        self.bcgImage = None

        print('Press q if stage is stuck')

        self.mkdir()

    def mkdir(self,path):
        folder = os.path.exists(self.path)
        if not folder:
            os.makedirs(self.path)
            os.makedirs(self.path+'./'+'Constant')
            os.makedirs(self.path+'./'+'Box')
                        
        else:
            print('please create a new folder')

    def save(self):
        for i in range(len(self.constantImage)):
            pathConstant = self.path+'./'+'Constant'
            pathBox = self.path+'./'+'Box'
            fileName = 'Image'
            fileIdx = 0
            np.save(str(pathConstant / fileName) + f'_{fileIdx}',self.constantImage[i])
            np.save(str(pathBox/ fileName) + f'_{fileIdx}',self.boxImage[i])
            fileIdx = fileIdx + 1 


    def record(self):
        for i in range(self.numberOfImage):
            #constant
            slmImage = np.zeros([self.sizeX,self.sizeY])
            slmImage = self.imageSLM.generateConstant(self.constantValue)
            self.slm.setImage(slmImage)
            self.rawConstant = self.camera.getLastImage()
            self.constantImage.append(self.rawConstant)
            
            #box1
            slmImage = np.zeros([self.sizeX,self.sizeY])
            slmImage = self.imageSLM.generateConstant(self.constantValue)
            slmImage += self.imageSLM.generateBinaryGrating(1-self.boxAxis,self.binaryValue0,self.binaryValue1)
            slmImage = self.imageSLM.generateBox1(axis=self.boxAxis,
                                            position=self.boxPosition,
                                            val0=self.boxValue0,
                                            val1=self.boxValue1,
                                            halfwidth=self.boxHalfwidth,
                                            bcgImage=slmImage)
            self.slm.setImage(slmImage)
            self.rawBox = self.camera.getLastImage()
            self.boxImage.append(self.rawBox)

            self.stage.move(self.stageMove,self.axis)

            if keyboard.is_pressed('q'):
                print("Loop terminated")
            break

autoSave = AutoSave()
autoSave.record()
autoSave.save()





autoSave.camera.disconnect()
autoSave.stage.disconnect()
autoSave.slm.disconnect()    


#%%

