import builtins
import math

class Parament(object):
    """
    """
    def __init__(self, _json):
        self.json = _json
        self.math = math

    def generator(self, name, arguments):
        default = {
            "range":builtins.range,
        }
        if name in default.keys():
            return default[name](**arguments)
        else:
            raise NameError("generator not found.\n")

    def constant(self, arguments):
        return arguments["value"]

    def reference(self, value):
        return value

    def constants(self, value):
        return value

    def set_parament(self):
        for k,v in self.json.items():
            self.__setattr__(k, self.__getattribute__(v["type"])(**v["property"]))
            
