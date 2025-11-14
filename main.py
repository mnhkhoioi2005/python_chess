"""
Game Cờ Vua - Main Entry Point
"""
import pygame
from game.menu import MainMenu
from game.chess_gui_game import ChessGUIGame
from game.online_game import OnlineChessGame
from game.lan_menu_integrated import LANMenu
from game.ip_dialog import IPDialog

def get_server_ip():
    """Hiển thị dialog để nhập IP server"""
    import os
    
    # Kiểm tra auto-connect từ environment
    auto_ip = os.environ.get('CHESS_AUTO_IP')
    if auto_ip:
        print(f"Auto-connecting to {auto_ip}")
        return auto_ip
    
    try:
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
            
    except Exception as e:
        print(f"GUI error: {e}")
        print("Falling back to console input...")
        
        # Fallback to console
        print("\n=== ENTER SERVER IP ===")
        ip = input("Server IP (Enter for localhost): ").strip()
        return ip if ip else "localhost"

def main():
    try:
        import os
        
        # Kiểm tra auto-connect từ environment (từ LAN launcher)
        auto_ip = os.environ.get('CHESS_AUTO_IP')
        if auto_ip:
            print(f"Auto-connecting to {auto_ip}...")
            game = OnlineChessGame(auto_ip)
            game.run()
            return
        
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
        elif mode == "lan_multiplayer":
            print("Opening LAN multiplayer menu...")
            # Get screen info from main menu
            info = pygame.display.Info()
            screen_width = info.current_w - 100
            screen_height = info.current_h - 100
            
            lan_menu = LANMenu(screen_width, screen_height)
            result = lan_menu.run()
            
            if result == "back":
                # Return to main menu
                main()
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
