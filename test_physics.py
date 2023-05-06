
import timeit

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
