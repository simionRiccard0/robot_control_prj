import pygame
import cfg
from shapes import init_shapes, init_shapes_size, extract_counts
from ur_comm import tcp_init, sock_init

def pygame_init():
	pygame.init()
	cfg.screen = pygame.display.set_mode((cfg.WIDTH, cfg.HEIGHT))
	pygame.display.set_caption("Tangram Game")

# Load assets
def load_assets():
	cfg.font = pygame.font.Font(None, 24)
	cfg.COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 165, 0), (128, 0, 128), (0, 255, 255)]
	cfg.TRASHCAN_ICON = pygame.image.load("trashcan.png")  # Ensure this image is available
	cfg.TRASHCAN_ICON = pygame.transform.scale(cfg.TRASHCAN_ICON, (30, 30))
	cfg.snap_sound = pygame.mixer.Sound("snap.mp3")  # Ensure this sound file is available

# Define Tangram Pieces (with center reference)
def init_pieces():
	cfg.pieces = []
	cfg.menu_buttons = []
	cfg.undo_stack = []
	cfg.redo_stack = []

# Example usage
def control_init():
	cfg.shape_counts = shapes.extract_counts(SHAPES) # Initial count for each shape
	cfg.selected_piece = None
	cfg.mouse_offset = (0, 0)


def placing_init():
	cfg.MM_PIX_RATIO = (cfg.HIGHER_COORD[1] - cfg.LOWER_COORD[1])/cfg.WIDTH #x & y are reversed between the bot and pygame plan
	#print("coords diff", (cfg.HIGHER_COORD[0] - cfg.LOWER_COORD[0]))
	cfg.PIX_MM_RATIO = 1/cfg.MM_PIX_RATIO
	cfg.HEIGHT = int((cfg.HIGHER_COORD[0] - cfg.LOWER_COORD[0])*cfg.PIX_MM_RATIO) + cfg.MENU_HEIGHT

	print(cfg.HEIGHT)

def init_menu_buttons():
	cfg.shape_counts = extract_counts(cfg.SHAPES)
	cfg.menu_buttons = []
	for i, shape in enumerate(cfg.SHAPES.keys()):
		x_position = 10 + (i * (cfg.button_width + cfg.button_spacing))
		cfg.menu_buttons.append({"shape": shape, "rect": pygame.Rect(x_position, 
																cfg.y_offset, 
																cfg.button_width, 
																cfg.button_height)})

def init():
	pygame_init()
	load_assets()
	placing_init()
	init_shapes_size()
	init_shapes()
	init_pieces()
	init_menu_buttons()
	tcp_init()
	sock_init()