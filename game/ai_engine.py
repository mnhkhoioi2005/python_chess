import chess
import chess.engine
import subprocess
import os
import platform

class AIEngine:
    def __init__(self):
        self.engine = None
        
    def start_engine(self):
        try:
            print("Starting Stockfish engine...")
            
            # Tự động phát hiện hệ điều hành và thử các đường dẫn
            import sys
            
            if sys.platform.startswith('win'):
                # Windows
                paths = [
                    "stockfish.exe",
                    r"C:\stockfish\stockfish.exe",
                    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "stockfish", "stockfish-windows-x86-64-avx2.exe")
                ]
            else:
                # Linux/Mac
                paths = [
                    "/usr/games/stockfish",
                    "/usr/bin/stockfish", 
                    "stockfish"
                ]
            
            for path in paths:
                try:
                    print(f"Trying: {path}")
                    self.engine = chess.engine.SimpleEngine.popen_uci(path)
                    print("Stockfish started successfully!")
                    return True
                except Exception as e:
                    print(f"Failed: {e}")
                    continue
            
            print("Could not start Stockfish engine")
            return False
            
        except Exception as e:
            print(f"Failed to start Stockfish: {e}")
            return False
    
    def stop_engine(self):
        if self.engine:
            try:
                self.engine.quit()
            except:
                pass
    
    def get_best_move(self, fen_position):
        if not self.engine:
            return None
        
        try:
            board = chess.Board(fen_position)
            result = self.engine.play(board, chess.engine.Limit(time=0.5))
            return str(result.move)
        except Exception as e:
            print(f"AI move error: {e}")
            return None
    
    def convert_move_to_coords(self, move_str):
        """Chuyển đổi move string (e2e4) thành tọa độ"""
        if not move_str or len(move_str) < 4:
            return None, None
        
        try:
            from_square = move_str[:2]
            to_square = move_str[2:4]
            
            # Chuyển đổi a1-h8 thành (row, col)
            def square_to_coords(square):
                col = ord(square[0]) - ord('a')  # a=0, b=1, ..., h=7
                row = 8 - int(square[1])         # 8=0, 7=1, ..., 1=7
                return (row, col)
            
            from_pos = square_to_coords(from_square)
            to_pos = square_to_coords(to_square)
            
            return from_pos, to_pos
        except Exception as e:
            print(f"Move conversion error: {e}")
            return None, None
