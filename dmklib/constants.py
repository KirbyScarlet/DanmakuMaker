import pygame.locals
import enum

DEFAULT_WINDOW_SIZE = 640,480
DEFAULT_SCOPE_SIZE = 400,440
DEFAULT_SCOPE_POSITION = 30,20

@enum.unique
class GameState(enum.Enum):
    loading = 1
    menu = 2
    playing = 3
    pause = 4
    gameover = 5
    cg = 6
    
@enum.unique
class DefaultKey(enum.Enum):
    pass

@enum.unique
class MobjectType(enum.Enum):
    player = 0
    boss = 1
    elf = 2
    danmaku = 3
    item = 4
    