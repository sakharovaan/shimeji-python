import yaml
import logging
import pyttsx3
import threading
import time


class Plugin:
    def __init__(self, window, _ghostconfig):
        self.w = window

        with open(_ghostconfig) as f:
            self._config = yaml.safe_load(f.read())

        self._voice_thr = None
        window.app.after(100, self.tick)

    def tick(self):
        self._voice_thr = threading.Thread(target=self._thread)
        self._voice_thr.start()

    def _thread(self):
        self._engine = pyttsx3.init()

        for voice in self._engine.getProperty('voices'):
            logging.debug('index-> ' + voice.name + ' ' + voice.id)

        self._engine.setProperty('rate', self._config['voice']['rate'])
        self._engine.setProperty('volume', self._config['voice']['volume'] / 10)
        self._engine.setProperty('voice', self._config['voice']['voice'])

        while not self.w.config['exit_initiated']:
            if not self.w.voice_queue.empty():
                text = self.w.voice_queue.get(block=False)
                if self.w.config['voice_enabled'].get():
                    self._engine.say('<pitch middle="' + str(self._config['voice']['pitch']) + '">' + text + '</pitch>')
                    self._engine.runAndWait()
            time.sleep(0.1)
