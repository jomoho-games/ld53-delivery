from game.alchemy import element_colors
import json

def adjust_color(rgb, brightness_factor):
    r, g, b = rgb

    # Clamp the brightness factor between -1 (darker) and 1 (lighter)
    brightness_factor = max(min(brightness_factor, 1), -1)

    if brightness_factor < 0:
        # Darken the color
        r = int(r * (1 + brightness_factor))
        g = int(g * (1 + brightness_factor))
        b = int(b * (1 + brightness_factor))
    else:
        # Lighten the color
        r = int(r + (255 - r) * brightness_factor)
        g = int(g + (255 - g) * brightness_factor)
        b = int(b + (255 - b) * brightness_factor)

    return r, g, b

def col2s(rgb):
    r, g, b = rgb
    return f"rgb({r}, {g}, {b})"

def col2grad(c, f=0.2):
  return f"{col2s(c)},{col2s(adjust_color(c, f))},90"

def txt4bg(rgb):
    r, g, b = rgb

    # Calculate the perceived brightness using the formula: (0.299 * R) + (0.587 * G) + (0.114 * B)
    brightness = (0.299 * r) + (0.587 * g) + (0.114 * b)

    # Use black text for light backgrounds, and white text for dark backgrounds
    if brightness > 127:
        return (0, 0, 0)  # Black text
    else:
        return (255, 255, 255)  # White text

theme = {}
for e in element_colors:
  c = element_colors[e]
  print(e,c)
  hc = adjust_color(c, -0.3)
  theme[f"#{e}"] = {
    "colours":
        {
            "normal_bg": col2grad(c),
            "hovered_bg": col2grad(hc, -0.2),
            "normal_text": col2s(txt4bg(c)),
            "hovered_text": col2s(txt4bg(hc)),
        },
  }
print("")
print(json.dumps(theme))

