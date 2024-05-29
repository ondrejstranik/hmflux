#%%
''' class to control laser'''

import slmpy

import numpy as np
import time
from viscope.instrument.base.baseSLM import BaseSLM


class ScreenSLM(BaseSLM):
    ''' class of spatial light modulator based on slmpy'''

    DEFAULT = {'name':'screenSML',
             'monitor': 1} 
    
    def __init__(self,name=DEFAULT['name'], **kwargs):
        ''' laser initialisation'''
        super().__init__(name=name, **kwargs)

        self.monitor = kwargs['monitor'] if 'monitor' in kwargs else ScreenSLM.DEFAULT['monitor']

        self.slm = None
        
        self._testImage = None


    def connect(self,**kwargs):
        ''' connect to the instrument '''
        super().connect()

        self.slm = slmpy.SLMdisplay(monitor=self.monitor,isImageLock = True)

        self.sizeX, self.sizeY = self.slm.getSize()

        # set image
        self.setImage(np.zeros((self.sizeY,self.sizeX)))

        # set testing image (for internal use only)
        X,Y = np.meshgrid(np.linspace(0,self.sizeX,self.sizeX),np.linspace(0,self.sizeY,self.sizeY))
        self._testImage = np.round((2**8-1)*(0.5+0.5*np.sin(2*np.pi*X/50))).astype('uint8')

    def disconnect(self):
        super().disconnect()

        self.slm.close()
    
    def setImage(self,image):
        self.image = image
        self.slm.updateArray(self.image)



if __name__ == '__main__':

    pass




# %%