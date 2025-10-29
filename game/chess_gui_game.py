import pygame
import sys
from .board import Board
from .gui import ChessGUI
from .ai_engine import AIEngine
import threading
import time

class ChessGUIGame:
    def __init__(self, ai_mode=False):
        try:
            self.board = Board()
            self.gui = ChessGUI()
            self.clock = pygame.time.Clock()
            self.running = True
            self.waiting_for_promotion = False
            self.promotion_move = None
            
            # AI setup
            self.ai_mode = ai_mode
            self.ai_engine = None
            self.ai_thinking = False
            
            if self.ai_mode:
                print("Initializing AI engine...")
                self.ai_engine = AIEngine()
                if not self.ai_engine.start_engine():
                    print("Failed to start AI engine! Switching to player vs player mode.")
                    self.ai_mode = False
                else:
                    print("AI engine started successfully!")
        except Exception as e:
            print(f"Error initializing game: {e}")
            raise
    
    def make_move(self, from_pos, to_pos, promotion_piece='Q'):
        """Thực hiện nước đi"""
        return self.board.make_move(from_pos, to_pos, promotion_piece)
    
    def make_ai_move(self):
        """AI thực hiện nước đi"""
        if not self.ai_mode or not self.ai_engine or self.ai_thinking:
            return
        
        def ai_move_thread():
            self.ai_thinking = True
            print(f"AI analyzing position... Current player: {self.board.current_player}")
            
            fen = self.board.get_fen()
            print(f"FEN: {fen}")
            
            move_str = self.ai_engine.get_best_move(fen)
            print(f"AI move: {move_str}")
            
            if move_str:
                from_pos, to_pos = self.ai_engine.convert_move_to_coords(move_str)
                print(f"Move coords: {from_pos} -> {to_pos}")
                
                if from_pos and to_pos:
                    result = self.make_move(from_pos, to_pos)
                    print(f"Move result: {result}")
                    
                    if result == 'checkmate':
                        print("AI wins - Checkmate!")
                    elif result == 'stalemate':
                        print("Game Over - Stalemate!")
                else:
                    print("Failed to convert move coordinates")
            else:
                print("AI couldn't find a move")
            
            self.ai_thinking = False
        
        threading.Thread(target=ai_move_thread, daemon=True).start()
    
    def check_promotion(self, from_pos, to_pos):
        """Kiểm tra có cần phong cấp không"""
        piece = self.board.board[from_pos[0]][from_pos[1]]
        if piece and piece[1] == 'P':
            if (piece[0] == 'w' and to_pos[0] == 0) or (piece[0] == 'b' and to_pos[0] == 7):
                return True
        return False
    
    def run(self):
        """Chạy game loop"""
        print("Game started! First turn: white")
        if self.ai_mode:
            print("AI Mode: You are WHITE, AI is BLACK")
        
        while self.running:
            try:
                # Kiểm tra nếu đến lượt AI (đen) và không đang suy nghĩ
                if (self.ai_mode and self.board.current_player == 'black' and 
                    not self.ai_thinking and not self.waiting_for_promotion):
                    print("AI's turn - thinking...")
                    self.make_ai_move()
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:  # Left click
                            # Kiểm tra click vào nút trước
                            button_action = self.gui.handle_button_click(event.pos)
                            if button_action == "exit":
                                self.running = False
                                continue
                            elif button_action == "surrender":
                                if self.ai_mode:
                                    print("You surrendered! AI wins!")
                                    self.running = False
                                continue
                            elif button_action == "undo":
                                # Undo 2 nước (người chơi + AI)
                                if self.ai_mode:
                                    self.board.undo_last_move()  # AI move
                                    self.board.undo_last_move()  # Player move
                                else:
                                    self.board.undo_last_move()  # Player move
                                print("Move undone!")
                                continue
                            
                            # Chỉ cho phép người chơi di chuyển khi không phải lượt AI
                            if self.ai_mode and self.board.current_player == 'black':
                                print("It's AI's turn, please wait...")
                                continue
                                
                            if self.waiting_for_promotion:
                                # Xử lý click trong dialog phong cấp
                                selected_piece = self.gui.handle_promotion_click(event.pos, self.promotion_rects)
                                if selected_piece:
                                    # Thực hiện nước đi với quân được chọn
                                    result = self.make_move(self.promotion_move[0], self.promotion_move[1], selected_piece)
                                    self.waiting_for_promotion = False
                                    self.promotion_move = None
                                    
                                    if result == 'checkmate':
                                        print("Game Over - Checkmate!")
                                    elif result == 'stalemate':
                                        print("Game Over - Stalemate!")
                            else:
                                try:
                                    self.gui.handle_mouse_down(event.pos, self.board.board)
                                except Exception as e:
                                    print(f"Mouse down error: {e}")
                    
                    elif event.type == pygame.MOUSEBUTTONUP:
                        if event.button == 1 and not self.waiting_for_promotion:  # Left click
                            try:
                                if self.gui.dragging and self.gui.selected_square:
                                    target_square = self.gui.get_square_from_pos(event.pos)
                                    if target_square and target_square != self.gui.selected_square:
                                        # Kiểm tra phong cấp trước khi thực hiện nước đi
                                        if self.check_promotion(self.gui.selected_square, target_square):
                                            # Hiển thị dialog chọn quân phong cấp
                                            piece = self.board.board[self.gui.selected_square[0]][self.gui.selected_square[1]]
                                            self.promotion_rects = self.gui.show_promotion_dialog(piece[0])
                                            self.waiting_for_promotion = True
                                            self.promotion_move = (self.gui.selected_square, target_square)
                                        else:
                                            # Thực hiện nước đi bình thường
                                            result = self.make_move(self.gui.selected_square, target_square)
                                            if result == 'checkmate':
                                                print("Game Over - Checkmate!")
                                            elif result == 'stalemate':
                                                print("Game Over - Stalemate!")
                                    
                                    # Reset trạng thái kéo thả
                                    self.gui.dragging = False
                                    self.gui.drag_piece = None
                                    self.gui.selected_square = None
                            except Exception as e:
                                print(f"Mouse up error: {e}")
                    
                    elif event.type == pygame.MOUSEMOTION:
                        if not self.waiting_for_promotion:
                            try:
                                self.gui.handle_mouse_motion(event.pos)
                            except Exception as e:
                                print(f"Mouse motion error: {e}")
                
                # Vẽ game
                try:
                    if self.waiting_for_promotion:
                        # Vẽ board trước, sau đó vẽ dialog
                        self.gui.draw_board(self.board.board)
                        self.gui.draw_pieces(self.board.board)
                        # Vẽ lại dialog
                        piece = self.board.board[self.promotion_move[0][0]][self.promotion_move[0][1]]
                        self.promotion_rects = self.gui.show_promotion_dialog(piece[0])
                    else:
                        self.gui.draw(self.board.board, self.ai_mode, self.board.move_history)
                except Exception as e:
                    print(f"Draw error: {e}")
                
                self.clock.tick(60)
                
            except Exception as e:
                print(f"Game loop error: {e}")
                continue
        
        # Cleanup
        if self.ai_engine:
            self.ai_engine.stop_engine()
        pygame.quit()
        print("Game ended!")
