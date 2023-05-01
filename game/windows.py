import pygame as pg
from pygame.math import Vector2 as vec
import os
import asyncio
import pygame_gui
import pygame_gui.elements as gui
import math
from pygame_gui.core import ObjectID
from .quests import *


class AlchemizerWin:
    def __init__(self, obj_man, ui_manager, WIDTH, HEIGHT):
        w = WIDTH-100
        h = HEIGHT-100
        self.win = gui.UIWindow(pg.Rect(50, 50, w, h),
                                draggable=False,
                                object_id="#inv_window",
                                window_display_title="Alchemizer")

        elementlist = [(f'{k}: {n}', f"#{k}")
                       for k, n in obj_man.inventory.items() if n > 0]
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

        self.status_text = gui.UILabel(pg.Rect(w/2-120, h-210, 600, 50),
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
                                                object_id="close_button",
                                                text="Close",
                                                )
        self.spr = obj_man.sprites.get_sprite("points", 18)
        desired_width = 400
        spr_scale = desired_width / self.spr.get_width()
        self.img = gui.UIImage(pg.Rect(w/2, 50, self.spr.get_width()*spr_scale, self.spr.get_height()*spr_scale),
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


class CityWin:
    def __init__(self, city, obj_man, ui_manager, WIDTH, HEIGHT):
        self.city = city
        self.obj_man = obj_man

        print(city)
        self.name = city['name']
        w = WIDTH-100
        h = HEIGHT-100
        self.win = gui.UIWindow(pg.Rect(50, 50, w, h),
                                draggable=False,
                                object_id="#inv_window",
                                window_display_title=f"{self.name}")
        quest_list = [(f'{k["title"]}:', f"#{city['city_id']}${i}")
                      for i, k in enumerate(city['quests']) if not k['done']]

        self.ui_element_select = gui.UISelectionList(pg.Rect(w-250, 50, 200, h-200),
                                                     manager=ui_manager,
                                                     container=self.win,
                                                     item_list=list(
                                                         quest_list),
                                                     object_id="quest_select",
                                                     allow_multi_select=False)

        self.status_text = gui.UILabel(pg.Rect(w-295, 20, 200, 40),
                                       manager=ui_manager,
                                       container=self.win,
                                       text="Choose a delivery",
                                       )
        self.text_output_box = gui.UITextBox(f'<font face="norwester" color="#ffffff" size=30>{self.city["name"]}</font>\n<br>{self.city["welcome"]}',
                                             pg.Rect(400, 50, 500, h-200),
                                             container=self.win)

        self.accept_btn = gui.ui_button.UIButton(pg.Rect(400, h-120, 200, 50),
                                                 manager=ui_manager,
                                                 container=self.win,
                                                 text="Accept!",
                                                 object_id="#accept_quest",
                                                 )
        self.accept_btn.hide()
        self.delivery_btn = gui.ui_button.UIButton(pg.Rect(400, h-120, 200, 50),
                                                   manager=ui_manager,
                                                   container=self.win,
                                                   text="FULFILL DELIVERY!",
                                                   object_id="#delivery",
                                                   )
        self.delivery_btn.hide()
        self.close_btn = gui.ui_button.UIButton(pg.Rect(w-250, h-120, 200, 50),
                                                manager=ui_manager,
                                                container=self.win,
                                                object_id="close_button",
                                                text="Close",
                                                )
        self.spr = obj_man.sprites.get_sprite("points", city['sprite_id'])
        desired_width = 340  # Set this to your desired width
        max_height = h-120
        # Calculate the scale value
        spr_scale = desired_width / self.spr.get_width()

        # Check if the scaled height is greater than the maximum height
        if int(self.spr.get_height() * spr_scale) > max_height:
            # Adjust the scale value based on the maximum height
            spr_scale = max_height / self.spr.get_height()

        print("City sprite_id:", city['sprite_id'])
        self.img = gui.UIImage(pg.Rect(30, 50, self.spr.get_width()*spr_scale, self.spr.get_height()*spr_scale),
                               self.spr,
                               manager=ui_manager,
                               container=self.win,
                               )

    def refresh_quest_list(self):
      quest_list = [(f'{k["title"]}:', f"#{self.city['city_id']}${i}")
                      for i, k in enumerate(self.city['quests']) if not k['done']]
      self.ui_element_select.set_item_list(quest_list)

    def press_delivery_btn(self, obj_man):
        # TODO
        q = self.city["quests"][self.selected_id]
        print("press_delivery_btn")
        q['status'] = 'done'
        q['done'] = True
        for k,v in q['required'].items():
          obj_man.inventory[k] -= v
        self.refresh_quest_list()
        self.text_output_box.set_text(f'<font face="norwester" color="#ffffff" size=30>{self.city["name"]}</font>\n<br>{self.city["welcome"]}',)
        self.delivery_btn.hide()

    def press_accept_btn(self, obj_man):
        q = self.city["quests"][self.selected_id]
        obj_man.open_quests.append((q, self.city['city_id'], self.selected_id))
        q['status'] = 'accepted'
        self.accept_btn.disable()
        self.accept_btn.hide()
        self.select_quest(self.selected_id)



    def select_quest(self, id):
        self.selected_id = id
        # "<font size=20>Title Text</font>\n<br><br> Description etc.<br> requirements: 2 gold, 5 fish"
        q = self.city["quests"][id]

        req = "\n<font color='#ffffff'>Required:</font>\n"
        for r, v in q['required'].items():
            req += f'{r}: {v} \n'
        stat = "Accept Delivery to Start working on it"
        self.accept_btn.enable()
        self.accept_btn.show()
        self.delivery_btn.hide()
        if q['status'] == 'accepted':
            self.accept_btn.disable()
            self.accept_btn.hide()
            stat = "Gather Elements and Alchemize them to fulfill the delivery!"
            if can_fulfill_quest(self.obj_man.inventory, q['required']):
                stat = "You can fulfill the delivery! Push the Button to be rewarded!"
                self.delivery_btn.enable()
                self.delivery_btn.show()

        self.text_output_box.set_text(
            f'<font face="norwester" color="#ffffff" size=30>{q["title"]}</font>\n\n{q["description"]}\n{req}\n<font color="#ffffff">Status:</font>\n{stat}')


    def update_input(self):
        input_list = [(f'{k}: {n}', f"#{k}")
                      for k, n in self.input_items.items() if n > 0]
        self.ui_input_select.set_item_list(input_list)

    def update_inventory(self, obj_man):
        elementlist = [(f'{k}: {n}', f"#{k}")
                       for k, n in obj_man.inventory.items() if n > 0]
        self.ui_element_select.set_item_list(elementlist)
    def close(self):
        self.win.kill()


intro_msg = """<p><strong>Welcome, brave Alchemist!</strong> In a galaxy filled with wonder and mystery, you have embarked on a grand journey through the cosmos as a master of the ancient art of Alchemy. You possess the unique ability to combine elements and materials, harnessing their powers to create new substances and complete various quests across the universe.</p>
<p>As you traverse through the vast expanse of space, you will encounter diverse planets and celestial settlements, each with their own unique challenges and materials. By solving their quests and helping the inhabitants, you will not only gain valuable resources but also expand your knowledge of Alchemy.</p>
<p>To begin your adventure, you will start with a basic set of materials. As you progress, you will unlock new elements and recipes by combining existing materials. Remember, the universe is vast and unexplored, and not all combinations are known. Experimentation and creativity are crucial to your success.</p>
<p>Now, prepare yourself and embark on this epic journey to become the greatest Alchemist in the cosmos.
<b>Good luck, and may the stars guide you!</b></p>"""


class MenuWin:
    def __init__(self, obj_man, ui_manager, WIDTH, HEIGHT):
        w = WIDTH-100
        h = HEIGHT-100
        # self.win = gui.UIWindow(pg.Rect(50, 50, w, h),
        #                         draggable=False,
        #                         visible=False,
        #                         object_id="#inv_window",
        #                         window_display_title="Alchemy Delivery")
        self.text_output_box = gui.UITextBox(intro_msg,
                                             pg.Rect(100, 80, WIDTH -
                                                     200, HEIGHT-220),
                                             object_id="#intro_text",
                                             )

        self.win = gui.ui_button.UIButton(pg.Rect(WIDTH/2-100, HEIGHT-100, 200, 50),
                                          manager=ui_manager,
                                          # container=self.win,
                                          object_id="close_button",
                                          text="Start Game",
                                          )

    def close(self):
        self.win.kill()
        self.text_output_box.kill()
