import random
import math
from pygame.math import Vector2 as vec

def generate_random_locations(num_locations, map_rect, min_radius, max_radius):
    locations = []

    for _ in range(num_locations):
        while True:
            radius = random.uniform(min_radius, max_radius)
            x = random.uniform(radius+map_rect.left, map_rect.right - radius)
            y = random.uniform(radius+map_rect.top, map_rect.bottom - radius)

            if not any(math.sqrt((x - loc['pos'].x) ** 2 + (y - loc['pos'].y) ** 2) < (radius + loc['radius']) for loc in locations):
                break

        locations.append({'pos': vec(x,y), 'radius': radius})

    return locations

def place_elements_on_map(num_elements, element_spread, locations):
    elements = []

    for i in range(num_elements):
        element_center = random.choice(locations)
        pos = element_center['pos']
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(0, element_center['radius'])
        x = pos.x + math.cos(angle) * distance
        y = pos.y + math.sin(angle) * distance

        elements.append({
            'id': i,
            'x': x,
            'y': y,
            'concentration': random.uniform(0, element_spread)
        })

    return elements

