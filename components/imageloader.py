# с помощью итератора получать следуюее состояние
# сделать кэш картинок (не разогревать его при старте) - ресайз
# ключ eyes_eyebrows_mouth. думаю что можно без тэгов пока
import logging
import re
from os import listdir
from os.path import isfile, join, abspath
from collections import OrderedDict

import yaml

from PIL import Image, ImageTk


class ImageLoader:
    def __init__(self, ghostconfig):
        self._ghostconfig = ghostconfig
        self._imagecache = {}  # cache of raw/rescaled files
        self._imagebase = {}  # cache of rendered layer files
        self._imagepaths = {}  # dict of file_key->file_path
        self._dialoguebase = {}

        with open(self._ghostconfig) as f:
            self._config = yaml.safe_load(f.read())

        self._image_re = re.compile(self._config['images']['search']['regex'])
        for f in listdir(self._config['images']['search']['path']):
            abs_path = abspath(join(self._config['images']['search']['path'], f))

            if isfile(abs_path):
                self._imagepaths[re.findall(self._image_re, f)[0]] = abs_path

        for d in self._config['dialogue']['elements']:
            self._dialoguebase[d['name']] = self._render_dialogue(d)

    def _render_dialogue(self, d):
        return ImageTk.PhotoImage(self._loadimage(d['file'], pathisabs=True, confsource="dialogue"))

    def _loadimage(self, path, pathisabs=False, confsource="ghost"):
        if path in self._imagecache:
            logging.debug("got cached " + path)
            return self._imagecache[path]
        else:
            with self.RBGAImage(path if pathisabs else self._imagepaths[path]) as im:
                wpercent = (self._config[confsource]['width'] / float(im.size[0]))
                hsize = int((float(im.size[1]) * float(wpercent)))
                self._imagecache[path] = im.resize((self._config[confsource]['width'], hsize), Image.BICUBIC)
            logging.debug("rendered " + path)

            return self._imagecache[path]

    def _generate_image(self, expr):
        """
        Генерируем картинку из заданного набора слоёв
        :param expr: OrderedDict
        :return: ImageTk.PhotoImage
        """
        op = self._loadimage(self._config['background']['file']).copy()

        for layer, path in expr.items():
            if layer in self._config['elements']:
                if type(path) is str:
                    for f in self._config['elements'][layer][path]['file']:
                        logging.debug("adding layer " + f)
                        op = Image.alpha_composite(op, self._loadimage(f))
                if type(path) is list:
                    fl = self._config['elements'][layer]
                    for path_elem in path:
                        fl = fl[path_elem]
                    if 'file' not in fl:
                        raise Exception('path ' + str(layer) + str(path) + ' is incorrect, should lead to file list')
                    else:
                        for f in fl['file']:
                            logging.debug("adding layer " + f)
                            op = Image.alpha_composite(op, self._loadimage(f))

        return ImageTk.PhotoImage(op)

    def _getfromcache(self, expr):
        """
        Кэшируем картинки, которые мы уже собирали из слоёв - возвращаем старую или генерируем если cache miss
        :param expr: OrderedDict
        :return: ImageTk.PhotoImage
        """
        k = "_".join(["{}={}".format(*x) for x in expr.items()])
        if k not in self._imagebase:
            logging.debug("generating " + k)
            self._imagebase[k] = self._generate_image(expr)
        else:
            logging.debug("got cached " + k)

        return self._imagebase[k]

    def getimg(self, expr, **kwargs):
        """
        Входная точка, получаем изображение из набора желаемых слоёв
        Здесь же обрабатываем специальный ключ eyes_state -- для вышележащей логики это варианты одного выражения, для нас нет

        :param expr: Expression
        :param kwargs: дополнительные параметры, например time и state
        :return: ImageTk.PhotoImage
        """
        expr = OrderedDict(expr.expr_dict)
        if 'eyes_state' in kwargs:
            expr['eyes'] = [expr['eyes'], kwargs['eyes_state']]

        return self._getfromcache(expr)

    @staticmethod
    def RBGAImage(path):
        return Image.open(path).convert("RGBA")

    def getdlimg(self, pos):
        return self._dialoguebase[pos]
