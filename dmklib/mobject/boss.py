from . import Mobject
from constants import MobjectType
from constants import CheckType

class Boss(Mobject):
    """
    """
    __info = {
        "hp":0,
        "invincible":False,
        "attack":0,
        "defence":0,
        "crash_damage":0,
    }
    __attack_list = [
        {
            "queue":0,
            "type":"initial",
            "duration":3,
            "hp":"inf",
            "rule":[
                {
                    "type":"movement",
                    "time":0,
                    "repeat":False,
                    "contant":[
                        {
                            "time":0,
                            "action":{
                                "function":"easy_ease",
                                "arguments":{
                                    "destination":{
                                        "x":"center",
                                        "y":"1/5*SCOPE_HEIGHT"
                                    }
                                }
                            }
                        }
                    ]
                }
            ]
        }
    ]

    attack_list = {}

    def __init__(self, *_json, **kwargs):
        pass

    