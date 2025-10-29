#!/usr/bin/env python3
from game.board_simple import Board

def main():
    board = Board()
    print("=== GAME CỜ VUA HOÀN CHỈNH ===")
    print("Tính năng:")
    print("- Kéo thả quân cờ")
    print("- Phong cấp tốt: e7e8q")
    print("- Các luật cờ vua cơ bản")
    print()
    
    while True:
        board.display()
        print(f"\nLượt: {board.current_player}")
        
        move = input("Nhập nước đi (hoặc 'quit'): ").strip().lower()
        if move == 'quit':
            break
            
        if len(move) >= 4:
            try:
                from_col = ord(move[0]) - ord('a')
                from_row = 8 - int(move[1])
                to_col = ord(move[2]) - ord('a')
                to_row = 8 - int(move[3])
                
                promotion_piece = 'Q'
                if len(move) == 5:
                    promotion_piece = move[4].upper()
                
                result = board.make_move((from_row, from_col), (to_row, to_col), promotion_piece)
                if result:
                    print("✓ Nước đi hợp lệ!")
                else:
                    print("✗ Nước đi không hợp lệ!")
            except Exception as e:
                print(f"✗ Lỗi: {e}")
        else:
            print("✗ Format: e2e4 hoặc e7e8q")

if __name__ == "__main__":
    main()
