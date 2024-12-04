'''
class for managing values of the intensity of emitters 
'''
#%%
import numpy as np


class EmitterDataProfile:
    ''' container for signal from emitters
        (this is a copy of a class spotDAta from package --plim--) '''
    DEFAULT = {}


    def __init__(self,signal=None,axis=None,**kwarg):
        ''' initialization of the parameters '''
        #TODO: implement signal and time definition for a single values. 

        self.signal = None # numpy array, each column represent signal from one spot
        
        if signal is not None: self.signal = np.array(signal)  
        if axis is not None: self.axis = np.array(axis) # corresponding axis point

        self.axis0 = self.axis[0] if axis is not None else 1 # position of zero axis point


    def setData(self,signal,axis=None):
        ''' set signal and axis point'''
        self.signal = np.array(signal)
        self.axis = np.array(axis) if axis is not None else np.arange(self.signal.shape[0])  # corresponding axis point
        self.axis0 = self.axis[0]

    def addDataValue(self, valueVector,axis=None):
        ''' add value list to the signal
            return axis0 if data are reset'''
        
        valueVector = np.array(valueVector)
        if self.signal is not None and valueVector.shape[0] == self.signal.shape[1]:
            self.signal = valueVector.T
            return None
        else:
            self.signal = np.array(valueVector)[None,:]
            if axis is not None: 
                self.axis = np.array(axis)[None]
                self.axis0 = self.axis[0] # reset
            else:
                self.axis0 = 0
            return self.axis0
                

    def getData(self):
        ''' return the signal and coordinate '''
        if self.signal is not None:
            if (hasattr(self,'axis')  and self.signal.shape[0] == self.axis.shape[1]):
                return (self.signal,self.axis)
            else:
                return (self.signal,np.arange(self.signal.shape[0]))
        else:
            return (None, None)


    def clearData(self):
        ''' clear the data '''
        self.signal = None
        self.axis = None
        self.axis0 = 1

        #%%

if __name__ == "__main__":
    pass

# %%
