import random
import yaml

from .base_plugin import BasePlugin


class Plugin(BasePlugin):
    def __init__(self, window):
        super(Plugin, self).__init__(window)
        self.blinked = False

        # better preload these values to prevent excessive dict lookup each time
        self.blink_open_max = self.w.config['conffile']['timings']['blink']['open']['max']
        self.blink_open_min = self.w.config['conffile']['timings']['blink']['open']['min']
        self.blink_close_min = self.w.config['conffile']['timings']['blink']['closed']['min']
        self.blink_close_max = self.w.config['conffile']['timings']['blink']['closed']['max']

        window.app.after(10, self.tick)

    def tick(self):
        if self.blinked:
            self.w.grip.tag_raise("image_open", "image_closed")
            self.blinked = False
            self.w.app.after(random.randint(self.blink_open_min, self.blink_open_max), self.tick)
        else:
            self.w.grip.tag_raise("image_closed", "image_open")
            self.blinked = True
            self.w.app.after(random.randint(self.blink_close_min, self.blink_close_max), self.tick)
