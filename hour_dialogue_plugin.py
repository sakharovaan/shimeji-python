import yaml
from datetime import datetime, timedelta
import logging
import humanize


class HourDialoguePlugin:
    def __init__(self, window, _ghostconfig):
        self.w = window
        self.blinked = False

        with open(_ghostconfig) as f:
            self._config = yaml.safe_load(f.read())

        self._elapsed_seconds = 0
        self._t = humanize.i18n.activate("ru_RU")

        window.app.after(3000, self.tick)

    def tick(self):
        now = datetime.now()
        if now.minute == 0 and self._elapsed_seconds > 60:
            logging.debug("hour dialogue activated! " + str(now.hour))
            self._elapsed_seconds = 0
            self.w.dialogue_queue.put("Сейчас " + humanize.naturaldelta(timedelta(hours=now.hour)), block=False, timeout=None)
            self.w.app.after(3000, self.tick)
        else:
            self._elapsed_seconds += 3
            self.w.app.after(3000, self.tick)
        logging.debug("hour dialogue " + str(self._elapsed_seconds))
