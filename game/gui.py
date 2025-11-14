import pygame
import sys
import os

class ChessGUI:
    def __init__(self, server_ip=None):
        pygame.init()
        
        # Maximize window setup
        info = pygame.display.Info()
        self.screen_width = info.current_w - 100  # Trừ đi một chút để có viền
        self.screen_height = info.current_h - 100
        
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        
        # Tính toán kích thước bàn cờ dựa trên màn hình (tăng kích thước)
        self.BOARD_SIZE = min(self.screen_width, self.screen_height) - 100  # Giảm margin
        self.MARGIN = 40
        self.SQUARE_SIZE = (self.BOARD_SIZE - 2 * self.MARGIN) // 8
        
        # Căn giữa bàn cờ
        self.board_x = (self.screen_width - self.BOARD_SIZE) // 2
        self.board_y = (self.screen_height - self.BOARD_SIZE) // 2
        
        pygame.display.set_caption("Cờ Vua")
        
        # Server IP for display
        self.server_ip = server_ip
        
        # Màu sắc
        self.WHITE = (240, 217, 181)
        self.BLACK = (181, 136, 99)
        self.HIGHLIGHT = (255, 255, 0, 128)
        self.TEXT_COLOR = (50, 50, 50)
        self.BG_COLOR = (245, 245, 245)
        
        # Quân cờ Unicode (fallback)
        self.pieces_unicode = {
            'wK': '♔', 'wQ': '♕', 'wR': '♖', 'wB': '♗', 'wN': '♘', 'wP': '♙',
            'bK': '♚', 'bQ': '♛', 'bR': '♜', 'bB': '♝', 'bN': '♞', 'bP': '♟'
        }
        
        # Load hình ảnh quân cờ
        self.piece_images = {}
        self.load_piece_images()
        
        # Game control buttons (đặt bên phải bàn cờ)
        button_x = self.board_x + self.BOARD_SIZE + 20
        self.surrender_button = pygame.Rect(button_x, self.board_y + 50, 120, 40)
        self.undo_button = pygame.Rect(button_x, self.board_y + 100, 120, 40)
        
        # Exit button (góc trên phải)
        self.exit_button = pygame.Rect(self.screen_width - 100, 20, 80, 40)
        
        # Colors for buttons
        self.RED = (200, 50, 50)
        self.BLUE = (50, 100, 200)
        self.button_font = pygame.font.Font(None, 24)
        
        # Fonts
        self.piece_font = pygame.font.Font(None, 70)
        self.coord_font = pygame.font.Font(None, 24)
        
        self.selected_square = None
        self.dragging = False
        self.drag_piece = None
        self.drag_pos = (0, 0)
        self.promotion_dialog = None
    
    def load_piece_images(self):
        """Load hình ảnh quân cờ từ thư mục assets"""
        assets_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'pieces')
        
        for piece in self.pieces_unicode.keys():
            image_path = os.path.join(assets_path, f'{piece}.png')
            if os.path.exists(image_path):
                try:
                    image = pygame.image.load(image_path)
                    # Resize về kích thước phù hợp
                    image = pygame.transform.scale(image, (self.SQUARE_SIZE - 10, self.SQUARE_SIZE - 10))
                    self.piece_images[piece] = image
                    print(f"Loaded image for {piece}")
                except pygame.error as e:
                    print(f"Không thể load {piece}.png: {e}")
        
        print(f"Loaded {len(self.piece_images)} piece images")
        
    def draw_board(self, board):
        """Vẽ bàn cờ với tọa độ"""
        # Vẽ nền
        self.screen.fill(self.BG_COLOR)
        
        # Vẽ các ô cờ
        for row in range(8):
            for col in range(8):
                color = self.WHITE if (row + col) % 2 == 0 else self.BLACK
                x = self.board_x + self.MARGIN + col * self.SQUARE_SIZE
                y = self.board_y + self.MARGIN + row * self.SQUARE_SIZE
                rect = pygame.Rect(x, y, self.SQUARE_SIZE, self.SQUARE_SIZE)
                pygame.draw.rect(self.screen, color, rect)
                
                # Highlight ô được chọn
                if self.selected_square == (row, col):
                    s = pygame.Surface((self.SQUARE_SIZE, self.SQUARE_SIZE))
                    s.set_alpha(128)
                    s.fill((255, 255, 0))
                    self.screen.blit(s, (x, y))
        
        # Vẽ tọa độ cột (a-h)
        for col in range(8):
            letter = chr(ord('a') + col)
            text = self.coord_font.render(letter, True, self.TEXT_COLOR)
            x = self.board_x + self.MARGIN + col * self.SQUARE_SIZE + self.SQUARE_SIZE // 2 - text.get_width() // 2
            # Trên và dưới
            self.screen.blit(text, (x, self.board_y + 10))
            self.screen.blit(text, (x, self.board_y + self.BOARD_SIZE - 30))
        
        # Vẽ tọa độ hàng (1-8)
        for row in range(8):
            number = str(8 - row)
            text = self.coord_font.render(number, True, self.TEXT_COLOR)
            y = self.board_y + self.MARGIN + row * self.SQUARE_SIZE + self.SQUARE_SIZE // 2 - text.get_height() // 2
            # Trái và phải
            self.screen.blit(text, (self.board_x + 10, y))
            self.screen.blit(text, (self.board_x + self.BOARD_SIZE - 25, y))
    
    def draw_pieces(self, board):
        """Vẽ quân cờ - ưu tiên hình ảnh, fallback Unicode"""
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece and not (self.dragging and self.selected_square == (row, col)):
                    x = self.board_x + self.MARGIN + col * self.SQUARE_SIZE + self.SQUARE_SIZE // 2
                    y = self.board_y + self.MARGIN + row * self.SQUARE_SIZE + self.SQUARE_SIZE // 2
                    
                    # Vẽ hình ảnh nếu có
                    if piece in self.piece_images:
                        image = self.piece_images[piece]
                        image_rect = image.get_rect(center=(x, y))
                        self.screen.blit(image, image_rect)
                    else:
                        # Fallback về Unicode
                        piece_char = self.pieces_unicode.get(piece, '?')
                        
                        # Tạo shadow effect
                        shadow = self.piece_font.render(piece_char, True, (0, 0, 0))
                        text = self.piece_font.render(piece_char, True, 
                                                    (255, 255, 255) if piece[0] == 'w' else (0, 0, 0))
                        
                        # Vẽ shadow
                        shadow_rect = shadow.get_rect(center=(x + 2, y + 2))
                        self.screen.blit(shadow, shadow_rect)
                        
                        # Vẽ quân cờ
                        text_rect = text.get_rect(center=(x, y))
                        self.screen.blit(text, text_rect)
    
    def draw_dragging_piece(self):
        """Vẽ quân cờ đang kéo - phóng to nhẹ"""
        if self.dragging and self.drag_piece:
            # Vẽ hình ảnh nếu có
            if self.drag_piece in self.piece_images:
                image = self.piece_images[self.drag_piece]
                # Phóng to nhẹ khi kéo (chỉ +10 pixels)
                new_size = self.SQUARE_SIZE - 5
                big_image = pygame.transform.scale(image, (new_size, new_size))
                image_rect = big_image.get_rect(center=self.drag_pos)
                self.screen.blit(big_image, image_rect)
            else:
                # Fallback về Unicode - phóng to nhẹ
                piece_char = self.pieces_unicode.get(self.drag_piece, '?')
                
                # Font lớn hơn một chút (từ 70 lên 75)
                big_font = pygame.font.Font(None, 75)
                shadow = big_font.render(piece_char, True, (0, 0, 0))
                text = big_font.render(piece_char, True, 
                                     (255, 255, 255) if self.drag_piece[0] == 'w' else (0, 0, 0))
                
                # Vẽ shadow
                shadow_rect = shadow.get_rect(center=(self.drag_pos[0] + 2, self.drag_pos[1] + 2))
                self.screen.blit(shadow, shadow_rect)
                
                # Vẽ quân cờ
                text_rect = text.get_rect(center=self.drag_pos)
                self.screen.blit(text, text_rect)
    
    def get_square_from_pos(self, pos):
        """Chuyển tọa độ mouse thành ô cờ với margin"""
        x, y = pos
        # Kiểm tra có trong vùng bàn cờ không
        if x < self.board_x + self.MARGIN or x >= self.board_x + self.MARGIN + 8 * self.SQUARE_SIZE or \
           y < self.board_y + self.MARGIN or y >= self.board_y + self.MARGIN + 8 * self.SQUARE_SIZE:
            return None
        
        col = (x - self.board_x - self.MARGIN) // self.SQUARE_SIZE
        row = (y - self.board_y - self.MARGIN) // self.SQUARE_SIZE
        
        if 0 <= row < 8 and 0 <= col < 8:
            return (row, col)
        return None
    
    def handle_mouse_down(self, pos, board):
        """Xử lý click chuột"""
        square = self.get_square_from_pos(pos)
        if square:
            row, col = square
            piece = board[row][col]
            if piece:
                self.selected_square = square
                self.dragging = True
                self.drag_piece = piece
                self.drag_pos = pos
                return True
        return False
    
    def handle_mouse_up(self, pos, board, game):
        """Xử lý thả chuột"""
        try:
            if self.dragging and self.selected_square:
                target_square = self.get_square_from_pos(pos)
                if target_square and target_square != self.selected_square:
                    # Thực hiện nước đi
                    success = game.make_move(self.selected_square, target_square)
                    if not success:
                        print("Invalid move")
                else:
                    print("Drop piece back to original position or outside board")
        except Exception as e:
            print(f"Error when dropping piece: {e}")
        finally:
            # Luôn reset trạng thái kéo thả
            self.dragging = False
            self.drag_piece = None
            self.selected_square = None
    
    def handle_mouse_motion(self, pos):
        """Xử lý di chuyển chuột"""
        if self.dragging:
            self.drag_pos = pos
    
    def show_promotion_dialog(self, color):
        """Hiển thị dialog chọn quân phong cấp"""
        pieces = ['Q', 'R', 'B', 'N']
        piece_names = ['Hậu', 'Xe', 'Tượng', 'Mã']
        
        # Vẽ overlay
        overlay = pygame.Surface((self.BOARD_SIZE, self.BOARD_SIZE))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Vẽ dialog
        dialog_width = 400
        dialog_height = 150
        dialog_x = (self.BOARD_SIZE - dialog_width) // 2
        dialog_y = (self.BOARD_SIZE - dialog_height) // 2
        
        pygame.draw.rect(self.screen, (255, 255, 255), 
                        (dialog_x, dialog_y, dialog_width, dialog_height))
        pygame.draw.rect(self.screen, (0, 0, 0), 
                        (dialog_x, dialog_y, dialog_width, dialog_height), 2)
        
        # Title
        font = pygame.font.Font(None, 36)
        title = font.render("Chọn quân phong cấp:", True, (0, 0, 0))
        title_rect = title.get_rect(center=(dialog_x + dialog_width//2, dialog_y + 30))
        self.screen.blit(title, title_rect)
        
        # Vẽ các quân để chọn
        piece_size = 60
        start_x = dialog_x + 50
        y = dialog_y + 70
        
        rects = []
        for i, (piece, name) in enumerate(zip(pieces, piece_names)):
            x = start_x + i * 80
            rect = pygame.Rect(x, y, piece_size, piece_size)
            rects.append((rect, piece))
            
            # Vẽ nền
            pygame.draw.rect(self.screen, (240, 240, 240), rect)
            pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)
            
            # Vẽ quân cờ
            piece_key = f'{color}{piece}'
            if piece_key in self.piece_images:
                image = pygame.transform.scale(self.piece_images[piece_key], (piece_size-10, piece_size-10))
                image_rect = image.get_rect(center=rect.center)
                self.screen.blit(image, image_rect)
            else:
                piece_char = self.pieces_unicode.get(piece_key, '?')
                text = self.piece_font.render(piece_char, True, (0, 0, 0))
                text_rect = text.get_rect(center=rect.center)
                self.screen.blit(text, text_rect)
            
            # Tên quân
            name_font = pygame.font.Font(None, 20)
            name_text = name_font.render(name, True, (0, 0, 0))
            name_rect = name_text.get_rect(center=(x + piece_size//2, y + piece_size + 15))
            self.screen.blit(name_text, name_rect)
        
        pygame.display.flip()
        return rects
    
    def handle_promotion_click(self, pos, rects):
        """Xử lý click trong dialog phong cấp"""
        for rect, piece in rects:
            if rect.collidepoint(pos):
                return piece
        return None

    def draw_ip_info(self):
        """Vẽ thông tin IP ở góc trên trái"""
        if self.server_ip:
            font = pygame.font.Font(None, 36)
            
            # Background box
            ip_text = f"Server IP: {self.server_ip}"
            text_surface = font.render(ip_text, True, (255, 255, 255))
            text_rect = text_surface.get_rect()
            
            # Box với padding
            box_rect = pygame.Rect(10, 10, text_rect.width + 20, text_rect.height + 10)
            pygame.draw.rect(self.screen, (0, 0, 0, 180), box_rect)
            pygame.draw.rect(self.screen, (255, 0, 0), box_rect, 2)
            
            # Text
            self.screen.blit(text_surface, (20, 15))
            
            # Share instruction
            share_font = pygame.font.Font(None, 24)
            share_text = share_font.render("Share this IP with your friend", True, (200, 200, 200))
            self.screen.blit(share_text, (20, 45))

    def draw(self, board, ai_mode=False, move_history=None):
        """Vẽ toàn bộ game với hiệu ứng đẹp"""
        self.draw_board(board)
        self.draw_pieces(board)
        self.draw_dragging_piece()
        self.draw_buttons(ai_mode)
        
        # Vẽ thông tin IP
        self.draw_ip_info()
        
        # Vẽ lịch sử nước đi
        if move_history:
            self.draw_move_history(move_history)
        
        # Vẽ viền bàn cờ
        border_rect = pygame.Rect(self.board_x + self.MARGIN - 2, self.board_y + self.MARGIN - 2, 
                                8 * self.SQUARE_SIZE + 4, 8 * self.SQUARE_SIZE + 4)
        pygame.draw.rect(self.screen, (100, 100, 100), border_rect, 2)
        
        pygame.display.flip()
    def draw_move_history(self, move_history):
        """Vẽ lịch sử nước đi"""
        # Vị trí hiển thị lịch sử (bên trái bàn cờ)
        history_x = 20
        history_y = self.board_y + 50
        history_width = 200
        
        # Tiêu đề
        title_font = pygame.font.Font(None, 28)
        title_text = title_font.render("Move History", True, (255, 255, 255))
        self.screen.blit(title_text, (history_x, history_y - 30))
        
        # Vẽ nền cho lịch sử
        history_rect = pygame.Rect(history_x - 10, history_y - 5, history_width, min(len(move_history) * 25 + 10, 400))
        pygame.draw.rect(self.screen, (50, 50, 50), history_rect)
        pygame.draw.rect(self.screen, (100, 100, 100), history_rect, 2)
        
        # Font cho nước đi
        move_font = pygame.font.Font(None, 20)
        
        # Hiển thị các nước đi (10 nước cuối)
        start_idx = max(0, len(move_history) - 15)
        for i, move in enumerate(move_history[start_idx:]):
            move_num = start_idx + i + 1
            
            # Chuyển đổi tọa độ thành ký hiệu cờ
            from_square = f"{chr(ord('a') + move['from_pos'][1])}{8 - move['from_pos'][0]}"
            to_square = f"{chr(ord('a') + move['to_pos'][1])}{8 - move['to_pos'][0]}"
            
            # Tên quân cờ
            piece_names = {
                'P': 'P', 'R': 'R', 'N': 'N', 'B': 'B', 'Q': 'Q', 'K': 'K'
            }
            piece_name = piece_names.get(move['piece'][1], move['piece'][1])
            
            # Hiển thị nước đi
            move_text = f"{move_num}. {piece_name}{from_square}-{to_square}"
            if move['captured_piece']:
                move_text += "x"
            
            color = (255, 255, 255) if move['player'] == 'white' else (200, 200, 200)
            text = move_font.render(move_text, True, color)
            self.screen.blit(text, (history_x, history_y + i * 25))
    
    def draw_buttons(self, ai_mode=False):
        """Vẽ các nút điều khiển"""
        # Nút EXIT (góc trên phải)
        pygame.draw.rect(self.screen, (100, 100, 100), self.exit_button)
        pygame.draw.rect(self.screen, (255, 255, 255), self.exit_button, 2)
        
        exit_text = self.button_font.render("EXIT", True, (255, 255, 255))
        text_rect = exit_text.get_rect(center=self.exit_button.center)
        self.screen.blit(exit_text, text_rect)
        
        # Nút đầu hàng (chỉ hiện khi chơi với AI)
        if ai_mode:
            pygame.draw.rect(self.screen, self.RED, self.surrender_button)
            pygame.draw.rect(self.screen, (0, 0, 0), self.surrender_button, 2)
            
            surrender_text = self.button_font.render("SURRENDER", True, (255, 255, 255))
            text_rect = surrender_text.get_rect(center=self.surrender_button.center)
            self.screen.blit(surrender_text, text_rect)
        
        # Nút undo
        pygame.draw.rect(self.screen, self.BLUE, self.undo_button)
        pygame.draw.rect(self.screen, (0, 0, 0), self.undo_button, 2)
        
        undo_text = self.button_font.render("UNDO", True, (255, 255, 255))
        text_rect = undo_text.get_rect(center=self.undo_button.center)
        self.screen.blit(undo_text, text_rect)
    
    def handle_button_click(self, pos):
        """Xử lý click vào nút"""
        if self.exit_button.collidepoint(pos):
            return "exit"
        elif self.surrender_button.collidepoint(pos):
            return "surrender"
        elif self.undo_button.collidepoint(pos):
            return "undo"
        return None
