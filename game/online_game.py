import pygame
import sys
from .board import Board
from .gui import ChessGUI
from .network_client import ChessClient
import threading
import time

class OnlineChessGame:
    def __init__(self, server_ip='localhost'):
        self.board = Board()
        self.gui = ChessGUI()
        self.clock = pygame.time.Clock()
        self.running = True
        self.waiting_for_promotion = False
        self.promotion_move = None
        
        # Network setup
        self.client = ChessClient()
        self.server_ip = server_ip
        self.my_color = None
        self.opponent_connected = False
        self.game_started = False
        
        # Connect to server
        if not self.client.connect(server_ip):
            print("Failed to connect to server!")
            self.running = False
            return
        
        self.client.set_message_callback(self.handle_network_message)
    
    def handle_network_message(self, message):
        """Xử lý tin nhắn từ server"""
        if message['type'] == 'player_info':
            self.my_color = message['color']
            print(f"You are playing as {self.my_color}")
        
        elif message['type'] == 'game_start':
            self.game_started = True
            self.opponent_connected = True
            print("Game started! Both players connected.")
        
        elif message['type'] == 'move':
            # Opponent đã di chuyển
            from_pos = tuple(message['from_pos'])
            to_pos = tuple(message['to_pos'])
            self.board.make_move(from_pos, to_pos)
            print(f"Opponent moved: {from_pos} -> {to_pos}")
        
        elif message['type'] == 'game_over':
            if message['winner'] == 'you':
                print("You won! Opponent surrendered.")
            else:
                print("You lost! Game over.")
    
    def can_move(self):
        """Kiểm tra có thể di chuyển không"""
        if not self.game_started:
            return False
        
        # Chỉ được di chuyển khi đến lượt mình
        current_player_color = 'white' if self.board.current_player == 'white' else 'black'
        return current_player_color == self.my_color
    
    def make_move(self, from_pos, to_pos, promotion_piece='Q'):
        """Thực hiện nước đi"""
        if not self.can_move():
            print("Not your turn!")
            return False
        
        # Thực hiện nước đi local
        result = self.board.make_move(from_pos, to_pos, promotion_piece)
        if result:
            # Gửi nước đi đến server
            self.client.send_move(from_pos, to_pos)
            return result
        return False
    
    def run(self):
        """Chạy game loop"""
        print("Waiting for opponent to connect...")
        
        while self.running:
            try:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:  # Left click
                            # Kiểm tra click vào nút
                            button_action = self.gui.handle_button_click(event.pos)
                            if button_action == "exit":
                                self.running = False
                                continue
                            elif button_action == "surrender":
                                self.client.send_surrender()
                                print("You surrendered!")
                                self.running = False
                                continue
                            elif button_action == "undo":
                                print("Undo not available in online mode")
                                continue
                            
                            # Chỉ cho phép di chuyển khi đến lượt
                            if not self.can_move():
                                print("Wait for your turn or opponent to connect...")
                                continue
                            
                            if self.waiting_for_promotion:
                                # Xử lý promotion
                                selected_piece = self.gui.handle_promotion_click(event.pos, self.promotion_rects)
                                if selected_piece:
                                    result = self.make_move(self.promotion_move[0], self.promotion_move[1], selected_piece)
                                    self.waiting_for_promotion = False
                                    self.promotion_move = None
                            else:
                                try:
                                    self.gui.handle_mouse_down(event.pos, self.board.board)
                                except Exception as e:
                                    print(f"Mouse down error: {e}")
                    
                    elif event.type == pygame.MOUSEBUTTONUP:
                        if event.button == 1 and not self.waiting_for_promotion and self.can_move():
                            try:
                                if self.gui.dragging and self.gui.selected_square:
                                    target_square = self.gui.get_square_from_pos(event.pos)
                                    if target_square and target_square != self.gui.selected_square:
                                        # Kiểm tra promotion
                                        piece = self.board.board[self.gui.selected_square[0]][self.gui.selected_square[1]]
                                        if (piece and piece[1] == 'P' and 
                                            ((piece[0] == 'w' and target_square[0] == 0) or 
                                             (piece[0] == 'b' and target_square[0] == 7))):
                                            # Show promotion dialog
                                            self.promotion_rects = self.gui.show_promotion_dialog(piece[0])
                                            self.waiting_for_promotion = True
                                            self.promotion_move = (self.gui.selected_square, target_square)
                                        else:
                                            # Normal move
                                            self.make_move(self.gui.selected_square, target_square)
                                    
                                    # Reset drag state
                                    self.gui.dragging = False
                                    self.gui.drag_piece = None
                                    self.gui.selected_square = None
                            except Exception as e:
                                print(f"Mouse up error: {e}")
                    
                    elif event.type == pygame.MOUSEMOTION:
                        if not self.waiting_for_promotion and self.can_move():
                            try:
                                self.gui.handle_mouse_motion(event.pos)
                            except Exception as e:
                                print(f"Mouse motion error: {e}")
                
                # Vẽ game
                try:
                    if self.waiting_for_promotion:
                        self.gui.draw_board(self.board.board)
                        self.gui.draw_pieces(self.board.board)
                        piece = self.board.board[self.promotion_move[0][0]][self.promotion_move[0][1]]
                        self.promotion_rects = self.gui.show_promotion_dialog(piece[0])
                    else:
                        self.gui.draw(self.board.board, False, self.board.move_history)
                        
                        # Hiển thị trạng thái game
                        if not self.game_started:
                            font = pygame.font.Font(None, 48)
                            if not self.opponent_connected:
                                text = font.render("Waiting for opponent...", True, (255, 255, 0))
                            else:
                                text = font.render("Game starting...", True, (0, 255, 0))
                            
                            text_rect = text.get_rect(center=(self.gui.screen_width//2, 50))
                            self.gui.screen.blit(text, text_rect)
                        
                        elif self.my_color:
                            # Hiển thị lượt chơi
                            font = pygame.font.Font(None, 32)
                            current_color = self.board.current_player
                            if current_color == self.my_color:
                                turn_text = "Your turn"
                                color = (0, 255, 0)
                            else:
                                turn_text = "Opponent's turn"
                                color = (255, 255, 0)
                            
                            text = font.render(f"{turn_text} ({self.my_color})", True, color)
                            self.gui.screen.blit(text, (self.gui.board_x + self.gui.BOARD_SIZE + 50, self.gui.board_y + 200))
                        
                        pygame.display.flip()
                        
                except Exception as e:
                    print(f"Draw error: {e}")
                
                self.clock.tick(60)
                
            except Exception as e:
                print(f"Game loop error: {e}")
                continue
        
        # Cleanup
        self.client.disconnect()
        pygame.quit()
        print("Game ended!")
