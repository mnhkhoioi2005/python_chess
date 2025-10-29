#!/usr/bin/env python3
from game.board import Board

def main():
    board = Board()
    print("=== GAME CỜ VUA CONSOLE ===")
    print("Nhập nước đi: e2e4 (từ e2 đến e4)")
    print("Phong cấp tốt: e7e8q (q=hậu, r=xe, b=tượng, n=mã)")
    print("Gõ 'quit' để thoát\n")
    
    while True:
        board.display()
        print(f"\nLượt: {board.current_player}")
        
        # Kiểm tra trạng thái game
        if board.is_checkmate(board.current_player):
            winner = 'white' if board.current_player == 'black' else 'black'
            print(f"CHIẾU BÍ! {winner.upper()} THẮNG!")
            break
        elif board.is_stalemate(board.current_player):
            print("HÒA CỜ!")
            break
        elif board.is_in_check(board.current_player):
            print(f"CHIẾU! {board.current_player}")
        
        move = input("Nhập nước đi: ").strip().lower()
        if move == 'quit':
            break
            
        if len(move) >= 4:
            try:
                from_col = ord(move[0]) - ord('a')
                from_row = 8 - int(move[1])
                to_col = ord(move[2]) - ord('a')
                to_row = 8 - int(move[3])
                
                # Kiểm tra phong cấp
                promotion_piece = 'Q'  # Mặc định là hậu
                if len(move) == 5:
                    promotion_piece = move[4].upper()
                
                result = board.make_move((from_row, from_col), (to_row, to_col), promotion_piece)
                if result == True:
                    print("✓ Nước đi hợp lệ!")
                elif result == 'checkmate':
                    print("✓ Nước đi hợp lệ! CHIẾU BÍ!")
                elif result == 'stalemate':
                    print("✓ Nước đi hợp lệ! HÒA CỜ!")
                else:
                    print("✗ Nước đi không hợp lệ!")
            except:
                print("✗ Format sai! Dùng: e2e4 hoặc e7e8q")
        else:
            print("✗ Format sai! Dùng: e2e4 hoặc e7e8q")

if __name__ == "__main__":
    main()
