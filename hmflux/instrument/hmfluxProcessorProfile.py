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
from hmflux.algorithm.emitterDataProfile import EmitterDataProfile
from hmflux.algorithm.emitterImageProfile import EmitterImageProfile
from hmflux.PRIVATE.seeDip import SeeDip

class HMFluxProcessorProfile (BaseProcessor):
    ''' class to control processing of image and get the intensity value of the emitter'''
    DEFAULT = {'name': 'HMFluxProcessorProfile',
               'xPos': 0,
               'yPos': 0,
               'length': 20,
               'aveWidth': 0,
               'axisDirection': 0,
               'coordinate': 0}

    def __init__(self, name=None, **kwargs):
        ''' initialisation '''

        if name== None: name= HMFluxProcessorProfile.DEFAULT['name']
        super().__init__(name=name, **kwargs)
        
        # camera
        self.camera = None

        self.seeDip = SeeDip()
        self.contrast = 0

        # calculation parameter
        self.xPos = HMFluxProcessorProfile.DEFAULT['xPos']
        self.yPos = HMFluxProcessorProfile.DEFAULT['yPos']
        self.length = HMFluxProcessorProfile.DEFAULT['length']
        self.coordinate = HMFluxProcessorProfile.DEFAULT['coordinate']
        self.coordinateTable = np.arange(self.coordinate,self.coordinate+self.length)
        self.axisDirection = HMFluxProcessorProfile.DEFAULT['axisDirection']
        self.aveWidth = HMFluxProcessorProfile.DEFAULT['aveWidth']

        self.seeDip.setnAve(self.aveWidth)

        # data container
        self.emitterDataProfile = EmitterDataProfile()
        # class for calculating emitterData
        self.emitterImageProfile = EmitterImageProfile()


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

        if self.axisDirection == 0:
            try:
                self.coordinate = self.yPos
                self.coordinateTable = np.arange(self.coordinate,self.coordinate+self.length)
                self.emitterImageProfile.setImageSet(self.camera.rawImage[self.yPos:self.yPos+self.aveWidth+1, :])
                contrastData = self.emitterImageProfile.getSignal()
                # maybe initialization problem, cannot calculate at the begining, throw the tuple out of index error
                # self.contrast = self.seeDip.calContrast(im=contrastData, axis=self.axisdirection)
                self.emitterImageProfile.setImageSet(self.camera.rawImage[self.yPos,self.xPos:self.xPos+self.length])
                newSignal = self.emitterImageProfile.getSignal()
            except:
                # print(11)
                newSignal = 0
        elif self.axisDirection == 1:
            try:
                self.coordinate = self.xPos
                self.coordinateTable = np.arange(self.coordinate,self.coordinate+self.length)
                self.emitterImageProfile.setImageSet(self.camera.rawImage[:, self.xPos:self.xPos+self.aveWidth+1])
                contrastData = self.emitterImageProfile.getSignal()
                self.contrast = self.seeDip.calContrast(contrastData, self.axisDirection)
                self.emitterImageProfile.setImageSet(self.camera.rawImage[self.yPos:self.yPos+self.length, self.xPos])
                newSignal = self.emitterImageProfile.getSignal()
            except:
                newSignal = 0

        self.emitterDataProfile.addDataValue(valueVector=[newSignal], contarst=self.contrast, axis=self.coordinateTable)

        


#%%
if __name__ == '__main__':
    pass

#%%
