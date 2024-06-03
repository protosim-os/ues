import pygame
import sqlite3
import threading
from simulator.universe_simulator import UniverseSimulator
from simulator.db_manager import initialize_database, save_universe_to_db, load_universe_from_db
from ui.main_menu import main_menu
from ui.visualization import visualize_universe, display_tile_attributes, draw_pause_menu
from real_time_manager import RealTimeManager

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Universal Evolution Simulator")

initialize_database()

choice = main_menu()
simulator = None
if choice == 'new_game':
    seed = 12345  # Use a default seed
    simulator = UniverseSimulator(seed=seed)
elif choice == 'load_game':
    conn = sqlite3.connect('universe.db')
    cells = load_universe_from_db(conn)
    simulator = UniverseSimulator(seed=12345)  # Adjust this line to load seed if saved
    simulator.grid = cells
    conn.close()

if simulator:
    sim_thread = threading.Thread(target=simulator.run)
    sim_thread.start()

    clock = pygame.time.Clock()
    running = True
    paused = False
    show_grid = True
    zoom = 1
    offset_x, offset_y = 0, 0
    dragging = False
    drag_start_x, drag_start_y = 0, 0

    real_time_manager = RealTimeManager(screen)
    real_time_manager.start()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    dragging = True
                    drag_start_x, drag_start_y = event.pos
                else:
                    mouse_pos = event.pos
                    for i, rect in enumerate(button_rects):
                        if rect.collidepoint(mouse_pos):
                            simulator.set_speed(i + 1)
                            simulator.play()
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging = False
            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    dx = event.pos[0] - drag_start_x
                    dy = event.pos[1] - drag_start_y
                    offset_x += dx
                    offset_y += dy
                    drag_start_x, drag_start_y = event.pos
            elif event.type == pygame.MOUSEWHEEL:
                zoom += event.y * 0.1
                zoom = max(0.1, min(zoom, 5))  # Limit zoom levels
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if simulator.running:
                        simulator.pause()
                    else:
                        simulator.play()
                elif event.key == pygame.K_ESCAPE:
                    paused = not paused
                elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6]:
                    simulator.set_speed(int(event.unicode))
                    simulator.play()
                elif event.key == pygame.K_g:
                    show_grid = not show_grid
        
        if not paused:
            grid = simulator.grid
            button_rects = visualize_universe(screen, grid, simulator.time_step, zoom, offset_x, offset_y, show_grid)
            mouse_pos = pygame.mouse.get_pos()
            display_tile_attributes(screen, grid, mouse_pos, zoom, offset_x, offset_y)
        
        if paused:
            draw_pause_menu(screen)

        pygame.display.flip()
        clock.tick(60)  # Limit the frame rate to 60 FPS

    simulator.pause()
    real_time_manager.stop()
    conn = sqlite3.connect('universe.db')
    save_universe_to_db(conn, simulator.grid)
    conn.close()

pygame.quit()
