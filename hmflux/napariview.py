#%%
import napari
import os
import numpy as np
from pathlib import Path

path = r'C:\Users\ZihaoXiao\Documents\GitHub\hmflux\hmflux\DATA\20240624-marker-1-hw1'
pathConsant = (path+'./'+'Binary')
pathBox = (path+'./'+'Box')



constantImage = []
boxImage = []

nFile = len(os.listdir(pathBox))
filenameConst = 'Image_{}.npy'
filenameBox = filenameConst

#%%

for ii in range(nFile):
    cImage = np.load(pathConsant+'./'+filenameConst.format(ii))
    constantImage.append(cImage)
    bImage = np.load(pathBox+'/'+filenameBox.format(ii))
    boxImage.append(bImage)


viewer = napari.Viewer()
viewer.add_image(np.array(constantImage), name='binary')
viewer.add_image(np.array(boxImage), name='box')
napari.run()
