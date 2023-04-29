from game.alchemy import *
# alchemy_game_data = { ... }  # The alchemy_game_data dictionary provided earlier
input_elements = {'laser': 2, 'water': 2}
skill_level = 2
discovered_combinations = ['mud', 'smoke', 'steam']

result = attempt_combination(input_elements, skill_level, discovered_combinations, alchemy_game_data)
print(result)