"""
plasmon processor - process the spectral images

Created on Mon Nov 15 12:08:51 2021

@author: ostranik
"""
#%%

import os
import time
import numpy as np
from viscope.instrument.base.baseSequencer import BaseSequencer
from plim.algorithm.plasmonFit import PlasmonFit
from plim.algorithm.spotSpectra import SpotSpectra
from plim.algorithm.spotData import SpotData
from plim.algorithm.flowData import FlowData


class StageSequencer(BaseSequencer):
    ''' class to control recording of images with moving stage
    '''
    DEFAULT = {'name': 'StageSequencer'}

    def __init__(self, name=None, **kwargs):
        ''' initialisation '''

        if name== None: name= StageSequencer.DEFAULT['name']
        super().__init__(name=name, **kwargs)
        
        # camera
        self.camera = None
        # stage
        self.stage = None
        # slm
        self.slm = None

    def connect(self,camera=None,stage=None,slm=None):
        ''' connect sequencer with the camera, stage, slm '''
        super().connect()
        if camera is not None: self.setParameter('camera',camera)
        if stage is not None: self.setParameter('stage',stage)
        if slm is not None: self.setParameter('slm',slm)

    def setParameter(self,name, value):
        ''' set parameter of the spectral camera'''
        super().setParameter(name,value)

        if name== 'camera':
            self.camera = value
        if name== 'stage':
            self.stage = value
        if name== 'slm':
            self.slm = value

    def getParameter(self,name):
        ''' get parameter of the camera '''
        _value = super().getParameter(name)
        if _value is not None: return _value        

        if name== 'camera':
            return self.camera
        if name== 'stage':
            return self.stage
        if name== 'slm':
            return self.slm

    def processData(self):
        ''' process newly arrived data '''
        #print(f"processing data from {self.DEFAULT['name']}")
        self.spotSpectra.setImage(self.sCamera.sImage)
        self.pF.setSpectra(self.spotSpectra.getA())
        self.pF.setWavelength(self.sCamera.wavelength)
        self.pF.calculateFit()
        newTime = time.time()
        newFlow = self.pump.getParameter('flowRateReal')
        newSignal = self.pF.getPosition()
        if newSignal != []:
            t0 = self.spotData.addDataValue(newSignal,newTime)
            if t0 is not None: 
                self.flowData.clearData()
                self.flowData.setT0(t0)
        if newFlow is not None:
            self.flowData.addDataValue([newFlow],newTime)


        


#%%

# TODO: test it!
if __name__ == '__main__':
    pass
