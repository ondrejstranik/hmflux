''' class for setting and viewing slm images'''

import napari

from magicgui import magicgui

from hmflux.algorithm.imageSLM import ImageSLM
import numpy as np

class SLMViewer():
    ''' main class to define and view SLM images'''

    def __init__(self,sizeX=200,sizeY=100, **kwargs):
        ''' initialise the class '''

        # data parameter
        self.imageSLM = ImageSLM()
        self.imageSLM.setSizeSLM(sizeX,sizeY)

        self.imageType = 'constant'

        # initiate napari
        if 'show' in kwargs:
            self.viewer = napari.Viewer(show=kwargs['show'])
        else:
            self.viewer = napari.Viewer()
        self.imageLayer = self.viewer.add_image(
            self.imageSLM.image, name='setting Image', colormap='red',
            contrast_limits= (0,255))
        self.dockWidgetParameter = None


        # set gui of this class
        SLMViewer._setWidget(self)

    def generateImage(self):
        ''' generate image according the gui setting'''
        if self.imageType == 'constant':
            im = self.imageSLM.generateConstant(self.constGui.const.value)
        
        if self.imageType == 'sinus':
            im = self.imageSLM.generateConstant(self.constGui.const.value)
            im += self.imageSLM.generateSinGrating(self.sinWaveGui.axis.value,
                                                   self.sinWaveGui.stepIdx.value,
                                                   self.sinWaveGui.nStep.value,
                                                   self.sinWaveGui.period.value,
                                                   self.sinWaveGui.spectrumShift.value)

        if self.imageType == 'slanted':
            im = self.imageSLM.generateConstant(self.constGui.const.value)

            im += self.imageSLM.generateSlantedGrating(self.slantedGui.axis.value,
                                                      self.slantedGui.val0.value,
                                                      self.slantedGui.val1.value,
                                                      self.slantedGui.val2.value,
                                                      self.slantedGui.val3.value)

        if self.imageType == 'binary':
            im = self.imageSLM.generateConstant(self.constGui.const.value)

            im += self.imageSLM.generateBinaryGrating(self.binaryGui.axis.value,
                                                      self.binaryGui.rVal.value[0],
                                                      self.binaryGui.rVal.value[1])



        if self.imageType == 'box1':
            im = self.imageSLM.generateConstant(self.constGui.const.value)

            # add dark (binary) backgound
            if self.box1Gui.backgroundType.value  == 'binary':
                im += self.imageSLM.generateBinaryGrating(1-self.box1Gui.axis.value,
                                                        self.binaryGui.rVal.value[0],
                                                        self.binaryGui.rVal.value[1])
            # add bright (slanted) backgound
            if self.box1Gui.backgroundType.value == 'slanted':
                im += self.imageSLM.generateSlantedGrating(1-self.box1Gui.axis.value,
                                                        self.slantedGui.val0.value,
                                                        self.slantedGui.val1.value,
                                                        self.slantedGui.val2.value,
                                                        self.slantedGui.val3.value)

            im = self.imageSLM.generateBox1(axis=self.box1Gui.axis.value,
                                            position=self.box1Gui.position.value,
                                            val0=self.box1Gui.rVal.value[0],
                                            val1=self.box1Gui.rVal.value[1],
                                            halfwidth=self.box1Gui.halfwidth.value,
                                            bcgImage=im)
            
        if self.imageType == 'box2':
            im = self.imageSLM.generateConstant(self.constGui.const.value)
            im += self.imageSLM.generateBinaryGrating(1-self.box2Gui.axis.value,
                                                      self.binaryGui.rVal.value[0],
                                                      self.binaryGui.rVal.value[1])
            im = self.imageSLM.generateBox2(axis=self.box2Gui.axis.value,
                                            position=self.box2Gui.position.value,
                                            val0=self.box2Gui.rVal.value[0],
                                            val1=self.box2Gui.rVal.value[1],
                                            weightFactor=self.box2Gui.weightFactor.value,
                                            compensation=self.box2Gui.compensation.value,
                                            halfwidth=self.box2Gui.halfwidth.value,
                                            bcgImage=im)
            
        self.imageLayer.data = im


    def _setWidget(self):
        ''' prepare the qui '''

        @magicgui(auto_call='True',
                  imageType={
        "choices": ("constant", "sinus", "binary", "slanted", "box1", "box2"),
        "allow_multiple": False,
        })
        def choiceGui(imageType=(self.imageType)):
            self.imageType = imageType
            self.generateImage()

        @magicgui(auto_call= 'True',
                  const={"widget_type": "Slider", "max": 255})
        def constGui(const:int):
            self.generateImage()

        @magicgui(auto_call= 'True',
                  axis={'max':1},
                  stepIdx={"widget_type": "Slider", "min":-20, "max": 20},
                  period={"widget_type": "Slider", "min":2, "max": 512},
                  spectrumShift={"widget_type": "SpinBox", "min":0, "max": 256})
        def sinWaveGui(axis=0,stepIdx = 0, nStep = 10, period = 50, spectrumShift=0):
            sinWaveGui.stepIdx.min = -2*sinWaveGui.nStep.value
            sinWaveGui.stepIdx.max =  2*sinWaveGui.nStep.value
            
            self.generateImage()

        @magicgui(auto_call= 'True',
                  axis = {"max":1},
                  rVal={"widget_type": "RangeSlider", "max": 255})
        def binaryGui(axis = 0, rVal = (0,255)):
            self.generateImage()

        @magicgui(auto_call= 'True',
                axis={'max':1},
                val0={"widget_type": "Slider", "max": 255},
                val1={"widget_type": "Slider", "max": 255},
                val2={"widget_type": "Slider", "max": 255},
                val3={"widget_type": "Slider", "max": 255}
                )
        def slantedGui(axis=0,val0=0,val1=63,val2=127,val3=191):
            self.generateImage()


        @magicgui(auto_call= 'True',
                  axis = {"max":1},
                  backgroundType={
                    "choices": ("constant", "binary", "slanted"),
                    "allow_multiple": False,
                    },
                  position={"widget_type": "Slider", "max": self.imageSLM.sizeY},
                  rVal={"widget_type": "RangeSlider", "max": 255},
                  halfwidth={"widget_type": "Slider", "max": self.imageSLM.sizeY//2}
                  )
        def box1Gui(axis = 0,backgroundType= "binary",
                position= self.imageSLM.sizeY//2, rVal = (0,255), halfwidth=3):
            
            if axis ==0 and box1Gui.position.max != self.imageSLM.sizeY:
                box1Gui.position.max = self.imageSLM.sizeY
                box1Gui.halfwidth.max = self.imageSLM.sizeY//2

            if axis ==1 and box1Gui.position.max != self.imageSLM.sizeX:
                box1Gui.position.max = self.imageSLM.sizeX
                box1Gui.halfwidth.max = self.imageSLM.sizeX//2

            self.generateImage()

        @magicgui(auto_call= 'True',
                  axis = {"max":1},
                  position={"widget_type": "Slider", "max": self.imageSLM.sizeY},
                  rVal={"widget_type": "RangeSlider", "max": 255},
                  weightFactor = {"widget_type": "FloatSlider", "max": 1, "min":0},
                  compensation = {"widget_type": "Slider", "max": 255},
                  halfwidth={"widget_type": "Slider", "max": self.imageSLM.sizeY//2}
                  )
        def box2Gui(axis = 0, position = self.imageSLM.sizeY//2, rVal = (0,255), weightFactor = 0.0, compensation = 0, halfwidth = 2):
            if axis ==0 and box2Gui.position.max != self.imageSLM.sizeY:
                box2Gui.position.max = self.imageSLM.sizeY
                box2Gui.halfwidth.max = self.imageSLM.sizeY//2

            if axis ==1 and box2Gui.position.max != self.imageSLM.sizeX:
                box2Gui.position.max = self.imageSLM.sizeX
                box2Gui.halfwidth.max = self.imageSLM.sizeX//2

            self.generateImage()
            

        self.choiceGui = choiceGui
        self.sinWaveGui = sinWaveGui
        self.binaryGui = binaryGui
        self.slantedGui = slantedGui
        self.constGui = constGui
        self.box1Gui = box1Gui
        self.box2Gui = box2Gui

        # add widget 
        dw = self.viewer.window.add_dock_widget(self.choiceGui, name ='choice', area='bottom')
        if self.dockWidgetParameter is not None:
            self.viewer.window._qt_window.tabifyDockWidget(self.dockWidgetParameter,dw)
        self.dockWidgetParameter = dw
        dw = self.viewer.window.add_dock_widget(self.sinWaveGui, name ='sin', area='bottom')
        self.viewer.window._qt_window.tabifyDockWidget(self.dockWidgetParameter,dw)
        self.dockWidgetParameter = dw
        dw = self.viewer.window.add_dock_widget(self.binaryGui, name ='binary', area='bottom')
        self.viewer.window._qt_window.tabifyDockWidget(self.dockWidgetParameter,dw)
        self.dockWidgetParameter = dw
        dw = self.viewer.window.add_dock_widget(self.slantedGui, name ='slanted', area='bottom')
        self.viewer.window._qt_window.tabifyDockWidget(self.dockWidgetParameter,dw)
        self.dockWidgetParameter = dw
        dw = self.viewer.window.add_dock_widget(self.constGui, name ='const', area='bottom')
        self.viewer.window._qt_window.tabifyDockWidget(self.dockWidgetParameter,dw)
        self.dockWidgetParameter = dw
        dw = self.viewer.window.add_dock_widget(self.box1Gui, name ='box1Gui', area='bottom')
        self.viewer.window._qt_window.tabifyDockWidget(self.dockWidgetParameter,dw)
        self.dockWidgetParameter = dw
        dw = self.viewer.window.add_dock_widget(self.box2Gui, name ='box2Gui', area='bottom')
        self.viewer.window._qt_window.tabifyDockWidget(self.dockWidgetParameter,dw)
        self.dockWidgetParameter = dw


    def run(self):
        ''' start napari engine '''
        napari.run()

if __name__ == '__main__':
    pass

    
