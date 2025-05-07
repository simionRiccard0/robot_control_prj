#cfg.py
import pygame

# Configuration file for constants and settings

# IP Address
ip_address = "192.168.65.164"
trgt_port = 8888

# Placing coordinates
LOWER_COORD = (284, -350) #x, y
HIGHER_COORD = (544, 25) #x, y for the robot
TZ = 50 #mm
RX = 3.12 #rad
RY = -0.386 #rad
RZ = 0 #rad
SHAPE_0 = [1, 
			1, 
			TZ, 
			RX, 
			RY, 
			RZ]


# Screen dimensions
MENU_HEIGHT = 50
WIDTH, HEIGHT = 1300, (910+MENU_HEIGHT)

# Colors
BACKGROUND_COLOR = (255, 255, 255)
MENU_COLOR = (200, 200, 200)
SNAP_DISTANCE = 20
VECTOR_COLOR = (0, 0, 0)
TRASHCAN_COLOR = (255, 0, 0)
BUTTON_COLOR = (150, 150, 150)
VECTOR_LENGTH = 15


# Rectangles for UI elements
TRASHCAN_RECT = pygame.Rect(WIDTH - 100, 10, 80, 30)
EXPORT_BUTTON_RECT = pygame.Rect(WIDTH - 210, 10, 90, 30)
RESET_BUTTON_RECT = pygame.Rect(WIDTH - 320, 10, 90, 30)
UNDO_BUTTON_RECT = pygame.Rect(WIDTH - 430, 10, 90, 30)
REDO_BUTTON_RECT = pygame.Rect(WIDTH - 540, 10, 90, 30)

# Create menu buttons for shapes
y_offset = 10
button_width = 150
button_height = 30
button_spacing = 10

# Pygame related variables
font = None
screen = None

# Shapes
SHAPES = None
shape_counts =None 
selected_piece = None
mouse_offset = (0, 0)

#Placing plane variables
MM_PIX_RATIO = None
PIX_MM_RATIO = None


#Assets
font = None
COLORS = None
TRASHCAN_ICON = None
snap_sound = None

#Pieces
pieces = None
menu_buttons = None
undo_stack = None
redo_stack = None

# Communication
comm_socket = None
thread_list = None
kill_thread_event = None
snd_q = None
rcv_q = None
host = None
port = None
