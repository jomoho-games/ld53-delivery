from collections import OrderedDict
import random
import math


class GameProgress:
    def __init__(self):
        self.inventory = {}
        self.skill_level = 1
        self.unlocked = []
        self.refresh_unlocked()
        self.xp = 0

    def add_xp(self, xp):
        self.xp += xp
        self.skill_level = self.calculate_skill_level()

    def calculate_skill_level(self):
        level = 1
        xp_required = 100
        xp = int(self.xp)

        while xp >= xp_required:
            xp -= xp_required
            level += 1
            xp_required *= 2

        return level

    def xp_required_for_next_level(self):
        level = self.calculate_skill_level()
        return 100 * (2 ** (level - 1))

    def refresh_unlocked(self):
        self.unlocked = []
        for s in alchemy_game_data['skill_progression']:
            if self.skill_level >= s['level']:
                self.unlocked.extend(s['unlocks'])
        self.unlocked = list(set(self.unlocked))


alchemy_game_data = {

    'elements': [
        'earth', 'water', 'fire', 'air', 'metal', 'wood', 'light', 'darkness', 'electricity', 'ice'
    ],
    'recipes': [
        {'input': ['earth', 'water'], 'output': 'mud'},
        {'input': ['fire', 'air'], 'output': 'smoke'},
        {'input': ['water', 'fire'], 'output': 'steam'},
        {'input': ['earth', 'fire'], 'output': 'lava'},
        {'input': ['air', 'water'], 'output': 'mist'},
        {'input': ['earth', 'air'], 'output': 'dust'},

        {'input': ['water', 'metal'], 'output': 'rust'},
        {'input': ['earth', 'wood'], 'output': 'fossil'},
        {'input': ['fire', 'wood'], 'output': 'charcoal'},
        {'input': ['steam', 'metal'], 'output': 'boiler'},

        {'input': ['fire', 'light'], 'output': 'laser'},
        {'input': ['air', 'darkness'], 'output': 'void'},
        {'input': ['air', 'electricity'], 'output': 'static'},
        {'input': ['water', 'electricity'], 'output': 'shock'},
        {'input': ['water', 'ice'], 'output': 'snow'},
        {'input': ['fire', 'ice'], 'output': 'slush'},
        {'input': ['mud', 'fire'], 'output': 'brick'},
        {'input': ['laser', 'electricity'], 'output': 'plasma'},
        {'input': ['steam', 'earth'], 'output': 'geyser'},
        {'input': ['mud', 'wood'], 'output': 'swamp'},
        {'input': ['smoke', 'void'], 'output': 'shadow'},
        {'input': ['lava', 'water'], 'output': 'obsidian'},
        {'input': ['laser', 'metal'], 'output': 'cutting_beam'},
        {'input': ['static', 'shock'], 'output': 'lightning'},
        {'input': ['plasma', 'earth'], 'output': 'energy_crystal'},
        {'input': ['brick', 'metal'], 'output': 'reinforced_structure'},
        {'input': ['mist', 'ice'], 'output': 'frost'},
        {'input': ['snow', 'wood'], 'output': 'snowy_forest'},
        {'input': ['slush', 'earth'], 'output': 'permafrost'},
        {'input': ['void', 'light'], 'output': 'twilight'}
    ],
    'skill_progression': [
        {'level': 1, 'unlocks': ['earth', 'water', 'fire', 'air']},
        {'level': 2, 'unlocks': ['metal', 'wood'], 'efficiency': 1.1},
        {'level': 3, 'unlocks': ['light', 'darkness'], 'efficiency': 1.2},
        {'level': 4, 'unlocks': ['electricity', 'ice'], 'efficiency': 1.3},
        {'level': 5, 'efficiency': 1.5, 'bonus': 'discover_new_combinations'}
    ]
}


updated_recipes = [
    {'input': ['earth', 'water'], 'output': 'mud'},
    {'input': ['fire', 'air'], 'output': 'smoke'},
    {'input': ['water', 'fire'], 'output': 'steam'},
    {'input': ['earth', 'fire'], 'output': 'lava'},
    {'input': ['air', 'water'], 'output': 'mist'},
    {'input': ['earth', 'air'], 'output': 'dust'},

    {'input': ['lava', 'water'], 'output': 'stone'},
    {'input': ['water', 'metal'], 'output': 'rust'},
    {'input': ['earth', 'wood'], 'output': 'herbs'},
    {'input': ['fire', 'wood'], 'output': 'charcoal'},
    {'input': ['steam', 'metal'], 'output': 'gears'},

    {'input': ['fire', 'light'], 'output': 'glowstone'},
    {'input': ['air', 'darkness'], 'output': 'shadow'},
    {'input': ['air', 'electricity'], 'output': 'sound'},
    {'input': ['water', 'electricity'], 'output': 'thunder'},
    {'input': ['water', 'ice'], 'output': 'snow'},
    {'input': ['fire', 'ice'], 'output': 'rainbow'},

    {'input': ['mud', 'fire'], 'output': 'brick'},
    {'input': ['laser', 'electricity'], 'output': 'plasma'},
    {'input': ['steam', 'earth'], 'output': 'geyser'},
    {'input': ['mud', 'wood'], 'output': 'swamp'},

    {'input': ['laser', 'metal'], 'output': 'steel'},
    {'input': ['static', 'shock'], 'output': 'lightning'},
    {'input': ['plasma', 'earth'], 'output': 'crystal'},
    {'input': ['mist', 'ice'], 'output': 'wind'},
    {'input': ['snow', 'wood'], 'output': 'life'},
    {'input': ['snow', 'air'], 'output': 'frost'},
    {'input': ['slush', 'earth'], 'output': 'purity'},
    {'input': ['swamp', 'fire'], 'output': 'swampfire'}
]


alchemy_game_data['recipes'] = updated_recipes


def gather_unique_materials(alchemy_game_data):
    unique_materials = list(alchemy_game_data['elements'])

    for recipe in alchemy_game_data['recipes']:
        unique_materials.extend(recipe['input'])
        unique_materials.append(recipe['output'])
    unique_materials = list(OrderedDict.fromkeys(unique_materials).keys())
    return unique_materials


def collect_required_materials(quest_materials, recipes):
    materials = set(quest_materials)

    for material in quest_materials:
        for recipe in recipes:
            if recipe['output'] == material:
                materials.update(recipe['input'])
                break

    return materials


def attempt_combination(input_elements, skill_level, alchemy_data):
    # Check if the user has enough elements for the combination
    # for element, amount in input_elements.items():
    #     if amount <= 0:
    #         return {'status': 'error', 'message': f'Not enough {element} to attempt combination'}

    # Find the recipe for the given input_elements
    input_set = set([k for k, n in input_elements.items() if n > 0])
    recipe = None
    for r in alchemy_data['recipes']:
        if set(r['input']) == input_set:
            recipe = r
            break

    # Check if the recipe is found and if it's already discovered
    if recipe is None:  # or recipe['output'] not in discovered_combinations:
        return {'status': 'error', 'message': 'Unknown combination'}

    # Apply efficiency based on skill level
    efficiency = 1
    for skill in alchemy_data['skill_progression']:
        if skill_level >= skill['level']:
            efficiency = skill.get('efficiency', efficiency)
        else:
            break

    # Adjust the amount of resources used based on efficiency
    used_resources = {}
    for element, amount in input_elements.items():
        used_amount = int(math.ceil(amount * (1 / efficiency)))
        if used_amount > 0:
            used_resources[element] = used_amount

    # Calculate the success chance and determine if the combination is successful
    success_chance = random.uniform(0, 1)
    amount = min(used_resources.values())
    if success_chance <= efficiency:
        result = {'status': 'success',
                  'output': recipe['output'],
                  'message': f'Combination succeeded: {amount} {recipe["output"]} created!',
                  'amount': amount, 'used_resources': used_resources}
    else:
        result = {'status': 'failure', 'message': 'Combination attempt failed',
                  'used_resources': used_resources}

    return result


element_colors = {
    "air": (230, 230, 230),
    "earth": (139, 69, 19),
    "fire": (255, 69, 0),
    "water": (30, 144, 255),
    "steam": (192, 192, 192),
    "mud": (121, 68, 59),
    "lava": (207, 16, 32),
    "dust": (210, 180, 140),
    "energy": (255, 215, 0),
    "life": (50, 205, 50),
    "stone": (112, 128, 144),
    "rain": (70, 130, 180),
    "storm": (72, 61, 139),
    "ice": (176, 224, 230),
    "swamp": (47, 79, 79),
    "light": (255, 255, 224),
    "darkness": (25, 25, 112),
    "cloud": (245, 245, 245),
    "thunder": (255, 140, 0),
    "sand": (244, 164, 96),
    "glass": (211, 211, 211),
    "crystal": (0, 191, 255),
    "salt": (255, 250, 250),
    "electricity": (233, 236, 179),
    "snow": (255, 250, 250),
    "metal": (192, 192, 192),
    "wood": (139, 115, 85),
    "charcoal": (54, 69, 79),
    "mist": (224, 255, 255),
    "rust": (183, 65, 14),
    "smoke": (105, 105, 105),
    "ash": (135, 135, 135),
    "glowstone": (255, 255, 153),
    "laser": (255, 20, 147),
    "rainbow": (148, 0, 211),
    "sound": (123, 104, 238),
    "frost": (135, 206, 235),
    "purity": (255, 255, 255),
    "shock": (0, 255, 127),
    "brick": (178, 34, 34),
    "gears": (169, 169, 169),
    "static": (220, 220, 220),
    "plasma": (255, 105, 180),
    "herbs": (60, 179, 113),
    "slush": (135, 206, 250),
    "shadow": (75, 0, 130),
    "steel": (70, 130, 180),
    "swampfire": (46, 139, 87),
    "geyser": (95, 158, 160),
    "lightning": (255, 255, 0),
    "wind": (240, 255, 255)
}
