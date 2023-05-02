import pygame
import time
from game.map_gen import *


def draw_locations(locations, target_width, target_height, map_rect):
    scale_x = target_width / map_rect.width
    scale_y = target_height / map_rect.height
    scale = min(scale_x, scale_y)

    surface = pygame.Surface((target_width, target_height))
    surface.fill((255, 255, 255))

    for location in locations:
        pos = location['pos'] - pygame.Vector2(map_rect.topleft)
        pos.x *= scale
        pos.y *= scale
        radius = location['radius'] * scale
        pygame.draw.circle(surface, (0, 0, 255), (pos.x, pos.y), radius, 1)

    return surface


WIDTH, HEIGHT = 1280, 720
mul = 7

MAP_LEFT = int(WIDTH*-mul)
MAP_TOP = int(HEIGHT*-mul)
MAP_RIGHT = int(WIDTH*mul)
MAP_BOTTOM = int(HEIGHT*mul)
MAP_WIDTH = int(WIDTH*2*mul)
MAP_HEIGHT = int(HEIGHT*2*mul)

def main(delay=0.01):
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Circle Locations')

    map_rect = pygame.Rect(
            MAP_LEFT, MAP_TOP, MAP_WIDTH, MAP_HEIGHT)
    num_iterations = 500
    # locations = generate_random_locations(6, map_rect,  WIDTH, WIDTH*5, 1)
    # map_rect = expand_rect_if_needed(map_rect, locations)

    running = True
    iteration = 0
    max_push_strength=0.0001
    damping=0.0001
    first_run = True

    while running:
        for event in pygame.event.get():
          if event.type == pygame.KEYDOWN or first_run:
              first_run = False
              num_iterations = 200
              locations = generate_random_locations(6, map_rect,  WIDTH, WIDTH*5, 1)
              map_rect = expand_rect_if_needed(map_rect, locations)
              iteration = 0

          if event.type == pygame.QUIT:
                running = False

        if iteration < num_iterations:
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

            iteration += 1
            print(iteration)
            time.sleep(delay)

        scaled_map = draw_locations(locations, 800, 600, map_rect)
        screen.blit(scaled_map, (0, 0))
        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main(delay=0.01)
