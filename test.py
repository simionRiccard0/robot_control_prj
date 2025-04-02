import pygame
import math
import json

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
MENU_HEIGHT = 50
BACKGROUND_COLOR = (255, 255, 255)
MENU_COLOR = (200, 200, 200)
SNAP_DISTANCE = 20
VECTOR_COLOR = (0, 0, 0)
VECTOR_LENGTH = 50
TRASHCAN_COLOR = (255, 0, 0)
BUTTON_COLOR = (150, 150, 150)
TRASHCAN_RECT = pygame.Rect(WIDTH - 100, 10, 80, 30)
EXPORT_BUTTON_RECT = pygame.Rect(WIDTH - 210, 10, 90, 30)
RESET_BUTTON_RECT = pygame.Rect(WIDTH - 320, 10, 90, 30)

TRASHCAN_ICON = pygame.image.load("trashcan.png")  # Ensure this image is available
TRASHCAN_ICON = pygame.transform.scale(TRASHCAN_ICON, (30, 30))

# Colors
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 165, 0), (128, 0, 128), (0, 255, 255)]

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tangram Game")

# Shape library
SHAPES = {
    "triangle": [(0, 0), (100, 100), (0, 100)],
    "square": [(0, 0), (100, 0), (100, 100), (0, 100)],
    "parallelogram": [(0, 0), (150, 0), (100, 100), (-50, 100)]
}

# Define Tangram Pieces (with center reference)
pieces = []
menu_buttons = []
shape_counts = {shape: 5 for shape in SHAPES}  # Initial count for each shape
selected_piece = None
mouse_offset = (0, 0)

# Create menu buttons for shapes
y_offset = 10
for i, shape in enumerate(SHAPES.keys()):
    menu_buttons.append({"shape": shape, "rect": pygame.Rect(10 + i * 110, y_offset, 100, 30)})

def get_center_of_gravity(shape_points):
    x_coords = [p[0] for p in shape_points]
    y_coords = [p[1] for p in shape_points]
    return (sum(x_coords) / len(x_coords), sum(y_coords) / len(y_coords))

def get_global_points(piece):
    points = SHAPES[piece['shape']]
    rotated_points = rotate(points, piece['angle'])
    cog = get_center_of_gravity(rotated_points)
    return [(x - cog[0] + piece['center'][0], y - cog[1] + piece['center'][1]) for x, y in rotated_points]

def rotate(points, angle):
    angle_rad = math.radians(angle)
    return [(x * math.cos(angle_rad) - y * math.sin(angle_rad), x * math.sin(angle_rad) + y * math.cos(angle_rad)) for x, y in points]

def snap_to_nearest(piece):
    for other_piece in pieces:
        if other_piece == piece:
            continue
        for px, py in get_global_points(piece):
            for ox, oy in get_global_points(other_piece):
                if abs(px - ox) < SNAP_DISTANCE and abs(py - oy) < SNAP_DISTANCE:
                    dx, dy = ox - px, oy - py
                    piece['center'] = (piece['center'][0] + dx, piece['center'][1] + dy)
                    return

def export_layout():
    layout = [{"shape": p['shape'], "center": p['center'], "angle": p['angle']} for p in pieces]
    with open("tangram_layout.json", "w") as f:
        json.dump(layout, f)
    print("Layout exported!")

running = True
while running:
    screen.fill(BACKGROUND_COLOR)
    pygame.draw.rect(screen, MENU_COLOR, (0, 0, WIDTH, MENU_HEIGHT))
    pygame.draw.rect(screen, TRASHCAN_COLOR, TRASHCAN_RECT)
    screen.blit(TRASHCAN_ICON, (TRASHCAN_RECT.x + 25, TRASHCAN_RECT.y))
    pygame.draw.rect(screen, BUTTON_COLOR, EXPORT_BUTTON_RECT)
    pygame.draw.rect(screen, BUTTON_COLOR, RESET_BUTTON_RECT)
    
    font = pygame.font.Font(None, 24)
    screen.blit(font.render("Export", True, (0, 0, 0)), (EXPORT_BUTTON_RECT.x + 20, EXPORT_BUTTON_RECT.y + 5))
    screen.blit(font.render("Reset", True, (0, 0, 0)), (RESET_BUTTON_RECT.x + 20, RESET_BUTTON_RECT.y + 5))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if EXPORT_BUTTON_RECT.collidepoint(event.pos):
                export_layout()
            elif RESET_BUTTON_RECT.collidepoint(event.pos):
                pieces.clear()
            else:
                for button in menu_buttons:
                    if button['rect'].collidepoint(event.pos) and shape_counts[button['shape']] > 0:
                        pieces.append({'shape': button['shape'], 'center': (WIDTH // 2, HEIGHT // 2), 'angle': 0, 'color': COLORS[len(pieces) % len(COLORS)]})
                        shape_counts[button['shape']] -= 1
                
                for piece in pieces:
                    polygon = get_global_points(piece)
                    if pygame.draw.polygon(screen, piece['color'], polygon).collidepoint(event.pos):
                        selected_piece = piece
                        mouse_offset = (event.pos[0] - piece['center'][0], event.pos[1] - piece['center'][1])
                        break
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and selected_piece:
                snap_to_nearest(selected_piece)
                if TRASHCAN_RECT.collidepoint(selected_piece['center']):
                    shape_counts[selected_piece['shape']] += 1
                    pieces.remove(selected_piece)
                selected_piece = None
        elif event.type == pygame.MOUSEMOTION and selected_piece:
            selected_piece['center'] = (event.pos[0] - mouse_offset[0], event.pos[1] - mouse_offset[1])
        elif event.type == pygame.KEYDOWN and selected_piece:
            if event.key == pygame.K_LEFT:  # Rotate left (counterclockwise)
                selected_piece['angle'] -= 15  
            elif event.key == pygame.K_RIGHT:  # Rotate right (clockwise)
                selected_piece['angle'] += 15 
            elif event.key == pygame.K_r:  # Reset rotation
                selected_piece['angle'] = 0  

    
    for piece in pieces:
    # Draw a glowing effect around the selected piece
        if selected_piece == piece:
            glow_color = (255, 255, 0)  # Light yellow for glow
            glow_thickness = 5  # Glow thickness
            for i in range(3):  # Draw multiple times with larger size to simulate a glow
                pygame.draw.polygon(screen, glow_color, get_global_points(piece), width=glow_thickness + i)
    
        # Draw the actual piece (with its color)
        pygame.draw.polygon(screen, piece['color'], get_global_points(piece))
    
        # Draw the reference vectors (rotated with the piece)
        center_x, center_y = piece['center']
        reference_vectors = [
            (0, VECTOR_LENGTH),  # Vector along X (horizontal)
            (VECTOR_LENGTH, 0)   # Vector along Y (vertical)
        ]
        rotated_vectors = [rotate([v], piece['angle'])[0] for v in reference_vectors]
    
        # Draw the rotated vectors
        for vector in rotated_vectors:
            pygame.draw.line(screen, VECTOR_COLOR, (center_x, center_y), (center_x + vector[0], center_y + vector[1]), 2)


    
    for button in menu_buttons:
        pygame.draw.rect(screen, BUTTON_COLOR, button['rect'])
        screen.blit(font.render(button['shape'], True, (0, 0, 0)), (button['rect'].x + 10, button['rect'].y + 5))


    pygame.display.flip()

pygame.quit()
