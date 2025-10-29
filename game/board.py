"""
Bàn cờ vua đơn giản với các tính năng cơ bản
"""

class Board:
    def __init__(self):
        self.board = self.create_initial_board()
        self.current_player = 'white'
        self.move_history = []  # Lưu lịch sử nước đi
    
    def create_initial_board(self):
        """Tạo bàn cờ ban đầu"""
        board = [[None for _ in range(8)] for _ in range(8)]
        
        # Quân đen (hàng 0,1)
        pieces = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        for i in range(8):
            board[0][i] = f'b{pieces[i]}'  # Hàng 8
            board[1][i] = 'bP'  # Tốt đen hàng 7
            board[6][i] = 'wP'  # Tốt trắng hàng 2
            board[7][i] = f'w{pieces[i]}'  # Hàng 1
        
        return board
    
    def display(self):
        """Hiển thị bàn cờ"""
        print("  a b c d e f g h")
        for i in range(8):
            print(f"{8-i} ", end="")
            for j in range(8):
                piece = self.board[i][j]
                print(f"{piece or '.':<2}", end="")
            print(f" {8-i}")
        print("  a b c d e f g h")
    
    def is_valid_pawn_move(self, from_pos, to_pos, color):
        """Kiểm tra nước đi tốt"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        # Trắng đi lên (giảm row), đen đi xuống (tăng row)
        direction = -1 if color == 'w' else 1
        start_row = 6 if color == 'w' else 1
        
        # Di chuyển thẳng
        if from_col == to_col:
            # Di chuyển 1 ô
            if to_row == from_row + direction and not self.board[to_row][to_col]:
                return True
            # Di chuyển 2 ô từ vị trí ban đầu
            if from_row == start_row and to_row == from_row + 2 * direction and not self.board[to_row][to_col]:
                return True
        
        # Ăn chéo
        elif abs(from_col - to_col) == 1 and to_row == from_row + direction:
            if self.board[to_row][to_col]:  # Có quân để ăn
                return True
        
        return False
    
    def is_valid_rook_move(self, from_pos, to_pos):
        """Kiểm tra nước đi xe"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        if from_row != to_row and from_col != to_col:
            return False
        
        return self.is_path_clear(from_pos, to_pos)
    
    def is_valid_knight_move(self, from_pos, to_pos):
        """Kiểm tra nước đi mã"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        row_diff = abs(from_row - to_row)
        col_diff = abs(from_col - to_col)
        
        return (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)
    
    def is_valid_bishop_move(self, from_pos, to_pos):
        """Kiểm tra nước đi tượng"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        if abs(from_row - to_row) != abs(from_col - to_col):
            return False
        
        return self.is_path_clear(from_pos, to_pos)
    
    def is_valid_queen_move(self, from_pos, to_pos):
        """Kiểm tra nước đi hậu"""
        return self.is_valid_rook_move(from_pos, to_pos) or self.is_valid_bishop_move(from_pos, to_pos)
    
    def is_valid_king_move(self, from_pos, to_pos):
        """Kiểm tra nước đi vua"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        return abs(from_row - to_row) <= 1 and abs(from_col - to_col) <= 1
    
    def is_path_clear(self, from_pos, to_pos):
        """Kiểm tra đường đi có bị cản không"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        row_step = 0 if from_row == to_row else (1 if to_row > from_row else -1)
        col_step = 0 if from_col == to_col else (1 if to_col > from_col else -1)
        
        current_row, current_col = from_row + row_step, from_col + col_step
        
        while (current_row, current_col) != (to_row, to_col):
            if self.board[current_row][current_col]:
                return False
            current_row += row_step
            current_col += col_step
        
        return True
    
    def is_valid_move(self, from_pos, to_pos):
        """Kiểm tra nước đi hợp lệ"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        piece = self.board[from_row][from_col]
        target = self.board[to_row][to_col]
        
        if not piece:
            return False
        
        # Không thể ăn quân cùng màu
        if target and piece[0] == target[0]:
            return False
        
        # Kiểm tra lượt đi
        if (piece[0] == 'w' and self.current_player != 'white') or \
           (piece[0] == 'b' and self.current_player != 'black'):
            return False
        
        # Kiểm tra nước đi cơ bản
        if not self.is_valid_move_basic(from_pos, to_pos):
            return False
        
        # Kiểm tra không tự chiếu
        if self.would_be_in_check(from_pos, to_pos, piece[0]):
            return False
        
        return True
    
    def promote_pawn(self, pos, new_piece='Q'):
        """Phong cấp tốt"""
        row, col = pos
        piece = self.board[row][col]
        if piece and piece[1] == 'P':
            color = piece[0]
            self.board[row][col] = f'{color}{new_piece}'
            return True
        return False
    
    def find_king(self, color):
        """Tìm vị trí vua"""
        king = f'{color}K'
        for row in range(8):
            for col in range(8):
                if self.board[row][col] == king:
                    return (row, col)
        return None
    
    def is_square_attacked(self, pos, by_color):
        """Kiểm tra ô có bị tấn công không"""
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece[0] == by_color:
                    if self.can_attack((row, col), pos):
                        return True
        return False
    
    def can_attack(self, from_pos, to_pos):
        """Kiểm tra quân có thể tấn công ô đích không (không tính chiếu)"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        piece = self.board[from_row][from_col]
        if not piece:
            return False
        
        piece_type = piece[1]
        
        if piece_type == 'P':
            # Tốt chỉ tấn công chéo
            direction = -1 if piece[0] == 'w' else 1
            return (to_row == from_row + direction and abs(from_col - to_col) == 1)
        elif piece_type == 'R':
            return self.is_valid_rook_move(from_pos, to_pos)
        elif piece_type == 'N':
            return self.is_valid_knight_move(from_pos, to_pos)
        elif piece_type == 'B':
            return self.is_valid_bishop_move(from_pos, to_pos)
        elif piece_type == 'Q':
            return self.is_valid_queen_move(from_pos, to_pos)
        elif piece_type == 'K':
            return self.is_valid_king_move(from_pos, to_pos)
        
        return False
    
    def is_in_check(self, color):
        """Kiểm tra vua có bị chiếu không"""
        king_pos = self.find_king(color)
        if not king_pos:
            return False
        
        enemy_color = 'b' if color == 'w' else 'w'
        return self.is_square_attacked(king_pos, enemy_color)
    
    def would_be_in_check(self, from_pos, to_pos, color):
        """Kiểm tra nước đi có khiến vua bị chiếu không"""
        # Lưu trạng thái
        piece = self.board[from_pos[0]][from_pos[1]]
        target = self.board[to_pos[0]][to_pos[1]]
        
        # Thực hiện nước đi tạm thời
        self.board[to_pos[0]][to_pos[1]] = piece
        self.board[from_pos[0]][from_pos[1]] = None
        
        # Kiểm tra chiếu
        in_check = self.is_in_check(color)
        
        # Khôi phục trạng thái
        self.board[from_pos[0]][from_pos[1]] = piece
        self.board[to_pos[0]][to_pos[1]] = target
        
        return in_check
    
    def get_all_valid_moves(self, color):
        """Lấy tất cả nước đi hợp lệ"""
        moves = []
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece[0] == color:
                    for to_row in range(8):
                        for to_col in range(8):
                            # Kiểm tra nước đi cơ bản
                            if self.is_valid_move_basic((row, col), (to_row, to_col)):
                                # Kiểm tra không tự chiếu
                                if not self.would_be_in_check((row, col), (to_row, to_col), color):
                                    moves.append(((row, col), (to_row, to_col)))
        return moves
    
    def is_valid_move_basic(self, from_pos, to_pos):
        """Kiểm tra nước đi cơ bản không tính chiếu"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        piece = self.board[from_row][from_col]
        target = self.board[to_row][to_col]
        
        if not piece:
            return False
        
        # Không thể ăn quân cùng màu
        if target and piece[0] == target[0]:
            return False
        
        piece_type = piece[1]
        
        if piece_type == 'P':
            return self.is_valid_pawn_move(from_pos, to_pos, piece[0])
        elif piece_type == 'R':
            return self.is_valid_rook_move(from_pos, to_pos)
        elif piece_type == 'N':
            return self.is_valid_knight_move(from_pos, to_pos)
        elif piece_type == 'B':
            return self.is_valid_bishop_move(from_pos, to_pos)
        elif piece_type == 'Q':
            return self.is_valid_queen_move(from_pos, to_pos)
        elif piece_type == 'K':
            return self.is_valid_king_move(from_pos, to_pos)
        
        return False
    
    def is_checkmate(self, color):
        """Kiểm tra chiếu bí"""
        if not self.is_in_check(color):
            return False
        return len(self.get_all_valid_moves(color)) == 0
    
    def is_stalemate(self, color):
        """Kiểm tra hòa cờ"""
        if self.is_in_check(color):
            return False
        return len(self.get_all_valid_moves(color)) == 0

    def make_move(self, from_pos, to_pos, promotion_piece='Q'):
        """Thực hiện nước đi"""
        try:
            if self.is_valid_move(from_pos, to_pos):
                piece = self.board[from_pos[0]][from_pos[1]]
                target = self.board[to_pos[0]][to_pos[1]]
                
                # Debug info
                from_square = f"{chr(ord('a') + from_pos[1])}{8 - from_pos[0]}"
                to_square = f"{chr(ord('a') + to_pos[1])}{8 - to_pos[0]}"
                print(f"Move {piece} from {from_square} to {to_square}")
                if target:
                    print(f"Capture {target}")
                
                # Lưu nước đi vào lịch sử (trước khi di chuyển)
                self.save_move(from_pos, to_pos, target, piece)
                
                # Thực hiện nước đi
                self.board[to_pos[0]][to_pos[1]] = piece
                self.board[from_pos[0]][from_pos[1]] = None
                
                # Kiểm tra phong cấp tốt
                if piece[1] == 'P':
                    if (piece[0] == 'w' and to_pos[0] == 0) or (piece[0] == 'b' and to_pos[0] == 7):
                        self.promote_pawn(to_pos, promotion_piece)
                        print(f"Pawn promoted to {promotion_piece}")
                
                # Đổi lượt
                self.current_player = 'black' if self.current_player == 'white' else 'white'
                
                # Kiểm tra chiếu bí và hòa cờ
                current_color = 'w' if self.current_player == 'white' else 'b'
                if self.is_checkmate(current_color):
                    winner = 'white' if self.current_player == 'black' else 'black'
                    print(f"CHECKMATE! {winner.upper()} WINS!")
                    return 'checkmate'
                elif self.is_stalemate(current_color):
                    print("STALEMATE! DRAW!")
                    return 'stalemate'
                elif self.is_in_check(current_color):
                    print(f"CHECK! {self.current_player}")
                
                print(f"Next turn: {self.current_player}")
                return True
            else:
                return False
        except Exception as e:
            print(f"Error in make_move: {e}")
            return False
    def save_move(self, from_pos, to_pos, captured_piece, moving_piece):
        """Lưu nước đi vào lịch sử"""
        move_data = {
            'from_pos': from_pos,
            'to_pos': to_pos,
            'piece': moving_piece,  # Quân cờ đang di chuyển
            'captured_piece': captured_piece,  # Quân bị bắt (có thể None)
            'player': self.current_player
        }
        self.move_history.append(move_data)
    
    def undo_last_move(self):
        """Lùi lại nước đi cuối"""
        if not self.move_history:
            return False
        
        # Lấy nước đi cuối
        last_move = self.move_history.pop()
        
        # Khôi phục vị trí
        from_pos = last_move['from_pos']
        to_pos = last_move['to_pos']
        moved_piece = last_move['piece']
        captured_piece = last_move['captured_piece']
        
        # Di chuyển quân về vị trí cũ
        self.board[from_pos[0]][from_pos[1]] = moved_piece
        self.board[to_pos[0]][to_pos[1]] = captured_piece
        
        # Đổi lại lượt
        self.current_player = last_move['player']
        
        return True
    
    def get_fen(self):
        """Trả về FEN string của bàn cờ hiện tại"""
        fen_parts = []
        
        # Board position
        for row in self.board:
            empty_count = 0
            row_str = ""
            for cell in row:
                if cell is None:
                    empty_count += 1
                else:
                    if empty_count > 0:
                        row_str += str(empty_count)
                        empty_count = 0
                    # Chuyển đổi ký hiệu quân cờ
                    piece_map = {
                        'wP': 'P', 'wR': 'R', 'wN': 'N', 'wB': 'B', 'wQ': 'Q', 'wK': 'K',
                        'bP': 'p', 'bR': 'r', 'bN': 'n', 'bB': 'b', 'bQ': 'q', 'bK': 'k'
                    }
                    row_str += piece_map.get(cell, cell)
            
            if empty_count > 0:
                row_str += str(empty_count)
            fen_parts.append(row_str)
        
        board_fen = "/".join(fen_parts)
        
        # Active color
        active_color = "w" if self.current_player == 'white' else "b"
        
        # Castling, en passant, halfmove, fullmove (simplified)
        return f"{board_fen} {active_color} KQkq - 0 1"
