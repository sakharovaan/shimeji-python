import tkinter as tk
from PIL import Image, ImageTk


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

        # self.label = tk.Label(self, text="Click on the grip to move")
        # self.grip = tk.Label(self, bitmap="gray25")
        # self.grip.pack(side="left", fill="y")
        # self.label.pack(side="right", fill="both", expand=True)

        im1 = self.RBGAImage('static/ghost/L01,R1,C1,background,hidden,normal,255.png').resize((450, 450))
        im2 = self.RBGAImage('static/ghost/L17,R1,C1,mouth_cat,hidden,normal,255.png').resize((450, 450))
        im3 = self.RBGAImage('static/ghost/L04,R1,C1,eyebrows_v,hidden,normal,255.png').resize((450, 450))

        com1 = Image.alpha_composite(im1, im2)
        eyes_closed = Image.alpha_composite(com1, im3)

        im4 = self.RBGAImage('static/ghost/L05,R1,C1,eye_under,hidden,normal,255.png').resize((450, 450))
        im5 = self.RBGAImage('static/ghost/L07,R1,C1,eye_direct,visible,normal,255.png').resize((450, 450))

        com3 = Image.alpha_composite(eyes_closed, im4)
        com4 = Image.alpha_composite(com3, im5)

        self.image_open = ImageTk.PhotoImage(com4)
        self.image_closed = ImageTk.PhotoImage(eyes_closed)
        self.grip = tk.Canvas(self, width=450, height=450,  background="brown", bd=0, highlightthickness=0, relief='ridge')

        self.grip.create_image(0, 0, image=self.image_closed, anchor='nw', tags=("image_closed",))
        self.grip.create_image(0, 0, image=self.image_open, anchor='nw', tags=("image_open",))

        self.grip.pack()

        self.menu = tk.Menu(self, tearoff=0)
        self.menu.add_command(label="Cut", command=lambda: self.menu_callback("aaa"))
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

        self.blinked = False
        self.app.after(1000, self.animate)

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

    def animate(self):
        if self.blinked:
            self.grip.tag_raise("image_open", "image_closed")
            self.blinked = False
            self.app.after(5000, self.animate)
        else:
            self.grip.tag_raise("image_closed", "image_open")
            self.blinked = True
            self.app.after(100, self.animate)

app=App()
app.mainloop()