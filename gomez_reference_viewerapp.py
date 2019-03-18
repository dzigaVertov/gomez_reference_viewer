from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.vector import Vector
import os
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.uix.scatter import Scatter
from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
# fsdfdfwsfds


# from kivy.core.window import Window


path = '/home/marcelo/Desktop/referencias/fievel/'


class Sprite(Image):
    def __init__(self, **kwargs):

        super(Sprite, self).__init__(**kwargs)
        # self.keep_data = True
        # print(type(self.texture))
        # bottomleft = self.texture.get_region(0, 0, 64, 64)
        # self.texture = bottomleft
        self.size = list(map(lambda x: x/2, self.texture_size))


class Referencia(Scatter):

    def __init__(self, source):
        super(Referencia, self).__init__()
        self.image = Sprite(source=source, allow_stretch=True)
        self.add_widget(self.image)
        self.size = self.image.size

    def on_touch_down(self, touch):
        x, y = touch.x, touch.y
        if self.collide_point(x, y) and len(touch.grab_list) == 0:
            super(Referencia, self).on_touch_down(touch)

            if touch.is_mouse_scrolling:  # and touch.grab_current is self:
                if touch.button == 'scrolldown':
                    self.scale = 1.1 * self.scale
                elif touch.button == 'scrollup':
                    self.scale = 0.9 * self.scale
            return False

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            self._touches = []
            touch.ungrab(self)

    # def scalar_image(self, factor):
    #     self.image.size = factor * Vector(*self.image.size)
    #     self.size = self.image.size


class Viewer(Widget):
    def __init__(self, **kwargs):

        super(Viewer, self).__init__(**kwargs)

        self.images = self.load_images()

        self.widgets = [self.add_widget(im) for im in self.images]

        self.files = FileChooserIconView()
        self._popup = Popup(
            title='hola', content=self.files, size_hint=(0.9, 0.9))
        self._popup.open()

#        self.add_widget(self.files)
 #       self.files.size = self.size

    def load_images(self):
        os.chdir(path)
        images = [Referencia(source=file) for file in os.listdir() if (
            file.endswith('png') or file.endswith('jpg'))]

        return images


class gomez_reference_viewerApp(App):
    def build(self):
        view = Viewer()
        return view


if __name__ == '__main__':
    gomez_reference_viewerApp().run()
