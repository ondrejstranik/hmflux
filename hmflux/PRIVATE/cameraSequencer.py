"""
plasmon processor - process the spectral images

Created on Mon Nov 15 12:08:51 2021

@author: ostranik
"""
#%%
import hmflux
from hmflux.instrument.recordSequencer import RecordSequencer
import numpy as np
import keyboard
from pathlib import Path


class CameraSequencer(RecordSequencer):
    ''' class to control recording images for given slm and shifting the stage.
        synchronous acquisition
    '''
    DEFAULT = {'name': 'CameraSequencer',
               'numberOfImage': 10,
               'shiftVector': np.array([1,0,0]),
               'laserPower': 100} # in mW

    def __init__(self, name=None, **kwargs):
        ''' initialisation '''

        if name== None: name= CameraSequencer.DEFAULT['name']
        super().__init__(name=name, **kwargs)

        # recording parameters
        self.numberOfImage = CameraSequencer.DEFAULT['numberOfImage']
        self.shiftVector = CameraSequencer.DEFAULT['shiftVector']
        self.dataFolder = str(Path(hmflux.dataFolder).joinpath('dataset'))
        self.laserPower = CameraSequencer.DEFAULT['laserPower']

        self.image = None
        self.imageSet = None
        self.roi = None

    def loop(self):

        # for synchronisation reasons it stop the camera acquisition
        self.camera.stopAcquisition()

        # check if the folder exist, if not create it
        p = Path(self.dataFolder)
        p.mkdir(parents=True, exist_ok=True)

        if self.laser is not None:
            originalLaserPower = self.laser.getParameter('power')
            self.laser.setParameter('power',self.laserPower)

        ''' finite loop of the sequence'''
        for ii in range(self.numberOfImage):
            print(f'recording {ii} image')
            # get image
            self.camera.startAcquisition()
            self.image = self.camera.getLastImage()
            self.camera.stopAcquisition()

            #select ROI from image
            if self.roi is not None:
                self.image = self.image[self.roi[1]:self.roi[1]+self.roi[3],
                                        self.roi[0]:self.roi[0]+self.roi[2]]

            # add image to the imageSet
            if ii==0:
                self.imageSet = np.empty((self.numberOfImage,*self.image.shape))
            self.imageSet[ii,...] = self.image

            # save image
            # to speedup recording the saving is done at the end
            #np.save(self.dataFolder + '/' + 'image' + f'_{ii:03d}',self.image)
            
            yield

            # keybord abort of the action
            if keyboard.is_pressed('ctrl+q'):
                print("Loop aborted")
                break


        if self.laser is not None:
            self.laser.setParameter('power',originalLaserPower)

        # save image set    
        np.save(self.dataFolder + '/' + 'imageSet',self.imageSet)


#%%

# TODO: test it!
if __name__ == '__main__':
    pass
