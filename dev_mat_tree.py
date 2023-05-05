
import sys
import pygame
from pygame.math import Vector2 as vec
from game.alchemy import alchemy_game_data, gather_unique_materials


def create_material_tree(elements, recipes):
    nodes = {}
    edges = []

    # Initialize nodes
    unique_materials = gather_unique_materials(
        {'elements': elements, 'recipes': recipes})
    for material in unique_materials:
        if material in elements:
            nodes[material] = {'level': 0, "inputs": 0}
        else:
            nodes[material] = {'level': 1, "inputs": 0}

    # Populate edges and add new materials to nodes
    for recipe in recipes:
        output = recipe['output']
        inputs = recipe['input']
        nodes[ recipe['output']]['inputs'] = len(inputs)

        for input_element in inputs:
            edges.append({'source': input_element, 'target': output})

    # Update levels
    updated = True
    while updated:
        updated = False
        for edge in edges:
            source_level = nodes[edge['source']]['level']
            target_level = nodes[edge['target']]['level']

            if not target_level > source_level :
                nodes[edge['target']]['level'] = source_level + 1
                updated = True

    return {'nodes': nodes, 'edges': edges}


tree = create_material_tree(
    alchemy_game_data['elements'], alchemy_game_data['recipes'])

print(tree)

def find_materials_with_no_inputs(tree, elements):
    materials_with_no_inputs = []

    for material, data in tree['nodes'].items():
        if material not in elements and data['level'] > 0:
            is_target = False
            for edge in tree['edges']:
                if edge['target'] == material:
                    is_target = True
                    break
            
            if not is_target:
                materials_with_no_inputs.append(material)
                
    return materials_with_no_inputs

# Usage example
no_input_materials = find_materials_with_no_inputs(tree, alchemy_game_data['elements'])
print("\nno_input_materials\n")
print(no_input_materials)


def draw_tree(tree, width=1200, height=800, bg_color=(0, 0, 0), font_size=18):
    pygame.init()

    # Create a window
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Material Tree")
    screen.fill(bg_color)

    # Prepare font
    font = pygame.font.Font(None, font_size)

    # Calculate tree depth
    max_depth = max(node['level'] for node in tree['nodes'].values())

    # Calculate horizontal and vertical spacing
    x_spacing = width / (max_depth + 2)
    y_spacing = height /19
    radius = 32

    # Draw nodes and labels
    node_positions = {}
    x_offset = x_spacing

    

    for level in range(max_depth + 1):
        y_offset = y_spacing

        for node, data in tree['nodes'].items():
            if data['level'] == level:
                pygame.draw.circle(screen, (64, 139, 192), (x_offset, y_offset), radius)
                pygame.draw.circle(screen, (55, 55, 55), (x_offset, y_offset), radius, 2)

                node_label = font.render(f"{node}:{data['inputs']}", True, (255, 250, 230))
                screen.blit(node_label, (x_offset - (node_label.get_width() // 2), y_offset - (node_label.get_height() // 2)))

                node_positions[node] = (x_offset, y_offset)
                y_offset += y_spacing

        x_offset += x_spacing


  # Draw edges
    for edge in tree['edges']:
        source_pos = node_positions[edge['source']]+vec(radius,0)
        target_pos = node_positions[edge['target']]+vec(-radius, 0)
        pygame.draw.line(screen, (200, 100, 0), source_pos, target_pos, 2)
        
    # Update display
    pygame.display.update()

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.time.delay(100)

    pygame.quit()
    sys.exit()

def print_level(tree, level):
  print('\nlevel', level)
  print('=========')
  res = []
  for node, data in tree['nodes'].items():
    l = data['level']
    if l == level:
      res.append(node)
  print(len(res),res)
  return res
      
print("materials:", len(tree['nodes']))

for i in range(max(node['level'] for node in tree['nodes'].values())+1):
  print_level(tree, i)
# Usage example
draw_tree(tree)
