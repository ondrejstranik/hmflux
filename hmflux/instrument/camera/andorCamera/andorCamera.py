"""
Camera DeviceModel

Created on Mon Nov 15 12:08:51 2021

@author: ostranik
"""
#%%

import os
import time
import numpy as np

from viscope.instrument.base.baseCamera import BaseCamera

import pylablib
from pylablib.devices import Andor


class AndorCamera(BaseCamera):
    ''' class to control andor camera. use pylablib package '''
    DEFAULT = {'name': 'andorCamera',
                'exposureTime': 10, # ms initially automatically set the exposure time
                'nFrame': 1,
                'gain': 1,
                'shutter': 'open',
                'acquisitionMode': 'cont',
                'funMode': 'full',
                'triggerMode': 'int',
                'andorPath': r'C:/Program Files/Andor Driver Pack 2'
}

    def __init__(self, name=None,**kwargs):
        ''' initialisation '''

        if name is None: name=AndorCamera.DEFAULT['name'] 
        super().__init__(name=name,**kwargs)
        
        # camera parameters
        self.exposureTime = AndorCamera.DEFAULT['exposureTime']
        self.nFrame = AndorCamera.DEFAULT['nFrame']

        self.cam = None

        pylablib.par['devices/dlls/andor_sdk2']=AndorCamera.DEFAULT['andorPath']

    def connect(self):
        super().connect()

        self.cam = Andor.AndorSDK2Camera()
        self.cam.setup_shutter(AndorCamera.DEFAULT['shutter'])
        self.cam.set_acquisition_mode(AndorCamera.DEFAULT['acquisitionMode'])
        self.cam.set_fan_mode(AndorCamera.DEFAULT['funMode'])
        self.cam.set_trigger_mode(AndorCamera.DEFAULT['triggerMode'])
        self.cam.set_exposure(0.0005)
        self.cam.set_EMCCD_gain(AndorCamera.DEFAULT['gain'],advanced=False)
        self._setExposureTime(self.exposureTime)

        cam.start_acquisition()

        # get the camera optimal exposure time 
        self.exposureTime = self.getParameter('exposureTime')

    def disconnect(self):
        self.cam.stop_acquisition()
        super().disconnect()

    def getLastImage(self):
        myframe = None
        for _ in range(self.nFrame):
            temporary_frame = None
            self.cam.wait_for_frame()
            _myframe = cam.read_oldest_image()
            if myframe is None:
                myframe = _myframe
            else:
                myframe += _myframe
        self.rawImage = myframe/self.nFrame
        return self.rawImage

    def _setExposureTime(self,value): # ms
        # set the expression time

        print(f'set Exposure Time {value}')
        self.cam.set_exposure(value/1000)     
        self.exposureTime = value

    def _getExposureTime(self):
        self.exposureTime = self.cam.get_exposure()*1000
        return self.exposureTime


#%%

if __name__ == '__main__':
    pass


