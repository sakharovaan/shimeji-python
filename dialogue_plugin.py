import yaml
import tkinter as tk
import random
import logging

class DialoguePlugin:
    def __init__(self, window, _ghostconfig):
        self.w = window
        self.blinked = False

        with open(_ghostconfig) as f:
            self._config = yaml.safe_load(f.read())

        self.grip = None
        self._text_to_render = iter("Привет, я Катра! Спасибо, что теперь я могу говорить!")
        self._rendered_text = ""
        self._textid = None
        self._textspeed = self._config['dialogue']['text']['speed']

    def _render_text_init(self):
        self._textid = self.w.grip.create_text(self._config['dialogue']['offset'] + self._config['dialogue']['text']['offset']['xleft'],
                                               self._config['dialogue']['text']['offset']['y'],
                                               text=self._rendered_text,
                                               anchor=tk.NW,
                                               width=self._config['dialogue']['width'] - self._config['dialogue']['text']['offset']['xright'],
                                               fill='black', font=(self._config['dialogue']['text']['font'],
                                                                   self._config['dialogue']['text']['size']))
        self.w.app.after(self._textspeed, self._render_text_tick)

    def _render_text_tick(self):
        newletter = next(self._text_to_render, None)
        if newletter is not None:
            self._rendered_text += newletter
            logging.debug("Rendering " + self._rendered_text)
            self.w.grip.itemconfig(self._textid, text=self._rendered_text)
            self.w.app.after(self._textspeed, self._render_text_tick)

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
