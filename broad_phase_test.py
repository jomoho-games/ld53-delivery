import bisect
import timeit
import pygame as pg
from pygame.math import Vector2 as vec
import sys
import random
from operator import attrgetter
from game import *
pg.font.init()

# Initialize Pygame
pg.init()

# Set screen dimensions
screen_width = 800
screen_height = 600
GAME_OBJECT_COUNT = 20000

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 250, 0)

# std_font = pg.font.Font(pg.font.get_default_font(),16)
std_font = pg.font.SysFont('arial', 10)
big_font = pg.font.SysFont('arial', 30)
# Create a screen
screen = pg.display.set_mode((screen_width, screen_height))
screen_rect = screen.get_rect()
cam_rect = pg.Rect(screen_rect)

image_manager = ImageManager()

# Load images and create GameObjects
objects = [GameObject("assets/spaceship_red.png", random.randint(0, screen_width*10),
                      random.randint(0, screen_height*10), image_manager) for _ in range(GAME_OBJECT_COUNT)]

objects.sort()

compare_slice_performance(objects, screen_rect)

call_timing(objects, cam_rect)

clock = pg.time.Clock()
debug_collisions = True
show_objects = True
# Main game loop
while True:

    pressed = pg.key.get_pressed()
    dt = clock.tick(60)/1000.0
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_r:
                objects = [GameObject("assets/spaceship_red.png", random.randint(0, screen_width*10),
                                      random.randint(0, screen_height*10), image_manager) for _ in range(GAME_OBJECT_COUNT)]
                objects.sort()
            if event.key == pg.K_p:
                compare_slice_performance(objects, cam_rect)
            if event.key == pg.K_t:
                call_timing(objects, cam_rect)
            if event.key == pg.K_c:
                debug_collisions = not debug_collisions
            if event.key == pg.K_h:
                show_objects = not show_objects
            if event.key == pg.K_PAGEUP:
                GAME_OBJECT_COUNT += 1000
            if event.key == pg.K_PAGEDOWN:
                GAME_OBJECT_COUNT -= 1000




        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    if pressed[pg.K_DOWN] or pressed[pg.K_s]:
        cam_rect.y += 10
    if pressed[pg.K_UP] or pressed[pg.K_w]:
        cam_rect.y -= 10
    if pressed[pg.K_LEFT] or pressed[pg.K_a]:
        cam_rect.x -= 10
    if pressed[pg.K_RIGHT] or pressed[pg.K_d]:
        cam_rect.x += 10
    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw game objects
    if show_objects:
        for_objects_in_view_rect(objects, cam_rect, lambda obj:
                                 screen.blit(obj.image, (obj.rect.x-cam_rect.x, obj.rect.y-cam_rect.y))
                                 )
    update_objects(objects, dt)

    # Perform Sweep and Prune
    potential_pairs = sweep_and_prune(
        visible_objects_slice(objects, cam_rect))

    # Check for AABB and pixel-perfect collisions
    i = 0
    coll_count = 0
    coll_count_pp = 0
    contacts = []

    for obj1, obj2 in potential_pairs:
        if debug_collisions:
            txt = f"{i},"
            obj1.tag += txt
            obj2.tag += txt

        if aabb_collision(obj1, obj2):
            coll_count += 1
            normal = calculate_collision_normal(obj1, obj2)
            contact = Contact(obj1, obj2, normal)

            obj1.on_collision(obj2, contact)
            obj2.on_collision(obj1, contact)

            if pixel_perfect_collision(obj1, obj2):
                coll_count_pp += 1
            #     if debug_collisions:
            #         pg.draw.rect(screen, WHITE, obj1.rect, width=1)
            #         pg.draw.rect(screen, WHITE, obj2.rect, width=1)
            # else:
            #     if debug_collisions:
            #         pg.draw.rect(screen, RED, obj1.rect, width=1)
            #         pg.draw.rect(screen, RED, obj2.rect, width=1)
        i += 1

    if debug_collisions:
        for obj in objects:
            txt = std_font.render(obj.tag, True, YELLOW)
            obj.tag = ""
            screen.blit(txt, (obj.rect.x-cam_rect.x, obj.rect.y-cam_rect.y))

    txt = big_font.render(
        f"obj:{len(objects)} pairs:{len(potential_pairs)} coll: {coll_count} coll_pp: {coll_count_pp}", True, GREEN)
    screen.blit(txt, (0, 0))
    txt = big_font.render(
        f"fps: {1.0/dt:.2f} dt: {dt:.4f}", True, GREEN)
    screen.blit(txt, (0, 30))

    pg.display.update()
