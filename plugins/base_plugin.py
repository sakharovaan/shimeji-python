from jinja2 import Environment, FunctionLoader, nodes
from jinja2.ext import Extension
from jinja2.runtime import Undefined
import random
import logging


class ExpressionTag(Extension):
    tags = {"expr"}

    def parse(self, parser):
        lineno = parser.stream.expect("name:expr").lineno
        component = parser.parse_expression()

        return nodes.CallBlock(self.call_method('_render', args=[component], dyn_args=component), [], [], []).set_lineno(lineno)

    def _render(self, component, *args, **kwargs):
        logging.debug(component._undefined_name)

        self.environment.plugin.w.face_queue.put(dict(eyes="direct", eyebrows="up", mouth="cat", time=45000),
                                                 block=False,
                                                 timeout=None)
        return ''


class BasePlugin:
    def __init__(self, window):
        self.w = window
        self._j2_loader = FunctionLoader(lambda t: random.choice(self.w.config['strings']['templates'].get(t, [])))
        self.j2_env = Environment(loader=self._j2_loader, extensions=[ExpressionTag])
        self.j2_env.plugin = self
        self.ready_to_exit = True

    def tick(self):
        self.after(100, self.tick)

    def render_text(self, text_id, *args, **kwargs):
        return self.j2_env.get_template(text_id).render(**(self.w.config['strings']['variables'] | kwargs))

    def stoms(self, sec):
        return sec * 1000

    def mstos(self, msec):
        return msec / 1000

    def after(self, time, func, *args, **kwargs):
        # if 'cons' in str(func):
        #     logging.debug('Putting ' + str(func) + ' after ' + str(self.mstos(time)) + ' sec')
        return self.w.app.after(time, func, *args, **kwargs)

    def cancel(self, *args, **kwargs):
        return self.w.app.after_cancel(*args, **kwargs)

    def on_stop(self):  # когда хотим выйти, все плагины получают этот коллбек
        pass

    def on_start(self):  # когда все плагины инициализировались (после __init__), все плагины получают этот коллбек
        pass


# just a dummy for not screwing plugin loading system
class Plugin(BasePlugin):
    def __init__(self, window):
        super(Plugin, self).__init__(window)
