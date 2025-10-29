"""
Game Cờ Vua - Main Entry Point
"""
import pygame
from game.menu import MainMenu
from game.chess_gui_game import ChessGUIGame
from game.online_game import OnlineChessGame
from game.ip_dialog import IPDialog

def get_server_ip():
    """Hiển thị dialog để nhập IP server"""
    pygame.init()
    
    # Tạo màn hình tạm để hiển thị dialog
    info = pygame.display.Info()
    screen_width = info.current_w - 100
    screen_height = info.current_h - 100
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Enter Server IP")
    
    dialog = IPDialog(screen_width, screen_height)
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            
            result = dialog.handle_event(event)
            if result == "ok":
                ip = dialog.get_ip()
                pygame.quit()
                return ip
            elif result == "cancel":
                pygame.quit()
                return None
        
        screen.fill((50, 50, 50))
        dialog.draw(screen)
        pygame.display.flip()
        clock.tick(60)

def main():
    try:
        # Hiển thị menu chính
        menu = MainMenu()
        mode = menu.run()
        
        if mode == "vs_player":
            print("Starting local multiplayer game...")
            game = ChessGUIGame(ai_mode=False)
            game.run()
        elif mode == "vs_ai":
            print("Starting AI game...")
            game = ChessGUIGame(ai_mode=True)
            game.run()
        elif mode == "online":
            print("Starting online game...")
            
            # Hiển thị dialog nhập IP
            server_ip = get_server_ip()
            if server_ip:
                print(f"Connecting to {server_ip}...")
                game = OnlineChessGame(server_ip)
                game.run()
            else:
                print("Online game cancelled.")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
