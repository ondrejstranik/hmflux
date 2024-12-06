''' script to visualise dip'''

#%% import and parameter defintion

import numpy  as np
import napari
import matplotlib.pyplot as plt

fFolder = r'g:\office\work\projects - funded\23-02-24 holominflux\DATA\20241205_dip_homoillu_100mW10ms'

fName = r'Image_0.npy'


#%% load data 

im = np.load(fFolder + '\\' + fName)


# %% display data
viewer = napari.Viewer()
viewer.add_image(im)

#%% define slice
pos = 1400
nAve = 3
slice = np.mean(im[:,pos:pos+nAve], axis=1)

#fig, ax = plt.subplots()
#ax.plot(slice)

# %% calculate background value

_med = np.median(slice)
#hist, bin_edges = np.histogram(slice,bins = np.arange(0,5*_med,0.1))
#val = bin_edges[:-1] + (bin_edges[1] - bin_edges[0])/2
#bcgValue = val[np.argmax(hist)]

# as simple way
bcgValue = _med

print(f'background value is {bcgValue}')

#fig, ax = plt.subplots()
#ax = plt.plot(val, hist)


# %% find peak and dips

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

#%% plot results


fig, ax = plt.subplots()
ax.plot(slice)
ax.plot([peakLPosition,dipPosition,peakRPosition],[peakLValue,dipValue,peakRValue], 'ro')
ax.plot(slice*0+bcgValue)

ax.set_title(f'contrast: {contrast} \n @ x-position {pos} averaged pixel {nAve}')

plt.show()








# %%
