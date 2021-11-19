from jinja2 import Environment, FunctionLoader
import random
import logging


class BasePlugin:
    def __init__(self, window):
        self.w = window
        self.j2_env = Environment(loader=FunctionLoader(lambda t: random.choice(self.w.config['strings']['templates'].get(t, []))))
        self.ready_to_exit = True

    def tick(self):
        self.after(100, self.tick)

    def render_text(self, text_id, **kwargs):
        return self.j2_env.get_template(text_id).render(**(self.w.config['strings']['variables'] | kwargs ))

    def stoms(self, sec):
        return sec * 1000

    def mstos(self, msec):
        return msec / 1000

    def after(self, time, func, *args, **kwargs):
        # if 'cons' in str(func):
        #     logging.debug('Putting ' + str(func) + ' after ' + str(self.mstos(time)) + ' sec')
        self.w.app.after(time, func, *args, **kwargs)

    def on_exit(self):
        pass


# just a dummy for not screwing plugin loading system
class Plugin(BasePlugin):
    def __init__(self, window):
        super(Plugin, self).__init__(window)
