import pygame
from cfg import WIDTH, HEIGHT, BACKGROUND_COLOR, MENU_COLOR, TRASHCAN_COLOR, BUTTON_COLOR, TRASHCAN_RECT, EXPORT_BUTTON_RECT, RESET_BUTTON_RECT, UNDO_BUTTON_RECT, REDO_BUTTON_RECT
from shapes import Shape, extract_counts, SHAPES

def pygame_init():
	pygame.init()
	cfg.font = pygame.font.Font(None, 24)
	COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 165, 0), (128, 0, 128), (0, 255, 255)]
	cfg.screen = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption("Tangram Game")

def init():
	pass


# Initialize pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tangram Game")

# Load assets
TRASHCAN_ICON = pygame.image.load("trashcan.png")  # Ensure this image is available
TRASHCAN_ICON = pygame.transform.scale(TRASHCAN_ICON, (30, 30))
snap_sound = pygame.mixer.Sound("snap.wav")  # Ensure this sound file is available

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
