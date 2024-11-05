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

from hmflux.algorithm.imageSLM import ImageSLM


class SlmSequencerSlant(RecordSequencer):
    ''' class to control recording images for given slm and shifting the stage.
        synchronous acquisition
    '''
    DEFAULT = {'name': 'SlmSequencerSl',
               'shiftVector': np.array([1,0,0]),
               'valMin':0,
               'valMax':255,
               'startOffset':0,
               'constantVal':0,
               'slantAxis':0,
               'laserPower': 100} # in mW

    def __init__(self, name=None, **kwargs):
        ''' initialisation '''

        if name== None: name= SlmSequencerSlant.DEFAULT['name']
        super().__init__(name=name, **kwargs)

        # recording parameters
        self.shiftVector = SlmSequencerSlant.DEFAULT['shiftVector']
        self.dataFolder = str(Path(hmflux.dataFolder).joinpath('dataset'))
        self.laserPower = SlmSequencerSlant.DEFAULT['laserPower']

        self.valMin = SlmSequencerSlant.DEFAULT['valMin']
        self.valMax = SlmSequencerSlant.DEFAULT['valMax']
        self.startOffset = SlmSequencerSlant.DEFAULT['startOffset']

        self.image = None
        self.imageSet = None
        self.roi = None

        self.imageSLMGen = ImageSLM()
        self.slantAxis = SlmSequencerSlant.DEFAULT['slantAxis']
        self.constantVal = SlmSequencerSlant.DEFAULT['constantVal']

    def loop(self):

        # for synchronisation reasons it stop the camera acquisition
        self.camera.stopAcquisition()

        # check if the folder exist, if not create it
        p = Path(self.dataFolder)
        p.mkdir(parents=True, exist_ok=True)

        if self.laser is not None:
            originalLaserPower = self.laser.getParameter('power')
            self.laser.setParameter('power',self.laserPower)

        self.val1 = int(self.valMax // 3)
        self.val2 = int(self.valMax / 3 * 2)

        offsetTable = np.arange(self.startOffset,255-self.valMax+1)


        self.imageSLMGen.setSizeSLM(self.slm.sizeX,self.slm.sizeY)
        
        ''' finite loop of the sequence'''
        for offset in offsetTable:
            print(f'recording offset {offset} image')
            slmImageSlant = self.imageSLMGen.generateConstant(self.constantVal)
            slmImageSlant += self.imageSLMGen.generateSlantedGrating(self.slantAxis,self.valMin+offset,self.val1+offset,self.val2+offset,self.valMax+offset)
            self.slm.setImage(slmImageSlant)
            # get image
            self.camera.startAcquisition()
            self.image = self.camera.getLastImage()
            self.camera.stopAcquisition()
            #select ROI from image
            if self.roi is not None:
                self.image = self.image[self.roi[1]:self.roi[1]+self.roi[3],
                                        self.roi[0]:self.roi[0]+self.roi[2]]

            # add image to the imageSet
            if offset==offsetTable[0]:
                self.imageSet = np.empty((np.shape(offsetTable)[0],*self.image.shape))
                ii = 0
            self.imageSet[ii,...] = self.image
            ii += 1

                # save image
                # to speedup recording the saving is done at the end
                #np.save(self.dataFolder + '/' + 'image' + f'_{ii:03d}',self.image)
            
            yield

            # keybord abort of the action
            if keyboard.is_pressed('ctrl+q'):
                print("Loop aborted")
                break
        np.save(self.dataFolder + '/' + f'imageSet{offset}',self.imageSet)

        if self.laser is not None:
            self.laser.setParameter('power',originalLaserPower)
            


#%%

# TODO: test it!
if __name__ == '__main__':
    pass
#%%
