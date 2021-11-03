from kivy.config import Config
Config.set('graphics', 'shaped', 1)
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

import pyautogui
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import DragBehavior
from kivy.uix.button import Button
from kivy.uix.popup import ModalView
from kivy.metrics import sp
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.resources import resource_find
from kivy.properties import StringProperty
from KivyOnTop import register_topmost

TITLE = 'Shimeji'


class PopMenu(object):

    def __init__(self, touch):
        myContent = BoxLayout(orientation='vertical')
        button = Button(text='button1')
        myContent.add_widget(button)
        button = Button(text='button2')
        myContent.add_widget(button)
        button = Button(text='button3')
        myContent.add_widget(button)
        self.popup = ModalView(size_hint=(None, None), height=myContent.height, pos_hint={'x' : touch.spos[0], 'top' : touch.spos[1]})
        self.popup.add_widget(myContent)

    def open(self, *args):
        self.popup.open()


class ShimejiGame(DragBehavior, BoxLayout):
    def __init__(self, **kwargs):
        super(ShimejiGame, self).__init__()
        # Photo can be reference by running the photo function once:
        Clock.schedule_interval(self.update, 0.06)

    def update(self, dt):
        # Replace the given image source value:
        self.ids.catraView.source = resource_find('../static/catra.png')

    def on_touch_down(self, touch):
        if touch.button == 'right':
            self.popup = PopMenu(touch)
            self.popup.open()

    def on_touch_move(self, touch):
        pos = pyautogui.position()
        Window.left = pos.x - touch.ox
        Window.top = pos.y - touch.oy
        return True


class ShimejiApp(App):
    def on_start(self):
        Clock.schedule_once(self.set_shape)

    def set_shape(self, *args):
        Window.shape_image = resource_find('../static/catra.png')
        Window.shape_mode = 'binalpha'


    def build(self):
        Window.set_title(TITLE)
        Window.size = 410, 410
        Window.left = 500
        Window.top = 500
        Window.borderless = '1'
        register_topmost(Window, TITLE)

        return ShimejiGame()


if __name__ == '__main__':
    ShimejiApp().run()
