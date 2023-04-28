import bisect
import timeit
import pygame
from pygame.math import Vector2 as vec
import sys
import random
from operator import attrgetter

pygame.font.init()

# Initialize Pygame
pygame.init()

# Set screen dimensions
screen_width = 800
screen_height = 600
GAME_OBJECT_COUNT = 20000

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 250, 0)

# std_font = pygame.font.Font(pygame.font.get_default_font(),16)
std_font = pygame.font.SysFont('arial', 10)
big_font = pygame.font.SysFont('arial', 30)
# Create a screen
screen = pygame.display.set_mode((screen_width, screen_height))
screen_rect = screen.get_rect()
cam_rect = pygame.Rect(screen_rect)


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


# Initialize ImageManager
image_manager = ImageManager()




# Object class
class GameObject:
    def __init__(self, image_path, x, y, image_manager):
        self.tag = ""
        self.image_path = image_path
        self.image, self.mask = image_manager.load_image(image_path)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.resting = True
        self.velocity = vec(0,0)
        if random.random() > 0.9:
          self.velocity = vec(random.randint(-5, 5) or 5, random.randint(-5, 5) or 5)
          self.velocity.normalize_ip()
        self._collided = False
        self.mass = 1.0
        self.inv_mass = 1.0/self.mass

    def update(self, dt):
        if not self.resting :
            self.rect.x += self.velocity.x*dt
            self.rect.y += self.velocity.y*dt
            self._collided = False

    def on_collision(self, other, contact):
        if self._collided:
            return

        if self.resting:
            self.resting = False
            # self.velocity = vec(random.randint (-5, 5) or 5, random.randint(-5, 5) or 5)
            p = vec(self.rect.center)
            o = vec(other.rect.center)
            d = o-p
            if d == vec(0, 0):
                d = vec(random.randint(-5, 5) or 5, random.randint(-5, 5) or 5)
            self.velocity = d.normalize()
            self.velocity *= -50
        else:
            self.resting = True
            self.cooldown = 10

        self._collided = True

    def __lt__(self, other):
        return self.rect.x < other.rect.x

    def __str__(self):
        return f"GameObject(image_path={self.image_path}, x={self.rect.x}, y={self.rect.y},w={self.rect.width} )"

#Physics:

class Contact:
    def __init__(self, obj1, obj2, normal, restitution=0.5):
        self.obj1 = obj1
        self.obj2 = obj2
        self.normal = normal
        self.restitution = restitution

def calculate_collision_normal(obj1, obj2):
    # Calculate the overlap in the x and y directions
    overlap_x = min(obj1.rect.right, obj2.rect.right) - max(obj1.rect.left, obj2.rect.left)
    overlap_y = min(obj1.rect.bottom, obj2.rect.bottom) - max(obj1.rect.top, obj2.rect.top)

    # Choose the direction with the smallest overlap
    if overlap_x < overlap_y:
        direction = vec(1, 0) if obj1.rect.centerx < obj2.rect.centerx else vec(-1, 0)
    else:
        direction = vec(0, 1) if obj1.rect.centery < obj2.rect.centery else vec(0, -1)

    # Normalize the direction vector to get the collision normal
    direction.normalize_ip()

    return direction
# Load images and create GameObjects
objects = [GameObject("assets/spaceship_red.png", random.randint(0, screen_width*10),
                      random.randint(0, screen_height*10), image_manager) for _ in range(GAME_OBJECT_COUNT)]

objects.sort()


def update_positions(objects, updates):
    for update in updates:
        obj, new_x, new_y = update

        # Remove the object from the sorted list
        index = bisect.bisect_left(objects, obj)
        if index < len(objects) and objects[index] == obj:
            objects.pop(index)
        else:
            raise ValueError("Object not found in sorted list")

        # Update the object's position
        obj.rect.x = new_x
        obj.rect.y = new_y

        # Reinsert the object into the sorted list
        bisect.insort(objects, obj)


def update_objects(objects, dt):
    for index, obj in enumerate(objects):
        if not obj.resting:
            # Remove the object from the sorted list
            objects.pop(index)

            # Update the object's position
            obj.update(dt)

            # Reinsert the object into the sorted list
            bisect.insort(objects, obj)


class XWrapper:
    def __init__(self, x):
        self.rect = pygame.Rect(x, 0, 1, 1)

    def __lt__(self, other):
        return self.rect.x < other.rect.x


def find_first_object_greater_than_x(objects, x):
    return bisect.bisect_left(objects, XWrapper(x))


def for_objects_in_view_rect(objects, view_rect, fn):
    # Find the index of the first object with an x-coordinate larger than the camera rect's left edge
    start_index = find_first_object_greater_than_x(objects, view_rect.left)

    # Iterate over the objects that fit into the camera rect
    for obj in objects[start_index:]:
        # If the object's x-coordinate is greater than the camera rect's right edge, break the loop
        if obj.rect.x > view_rect.right:
            break

        # Check if the object is within the camera rect's vertical bounds (top and bottom)
        if obj.rect.bottom >= view_rect.top and obj.rect.top <= view_rect.bottom:
            # The object fits into the camera rect
            fn(obj)


def find_last_object_less_than_x(objects, x):
    return bisect.bisect_right(objects, XWrapper(x)) - 1


def visible_objects_slice(objects, camera_rect):
    start_index = find_first_object_greater_than_x(objects, camera_rect.left)
    end_index = find_last_object_less_than_x(objects, camera_rect.right)
    horizontal_visible = objects[start_index:end_index + 1]

    return list(filter(lambda obj: obj.rect.bottom >= camera_rect.top and obj.rect.top <= camera_rect.bottom, horizontal_visible))


def visible_objects(objects, camera_rect):
    # Find the index of the first object with an x-coordinate larger than the camera rect's left edge
    start_index = find_first_object_greater_than_x(objects, camera_rect.left)

    visible = []

    # Iterate over the objects that fit into the camera rect
    for obj in objects[start_index:]:
        # If the object's x-coordinate is greater than the camera rect's right edge, break the loop
        if obj.rect.x > camera_rect.right:
            break

        # Check if the object is within the camera rect's vertical bounds (top and bottom)
        if obj.rect.bottom >= camera_rect.top and obj.rect.top <= camera_rect.bottom:
            # The object is visible, add it to the visible list
            visible.append(obj)

    return visible


def compare_slice_performance(objects, camera_rect, num_runs=1000):
    loop_method = timeit.timeit(lambda: visible_objects(
        objects, camera_rect), number=num_runs)
    slice_method = timeit.timeit(lambda: visible_objects_slice(
        objects, camera_rect), number=num_runs)

    print(f"Loop method: {loop_method:.6f} seconds")
    print(f"Slice method: {slice_method:.6f} seconds")

    if loop_method < slice_method:
        print("Loop method is faster")
    elif slice_method < loop_method:
        print("Slice method is faster")
    else:
        print("Both methods have the same performance")


compare_slice_performance(objects, screen_rect)

# Function for AABB collision detection


def aabb_collision(obj1, obj2):
    return obj1.rect.colliderect(obj2.rect)

# Function for pixel-perfect collision detection


def pixel_perfect_collision(obj1, obj2):
    if not aabb_collision(obj1, obj2):
        return False
    offset_x = obj2.rect.x - obj1.rect.x
    offset_y = obj2.rect.y - obj1.rect.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None

# Sweep and Prune implementation


def sweep_and_prune(objects):
    potential_collision_pairs = []

    # Sort objects along the x-axis
    objects_sorted_x = objects

    # Check for overlaps along the x-axis
    active_list = []
    for obj in objects_sorted_x:
        i = 0
        while i < len(active_list):
            active_obj = active_list[i]

            if active_obj.rect.right < obj.rect.left:
                active_list.pop(i)
            else:
                # Check for y-axis overlap
                if not (active_obj.rect.bottom < obj.rect.top or active_obj.rect.top > obj.rect.bottom):
                    potential_collision_pairs.append((active_obj, obj))
                i += 1

        active_list.append(obj)

    return potential_collision_pairs


def sweep_and_prune_view(objects, camera_rect):
    potential_collision_pairs = []

    # Find the index of the first object with an x-coordinate larger than the camera rect's left edge
    start_index = find_first_object_greater_than_x(objects, camera_rect.left)

    # Check for overlaps along the x-axis
    active_list = []
    for obj in objects[start_index:]:
        # If the object's x-coordinate is greater than the camera rect's right edge, break the loop
        if obj.rect.x > camera_rect.right:
            break

        i = 0
        while i < len(active_list):
            active_obj = active_list[i]

            # Check if the active object is still within the camera rect's vertical bounds
            if active_obj.rect.bottom < camera_rect.top or active_obj.rect.top > camera_rect.bottom:
                active_list.pop(i)
                continue

            if active_obj.rect.right < obj.rect.left:
                active_list.pop(i)
            else:
                # Check if the object is within the camera rect's vertical bounds
                if obj.rect.bottom >= camera_rect.top and obj.rect.top <= camera_rect.bottom:
                    potential_collision_pairs.append((active_obj, obj))
                i += 1

        # Add the object to the active list if it's within the camera rect's vertical bounds
        if obj.rect.bottom >= camera_rect.top and obj.rect.top <= camera_rect.bottom:
            active_list.append(obj)

    return potential_collision_pairs


def compare_sweep_and_prune_performance(objects, camera_rect, num_iterations=1000):
    def sweep_and_prune_visible_objects_slice():
        visible = visible_objects_slice(objects, camera_rect)
        return sweep_and_prune(visible)

    view_method = timeit.timeit(lambda: sweep_and_prune_view(
        objects, camera_rect), number=num_iterations)
    slice_method = timeit.timeit(
        sweep_and_prune_visible_objects_slice, number=num_iterations)

    print(f"View method sweep_and_prune_view: {view_method:.6f} seconds")
    print(f"Slice method sweep_and_prune: {slice_method:.6f} seconds")

    if view_method < slice_method:
        print("View method (sweep_and_prune_view) is faster")
    elif slice_method < view_method:
        print("Slice method (sweep_and_prune with visible_objects_slice) is faster")
    else:
        print("Both methods have the same performance")


def time_aabb_collision_checks(potential_pairs, num_iterations=1000):
    start_time = timeit.default_timer()

    for _ in range(num_iterations):
        for pair in potential_pairs:
            aabb_collision(*pair)

    end_time = timeit.default_timer()

    elapsed_time = end_time - start_time
    print(
        f"Elapsed time for {num_iterations} iterations of AABB collision checks: {elapsed_time:.6f} seconds or {(elapsed_time/num_iterations):.6f} s/iteration")


def time_pixel_perfect_collision_checks(potential_pairs, num_iterations=1000):
    start_time = timeit.default_timer()

    for _ in range(num_iterations):
        for pair in potential_pairs:
            pixel_perfect_collision(*pair)

    end_time = timeit.default_timer()

    elapsed_time = end_time - start_time
    print(
        f"Elapsed time for {num_iterations} iterations of pixel-perfect collision checks: {elapsed_time:.6f} seconds or {(elapsed_time/num_iterations):.6f} s/iteration")


# Call the timing functions with your list of objects
def call_timing(num_iterations=100):
    compare_sweep_and_prune_performance(
        objects, screen_rect, num_iterations=num_iterations)
    potential_pairs = sweep_and_prune(objects)
    time_aabb_collision_checks(potential_pairs, num_iterations=num_iterations)
    time_pixel_perfect_collision_checks(
        potential_pairs, num_iterations=num_iterations)


call_timing()

clock = pygame.time.Clock()
debug_collisions = True
show_objects = True
# Main game loop
while True:

    pressed = pygame.key.get_pressed()
    dt = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                objects = [GameObject("assets/spaceship_red.png", random.randint(0, screen_width*10),
                                      random.randint(0, screen_height*10), image_manager) for _ in range(GAME_OBJECT_COUNT)]
                objects.sort()
            if event.key == pygame.K_p:
                compare_slice_performance(objects, cam_rect)
            if event.key == pygame.K_t:
                call_timing()
            if event.key == pygame.K_c:
                debug_collisions = not debug_collisions
            if event.key == pygame.K_h:
                show_objects = not show_objects
            if event.key == pygame.K_PAGEUP:
                GAME_OBJECT_COUNT += 1000
            if event.key == pygame.K_PAGEDOWN:
                GAME_OBJECT_COUNT -= 1000




        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if pressed[pygame.K_DOWN] or pressed[pygame.K_s]:
        cam_rect.y += 10
    if pressed[pygame.K_UP] or pressed[pygame.K_w]:
        cam_rect.y -= 10
    if pressed[pygame.K_LEFT] or pressed[pygame.K_a]:
        cam_rect.x -= 10
    if pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
        cam_rect.x += 10
    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw game objects
    if show_objects:
        for_objects_in_view_rect(objects, cam_rect, lambda obj:
                                 screen.blit(obj.image, (obj.rect.x-cam_rect.x, obj.rect.y-cam_rect.y))
                                 )
    update_objects(objects, dt)

    # Perform Sweep and Prune
    potential_pairs = sweep_and_prune(
        visible_objects_slice(objects, cam_rect))

    # Check for AABB and pixel-perfect collisions
    i = 0
    coll_count = 0
    coll_count_pp = 0
    contacts = []

    for obj1, obj2 in potential_pairs:
        if debug_collisions:
            txt = f"{i},"
            obj1.tag += txt
            obj2.tag += txt

        if aabb_collision(obj1, obj2):
            coll_count += 1
            normal = calculate_collision_normal(obj1, obj2)
            contact = Contact(obj1, obj2, normal)

            obj1.on_collision(obj2, contact)
            obj2.on_collision(obj1, contact)

            if pixel_perfect_collision(obj1, obj2):
                coll_count_pp += 1
            #     if debug_collisions:
            #         pygame.draw.rect(screen, WHITE, obj1.rect, width=1)
            #         pygame.draw.rect(screen, WHITE, obj2.rect, width=1)
            # else:
            #     if debug_collisions:
            #         pygame.draw.rect(screen, RED, obj1.rect, width=1)
            #         pygame.draw.rect(screen, RED, obj2.rect, width=1)
        i += 1

    if debug_collisions:
        for obj in objects:
            txt = std_font.render(obj.tag, True, YELLOW)
            obj.tag = ""
            screen.blit(txt, (obj.rect.x-cam_rect.x, obj.rect.y-cam_rect.y))

    txt = big_font.render(
        f"obj:{len(objects)} pairs:{len(potential_pairs)} coll: {coll_count} coll_pp: {coll_count_pp}", True, GREEN)
    screen.blit(txt, (0, 0))
    txt = big_font.render(
        f"fps: {1.0/dt:.2f} dt: {dt:.4f}", True, GREEN)
    screen.blit(txt, (0, 30))

    pygame.display.update()
