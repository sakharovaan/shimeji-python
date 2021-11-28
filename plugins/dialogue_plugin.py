import tkinter as tk
import logging

from .base_plugin import BasePlugin


class Plugin(BasePlugin):
    def __init__(self, window):
        super(Plugin, self).__init__(window)
        self.blinked = False

        self._text_to_render = iter("")
        self._rendered_text = ""
        self._textid = None
        self._textspeed = self.w.config['conffile']['dialogue']['text']['speed']
        self._dialogue_desired_width = 40
        self._h_cursor = 0

        self._h_top = 0
        self._h_middle = 0
        self._h_bottom = 0

        self._h_bottom_id = None

        self._dialogue_is_shown = False
        self._dialogue_is_fully_rendered = True
        # чтобы достоверно проверять, что диалог отрисовался, прежде чем скрывать
        # если диалог не показывается, стоит True (то есть нам не нужно ничего больше дорисовывать)
        self._dialogue_is_shown_hide_id = False  # чтобы можно было принудительно закрывать диалог

        self.ready_to_exit = False
        self._exiting = False

    def on_start(self):
        if not self.w.plugins['expression_plugin'].image_rendered:
            self.w.app.after(100, self.on_start)
            return
        else:
            self._h_top = self.w.image.getdlimg('top').height()
            self._h_middle = self.w.image.getdlimg('middle').height()
            self._h_bottom = self.w.image.getdlimg('bottom').height()
            self.w.app.after(100, self.tick)

    def _clear(self):
        """
        После того как у нас диалог скроется, нам нужно будет привести все переменные в состоянии по умолчанию
        """
        self._text_to_render = iter("")  # итератор с текстом который нужно отрисовать
        self._rendered_text = ""  # текст который уже отрисован
        self._textid = None  # id объекта текста, чтобы каждый раз не искать
        self._dialogue_desired_width = 40  # затравка для отриовки диалога, начальная высота
        self._h_cursor = 0  # когда у нас динамический ресайз, эта переменная хранит текущее положение высоты,
        # на которой нужно отрисосвывать следующий фрагмент
        self._h_bottom_id = None  # это как флаг что у нас отрисован низ для динамического размера
        self._dialogue_is_shown = False  # чтобы отрисовывать только один диалог одновременно
        self._dialogue_is_fully_rendered = True

    def tick(self):
        """
        Основной коллбек на асинхронный цикл, проверяет, пуста ли очередь сообщений и инициирует диалог
        """
        if not self.w.dialogue_queue.empty() and not self._dialogue_is_shown and self.w.plugins['expression_plugin'].image_rendered:
            text = self.w.dialogue_queue.get(block=False)

            self._dialogue_is_fully_rendered = False
            self._dialogue_is_shown = True
            self._text_to_render = iter(str(text))
            self._render_text_init()
            self.w.voice_queue.put(text, block=False, timeout=None)

        self.after(500, self.tick)

    def _render_text_init(self):
        """
        Инциализация диалога
        """
        logging.debug('_render_text_init')
        self._textid = self.w.grip.create_text(self.w.config['conffile']['dialogue']['offset'] + self.w.config['conffile']['dialogue']['text']['offset']['xleft'],
                                               self.w.config['conffile']['dialogue']['text']['offset']['y'],
                                               text=self._rendered_text,
                                               anchor=tk.NW,
                                               tags=('dialogue_text', 'dialogue_all'),
                                               width=self.w.config['conffile']['dialogue']['width'] - self.w.config['conffile']['dialogue']['text']['offset']['xright'],
                                               fill='black', font=(self.w.config['conffile']['dialogue']['text']['font'],
                                                                   self.w.config['conffile']['dialogue']['text']['size']))
        self.after(self._textspeed, self._render_text_tick)

    def _render_text_tick(self):
        """
        Посимвольная отрисовка текста
        """
        newletter = next(self._text_to_render, None)
        if not self._h_bottom_id:
            self._render_back_top()
            self._render_back_down()

        if newletter is not None:
            self._rendered_text += newletter
            logging.debug("Rendering " + self._rendered_text)
            self.w.grip.itemconfig(self._textid, text=self._rendered_text)

            s = self.w.grip.bbox(self._textid)
            if s[1] - s[3] != self._dialogue_desired_width:
                # если у нас высота текста больше чем задник, перерисовываем его
                self._dialogue_desired_width = s[3] - s[1] + self._h_bottom
                self._render_back_down()

            self.after(self._textspeed, self._render_text_tick)
        else:  # если у нас больше нет символов для отрисовки -- мы устанавливаем таймер на его скрытие
            self._dialogue_is_fully_rendered = True
            self._dialogue_is_shown_hide_id = self.after(self.w.config['conffile']['dialogue']['wait'], self._hide_all)

        self.w.grip.tag_raise("dialogue_text", "dialogue_image")

    def _render_back_top(self):
        logging.debug('_render_back_top')
        self.w.grip.create_image(self.w.config['conffile']['dialogue']['offset'], self._h_cursor, image=self.w.image.getdlimg('top'),
                                                     anchor='nw', tags=('dialogue_top', 'dialogue_image',
                                                                        'dialogue_all'))
        self._h_cursor += self._h_top

    def _render_back_down(self):
        logging.debug('_render_back_down')
        if self._h_bottom_id:  # если у нас задник уже отрисован, мы удаляем низ, и дорисовываем средние части
            logging.debug('delete bottom image')
            self.w.grip.delete(self._h_bottom_id)
            self.w.grip.pack_forget()
        logging.debug("desired " + str(self._dialogue_desired_width) + " cursor " + str(self._h_cursor))
        while (self._h_cursor + self._h_bottom) < self._dialogue_desired_width:
            logging.debug('create middle image on' + str(self._h_cursor))
            # отрисовываем столько средних частей сколько нужно чтобы уместить текст
            self.w.grip.create_image(self.w.config['conffile']['dialogue']['offset'], self._h_cursor,
                                     image=self.w.image.getdlimg('middle'), anchor='nw',
                                     tags=('dialogue_middle', 'dialogue_image', 'dialogue_all'))
            self._h_cursor += self._h_middle

        logging.debug('create bottom image on' + str(self._h_cursor))
        # под конец отрисовываем низ
        self._h_bottom_id = self._h_bottom_id = self.w.grip.create_image(self.w.config['conffile']['dialogue']['offset'],
                                                                         self._h_cursor,
                                                                         image=self.w.image.getdlimg('bottom'),
                                                                         anchor='nw',
                                                                         tags=('dialogue_bottom', 'dialogue_image',
                                                                               'dialogue_all'))
        self.w.grip.pack(side="right", fill="both", expand=True)

    def _hide_all(self):
        for c in self.w.grip.find_withtag('dialogue_all'):
            self.w.grip.delete(c)
        self._clear()

    def do_next_dialogue(self):
        if self._dialogue_is_shown and self._dialogue_is_fully_rendered:
            try:
                self.cancel(self._dialogue_is_shown_hide_id)
            except Exception as e:
                logging.debug(e)
            self._hide_all()

    def on_stop(self):
        self.do_next_dialogue()
        if not all((self.w.dialogue_queue.empty(), self._exiting, self._dialogue_is_fully_rendered)):
            logging.debug("dialogue " + str((self.w.dialogue_queue.empty(), self._exiting, self._dialogue_is_fully_rendered)))
            self._exiting = True
            self.after(500, self.on_stop)
        else:
            self.ready_to_exit = True
