import yaml
import tkinter as tk
import random


class DialoguePlugin:
    def __init__(self, window, _ghostconfig):
        self.w = window
        self.blinked = False

        with open(_ghostconfig) as f:
            self._config = yaml.safe_load(f.read())

        self.grip = None

    def _render_back(self):
        h_cursor = 0
        h_top = self.w.image.getdlimg('top').height()
        h_middle = self.w.image.getdlimg('middle').height()
        h_bottom = self.w.image.getdlimg('bottom').height()
        desiredwidth = 600

        self.w.grip.create_image(self._config['dialogue']['offset'], h_cursor, image=self.w.image.getdlimg('top'), anchor='nw', tags=('dialogue',))
        h_cursor += h_top

        while h_cursor + h_bottom < desiredwidth:
            self.w.grip.create_image(self._config['dialogue']['offset'], h_cursor, image=self.w.image.getdlimg('middle'), anchor='nw', tags=('dialogue',))
            h_cursor += h_middle

        self.w.grip.create_image(self._config['dialogue']['offset'], h_cursor, image=self.w.image.getdlimg('bottom'), anchor='nw', tags=('dialogue',))
        self.w.grip.pack(side="right", fill="both", expand=True)

    def _hide_back(self):
        for c in self.w.grip.find_withtag('dialogue'):
            self.w.grip.delete(c)
