from .execute import Game


class Event():
    """
    """
    events = dict()
    def __init__(self, **events):
        self.events.update(**events)
        super().__init__()

    def __call__(self):
        pass

class Attribute(object):
    """
    """
    pass