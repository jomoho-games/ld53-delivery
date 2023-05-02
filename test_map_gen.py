from game.map_gen import *

import pygame


def draw_locations(locations, target_width, target_height, map_rect):
    scale_x = target_width / map_rect.width
    scale_y = target_height / map_rect.height
    scale = min(scale_x, scale_y)

    surface = pygame.Surface((target_width, target_height))
    surface.fill((255, 255, 255))

    for location in locations:
        pos = location['pos'] + pygame.Vector2(map_rect.topleft)
        pos.x *= scale
        pos.y *= scale
        radius = location['radius'] * scale
        pygame.draw.circle(surface, (0, 0, 255), (pos.x, pos.y), radius, 1)

    return surface


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Circle Locations')

    map_rect = pygame.Rect(0, 0, 800*10, 600*10)
    # locations = generate_random_locations(20, map_rect, 50, 150, 1000)
    # print(locations)
    first_run = True
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or first_run:
              first_run = False
              locations = generate_random_locations(6, map_rect, 800, 2000, 200)

            if event.type == pygame.QUIT:
                running = False

        scaled_map = draw_locations(locations, 800, 600, map_rect)
        screen.blit(scaled_map, (0, 0))
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
