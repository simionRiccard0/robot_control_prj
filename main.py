import pygame
from init import init#cfg.screen, cfg.pieces, cfg.menu_buttons, cfg.undo_stack, cfg.redo_stack, cfg.shape_counts, cfg.selected_piece, cfg.mouse_offset, cfg.snap_sound
import cfg
from shapes import Shape, extract_counts
import ur_comm as ur
import threading

def snap_to_nearest(piece):
	for other_piece in cfg.pieces:
		if other_piece == piece:
			continue
		for px, py in piece.get_global_points():
			for ox, oy in other_piece.get_global_points():
				if abs(px - ox) < cfg.SNAP_DISTANCE and abs(py - oy) < cfg.SNAP_DISTANCE:
					dx, dy = ox - px, oy - py
					piece.center = (piece.center[0] + dx, piece.center[1] + dy)
					cfg.snap_sound.play()  # Play snap sound
					return

def piece_to_pose(center, angle):
	# data send = [piece type, piece pose]
	#piece pose : [x, y, z, rx, ry, rz]
	tmp_p =[str(round(center[0]*cfg.MM_PIX_RATIO + cfg.LOWER_COORD[0], 3)).encode('ascii'), 
			str(round((center[1]- cfg.MENU_HEIGHT)*cfg.MM_PIX_RATIO + cfg.LOWER_COORD[1], 3)).encode('ascii'), 
			str(cfg.TZ).encode('ascii'), 
			str(cfg.RX).encode('ascii'), 
			str(cfg.RY).encode('ascii'), 
			str(angle - cfg.RZ).encode('ascii')]
	return tmp_p

def fetch_total_counts(data_dict):
    """
    This function takes a dictionary as input and returns a new dictionary
    containing the 'count' value for each key in the input dictionary.

    :param data_dict: Dictionary with nested 'count' keys.
    :return: Dictionary with 'count' values.
    """
    counts = 0
    for key, value in data_dict.items():
        if isinstance(value, dict) and 'count' in value:
            counts  += value['count']
        else:
            counts  += 0  # or handle the case where 'count' is not present
    return counts

def fetch_counts(data_dict):
    """
    This function takes a dictionary as input and returns a new dictionary
    containing the 'count' value for each key in the input dictionary.

    :param data_dict: Dictionary with nested 'count' keys.
    :return: Dictionary with 'count' values.
    """
    counts = {}
    for key, value in data_dict.items():
        if isinstance(value, dict) and 'count' in value:
            counts[key] = value['count']
    return counts

def export_layout():
	#layout = [piece_to_pose(p.center, p.angle) for p in cfg.pieces]
	layout = [cfg.SHAPE_0]*fetch_total_counts(cfg.SHAPES)

	counts = fetch_counts(cfg.SHAPES)
	small_i = 0
	big_i = 0

	for p in cfg.pieces:
		if p.shape_type == "triangle_mid":
			layout[0] = piece_to_pose(p.center, p.angle)

		elif p.shape_type == "triangle_small":
			layout[1+small_i] = piece_to_pose(p.center, p.angle)
			small_i += 1

		elif p.shape_type == "triangle_big":
			layout[1+big_i] = piece_to_pose(p.center, p.angle)
			big_i += 1

		elif p.shape_type == "square":
			layout[5] = piece_to_pose(p.center, p.angle)

		elif p.shape_type == "parallelogram":
			layout[6] = piece_to_pose(p.center, p.angle)
	print("Tangram Layout:")
	#print(layout)
	#ur.send_data(layout)
	for item in layout:
		print(item)
		ur.send_data(item)

def undo():
	if cfg.undo_stack:
		action = cfg.undo_stack.pop()
		cfg.redo_stack.append(action)
		if action["type"] == "add":
			cfg.pieces.remove(action["piece"])
			cfg.shape_counts[action["piece"].shape_type] += 1
		elif action["type"] == "remove":
			cfg.pieces.append(action["piece"])
			cfg.shape_counts[action["piece"].shape_type] -= 1

def redo():
	if cfg.redo_stack:
		action = cfg.redo_stack.pop()
		cfg.undo_stack.append(action)
		if action["type"] == "add":
			cfg.pieces.append(action["piece"])
			cfg.shape_counts[action["piece"].shape_type] -= 1
		elif action["type"] == "remove":
			cfg.pieces.remove(action["piece"])
			cfg.shape_counts[action["piece"].shape_type] += 1



def app_init():
	init()
	
	#print(cfg.thread_list)
	cfg.kill_thread_event = threading.Event()

	send_thread = threading.Thread(target=ur.send_lp, args=(cfg.host, cfg.port))
	cfg.thread_list.append(send_thread)

	receive_thread = threading.Thread(target=ur.recv_lp, args=(cfg.host, cfg.port))
	cfg.thread_list.append(receive_thread)

	for thread in cfg.thread_list:
		try:
			thread.start()
		except:
			pass
	

def main_loop():
	running = True

	while running:
		cfg.screen.fill(cfg.BACKGROUND_COLOR)
		pygame.draw.rect(cfg.screen, cfg.MENU_COLOR, (0, 0, cfg.WIDTH, cfg.MENU_HEIGHT))
		pygame.draw.rect(cfg.screen, cfg.TRASHCAN_COLOR, cfg.TRASHCAN_RECT)
		cfg.screen.blit(cfg.TRASHCAN_ICON, (cfg.TRASHCAN_RECT.x + 25, cfg.TRASHCAN_RECT.y))
		pygame.draw.rect(cfg.screen, cfg.BUTTON_COLOR, cfg.EXPORT_BUTTON_RECT)
		pygame.draw.rect(cfg.screen, cfg.BUTTON_COLOR, cfg.RESET_BUTTON_RECT)
		pygame.draw.rect(cfg.screen, cfg.BUTTON_COLOR, cfg.UNDO_BUTTON_RECT)
		pygame.draw.rect(cfg.screen, cfg.BUTTON_COLOR, cfg.REDO_BUTTON_RECT)
	
		cfg.screen.blit(cfg.font.render("Export", True, (0, 0, 0)), (cfg.EXPORT_BUTTON_RECT.x + 20, cfg.EXPORT_BUTTON_RECT.y + 5))
		cfg.screen.blit(cfg.font.render("Reset", True, (0, 0, 0)), (cfg.RESET_BUTTON_RECT.x + 20, cfg.RESET_BUTTON_RECT.y + 5))
		cfg.screen.blit(cfg.font.render("Undo", True, (0, 0, 0)), (cfg.UNDO_BUTTON_RECT.x + 20, cfg.UNDO_BUTTON_RECT.y + 5))
		cfg.screen.blit(cfg.font.render("Redo", True, (0, 0, 0)), (cfg.REDO_BUTTON_RECT.x + 20, cfg.REDO_BUTTON_RECT.y + 5))
				
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
				app_exit()
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if cfg.EXPORT_BUTTON_RECT.collidepoint(event.pos):
					export_layout()
				elif cfg.RESET_BUTTON_RECT.collidepoint(event.pos):
					cfg.pieces.clear()
					cfg.undo_stack.clear()
					cfg.redo_stack.clear()
					cfg.shape_counts = extract_counts(cfg.SHAPES)
				elif cfg.UNDO_BUTTON_RECT.collidepoint(event.pos):
					undo()
				elif cfg.REDO_BUTTON_RECT.collidepoint(event.pos):
					redo()
				else:
					for button in cfg.menu_buttons:
						if button['rect'].collidepoint(event.pos) and cfg.shape_counts[button['shape']] > 0:
							new_piece = Shape(button['shape'], (cfg.WIDTH // 2, cfg.HEIGHT // 2))
							cfg.pieces.append(new_piece)
							cfg.undo_stack.append({"type": "add", "piece": new_piece})
							cfg.redo_stack.clear()
							cfg.shape_counts[button['shape']] -= 1
	
					for piece in cfg.pieces:
						polygon = piece.get_global_points()
						if pygame.draw.polygon(cfg.screen, piece.color, polygon).collidepoint(event.pos):
							cfg.selected_piece = piece
							cfg.mouse_offset = (event.pos[0] - piece.center[0], event.pos[1] - piece.center[1])
							break
			elif event.type == pygame.MOUSEBUTTONUP:
				if event.button == 1 and cfg.selected_piece:
					snap_to_nearest(cfg.selected_piece)
					if cfg.TRASHCAN_RECT.collidepoint(cfg.selected_piece.center):
						cfg.undo_stack.append({"type": "remove", "piece": cfg.selected_piece})
						cfg.redo_stack.clear()
						cfg.shape_counts[cfg.selected_piece.shape_type] += 1
						cfg.pieces.remove(cfg.selected_piece)
					cfg.selected_piece = None
			elif event.type == pygame.MOUSEMOTION and cfg.selected_piece:
				cfg.selected_piece.center = (event.pos[0] - cfg.mouse_offset[0], event.pos[1] - cfg.mouse_offset[1])
			elif event.type == pygame.KEYDOWN and cfg.selected_piece:
				if event.key == pygame.K_LEFT:  # Rotate left (counterclockwise)
					cfg.selected_piece.angle -= 15
				elif event.key == pygame.K_RIGHT:  # Rotate right (clockwise)
					cfg.selected_piece.angle += 15
				elif event.key == pygame.K_r:  # Reset rotation
					cfg.selected_piece.angle = 0

		# Draw cfg.pieces
		for piece in cfg.pieces:
			if cfg.selected_piece == piece:
				glow_color = (255, 255, 0)  # Light yellow for glow
				glow_thickness = 5  # Glow thickness
				for i in range(3):  # Draw multiple times with larger size to simulate a glow
					pygame.draw.polygon(cfg.screen, glow_color, piece.get_global_points(), width=glow_thickness + i)

			pygame.draw.polygon(cfg.screen, piece.color, piece.get_global_points())

			center_x, center_y = piece.center
			reference_vectors = cfg.SHAPES[piece.shape_type]["vectors"]
			rotated_vectors = [piece.rotate([v], piece.angle)[0] for v in reference_vectors]
	
			for vector in rotated_vectors:
				pygame.draw.line(cfg.screen, cfg.VECTOR_COLOR, (center_x, center_y), (center_x + vector[0], center_y + vector[1]), 2)

		# Draw menu buttons
		for button in cfg.menu_buttons:
			pygame.draw.rect(cfg.screen, cfg.BUTTON_COLOR, button['rect'])
			shape_text = f"{button['shape']} ({cfg.shape_counts[button['shape']]})"
			cfg.screen.blit(cfg.font.render(shape_text, True, (0, 0, 0)), (button['rect'].x + 10, button['rect'].y + 5))

		pygame.display.flip()

def app_exit():
	cfg.kill_thread_event.set()
	pygame.display.quit()
	pygame.quit()
	for thread in cfg.thread_list:
		thread.join()

if __name__ == "__main__":
	app_init()
	main_loop()
	app_init()