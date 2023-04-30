
from pygame.math import Vector2 as vec
import pygame
import pygame as pg
import bisect
import random
from .alchemy import *
from .colors import *

MAX_VEL = 300

NUM_ELEMENTS = len(alchemy_game_data['elements'])


def init_obj(t, x, y, sprites):
    if t == "ship":
        s = random.randint(25, 50)
        obj = GameObject(pygame.transform.scale(sprites.get_sprite(
            "ships", random.randint(2, 40)),  (s, s)), x, y, t=t)
        obj.static = False
        obj.resting = False
        obj.velocity = vec(random.randint(-5, 5) or 5,
                           random.randint(-5, 5) or 5)
        obj.velocity.normalize_ip()
        obj.velocity *= random.randint(5, 50)
        obj.damage = random.randint(5, 15)


    if t == "clump":
        i = random.randint(0, 120)
        s = random.randint(15, 30)
        obj = GameObject(pygame.transform.scale(
            sprites.get_sprite("clumps", i), (s, s)), x, y, t=t)
        obj.static = True
        obj.resting = True
        obj.angle = random.randint(0, 360)
        obj.element = random.randint(0, NUM_ELEMENTS)

    if t == "element":
        i = random.randint(0, 120)
        s = random.randint(15, 30)
        obj = GameObject(pygame.transform.scale(
            sprites.get_sprite("clumps", i), (s, s)), x, y, t=t)
        obj.static = False
        obj.resting = False
        obj.angle = random.randint(0, 360)
        obj.element = random.randint(0, NUM_ELEMENTS)

    if t == "city" or t == "alchemizer":
        city_sprites = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
                        16, 17, 18, 19, 20, 21, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]
        i = city_sprites[random.randint(0, len(city_sprites)-1)]
        if t == "alchemizer":
            i = 22
        obj = GameObject(pygame.transform.scale_by(
            sprites.get_sprite("points", i), 4), x, y, t=t)
        obj.static = True
        obj.resting = True
        obj.sprite_id = i
        obj.rect.x -= obj.rect.width/2
        obj.rect.y -= obj.rect.height/2

    return obj


def init_city(city, sprites, location, city_id):
    obj = init_obj("city", city['pos'].x, city['pos'].y, sprites)
    obj.name = location['name']
    obj.quests = location['quests']
    obj.city_id = city_id

    return obj


def init_alchemizer(city, sprites, location):
    obj = init_obj("alchemizer", city['pos'].x, city['pos'].y, sprites)
    obj.name = "Alchemizer"

    return obj


class GameObject(pygame.sprite.Sprite):
    def __init__(self, image, x, y, t='', id=None):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.t = t
        self.id = id
        self.tag = ""
        self.image = image
        self.mask = pygame.mask.from_surface(image, threshold=16)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.resting = True
        self.velocity = vec(0, 0)
        if random.random() > 0.9:
            self.velocity = vec(random.randint(-5, 5) or 5,
                                random.randint(-5, 5) or 5)
            self.velocity.normalize_ip()
            self.resting = False
        self.static = self.resting

        self._collided = False
        self._updated = False
        self._destroy = False
        self.health = 100
        self.max_health = 100
        self.speed = 0
        self.angle= 0
        self.damage= 0
        self.city_timeout= 0

        # self.mass = 1.0
        # self.inv_mass = 1.0/self.mass

    def get_health_percentage(self):
        return self.health/self.max_health

    def update(self, dt):
        if(self.id == 'player') :
          self.city_timeout =max(0, self.city_timeout-dt)
        self.clamp_velocity()
        if self.static:
            self.velocity = vec(0, 0)

        if not self.resting:
            self.rect.x += self.velocity.x*dt
            self.rect.y += self.velocity.y*dt
            self._collided = False

    def on_collision(self, other, contact=None):
        if self._collided:
            return

        self.health -= other.damage
        if self.health <= 0:
          self._destroy = True

        if(self.id == 'player') and not contact.obj_man.in_transition() :
          if self.city_timeout<=0:
            self.city_timeout = 5
            if other.t == "alchemizer":
              pg.event.post(pg.event.Event(FADEOUT,  time=0.5))
              pg.time.set_timer(pg.event.Event(CHANGE_GAME_MODE, mode= 'alchemizer'), int(500), 1)
            if other.t == "city":
              pg.event.post(pg.event.Event(FADEOUT,  time=1))
              pg.time.set_timer(pg.event.Event(CHANGE_GAME_MODE, mode= 'city', city=other.city_id), int(1000), 1)

        if not self.resting:
            # self.velocity = vec(random.randint (-5, 5) or 5, random.randint(-5, 5) or 5)
            l, r = abs(self.rect.right-other.rect.left), abs(self.rect.left-other.rect.right)
            t, b = abs(self.rect.bottom-other.rect.top), abs(self.rect.top-other.rect.bottom)
            # if self.id=='player':
            #   print(l,r,t,b)
            if min(l,r) < min(t,b):
              if l > r:
                self.rect.x +=r
              else:
                self.rect.x -=l
            else:
              if t > b:
                self.rect.y +=b
              else:
                self.rect.y -=t
            p = vec(self.rect.center)
            o = vec(other.rect.center)
            d = o-p
            if d == vec(0, 0):
                d = vec(random.randint(-5, 5) or 5, random.randint(-5, 5) or 5)
            self.velocity = d.normalize()
            self.velocity *= -50  # random.randint(-30, -10)
            self.speed = self.velocity.length()
        self._collided = True

    def clamp_velocity(self):
        max_vel = MAX_VEL
        if self.id == "player":
            max_vel *= 3
        l = self.velocity.length()
        if l > max_vel:
            self.velocity.normalize_ip()
            self.velocity *= max_vel

    def ready(self):
        self._updated = False

    def __lt__(self, other):
        return self.rect.x < other.rect.x

    def __str__(self):
        return f"GameObject({self.id}, x={self.rect.x}, y={self.rect.y}, w={self.rect.width}, {self.resting}, v={self.velocity} )"


def update_objects(objects, dt, id_indices):
    index = 0
    [obj.ready() for obj in objects]
    while index < len(objects):
        obj = objects[index]
        if obj._destroy:
          # Remove the object and update the id_indices dictionary
            objects.pop(index)
            if obj.id in id_indices:
                del id_indices[obj.id]
                for other_id, other_index in id_indices.items():
                    if other_index > index:
                        id_indices[other_id] = other_index - 1
            continue

        if (not obj.resting and not obj._updated):
            # Remove the object from the sorted list
            old_index = index
            objects.pop(index)

            # Update the object's position
            obj.update(dt)
            obj._updated = True

            # Find the position where the object should be inserted
            new_index = bisect.bisect_right(objects, obj)

            # Insert the object at the new position
            objects.insert(new_index, obj)

            # Update id_indices dictionary if the object has an id
            if obj.id is not None:
                id_indices[obj.id] = new_index
                # print("new index", obj.id, new_index)

             # Update the indices of objects with IDs
            for other_id, other_index in id_indices.items():
                if other_id != obj.id:
                    if new_index <= other_index < old_index:
                        id_indices[other_id] = other_index + 1
                    elif old_index < other_index <= new_index:
                        id_indices[other_id] = other_index - 1

        index += 1


def populate_id_indices(objects):
    id_indices = {}
    for index, obj in enumerate(objects):
        if obj.id is not None:
            id_indices[obj.id] = index
    return id_indices


def get_obj(key, objects, id_indices):
    return objects[id_indices[key]]
