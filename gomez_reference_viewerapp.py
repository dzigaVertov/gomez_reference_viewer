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
from kivy.uix.behaviors import DragBehavior
from time import sleep


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

        
class Crop(DragBehavior, Popup):
    
    def __init__(self, image_texture):
        """
        Opens a crop editor to crop the image
        
        """
        self.image_texture = image_texture  # Sprite
        self.title = 'Cropear ' + image_texture.source
        self.touched = False
        
        
        super(Crop, self).__init__()
        
        

    def remap_coordinates(self, x, y, width, height):
        texture_width, texture_height = self.image_texture.texture.size
        widget_width, widget_height = self.ids.sprite_to_crop.size
        texture_width_here = widget_width
        texture_height_here = widget_height
        widget_ratio = widget_width/widget_height
        image_ratio = self.image_texture.image_ratio
        

        if widget_ratio > image_ratio:
            # there is leftover space to the sides
            print('first branch')
            texture_width_here = widget_height * image_ratio
            x_left_image = int((widget_width - texture_width_here)/2)
            x = x- x_left_image
            # width = width - x_left_image
        elif widget_ratio < image_ratio:
            # there is leftover space up und down
            print('second_branch')
            texture_height_here = widget_width/image_ratio
            y_down_image = int((widget_height - texture_height_here)/2)
            y = y- y_down_image
            # height = height - y_down_image
        

        new_x = int(x * texture_width/texture_width_here)
        new_y = int(y * texture_height/texture_height_here)

        new_width = int(width * texture_width/texture_width_here)
        new_height = int(height * texture_height/texture_height_here)

        # print('old_coordinates: ', (x, y, width, height))
        # print('new coordinates: ', (new_x, new_y, new_width, new_height))

        return (new_x, new_y, new_width, new_height)

        

        

        

        

    def dismiss(self):
        super(Crop, self).dismiss()
        
        
    def crop_image(self, x=0, y=0, width=100, height=150):
        self.image_texture.reload()
        
        tex = self.image_texture.texture

        tex_region = tex.get_region(*self.remap_coordinates(x, y, width, height))
        

        self.image_texture.texture = tex_region
        self.canvas.clear()
        
        
        self.dismiss()


    def on_touch_down(self, touch):
        self.x_rect = touch.x
        self.y_rect = touch.y
        self.touched = True

    def on_touch_move(self, touch):
        if self.touched:
            try:
                self.x_fin = touch.x
                self.y_fin = touch.y
                width = self.x_fin - self.x_rect
                height = self.y_fin - self.y_rect
                with self.canvas.after:
                    self.canvas.after.clear()
                    
                    Color(1., 0, 0, 0.5)
                    Rectangle(pos=(self.x_rect, self.y_rect), size=(width, height))
            except AttributeError as e:
                pass
        
    def on_touch_up(self, touch):

        if self.touched:        
            try:
                self.x_fin = touch.x
                self.y_fin = touch.y
                xs = sorted([self.x_rect, touch.x])
                ys = sorted([self.y_rect, touch.y])
            
                # print('x,y: ', self.x_rect, self.y_rect)
                # print('xfin, yfin: ', self.x_fin, self.y_fin)
                width = xs[1] - xs[0]
                height = ys[1] - ys[0]
                if width < 10 or height < 10:
                    return
                # print('width: ', width)
                # print('height: ', height)
                # print(self.size)
                # print(self.width/self.height)
                # print(type(self.image_texture))
                # print('size image_texture', self.image_texture.size)
                # print('size_norm', self.image_texture.norm_image_size)
                # print('aspect_ratio', self.image_texture.image_ratio)
        
                self.crop_image(xs[0], ys[0], width, height)
                self.touched = False
            except AttributeError as e:
                print('bad luck', e)
        


        

        

class Root_widget(BoxLayout):

    view = ObjectProperty(None)

    def agregar(self):
        """Abre el Popup para elegir archivos"""
        self.popi = Archs(self.ids.view)
        self.popi.open()
        print('probando')

    def set_mover(self, button=None):
        self.view.tool = "mover"
        print('mover')

    def set_cropear(self, button):
        self.view.tool = "cropear"
        print('croper')

        
        



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
                self.parent.crop_me(self)
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
        
    def crop_me(self, child):

        self.crop_popup = Crop(child.image)
        self.crop_popup.open()
        self.tool = "mover"
        
        # with self.canvas:
        #     Color(0, 0.5, 0, 0.5)
        #     Rectangle(pos=(0, 0), size=(500, 500))
        # with self.canvas.after:
        #     child.index=0

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
        self.title = "GRV"
        Window.bind(on_dropfile=self.open_dropped)
        return self.view

    def open_dropped(self, win, file):
        """Manages drag & drop for files"""
        self.view.ids.view.add_image_wid(file.decode("utf-8"))

        

if __name__ == '__main__':
    gomez_reference_viewerApp().run()
