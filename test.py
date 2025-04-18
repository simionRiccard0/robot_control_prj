import pygame
import math
import numpy as np

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1200, 675
MENU_HEIGHT = 50
BACKGROUND_COLOR = (255, 255, 255)
MENU_COLOR = (200, 200, 200)
SNAP_DISTANCE = 20
VECTOR_COLOR = (0, 0, 0)
TRASHCAN_COLOR = (255, 0, 0)
BUTTON_COLOR = (150, 150, 150)
VECTOR_LENGTH = 10
TRASHCAN_RECT = pygame.Rect(WIDTH - 100, 10, 80, 30)
EXPORT_BUTTON_RECT = pygame.Rect(WIDTH - 210, 10, 90, 30)
RESET_BUTTON_RECT = pygame.Rect(WIDTH - 320, 10, 90, 30)
UNDO_BUTTON_RECT = pygame.Rect(WIDTH - 430, 10, 90, 30)
REDO_BUTTON_RECT = pygame.Rect(WIDTH - 540, 10, 90, 30)

TRASHCAN_ICON = pygame.image.load("trashcan.png")  # Ensure this image is available
TRASHCAN_ICON = pygame.transform.scale(TRASHCAN_ICON, (30, 30))

# Colors
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 165, 0), (128, 0, 128), (0, 255, 255)]

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tangram Game")

# Load sound effects
snap_sound = pygame.mixer.Sound("snap.mp3")  # Ensure this sound file is available

class Shape:
    def __init__(self, shape_type, center, angle=0):
        self.shape_type = shape_type
        self.center = center
        self.angle = angle
        self.color = COLORS[len(pieces) % len(COLORS)]

    def get_global_points(self):
        points = SHAPES[self.shape_type]["points"]
        rotated_points = self.rotate(points, self.angle)
        cog = self.get_center_of_gravity(rotated_points)
        return [(x - cog[0] + self.center[0], y - cog[1] + self.center[1]) for x, y in rotated_points]

    def rotate(self, points, angle):
        angle_rad = math.radians(angle)
        return [(x * math.cos(angle_rad) - y * math.sin(angle_rad), x * math.sin(angle_rad) + y * math.cos(angle_rad)) for x, y in points]

    def get_center_of_gravity(self, shape_points):
        x_coords = [p[0] for p in shape_points]
        y_coords = [p[1] for p in shape_points]
        return (sum(x_coords) / len(x_coords), sum(y_coords) / len(y_coords))

def extract_counts(shapes):
    counts = {}
    for shape in shapes.keys():
        counts[shape] = shapes[shape]["count"]
    return counts

# Shape library with inherent reference vectors
SHAPES = {
    "triangle_small": {
        "points": [(73.7, 73.7), (73.7, 0), (0, 73.7)],
        "vectors": [(-(VECTOR_LENGTH - 24.57)*np.sin(np.pi/4), (VECTOR_LENGTH - 24.57)*np.cos(np.pi/4)),
        ((VECTOR_LENGTH - 24.57)*np.cos(np.pi/4), (VECTOR_LENGTH - 24.57)*np.sin(np.pi/4))],  # Example vectors for the triangle
        "count": 2
    },
    "triangle_mid": {
        "points": [(104.5, 104.5), (104.5, 0), (0, 104.5)],
        "vectors": [(-(VECTOR_LENGTH - 24.57)*np.sin(np.pi/4), (VECTOR_LENGTH - 24.57)*np.cos(np.pi/4)),
        ((VECTOR_LENGTH - 24.57)*np.cos(np.pi/4), (VECTOR_LENGTH - 24.57)*np.sin(np.pi/4))],  # Example vectors for the triangle
        "count": 1
    },
    "triangle_large": {
        "points": [(147.5, 147.5), (147.5, 0), (0, 147.5)],
        "vectors": [(-(VECTOR_LENGTH - 24.57)*np.sin(np.pi/4), (VECTOR_LENGTH - 24.57)*np.cos(np.pi/4)),
        ((VECTOR_LENGTH - 24.57)*np.cos(np.pi/4), (VECTOR_LENGTH - 24.57)*np.sin(np.pi/4))],  # Example vectors for the triangle
        "count": 2
    },
    "square": {
        "points": [(0, 0), (74, 0), (74, 74), (0, 74)],
        "vectors": [(VECTOR_LENGTH, 0), (0, -VECTOR_LENGTH)],  # Example vectors for the square
        "count": 1
    },
    "parallelogram": {
        "points": [(0 ,52.05), (52.6, 0), (52.6, 100), (0, 152.05)],
        "vectors": [(VECTOR_LENGTH, 0), (0, -VECTOR_LENGTH)],  # Example vectors for the parallelogram
        "count": 1
    }
}

# Define Tangram Pieces (with center reference)
pieces = []
menu_buttons = []
undo_stack = []
redo_stack = []

# Example usage
shape_counts = extract_counts(SHAPES) # Initial count for each shape
selected_piece = None
mouse_offset = (0, 0)

# Create menu buttons for shapes
y_offset = 10
button_width = 150
button_height = 30
button_spacing = 10

for i, shape in enumerate(SHAPES.keys()):
    x_position = 10 + (i * (button_width + button_spacing))
    menu_buttons.append({"shape": shape, "rect": pygame.Rect(x_position, y_offset, button_width, button_height)})

def snap_to_nearest(piece):
    for other_piece in pieces:
        if other_piece == piece:
            continue
        for px, py in piece.get_global_points():
            for ox, oy in other_piece.get_global_points():
                if abs(px - ox) < SNAP_DISTANCE and abs(py - oy) < SNAP_DISTANCE:
                    dx, dy = ox - px, oy - py
                    piece.center = (piece.center[0] + dx, piece.center[1] + dy)
                    snap_sound.play()  # Play snap sound
                    return

def export_layout():
    layout = [{"shape": p.shape_type, "center": p.center, "angle": p.angle} for p in pieces]
    print("Tangram Layout:")
    for item in layout:
        print(item)

def undo():
    if undo_stack:
        action = undo_stack.pop()
        redo_stack.append(action)
        if action["type"] == "add":
            pieces.remove(action["piece"])
            shape_counts[action["piece"].shape_type] += 1
        elif action["type"] == "remove":
            pieces.append(action["piece"])
            shape_counts[action["piece"].shape_type] -= 1

def redo():
    if redo_stack:
        action = redo_stack.pop()
        undo_stack.append(action)
        if action["type"] == "add":
            pieces.append(action["piece"])
            shape_counts[action["piece"].shape_type] -= 1
        elif action["type"] == "remove":
            pieces.remove(action["piece"])
            shape_counts[action["piece"].shape_type] += 1

running = True

while running:
    screen.fill(BACKGROUND_COLOR)
    pygame.draw.rect(screen, MENU_COLOR, (0, 0, WIDTH, MENU_HEIGHT))
    pygame.draw.rect(screen, TRASHCAN_COLOR, TRASHCAN_RECT)
    screen.blit(TRASHCAN_ICON, (TRASHCAN_RECT.x + 25, TRASHCAN_RECT.y))
    pygame.draw.rect(screen, BUTTON_COLOR, EXPORT_BUTTON_RECT)
    pygame.draw.rect(screen, BUTTON_COLOR, RESET_BUTTON_RECT)
    pygame.draw.rect(screen, BUTTON_COLOR, UNDO_BUTTON_RECT)
    pygame.draw.rect(screen, BUTTON_COLOR, REDO_BUTTON_RECT)

    font = pygame.font.Font(None, 24)
    screen.blit(font.render("Export", True, (0, 0, 0)), (EXPORT_BUTTON_RECT.x + 20, EXPORT_BUTTON_RECT.y + 5))
    screen.blit(font.render("Reset", True, (0, 0, 0)), (RESET_BUTTON_RECT.x + 20, RESET_BUTTON_RECT.y + 5))
    screen.blit(font.render("Undo", True, (0, 0, 0)), (UNDO_BUTTON_RECT.x + 20, UNDO_BUTTON_RECT.y + 5))
    screen.blit(font.render("Redo", True, (0, 0, 0)), (REDO_BUTTON_RECT.x + 20, REDO_BUTTON_RECT.y + 5))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if EXPORT_BUTTON_RECT.collidepoint(event.pos):
                export_layout()
            elif RESET_BUTTON_RECT.collidepoint(event.pos):
                pieces.clear()
                undo_stack.clear()
                redo_stack.clear()
                shape_counts = extract_counts(SHAPES)
            elif UNDO_BUTTON_RECT.collidepoint(event.pos):
                undo()
            elif REDO_BUTTON_RECT.collidepoint(event.pos):
                redo()
            else:
                for button in menu_buttons:
                    if button['rect'].collidepoint(event.pos) and shape_counts[button['shape']] > 0:
                        new_piece = Shape(button['shape'], (WIDTH // 2, HEIGHT // 2))
                        pieces.append(new_piece)
                        undo_stack.append({"type": "add", "piece": new_piece})
                        redo_stack.clear()
                        shape_counts[button['shape']] -= 1

                for piece in pieces:
                    polygon = piece.get_global_points()
                    if pygame.draw.polygon(screen, piece.color, polygon).collidepoint(event.pos):
                        selected_piece = piece
                        mouse_offset = (event.pos[0] - piece.center[0], event.pos[1] - piece.center[1])
                        break
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and selected_piece:
                snap_to_nearest(selected_piece)
                if TRASHCAN_RECT.collidepoint(selected_piece.center):
                    undo_stack.append({"type": "remove", "piece": selected_piece})
                    redo_stack.clear()
                    shape_counts[selected_piece.shape_type] += 1
                    pieces.remove(selected_piece)
                selected_piece = None
        elif event.type == pygame.MOUSEMOTION and selected_piece:
            selected_piece.center = (event.pos[0] - mouse_offset[0], event.pos[1] - mouse_offset[1])
        elif event.type == pygame.KEYDOWN and selected_piece:
            if event.key == pygame.K_LEFT:  # Rotate left (counterclockwise)
                selected_piece.angle -= 15
            elif event.key == pygame.K_RIGHT:  # Rotate right (clockwise)
                selected_piece.angle += 15
            elif event.key == pygame.K_r:  # Reset rotation
                selected_piece.angle = 0

    # Draw pieces
    for piece in pieces:
        if selected_piece == piece:
            glow_color = (255, 255, 0)  # Light yellow for glow
            glow_thickness = 5  # Glow thickness
            for i in range(3):  # Draw multiple times with larger size to simulate a glow
                pygame.draw.polygon(screen, glow_color, piece.get_global_points(), width=glow_thickness + i)

        pygame.draw.polygon(screen, piece.color, piece.get_global_points())

        center_x, center_y = piece.center
        reference_vectors = SHAPES[piece.shape_type]["vectors"]
        rotated_vectors = [piece.rotate([v], piece.angle)[0] for v in reference_vectors]

        for vector in rotated_vectors:
            pygame.draw.line(screen, VECTOR_COLOR, (center_x, center_y), (center_x + vector[0], center_y + vector[1]), 2)

    # Draw menu buttons
    for button in menu_buttons:
        pygame.draw.rect(screen, BUTTON_COLOR, button['rect'])
        shape_text = f"{button['shape']} ({shape_counts[button['shape']]})"
        screen.blit(font.render(shape_text, True, (0, 0, 0)), (button['rect'].x + 10, button['rect'].y + 5))

    pygame.display.flip()

pygame.quit()
