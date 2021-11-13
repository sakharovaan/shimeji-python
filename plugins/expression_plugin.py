# нужно будет для фраз делать expression force, пусть это будет в основном классе
# если force, то этот плагин не срабатывает, потом тот плагин который поставил force должен его снять
# force будет очевидно для фраз.
# может сделать force измнения в этом же плагине по другому таймеру,
# который будет опрашивать изменения в основном словаре (когда он появится)

import yaml
import random
import logging


class Plugin:
    def __init__(self, window, _ghostconfig):
        self.w = window
        with open(_ghostconfig) as f:
            self._config = yaml.safe_load(f.read())

        self.random_change_max = self._config['timings']['change_random_expression']['max']
        self.random_change_min = self._config['timings']['change_random_expression']['min']
        self._random_expression_init()
        window.app.after(10, self.random_tick)
        window.app.after(10, self.forced_tick)

    def _random_expression_init(self):
        self.w.grip.create_image(self._config['ghost']['width'], 0, image=self.w.image.getimg('direct_v_cat', 'closed'), anchor='nw', tags=("image_closed",))
        self.w.grip.create_image(self._config['ghost']['width'], 0, image=self.w.image.getimg('direct_v_cat', 'opened'), anchor='nw', tags=("image_open",))
        self.w.grip.pack(side="right", fill="both", expand=True)

    def random_tick(self):
        newexpr = random.choice(self.w.image.getexprlist())
        while 'bad' in self.w.image.getmood(newexpr):
            logging.debug(newexpr + " is bad mood expression, trying again")
            newexpr = random.choice(self.w.image.getexprlist())

        for c in self.w.grip.find_withtag('image_closed'):
            self.w.grip.itemconfig(c, image=self.w.image.getimg(newexpr, 'closed'))
        for c in self.w.grip.find_withtag('image_open'):
            self.w.grip.itemconfig(c, image=self.w.image.getimg(newexpr, 'opened'))

        self.w.app.after(random.randint(self.random_change_min, self.random_change_max), self.random_tick)

    def forced_tick(self):
        pass
