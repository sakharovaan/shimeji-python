import queue
import importlib
import pkgutil
import yaml
from functools import partial
import random
import logging

from jinja2 import Environment, FunctionLoader, nodes
from jinja2.ext import Extension

import tkinter as tk
from PIL import Image

from components.imageloader import ImageLoader
from components.expression import Expression


class ExpressionTag(Extension):
    tags = {"expr"}

    def parse(self, parser):
        # если мы пишем {% expr 'fefefe' %}, то component будет nodes.Const и передаваться в _render как string
        # если {% expr fefefe %}, то это будет Name, который потом будет резолвиться и передаваться в _render будет объект с именем fefefe
        lineno = parser.stream.expect("name:expr").lineno
        args = [nodes.Const(parser.parse_expression().name)]

        return nodes.Output([nodes.MarkSafeIfAutoescape(self.call_method('_render', args))]).set_lineno(lineno)

    def _render(self, component, *args, **kwargs):
        self.environment.plugin.face_queue.put(Expression(self.environment.plugin, component, 45000),
                                                 block=False, timeout=None)  # FIXME брать время из 2 опц аргумента тэга
        self.environment.plugin.dispatch_signal('do_next_expression')

        logging.debug('Forcing expression: ' + component + ' for ' + str(45000))
        return ''


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.floater = FloatingWindow(self)
        self.withdraw()


class ShimejiCore:
    """
    Класс, объединяющий в себе логику работы приложения и служебные функции
    """
    def __init__(self, *args, **kwargs):
        self.app = args[0]
        self.image = ImageLoader('ghost.yaml')

        self.config = dict(
            voice_enabled=tk.BooleanVar(),
            conffile={},
            strings={}
        )
        with open('ghost.yaml', encoding='utf8') as f:
            self.config['conffile'] = yaml.safe_load(f.read())
        with open('strings.yaml', encoding='utf8') as f:
            self.config['strings'] = yaml.safe_load(f.read())

        self.config['voice_enabled'].set(True)

        self.dialogue_queue = queue.Queue()
        self.voice_queue = queue.Queue()
        self.face_queue = queue.LifoQueue()
        self.plugins = {}

        self._j2_loader = FunctionLoader(lambda t: random.choice(self.config['strings']['templates'].get(t, [])))
        self.j2_env = Environment(loader=self._j2_loader, extensions=[ExpressionTag])
        self.j2_env.plugin = self

        self._plugins_modules = {
            name: importlib.import_module('plugins.' + name, package='.')
            for finder, name, ispkg
            in pkgutil.iter_modules(path=['plugins'])
        }

        self.plugins = {
            name: plugin.Plugin(self) for name, plugin in self._plugins_modules.items()
        }

    def start_core(self):
        self.dispatch_signal('on_start')

    def dispatch_signal(self, signal_name, *args, **kwargs):
        for plugin in self.plugins.values():
            getattr(plugin, signal_name)(*args, **kwargs)

    def run_dialogue(self, text_key, *args, **kwargs):
        text = self.render_text(text_key, *args, **kwargs)

        self.dialogue_queue.put(text, block=False, timeout=None)
        self.voice_queue.put(text, block=False, timeout=None)
        self.dispatch_signal('do_next_dialogue')

    def render_text(self, text_id, *args, **kwargs):
        return self.j2_env.get_template(text_id).render(**(self.config['strings']['variables'] | kwargs))

    @staticmethod
    def RBGAImage(path):
        return Image.open(path).convert("RGBA")


class FloatingWindow(tk.Toplevel, ShimejiCore):
    """
    В этот класс лучше всего помещать только вещи, связанные с tk (ввод-вывод/графика/меню...)
    """
    def __init__(self, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)
        ShimejiCore.__init__(self, *args, **kwargs)

        self.overrideredirect(True)
        self.geometry("+450+450")
        self.wm_attributes("-topmost", True)
        self.wm_attributes("-transparentcolor", "brown")

        self.grip = tk.Canvas(self, width=450+450, height=1000, background="brown", bd=0, highlightthickness=0, relief='ridge')

        self.menu = tk.Menu(self, tearoff=0)
        self.menu.add_command(label="Next expression", command=partial(self.dispatch_signal, 'do_next_expression'))
        self.menu.add_command(label="Show dialogue", command=partial(self.dispatch_signal, 'do_random_dialogue'))

        config_menu = tk.Menu(self.menu)
        config_menu.add_checkbutton(label="Voice Enabled", onvalue=1, offvalue=0, variable=self.config['voice_enabled'])
        self.menu.add_cascade(label='Configuration', menu=config_menu)

        self.menu.add_separator()
        self.menu.add_command(label="Exit", command=lambda: self.menu_callback("exit"))

        self.grip.bind("<ButtonPress-1>", self.left_press)
        self.grip.bind("<ButtonPress-3>", self.right_press)
        self.grip.bind("<ButtonRelease-1>", self.left_release)
        self.grip.bind("<B1-Motion>", self.do_move)

        self.start_core()

    def left_press(self, event):
        self.x = event.x
        self.y = event.y

    def right_press(self, event):
        try:
            self.menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.menu.grab_release()

    def menu_callback(self, element):
        if element == "exit":
            self.plugins['start_stop_plugin'].do_stop()
        else:
            raise

    def left_release(self, event):
        self.x = None
        self.y = None

    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.winfo_x() + deltax
        y = self.winfo_y() + deltay
        self.geometry(f"+{x}+{y}")


logging.basicConfig(level=logging.DEBUG)
logging.getLogger('comtypes').setLevel(level=logging.INFO)
logging.getLogger('PIL').setLevel(level=logging.INFO)
app=App()
app.mainloop()
