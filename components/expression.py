from collections import OrderedDict
import random


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
