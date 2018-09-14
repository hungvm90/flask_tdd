from .price import PriceAdjustSource


class Simple(object):
    def __init__(self):
        self.x = PriceAdjustSource("aaaa")
        print(self.x)

    def f(self):
        print(self.x.get_today_adjust())