from jinja2 import Environment, FunctionLoader
import random


class BasePlugin:
    def __init__(self, window):
        self.w = window
        self.j2_env = Environment(loader=FunctionLoader(lambda t: random.choice(self.w.config['strings']['templates'].get(t, []))))

    def tick(self):
        self.w.app.after(100, self.tick)

    def render_text(self, text_id, **kwargs):
        return self.j2_env.get_template(text_id).render(**(self.w.config['strings']['variables'] | kwargs ))


# just a dummy for not screwing plugin loading system
class Plugin(BasePlugin):
    def __init__(self, window):
        pass
