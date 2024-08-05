"""
plasmon processor - process the spectral images

Created on Mon Nov 15 12:08:51 2021

@author: ostranik
"""
#%%

from viscope.instrument.base.baseSequencer import BaseSequencer


class RecordSequencer(BaseSequencer):
    ''' helper class to control recording images by given parameters of stage and slm
    it defines the hardware. 
    '''
    DEFAULT = {'name': 'RecordSequencer'}

    def __init__(self, name=None, **kwargs):
        ''' initialisation '''

        if name== None: name= RecordSequencer.DEFAULT['name']
        super().__init__(name=name, **kwargs)
        
        # devices
        self.camera = None
        self.stage = None
        self.slm = None
        self.laser = None

        self.dataFolder = None

        # ROI of the camera
        self.roi = None


    def connect(self,camera=None,stage=None,slm=None,laser=None):
        ''' connect sequencer with the camera, stage, slm '''
        super().connect()
        if camera is not None: self.setParameter('camera',camera)
        if stage is not None: self.setParameter('stage',stage)
        if slm is not None: self.setParameter('slm',slm)
        if laser is not None: self.setParameter('laser',laser)

    def setParameter(self,name, value):
        ''' set parameter of the spectral camera'''
        super().setParameter(name,value)

        if name== 'camera':
            self.camera = value
        if name== 'stage':
            self.stage = value
        if name== 'slm':
            self.slm = value
        if name== 'laser':
            self.laser = value
        if name== 'roi':
            self.roi = value

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
        if name== 'laser':
            return self.laser

        if name== 'roi':
            return self.roi



#%%

# TODO: test it!
if __name__ == '__main__':
    pass
