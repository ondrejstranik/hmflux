

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
                'triggerMode': 'timed',       
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
        self.cam.setup_acquisition(TeledyneCamera.DEFAULT['acquisitionMode'],  nframes=2)
        self.cam.set_fan_mode(TeledyneCamera.DEFAULT['fanMode'])
        # self.cam.set_trigger_mode(TeledyneCamera.DEFAULT['triggerMode'])
        # self.cam.set_exposure(0.0005)
        # self.cam.set_EMCCD_gain(TeledyneCamera.DEFAULT['gain'],advanced=False)
        self._setExposureTime(self.exposureTime)
        # get the camera optimal exposure time 
        self.exposureTime = self.getParameter('exposureTime')
        self.startAcquisition()

    def disconnect(self):
        self.cam.stop_acquisition()
        super().disconnect()

    def getLastImage(self):
        myframe = None
        for _ in range(self.nFrame):
            # wait till camera is recording
            #while not self.cam.acquisition_in_progress():
            # self.cam.start_acquisition()
            #    print(f'camera is still running {self.cam.acquisition_in_progress()}')
            #    time.sleep(0.003)
            #camResult = False
            #while not camResult:
            #    camResult = self.cam.wait_for_frame(since= "lastread",timeout=None)
            #    print(f'camResult is {camResult}')
            #_myframe = self.cam.read_oldest_image()
            _myframe = None
            while _myframe is None:
                _myframe = self.cam.read_newest_image()
                time.sleep(0.003)
            # print(f'new image arrived')

            if myframe is None:
                myframe = _myframe
            else:
                myframe += _myframe
        self.rawImage = myframe/self.nFrame
        return self.rawImage

    def _setExposureTime(self,value): # ms
        # set the expression time

        #if self.worker is not None:
        #    self.worker.pause()
        
        is_acquition = self.cam.acquisition_in_progress()

        with self.lock:
            if is_acquition: 
                print('pausing the acquisition')
                self.stopAcquisition()

            print(f'set Exposure Time {value}')
            self.cam.set_exposure(value/1000)     
            self.exposureTime = value

            if is_acquition:
                print('re-starting camera acquisition')
                self.startAcquisition()

        #print(f'camera_progress is {self.cam.acquisition_in_progress()}')

        #while not self.cam.acquisition_in_progress():
        #    self.cam.start_acquisition()
        #    print(f'camera_progress is {self.cam.acquisition_in_progress()}')
        #    time.sleep(0.003)

        #if self.worker is not None:
        #    self.worker.resume()


    def _getExposureTime(self):
        self.exposureTime = self.cam.get_exposure()*1000
        return self.exposureTime


    def startAcquisition(self):
        # wrapper for start_acquistion
        self.cam.start_acquisition()
        self.cam.start_acquisition()

    def stopAcquisition(self):
        # wrapper for start_acquition
        self.cam.stop_acquisition()

    def getExposure(self):
        return self.cam.get_exposure()




#%%

if __name__ == '__main__':
    pass

#%%

