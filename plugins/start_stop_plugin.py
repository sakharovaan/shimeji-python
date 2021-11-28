import logging

from .base_plugin import BasePlugin


class Plugin(BasePlugin):
    def __init__(self, window):
        super(Plugin, self).__init__(window)
        self._exiting = False

    def on_start(self):
        self.w.dialogue_queue.put(self.render_text('on_start_phrazes'), block=False, timeout=None)

    def do_stop(self):
        if not self._exiting:
            self.w.dialogue_queue.put(self.render_text('on_stop_phrazes'), block=False, timeout=None)
            self._exiting = True
            self.w.dispatch_signal('on_stop')

    def on_stop(self):
        if all(pl.ready_to_exit for pl in self.w.plugins.values()):
            self.w.app.destroy()
        else:
            logging.debug('Ready to exit: ' + str([name + ': ' + str(pl.ready_to_exit) for name, pl in self.w.plugins.items()]))
            self.after(250, self.on_stop)
