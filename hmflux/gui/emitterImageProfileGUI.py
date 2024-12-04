'''
class to show emitter Image viewer
'''
#%%
from viscope.gui.baseGUI import BaseGUI
from hmflux.gui.emitterImageProfileViewer import EmitterImageProfileViewer

class EmitterImageProfileGUI(BaseGUI):
    ''' main class to show emitter Image viewer'''

    DEFAULT = {'nameGUI': 'Emitter Image'}

    def __init__(self, viscope, **kwargs):
        ''' initialise the class '''
        super().__init__(viscope, **kwargs)

        # prepare the gui of the class
        EmitterImageProfileGUI.__setWidget(self) 

    def __setWidget(self):
        ''' prepare the gui '''

        self.emitterImageProfileViewer = EmitterImageProfileViewer(show=False)

        self.viewer = self.emitterImageProfileViewer.viewer

        self.vWindow.addMainGUI(self.viewer.window._qt_window, name=self.DEFAULT['nameGUI'])

    def setData(self,emitterImage):
        ''' set the data'''
        self.emitterImageProfileViewer.setEmitterProfileImage(emitterImage=emitterImage)

if __name__ == "__main__":
    pass



