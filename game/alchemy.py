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
    'recipes': [],
    'skill_progression': [
        {'level': 1, 'unlocks': ['earth', 'water', 'fire', 'air']},
        {'level': 2, 'unlocks': ['metal', 'wood'], 'efficiency': 1.1},
        {'level': 3, 'unlocks': ['light', 'darkness'], 'efficiency': 1.2},
        {'level': 4, 'unlocks': ['electricity', 'ice'], 'efficiency': 1.3},
        {'level': 5, 'efficiency': 1.5, 'bonus': 'discover_new_combinations'}
    ]
}


updated_recipes = [
    {'lvl': 1, 'input': ['earth', 'water'], 'output': 'mud'},
    {'lvl': 1, 'input': ['fire', 'air'], 'output': 'smoke'},
    {'lvl': 1, 'input': ['water', 'fire'], 'output': 'steam'},
    {'lvl': 1, 'input': ['earth', 'fire'], 'output': 'lava'},
    {'lvl': 1, 'input': ['air', 'water'], 'output': 'mist'},
    {'lvl': 1, 'input': ['earth', 'air'], 'output': 'dust'},
    {'lvl': 1, 'input': ['fire', 'ice'], 'output': 'slush'},
    {'lvl': 2, 'input': ['lava', 'water'], 'output': 'stone'},
    {'lvl': 1, 'input': ['water', 'metal'], 'output': 'rust'},
    {'lvl': 1, 'input': ['earth', 'wood'], 'output': 'herbs'},
    {'lvl': 1, 'input': ['fire', 'wood'], 'output': 'charcoal'},
    {'lvl': 2, 'input': ['steam', 'metal'], 'output': 'gears'},
    {'lvl': 1, 'input': ['water', 'electricity'], 'output': 'shock'},
    {'lvl': 1, 'input': ['fire', 'light'], 'output': 'glowstone'},
    {'lvl': 1, 'input': ['air', 'darkness'], 'output': 'shadow'},
    {'lvl': 2, 'input': ['air', 'shock'], 'output': 'thunder'},
    {'lvl': 1, 'input': ['water', 'ice'], 'output': 'snow'},
    {'lvl': 1, 'input': ['fire', 'ice'], 'output': 'rainbow'},
    {'lvl': 1, 'input': ['air', 'electricity'], 'output': 'static'},
    {'lvl': 2, 'input': ['mud', 'fire'], 'output': 'brick'},
    {'lvl': 2, 'input': ['laser', 'electricity'], 'output': 'plasma'},
    {'lvl': 2, 'input': ['steam', 'earth'], 'output': 'geyser'},
    {'lvl': 2, 'input': ['mud', 'wood'], 'output': 'swamp'},
    {'lvl': 1, 'input': ['fire', 'light', 'electricity'], 'output': 'laser'},
    {'lvl': 2, 'input': ['laser', 'metal'], 'output': 'steel'},
    {'lvl': 2, 'input': ['static', 'shock'], 'output': 'lightning'},
    {'lvl': 3, 'input': ['plasma', 'earth'], 'output': 'crystal'},
    {'lvl': 2, 'input': ['mist', 'ice'], 'output': 'wind'},
    {'lvl': 2, 'input': ['snow', 'wood'], 'output': 'life'},
    {'lvl': 2, 'input': ['snow', 'air'], 'output': 'frost'},
    {'lvl': 2, 'input': ['slush', 'earth'], 'output': 'purity'},
    {'lvl': 3, 'input': ['swamp', 'fire'], 'output': 'swampfire'},
    {'lvl': 3, 'input': ['stone', 'water'], 'output': 'coral'},
    {'lvl': 3, 'input': ['brick', 'gears'], 'output': 'mechanism'},
    {'lvl': 3, 'input': ['life', 'shadow'], 'output': 'phantom'},
    {'lvl': 3, 'input': ['rust', 'charcoal'], 'output': 'smog'},
    {'lvl': 3, 'input': ['rainbow', 'snow'], 'output': 'aurora'},
    {'lvl': 3, 'input': ['smoke', 'ice'], 'output': 'haze'},
    {'lvl': 3, 'input': ['wind', 'electricity'], 'output': 'hurricane'},
    {'lvl': 3, 'input': ['gears', 'steam'], 'output': 'steam_engine'},
    {'lvl': 3, 'input': ['glowstone', 'darkness'], 'output': 'twilight'},
    {'lvl': 3, 'input': ['lightning', 'wood'], 'output': 'embers'},
    {'lvl': 4, 'input': ['crystal', 'coral'], 'output': 'prismatic_core'},
    {'lvl': 4, 'input': ['mechanism', 'steam_engine'], 'output': 'automaton'},
    {'lvl': 4, 'input': ['phantom', 'twilight'], 'output': 'spectre'},
    {'lvl': 4, 'input': ['smog', 'haze'], 'output': 'pollution'},
    {'lvl': 4, 'input': ['aurora', 'rainbow'], 'output': 'celestial_light'},
    {'lvl': 4, 'input': ['hurricane', 'embers'], 'output': 'firestorm'},
    {'lvl': 4, 'input': ['swampfire', 'steel', 'life'], 'output': 'bioforge'},
    {'lvl': 3, 'input': ['brick', 'steel', 'wood'], 'output': 'reinforced_structure'},
    {'lvl': 3, 'input': ['thunder', 'wind', 'crystal'], 'output': 'stormcore'},
    {'lvl': 4, 'input': ['glowstone', 'shadow', 'frost'], 'output': 'prismatic_shard'},
    {'lvl': 4, 'input': ['rust', 'lightning', 'stone'], 'output': 'conductite'},
    {'lvl': 3, 'input': ['rainbow', 'water', 'light'], 'output': 'spectrum_liquid'},
    {'lvl': 4, 'input': ['gears', 'electricity', 'life'], 'output': 'biomechanism'},
    {'lvl': 3, 'input': ['herbs', 'purity', 'earth'], 'output': 'regenerative_soil'},
    {'lvl': 4, 'input': ['reinforced_structure', 'biomechanism', 'prismatic_shard', 'conductite'], 'output': 'advanced_alloy'},
    {'lvl': 4, 'input': ['crystal', 'rainbow', 'sound', 'life'], 'output': 'elemental_essence'},
    {'lvl': 4, 'input': ['swampfire', 'ice', 'thunder', 'wind'], 'output': 'tempest_flame'},
    {'lvl': 4, 'input': ['lava', 'geyser', 'shadow', 'crystal'], 'output': 'magma_crux'},
    {'lvl': 3, 'input': ['steam', 'mist', 'frost', 'smoke'], 'output': 'climatic_orb'},
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
