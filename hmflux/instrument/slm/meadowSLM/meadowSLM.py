# Example usage of Blink_C_wrapper.dll
# Meadowlark Optics Spatial Light Modulators
# September 12 2019

import os
import numpy as np
from ctypes import *
from scipy import misc
from time import sleep

# # Load the DLL
# # Blink_C_wrapper.dll, Blink_SDK.dll, ImageGen.dll, FreeImage.dll and wdapi1021.dll
# # should all be located in the same directory as the program referencing the
# # library
# cdll.LoadLibrary("C:\\Program Files\\Meadowlark Optics\\Blink OverDrive Plus\\SDK\\Blink_C_wrapper")
# slm_lib = CDLL("Blink_C_wrapper")

# # Open the image generation library
# cdll.LoadLibrary("C:\\Program Files\\Meadowlark Optics\\Blink OverDrive Plus\\SDK\\ImageGen")
# image_lib = CDLL("ImageGen")

# # Basic parameters for calling Create_SDK
# bit_depth = c_uint(12)
# num_boards_found = c_uint(0)
# constructed_okay = c_uint(-1)
# is_nematic_type = c_bool(1)
# RAM_write_enable = c_bool(1)
# use_GPU = c_bool(1)
# max_transients = c_uint(20)
# board_number = c_uint(1)
# wait_For_Trigger = c_uint(0)
# flip_immediate = c_uint(0) #only supported on the 1024
# timeout_ms = c_uint(5000)
# center_x = c_float(256)
# center_y = c_float(256)
# VortexCharge = c_uint(3)
# fork = c_uint(0)
# RGB = c_uint(0)

# # Both pulse options can be false, but only one can be true. You either generate a pulse when the new image begins loading to the SLM
# # or every 1.184 ms on SLM refresh boundaries, or if both are false no output pulse is generated.
# OutputPulseImageFlip = c_uint(0)
# OutputPulseImageRefresh = c_uint(0); #only supported on 1920x1152, FW rev 1.8. 

from viscope.instrument.base.baseSLM import BaseSLM

class MeadowSLM(BaseSLM):
    DEFAULT = {'name': 'meadowSLM',
               'monitor': 1}
    
    def __init__(self,name=DEFAULT['name'], **kwargs):
        ''' laser initialisation'''
        super().__init__(name=name, **kwargs)

        self.monitor = kwargs['monitor'] if 'monitor' in kwargs else MeadowSLM.DEFAULT['monitor']

        self.slm = None
        
        self._testImage = None

        # restrict the slm value to 0-255
        self.image = np.zeros((self.sizeY,self.sizeX))

        # Load the DLL
        # # Blink_C_wrapper.dll, Blink_SDK.dll, ImageGen.dll, FreeImage.dll and wdapi1021.dll
        # # should all be located in the same directory as the program referencing the
        # # library
        cdll.LoadLibrary("C:\\Program Files\\Meadowlark Optics\\Blink OverDrive Plus\\SDK\\Blink_C_wrapper")
        self.slm_lib = CDLL("Blink_C_wrapper")
        
        # Open the image generation library
        cdll.LoadLibrary("C:\\Program Files\\Meadowlark Optics\\Blink OverDrive Plus\\SDK\\ImageGen")
        self.image_lib = CDLL("ImageGen")

        # Basic parameters for calling Create_SDK
        self.bit_depth = c_uint(12)
        self.num_boards_found = c_uint(0)
        self.constructed_okay = c_uint(-1)
        self.is_nematic_type = c_bool(1)
        self.RAM_write_enable = c_bool(1)
        self.use_GPU = c_bool(1)
        self.max_transients = c_uint(20)
        self.board_number = c_uint(1)
        self.wait_For_Trigger = c_uint(0)
        self.flip_immediate = c_uint(0) #only supported on the 1024
        self.timeout_ms = c_uint(5000)
        self.center_x = c_float(256)
        self.center_y = c_float(256)
        self.VortexCharge = c_uint(3)
        self.fork = c_uint(0)
        self.RGB = c_uint(0)

        # Both pulse options can be false, but only one can be true. You either generate a pulse when the new image begins loading to the SLM
        # or every 1.184 ms on SLM refresh boundaries, or if both are false no output pulse is generated.
        self.OutputPulseImageFlip = c_uint(0)
        self.OutputPulseImageRefresh = c_uint(0); #only supported on 1920x1152, FW rev 1.8. 


    def connect(self,**kwargs):
        super().connect()

        self.slm = self.slm_lib.Create_SDK(self.bit_depth, byref(self.num_boards_found), byref(self.constructed_okay), self.is_nematic_type, self.RAM_write_enable, self.use_GPU, self.max_transients, 0)

        if self.constructed_okay.value == 0:
            print ("Blink SDK did not construct successfully")
		
        if self.num_boards_found.value == 1:
            print ("Blink SDK was successfully constructed")
            print ("Found %s SLM controller(s)" % self.num_boards_found.value)
            self.height = c_uint(self.slm_lib.Get_image_height(self.board_number))
            self.width = c_uint(self.slm_lib.Get_image_width(self.board_number))
            self.depth = c_uint(self.slm_lib.Get_image_depth(self.board_number)) #Bits per pixel
            self.Bytes = c_uint(self.depth.value//8)
            self.center_x = c_uint(self.width.value//2)
            self.center_y = c_uint(self.height.value//2)
			
            if self.width == 512:
                if self.depth == 8:
                    self.slm_lib.Load_LUT_file(self.board_number, b"C:\\Program Files\\Meadowlark Optics\\Blink OverDrive Plus\\LUT Files\\512x512_linearVoltage.LUT")
                if self.depth == 16:
                    self.slm_lib.Load_LUT_file(self.board_number, b"C:\\Program Files\\Meadowlark Optics\\Blink OverDrive Plus\\LUT Files\\512x512_16bit_linearVoltage.LUT")
            if self.width == 1920:
                self.slm_lib.Load_LUT_file(self.board_number, b"C:\\Program Files\\Meadowlark Optics\\Blink OverDrive Plus\\LUT Files\\1920x1152_linearVoltage.LUT")
            if self.width == 1024:
                self.slm_lib.Load_LUT_file(self.board_number, b"C:\\Program Files\\Meadowlark Optics\\Blink OverDrive Plus\\LUT Files\\1024x1024_linearVoltage.LUT")
        
        self.sizeY = self.height.value
        self.sizeX = self.width.value

    def disconnect(self):
        super().disconnect()
        self.slm_lib.Delete_SDK()

    def setImage(self, image):
        self.image = image.astype('uint8')
        self.slm_lib.Write_image(self.board_number, self.image.ctypes.data_as(POINTER(c_ubyte)), self.height.value*self.width.value*self.Bytes.value, self.wait_For_Trigger, self.flip_immediate, self.OutputPulseImageFlip, self.OutputPulseImageRefresh,self.timeout_ms)

    def sizeSLM(self):
        return(self.slm.getSize())


if __name__ == '__main__':

    pass

#%%    