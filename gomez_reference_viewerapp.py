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


path = '/home/marcelo/Desktop/referencias/fievel/'



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
    def __init__(self, viejo):
        super(Archs, self).__init__()
        self.viejo = viejo

    def eve(self, args):
        
        print(args[0].selection)
        print(self.viejo.ids.vwr)
        self.viejo.ids.vwr.add_image_wid(args[0].selection[0])


class Root_widget(BoxLayout):

    vwr = ObjectProperty(None)

    def agregar(self):
        self.popi = Archs(self)
        self.popi.open()
        print('probando')


class Referencia(Scatter):
    def __init__(self, source):
        super(Referencia, self).__init__()
        self.image = Sprite(source=source, allow_stretch=True)
        self.add_widget(self.image)
        self.size = self.image.size
        self.auto_bring_to_front = True

    def on_touch_down(self, touch):
        x, y = touch.x, touch.y
        if self.collide_point(x, y) and len(touch.grab_list) == 0:
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
        self.images = self.load_images()

        with self.canvas.after:
            self.refs = [self.add_widget(im) for im in self.images]

    

    def load_images(self):
        os.chdir(path)
        images = [Referencia(source=file) for file in os.listdir() if (
            file.endswith('png') or file.endswith('jpg'))]

        return images

    def add_image_wid(self, imfile):
        self.add_widget(Referencia(source=imfile))


class gomez_reference_viewerApp(App):
    def build(self):
        view = Root_widget()
        return view


if __name__ == '__main__':
    gomez_reference_viewerApp().run()
