import random
import yaml


class Plugin:
    def __init__(self, window, _ghostconfig):
        self.w = window
        self.blinked = False

        with open(_ghostconfig) as f:
            self._config = yaml.safe_load(f.read())

        # better preload these values to prevent excessive dict lookup each time
        self.blink_open_max = self._config['timings']['blink']['open']['max']
        self.blink_open_min = self._config['timings']['blink']['open']['min']
        self.blink_close_min = self._config['timings']['blink']['closed']['min']
        self.blink_close_max = self._config['timings']['blink']['closed']['max']

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
