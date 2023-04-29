import pygame as pg
from pygame.math import Vector2 as vec
import os
import asyncio
import numpy as np
import pygame_gui
import pygame_gui.elements as gui
import math
from game import *

print(pg.version)
pg.freetype.init()
pg.font.init()

pg.mixer.init()

rad2deg = 180.0/math.pi
deg2rad = math.pi/180.0

WIDTH, HEIGHT = 1280, 720
FPS = 30
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Delivery Alchemist!")
screen_rect = screen.get_rect()
cam_rect = pg.Rect(screen_rect)

ui_manager = pygame_gui.UIManager((WIDTH, HEIGHT), 'assets/theme.json')
sprites = SpritesheetManager()
sprites.load_spritesheet("ships", "assets/sheets/sheet01.json")


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 250, 0)

GAME_OBJECT_COUNT = 20000

BORDER = pg.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

# BULLET_HIT_SOUND = pg.mixer.Sound('Assets/Grenade+1.mp3')
# BULLET_FIRE_SOUND = pg.mixer.Sound('Assets/Gun+Silencer.mp3')

std_font = pg.font.Font("assets/fonts/SHPinscher-Regular.otf", 12)
big_font = pg.font.SysFont('comicsans', 40)
WINNER_FONT = pg.font.SysFont('comicsans', 100)

ship = pg.transform.scale(sprites.get_sprite("ships", 0), (20, 20))
BG = pg.transform.scale(pg.image.load(
    os.path.join('assets', 'space3.png')), (WIDTH, HEIGHT))

elementlist = [(k, f"#{k}") for k in element_colors.keys()]
ui_element_select = gui.UISelectionList(pg.Rect(10, 50, 174, 400),
                    item_list=list(elementlist),
                    manager=ui_manager,
                    object_id="elem_select",
                    allow_multi_select=False)

def draw_fps(screen,fps):
    # screen.blit(BG, (0, 0))
    # pg.draw.rect(WIN, BLACK, BORDER)

    fps_text = std_font.render(f"FPS: {fps:.2f}", True, WHITE)
    # yellow_health_text = HEALTH_FONT.render(
    #     f"Health: {yellow_health}", True, YELLOW)

    screen.blit(fps_text, (WIDTH - fps_text.get_width() - 10, 10))
    # screen.blit(yellow_health_text, (10, 10))


image_manager = ImageManager()

def populate_objects():
    objects = [GameObject(pg.transform.scale(sprites.get_sprite("ships", random.randint(2, 40)), (20, 20)), random.randint(WIDTH*-10, WIDTH*10),
                      random.randint(HEIGHT*-10, HEIGHT*10)) for _ in range(GAME_OBJECT_COUNT)]
    objects[0] = GameObject(pg.transform.scale(sprites.get_sprite("ships", 0), (30, 30)), 0,0,"player")
    objects[0].resting = False
    objects.sort()
    id_indices = populate_id_indices(objects)
    return objects, id_indices;

async def main():

    quit_please = False
    red_health = 10
    yellow_health = 10
    objects, id_indices = populate_objects()
    print("player", objects[id_indices["player"]])

    clock = pg.time.Clock()
    run = True
    debug_collisions = True
    show_objects = True

    ship_pos = vec(20, 20)

    while run:
        dt = clock.tick(FPS)/1000.0
        fps = 1.0/dt
        for event in pg.event.get():
            if event.type == pg.QUIT or quit_please:
                run = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    quit_please = True


                if event.key == pg.K_r:
                    objects = populate_objects()
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

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                # if event.ui_element == hello_button1:
                print('Hello World!', event.ui_object_id)
                print(event)

            ui_manager.process_events(event)
        ui_manager.update(dt)

        pressed = pg.key.get_pressed()

        if pressed[pg.K_DOWN] or pressed[pg.K_s]:
            cam_rect.y += 10
        if pressed[pg.K_UP] or pressed[pg.K_w]:
            cam_rect.y -= 10
        if pressed[pg.K_LEFT] or pressed[pg.K_a]:
            cam_rect.x -= 10
        if pressed[pg.K_RIGHT] or pressed[pg.K_d]:
            cam_rect.x += 10



        player:GameObject = objects[id_indices["player"]]
        p = vec(pg.mouse.get_pos()) + vec(cam_rect.topleft)
        d = (p - vec(player.rect.center))
        angle = rad2deg * math.atan2(d.x, d.y)
        l = d.length()
        if l > 20.0:
            d.normalize_ip()
        else:
            d *= dt
        if not player._collided:
            player.velocity = d*(2+(l/5))


        # Clear the screen
        screen.fill((0, 0, 0))

        # Draw game objects
        if show_objects:
            for_objects_in_view_rect(objects, cam_rect, lambda obj:
                                    screen.blit(obj.image, (obj.rect.x-cam_rect.x, obj.rect.y-cam_rect.y))
                                    )

        screen.blit(pg.transform.rotate(ship, angle), ship_pos)
        update_objects(objects, dt, id_indices)

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
                    r1 = pg.Rect(obj1.rect.x-cam_rect.x, obj1.rect.y-cam_rect.y, obj1.rect.width, obj1.rect.height)
                    r2 = pg.Rect(obj2.rect.x-cam_rect.x, obj2.rect.y-cam_rect.y, obj2.rect.width, obj2.rect.height)
                    if debug_collisions:
                        pg.draw.rect(screen, WHITE, r1, width=1)
                        pg.draw.rect(screen, WHITE, r2, width=1)
                else:
                    if debug_collisions:
                        pg.draw.rect(screen, RED, r1, width=1)
                        pg.draw.rect(screen, RED, r2, width=1)
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


        draw_fps(screen, fps)
        ui_manager.draw_ui(screen)
        pg.display.update()
        await asyncio.sleep(0)

    pg.quit()
    exit()


# if __name__ == "__main__":
asyncio.run(main())
