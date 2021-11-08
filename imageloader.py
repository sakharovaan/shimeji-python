# с помощью итератора получать следуюее состояние
# сделать кэш картинок (не разогревать его при старте) - ресайз
# ключ eyes_eyebrows_mouth. думаю что можно без тэгов пока

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

        for e in self._config['elements']['eyes']:
            for b in self._config['elements']['eyebrows']:
                for m in self._config['elements']['mouth']:
                    self._imagebase[f"{e['name']}_{b['name']}_{m['name']}"] = self._render_ebm(e, b, m)

        for d in self._config['dialogue']['elements']:
            self._dialoguebase[d['name']] = self._render_dialogue(d)

    def _render_ebm(self, e, b, m):
        op = self._loadimage(self._config['background']['file'])

        for f in list(e['open']['file'] + b['file'] + m['file']):
            op = Image.alpha_composite(op, self._loadimage(f))

        cl = self._loadimage(self._config['background']['file'])

        for f in list(e['closed']['file'] + b['file'] + m['file']):
            cl = Image.alpha_composite(cl, self._loadimage(f))

        return {'opened': ImageTk.PhotoImage(op),
                'closed': ImageTk.PhotoImage(cl),
                'mood': list(m.get('mood', []) + b.get('mood', []) + e.get('mood', []))}

    def _render_dialogue(self, d):
        return ImageTk.PhotoImage(self._loadimage(d['file'], confsource="dialogue"))

    def _loadimage(self, path, confsource="ghost"):
        if path in self._imagecache:
            return self._imagecache[path]
        else:
            with self.RBGAImage(path) as im:
                wpercent = (self._config[confsource]['width'] / float(im.size[0]))
                hsize = int((float(im.size[1]) * float(wpercent)))
                self._imagecache[path] = im.resize((self._config[confsource]['width'], hsize), Image.BICUBIC)

            return self._imagecache[path]

    @staticmethod
    def RBGAImage(path):
        return Image.open(path).convert("RGBA")

    def getimg(self, ident, state):
        return self._imagebase[ident][state]

    def getmood(self, ident):
        return self._imagebase[ident]['mood']

    def getexprlist(self):
        return list(self._imagebase.keys())

    def getdlimg(self, pos):
        return self._dialoguebase[pos]
