__doc__ = """
motions
"""

import math

class Action():
    """
    """
    __action = {}

    @staticmethod
    def change_speed(start_timer, speed):
        def _temp_change_speed(self):
            if self.timer==start_timer:
                self.vector.scale_to_length(speed)
                return 
        return _temp_change_speed

    @staticmethod
    def change_direction(start_timer, direction):
        def _temp_change_direction(self):
            if self.timer==start_timer:
                self.vector.update(direction)
                return
        return _temp_change_direction

    @staticmethod
    def linear_speed(start_timer, stop_timer, speed1, speed2):
        d = (speed2-speed1)/(stop_timer-start_timer)
        def _temp_linear_speed(self):
            self.direct.scale_to_length
        return _temp_linear_speed

    @staticmethod
    def init(_json={}):
        def action_init(self, _json):
            self.vector.scale_to_length(_json["speed"])


    def __call__(self, timer, speed):
        pass

    