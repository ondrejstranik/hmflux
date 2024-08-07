#%%
import napari
import os
import numpy as np
from pathlib import Path

path = r'.\hmflux\DATA\20240723-autoTest'
# path1 = r'.\hmflux\DATA'
# path = r'D:\ZihaoData\DATA\PrimeBSI\20240718-100'
pathConsant = (path+'./'+'Binary')
pathBox = (path+'./'+'Box')
# pathSLMBi = (path+'./'+'SLMBi')
# pathSLMBox = (path+'./'+'SLMBox')


constantImage = []
boxImage = []
# testImage = []
# slmBi = []
# slmBox = []

# testFile = ['Image_000.npy','Image_001.npy']
# tempImage = np.load(path1+'./'+testFile[0])
# testImage.append(tempImage)
# tempImage = np.load(path1+'./'+testFile[1])
# testImage.append(tempImage)

# filenames = os.listdir(pathBox)
filenames = os.listdir(pathConsant)

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
# viewer.add_image(np.array(testImage), name='test')
# viewer.add_image(np.array(SLMBiImage), name='SLMBi')
# viewer.add_image(np.array(SLMBoxImage), name='SLMBox')

napari.run()

#%%
