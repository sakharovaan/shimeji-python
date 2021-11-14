import yaml
import tkinter as tk
import logging


class Plugin:
    def __init__(self, window, _ghostconfig):
        self.w = window
        self.blinked = False

        with open(_ghostconfig) as f:
            self._config = yaml.safe_load(f.read())

        self._text_to_render = iter("")
        self._rendered_text = ""
        self._textid = None
        self._textspeed = self._config['dialogue']['text']['speed']
        self._dialogue_desired_width = 40
        self._h_cursor = 0
        self._h_top = self.w.image.getdlimg('top').height()
        self._h_middle = self.w.image.getdlimg('middle').height()
        self._h_bottom = self.w.image.getdlimg('bottom').height()
        self._h_bottom_id = None

        self._dialogue_is_shown = False

        window.app.after(100, self.tick)

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

    def tick(self):
        """
        Основной коллбек на асинхронный цикл, проверяет, пуста ли очередь сообщений и инициирует диалог
        """
        if not self.w.dialogue_queue.empty() and not self._dialogue_is_shown:
            text = self.w.dialogue_queue.get(block=False)

            self._dialogue_is_shown = True
            self._text_to_render = iter(str(text))
            self._render_text_init()
            self.w.voice_queue.put(text, block=False, timeout=None)

        self.w.app.after(100, self.tick)

    def _render_text_init(self):
        """
        Инциализация диалога
        """
        logging.debug('_render_text_init')
        self._textid = self.w.grip.create_text(self._config['dialogue']['offset'] + self._config['dialogue']['text']['offset']['xleft'],
                                               self._config['dialogue']['text']['offset']['y'],
                                               text=self._rendered_text,
                                               anchor=tk.NW,
                                               tags=('dialogue_text', 'dialogue_all'),
                                               width=self._config['dialogue']['width'] - self._config['dialogue']['text']['offset']['xright'],
                                               fill='black', font=(self._config['dialogue']['text']['font'],
                                                                   self._config['dialogue']['text']['size']))
        self.w.app.after(self._textspeed, self._render_text_tick)

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

            self.w.app.after(self._textspeed, self._render_text_tick)
        else:  # если у нас больше нет символов для отрисовки -- мы устанавливаем таймер на его скрытие
            self.w.app.after(self._config['dialogue']['wait'], self._hide_all)

        self.w.grip.tag_raise("dialogue_text", "dialogue_image")

    def _render_back_top(self):
        logging.debug('_render_back_top')
        self.w.grip.create_image(self._config['dialogue']['offset'], self._h_cursor, image=self.w.image.getdlimg('top'),
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
            self.w.grip.create_image(self._config['dialogue']['offset'], self._h_cursor,
                                     image=self.w.image.getdlimg('middle'), anchor='nw',
                                     tags=('dialogue_middle', 'dialogue_image', 'dialogue_all'))
            self._h_cursor += self._h_middle

        logging.debug('create bottom image on' + str(self._h_cursor))
        # под конец отрисовываем низ
        self._h_bottom_id = self._h_bottom_id = self.w.grip.create_image(self._config['dialogue']['offset'],
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