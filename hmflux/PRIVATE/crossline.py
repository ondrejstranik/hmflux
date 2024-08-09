#%%
import numpy as np
import matplotlib.pyplot as plt
import napari

path = r'E:\ZihaoData\DATA\PrimeBSI'
filenames = ['Image_0.npy','Image_1.npy']

images = []
for filename in filenames:
    image = np.load(path+'./'+filename)
    images.append(image)

# viewer = napari.Viewer()
# viewer.add_image(np.array(images))

temp = images[0]
crossLine = temp[:,1300]
plt.plot(np.arange(np.shape(temp)[0]),crossLine)


temp = images[1]
crossLine1 = temp[800,:]
plt.figure()
plt.plot(np.arange(np.shape(temp)[0]),crossLine1)

plt.show()
