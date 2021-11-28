from datetime import datetime
import logging

from .base_plugin import BasePlugin


class Plugin(BasePlugin):
    def __init__(self, window):
        super(Plugin, self).__init__(window)
        self.blinked = False

        self._elapsed_seconds = 0

    def on_start(self):
        self.w.app.after(3000, self.tick)

    def tick(self):
        now = datetime.now()
        if now.minute == 0 and self._elapsed_seconds > 60:  # set to 'if True' for debugging
            logging.debug("hour dialogue activated! " + str(now.hour))
            self._elapsed_seconds = 0
            self.w.dialogue_queue.put(self.render_text('houly_dialogue', hour=now.hour), block=False, timeout=None)
        else:
            self._elapsed_seconds += 3
        self.after(3000, self.tick)
        # logging.debug("hour dialogue " + str(self._elapsed_seconds))
