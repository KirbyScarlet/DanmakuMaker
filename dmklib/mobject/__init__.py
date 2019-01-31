import os
import sys
import pickle

from pygame.image import load
from pygame.image import tostring
from pygame.image import frombuffer
from pygame.sprite import Sprite
from pygame.math import Vector2
from pygame.rect import Rect

from collections import deque


class HP(object):
    """
    >>> mobject.hp
    128
    >>> mobject.hp = 50
    >>> mobject.hp += 10
    >>> mobject.hp -= 20
    >>> mobject.hp
    40
    >>> mobject.hp.max
    128
    >>> mobject.hp.max = 200
    >>> mobject.hp.full()  # 200
    """

    __hp = 0
    __max_hp = 0

    def __init__(self, hp=128):
        self.__hp = hp
        self.__max_hp = hp

    @property
    def max(self):
        return self.__max_hp
    @max.setter
    def max(self, value):
        self.__max_hp = value

    def full(self):
        self.__hp = self.__max_hp

    def __add__(self, other):
        return HP(self.__hp+other)

    def __sub__(self, other):
        return HP(self.__hp-other)

    def __get__(self, instance, owner):
        return self.__hp

    def __set__(self, instance, value):
        self.__hp = value


class Damage(object):
    """
    """

    __attack_damage = 0
    __ability_power = 0
    __special_damage = None

    @property
    def attack_damage(self):
        return self.__attack_damage
    @attack_damage.setter
    def attack_damage(self, value):
        self.__attack_damage = value

    @property
    def ability_power(self):
        return self.__ability_power
    @ability_power.setter
    def ability_power(self, value):
        self.__ability_power = value

    def special(self):
        pass

    def check(self, mobject):
        if mobject.hp <= self.__attack_damage:
            mobject.hp = 0
            return
        mobject.hp -= self.__attack_damage
        if mobject.hp < self.__ability_power:
            mobject.hp = 1
            return
        mobject.hp -= self.__ability_power
        self.special()


class Mobject(Sprite):

    """
    """

    name = "Mobject"       # mobject name
    _type = None           # constants.MobjectType

    timer = 0              # timer

    image = deque()        # pictures map (or frames)
    rect = Rect(0,0,3,3)   # collision box
    collidable = True      # collidable
    position = Vector2()   # mobject position
    vector = Vector2()     # movements speed and direction

    __sources = {
        "name" : "Mobject",
        "image_path" : None,
        "image" : None,
    }
    @property
    @classmethod
    def source(cls):
        return cls.__sources
    @source.setter
    @classmethod
    def source(cls, *args, **kwargs):
        cls.__sources.update(kwargs)
        cls.name = kwargs["name"]
        cls.load(kwargs["name"], kwargs["image_path"])

    __settings = {
        "collision_box_size" : 3,   # pixel
        "collidable" : None,        # default in True
        "crash_damage" : 0,
        "image_fps_delay" : 1,      # x frame(s) change image
        "initial_position" : (-50, -50),   # must be out of the scope
        "initial_vector" : (0, 1),
        "hp" : 0,
        "max_hp" : 0, 
        "invincible" : None,
        "attack" : 0,
        "defence" : 0,
        "bonus" : 0,
        "buff" : None,
        "item" : None,
    }
    @property
    @classmethod
    def settings(cls):
        return cls.__settings
    @settings.setter
    @classmethod
    def settings(cls, *args, **kwargs):
        cls.__settings.update(kwargs)
        if cls.__settings.get("hp"):
            cls.hp = HP(cls.__settings["max_hp"])
            if cls.__settings.get("max_hp"):
                cls.hp.max = cls.__settings["max_hp"]
            else:
                cls.hp.max = cls.hp
        if cls.__settings.get("attack"):
            cls.atk = cls.__settings["attack"]
        if cls.__settings.get("defence"):
            cls.defence = cls.__settings["defence"]
        if cls.__settings.get("invincible") is not None:
            cls.invincible = cls.__settings["invincible"]
        if cls.__settings.get("collidable") is not None:
            cls.collidable = cls.__settings["collidable"]
        if cls.__settings.get("crash_damage"):
            cls.crash_damage = cls.__settings["crash_damage"]
        if cls.__settings.get("collision_box_size"):
            cls.rect = Rect(0,
                            0,
                            cls.__settings["collision_box_size"],
                            cls.__settings["collision_box_size"])
        cls.position = Vector2(cls.__settings["initial_position"])
        cls.vector = Vector2(cls.__settings["initial_vector"])
        

    @classmethod
    def load(cls, name, path=None, built=False):
        if not built:
            cls.picture_path = path
            if cls.picture_path:
                if not os.path.exists("__cache__"):
                    os.mkdir("__cache__")
                for f in sorted(os.listdir(os.path.abspath(path))):
                    if f.find(name):
                        i = load(f).convert_alpha()
                        cls.image.append(i)
        else:
            pass
        cls.image_position = cls.picture_rect.get_rect()

    @classmethod
    def build(cls):
        pass

    def move(self):
        self.position += self.motion
        self.rect.centerx, self.rect.centery = self.vector.x, self.vector.y
        self.collision_box.x, self.collision_box.y = self.vector.x, self.vector.y
        self.timer += 1

    def print(self, scope):
        scope.blit(self.image, self.rect)
        