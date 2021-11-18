# с помощью итератора получать следуюее состояние
# сделать кэш картинок (не разогревать его при старте) - ресайз
# ключ eyes_eyebrows_mouth. думаю что можно без тэгов пока
import logging

import yaml

from PIL import Image, ImageTk


class ImageLoader:
    def __init__(self, ghostconfig):
        self._ghostconfig = ghostconfig
        self._imagecache = {} #cache of raw/rescaled files
        self._imagebase = {} #cache of rendered layer files
        self._dialoguebase = {}

        with open(self._ghostconfig) as f:
            self._config = yaml.safe_load(f.read())

        for d in self._config['dialogue']['elements']:
            self._dialoguebase[d['name']] = self._render_dialogue(d)

    def _render_dialogue(self, d):
        return ImageTk.PhotoImage(self._loadimage(d['file'], confsource="dialogue"))

    def _loadimage(self, path, confsource="ghost"):
        if path in self._imagecache:
            logging.debug("got " + path + " from cache")
            return self._imagecache[path]
        else:
            with self.RBGAImage(path) as im:
                wpercent = (self._config[confsource]['width'] / float(im.size[0]))
                hsize = int((float(im.size[1]) * float(wpercent)))
                self._imagecache[path] = im.resize((self._config[confsource]['width'], hsize), Image.BICUBIC)
            logging.debug("rendered " + path )

            return self._imagecache[path]

    def _generate_image(self, **kwargs):
        op = self._loadimage(self._config['background']['file']).copy()

        for f in list(self._config['elements']['eyes'].get(kwargs['eyes'])[kwargs['state']]['file'] +
                      self._config['elements']['eyebrows'].get(kwargs['eyebrows'])['file'] +
                      self._config['elements']['mouth'].get(kwargs['mouth'])['file']):
            logging.debug("adding layer " + f)
            op = Image.alpha_composite(op, self._loadimage(f))

        return ImageTk.PhotoImage(op)

    def _getfromcache(self, **kwargs):
        k = "_".join(["{}={}".format(*x) for x in kwargs.items()])
        logging.debug("  ")
        if k not in self._imagebase:
            logging.debug("generating " + k)
            self._imagebase[k] = self._generate_image(**kwargs)
        else:
            logging.debug("got " + k + " from cache")

        return self._imagebase[k]

    def getimg(self, **kwargs):
        return self._getfromcache(**kwargs)

    @staticmethod
    def RBGAImage(path):
        return Image.open(path).convert("RGBA")

    def getdlimg(self, pos):
        return self._dialoguebase[pos]
