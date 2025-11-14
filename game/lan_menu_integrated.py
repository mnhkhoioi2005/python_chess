import pygame
import sys
import threading
import time
import socket
from game.network_server import ChessServer
from game.online_game import OnlineChessGame
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lan_discovery import LANDiscovery

class LANMenu:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("LAN Chess Game")
        
        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (128, 128, 128)
        self.GREEN = (0, 128, 0)
        self.BLUE = (0, 0, 128)
        self.RED = (255, 0, 0)
        self.ORANGE = (255, 165, 0)
        
        # Fonts
        self.title_font = pygame.font.Font(None, 80)
        self.button_font = pygame.font.Font(None, 50)
        self.text_font = pygame.font.Font(None, 40)
        self.ip_font = pygame.font.Font(None, 60)
        
        # Buttons
        button_width, button_height = 250, 60
        center_x = screen_width // 2
        center_y = screen_height // 2
        
        self.host_button_rect = pygame.Rect(center_x - button_width//2, center_y - 60, button_width, button_height)
        self.join_button_rect = pygame.Rect(center_x - button_width//2, center_y + 20, button_width, button_height)
        self.back_button_rect = pygame.Rect(center_x - button_width//2, center_y + 100, button_width, button_height)
        
        self.servers = []
        self.scanning = False
        self.hosting = False
        self.status_message = ""
        self.local_ip = self.get_local_ip()
        
    def get_local_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "localhost"
    
    def draw(self):
        self.screen.fill((240, 240, 240))
        
        # Title
        title_text = self.title_font.render("LAN MULTIPLAYER", True, self.BLACK)
        title_rect = title_text.get_rect(center=(self.screen_width//2, 80))
        self.screen.blit(title_text, title_rect)
        
        # IP info - Larger and more prominent
        ip_text = self.ip_font.render(f"Your IP: {self.local_ip}", True, self.RED)
        ip_rect = ip_text.get_rect(center=(self.screen_width//2, 150))
        self.screen.blit(ip_text, ip_rect)
        
        # Share instruction
        share_text = self.text_font.render("Share this IP with your friend to connect", True, self.GRAY)
        share_rect = share_text.get_rect(center=(self.screen_width//2, 190))
        self.screen.blit(share_text, share_rect)
        
        # Status message
        if self.status_message:
            status_color = self.ORANGE if self.hosting or self.scanning else self.BLACK
            status_text = self.text_font.render(self.status_message, True, status_color)
            status_rect = status_text.get_rect(center=(self.screen_width//2, 230))
            self.screen.blit(status_text, status_rect)
        
        # Host button
        host_color = self.ORANGE if self.hosting else self.GREEN
        pygame.draw.rect(self.screen, host_color, self.host_button_rect)
        pygame.draw.rect(self.screen, self.BLACK, self.host_button_rect, 3)
        host_text = self.button_font.render("HOST GAME", True, self.WHITE)
        host_rect = host_text.get_rect(center=self.host_button_rect.center)
        self.screen.blit(host_text, host_rect)
        
        # Join button
        join_color = self.ORANGE if self.scanning else self.BLUE
        pygame.draw.rect(self.screen, join_color, self.join_button_rect)
        pygame.draw.rect(self.screen, self.BLACK, self.join_button_rect, 3)
        join_text = self.button_font.render("JOIN GAME", True, self.WHITE)
        join_rect = join_text.get_rect(center=self.join_button_rect.center)
        self.screen.blit(join_text, join_rect)
        
        # Back button
        pygame.draw.rect(self.screen, self.GRAY, self.back_button_rect)
        pygame.draw.rect(self.screen, self.BLACK, self.back_button_rect, 3)
        back_text = self.button_font.render("BACK", True, self.WHITE)
        back_rect = back_text.get_rect(center=self.back_button_rect.center)
        self.screen.blit(back_text, back_rect)
        
        pygame.display.flip()
    
    def host_game(self):
        """Host game và mở bàn cờ"""
        self.hosting = True
        self.status_message = "Starting server... Please wait"
        self.draw()  # Update UI
        
        # Start server in thread
        server_thread = threading.Thread(
            target=self.start_server_thread, 
            args=(self.local_ip, 12345), 
            daemon=True
        )
        server_thread.start()
        
        # Wait for server to start
        time.sleep(1)
        
        self.status_message = "Server ready! Waiting for opponent..."
        self.draw()  # Update UI
        
        # Terminal info
        print("=" * 50)
        print("🎮 HOSTING CHESS GAME")
        print("=" * 50)
        print(f"📍 Your IP Address: {self.local_ip}")
        print(f"🔗 Share this IP with your friend: {self.local_ip}")
        print("✅ Server started successfully!")
        print("🎲 Opening chess board...")
        
        # Open game
        try:
            game = OnlineChessGame(self.local_ip)
            game.run()
        except Exception as e:
            print(f"❌ Host game error: {e}")
        
        print("🏁 Game ended!")
        self.hosting = False
        self.status_message = ""
    
    def start_server_thread(self, host, port):
        """Start server in thread"""
        server = ChessServer(host, port)
        try:
            server.start()
        except Exception as e:
            print(f"Server error: {e}")
    
    def join_game(self):
        """Scan và join game"""
        self.scanning = True
        self.status_message = "Scanning for games on LAN..."
        self.draw()  # Update UI
        
        print("=" * 50)
        print("🔍 JOINING CHESS GAME")
        print("=" * 50)
        print("📡 Scanning for games on LAN...")
        
        discovery = LANDiscovery()
        
        # Scan for servers
        servers = discovery.scan_for_servers(timeout=3)
        self.scanning = False
        
        if not servers:
            self.status_message = "No games found. Enter IP manually"
            self.draw()  # Update UI
            print("❌ No games found on LAN")
            print("💡 You can enter IP manually")
            # Manual IP input
            ip = self.get_manual_ip()
            if ip:
                print(f"🔗 Connecting to {ip}...")
                self.connect_to_game(ip)
        else:
            self.status_message = f"Found {len(servers)} game(s)! Select one"
            self.draw()  # Update UI
            print(f"✅ Found {len(servers)} game(s)!")
            for i, server in enumerate(servers, 1):
                print(f"   {i}. {server['name']} - {server['ip']}")
            # Show server list
            selected_ip = self.show_server_list(servers)
            if selected_ip:
                print(f"🔗 Connecting to {selected_ip}...")
                self.connect_to_game(selected_ip)
        
        self.status_message = ""
    
    def get_manual_ip(self):
        """Simple IP input dialog"""
        ip = ""
        input_active = True
        
        while input_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return ip if ip else "localhost"
                    elif event.key == pygame.K_ESCAPE:
                        return None
                    elif event.key == pygame.K_BACKSPACE:
                        ip = ip[:-1]
                    else:
                        ip += event.unicode
            
            # Draw input dialog
            self.screen.fill((240, 240, 240))
            
            title_text = self.text_font.render("Enter Server IP:", True, self.BLACK)
            title_rect = title_text.get_rect(center=(self.screen_width//2, self.screen_height//2 - 50))
            self.screen.blit(title_text, title_rect)
            
            # Input box
            input_rect = pygame.Rect(self.screen_width//2 - 150, self.screen_height//2, 300, 40)
            pygame.draw.rect(self.screen, self.WHITE, input_rect)
            pygame.draw.rect(self.screen, self.BLACK, input_rect, 2)
            
            ip_text = self.text_font.render(ip, True, self.BLACK)
            self.screen.blit(ip_text, (input_rect.x + 5, input_rect.y + 5))
            
            hint_text = self.text_font.render("Press Enter to connect, Esc to cancel", True, self.GRAY)
            hint_rect = hint_text.get_rect(center=(self.screen_width//2, self.screen_height//2 + 80))
            self.screen.blit(hint_text, hint_rect)
            
            pygame.display.flip()
        
        return None
    
    def show_server_list(self, servers):
        """Show list of found servers"""
        selected = 0
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected = (selected - 1) % len(servers)
                    elif event.key == pygame.K_DOWN:
                        selected = (selected + 1) % len(servers)
                    elif event.key == pygame.K_RETURN:
                        return servers[selected]['ip']
                    elif event.key == pygame.K_ESCAPE:
                        return None
            
            # Draw server list
            self.screen.fill((240, 240, 240))
            
            title_text = self.text_font.render("Select Server:", True, self.BLACK)
            title_rect = title_text.get_rect(center=(self.screen_width//2, 100))
            self.screen.blit(title_text, title_rect)
            
            for i, server in enumerate(servers):
                color = self.GREEN if i == selected else self.WHITE
                y_pos = 200 + i * 60
                
                server_rect = pygame.Rect(self.screen_width//2 - 200, y_pos, 400, 50)
                pygame.draw.rect(self.screen, color, server_rect)
                pygame.draw.rect(self.screen, self.BLACK, server_rect, 2)
                
                server_text = self.text_font.render(f"{server['name']} - {server['ip']}", True, self.BLACK)
                text_rect = server_text.get_rect(center=server_rect.center)
                self.screen.blit(server_text, text_rect)
            
            hint_text = self.text_font.render("Use arrows to select, Enter to connect", True, self.GRAY)
            hint_rect = hint_text.get_rect(center=(self.screen_width//2, self.screen_height - 50))
            self.screen.blit(hint_text, hint_rect)
            
            pygame.display.flip()
    
    def connect_to_game(self, ip):
        """Connect to game"""
        print("🎲 Opening chess board...")
        try:
            game = OnlineChessGame(ip)
            game.run()
            print("🏁 Game ended!")
        except Exception as e:
            print(f"❌ Connection error: {e}")
    
    def handle_click(self, pos):
        if self.host_button_rect.collidepoint(pos):
            return "host"
        elif self.join_button_rect.collidepoint(pos):
            return "join"
        elif self.back_button_rect.collidepoint(pos):
            return "back"
        return None
    
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit"
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    result = self.handle_click(event.pos)
                    if result == "host":
                        self.host_game()
                        return "game_ended"
                    elif result == "join":
                        self.join_game()
                        return "game_ended"
                    elif result == "back":
                        return "back"
            
            self.draw()
            pygame.time.Clock().tick(60)
        
        return None
