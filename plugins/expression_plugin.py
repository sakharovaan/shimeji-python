# нужно будет для фраз делать expression force, пусть это будет в основном классе
# если force, то этот плагин не срабатывает, потом тот плагин который поставил force должен его снять
# force будет очевидно для фраз.
# может сделать force измнения в этом же плагине по другому таймеру,
# который будет опрашивать изменения в основном словаре (когда он появится)

import random
import logging
import queue

from .base_plugin import BasePlugin


class Plugin(BasePlugin):
    def __init__(self, window):
        super(Plugin, self).__init__(window)

        self.random_change_max = self.w.config['conffile']['timings']['change_random_expression']['max']
        self.random_change_min = self.w.config['conffile']['timings']['change_random_expression']['min']

        self._image_rendered = False  # image already rendered (itemconfig instead of create_image)
        self._timer_set = 0  # for more precisive timer (tkinker timer tends to tick faster than we need)
        self._timer_elapsed = 10  # a little bit bigger to init change on first use

        self._random_expression_prod()
        self._random_expression_cons()

    def next_rand(self):
        self._timer_elapsed = self._timer_set*2

    def _random_expression_prod(self):
        eyes = ["direct", "right", "left"]
        eyebrows = ["v", "up", "straight"]
        mouth = ["cat", "sidesmile", "lightgrin", "sidestraight", "straight", "straightdown"]

        if self.w.face_queue.qsize() <= 1:
            expr = dict(eyes=random.choice(eyes),
                        eyebrows=random.choice(eyebrows),
                        mouth=random.choice(mouth),
                        time=random.randint(self.random_change_min, self.random_change_max))
            self.w.face_queue.put(expr)
            logging.debug('put expr ' + str(expr))

        self.after(500, self._random_expression_prod)

    def _random_expression_cons(self):
        if self._timer_set <= self._timer_elapsed:
            logging.debug("expr queue size length is " + str(self.w.face_queue.qsize()))
            expr = self.w.face_queue.get()
            logging.debug('got ' + str(expr))

            if not self._image_rendered:
                self.w.grip.create_image(self.w.config['conffile']['ghost']['width'], 0,
                                         image=self.w.image.getimg(eyes=expr['eyes'], eyebrows=expr['eyebrows'], mouth=expr['mouth'], state='close'),
                                         anchor='nw', tags=("image_closed",))
                self.w.grip.create_image(self.w.config['conffile']['ghost']['width'], 0,
                                         image=self.w.image.getimg(eyes=expr['eyes'], eyebrows=expr['eyebrows'], mouth=expr['mouth'], state='open'),
                                         anchor='nw', tags=("image_open",))
                self.w.grip.pack(side="right", fill="both", expand=True)
                self._image_rendered = True
            else:
                for c in self.w.grip.find_withtag('image_closed'):
                    self.w.grip.itemconfig(c, image=self.w.image.getimg(eyes=expr['eyes'], eyebrows=expr['eyebrows'], mouth=expr['mouth'], state='close'))
                for c in self.w.grip.find_withtag('image_open'):
                    self.w.grip.itemconfig(c, image=self.w.image.getimg(eyes=expr['eyes'], eyebrows=expr['eyebrows'], mouth=expr['mouth'], state='open'))

            self._timer_elapsed = 0
            self._timer_set = expr['time']
            logging.debug("Set timer on " + str(self._timer_set))
        else:
            # logging.debug("Set timer " + str(self._timer_set) + " elapsed " + str(self._timer_elapsed))
            self._timer_elapsed += 250

        self.after(250, self._random_expression_cons)
