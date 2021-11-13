import yaml
import logging
import pyttsx3
import threading
import time


class VoicePlugin:
    def __init__(self, window, _ghostconfig):
        self.w = window

        with open(_ghostconfig) as f:
            self._config = yaml.safe_load(f.read())

        self._voice_thr = None
        window.app.after(100, self.tick)

    @staticmethod
    def onStart(name):
        print('starting ' + name)

    @staticmethod
    def onWord(name, location, length):
        print('word ' + name + location + length)

    @staticmethod
    def onEnd(name, completed):
        print('finishing ' + name + completed)

    def tick(self):
        self._voice_thr = threading.Thread(target=self._thread)
        self._voice_thr.start()

    def _thread(self):
        self._engine = pyttsx3.init()

        self._engine.setProperty('rate', 150)
        self._engine.setProperty('volume', 0.5)
        self._engine.setProperty('voice',
                                 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\Vocalizer Expressive milena premium-high 22kHz')

        while True:
            if not self.w.voice_queue.empty():
                text = self.w.voice_queue.get(block=False)
                self._engine.say('<pitch middle="5">' + text + '</pitch>')
                self._engine.runAndWait()
            time.sleep(0.1)
