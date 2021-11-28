import logging
import pyttsx3
import threading
import time

from plugins.base_plugin import BasePlugin


class Plugin(BasePlugin):
    def __init__(self, window):
        super(Plugin, self).__init__(window)

        self._voice_thr = None

        self._exiting = False
        self._final_phrase_said = False  # костыль чтобы при выходе всегда получать последнюю фразу из очереди
        self.ready_to_exit = False

    def on_start(self):
        self.w.app.after(100, self.tick)

    def tick(self):
        self._voice_thr = threading.Thread(target=self._thread)
        self._voice_thr.start()

    def _thread(self):
        self._engine = pyttsx3.init()

        for voice in self._engine.getProperty('voices'):
            logging.debug('voices-> ' + voice.name + ' ' + voice.id)

        self._engine.setProperty('rate', self.w.config['conffile']['voice']['rate'])
        self._engine.setProperty('volume', self.w.config['conffile']['voice']['volume'] / 10)
        self._engine.setProperty('voice', self.w.config['conffile']['voice']['voice'])

        while not self._exiting or not self._final_phrase_said:
            if not self.w.voice_queue.empty():
                text = self.w.voice_queue.get(block=False)
                logging.debug('voice queue get ' + text)
                if self.w.config['voice_enabled'].get():
                    self._engine.say('<pitch middle="' + str(self.w.config['conffile']['voice']['pitch']) + '">' + text + '</pitch>')
                    self._engine.runAndWait()

                    if not self._final_phrase_said and self._exiting:
                        self._final_phrase_said = True

            time.sleep(0.1)
        else:
            logging.debug('voice exit ' + str((self._exiting, self.w.voice_queue.empty(), self._final_phrase_said)))
            self.ready_to_exit = True

    def on_stop(self):
        self._exiting = True
