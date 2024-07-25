#%%
import napari
import os
import numpy as np
from pathlib import Path

# path = r'.\hmflux\DATA\20240723-autoTest-1'
path = r'E:\ZihaoData\DATA\PrimeBSI\20240725-100'
# pathConsant = (path+'./'+'Binary')
pathBox = (path+'./'+'Box')
# pathDark = (path+'./'+'Dark')

constantImage = []
boxImage = []
darkImage = []

filenames = os.listdir(pathBox)
# filenames = os.listdir(pathConsant)

#%%

for filename in filenames:
    # cImage = np.load(pathConsant+'./'+filename)
    # constantImage.append(cImage)
    bImage = np.load(pathBox+'./'+filename)
    boxImage.append(bImage)
    # dImage = np.load(pathDark+'./'+filename)
    # darkImage.append(dImage)

viewer = napari.Viewer()
# viewer.add_image(np.array(constantImage), name='binary')
viewer.add_image(np.array(boxImage), name='box')
# viewer.add_image(np.array(darkImage), name='dark')

napari.run()

#%%
