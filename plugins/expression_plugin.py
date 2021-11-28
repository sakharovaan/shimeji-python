import random
import logging
import queue

from plugins.base_plugin import BasePlugin
from components.expression import Expression


class Plugin(BasePlugin):
    def __init__(self, window):
        super(Plugin, self).__init__(window)
        self.image_rendered = False  # image already rendered (itemconfig instead of create_image)
        self._timer_set = 0  # for more precisive timer (tkinker timer tends to tick faster than we need)
        self._timer_elapsed = 10  # a little bit bigger to init change on first use

    def on_start(self):
        self._random_expression_prod()  # FIXME cons должен быть в init, чтобы стартовая эмоция первой отображалась -- но без синхронизации там сначала белый квадрат
        self._random_expression_cons()

    def do_next_expression(self):
        self._timer_elapsed = self._timer_set*2

    def _random_expression_prod(self):
        if self.w.face_queue.empty():
            expr = Expression(self.w, 'random_emotion', 'change_random_expression')
            self.w.face_queue.put(expr)
            logging.debug('put expr ' + str(expr))

        self.after(500, self._random_expression_prod)

    def _random_expression_cons(self):
        if self._timer_set <= self._timer_elapsed:
            logging.debug("expr queue size length is " + str(self.w.face_queue.qsize()))

            try:
                expr = self.w.face_queue.get(block=False, timeout=None)
            except queue.Empty:
                self.after(250, self._random_expression_cons)
                return

            logging.debug('got ' + str(expr))

            if not self.image_rendered:
                self.w.grip.create_image(self.w.config['conffile']['ghost']['width'], 0,
                                         image=self.w.image.getimg(expr, state='close'),
                                         anchor='nw', tags=("image_closed",))
                self.w.grip.create_image(self.w.config['conffile']['ghost']['width'], 0,
                                         image=self.w.image.getimg(expr, state='open'),
                                         anchor='nw', tags=("image_open",))
                self.w.grip.pack(side="right", fill="both", expand=True)
                self.image_rendered = True
            else:
                for c in self.w.grip.find_withtag('image_closed'):
                    self.w.grip.itemconfig(c, image=self.w.image.getimg(expr, state='close'))
                for c in self.w.grip.find_withtag('image_open'):
                    self.w.grip.itemconfig(c, image=self.w.image.getimg(expr, state='open'))

            self._timer_elapsed = 0
            self._timer_set = expr.time
            logging.debug("Set timer on " + str(self._timer_set))
        else:
            # logging.debug("Set timer " + str(self._timer_set) + " elapsed " + str(self._timer_elapsed))
            self._timer_elapsed += 250

        self.after(250, self._random_expression_cons)
