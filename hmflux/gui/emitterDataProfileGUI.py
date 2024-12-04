'''
class for viewing signals from spots' plasmon resonance
'''

import pyqtgraph as pg
from viscope.gui.baseGUI import BaseGUI
from PyQt5.QtGui import QColor, QPen
from qtpy.QtWidgets import QWidget,QVBoxLayout
from magicgui import magicgui

import numpy as np
from hmflux.algorithm.emitterDataProfile import EmitterDataProfile

class EmitterDataProfileGUI(BaseGUI):
    ''' main class for viewing emitter signal'''
    DEFAULT = {'nameGUI':'Emitter Signal'}

    def __init__(self,viscope, **kwargs):
        ''' initialise the class '''
        super().__init__(viscope, **kwargs)

        self.eD = EmitterDataProfile()

        self.fitParameter = None
        self.graph = None
        
        self.viewer = None
        self.maskLayer = None
        self.pointLayer = None

        # set this gui of this class
        EmitterDataProfileGUI._setWidget(self)

    def _setWidget(self):
        ''' prepare the gui '''

        @magicgui(auto_call=True,
                  xPos={'max':10000},
                  yPos={'max':10000},
                  length={'max':10000},
                  coordinate={'max':10000},
                  axisDirection={'min':0,'max':1})
        def fitParameter(
            xPos: int = 0,
            yPos: int = 0,
            length: int = 20,
            coordinate: int = 0,
            axisDirection: int = 0  # 0 is Y, 1 is X
            ):
            self.device.xPos = xPos
            self.device.yPos = yPos
            self.device.length = length
            self.device.axisDirection = axisDirection
            if axisDirection == 0:
                coordinate = yPos
                self.device.coordinate = coordinate
            elif axisDirection == 1:
                coordinate = xPos
                self.device.coordinate = coordinate

            
            self.fitParameter._auto_call = False
            self.fitParameter.xPos.value = xPos
            self.fitParameter.yPos.value = yPos
            self.fitParameter.length.value = length
            self.fitParameter.axisDirection.value = axisDirection
            self.fitParameter.coordinate.value = coordinate
            self.fitParameter._auto_call = True


            if self.viewer is None: return
           
            # update mask layer
            mask = self.device.camera.rawImage*0

            if axisDirection == 0:
                mask[yPos,xPos:xPos+length] = 1
            elif axisDirection == 1:
                mask[yPos:yPos+length,xPos] = 1

            self.maskLayer.data = mask



        @magicgui(call_button="clear")
        def clearDataButton():
            self.eD.clearData()

        # add graph
        self.graph = pg.plot()
        self.graph.setTitle(f'Intensity')
        styles = {'color':'r', 'font-size':'20px'}
        self.graph.setLabel('left', 'Value', units='1')
        self.graph.setLabel('bottom', 'coordinate', units='1')

        # fit parameter
        self.fitParameter = fitParameter
        self.clearDataButton = clearDataButton

        layout = QVBoxLayout()
        layout.addWidget(self.graph)
        layout.addWidget(self.fitParameter.native)
        layout.addWidget(self.clearDataButton.native)

        _widget = QWidget()
        _widget.setLayout(layout)

        self.vWindow.addMainGUI(_widget, name=self.DEFAULT['nameGUI'])

    def drawGraph(self):
        ''' draw all new lines in the graph'''
        (signal, coordinateTable) = self.eD.getData()
        coordinateTable = coordinateTable.T
        coordinateTable = coordinateTable.reshape(np.shape(coordinateTable)[0])
        print(coordinateTable)
        # if there is no signal then do not continue
        if signal is None:
            return

        # remove all lines
        self.graph.clear()

        offSet = np.zeros(signal.shape[1])

        #try:
            # draw lines
        for ii in np.arange(signal.shape[1]):
            mypen = QPen()
            mypen.setWidth(0)
            #lineplot = self.graph.plot(pen= mypen)
            lineplot = self.graph.plot()

            lineplot.setData(coordinateTable, signal[:,ii]-offSet[ii])
        #except:
        #    print('error occurred in drawSpectraGraph - pointSpectra')

    def setDevice(self, device):
        super().setDevice(device)

        # connect data container
        self.eD = self.device.emitterDataProfile

        # set the value in GUI according the device
        self.fitParameter.xPos.value = self.device.xPos
        self.fitParameter.yPos.value = self.device.yPos
        self.fitParameter.length.value = self.device.length
        self.fitParameter.axisDirection.value = self.device.axisDirection

        # connect signals
        self.device.worker.yielded.connect(self.guiUpdateTimed)

    def interconnectGui(self,cameraViewGUI=None):
        ''' connect with other gui'''
        if cameraViewGUI is not None:
            self.viewer = cameraViewGUI.viewer 

            colors = np.linspace(
                start=[0, 0, 1, 1],
                stop=[0, 1, 0, 1],
                num=3,
                endpoint=True
            )
            colors[0] = np.array([0.,0.,1., 0])
            transparentRedGreen_colormap = {
            'colors': colors,
            'name': 'red_and_green',
            'interpolation': 'linear'
            }
            self.maskLayer = self.viewer.add_image(np.zeros((2,2)), name='profile_mask',
            colormap=transparentRedGreen_colormap, opacity = 0.5)

            @self.maskLayer.mouse_double_click_callbacks.append
            def on_second_click_of_double_click(layer, event):
                self.fitParameter(
                xPos = int(event.position[1]),
                yPos = int(event.position[0]),
                length = self.fitParameter.length.value,
                axisDirection = self.fitParameter.axisDirection.value,
                )


    def updateGui(self):
        ''' update the data in gui '''
        self.drawGraph()

if __name__ == "__main__":
    pass

        














