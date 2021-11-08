import tkinter as tk
from PIL import Image
import logging

from imageloader import ImageLoader
from blink_plugin import BlinkPlugin
from expression_plugin import ExpressionPlugin


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

        self.grip = tk.Canvas(self, width=450, height=450, background="brown", bd=0, highlightthickness=0, relief='ridge')

        self.ep = ExpressionPlugin(self, 'ghost.yaml')
        self.bp = BlinkPlugin(self, 'ghost.yaml')

        self.menu = tk.Menu(self, tearoff=0)
        self.menu.add_command(label="Next expression", command=self.ep.random_tick)
        self.menu.add_command(label="Copy", command=lambda: self.menu_callback("2"))
        self.menu.add_command(label="Paste", command=lambda: self.menu_callback("3"))
        self.menu.add_command(label="Reload", command=lambda: self.menu_callback("4"))
        self.menu.add_checkbutton(label="add_checkbutton")
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
            self.app.destroy()
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
app=App()
app.mainloop()
