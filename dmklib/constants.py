import pygame
import enum

DEFAULT_WINDOW_SIZE = 640,480
DEFAULT_SCOPE_SIZE = 400,440
DEFAULT_SCOPE_POSITION = 30,20

__author__ = "KirbyScarlet"

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
    up = pygame.K_UP
    down = pygame.K_DOWN
    left = pygame.K_LEFT
    right = pygame.K_RIGHT
    shooting = pygame.K_Z
    smooth = pygame.K_LSHIFT
    spell = pygame.K_X
    special = pygame.K_C

@enum.unique
class MobjectType(enum.Enum):
    player = 0
    boss = 1
    elf = 2
    danmaku = 3
    item = 4

@enum.unique
class CheckType(enum.Enum):
    collide = 0
    damage = 1
    buff = 2
    debuff = 3
    