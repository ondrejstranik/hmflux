'''
class to generate specific pattern on slm for the holomin flux algorithm'''

import numpy as np
import matplotlib.pyplot as plt

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

    def pixelshift(self, image, shift,axis):
        '''frequency domain pixel shift of sinus grating'''
        spectrum = np.fft.fftshift(np.fft.fft2(image))
        X,Y = np.shape(spectrum)
        if axis == 0:
            sliced = spectrum[int(X/2),:]
            slice_left = sliced[0:int(Y/2-1)]
            slice_right = sliced[int(Y/2+1):np.shape(sliced)[0]]
            slice_left[-1-shift+1:np.shape(slice_left)[0]] = 0+0j
            slice_left = np.roll(slice_left,shift)
            slice_right[0:shift] = 0+0j
            slice_right = np.roll(slice_right,-shift)
            sliced[0:int(Y/2-1)] = slice_left
            sliced[int(Y/2+1):np.shape(sliced)[0]] = slice_right
            spectrum[int(X/2),:] = sliced
        else:
            sliced = spectrum[:,int(Y/2)]  #slice into row array
            slice_left = sliced[0:int(X/2-1)]
            slice_right = sliced[int(X/2+1):np.shape(sliced)[0]]
            slice_left[-1-shift+1:np.shape(slice_left)[0]] = 0+0j
            slice_left = np.roll(slice_left,shift)
            slice_right[0:shift] = 0+0j
            slice_right = np.roll(slice_right,-shift)
            sliced[0:int(X/2-1)] = slice_left
            sliced[int(X/2+1):np.shape(sliced)[0]] = slice_right
            spectrum[:,int(Y/2)] = sliced

        imageShiftedTemp = np.fft.ifft2(np.fft.ifftshift(spectrum))
        imageShiftedTemp = np.abs(imageShiftedTemp)
        imageShifted = np.interp(imageShiftedTemp, (imageShiftedTemp.min(), imageShiftedTemp.max()), (0, 255)).astype(int)
        
        return imageShifted

    def generateConstant(self,value=0):
        self.image = self.clipValue(np.zeros((self.sizeY,self.sizeX)) + value)
        return self.image

    def generateSinGrating(self,axis=0,stepIdx=0,nStep=10,period=50, spectrumShift=0):
        ''' sinus grating'''
        # set testing image (for internal use only)
        X,Y = np.meshgrid(np.linspace(0,self.sizeX,self.sizeX),np.linspace(0,self.sizeY,self.sizeY))
        if axis == 0:
            image1 = self.clipValue(np.round((2**8-1)*(0.5+0.5*np.sin(2*np.pi*X/period+1.0*stepIdx/nStep*np.pi))).astype('uint8'))
        else:
            image1 = self.clipValue(np.round((2**8-1)*(0.5+0.5*np.sin(2*np.pi*Y/period+1.0*stepIdx/nStep*np.pi))).astype('uint8'))
        # image1 = self.image
        im = self.pixelshift(image1, spectrumShift, axis)
        self.image = self.clipValue(im)
        return im

    def generateBinaryGrating(self,axis=0,val0=0,val1=255):
        ''' binary grating '''
        
        im  = np.zeros((self.sizeY,self.sizeX))+ val0
        if axis == 0:
            im[::2,:]= val1
        else:
            im[:,::2]= val1
        self.image = self.clipValue(im)
        return im

    def generateSlanted3Grating(self,axis=0,val0=0,val1=78,val2=154):
        ''' generate slanted three pixel grating
        the values are 0, 2pi/3, 4pi/3'''
        im  = np.zeros((self.sizeY,self.sizeX))+ val0
        if axis == 0:
            im[1::3,:]= val1
            im[2::3,:]= val2
        else:
            im[:,1::3]= val1
            im[:,2::3]= val2
        self.image = self.clipValue(im)

        return im

    def generateSlanted4Grating(self,axis=0,val0=0,val1=59,val2=118,val3=172):
        ''' generate slanted four pixel grating
        it should make homogenous illumination, if the values are 0, pi/2, pi, 3/2*pi'''
        im  = np.zeros((self.sizeY,self.sizeX))+ val0
        if axis == 0:
            im[1::4,:]= val1
            im[2::4,:]= val2
            im[3::4,:]= val3
        else:
            im[:,1::4]= val1
            im[:,2::4]= val2
            im[:,3::4]= val3
        self.image = self.clipValue(im)

        return im

    #internal use, clip the pi shift if it over 255 after adding
    def piClip(self,value,binaryVal):
        # piValue=118
        pi2Value = 225
        # pi2Value = 198
        valTemp = value+binaryVal
        # clipedValue = valTemp if valTemp<255 else valTemp-pi2Value
        clipedValue = valTemp if valTemp<pi2Value else valTemp-pi2Value
        return clipedValue
    
    def generateSlanted6Grating(self,axis=0,val0=0,val1=78,val2=154,binaryVal=118):
        im = np.zeros((self.sizeY,self.sizeX))+ val0
        val01 = self.piClip(val0,binaryVal)
        val11 = self.piClip(val1,binaryVal)
        val21 = self.piClip(val2,binaryVal)
        if axis == 0:
            im[1::6,:]= val1
            im[2::6,:]= val2
            im[3::6,:]= val01
            im[4::6,:]= val11
            im[5::6,:]= val21
        else:
            im[:,1::6]= val1
            im[:,2::6]= val2
            im[:,3::6]= val01
            im[:,4::6]= val11
            im[:,5::6]= val21
        self.image = self.clipValue(im)

        return im
        
    def generateSlanted8Grating(self,axis=0,val0=0,val1=59,val2=118,val3=172,binaryVal=118):
        ''' generate slanted eight pixel grating, the values are 0, pi/2, pi, 3/2*pi
        but with the 0 pi modulation, one period plus 0, next period plus pi, then next
        plus 0'''
        im = np.zeros((self.sizeY,self.sizeX))+ val0
        val01 = self.piClip(val0,binaryVal)
        val11 = self.piClip(val1,binaryVal)
        val21 = self.piClip(val2,binaryVal)
        val31 = self.piClip(val3,binaryVal)
        if axis == 0:
            im[1::8,:]= val1
            im[2::8,:]= val2
            im[3::8,:]= val3
            im[4::8,:]= val01
            im[5::8,:]= val11
            im[6::8,:]= val21
            im[7::8,:]= val31
        else:
            im[:,1::8]= val1
            im[:,2::8]= val2
            im[:,3::8]= val3
            im[:,4::8]= val01
            im[:,5::8]= val11
            im[:,6::8]= val21
            im[:,7::8]= val31
        self.image = self.clipValue(im)

        return im

    def generateBox1(self,axis=0,position= None, val0=0,val1=255,halfwidth=3,bcgImage=None):
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
    
    def generateBox2(self,axis=0,position= None, val0=0,val1=255,weightFactor=0,compensation=0,halfwidth=2,bcgImage=None):
        ''' type2 box generation for minima'''

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
            im[position-halfwidth:position,:]= val0+compensation
            im[position+1:position+halfwidth+1,:]= val1-compensation
            im[position,:]=weightFactor*val0+(1-weightFactor)*val1
            im[position-halfwidth-1,:]=weightFactor*val0+(1-weightFactor)*im[position-halfwidth-2,:]
            im[position+halfwidth+1,:]=weightFactor*im[position+halfwidth+2,:]+(1-weightFactor)*val1
        else:
            im[:,position-halfwidth:position]= val0+compensation
            im[:,position+1:position+halfwidth+1]= val1-compensation
            im[:,position]=weightFactor*val0+(1-weightFactor)*val1
            im[:,position-halfwidth-1]=weightFactor*val0+(1-weightFactor)*im[:,position-halfwidth-2]
            im[:,position+halfwidth+1]=weightFactor*im[:,position+halfwidth+2]+(1-weightFactor)*val1
            
        
        self.image = self.clipValue(im)

        return im





if __name__ == '__main__':

    pass



#%%


