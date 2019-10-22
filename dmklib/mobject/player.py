from . import Mobject
from ..constants import MobjectType
from ..constants import DefaultKey
from pygame.key import get_pressed

class Player(Mobject):
    """
    """

    __sources = {
        
    }
    def __init__(self, follower=None):
        self._type = MobjectType.player
        
        super().__init__()

    

class Follower(Mobject):
    """
    """

    def __init__(self):
        self._type = MobjectType.player
        super().__init__()

