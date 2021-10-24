import pygame
import enum

__author__ = "KirbyScarlet"

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
    up = pygame.K_UP
    down = pygame.K_DOWN
    left = pygame.K_LEFT
    right = pygame.K_RIGHT
    shooting = pygame.K_z
    smooth = pygame.K_LSHIFT
    spell = pygame.K_x
    special = pygame.K_c
    
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

@enum.unique
class TextType(enum.Enum):
    text = 0
    image = 1
    
class Scope():
    left = 0
    top = 0
    right = 400  # default
    bottom = 440  # default