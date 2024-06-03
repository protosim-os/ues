import time
import threading
import pygame
import psutil

class RealTimeManager:
    def __init__(self):
        self.screen = pygame.display.set_mode((200, 100))
        pygame.display.set_caption("Usage Monitor")
        self.font = pygame.font.Font(None, 24)
        self.running = False

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def stop(self):
        self.running = False
        self.thread.join()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            cpu_usage = psutil.cpu_percent(interval=1)
            memory_info = psutil.virtual_memory()
            self.display_usage(cpu_usage, memory_info)
            time.sleep(1)

    def display_usage(self, cpu_usage, memory_info):
        self.screen.fill((0, 0, 0))  # Clear previous info
        cpu_text = self.font.render(f'CPU Usage: {cpu_usage}%', True, (255, 255, 255))
        mem_text = self.font.render(f'Memory Usage: {memory_info.percent}%', True, (255, 255, 255))
        self.screen.blit(cpu_text, (10, 10))
        self.screen.blit(mem_text, (10, 40))
        pygame.display.flip()
