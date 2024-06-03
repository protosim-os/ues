import pygame

def draw_button(screen, text, rect, color, font):
    pygame.draw.rect(screen, color, rect)
    text_surface = font.render(text, True, (0, 0, 0))
    screen.blit(text_surface, (rect.x + (rect.width - text_surface.get_width()) // 2, rect.y + (rect.height - text_surface.get_height()) // 2))

def visualize_universe(screen, grid, time_step, zoom, offset_x, offset_y, show_grid):
    screen.fill((255, 255, 255))  # White background
    for (x, y), cell in grid.items():
        color = (0, 0, 0)  # Black tiles
        rect = pygame.Rect((x * 10 + 400 + offset_x) * zoom, (y * 10 + 300 + offset_y) * zoom, 10 * zoom, 10 * zoom)
        pygame.draw.rect(screen, color, rect)
        if show_grid:
            pygame.draw.rect(screen, (200, 200, 200), rect, 1)  # Grid lines

    # Display time step
    font = pygame.font.Font(None, 36)
    time_text = font.render(f'Time: {time_step}', True, (0, 0, 0))
    screen.blit(time_text, (10, 10))

    # Calculate universe dimensions
    min_x = min(cell.x for cell in grid.values())
    max_x = max(cell.x for cell in grid.values())
    min_y = min(cell.y for cell in grid.values())
    max_y = max(cell.y for cell in grid.values())
    dimensions_text = f'Width: {max_x - min_x + 1}, Height: {max_y - min_y + 1}'
    dimensions_surface = font.render(dimensions_text, True, (0, 0, 0))
    screen.blit(dimensions_surface, (10, 50))

    # Draw speed control buttons
    button_rects = []
    button_color = (200, 200, 200)
    for i, speed in enumerate(['1', '2', '3', '4', '5', '6']):
        rect = pygame.Rect(10 + i * 60, 100, 50, 30)
        draw_button(screen, speed, rect, button_color, font)
        button_rects.append(rect)
    return button_rects

def display_tile_attributes(screen, grid, mouse_pos, zoom, offset_x, offset_y):
    x, y = (mouse_pos[0] / zoom - 400 - offset_x) // 10, (mouse_pos[1] / zoom - 300 - offset_y) // 10
    if (x, y) in grid:
        cell = grid[(x, y)]
        font = pygame.font.Font(None, 24)
        text_surface = font.render(f'Density: {cell.density:.2f}, Temp: {cell.temperature:.2f}', True, (255, 255, 255))
        screen.blit(text_surface, (mouse_pos[0], mouse_pos[1]))

def draw_pause_menu(screen):
    font = pygame.font.Font(None, 74)
    pause_text = font.render('Paused', True, (0, 0, 0))
    screen.blit(pause_text, (screen.get_width() // 2 - pause_text.get_width() // 2, screen.get_height() // 2 - pause_text.get_height() // 2))
