
import bisect
import timeit
import pygame as pg
from pygame.math import Vector2 as vec
import sys
import random

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



# def update_positions(objects, updates):
#     for update in updates:
#         obj, new_x, new_y = update

#         # Remove the object from the sorted list
#         index = bisect.bisect_left(objects, obj)
#         if index < len(objects) and objects[index] == obj:
#             objects.pop(index)
#         else:
#             raise ValueError("Object not found in sorted list")

#         # Update the object's position
#         obj.rect.x = new_x
#         obj.rect.y = new_y

#         # Reinsert the object into the sorted list
#         bisect.insort(objects, obj)


class XWrapper:
    def __init__(self, x):
        self.rect = pg.Rect(x, 0, 1, 1)

    def __lt__(self, other):
        return self.rect.x < other.rect.x


def find_first_object_greater_than_x(objects, x):
    return bisect.bisect_left(objects, XWrapper(x))

def for_objects_in_view_rect(objects, view_rect, fn):
    # Find the index of the first object with an x-coordinate larger than the camera rect's left edge
    start_index = max(0,find_first_object_greater_than_x(objects, view_rect.left)-200)

    # Iterate over the objects that fit into the camera rect
    for obj in objects[start_index:]:
        # If the object's x-coordinate is greater than the camera rect's right edge, break the loop
        if obj.rect.left > view_rect.right:
            break

        # Check if any of the object's four corners are within the camera rect
        corners = [
            (obj.rect.left, obj.rect.top),
            (obj.rect.right, obj.rect.top),
            (obj.rect.left, obj.rect.bottom),
            (obj.rect.right, obj.rect.bottom),
        ]

        for corner_x, corner_y in corners:
            if view_rect.collidepoint(corner_x, corner_y):
                # One of the object's corners is within the camera rect
                fn(obj)
                break  # No need to check the other corners, move to the next object

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



# Function for AABB collision detection


def aabb_collision(obj1, obj2):
    return pg.Rect.colliderect(obj1.rect,obj2.rect)

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
def call_timing(objects, rect, num_iterations=100):
    compare_sweep_and_prune_performance(
        objects, rect, num_iterations=num_iterations)
    potential_pairs = sweep_and_prune(objects)
    time_aabb_collision_checks(potential_pairs, num_iterations=num_iterations)
    time_pixel_perfect_collision_checks(
        potential_pairs, num_iterations=num_iterations)
