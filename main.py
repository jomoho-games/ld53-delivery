import pygame as pg
from pygame.math import Vector2 as vec
import os
import asyncio
import numpy as np
import pygame_gui
import math

print(pg.version)
pg.freetype.init()
pg.font.init()

pg.mixer.init()

rad2deg = 180.0/math.pi
deg2rad = math.pi/180.0

WIDTH, HEIGHT = 900, 500
FPS = 30
window = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("First Game!")

ui_manager = pygame_gui.UIManager((WIDTH, HEIGHT), 'assets/theme.json')


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pg.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

# BULLET_HIT_SOUND = pg.mixer.Sound('Assets/Grenade+1.mp3')
# BULLET_FIRE_SOUND = pg.mixer.Sound('Assets/Gun+Silencer.mp3')

std_font = pg.font.Font("assets/fonts/SHPinscher-Regular.otf", 12)
HEALTH_FONT = pg.font.SysFont('comicsans', 40)
WINNER_FONT = pg.font.SysFont('comicsans', 100)

ship = pg.transform.scale(pg.image.load(
    os.path.join('assets', 'spaceship_red.png')), (20, 20))
BG = pg.transform.scale(pg.image.load(
    os.path.join('assets', 'space.png')), (WIDTH, HEIGHT))


def draw_window(fps):
    window.blit(BG, (0, 0))
    # pg.draw.rect(WIN, BLACK, BORDER)

    fps_text = std_font.render(f"FPS: {fps:.2f}", True, WHITE)
    # yellow_health_text = HEALTH_FONT.render(
    #     f"Health: {yellow_health}", True, YELLOW)

    window.blit(fps_text, (WIDTH - fps_text.get_width() - 10, 10))
    # window.blit(yellow_health_text, (10, 10))


async def main():
    quit_please = False
    red_health = 10
    yellow_health = 10

    hello_button = pygame_gui.elements.UIButton(relative_rect=pg.Rect((0, 0), (100, 50)),
                                                text='Say Hello',
                                                object_id="1",
                                                anchors={'center': 'center'})
    hello_button1 = pygame_gui.elements.UIButton(relative_rect=pg.Rect((0, 100), (100, 50)),
                                                 text='Say Hello',
                                                 object_id="2",
                                                 anchors={'center': 'center'})
    # ui_manager.set_visual_debug_mode(True)

    clock = pg.time.Clock()
    run = True

    ship_pos = vec(20, 20)

    while run:
        time_delta = clock.tick(FPS)/1000.0
        fps = 1.0/time_delta
        for event in pg.event.get():
            if event.type == pg.QUIT or quit_please:
                run = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    quit_please = True
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                # if event.ui_element == hello_button1:
                print('Hello World!', event.ui_object_id)
                print(event)

            ui_manager.process_events(event)
        ui_manager.update(time_delta)

        keys_pressed = pg.key.get_pressed()
        # yellow_handle_movement(keys_pressed, yellow)
        # red_handle_movement(keys_pressed, red)

        # handle_bullets(yellow_bullets, red_bullets, yellow, red)

        p = vec(pg.mouse.get_pos())
        d = (p - ship_pos)
        angle = rad2deg * math.atan2(d.x, d.y)
        l = d.length()
        if l > 20.0:
            d.normalize_ip()
        else:
            d *= time_delta
        ship_pos += d*time_delta*(200+(l/5))

        # print(x)
        draw_window(fps)
        window.blit(pg.transform.rotate(ship, angle), ship_pos)

        ui_manager.draw_ui(window)
        pg.display.update()
        await asyncio.sleep(0)

    pg.quit()
    exit()


# if __name__ == "__main__":
asyncio.run(main())
