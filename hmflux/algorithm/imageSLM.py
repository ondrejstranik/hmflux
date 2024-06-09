'''
class to generate specific pattern on slm for the holomin flux algorithm'''

import numpy as np

class ImageSLM:
    ''' class to generate specific pattern on slm for holominflux algorithm'''

    DEFAULT = {'clip':True,
               'clipMin': 0,
               'clipMax':255}

    def __init__(self):
        ''' initialisation'''

        self.image = None
        self.sizeX = None
        self.sizeY = None

        self.clip = self.DEFAULT['clip']
        
    def clipValue(self,image):
        if self.clip:
            image[image<self.DEFAULT['clipMin']] = self.DEFAULT['clipMin']
            image[image>self.DEFAULT['clipMax']] = self.DEFAULT['clipMax']
        return image

    def setClip(self,value:bool):
        self.clip = value

    def setSizeSLM(self,sizeX,sizeY):
        
        # if not changes than do not clear the image 
        if ((self.sizeX is not None) and (self.sizeY is not None) and
            (self.sizeX ==sizeX) and (self.sizeY == sizeY)):
            return

        self.sizeX = sizeX
        self.sizeY = sizeY
        self.generateConstant()

    def generateConstant(self,value=0):
        self.image = self.clipValue(np.zeros((self.sizeY,self.sizeX)) + value)
        return self.image

    def generateSinGrating(self,stepIdx=0,nStep= 10,period=50):
        ''' sinus grating'''
        # set testing image (for internal use only)
        X,Y = np.meshgrid(np.linspace(0,self.sizeX,self.sizeX),np.linspace(0,self.sizeY,self.sizeY))
        self.image = self.clipValue(np.round((2**8-1)*(0.5+0.5*np.sin(2*np.pi*X/period+1.0*stepIdx/nStep*np.pi))).astype('uint8'))

        return self.image

    def generateBinaryGrating(self,axis=0,val0=0,val1=255):
        ''' binary grating '''
        
        im  = np.zeros((self.sizeY,self.sizeX))+ val0
        if axis == 0:
            im[::2,:]= val1
        else:
            im[:,::2]= val1
        self.image = self.clipValue(im)

        return im

    def generateBox1(self,axis=0,position= None, val0=0,val1=255,halfwidth=6,bcgImage=None):
        ''' box generation for minima'''

        # define background
        if bcgImage is None:
            im = np.zeros((self.sizeY,self.sizeX))
        else:
            im = bcgImage

        # define position
        if position is None:
            if axis == 0: position = self.sizeY//2
            else: position = self.sizeX//2

        if axis == 0:
            im[position-halfwidth:position,:]= val0
            im[position:position+halfwidth,:]= val1           
        else:
            im[:,position-halfwidth:position]= val0
            im[:,position:position+halfwidth]= val1 
        
        self.image = self.clipValue(im)

        return im





if __name__ == '__main__':

    pass



#%%


