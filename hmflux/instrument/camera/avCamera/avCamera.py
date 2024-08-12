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

from vmbpy import * 


class AVCamera(BaseCamera):
    ''' class to control allied Vision camera. use vmbpy package '''
    DEFAULT = {'name': 'AVCamera',
                'exposureTime': 10, # ms initially automatically set the exposure time
                'nFrame': 1,
                'idx': 0,
                'blackLevel':5

}

    def __init__(self, name=None, idx=None, **kwargs):
        ''' initialisation '''

        if name is None: name=AVCamera.DEFAULT['name'] 
        super().__init__(name=name,**kwargs)
        
        # camera parameters
        self.exposureTime = AVCamera.DEFAULT['exposureTime']
        self.nFrame = AVCamera.DEFAULT['nFrame']

        self.idx = idx if idx is not None else AVCamera.DEFAULT['idx']
        self.cam = None
        self.vmb = None

        self.blackLevel = AVCamera.DEFAULT['blackLevel']


    def connect(self):
        super().connect()

        self.vmb = VmbSystem.get_instance()
        self.vmb.__enter__()

        self.cam = self.vmb.get_all_cameras()[self.idx]
        self.cam.__enter__()

        self.width = self.cam.get_feature_by_name('Width').get()
        self.height = self.cam.get_feature_by_name('Height').get()

        # set camera exposure time 
        self.cam.get_feature_by_name('ExposureTime').set(self.exposureTime*1000)
        #self.cam.get_feature_by_name('ExposureAuto').set('Off')
        #self.cam.get_feature_by_name('ExposureMode').set('Timed')
        
        #ZH black level
        self.cam.get_feature_by_name('BlackLevel').set(self.blackLevel)


    def disconnect(self):

        self.cam.__exit__(0,None,None)
        self.cam = None
        self.vmb.__exit__(0,None,None)
        super().disconnect()

    def getLastImage(self):
        ''' synchronous acquisition of the frame 
        only black/white camera implemented'''
        _frame = None
 
        for frame in self.cam.get_frame_generator(limit=self.nFrame, timeout_ms=int(self.exposureTime)*3 +100):
                if _frame is None:
                    _frame = frame.as_numpy_ndarray()[:,:,0].astype('float')
                else:
                    _frame = _frame + frame.as_numpy_ndarray()[:,:,0]
        self.rawImage = _frame/self.nFrame
        return self.rawImage                    

    def _setExposureTime(self,value): # ms
        # set the expression time
        self.exposureTime = value
        self.cam.get_feature_by_name('ExposureTime').set(self.exposureTime*1000)

    def _getExposureTime(self):
        self.exposureTime = self.cam.get_feature_by_name('ExposureTime').get()/1000
        return self.exposureTime


#%%

if __name__ == '__main__':
    pass


