

#%%

import os
import time
import numpy as np

from viscope.instrument.base.baseCamera import BaseCamera

import pylablib
from pylablib.devices import Photometrics

class TeledyneCamera(BaseCamera):

    DEFAULT = {'name': 'TeledyneCamera',
                'exposureTime': 10, # ms initially automatically set the exposure time
                'nFrame': 1,
                'gain': 1,
                # 'shutter': 'open',
                'acquisitionMode': 'sequence',
                'fanMode': 'high',
                # 'triggerMode': 'int',       
}
     
    def __init__(self, name=None,**kwargs):
        ''' initialisation '''

        if name is None: name=TeledyneCamera.DEFAULT['name'] 
        super().__init__(name=name,**kwargs)
        
        # camera parameters
        self.exposureTime = TeledyneCamera.DEFAULT['exposureTime']
        self.nFrame = TeledyneCamera.DEFAULT['nFrame']

        self.cam = None

    def connect(self):
        super().connect()

        self.cam = Photometrics.PvcamCamera()
        # self.cam.setup_shutter(TeledyneCamera.DEFAULT['shutter'])
        self.cam.setup_acquisition(TeledyneCamera.DEFAULT['acquisitionMode'])
        self.cam.set_fan_mode(TeledyneCamera.DEFAULT['fanMode'])
        # self.cam.set_trigger_mode(TeledyneCamera.DEFAULT['triggerMode'])
        # self.cam.set_exposure(0.0005)
        # self.cam.set_EMCCD_gain(TeledyneCamera.DEFAULT['gain'],advanced=False)
        self._setExposureTime(self.exposureTime)

        self.cam.start_acquisition()

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
            _myframe = self.cam.read_oldest_image()
            if myframe is None:
                myframe = _myframe
            else:
                myframe += _myframe
        self.rawImage = myframe/self.nFrame
        return self.rawImage

    def _setExposureTime(self,value): # ms
        # set the expression time

        self.cam.stop_acquisition()

        print(f'set Exposure Time {value}')
        self.cam.set_exposure(value/1000)     
        self.exposureTime = value

        self.cam.start_acquisition()

    def _getExposureTime(self):
        self.exposureTime = self.cam.get_exposure()*1000
        return self.exposureTime
    
    #for solving the autoSave problem
    def startAcquisitionTest(self):
        self.cam.start_acquisition()

    def stopAcquisitionTest(self):
        self.cam.stop_acquisition()



#%%

if __name__ == '__main__':
    pass
