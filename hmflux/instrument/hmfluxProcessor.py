"""
plasmon processor - process the spectral images

Created on Mon Nov 15 12:08:51 2021

@author: ostranik
"""
#%%

import os
import time
import numpy as np
from viscope.instrument.base.baseProcessor import BaseProcessor
from hmflux.algorithm.emitterData import EmitterData
from hmflux.algorithm.emitterImage import EmitterImage

class HMFluxProcessor(BaseProcessor):
    ''' class to control processing of image and get the intensity value of the emitter'''
    DEFAULT = {'name': 'HMFluxProcessor',
               'xPos': 0,
               'yPos': 0,
               'deltaX': 5,
               'deltaY': 20}

    def __init__(self, name=None, **kwargs):
        ''' initialisation '''

        if name== None: name= HMFluxProcessor.DEFAULT['name']
        super().__init__(name=name, **kwargs)
        
        # camera
        self.camera = None
        
        # data container
        self.emitterData = EmitterData()
        # class for calculating emitterData
        self.emitterImage = EmitterImage()

        # calculation parameter
        self.xPos = HMFluxProcessor.DEFAULT['xPos']
        self.yPos = HMFluxProcessor.DEFAULT['yPos']
        self.deltaX = HMFluxProcessor.DEFAULT['deltaX']
        self.deltaY = HMFluxProcessor.DEFAULT['deltaY']


    def connect(self,camera=None):
        ''' connect data processor with the camera '''
        super().connect()
        if camera is not None: self.setParameter('camera',camera)

    def setParameter(self,name, value):
        ''' set parameter of the spectral camera'''
        super().setParameter(name,value)

        if name== 'camera':
            self.camera = value
            self.flagToProcess = self.camera.flagLoop

    def getParameter(self,name):
        ''' get parameter of the camera '''
        _value = super().getParameter(name)
        if _value is not None: return _value        

        if name== 'camera':
            return self.camera

    def processData(self):
        ''' process newly arrived data '''
        #print(f"processing data from {self.DEFAULT['name']}")
        newTime = time.time()

        try:
            self.emitterImage.setImageSet(self.camera.rawImage[self.yPos:self.yPos+self.deltaY,
                                                    self.xPos:self.xPos+self.deltaX])
            newSignal = self.emitterImage.getSignal()
        except:
            newSignal = 0
        
        self.emitterData.addDataValue([newSignal],newTime)

        


#%%
if __name__ == '__main__':
    pass
