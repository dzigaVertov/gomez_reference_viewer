from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.vector import Vector
from kivy.graphics import Rectangle
from kivy.graphics import Color
import os
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.uix.scatter import Scatter
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stencilview import StencilView
from kivy.properties import ObjectProperty
from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')


class Sprite(Image):
    def __init__(self, **kwargs):

        super(Sprite, self).__init__(**kwargs)

        # para el crop
        # self.keep_data = True
        # print(type(self.texture))
        # bottomleft = self.texture.get_region(0, 0, 64, 64)
        # self.texture = bottomleft
        self.size = list(map(lambda x: x/2, self.texture_size))


class Archs(Popup):
    def __init__(self, view_widget):
        super(Archs, self).__init__()
        self.view_widget = view_widget

    def aceptar_pressed(self, button):
        if self.ids.chooser.selection:
            for im in self.ids.chooser.selection:
                self.view_widget.add_image_wid(im)

        self.dismiss()

    def add_reference(self, chooser, selected, event):
        self.view_widget.add_image_wid(chooser.selection.pop())
        

class Root_widget(BoxLayout):

    view = ObjectProperty(None)

    def agregar(self):
        self.popi = Archs(self.ids.view)
        self.popi.open()
        print('probando')

    def set_mover(self, button):
        self.view.tool = "mover"

    def set_cropear(self, button):
        self.view.tool = "cropear"

        
        



class Referencia(Scatter):
    def __init__(self, source, viewer):
        super(Referencia, self).__init__()
        self.image = Sprite(source=source, allow_stretch=True)
        self.add_widget(self.image)
        self.size = self.image.size
        self.center = viewer.center
        self.auto_bring_to_front = True

    def on_touch_down(self, touch):
        x, y = touch.x, touch.y
        if self.collide_point(x, y) and len(touch.grab_list) == 0:
            if self.parent.tool == 'cropear':
                self.parent.select_me(self)
            super(Referencia, self).on_touch_down(touch)

            if touch.is_mouse_scrolling:
                if touch.button == 'scrolldown':
                    self.scale = 1.1 * self.scale
                elif touch.button == 'scrollup':
                    self.scale = 0.9 * self.scale
            return False

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            self._touches = []
            touch.ungrab(self)


class Viewer(StencilView):
    def __init__(self, **kwargs):

        super(Viewer, self).__init__(**kwargs)
        self.rect = None
        self.tool = "mover"
        
    def select_me(self, child):
        with self.canvas:
            Color(0, 0.5, 0, 0.5)
            Rectangle(pos=(0, 0), size=(500, 500))
        with self.canvas.after:
            child.index=0

    def on_touch_up(self, touch):
        if self.rect:
            self.canvas.remove(self.rect)
        super(Viewer, self).on_touch_up(touch)

    def add_image_wid(self, imfile):
        self.add_widget(Referencia(source=imfile, viewer=self))

    # def on_touch_down(self, touch):
    #     if self.tool == "Mover":
    #         print('mover')
    #         return super(Viewer, self).on_touch_down(touch)
    #     else:
    #         print("cropear")



class gomez_reference_viewerApp(App):
    def build(self):
        self.view = Root_widget()
        self.drops = []
        Window.bind(on_dropfile=self.open_dropped)
        return self.view

    def open_dropped(self, win, file):
        self.view.ids.view.add_image_wid(file.decode("utf-8"))

        

if __name__ == '__main__':
    gomez_reference_viewerApp().run()
