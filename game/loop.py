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


def core_loop(screen, dt, cam_rect, objects, id_indices, cities, std_font, big_font, WIDTH, HEIGHT,debug_collisions):

  fps = 1.0/dt
  player: GameObject = objects[id_indices["player"]]
  p = vec(pg.mouse.get_pos()) + vec(cam_rect.topleft)
  d = (p - vec(player.rect.center))
  angle = rad2deg * math.atan2(d.x, d.y)
  l = d.length()
  if l > 20.0:
      d.normalize_ip()
  else:
      d *= dt
  if not player._collided:
      player.velocity = d*(150+(l/5))
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
          screen.blit(obj.name_txt, lp+vec(0, -30))

  # Draw game objects
  for_objects_in_view_rect(objects, cam_rect, draw_object)

  for c in cities:
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

  update_objects(objects, dt, id_indices)

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

  if debug_collisions:
      for obj in objects:
          txt = std_font.render(obj.tag, True, YELLOW)
          obj.tag = ""
          screen.blit(
              txt, (obj.rect.x-cam_rect.x, obj.rect.y-cam_rect.y))


  if debug_collisions:
      txt = big_font.render(
          f"obj:{len(objects)} pairs:{len(potential_pairs)} coll: {coll_count} coll_pp: {coll_count_pp}", True, GREEN)
      screen.blit(txt, (0, 0))
      txt = big_font.render(
          f"fps: {1.0/dt:.2f} dt: {dt:.4f}", True, GREEN)
      screen.blit(txt, (0, 30))
      draw_fps(screen, fps, std_font, WIDTH)
