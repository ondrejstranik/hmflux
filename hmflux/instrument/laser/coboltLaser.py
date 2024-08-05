#%%
''' class to control cobolt laser via microsocpe package'''

from viscope.instrument.base.baseLaser import BaseLaser
from microscope.lights.cobolt import CoboltLaser as MCLaser

class CoboltLaser(BaseLaser):
    ''' base class of cobolt laser
    '''

    DEFAULT = {'name':'coboltLaser',
                'power': 0, #mW
                'keySwitch': False,
                'port': 'COM4',
                  } 
    
    def __init__(self,name=DEFAULT['name'], **kwargs):
        ''' laser initialisation'''
        super().__init__(name=name,**kwargs)
        
        self.power = None
        self.keySwitch = None

        self._port= kwargs['port'] if 'port' in kwargs else CoboltLaser.DEFAULT['port']
        self._device = None

    def connect(self,**kwargs):
        ''' connect to the laser '''
        super().connect()
        self._device = MCLaser(com=self._port)

        # prepare the laser
        self.setParameter('keySwitch',CoboltLaser.DEFAULT['power'])
        self.setParameter('power',CoboltLaser.DEFAULT['keySwitch'])

    def disconnect(self):
        super().disconnect()
        self._device.shutdown()

    def _setPower(self,value):
        ''' value in mW'''
        self.power = value
        self._device.power = value/1000

    def _setKeySwitch(self,value):
        self.keySwitch = value
        if self.keySwitch:
            self._device.enable()
        if not self.keySwitch:
            self._device.disable()
    
    def _getPower(self):
        ''' value in mW'''
        self.power = self._device.power*1000
        return self.power

    def _getKeySwitch(self):
        return self.keySwitch

if __name__ == '__main__':
    pass






# %%