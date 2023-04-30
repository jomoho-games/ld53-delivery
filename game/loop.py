from .game_objects import *
from .physics import *
from .colors import *
import pygame as pg
import math

rad2deg = 180.0/math.pi
deg2rad = math.pi/180.0


def draw_fps(screen, fps, std_font, WIDTH):
    # screen.blit(BG, (0, 0))
    # pg.draw.rect(WIN, BLACK, BORDER)

    fps_text = std_font.render(f"FPS: {fps:.2f}", True, WHITE)
    # yellow_health_text = HEALTH_FONT.render(
    #     f"Health: {yellow_health}", True, YELLOW)

    screen.blit(fps_text, (WIDTH - fps_text.get_width() - 10, 10))
    # screen.blit(yellow_health_text, (10, 10))


def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)


def core_loop(screen, dt, pressed, cam_rect, obj_man, std_font, big_font, WIDTH, HEIGHT, debug_collisions):

    fps = 1.0/dt
    player = None
    if 'player' in obj_man.id_indices:
        player: GameObject = obj_man.objects[obj_man.id_indices["player"]]
        # p = vec(pg.mouse.get_pos()) + vec(cam_rect.topleft)
        # d = (p - vec(player.rect.center))
        # angle = rad2deg * math.atan2(d.x, d.y)
        # l = d.length()
        # if l > 20.0:
        #     d.normalize_ip()
        # else:
        #     d *= dt
        # if not player._collided:
        #     player.velocity = d*(200+(l/3))
        av = 100
        acc = 500
        if pressed[pg.K_DOWN] or pressed[pg.K_s]:
            player.speed -= acc*dt
        if pressed[pg.K_UP] or pressed[pg.K_w]:
            player.speed += acc*dt
        if pressed[pg.K_LEFT] or pressed[pg.K_a]:
            player.angle += av*dt
        if pressed[pg.K_RIGHT] or pressed[pg.K_d]:
            player.angle -= av*dt
        player.speed = min(300, max(-300, player.speed))
        player.speed -= av * dt * math.copysign(1, player.speed)
        player.velocity = vec(math.sin(player.angle*deg2rad),
                              math.cos(player.angle*deg2rad))*player.speed

        cam_rect.center = player.rect.center

    # Clear the screen
    screen.fill(BG_COLOR)

    def draw_object(obj):
        angle = 0
        if not obj.resting and not obj.static:
            angle = rad2deg * math.atan2(obj.velocity.x, obj.velocity.y)
        if hasattr(obj, 'angle'):
            angle = obj.angle
        p = (obj.rect.x-cam_rect.x, obj.rect.y-cam_rect.y)
        lp = vec(obj.rect.centerx-cam_rect.x, obj.rect.centery-cam_rect.y)
        screen.blit(pg.transform.rotate(obj.image, angle), p)
        if debug_collisions:
            pg.draw.line(screen, YELLOW, lp, lp+obj.velocity)
        if hasattr(obj, 'name_txt'):
            screen.blit(obj.name_txt, lp +
                        vec(- obj.name_txt.get_width()/2, -30))
        if obj.t == 'ship' or obj.id == 'player':
            pg.draw.rect(screen, WHITE, pg.Rect(lp.x-16, lp.y-2, 32, 6))
            pg.draw.rect(screen, RED, pg.Rect(
                lp.x-15, lp.y-1, 30*obj.get_health_percentage(), 4))

    # Draw game objects
    for_objects_in_view_rect(obj_man.objects, cam_rect, draw_object)
    if player != None:
        for c in obj_man.cities:
            cp = c['pos']-vec(cam_rect.topleft)
            pp = vec(player.rect.center)-vec(cam_rect.topleft)
            # print(cp,pp)
            dd = cp-pp
            ll = int(dd.length()/10)
            r = WIDTH/20
            dd.normalize_ip()
            pr = pp+(dd*60)
            if debug_collisions:
                pg.draw.line(screen, GREEN, pp, pr)
            if ll > r:
                txt = std_font.render(f"{c['name']}: {ll}", True, WHITE)
                tp = pp+(dd*100)
                tp.x -= txt.get_width()/2
                tp.y -= txt.get_height()/2
                screen.blit(txt, tp)
            # else:
            #     txt = big_font.render(f"{ll}", True, RED)
            #     screen.blit(txt, pp+(dd*70))
        if (player._destroy):
            pg.event.post(pg.event.Event(FADEOUT,  time=2))
            pg.time.set_timer(pg.event.Event(
                CHANGE_GAME_MODE, mode='game_over'), int(2*1000), 1)

    if obj_man.fadeout < obj_man.fadeout_time:  # no player
        prg = 255 * min(1.0, obj_man.fadeout/obj_man.fadeout_time)
        draw_rect_alpha(screen, (BG_COLOR[0], BG_COLOR[1], BG_COLOR[2], prg), pg.Rect(
            0, 0, WIDTH, HEIGHT))
        obj_man.fadeout += dt

    update_objects(obj_man.objects, dt, obj_man.id_indices)

    # Perform Sweep and Prune
    potential_pairs = sweep_and_prune(
        visible_objects_slice(obj_man.objects, cam_rect))

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
            contact.obj_man = obj_man

            obj1.on_collision(obj2, contact)
            obj2.on_collision(obj1, contact)

            if debug_collisions:
                r1 = pg.Rect(obj1.rect.x-cam_rect.x, obj1.rect.y -
                             cam_rect.y, obj1.rect.width, obj1.rect.height)
                r2 = pg.Rect(obj2.rect.x-cam_rect.x, obj2.rect.y -
                             cam_rect.y, obj2.rect.width, obj2.rect.height)
                if pixel_perfect_collision(obj1, obj2):
                    coll_count_pp += 1
                    pg.draw.rect(screen, WHITE, r1, width=1)
                    pg.draw.rect(screen, WHITE, r2, width=1)
                else:
                    pg.draw.rect(screen, RED, r1, width=1)
                    pg.draw.rect(screen, RED, r2, width=1)
        i += 1

    for i, q in enumerate(obj_man.open_quests):
        c = obj_man.cities[q[1]]
        txt = std_font.render(f"{c['name']}: {q[0]['title']}", True, WHITE)
        screen.blit(txt, (WIDTH-250, 50 + 20*i))

    if debug_collisions:
        for obj in obj_man.objects:
            txt = std_font.render(obj.tag, True, YELLOW)
            obj.tag = ""
            screen.blit(
                txt, (obj.rect.x-cam_rect.x, obj.rect.y-cam_rect.y))

    if debug_collisions:
        txt = big_font.render(
            f"obj:{len(obj_man.objects)} pairs:{len(potential_pairs)} coll: {coll_count} coll_pp: {coll_count_pp}", True, GREEN)
        screen.blit(txt, (0, 0))
        txt = big_font.render(
            f"fps: {1.0/dt:.2f} dt: {dt:.4f}", True, GREEN)
        screen.blit(txt, (0, 30))
        draw_fps(screen, fps, std_font, WIDTH)
