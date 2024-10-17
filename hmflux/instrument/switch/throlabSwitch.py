#%%
'''class to control a thorlab wheel switch'''

import numpy as np
import time

from viscope.instrument.base.baseSwitch import BaseSwitch
from microscope.filterwheels.thorlabs import ThorlabsFilterWheel

class ThrolabSwitch(BaseSwitch):
    ''' main class to control a thorlab wheel switch'''
    DEFAULT = {'name':'thorlabFilterWheel',
                'initialPosition':5,
                'port': 'COM3'
                }

    def __init__(self,name=DEFAULT['name'], **kwargs):
        ''' switch initialisation'''
        super().__init__(name=name, **kwargs)
        
        self._port= kwargs['port'] if 'port' in kwargs else ThrolabSwitch.DEFAULT['port']
        self._device = None


    def _setPosition(self,positionNumber):
        ''' set the position in the switcher '''
        self.position = positionNumber
        self._device.position = self.position

    def _getPosition(self):
        ''' get the position of the switcher '''
        self.position = self._device.position
        return self.position
        
    def connect(self,initialPosition=DEFAULT['initialPosition'],port=None):
        super().connect()
        
        if port is not None: self._port = port

        self._device = ThorlabsFilterWheel(com=self._port)
        
        self.setParameter('position',initialPosition)

    def disconnect(self):
        super().disconnect()
        self._device.shutdown()


if __name__ == '__main__':

    pass





# %%