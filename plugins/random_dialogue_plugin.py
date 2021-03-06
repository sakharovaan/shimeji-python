import yaml
import logging
from datetime import datetime
import random

from plugins.base_plugin import BasePlugin


class Plugin(BasePlugin):
    def __init__(self, window):
        super(Plugin, self).__init__(window)
        self.blinked = False

        self._elapsed_seconds = 0
        self._random_min = self.w.config['conffile']['timings']['random_phrase']['min']
        self._random_max = self.w.config['conffile']['timings']['random_phrase']['max']
        self._next_random = random.randint(self._random_min, self._random_max)

       #window.app.after(3000, self.tick)

    def tick(self):
        now = datetime.now()
        if self._elapsed_seconds > self._next_random:
            logging.debug("random dialogue activated!")
            self._elapsed_seconds = 0
            self.do_random_dialogue()
            self.after(3000, self.tick)
        else:
            self._elapsed_seconds += 3
            self.after(3000, self.tick)
        logging.debug("random dialogue " + str(self._elapsed_seconds))

    def do_random_dialogue(self):
        self.w.run_dialogue('random_phrazes')
