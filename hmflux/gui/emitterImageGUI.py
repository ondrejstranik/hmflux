'''
class to show emitter Image viewer
'''
#%%
from viscope.gui.baseGUI import BaseGUI
from hmflux.gui.emitterImageViewer import EmitterImageViewer

class EmitterImageGUI(BaseGUI):
    ''' main class to show emitter Image viewer'''

    DEFAULT = {'nameGUI': 'Emitter Image'}

    def __init__(self, viscope, **kwargs):
        ''' initialise the class '''
        super().__init__(viscope, **kwargs)

        # prepare the gui of the class
        EmitterImageGUI.__setWidget(self) 

    def __setWidget(self):
        ''' prepare the gui '''

        self.emitterImageViewer = EmitterImageViewer(show=False)

        self.viewer = self.emitterImageViewer.viewer

        self.vWindow.addMainGUI(self.viewer.window._qt_window, name=self.DEFAULT['nameGUI'])

    def setData(self,emitterImage):
        ''' set the data'''
        self.emitterImageViewer.setEmitterImage(emitterImage=emitterImage)

if __name__ == "__main__":
    pass



