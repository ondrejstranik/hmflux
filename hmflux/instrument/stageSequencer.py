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


class StageSequencer(RecordSequencer):
    ''' class to control recording images for given slm and shifting the stage.
        synchronous acquisition
    '''
    DEFAULT = {'name': 'StageSequencer',
               'numberOfImage': 10,
               'shiftVector': np.array([1,0,0])}

    def __init__(self, name=None, **kwargs):
        ''' initialisation '''

        if name== None: name= StageSequencer.DEFAULT['name']
        super().__init__(name=name, **kwargs)

        # recording parameters
        self.numberOfImage = StageSequencer.DEFAULT['numberOfImage']
        self.shiftVector = StageSequencer.DEFAULT['shiftVector']
        self.dataFolder = str(Path(hmflux.dataFolder).joinpath('dataset'))


    def loop(self):

        # for synchronisation reasons it stop the camera acquisition
        self.camera.stopAcquisition()

        # check if the folder exist, if not create it
        p = Path(self.dataFolder)
        p.mkdir(parents=True, exist_ok=True)

        initialPosition = self.stage.getParameter('position')


        ''' finite loop of the sequence'''
        for ii in range(self.numberOfImage):
            print(f'recording {ii} image')
            # get image
            self.camera.startAcquisition()
            self.image = self.camera.getLastImage()
            self.camera.stopAcquisition()
            # save image
            np.save(self.dataFolder + '/' + 'image' + f'_{ii:03d}',self.image)
            yield
            # move stage
            self.stage.setParameter('position',initialPosition + (ii+1)*self.shiftVector)

            # keybord abort of the action
            if keyboard.is_pressed('ctrl+q'):
                print("Loop aborted")


            
       


#%%

# TODO: test it!
if __name__ == '__main__':
    pass
