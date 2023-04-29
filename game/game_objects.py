
from pygame.math import Vector2 as vec
import pygame
import bisect
import random

MAX_VEL = 200
class GameObject:
    def __init__(self, image, x, y, id=None):
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
        # self.mass = 1.0
        # self.inv_mass = 1.0/self.mass

    def update(self, dt):
        self.clamp_velocity()
        if self.static:
            self.velocity = vec(0, 0)

        if not self.resting:
            self.rect.x += self.velocity.x*dt
            self.rect.y += self.velocity.y*dt
            self._collided = False

    def on_collision(self, other, contact):
        if self._collided:
            return

        if not self.resting:
            # self.velocity = vec(random.randint (-5, 5) or 5, random.randint(-5, 5) or 5)
            p = vec(self.rect.center)
            o = vec(other.rect.center)
            d = o-p
            if d == vec(0, 0):
                d = vec(random.randint(-5, 5) or 5, random.randint(-5, 5) or 5)
            self.velocity = d.normalize()
            self.velocity *=  -50 #random.randint(-30, -10)
        self._collided = True

    def clamp_velocity(self):
        l = self.velocity.length()
        if l > MAX_VEL:
            self.velocity.normalize_ip()
            self.velocity *= MAX_VEL

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
        if not obj.resting and not obj._updated:
            # Remove the object from the sorted list
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

        index += 1


def populate_id_indices(objects):
    id_indices = {}
    for index, obj in enumerate(objects):
        if obj.id is not None:
            id_indices[obj.id] = index
    return id_indices


def get_obj(key, objects, id_indices):
    return objects[id_indices[key]]
