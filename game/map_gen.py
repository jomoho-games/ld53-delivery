import random
import math
import pygame
from pygame.math import Vector2 as vec

from pygame.math import Vector2 as vec

EXPAND_RECT_RATIO=0.8
def calculate_total_area(locations):
    total_area = 0
    for location in locations:
        radius = location['radius']
        area = math.pi * (radius ** 2)
        total_area += area
    return total_area

def calculate_rect_area(rect):
    return rect.width * rect.height


def expand_rect(rect, expansion_amount):
    expanded_rect = pygame.Rect(
        rect.left - expansion_amount,
        rect.top - expansion_amount,
        rect.width + expansion_amount * 2,
        rect.height + expansion_amount * 2
    )
    return expanded_rect

def expand_rect_if_needed(rect, locations, target_ratio=EXPAND_RECT_RATIO):
    rect_area = calculate_rect_area(rect)
    circle_area = calculate_total_area(locations)
    ratio = circle_area / rect_area

    if ratio > target_ratio:
        required_ratio = circle_area / target_ratio
        expansion_amount = math.sqrt(required_ratio / rect_area) - 1
        expansion_amount *= max(rect.width, rect.height) / 2
        expanded_rect = expand_rect(rect, expansion_amount)
        return expanded_rect
    else:
        return rect

def generate_random_locations(num_locations, map_rect, min_radius, max_radius, iterations=200, max_push_strength=0.0001, damping=0.0001):
    locations = []

    # Generate random circles
    for _ in range(num_locations):
        radius = random.uniform(min_radius, max_radius)
        x = random.uniform(radius + map_rect.left, map_rect.right - radius)
        y = random.uniform(radius + map_rect.top, map_rect.bottom - radius)
        locations.append({'pos': vec(x, y), 'radius': radius, 'prev_pos': vec(x, y)})

    map_rect = expand_rect_if_needed(map_rect, locations)

    # Push circles away from each other
    for _ in range(iterations):
        for i, loc1 in enumerate(locations):
            for j, loc2 in enumerate(locations):
                if i != j:
                    d = loc1['pos'] - loc2['pos']
                    distance = d.length()

                    if distance < loc1['radius'] + loc2['radius']:
                        d.normalize()
                        overlap = loc1['radius'] + loc2['radius'] - distance
                        push_strength = max_push_strength * (1 - distance / (loc1['radius'] + loc2['radius']))
                        displacement = d * (overlap / 2) * push_strength

                        loc1['pos'] += displacement
                        loc2['pos'] -= displacement

                        # Update positions using Verlet integration
                        loc1['pos'] += (loc1['pos'] - loc1['prev_pos']) * damping
                        loc2['pos'] += (loc2['pos'] - loc2['prev_pos']) * damping

                        loc1['prev_pos'] = loc1['pos'] - displacement
                        loc2['prev_pos'] = loc2['pos'] + displacement

                        # Ensure circles stay within map boundaries
                        loc1['pos'].x = max(min(loc1['pos'].x, map_rect.right - loc1['radius']), map_rect.left + loc1['radius'])
                        loc1['pos'].y = max(min(loc1['pos'].y, map_rect.bottom - loc1['radius']), map_rect.top + loc1['radius'])
                        loc2['pos'].x = max(min(loc2['pos'].x, map_rect.right - loc2['radius']), map_rect.left + loc2['radius'])
                        loc2['pos'].y = max(min(loc2['pos'].y, map_rect.bottom - loc2['radius']), map_rect.top + loc2['radius'])

    # Remove previous position data from the result
    # for location in locations:
    #     location.pop('prev_pos')

    return locations

def draw_debug_locations(locations, target_width, target_height, map_rect):
    scale_x = target_width / map_rect.width
    scale_y = target_height / map_rect.height
    scale = min(scale_x, scale_y)

    surface = pygame.Surface((target_width, target_height), pygame.SRCALPHA)
    # surface.set_alpha(0)
    # surface.fill((255, 255, 255))

    for location in locations:
        pos = location['pos'] - pygame.Vector2(map_rect.topleft)
        pos.x *= scale
        pos.y *= scale
        radius = location['radius'] * scale
        pygame.draw.circle(surface, (255, 255, 255, 255), (pos.x, pos.y), radius, 1)

    return surface

def draw_map(locations, target_width, target_height, map_rect):
    scale_x = target_width / map_rect.width
    scale_y = target_height / map_rect.height
    scale = min(scale_x, scale_y)

    surface = pygame.Surface((target_width, target_height), pygame.SRCALPHA)
    # surface.set_alpha(0)
    # surface.fill((255, 255, 255))

    for location in locations:
        pos = location['pos'] - pygame.Vector2(map_rect.topleft)
        pos.x *= scale
        pos.y *= scale
        radius = location['radius'] * scale
        pygame.draw.circle(surface, (90, 230, 205, 96), (pos.x, pos.y), radius-20)
        pygame.draw.circle(surface, (255, 205, 64, 200), (pos.x, pos.y),  max(20,radius/3))

    return surface



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
