import yaml
from datetime import datetime, timedelta
import logging


class Plugin:
    def __init__(self, window, _ghostconfig):
        self.w = window
        self.blinked = False

        with open(_ghostconfig) as f:
            self._config = yaml.safe_load(f.read())

        self._elapsed_seconds = 0
        self._hourdict = {
            0: 'полночь',
            1: 'час ночи',
            2: 'два часа ночи',
            3: 'три часа ночи',
            4: 'четыре часа утра',
            5: 'пять часов утра',
            6: 'шесть часов утра',
            7: 'семь часов утра',
            8: 'восемь часов утра',
            9: 'девять часов утра',
            10: 'десять часов утра',
            11: 'одиннадцать часов утра',
            12: 'полдень',
            13: 'час дня',
            14: 'два часа дня',
            15: 'три часа дня',
            16: 'четыре часа дня',
            17: 'пять часов вечера',
            18: 'шесть часов вечера',
            19: 'семь часов вечера',
            20: 'восемь часов вечера',
            21: 'девять часов вечера',
            22: 'десять часов вечера',
            23: 'одиннадцать часов вечера',
        }

        window.app.after(3000, self.tick)

    def tick(self):
        now = datetime.now()
        if now.minute == 0 and self._elapsed_seconds > 60:
            logging.debug("hour dialogue activated! " + str(now.hour))
            self._elapsed_seconds = 0
            self.w.dialogue_queue.put("Сейчас " + self._hourdict[now.hour], block=False, timeout=None)
        else:
            self._elapsed_seconds += 3
        self.w.app.after(3000, self.tick)
        logging.debug("hour dialogue " + str(self._elapsed_seconds))
