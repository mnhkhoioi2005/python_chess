import socket
import threading
import json

class ChessClient:
    def __init__(self):
        self.socket = None
        self.connected = False
        self.player_color = None
        self.player_number = None
        self.message_callback = None
        self.running = False
    
    def connect(self, host='localhost', port=12345):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((host, port))
            self.connected = True
            self.running = True
            print(f"Connected to server at {host}:{port}")
            
            # Start thread để nhận messages
            threading.Thread(target=self.receive_messages, daemon=True).start()
            return True
            
        except Exception as e:
            print(f"Connection failed: {e}")
            return False
    
    def receive_messages(self):
        try:
            while self.running and self.connected:
                data = self.socket.recv(1024).decode()
                if not data:
                    break
                
                message = json.loads(data)
                self.handle_message(message)
                
        except Exception as e:
            print(f"Receive error: {e}")
        finally:
            self.connected = False
    
    def handle_message(self, message):
        if message['type'] == 'player_info':
            self.player_color = message['color']
            self.player_number = message['player_number']
            print(f"You are player {self.player_number} ({self.player_color})")
        
        # Gọi callback nếu có
        if self.message_callback:
            self.message_callback(message)
    
    def send_move(self, from_pos, to_pos):
        if self.connected:
            message = {
                'type': 'move',
                'from_pos': from_pos,
                'to_pos': to_pos,
                'player': self.player_color
            }
            self.send_message(message)
    
    def send_surrender(self):
        if self.connected:
            message = {'type': 'surrender', 'player': self.player_color}
            self.send_message(message)
    
    def send_message(self, message):
        try:
            if self.connected:
                self.socket.send(json.dumps(message).encode())
        except Exception as e:
            print(f"Send error: {e}")
            self.connected = False
    
    def set_message_callback(self, callback):
        self.message_callback = callback
    
    def disconnect(self):
        self.running = False
        self.connected = False
        if self.socket:
            self.socket.close()
