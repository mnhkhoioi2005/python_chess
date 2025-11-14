import pygame
import sys

class MainMenu:
    def __init__(self):
        pygame.init()
        
        # Maximize window
        info = pygame.display.Info()
        self.screen_width = info.current_w - 100
        self.screen_height = info.current_h - 100
        
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Chess Game")
        self.clock = pygame.time.Clock()
        
        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (128, 128, 128)
        self.LIGHT_GRAY = (200, 200, 200)
        self.GREEN = (0, 128, 0)
        
        # Fonts
        self.title_font = pygame.font.Font(None, 120)
        self.button_font = pygame.font.Font(None, 60)
        
        # Buttons (centered)
        button_width, button_height = 300, 60
        center_x = self.screen_width // 2
        center_y = self.screen_height // 2
        
        self.vs_player_button_rect = pygame.Rect(center_x - button_width//2, center_y - 120, button_width, button_height)
        self.vs_ai_button_rect = pygame.Rect(center_x - button_width//2, center_y - 40, button_width, button_height)
        self.online_button_rect = pygame.Rect(center_x - button_width//2, center_y + 40, button_width, button_height)
        self.exit_button_rect = pygame.Rect(center_x - button_width//2, center_y + 120, button_width, button_height)
        
    def draw(self):
        self.screen.fill((240, 240, 240))  # Nền xám nhạt
        
        # Title
        title_text = self.title_font.render("CHESS GAME", True, self.BLACK)
        title_rect = title_text.get_rect(center=(self.screen_width//2, self.screen_height//2 - 200))
        self.screen.blit(title_text, title_rect)
        
        # VS Player button
        pygame.draw.rect(self.screen, self.GREEN, self.vs_player_button_rect)
        pygame.draw.rect(self.screen, self.BLACK, self.vs_player_button_rect, 3)
        
        vs_player_text = self.button_font.render("VS PLAYER", True, self.WHITE)
        vs_player_rect = vs_player_text.get_rect(center=self.vs_player_button_rect.center)
        self.screen.blit(vs_player_text, vs_player_rect)
        
        # VS AI button
        pygame.draw.rect(self.screen, (0, 0, 128), self.vs_ai_button_rect)
        pygame.draw.rect(self.screen, self.BLACK, self.vs_ai_button_rect, 3)
        
        vs_ai_text = self.button_font.render("VS AI", True, self.WHITE)
        vs_ai_rect = vs_ai_text.get_rect(center=self.vs_ai_button_rect.center)
        self.screen.blit(vs_ai_text, vs_ai_rect)
        
        # Online button
        pygame.draw.rect(self.screen, (128, 0, 128), self.online_button_rect)
        pygame.draw.rect(self.screen, self.BLACK, self.online_button_rect, 3)
        
        online_text = self.button_font.render("LAN MULTIPLAYER", True, self.WHITE)
        online_rect = online_text.get_rect(center=self.online_button_rect.center)
        self.screen.blit(online_text, online_rect)
        
        # Exit button
        pygame.draw.rect(self.screen, self.GRAY, self.exit_button_rect)
        pygame.draw.rect(self.screen, self.BLACK, self.exit_button_rect, 3)
        
        exit_text = self.button_font.render("EXIT", True, self.WHITE)
        exit_text_rect = exit_text.get_rect(center=self.exit_button_rect.center)
        self.screen.blit(exit_text, exit_text_rect)
        
        pygame.display.flip()
    
    def handle_click(self, pos):
        if self.vs_player_button_rect.collidepoint(pos):
            return "vs_player"
        elif self.vs_ai_button_rect.collidepoint(pos):
            return "vs_ai"
        elif self.online_button_rect.collidepoint(pos):
            return "lan_multiplayer"  # Changed to LAN multiplayer
        elif self.exit_button_rect.collidepoint(pos):
            return "exit"
        return None
    
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    result = self.handle_click(event.pos)
                    if result == "vs_player":
                        return "vs_player"
                    elif result == "vs_ai":
                        return "vs_ai"
                    elif result == "lan_multiplayer":
                        return "lan_multiplayer"
                    elif result == "exit":
                        pygame.quit()
                        sys.exit()
            
            self.draw()
            self.clock.tick(60)
        
        return None
