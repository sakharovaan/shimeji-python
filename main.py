import tkinter as tk
from PIL import Image
import logging
import queue

from imageloader import ImageLoader
from blink_plugin import BlinkPlugin
from expression_plugin import ExpressionPlugin
from dialogue_plugin import DialoguePlugin
from hour_dialogue_plugin import HourDialoguePlugin
from random_dialogue_plugin import RandomDialoguePlugin
from voice_plugin import VoicePlugin


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.floater = FloatingWindow(self)
        self.withdraw()


class FloatingWindow(tk.Toplevel):
    def __init__(self, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)
        self.app = args[0]
        self.overrideredirect(True)
        self.geometry("+450+450")
        self.wm_attributes("-topmost", True)
        self.wm_attributes("-transparentcolor", "brown")
        self.image = ImageLoader('ghost.yaml')

        self.grip = tk.Canvas(self, width=450+450, height=1000, background="brown", bd=0, highlightthickness=0, relief='ridge')

        self.config = dict(
            exit_initiated=False,
            voice_enabled=tk.BooleanVar()
        )
        self.config['voice_enabled'].set(True)

        self.dialogue_queue = queue.Queue()
        self.voice_queue = queue.Queue()

        self.ep = ExpressionPlugin(self, 'ghost.yaml')
        self.bp = BlinkPlugin(self, 'ghost.yaml')
        self.dp = DialoguePlugin(self, 'ghost.yaml')
        self.vp = VoicePlugin(self, 'ghost.yaml')
        self.hdp = HourDialoguePlugin(self, 'ghost.yaml')
        self.rdp = RandomDialoguePlugin(self, 'ghost.yaml')

        self.menu = tk.Menu(self, tearoff=0)
        self.menu.add_command(label="Next expression", command=self.ep.random_tick)
        self.menu.add_command(label="Show dialogue", command=self.rdp._say)

        config_menu = tk.Menu(self.menu)
        config_menu.add_checkbutton(label="Voice Enabled", onvalue=1, offvalue=0, variable=self.config['voice_enabled'])
        self.menu.add_cascade(label='Configuration', menu=config_menu)

        self.menu.add_separator()
        self.menu.add_command(label="Exit", command=lambda: self.menu_callback("exit"))

        self.grip.bind("<ButtonPress-1>", self.left_press)
        self.grip.bind("<ButtonPress-3>", self.right_press)
        self.grip.bind("<ButtonRelease-1>", self.left_release)
        self.grip.bind("<B1-Motion>", self.do_move)

    @staticmethod
    def RBGAImage(path):
        return Image.open(path).convert("RGBA")

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
            self.do_exit()
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

    def do_exit(self):
        self.config['exit_initiated'] = True
        self.app.destroy()


logging.basicConfig(level=logging.DEBUG)
app=App()
app.mainloop()
