#%%
import napari
import os
import numpy as np
from pathlib import Path

path = r'C:\Users\ZihaoXiao\Documents\GitHub\hmflux\hmflux\DATA\20240624-half2'
pathConsant = (path+'./'+'Constant')
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
viewer.add_image(np.array(constantImage), name='const')
viewer.add_image(np.array(boxImage), name='block')
napari.run()
