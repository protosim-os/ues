import pygame

def main_menu():
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Universal Evolution Simulator")

    font = pygame.font.Font(None, 74)
    new_game_text = font.render('New Game', True, (255, 255, 255))
    load_game_text = font.render('Load Game', True, (255, 255, 255))

    while True:
        screen.fill((0, 0, 0))
        screen.blit(new_game_text, (300, 200))
        screen.blit(load_game_text, (300, 300))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if 300 < mouse_pos[0] < 500:
                    if 200 < mouse_pos[1] < 274:
                        return 'new_game'
                    elif 300 < mouse_pos[1] < 374:
                        return 'load_game'

        pygame.display.flip()
