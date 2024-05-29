'''
class to generate specific pattern on slm for the holomin flux algorithm'''

import numpy as np

class ImageSLM:
    ''' class to generate specific pattern on slm for holominflux algorithm'''

    def __init__(self):
        ''' initialisation'''

        self.image = None
        self.sizeX = None
        self.sizeY = None

    def setSizeSLM(self,sizeX,sizeY):
        
        # if not changes than do not clear the image 
        if ((self.sizeX is not None) and (self.sizeY is not None) and
            (self.sizeX ==sizeX) and (self.sizeY == sizeY)):
            return

        self.sizeX = sizeX
        self.sizeY = sizeY
        self.clearImage()

    def clearImage(self):
        self.image = np.zeros((self.sizeY,self.sizeX))

    def generateSinGrating(self,stepIdx=0,nStep= 10):
        ''' sinus grating'''
        # set testing image (for internal use only)
        X,Y = np.meshgrid(np.linspace(0,self.sizeX,self.sizeX),np.linspace(0,self.sizeY,self.sizeY))
        self.image = np.round((2**8-1)*(0.5+0.5*np.sin(2*np.pi*X/50+1.0*stepIdx/nStep*np.pi))).astype('uint8')

        return self.image

    def generateBinaryGrating(self,axis=0):
        ''' binary grating '''
        
        im  = np.zeros((self.sizeY,self.sizeX)).astype('uint8')
        if axis == 0:
            im[::2,:]= (2**8-1)
        else:
            im[:,::2]= (2**8-1)
        self.image = im

        return im



if __name__ == '__main__':

    pass






