from kivy.config import Config
Config.set('graphics', 'shaped', 1)

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.resources import resource_find
from kivy.properties import StringProperty
from KivyOnTop import register_topmost

TITLE = 'Shimeji'


class ShimejiGame(BoxLayout):
    def __init__(self, **kwargs):
        super(ShimejiGame, self).__init__()
        # Photo can be reference by running the photo function once:
        Clock.schedule_interval(self.update, 0.06)

    def update(self, dt):
        # Replace the given image source value:
        self.ids.catraView.source = resource_find('static/catra.png')


class ShimejiApp(App):
    def on_start(self):
        Clock.schedule_once(self.set_shape)

    def set_shape(self, *args):
        Window.shape_image = resource_find('static/catra.png')
        Window.shape_mode = 'binalpha'


    def build(self):
        Window.set_title(TITLE)
        Window.size = 410, 410
        Window.borderless = '1'
        register_topmost(Window, TITLE)

        return ShimejiGame()


if __name__ == '__main__':
    ShimejiApp().run()
