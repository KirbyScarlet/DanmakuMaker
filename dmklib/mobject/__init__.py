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

import pygame.mixer
from pygame.image import load
from pygame.image import tostring
from pygame.image import frombuffer
from pygame.sprite import Sprite
from pygame.sprite import Group
from pygame.math import Vector2
from pygame.rect import Rect

from ..constants import MobjectType


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
        return self.__hp.__add__(other)

    def __sub__(self, other):
        return self.__hp.__sub__(other)

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
        if mobject.hp <= self.__ability_power:
            mobject.hp = 1
            return
        mobject.hp -= self.__ability_power
        self.special()


#Image = namedtuple("Image", "illustration animation extra")
#Animation = namedtuple("Animation", "stand turn_left turn_right")

class Mapping(object):

    """
    """

    def __init__(self):
        self.__animation = []
        self.__illustration = []

    def load_image(self, image_json, built=False):
        for pic in image_json.get("image"):
            self.__animation.append(load(pic).convert_alpha())
        for pic in image_json.get("illustration"):
            self.__illustration.append(load(pic).convert_alpha())
        self.__animate_cycle = cycle(self.__animation)  

    def animate(self):
        return next(self.__animate_cycle)


class BackgroundMusic(object):

    """
    """

    def __init__(self):
        self.backgroudmusic = {}

    def load_sound(self, _json, built=False):
        self.backgroudmusic[_json["bgm"]["name"]] = io.BytesIO(_json["bgm"]["path"])

    def set_bgm(self, name):
        pygame.mixer.music.load(self.backgroudmusic.get("name"))

    def play(self, loop):
        pygame.mixer.music.play(loop)

    def pause(self):
        pygame.mixer.music.pause()


class Source(object):
    """
    """
    pixel = []
    illustration = []
    image_fps_delay = 1
    def __init__(self, mob, _json):
        if mob._type == MobjectType.danmaku:
            self.__type_danmaku(_json)
        elif mob._type == MobjectType.boss:
            self.__type_boss(_json)

    def __type_danmaku(self, _json):
        for im in _json:
            self.pixel.append(load(im).convert_alpha())
    
    def __type_boss(self, _json):
        for im in _json["pixel"]:
            self.pixel.append(load(im).convert_alpha())
        for im in _json["illustration"]:
            self.illustration.append(load(im).convert_alpha())


class Direction(object):
    """
    """
    def __init__(self, mob):
        self.vector = mob.vector

    @property
    def radian(self):
        return self.vector.as_polar()[1]

    @radian.setter
    def radian(self, value):
        self.vector.from_polar((self.vector.length(), value))

    @property
    def degree(self):
        return self.vector.as_polar()[1]*180/pi

    @degree.setter
    def degree(self, value):
        self.vector.from_polar((self.vector.length(), value*pi/180))

    @property
    def coordinate(self):
        return [self.vector.x, self.vector.y]

    @coordinate.setter
    def coordinate(self, value):
        self.vector.x, self.vector.y = value

    def __get__(self, instance, owner):
        return self.radian

    def __set__(self, instance, value):
        self.radian = value
        return


class MobjectGroup(Group):
    """
    class MobjectGroup(pygame.sprite.Group):

    add property:

    layer -> int:
        group 0 will on the top layer.
    """
    layer = 0


class Mobject_old(Sprite):

    """

    class Mobject(pygame.sprite.Sprite):
    
    the class of all the moveble objects

    property:
        name -> str:
            mobject name
        id -> int:
            mobject id
        _type -> constants.MobjectType:
            mobject type
        timer -> int:
            mobject life time
        images -> collections.namedtuple:
            pictures or illustractions
        vector -> pygame.math.Vector2:
            direction and speed
        position -> pygame.math.Vector2:
            position
        colliable -> bool:
            specify mobject can cause damage or not
        rect -> pygame.rect.Rect:
            collision box
        radius -> int:
            collision circle if exist

        
    method:
        Sprite.add(pygame.sprite.Group): return None
            append a mobject in a new group
        Sprite.kill(): return None
            kill a mobject itself
        print(pygame.surface.Surface): return None
            display on the screen or scope
        action(self, *arg, **kwarg): return None
            specify path of mobject movements
        
        
    """

    name = "Mobject"       # mobject name
    _type = None           # constants.MobjectType

    timer = 0              # timer

    animation = {}
    __rect = Rect(0,0,3,3) # collision box
    collidable = True      # collidable
    position = Vector2()   # mobject position
    vector = Vector2()     # movements speed and direction
    
    @property
    @classmethod
    def speed(cls):
        return cls.vector.length()
    
    @speed.setter
    @classmethod
    def speed(cls, value):
        cls.vector.scale_to_length(value)

    '''
    __sources = {
        "name" : "Mobject",
        "image_path" : {
            "illustration" : None,
            "pixel":None,
            "animation" : {
                "stand" : None,
                "turn_left" : None,
                "turn_right" : None,
                },
            "extra" : {},
        },
        "image_fps_delay" : 1,      # x frame(s) change image
    }
    '''

    __settings = {
        "initial" : {
            "initial_position" : (-50, -50),   # must be out of the scope
            "initial_vector" : (0, 1),
        },
        "collide" : {
            "collidable" : True,        # default in True
            "collision_box_size" : 3,   # pixel
        },
        # "info":{
        #     "invincible" : False,
        #     "hp" : 0,
        #     "max_hp" : 0, 
        #     "attack" : 0,
        #     "defence" : 0,
        #     "crash_damage" : 0,
        # },
        "rotate" : {
            "rotatable" : False,
            "palstance" : 0,          # degree
        },
        "extra" : {
            "bonus" : None,
            "buff" : [],
            "item" : [],
        },
    }

    @property
    @classmethod
    def source(cls):
        return cls.__sources
    @source.setter
    @classmethod
    def source(cls, _json):
        cls.__sources = Source(cls, _json)

    @property
    @classmethod
    def settings(cls):
        return cls.__settings
    @settings.setter
    @classmethod
    def settings(cls, *args, **kwargs):
        cls.__settings.update(kwargs)
        cls.position = kwargs["initial"]["initial_position"]
        cls.vector = kwargs["initial"]["initial_vector"]
        if kwargs["collide"]["collidable"]:
            cls.rect = Rect(0,0,
                            kwargs["collide"]["collision_box_size"],
                            kwargs["collide"]["collision_box_size"]
                            )
        # cls.invincible = kwargs["info"]["invincible"]
        # cls.hp = HP(kwargs["info"]["max_hp"])
        # cls.hp = kwargs["info"]["hp"]
        # cls.attack = kwargs["info"]["attack"]
        # cls.defence = kwargs["info"]["defence"]
        # cls.crash_damage = kwargs["info"]["crash_damage"]
        if kwargs["rotate"]["rotatable"]:
            cls.palstance = kwargs["rotate"]["palstance"]
        cls.bonus = kwargs["extra"]["bonus"]
        cls.buff = BuffGroup(kwargs["extra"]["buff"])
        cls.item = ItemGroup(kwargs["extra"]["item"])

    @property
    @classmethod
    def rect(cls):
        return cls.__rect
    @rect.setter
    @classmethod
    def rect(cls, *value):
        l = len(value)
        if l==1:
            cls.__rect == Rect(0,0,value[0],value[0])
        elif l==2:
            cls.__rect == Rect(0,0,value[0],value[1])
        else:
            raise ValueError("please check the syntax of danmaku collide box\n")

    @classmethod
    def load(cls, name, path=None, json=None, built=False):
        pass

    @classmethod
    def build(cls):
        pass

    def __new__(cls, *args, **kwargs):
        cls.direction = Direction(cls)
        return super().__new__(*args, **kwargs)

    def motion(self):
        return Vector2(0,0)

    def collision_map_update(self, c_map):
        for i in range(c_map):
            pass

    def move(self):
        self.position += self.motion()
        self.rect.centerx, self.rect.centery = self.vector.x, self.vector.y
        self.timer += 1

    def print(self, scope):
        scope.blit(self.image, self.rect)
        

class Mobject(Sprite):
    
    """
    """
    
    __type = None

    def __init__(self, _json={}):
        pass

    @classmethod
    def load_image(cls, _json, built=False):
        cls.image = Mapping()
        cls.image.load_image(_json["picture"])

    @classmethod
    def load_sound(cls, _json, built=False):
        cls.sound

    @staticmethod
    def build_source(_json={}):
        images = {"image":[], "illustration":[]}
        sounds = {"bgm":[], "effects":[]}
        for img in _json["image"]:
            temp_img = load(img).convert_alpha()
            temp_rect = temp_img.get_rect()
            images["image"].append((tostring(temp_img, "RGBA"), temp_rect.size))
        for illu in _json["illustration"]:
            temp_illu = load(illu).convert_alpha()
            temp_rect = temp_illu.get_rect()
            images["illustration"].append((tostring(temp_illu, "RGBA"), temp_rect.size))
        for bgm in _json["bgm"]:
            with open(bgm["path"], 'rb') as temp_bgm:
                sounds["bgm"].append((bgm.get("name"), temp_bgm.read()))
        for efx in _json["sound_effects"]:
            with open(bgm["path"], 'rb') as temp_efx:
                sounds["effects"].append((efx.get("name"), temp_bgm.read()))
        

