from game.map_gen import *

map_size = 1000
num_locations = 10
min_location_radius = 50
max_location_radius = 150
num_elements = 50
element_spread = 10

locations = generate_random_locations(num_locations, map_size, min_location_radius, max_location_radius)
elements = place_elements_on_map(num_elements, element_spread, locations)

print(locations)
# print(elements)