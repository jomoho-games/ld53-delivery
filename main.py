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

WIDTH, HEIGHT = 1280, 720
FPS = 30
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Delivery Alchemist!")
screen_rect = screen.get_rect()
cam_rect = pg.Rect(screen_rect)

ui_manager = pygame_gui.UIManager((WIDTH, HEIGHT), 'assets/theme.json')
sprites = SpritesheetManager()
sprites.load_spritesheet("ships", "assets/sheets/sheet01.json")
sprites.load_spritesheet("points", "assets/sheets/sheet_nice.json")
sprites.load_spritesheet("clumps", "assets/sheets/sheet_clumps.json")


GAME_OBJECT_COUNT = 20000
LEVEL = 'level_1'

BORDER = pg.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

# BULLET_HIT_SOUND = pg.mixer.Sound('Assets/Grenade+1.mp3')
# BULLET_FIRE_SOUND = pg.mixer.Sound('Assets/Gun+Silencer.mp3')

std_font = pg.font.Font("assets/fonts/SHPinscher-Regular.otf", 16)
big_font = pg.font.Font('assets/fonts/norwester.otf', 40)

BG = pg.transform.scale(pg.image.load(
    os.path.join('assets', 'space3.png')), (WIDTH, HEIGHT))

inventory = {
    "fire": 100,
    "water": 100,
    "earth": 100,
    "air": 100,
}


class InventoryWin:
    def __init__(self, inventory, ui_manager, WIDTH, HEIGHT):
        w = WIDTH-100
        h = HEIGHT-100
        self.win = gui.UIWindow(pg.Rect(50, 50, w, h),
                                draggable=False,
                                object_id="#inv_window",
                                window_display_title="Inventory")

        elementlist = [(f'{k}: {n}', f"#{k}")
                       for k, n in inventory.items() if n > 0]
        self.ui_element_select = gui.UISelectionList(pg.Rect(10, 50, 200, h-150),
                                                     manager=ui_manager,
                                                     container=self.win,
                                                     item_list=list(
                                                         elementlist),
                                                     object_id="elem_select",
                                                     allow_multi_select=False)
        self.input_items = {
            "fire": 0,
            "water": 0,
            "earth": 0,
            "air": 0,
        }
        input_list = [(f'{k}: {n}', f"#{k}")
                      for k, n in self.input_items.items() if n > 0]

        self.ui_input_select = gui.UISelectionList(pg.Rect(220, 50, 200, h-150),
                                                   manager=ui_manager,
                                                   container=self.win,
                                                   item_list=list(input_list),
                                                   object_id="input_select",
                                                   allow_multi_select=False)

        self.status_text = gui.UILabel(pg.Rect(w/2-200, h-220, 600, 50),
                                                manager=ui_manager,
                                                container=self.win,
                                                text="Run the alchemizer using input elements",
                                                )
        self.craft_btn = gui.ui_button.UIButton(pg.Rect(w/2+50, h-120, 200, 50),
                                                manager=ui_manager,
                                                container=self.win,
                                                text="Run Alchemizer",
                                                object_id="#craft_beer",
                                                )
        self.close_btn = gui.ui_button.UIButton(pg.Rect(w-200, h-120, 120, 50),
                                                manager=ui_manager,
                                                container=self.win,
                                                object_id="#close_button",
                                                text="Close",
                                                )
        self.spr = sprites.get_sprite("points", 22)
        self.img = gui.UIImage(pg.Rect(w/2, 50, self.spr.get_width()*2, self.spr.get_height()*2),
                               self.spr,
                               manager=ui_manager,
                               container=self.win,
                               )

    def update_input(self):
        input_list = [(f'{k}: {n}', f"#{k}")
                      for k, n in self.input_items.items() if n > 0]
        self.ui_input_select.set_item_list(input_list)

    def update_inventory(self, inventory):
        elementlist = [(f'{k}: {n}', f"#{k}")
                       for k, n in inventory.items() if n > 0]
        self.ui_element_select.set_item_list(elementlist)


START_GAME_MODE = "inventory"
image_manager = ImageManager()


def populate_objects():
    print("POP")
    objects = [init_obj("ship", random.randint(WIDTH*-10, WIDTH*10), random.randint(
        HEIGHT*-10, HEIGHT*10), sprites) for _ in range(int(GAME_OBJECT_COUNT/6))]
    objects.extend([init_obj("clump", random.randint(WIDTH*-10, WIDTH*10), random.randint(
        HEIGHT*-10, HEIGHT*10), sprites) for _ in range(int(GAME_OBJECT_COUNT/3))])

    locations = alchemy_quests[LEVEL]["locations"]
    cities = generate_random_locations(len(locations), pg.Rect(
        WIDTH*-10, HEIGHT*-10, WIDTH*20, HEIGHT*20), WIDTH*2, WIDTH*5)
    city_objs = [init_city(city, sprites, locations[i])
                 for i, city in enumerate(cities)]
    for i, c in enumerate(cities):
        c["name"] = locations[i]["name"]
        c["quests"] = locations[i]["quests"]
    for c in city_objs:
        c.name_txt = big_font.render(f"{c.name}", True, WHITE)
    print(cities)
    print(city_objs)
    objects.extend(city_objs)

    objects[0] = GameObject(pg.transform.scale(
        sprites.get_sprite("ships", 0), (40, 40)), 0, 0, id="player")
    objects[0].resting = False
    objects[0].static = False
    objects.sort()
    id_indices = populate_id_indices(objects)
    return objects, id_indices, cities


DEV_MODE = True


async def main():
    ui_inventory_win = InventoryWin(inventory, ui_manager, WIDTH, HEIGHT)

    game_mode = START_GAME_MODE
    if game_mode != 'inventory':
        ui_inventory_win.win.kill()
        ui_inventory_win = None
    quit_please = False
    red_health = 10
    yellow_health = 10
    objects, id_indices, cities = populate_objects()
    print("player", objects[id_indices["player"]])

    clock = pg.time.Clock()
    run = True
    debug_collisions = DEV_MODE
    ship_pos = vec(20, 20)
    cam_rect.x -= WIDTH/2
    cam_rect.y -= HEIGHT/2

    while run:
        dt = clock.tick(FPS)/1000.0
        for event in pg.event.get():
            if event.type == pg.QUIT or quit_please:
                run = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    quit_please = True
                if event.key == pg.K_i:
                    game_mode = "inventory"
                    ui_inventory_win = InventoryWin(
                        inventory, ui_manager, WIDTH, HEIGHT)
                if event.key == pg.K_g:
                    game_mode = "game"
                if DEV_MODE:
                    if event.key == pg.K_r:
                        objects = populate_objects()
                    if event.key == pg.K_p:
                        compare_slice_performance(objects, cam_rect)
                    if event.key == pg.K_t:
                        call_timing(objects, cam_rect)
                    if event.key == pg.K_c:
                        debug_collisions = not debug_collisions

                    if event.key == pg.K_PAGEUP:
                        GAME_OBJECT_COUNT += 1000
                    if event.key == pg.K_PAGEDOWN:
                        GAME_OBJECT_COUNT -= 1000

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                # if event.ui_element == hello_button1:
                print('Hello World!', event.ui_object_id)
                print(event)
                if event.ui_object_id == '#inv_window.#close_button':
                    game_mode = "game"
                    ui_inventory_win.win.kill()
                    ui_inventory_win = None
                if event.ui_object_id == '#inv_window.#craft_beer':
                    print("craft")
                    res = attempt_combination(
                        ui_inventory_win.input_items, 1, alchemy_game_data)
                    print(res)
                    if 'message' in res:
                        ui_inventory_win.status_text.set_text(res['message'])
                    if res['status'] == 'success':
                        out_el =res['output']
                        if not out_el in inventory:
                            inventory[out_el] = 0
                        inventory[out_el] += res['amount']
                    if 'used_resources' in res:
                        for k in  res['used_resources']:
                            ui_inventory_win.input_items[k] -= res['used_resources'][k]
                    ui_inventory_win.update_input()
                    ui_inventory_win.update_inventory(inventory)

                if event.ui_object_id.startswith('#inv_window.elem_select'):
                    elem = event.ui_object_id.split('.')[-1][1:]
                    if elem in inventory and inventory[elem] > 0:
                        inventory[elem] -= 1
                        if not elem in ui_inventory_win.input_items:
                            ui_inventory_win.input_items[elem] = 0

                        ui_inventory_win.input_items[elem] += 1
                        ui_inventory_win.update_input()
                        ui_inventory_win.update_inventory(inventory)

                    print(f"selected: '{elem}'")
                if event.ui_object_id.startswith('#inv_window.input_select'):
                    elem = event.ui_object_id.split('.')[-1][1:]
                    print(f"input_select: '{elem}'")

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
        if game_mode == "game":
            core_loop(screen, dt, cam_rect, objects, id_indices,
                      cities, std_font, big_font, WIDTH, HEIGHT, debug_collisions)
        if game_mode == "inventory":
            # Clear the screen
            screen.fill(BG_COLOR)
            txt = big_font.render(f"Inventory", True, WHITE)
            screen.blit(txt, (WIDTH/2 - txt.get_width()/2, 10))
        ui_manager.draw_ui(screen)
        pg.display.update()
        await asyncio.sleep(0)

    pg.quit()
    exit()


# if __name__ == "__main__":
asyncio.run(main())
