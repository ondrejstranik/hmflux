#%%
import napari
import os
import numpy as np
from pathlib import Path

# path = r'.\hmflux\DATA\20240708-test'
path = r'D:\ZihaoData\DATA\20240705-test1-1'
pathConsant = (path+'./'+'Binary')
pathBox = (path+'./'+'Box')
# pathSLMBi = (path+'./'+'SLMBi')
# pathSLMBox = (path+'./'+'SLMBox')



constantImage = []
boxImage = []
# slmBi = []
# slmBox = []

filenames = os.listdir(pathBox)

# nFile = len(os.listdir(pathBox))
# filenameConst = 'Image_{}.npy'
# filenameBox = filenameConst
# filenameSLMBi = filenameConst
# filenameSLMBox = filenameConst

#%%

for filename in filenames:
    cImage = np.load(pathConsant+'./'+filename)
    constantImage.append(cImage)
    bImage = np.load(pathBox+'./'+filename)
    boxImage.append(bImage)


# for ii in range(nFile):
#     cImage = np.load(pathConsant+'./'+filenameConst.format(ii))
#     constantImage.append(cImage)
#     bImage = np.load(pathBox+'/'+filenameBox.format(ii))
#     boxImage.append(bImage)

    # SLMBiImage = np.load(pathSLMBi+'./'+filenameSLMBi.format(ii))
    # slmBi.append(SLMBiImage)
    # SLMBoxImage = np.load(pathSLMBox+'/'+filenameSLMBox.format(ii))
    # slmBox.append(SLMBoxImage)


viewer = napari.Viewer()
viewer.add_image(np.array(constantImage), name='binary')
viewer.add_image(np.array(boxImage), name='box')
# viewer.add_image(np.array(SLMBiImage), name='SLMBi')
# viewer.add_image(np.array(SLMBoxImage), name='SLMBox')

napari.run()
