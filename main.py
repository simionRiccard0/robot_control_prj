import pygame
from init import screen, pieces, menu_buttons, undo_stack, redo_stack, shape_counts, selected_piece, mouse_offset, snap_sound
from cfg import WIDTH, HEIGHT, BACKGROUND_COLOR, MENU_COLOR, TRASHCAN_COLOR, BUTTON_COLOR, TRASHCAN_RECT, EXPORT_BUTTON_RECT, RESET_BUTTON_RECT, UNDO_BUTTON_RECT, REDO_BUTTON_RECT
from shapes import Shape, SHAPES

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
