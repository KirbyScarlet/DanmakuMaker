from . import Mobject
from . import MobjectGroup
from ..constants import CheckType
from math import inf

from ..functions import Parament
from ..constants import MobjectType

__modules = {
    "line":[
        {
            "type":"",
            "time":[0,inf],

        }
    ]
}

class Danmaku(Mobject):
    """
    """
    _type = MobjectType.danmaku
    def __init__(self, _json={}):
        self._json = _json
        self.source = self._json["source"]

def emitter(continuity="disposable"):
    """
    """
    def disposable(_json, **kwargs):
        group = MobjectGroup()
        for _ in _json["amount"]:
            group.add(Danmaku())  #¿?

class Emitter(object):
    """
    """
    def __init__(self, _json):
        self._json = _json
        self.parament = Parament(_json["parament"])
        self.danmaku_initialized = self.dmkinit()

    def dmkinit(self):
        l = {}
        for d in self._json["danmaku_initialized"]:
            l[d["name"]] = Danmaku(d)

    @staticmethod
    def disposable(): pass