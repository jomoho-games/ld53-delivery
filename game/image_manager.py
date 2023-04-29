import json
import pygame


class ImageManager:
    def __init__(self):
        self.images = {}
        self.masks = {}

    def load_image(self, image_path):
        if image_path not in self.images:
            image = pygame.image.load(image_path)
            mask = pygame.mask.from_surface(image, threshold=16)
            self.images[image_path] = image
            self.masks[image_path] = mask

        return self.images[image_path], self.masks[image_path]

class SpritesheetManager:
    def __init__(self):
        self.spritesheets = {}
        self.sprites = {}

    def load_spritesheet(self, key, json_file):
        with open(json_file, 'r') as f:
            data = json.load(f)

        spritesheet = pygame.image.load(data['filename']).convert_alpha()
        self.spritesheets[key] = spritesheet
        print(f"SS loaded: {key}: {len(data['sprites'])}")

        sprites = []
        for sprite_data in data['sprites']:
            x, y, width, height = sprite_data['x'], sprite_data['y'], sprite_data['width'], sprite_data['height']
            sprite = pygame.Surface((width, height), pygame.SRCALPHA)
            sprite.blit(spritesheet, (0, 0), (x, y, width, height))
            sprites.append(sprite)


        self.sprites[key] = sprites

    def get_sprite(self, key, index):
        return self.sprites[key][index]
