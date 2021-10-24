import os
import sys
import pickle
import io

import numpy

from collections import deque
from collections import namedtuple
from itertools import count
from itertools import cycle
from math import pi

import pygame
import pygame.mixer
from pygame.image import load
from pygame.image import tostring
from pygame.image import frombuffer
from pygame.sprite import Sprite
from pygame.sprite import Group
from pygame.math import Vector2
from pygame.rect import Rect
from pygame.color import Color

from .constants import TextType


class Widget(Sprite):
    """
    """
    _type = None

    def __init__(self, *args, **kwargs):
        self.timer = 0
        super().__init__(*args, **kwargs)
        

class TextFromImage(Widget):
    
    _type = "text"
    
    def __init__(self, *args, **kwargs):
        self.images = kwargs.get("image")
        self.character_table = {}

        super().__init__(*args, **kwargs)

    def load_character_table(self):
        pass

    def load_character(self, image, area=None):
        return 


class TextFromFont(Widget):

    _type = "text"
    
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)


class Text(Widget):
    """
    """
    _type = "text"
    def __init__(self, *args, **kwargs):
        if t:=kwargs.get("text"):
            self.text = t
        else:
            self.text = "No text input."
        self.text_type = 

    def load_from_font(self, font_file=None, size=15):
        self.font = pygame.font.Font(font_file, size)

    def load_from_image(self, image, **character_table):
        self.character_image = image
        self.character = {chara:self.character_image.subsurface(rect) for chara,rect in character_table.items()}

