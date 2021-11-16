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
        self._random_expression_prod()
        window.app.after(10, self._random_expression_cons)

    def next_rand(self):
        self._random_expression_prod()
        self._random_expression_cons()

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

        self.w.app.after(100, self._random_expression_prod)

    def _random_expression_cons(self):
        if self.w.face_queue.qsize() > 0:
            expr = self.w.face_queue.get()
            logging.debug('got ' + str(expr))
            self.w.grip.create_image(self.w.config['conffile']['ghost']['width'], 0,
                                     image=self.w.image.getimg(expr['eyes'] + '_' + expr['eyebrows'] + '_' + expr['mouth'], 'closed'),
                                     anchor='nw', tags=("image_closed",))
            self.w.grip.create_image(self.w.config['conffile']['ghost']['width'], 0,
                                     image=self.w.image.getimg(expr['eyes'] + '_' + expr['eyebrows'] + '_' + expr['mouth'], 'opened'),
                                     anchor='nw', tags=("image_open",))
            self.w.grip.pack(side="right", fill="both", expand=True)
            self.w.app.after(expr['time'], self._random_expression_cons)
        else:
            logging.debug('expr get queue is empty')
            self.w.app.after(100, self._random_expression_cons)
