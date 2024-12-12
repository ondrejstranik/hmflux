''' script to visualise dip'''

#%% import and parameter defintion

import numpy  as np
import napari
import matplotlib.pyplot as plt


#%% define slice

class SeeDip:
    def __init__(self):
        self.nAve = 0

    def setnAve(self, nAve):
        self.nAve = nAve

    def calContrast(self, im, axis):
        if axis == 0:
            slice = np.mean(im[:,:], axis=0)

        elif axis == 1:
            slice = np.mean(im[:,:], axis=1)

        _med = np.median(slice)
        #hist, bin_edges = np.histogram(slice,bins = np.arange(0,5*_med,0.1))
        #val = bin_edges[:-1] + (bin_edges[1] - bin_edges[0])/2
        #bcgValue = val[np.argmax(hist)]

        # as simple way
        bcgValue = _med

        # print(f'background value is {bcgValue}')

        # find peak and dips

        _max = np.max(slice)
        _mask = (slice > _max/3)
        idx = np.arange(len(_mask))[_mask]

        r1 = np.min(idx)
        r2 = np.max(idx)

        dip = slice[r1:r2]

        dipValue = np.min(dip)
        _dipPosition = np.argmin(dip)
        peakLValue = np.max(dip[0:_dipPosition])
        _peakLPosition = np.argmax(dip[0:_dipPosition])
        peakRValue = np.max(dip[_dipPosition:])
        _peakRPosition = np.argmax(dip[_dipPosition:])

        dipPosition = _dipPosition + r1
        peakLPosition = _peakLPosition + r1
        peakRPosition  = _peakRPosition + dipPosition

        contrast = (((peakLValue + peakRValue)/2 - bcgValue) /
                    (dipValue -  bcgValue))
        
        return contrast


# %%
