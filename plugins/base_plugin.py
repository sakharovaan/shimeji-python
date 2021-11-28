import random
import logging
from collections import OrderedDict

from jinja2 import Environment, FunctionLoader, nodes
from jinja2.ext import Extension


class Expression:
    def __init__(self, w, expr_name, time):
        """
        :param w: w (FloatingWindow)
        :param expr_name: строка с описанием эмоции (expressions в конфиге)
        :param time: число (мсек) или строка (timings в конфиге)
        """
        self.w = w
        self.cur_expr = self.w.config['conffile']['expressions'][expr_name]

        self.expr_dict = OrderedDict()
        for k, v in self.cur_expr.items():
            self.expr_dict[k] = random.choice(v)

        if type(time) is int:
            self.expr_dict['time'] = time
        elif type(time) is str:
            self.expr_dict['time'] = random.randint(self.w.config['conffile']['timings'][time]['min'],
                                                    self.w.config['conffile']['timings'][time]['max'])
        else:
            raise Exception

    def as_dict(self):
        return self.expr_dict

    def __str__(self):
        return str(self.expr_dict)

    def __getattr__(self, item):
        return self.expr_dict[item]


class ExpressionTag(Extension):
    tags = {"expr"}

    def parse(self, parser):
        # если мы пишем {% expr 'fefefe' %}, то component будет nodes.Const и передаваться в _render как string
        # если {% expr fefefe %}, то это будет Name, который потом будет резолвиться и передаваться в _render будет объект с именем fefefe
        lineno = parser.stream.expect("name:expr").lineno
        args = [nodes.Const(parser.parse_expression().name)]

        return nodes.Output([nodes.MarkSafeIfAutoescape(self.call_method('_render', args))]).set_lineno(lineno)

    def _render(self, component, *args, **kwargs):
        self.environment.plugin.w.face_queue.put(Expression(self.environment.plugin.w, component, 45000),
                                                 block=False, timeout=None)  # FIXME брать время из 2 опц аргумента тэга
        self.environment.plugin.w.dispatch_signal('do_next_expression')

        logging.debug('Forcing expression: ' + component + ' for ' + str(45000))
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

    def __getattr__(self, item):  # для многочисленных сигналов плагинов, чтобы не прописывать их тут
        return lambda: None


# just a dummy for not screwing plugin loading system
class Plugin(BasePlugin):
    def __init__(self, window):
        super(Plugin, self).__init__(window)
