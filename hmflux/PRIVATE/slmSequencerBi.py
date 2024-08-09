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


class SlmSequencerBi(RecordSequencer):
    ''' class to control recording images for given slm and shifting the stage.
        synchronous acquisition
    '''
    DEFAULT = {'name': 'SlmSequencerBi',
               'shiftVector': np.array([1,0,0]),
               'valMin':0,
               'valMax':255,
               'initialDifference':1,
               'constantVal':0,
               'binaryAxis':0,
               'laserPower': 100} # in mW

    def __init__(self, name=None, **kwargs):
        ''' initialisation '''

        if name== None: name= SlmSequencerBi.DEFAULT['name']
        super().__init__(name=name, **kwargs)

        # recording parameters
        self.shiftVector = SlmSequencerBi.DEFAULT['shiftVector']
        self.dataFolder = str(Path(hmflux.dataFolder).joinpath('dataset'))
        self.laserPower = SlmSequencerBi.DEFAULT['laserPower']

        self.valMin = SlmSequencerBi.DEFAULT['valMin']
        self.valMax = SlmSequencerBi.DEFAULT['valMax']
        self.initialDifference = SlmSequencerBi.DEFAULT['initialDifference']

        self.image = None
        self.imageSet = None
        self.roi = None

        self.imageSLMGen = ImageSLM()
        self.constantVal = SlmSequencerBi.DEFAULT['constantVal']
        self.binaryAxis = SlmSequencerBi.DEFAULT['binaryAxis']

    def loop(self):

        # for synchronisation reasons it stop the camera acquisition
        self.camera.stopAcquisition()

        # check if the folder exist, if not create it
        p = Path(self.dataFolder)
        p.mkdir(parents=True, exist_ok=True)

        if self.laser is not None:
            originalLaserPower = self.laser.getParameter('power')
            self.laser.setParameter('power',self.laserPower)

        differenceTable = np.arange(self.initialDifference,self.valMax-self.valMin+1)
        self.imageSLMGen.setSizeSLM(self.slm.sizeX,self.slm.sizeY)
        
        ''' finite loop of the sequence'''
        for differnece in differenceTable:
            stepTable = np.arange(self.valMin,self.valMax-differnece+1)
            for value in stepTable:
                print(f'recording {value} image')
                slmImageBi = self.imageSLMGen.generateConstant(self.constantVal)
                slmImageBi += self.imageSLMGen.generateBinaryGrating(self.binaryAxis,value,value+differnece)
                self.slm.setImage(slmImageBi)
                # get image
                self.camera.startAcquisition()
                self.image = self.camera.getLastImage()
                self.camera.stopAcquisition()

                #select ROI from image
                if self.roi is not None:
                    self.image = self.image[self.roi[1]:self.roi[1]+self.roi[3],
                                            self.roi[0]:self.roi[0]+self.roi[2]]

                # add image to the imageSet
                if value==self.valMin:
                    self.imageSet = np.empty((np.shape(stepTable)[0],*self.image.shape))
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
            if keyboard.is_pressed('ctrl+q'):
                    print("Loop aborted")
                    break
            np.save(self.dataFolder + '/' + f'imageSet{differnece}',self.imageSet)
            
    

        


        if self.laser is not None:
            self.laser.setParameter('power',originalLaserPower)
            


#%%

# TODO: test it!
if __name__ == '__main__':
    pass
#%%
