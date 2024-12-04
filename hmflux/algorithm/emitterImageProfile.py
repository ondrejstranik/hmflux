'''
class for managing images of emitter
'''
#%%
import numpy as np
import time


class EmitterImageProfile:
    ''' container of images of emitter '''
    DEFAULT = {}


    def __init__(self,imageSet:np.ndarray = None, **kwarg):
        ''' initialization of the parameters '''
        self.imageSet = imageSet
        self.signal = None 
        
    def setImageSet(self,imageSet):
        ''' set imageSet'''
        self.imageSet = imageSet

    def getImageSet(self):
        ''' return imageSet'''
        return self.imageSet

    def getSignal(self):
        ''' calculate signal from image set'''
        self.signal = self.imageSet

        return self.signal

        
#%%

if __name__ == "__main__":
    pass

# %%
