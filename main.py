import argparse
import pygame as pg
from pygame.math import Vector2 as vec
import os
import asyncio
import pygame_gui
import pygame_gui.elements as gui
import math
from game import *
from pygame_gui.core import ObjectID
from collections import OrderedDict

print(pg.version)
pg.freetype.init()
pg.font.init()

pg.mixer.init()

WIDTH, HEIGHT = 1280, 720
mul = 7

MAP_LEFT = int(WIDTH*-mul)
MAP_TOP = int(HEIGHT*-mul)
MAP_RIGHT = int(WIDTH*mul)
MAP_BOTTOM = int(HEIGHT*mul)
MAP_WIDTH = int(WIDTH*2*mul)
MAP_HEIGHT = int(HEIGHT*2*mul)

GAME_TITLE = "Delivery Alchemist!"
FPS = 60
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption(GAME_TITLE)
screen_rect = screen.get_rect()
cam_rect = pg.Rect(screen_rect)

ui_manager = pygame_gui.UIManager((WIDTH, HEIGHT), 'assets/theme.json')
ui_manager.add_font_paths("SHPinscher",
                          "assets/fonts/SHPinscher-Regular.otf",)
ui_manager.add_font_paths("norwester",
                          "assets/fonts/norwester.otf",)

ui_manager.preload_fonts([
    {'name': 'SHPinscher', 'point_size': 16, 'style': 'regular'},
    {'name': 'SHPinscher', 'point_size': 16, 'style': 'bold'},
    {'name': 'SHPinscher', 'point_size': 20, 'style': 'regular'},
    {'name': 'SHPinscher', 'point_size': 20, 'style': 'bold'},
    {'name': 'SHPinscher', 'point_size': 30, 'style': 'regular'},
    {'name': 'SHPinscher', 'point_size': 30, 'style': 'bold'},

])

sprites = SpritesheetManager()
sprites.load_spritesheet("ships", "assets/sheets/sheet01.json")
sprites.load_spritesheet("points", "assets/sheets/sheet_nice_large.json")
sprites.load_spritesheet("clumps", "assets/sheets/sheet_clumps.json")
sprites.load_spritesheet("elements", "assets/sheets/sheet_elements.json")

std_font = pg.font.Font("assets/fonts/SHPinscher-Regular.otf", 16)
big_font = pg.font.Font('assets/fonts/norwester.otf', 40)

GAME_OBJECT_COUNT = 12000
LEVEL = 'level_1'

BORDER = pg.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

# BULLET_HIT_SOUND = pg.mixer.Sound('Assets/Grenade+1.mp3')
# BULLET_FIRE_SOUND = pg.mixer.Sound('Assets/Gun+Silencer.mp3')


TITLE = pg.transform.scale(pg.image.load(
    os.path.join('assets', 'space3_title.png')), (WIDTH, HEIGHT))

BG = pg.transform.scale(pg.image.load(
    os.path.join('assets', 'space3.png')), (WIDTH, HEIGHT))
STARS = pg.image.load('assets/starfield.png')


START_GAME_MODE = "main_menu"
START_GAME_MODE = "startup"
image_manager = ImageManager()

DEV_MODE = False


class ObjManager:
    def __init__(self, level):
        print("POP")
        self.level = level
        self.objects = [init_obj("ship", random.randint(MAP_LEFT, MAP_RIGHT), random.randint(
            MAP_TOP, MAP_BOTTOM), sprites, self.level) for _ in range(int(GAME_OBJECT_COUNT/6))]

        self.objects.extend([init_obj("clump", random.randint(MAP_LEFT, MAP_RIGHT), random.randint(
            MAP_TOP, MAP_BOTTOM), sprites, self.level) for _ in range(int(GAME_OBJECT_COUNT/4))])

        self.element_objects = []
        self.element_indices = {}

        self.element_objects.extend([init_obj("element", random.randint(MAP_LEFT, MAP_RIGHT), random.randint(
            MAP_TOP, MAP_BOTTOM), sprites, self.level) for _ in range(int(GAME_OBJECT_COUNT/5))])

        self.element_objects[0] = init_obj(
            "player_ghost", 0, 0,  sprites, self.level)
        self.element_objects[0].id = "player_ghost"

        locations = alchemy_quests[self.level]["locations"]

        city_count = len(locations)
        print("gen_random_locations...")
        self.map_rect = pg.Rect(MAP_LEFT, MAP_TOP, MAP_WIDTH, MAP_HEIGHT)
        self.cities = generate_random_locations(
            city_count+3, self.map_rect, WIDTH, WIDTH*5)

        self.map_rect = expand_rect_if_needed(self.map_rect, self.cities)
        print("done")
        self.city_objs = [init_city(city, sprites, locations[i], i, self.level)
                          for i, city in enumerate(self.cities[:city_count])]
        self.city_objs.extend([init_alchemizer(city, sprites, locations[i], self.level)
                               for i, city in enumerate(self.cities[city_count:])])
        for i, c in enumerate(self.cities[:city_count]):
            c["name"] = locations[i]["name"]
            c["quests"] = locations[i]["quests"]
            c["welcome"] = locations[i]["welcome"]
            c["city_id"] = i

        for i, c in enumerate(self.cities[city_count:]):
            c["name"] = "Alchemizer"

        print("self.cities")
        print([c["name"] for c in self.cities])

        for i, c in enumerate(self.city_objs):
            c.name_txt = big_font.render(f"{c.name}", True, WHITE)
            self.cities[i]['sprite_id'] = c.sprite_id
        # print(self.cities)
        # print(self.city_objs)
        self.objects.extend(self.city_objs)

        self.objects[0] = GameObject(pg.transform.scale(
            sprites.get_sprite("ships", 0), (40, 40)), 0, 0, id="player")
        self.objects[0].resting = False
        self.objects[0].static = False
        self.objects[0].damage = 5
        self.objects[0].city_timeout = 0
        self.objects[0].angle = 180
        self.objects[0].can_tractor = False
        self.objects[0].can_collect = False
        self.objects[0].collected = []
        self.objects[0].health = 200
        self.objects[0].max_health = 200

        self.element_objects.sort()
        self.objects.sort()
        self.id_indices = populate_id_indices(self.objects)
        self.element_indices = populate_id_indices(self.element_objects)

        self.reset_progress()

        self.sprites = sprites
        self.STARS = STARS

    def reset_progress(self):
        self.inventory = {
            "fire": 1,
            "water": 1,
        }
        self.fadeout = 0
        self.fadeout_time = 0
        self.gold = 0

        quest_mat = []
        for k, l in alchemy_quests.items():
            for loc in l['locations']:
                for q in loc['quests']:
                    q['done'] = False
                    q['status'] = 'open'
                    q['reward'] = sum([v for k, v in q['required'].items()])
                    quest_mat.extend([k for k, v in q['required'].items()])
                # print(loc['quests'])
        self.open_quests = []
        self.sorted_materials = gather_unique_materials(alchemy_game_data)

        if DEV_MODE:
            quest_mat = set(quest_mat)
            uniq_mat = set(gather_unique_materials(alchemy_game_data))
            req_mat = collect_required_materials(
                quest_mat, alchemy_game_data['recipes'])
            self.inventory = {key: 100 for key in uniq_mat}
            self.sort_inventory()
            print("\n DO required materials match receipes? \n",
                  req_mat == uniq_mat)
            print("quest_mat", quest_mat,)
            print("uniq_mat", uniq_mat,)
            print("req_mat", req_mat,)
            print("missing for quests:\n", req_mat - uniq_mat,)
            print("superflous receipes:\n", uniq_mat-req_mat,)
            colored = set(element_colors.keys())
            print("missing colors:\n", uniq_mat - colored,)

    def sort_inventory(self):
        self.inventory = {
            key:  self.inventory[key] for key in self.sorted_materials if key in self.inventory}

    def in_transition(self):
        return self.fadeout < self.fadeout_time

    def total_material_amount(self):
        return sum(self.inventory.values())

    def draw_hud(self, screen, x, y):
        txt = std_font.render(
            # f"level: {self.level} gold:{self.gold} materials: {self.total_material_amount()}", True, WHITE)
            f"level: {self.level} materials: {self.total_material_amount()}", True, WHITE)
        screen.blit(txt, (x, y))


async def main(dev_mode, start_mode, start_level):
    global DEV_MODE
    DEV_MODE = dev_mode
    game_mode = START_GAME_MODE
    current_level = LEVEL

    if start_mode != None:
        game_mode = start_mode
    if start_level != None:
        current_level = start_level
    obj_man = ObjManager(current_level)

    ui_alchemizer_win = AlchemizerWin(
        obj_man, ui_manager, WIDTH, HEIGHT)
    if game_mode != "alchemizer":
        ui_alchemizer_win.win.kill()
        ui_alchemizer_win = None
    ui_main = MenuWin(obj_man, ui_manager, WIDTH, HEIGHT)
    if game_mode != "main_menu":
        ui_main.close()
        ui_main = None
    ui_city_win = CityWin(
        obj_man.cities[0], obj_man, ui_manager, WIDTH, HEIGHT)
    if game_mode != "city":
        ui_city_win.close()
        ui_city_win = None

    quit_please = False
    red_health = 10
    yellow_health = 10
    print("player", obj_man.objects[obj_man.id_indices["player"]])

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
            if event.type == FADEOUT:
                obj_man.do_fadeout = True
                obj_man.fadeout = 0
                obj_man.fadeout_time = event.time
            if event.type == CHANGE_GAME_MODE:
                game_mode = event.mode
                if event.mode == 'next_level':
                    current_level = event.next_level
                    game_mode = "game"
                    obj_man = ObjManager(current_level)
                    if ui_alchemizer_win != None:
                        ui_alchemizer_win.win.kill()
                        ui_alchemizer_win = None
                    if ui_main != None:
                        ui_main.close()
                        ui_main = None
                    if ui_city_win != None:
                        ui_city_win.close()
                        ui_city_win = None
                if event.mode == 'game_over':
                    pg.time.set_timer(pg.event.Event(
                        CHANGE_GAME_MODE, mode='main_menu'), 3*1000, 1)
                if event.mode == 'main_menu':
                    ui_main = MenuWin(obj_man, ui_manager, WIDTH, HEIGHT)
                    obj_man = ObjManager(current_level)
                if event.mode == "alchemizer":
                    ui_alchemizer_win = AlchemizerWin(
                        obj_man, ui_manager, WIDTH, HEIGHT)
                if event.mode == "city":
                    ui_city_win = CityWin(obj_man.cities[event.city],
                                          obj_man, ui_manager, WIDTH, HEIGHT)

            if (event.type == pg.MOUSEBUTTONDOWN or event.type == pg.KEYDOWN) \
                    and game_mode == "startup":
                pg.event.post(pg.event.Event(FADEOUT,  time=0.4))
                pg.time.set_timer(pg.event.Event(
                    CHANGE_GAME_MODE, mode='main_menu'), 400, 1)
            if DEV_MODE:
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        quit_please = True
                    if event.key == pg.K_g:
                        pg.time.set_timer(pg.event.Event(
                            CHANGE_GAME_MODE, mode='main_menu'), 10, 1)
                    if event.key == pg.K_i:
                        game_mode = "alchemizer"
                        ui_alchemizer_win = AlchemizerWin(
                            obj_man, ui_manager, WIDTH, HEIGHT)
                    if event.key == pg.K_g:
                        game_mode = "game"

                    if event.key == pg.K_r:
                        obj_man = ObjManager(current_level)
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
                    if event.key == pg.K_END:
                        force_level_completion(alchemy_quests, current_level)

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                # if event.ui_element == hello_button1:
                print('Hello World!', event.ui_object_id)
                print(event)
                if event.ui_object_id == '#inv_window.#close_button' \
                        or event.ui_object_id.endswith('close_button'):
                    game_mode = "game"
                    if ui_alchemizer_win != None:
                        ui_alchemizer_win.win.kill()
                        ui_alchemizer_win = None
                    if ui_main != None:
                        ui_main.close()
                        ui_main = None
                    if ui_city_win != None:
                        ui_city_win.close()
                        ui_city_win = None
                if event.ui_object_id == '#inv_window.#delivery':
                    print("#delivery")
                    ui_city_win.press_delivery_btn(obj_man)
                if event.ui_object_id == '#inv_window.#accept_quest':
                    print("#accept_quest")
                    ui_city_win.press_accept_btn(obj_man)
                if event.ui_object_id == '#inv_window.#craft_beer':
                    print("craft")
                    res = attempt_combination(
                        ui_alchemizer_win.input_items, 1, alchemy_game_data)
                    print(res)
                    if 'message' in res:
                        ui_alchemizer_win.status_text.set_text(res['message'])
                    if res['status'] == 'success':
                        out_el = res['output']
                        if not out_el in obj_man.inventory:
                            obj_man.inventory[out_el] = 0
                        obj_man.inventory[out_el] += res['amount']
                    if 'used_resources' in res:
                        for k in res['used_resources']:
                            ui_alchemizer_win.input_items[k] -= res['used_resources'][k]
                    ui_alchemizer_win.update_input()
                    ui_alchemizer_win.update_inventory(obj_man.inventory)

                if event.ui_object_id.startswith('#inv_window.elem_select'):
                    elem = event.ui_object_id.split('.')[-1][1:]
                    if elem in obj_man.inventory and obj_man.inventory[elem] > 0:
                        obj_man.inventory[elem] -= 1
                        if not elem in ui_alchemizer_win.input_items:
                            ui_alchemizer_win.input_items[elem] = 0

                        ui_alchemizer_win.input_items[elem] += 1
                        ui_alchemizer_win.update_input()
                        ui_alchemizer_win.update_inventory(obj_man.inventory)

                    print(f"selected: '{elem}'")
                if event.ui_object_id.startswith('#inv_window.input_select'):
                    elem = event.ui_object_id.split('.')[-1][1:]
                    print(f"input_select: '{elem}'")
                    obj_man.inventory[elem] += 1
                    ui_alchemizer_win.input_items[elem] -= 1
                    ui_alchemizer_win.update_input()
                    ui_alchemizer_win.update_inventory(obj_man.inventory)
                if event.ui_object_id.startswith('#inv_window.quest_select'):
                    city_id, quest_id = event.ui_object_id.split(
                        '.')[-1][1:].split("$")
                    city_id, quest_id = int(city_id), int(quest_id)
                    print(f"quest_select: '{city_id, quest_id }'")
                    ui_city_win.select_quest(quest_id)

            ui_manager.process_events(event)
        ui_manager.update(dt)
        completed, next_level = check_level_completion(
            alchemy_quests, current_level)
        if completed:
            print("completed, next:", next_level)
            pg.time.set_timer(pg.event.Event(
                CHANGE_GAME_MODE, mode='next_level', next_level=next_level), 10, 1)

        pressed = pg.key.get_pressed()

        if game_mode == "game":
            core_loop(screen, dt, pressed, cam_rect, obj_man,
                      std_font, big_font, WIDTH, HEIGHT, debug_collisions)
        if game_mode == "alchemizer":
            # Clear the screen
            screen.fill(BG_COLOR)
            txt = big_font.render(f"Alchemizer", True, WHITE)
            screen.blit(txt, (WIDTH/2 - txt.get_width()/2, 10))
        if game_mode == "city":
            # Clear the screen
            screen.fill(BG_COLOR)
            txt = big_font.render(f"{ui_city_win.name}", True, WHITE)
            screen.blit(txt, (WIDTH/2 - txt.get_width()/2, 10))
        if game_mode == "game_over":
            # Clear the screen
            screen.fill(BG_COLOR)
            txt = big_font.render(f"GAME OVER", True, WHITE)
            screen.blit(txt, (WIDTH/2 - txt.get_width()/2, HEIGHT/3))
        if game_mode == "main_menu":
            # Clear the screen
            screen.fill(BG_COLOR)
            screen.blit(BG, (0, 0))
            txt = big_font.render(f"{GAME_TITLE}", True, WHITE)
            screen.blit(txt, (WIDTH/2 - txt.get_width()/2, 10))
        if game_mode == "startup":
            # Clear the screen
            screen.fill(BG_COLOR)
            screen.blit(TITLE, (0, 0))
            txt = big_font.render(f"Press a Key!", True, WHITE)
            screen.blit(txt, (WIDTH/2 - txt.get_width()/2, HEIGHT-200))
        ui_manager.draw_ui(screen)
        if obj_man.fadeout < obj_man.fadeout_time:  # no player
            prg = 255 * min(1.0, obj_man.fadeout/obj_man.fadeout_time)
            draw_rect_alpha(screen, (BG_COLOR[0], BG_COLOR[1], BG_COLOR[2], prg), pg.Rect(
                0, 0, WIDTH, HEIGHT))
            obj_man.fadeout += dt

        if not game_mode in ["game_over", "main_menu"]:
            obj_man.draw_hud(screen, 20, 10)
        if DEV_MODE:
            fps = 1.0/dt
            draw_fps(screen, fps, std_font, WIDTH)
        pg.display.update()
        await asyncio.sleep(0)

    pg.quit()
    exit()

parser = argparse.ArgumentParser(description="Alchemy Game")
parser.add_argument('--dev', action='store_true', help="Enable developer mode")
parser.add_argument('--start_mode', type=str, default=None,
                    required=False, help="start game mode")
parser.add_argument('--start_level', type=str, default=None,
                    required=False, help="start specific level")
args = parser.parse_args()

asyncio.run(main(args.dev, args.start_mode, args.start_level))
