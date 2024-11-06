#%%
import napari
import os
import numpy as np
from pathlib import Path
import pyqtgraph as pg

path = r'.\hmflux\DATA\dataset_000'
# path = r'E:\ZihaoData\DATA\PrimeBSI\20240801-horizontal_001'
# pathConsant = (path+'./'+'Binary')
# pathBox = (path+'./'+'Box')
# pathDark = (path+'./'+'Dark')

constantImage = []
boxImage = []
darkImage = []

filenames = os.listdir(path)
# filenames = os.listdir(pathBox)
# filenames = os.listdir(pathConsant)

#%%

for filename in filenames:
    # cImage = np.load(pathConsant+'./'+filename)
    # constantImage.append(cImage)
    # bImage = np.load(pathBox+'./'+filename)
    # boxImage.append(bImage)
    # dImage = np.load(pathDark+'./'+filename)
    # darkImage.append(dImage)
    bImage = np.load(path+'./'+filename)
    boxImage.append(bImage)

viewer = napari.Viewer()
# viewer.add_image(np.array(constantImage), name='binary')
viewer.add_image(np.array(boxImage), name='box')
# viewer.add_image(np.array(darkImage), name='dark')
intensitySum = np.sum(boxImage,axis=(1,2))
pg.plot(intensitySum)

napari.run()

#%%
