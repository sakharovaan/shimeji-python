class BasePlugin:
    def __init__(self, window):
        self.w = window
        self.ready_to_exit = True

    def tick(self):
        self.after(100, self.tick)

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
