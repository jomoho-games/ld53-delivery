
alchemy_quests = {
    'level_1': {
        'max_elements': 3,
        'locations': [
            {
                'name': 'Mudville',
                'welcome':"Welcome to Mudville, the home of mud lovers! Our village is famous for its Mud Festival, muddy marshes, and cozy mud-brick houses. Join us in our muddy adventures and help keep Mudville the muddiest place around!",

                'quests': [
                    {
                        'title': 'Mud for the Mud Festival',
                        'description': 'The Mud Festival is approaching, and the villagers need more mud for the event. Deliver 10 units of mud to the Mudville Town Hall.',
                        'required': {'mud': 10}
                    },
                    {
                        'title': 'Muddy Marsh Restoration',
                        'description': 'Mudville\'s marsh is drying up. Deliver 20 units of mud and 10 units of water to the Muddy Marsh to help restore it.',
                        'required': {'mud': 20, 'water': 10}
                    },
                    {
                        'title': 'Mud Bricks for New Houses',
                        'description': 'Mudville is growing and needs more houses. Deliver 30 units of mud and 10 units of stone to the Mudville Construction Site to create mud bricks.',
                        'required': {'mud': 30, 'stone': 10}
                    }
                ]
            },
            {
                'name': 'Smoke Valley',
                'welcome': "Welcome to Smoke Valley, where the air is filled with the scent of smoke. We take pride in our Great Smoke Signal ceremony, the delicious BBQ Festival, and our unique smoke screen defense system. Join us and become a part of the smoky atmosphere!",
                'quests': [
                    {
                        'title': 'The Great Smoke Signal',
                        'description': 'The chief of Smoke Valley needs smoke for the Great Smoke Signal ceremony. Deliver 5 units of smoke to the Smoke Valley Chief\'s tent.',
                        'required': {'smoke': 5}
                    },
                    {
                        'title': 'Smoke Valley BBQ Festival',
                        'description': 'Smoke Valley is hosting a BBQ festival and needs more smoke for the perfect flavor. Deliver 15 units of smoke and 10 units of wood to the Smoke Valley BBQ Festival Grounds.',
                        'required': {'smoke': 15, 'wood': 10}
                    },
                    {
                        'title': 'Smoke Screen Defense',
                        'description': 'Smoke Valley needs to create a smoke screen to protect the valley. Deliver 25 units of smoke and 5 units of mist to the Smoke Valley Defense Outpost.',
                        'required': {'smoke': 25, 'mist': 5}
                    }
                ]
            },
            {
                'name': 'Steamtown',
                'welcome': "Welcome to Steamtown, the city powered by steam! Our steam engine, saunas, and steam-powered clock tower are the pride of our town. Lend a hand in maintaining our steampunk paradise and help us keep the steam flowing!",
                'quests': [
                    {
                        'title': 'Powering the Steam Engine',
                        'description': 'Steamtown\'s steam engine is running low on steam. Deliver 20 units of steam to the Steamtown Power Plant.',
                        'required': {'steam': 20}
                    },
                    {
                        'title': 'Steamtown Sauna',
                        'description': 'The Steamtown Sauna is not hot enough for its customers. Deliver 30 units of steam and 10 units of lava to the Steamtown Sauna to heat it up.',
                        'required': {'steam': 30, 'lava': 10}
                    },
                    {
                        'title': 'Steam-Powered Clock Tower',
                        'description': 'Steamtown\'s clock tower needs more steam to keep it running. Deliver 50 units of steam and 20 units of gears to the Steamtown Clock Tower.',
                        'required': {'steam': 50, 'gears': 20}
                    }
                ]
            }
        ]
    },
    'level_2': {
        'max_elements': 4,
        'locations': [
            {
                'name': 'Lava Island',
                'welcome': "",
                'quests': [
                    {
                        'title': 'Heating the Lava Pools',
                        'description': 'The natural lava pools on Lava Island have cooled down. Deliver 15 units of lava to the Lava Pool Park to heat them up again.',
                        'required': {'lava': 15}
                    },
                    {
                        'title': 'Lava Island Volcano Ritual',
                        'description': 'Lava Island needs more lava for their annual volcano ritual. Deliver 30 units of lava and 10 units of fire to the Volcano Ritual Site.',
                        'required': {'lava': 30, 'fire': 10}
                    },
                    {
                        'title': 'Lava-Powered Forge',
                        'description': 'The blacksmith on Lava Island needs more lava to power his forge. Deliver 40 units of lava and 20 units of stone to the Lava Island Blacksmith.',
                        'required': {'lava': 40, 'stone': 20}
                    }
                ]
            },
            {
                'name': 'Mistwood',
                'welcome': "",
                'quests': [
                    {
                        'title': 'Mystical Mist',
                        'description': 'Mistwood\'s mystical mist is disappearing. Deliver 10 units of mist to the Mistwood Altar to restore the magical atmosphere.',
                        'required': {'mist': 10}
                    },
                    {
                        'title': 'Mistwood Healing Sanctuary',
                        'description': 'The Healing Sanctuary in Mistwood needs more mist for its medicinal baths. Deliver 20 units of mist and 10 units of herbs to the Mistwood Healing Sanctuary.',
                        'required': {'mist': 20, 'herbs': 10}
                    },
                    {
                        'title': 'Mistwood Foggy Forest',
                        'description': 'The Foggy Forest in Mistwood is losing its fog. Deliver 30 units of mist and 15 units of darkness to the Mistwood Foggy Forest Entrance.',
                        'required': {'mist': 30, 'darkness': 15}
                    }
                ]
            },
            {
                'name': 'Dust Valley',
                'welcome': "",
                'quests': [
                    {
                        'title': 'The Dusty Road',
                        'description': 'The Dust Valley roads are too clean, and the locals are suspicious. Deliver 20 units of dust to the Dust Valley Road Maintenance Department.',
                        'required': {'dust': 20}
                    },
                    {
                        'title': 'Desert Agriculture',
                        'description': 'Dust Valley needs more dust to support their desert agriculture. Deliver 30 units of dust and 10 units of water to the Dust Valley Agricultural Research Center.',
                        'required': {'dust': 30, 'water': 10}
                    },
                    {
                        'title': 'Dust Valley Sandstorm Festival',
                        'description': 'The Sandstorm Festival in Dust Valley is approaching, and they need more dust to create sandstorms. Deliver 40 units of dust and 20 units of wind to the Dust Valley Sandstorm Festival Grounds.',
                        'required': {'dust': 40, 'wind': 20}
                    }
                ]
            }
        ]
    },
    'level_3': {
        'max_elements': 5,
        'locations': [
            {
                'name': 'Rust Harbor',
                'welcome': "",
                'quests': [
                    {
                        'title': 'Rusting the Anchors',
                        'description': 'Rust Harbor needs more rust for their rusty anchor exhibition. Deliver 25 units of rust to the Rust Harbor Museum.',
                        'required': {'rust': 25}
                    },
                    {
                        'title': 'Restoring the Rusty Bridge',
                        'description': 'The Rusty Bridge in Rust Harbor needs reinforcement. Deliver 35 units of rust and 15 units of steel to the Rust Harbor Bridge Repair Team.',
                        'required': {'rust': 35, 'steel': 15}
                    },
                    {
                        'title': 'Rust Harbor Rust-Proof Coating',
                        'description': 'Rust Harbor needs a rust-proof coating to protect their structures. Deliver 45 units of rust and 25 units of crystal to the Rust Harbor Infrastructure Department.',
                        'required': {'rust': 45, 'crystal': 25}
                    }
                ]
            },
            {
                'name': 'Charcoal Village',
                'welcome': "",
                'quests': [
                    {
                        'title': 'Charcoal Drawings',
                        'description': 'Charcoal Village is hosting a charcoal drawing competition. Deliver 20 units of charcoal to the Charcoal Village Art Center.',
                        'required': {'charcoal': 20}
                    },
                    {
                        'title': 'Charcoal Village BBQ Party',
                        'description': 'Charcoal Village is hosting a BBQ party and needs more charcoal for grilling. Deliver 25 units of charcoal to the Charcoal Village BBQ Grounds.',
                        'required': {'charcoal': 25}
                    },
                    {
                        'title': 'Charcoal Village Blacksmith',
                        'description': 'Charcoal Village\'s furnace is low on fuel. Deliver 30 units of charcoal to the Charcoal Village Blacksmith.',
                        'required': {'charcoal': 30}
                    }
                ]
            },
            {
                'name': 'Glowstone Caverns',
                'welcome': "",
                'quests': [
                    {
                        'title': 'Glowstone Caverns Lighting',
                        'description': 'Glowstone Caverns is running low on light. Deliver 10 units of glowstone to the Glowstone Caverns Tourist Center.',
                        'required': {'glowstone': 10}
                    },
                    {
                        'title': 'Glowstone Caverns Bioluminescent Garden',
                        'description': 'The bioluminescent garden in Glowstone Caverns needs more light. Deliver 20 units of glowstone and 15 units of life to the Glowstone Caverns Bioluminescent Garden.',
                        'required': {'glowstone': 20, 'life': 15}
                    },
                    {
                        'title': 'Glowstone Caverns Crystal Clear Waters',
                        'description': 'The crystal clear waters in Glowstone Caverns need more glowstone to maintain their clarity. Deliver 30 units of glowstone and 20 units of purity to the Glowstone Caverns Crystal Clear Waters.',
                        'required': {'glowstone': 30, 'purity': 20}
                    }
                ]
            }
        ]
    },
    'level_4': {
        'max_elements': 9,
        'locations': [
            {
                'name': 'Laser City',
                'welcome': "",
                'quests': [
                    {
                        'title': 'Laser City Laser Tag Arena',
                        'description': 'The Laser City Laser Tag Arena needs more lasers for their games. Deliver 10 units of laser to the Laser City Laser Tag Arena.',
                        'required': {'laser': 10}
                    },
                    {
                        'title': 'Laser City Light Speed Transportation',
                        'description': 'Laser City is developing a light-speed transportation system and needs more lasers for research. Deliver 15 units of laser and 10 units of light to the Laser City Research Lab.',
                        'required': {'laser': 15, 'light': 10}
                    },
                    {
                        'title': 'Light Show Spectacle',
                        'description': 'Laser City is hosting a light show, and they need more lasers for the spectacle. Deliver 20 units of laser and 10 units of rainbow to the Laser City Light Show Grounds.',
                        'required': {'laser': 20, 'rainbow': 10}
                    }
                ]
            },
            {
                'name': 'Thunderstorm Bay',
                'welcome': "",
                'quests': [
                    {
                        'title': 'Thunderstorm Bay Lighthouse',
                        'description': 'The Thunderstorm Bay Lighthouse needs more electricity to function. Deliver 25 units of electricity to the Thunderstorm Bay Lighthouse.',
                        'required': {'electricity': 25}
                    },
                    {
                        'title': 'Thunderstorm Bay Concert',
                        'description': 'Thunderstorm Bay is hosting a concert and needs more electricity for the stage. Deliver 30 units of electricity and 20 units of sound to the Thunderstorm Bay Concert Grounds.',
                        'required': {'electricity': 30, 'sound': 20}
                    },
                    {
                        'title': 'Thunderstorm Bay Power Plant',
                        'description': 'The Thunderstorm Bay Power Plant needs more electricity to power the city. Deliver 35 units of electricity and 15 units of thunder to the Thunderstorm Bay Power Plant.',
                        'required': {'electricity': 35, 'thunder': 15}
                    }
                ]
            },
            {
                'name': 'Frostpeak Village',
                'welcome': "",
                'quests': [
                    {
                        'title': 'Frostpeak Village Ice Sculpture Contest',
                        'description': 'Frostpeak Village is hosting an ice sculpture contest and needs more ice. Deliver 20 units of ice to the Frostpeak Village Contest Grounds.',
                        'required': {'ice': 20}
                    },
                    {
                        'title': 'Frostpeak Village Ski Resort',
                        'description': 'The Frostpeak Village Ski Resort needs more ice for their slopes. Deliver 25 units of ice and 10 units of snow to the Frostpeak Village Ski Resort.',
                        'required': {'ice': 25, 'snow': 10}
                    },
                    {
                        'title': 'Frostpeak Village Ice Wine Festival',
                        'description': 'The Ice Wine Festival in Frostpeak Village needs more ice to chill the wine. Deliver 30 units of ice and 15 units of frost to the Frostpeak Village Ice Wine Festival Grounds.',
                        'required': {'ice': 30, 'frost': 15}
                    }
                ]
            }
        ]
    },
    'level_5': {
        'max_elements': 9,
        'locations': [
            {
                'name': 'Electro City',
                'welcome': "",
                'quests': [
                    {
                        'title': 'Electrostatic Field Generator',
                        'description': 'Electro City needs more static to power their electrostatic field generator. Deliver 20 units of static to the Electro City Generator Facility.',
                        'required': {'static': 20}
                    },
                    {
                        'title': 'Lightning Rod Installation',
                        'description': 'Electro City is installing lightning rods and needs more lightning. Deliver 30 units of lightning to the Electro City Lightning Rod Distribution Center.',
                        'required': {'lightning': 30}
                    },
                    {
                        'title': 'Shockproof Armor Research',
                        'description': 'Electro City is researching shockproof armor and needs more shock. Deliver 15 units of shock to the Electro City Research Lab.',
                        'required': {'shock': 15}
                    }
                ]
            },
            {
                'name': 'Shady Grove',
                'welcome': "",
                'quests': [
                    {
                        'title': 'Shadow Puppet Theater',
                        'description': 'Shady Grove is hosting a shadow puppet theater and needs more shadow. Deliver 25 units of shadow to the Shady Grove Puppet Theater.',
                        'required': {'shadow': 25}
                    },
                    {
                        'title': 'Shadow Tonic Production',
                        'description': 'Shady Grove needs more shadow tonics for their annual Shadow Festival. Deliver 30 units of shadow and 20 units of herbs to the Shady Grove Apothecary.',
                        'required': {'shadow': 30, 'herbs': 20}
                    },
                    {
                        'title': 'Darkness Illumination Research',
                        'description': 'Shady Grove is researching the illumination of darkness. Deliver 25 units of darkness and 15 units of light to the Shady Grove Research Center.',
                        'required': {'darkness': 25, 'light': 15}
                    }
                ]
            },
            {
                'name': 'Swamplandia',
                'welcome': "",
                'quests': [
                    {
                        'title': 'Swamplandia Boardwalk Expansion',
                        'description': 'Swamplandia is expanding their boardwalk and needs more swamp materials. Deliver 40 units of swamp to the Swamplandia Boardwalk Construction Site.',
                        'required': {'swamp': 40}
                    },
                    {
                        'title': 'Swampfire Lanterns',
                        'description': 'Swamplandia needs more swampfire lanterns for their Swampfire Festival. Deliver 30 units of swampfire and 20 units of glowstone to the Swamplandia Lantern Workshop.',
                        'required': {'swampfire': 30, 'glowstone': 20}
                    },
                    {
                        'title': 'Swamplandia Mud Baths',
                        'description': 'Swamplandia is opening a new mud bath spa and needs more mud. Deliver 50 units of mud and 20 units of herbs to the Swamplandia Mud Bath Spa.',
                        'required': {'mud': 50, 'herbs': 20}
                    }
                ]
            }
        ]
    },
    'level_6': {
        'max_elements': 9,
        'locations': [
            {
                'name': 'Geyser Springs',
                'welcome': "",
                'quests': [
                    {
                        'title': 'Geothermal Energy Research',
                        'description': 'Geyser Springs is researching geothermal energy and needs more geysers. Deliver 25 units of geyser to the Geyser Springs Geothermal Research Center.',
                        'required': {'geyser': 25}
                    },
                    {
                        'title': 'Geyser-Powered Turbine Maintenance',
                        'description': 'Geyser Springs needs more steam to maintain their geyser-powered turbines. Deliver 30 units of steam to the Geyser Springs Turbine Maintenance Facility.',
                        'required': {'steam': 30}
                    },
                    {
                        'title': 'Hot Springs Restoration',
                        'description': 'Geyser Springs is restoring their hot springs and needs more lava. Deliver 20 units of lava to the Geyser Springs Hot Springs Restoration Site.',
                        'required': {'lava': 20}
                    }
                ]
            },
            {
                'name': 'Brickton',
                'welcome': "",
                'quests': [
                    {
                        'title': 'Brickton Construction Project',
                        'description': 'Brickton is building new structures and needs more bricks. Deliver 50 units of brick to the Brickton Construction Site.',
                        'required': {'brick': 50}
                    },
                    {
                        'title': 'Brickton Infrastructure Improvement',
                        'description': 'Brickton needs more steel to improve their infrastructure. Deliver 40 units of steel to the Brickton Infrastructure Improvement Site.',
                        'required': {'steel': 40}
                    },
                    {
                        'title': 'Brickton Decorative Sculptures',
                        'description': 'Brickton is creating decorative sculptures and needs more crystal. Deliver 15 units of crystal to the Brickton Sculpture Workshop.',
                        'required': {'crystal': 15}
                    }
                ]
            },
            {
                'name': 'Final Challenge Island',
                'welcome': "",
                'quests': [
                    {
                        'title': 'Elemental Balance',
                        'description': 'Final Challenge Island needs a balance of elemental materials. Deliver 10 units each of fire, water, earth, and air to the Elemental Balance Shrine.',
                        'required': {'fire': 10, 'water': 10, 'earth': 10, 'air': 10}
                    },
                    {
                        'title': 'Restore the Purity Fountain',
                        'description': 'Final Challenge Island needs more purity to restore the Purity Fountain. Deliver 20 units of purity to the Purity Fountain Restoration Site.',
                        'required': {'purity': 20}
                    },
                    {
                        'title': 'Activate the Rainbow Bridge',
                        'description': 'Final Challenge Island needs more rainbow to activate the Rainbow Bridge. Deliver 15 units of rainbow to the Rainbow Bridge Activation Site.',
                        'required': {'rainbow': 15}
                    },
                    {
                        'title': 'Recharge the Plasma Core',
                        'description': 'Final Challenge Island needs more plasma to recharge their Plasma Core. Deliver 25 units of plasma to the Plasma Core Recharge Station.',
                        'required': {'plasma': 25}
                    },
                    {
                        'title': 'Power the Swampfire Beacon',
                        'description': 'Final Challenge Island needs more swampfire to power the Swampfire Beacon. Deliver 30 units of swampfire to the Swampfire Beacon Activation Site.',
                        'required': {'swampfire': 30}
                    }
                ]
            }
        ]
    }
}
def can_fulfill_quest(inventory, quest_requirements):
    for material, required_amount in quest_requirements.items():
        if inventory.get(material, 0) < required_amount:
            return False
    return True


def force_level_completion(alchemy_quests, current_level):
    level = alchemy_quests[current_level]
    level_complete = True

    for location in level['locations']:
        for quest in location['quests']:
            quest['done']=True

def check_level_completion(alchemy_quests, current_level):
    level = alchemy_quests[current_level]
    level_complete = True

    for location in level['locations']:
        for quest in location['quests']:
            if not quest.get('done', False):
                level_complete = False
                break

    if level_complete:
        next_level = f'level_{int(current_level.split("_")[1]) + 1}'
        if next_level in alchemy_quests:
            return (True, next_level)
        else:
            return (True, None)
    else:
        return (False, None)
