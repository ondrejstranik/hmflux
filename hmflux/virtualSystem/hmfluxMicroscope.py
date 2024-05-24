"""
virtual basic microscope

components: camera

@author: ostranik
"""
#%%

import time

from viscope.virtualSystem.base.baseSystem import BaseSystem
from viscope.virtualSystem.component.component import Component
from spectralCamera.virtualSystem.component.component2 import Component2
from spectralCamera.virtualSystem.component.sample2 import Sample2

import numpy as np


class HMFluxMicroscope(BaseSystem):
    ''' class to emulate microscope '''
    DEFAULT = {}
               
    
    def __init__(self,**kwargs):
        ''' initialisation '''
        super().__init__(**kwargs)

    def setVirtualDevice(self,camera=None):
        ''' set instruments of the microscope '''
        self.device['camera'] = camera

    def calculateVirtualFrame(self):
        ''' update the virtual Frame of the camera '''

        # image sample onto camera
        oFrame = Component.ideal4fImagingOnCamera(camera=self.device['camera'],
                iFrame= self.sample.get(),iPixelSize=self.sample.pixelSize,
                magnification= self.DEFAULT['magnification'])

        print('virtual Frame updated')

        return oFrame


    def loop(self):
        ''' infinite loop to carry out the microscope state update
        it is a state machine, which should be run in separate thread '''
        while True:
            yield 
            if self.deviceParameterIsChanged():
                print(f'calculate virtual frame')
                self.device['camera'].virtualFrame = self.calculateVirtualFrame()
                self.deviceParameterFlagClear()

            time.sleep(0.03)

        

#%%

if __name__ == '__main__':

    pass