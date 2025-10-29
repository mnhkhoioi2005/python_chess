#!/usr/bin/env python3
import os
import sys

def main():
    try:
        # Set display for WSL
        if 'WSL' in os.environ.get('WSL_DISTRO_NAME', ''):
            os.environ['DISPLAY'] = ':0'
        
        from game.chess_gui_game import ChessGUIGame
        
        print("Khởi động game cờ vua...")
        print("Cách chơi:")
        print("- Click và kéo quân cờ để di chuyển")
        print("- Thả chuột để đặt quân")
        print("- Đóng cửa sổ để thoát")
        
        game = ChessGUIGame()
        game.run()
        
    except ImportError as e:
        print(f"Lỗi import: {e}")
        print("Hãy cài pygame: pip install pygame")
    except Exception as e:
        print(f"Lỗi khởi động game: {e}")
        print("Thử chạy version console: python3 test_console.py")

if __name__ == "__main__":
    main()
