import yaml
import logging
from datetime import datetime
import random


class RandomDialoguePlugin:
    def __init__(self, window, _ghostconfig):
        self.w = window
        self.blinked = False

        with open(_ghostconfig) as f:
            self._config = yaml.safe_load(f.read())

        self._elapsed_seconds = 0
        self._random_min = self._config['timings']['random_phrase']['min']
        self._random_max = self._config['timings']['random_phrase']['max']
        self._next_random = random.randint(self._random_min, self._random_max)

        self._phrases = [
            "Привет! Ты пока не добавил ни одной толковой фразы, но я верю в тебя!"
        ]

       #window.app.after(3000, self.tick)

    def tick(self):
        now = datetime.now()
        if self._elapsed_seconds > self._next_random:
            logging.debug("random dialogue activated!")
            self._elapsed_seconds = 0
            self._say()
            self.w.app.after(3000, self.tick)
        else:
            self._elapsed_seconds += 3
            self.w.app.after(3000, self.tick)
        logging.debug("random dialogue " + str(self._elapsed_seconds))

    def _say(self):
        self.w.dialogue_queue.put(random.choice(self._phrases), block=False, timeout=None)
