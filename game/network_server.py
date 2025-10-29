import socket
import threading
import json
import time

class ChessServer:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.game_state = {
            'board': None,
            'current_player': 'white',
            'move_history': []
        }
        self.running = False
    
    def start(self):
        try:
            self.socket.bind((self.host, self.port))
            self.socket.listen(2)
            self.running = True
            print(f"Server started on {self.host}:{self.port}")
            print("Waiting for players...")
            
            while self.running and len(self.clients) < 2:
                client_socket, addr = self.socket.accept()
                self.clients.append(client_socket)
                print(f"Player {len(self.clients)} connected from {addr}")
                
                # Gửi thông tin player
                player_color = 'white' if len(self.clients) == 1 else 'black'
                self.send_to_client(client_socket, {
                    'type': 'player_info',
                    'color': player_color,
                    'player_number': len(self.clients)
                })
                
                # Start thread để xử lý client
                threading.Thread(target=self.handle_client, args=(client_socket, len(self.clients))).start()
            
            if len(self.clients) == 2:
                print("Game started! Both players connected.")
                self.broadcast({'type': 'game_start'})
                
        except Exception as e:
            print(f"Server error: {e}")
    
    def handle_client(self, client_socket, player_num):
        try:
            while self.running:
                data = client_socket.recv(1024).decode()
                if not data:
                    break
                
                message = json.loads(data)
                self.process_message(message, client_socket, player_num)
                
        except Exception as e:
            print(f"Client {player_num} error: {e}")
        finally:
            if client_socket in self.clients:
                self.clients.remove(client_socket)
            client_socket.close()
    
    def process_message(self, message, sender_socket, player_num):
        if message['type'] == 'move':
            # Broadcast nước đi đến tất cả clients
            self.broadcast(message, exclude=sender_socket)
            print(f"Player {player_num} moved: {message['from_pos']} -> {message['to_pos']}")
        
        elif message['type'] == 'surrender':
            self.broadcast({'type': 'game_over', 'winner': 'opponent', 'reason': 'surrender'}, exclude=sender_socket)
            self.send_to_client(sender_socket, {'type': 'game_over', 'winner': 'you', 'reason': 'opponent_surrender'})
    
    def send_to_client(self, client_socket, message):
        try:
            client_socket.send(json.dumps(message).encode())
        except:
            pass
    
    def broadcast(self, message, exclude=None):
        for client in self.clients[:]:
            if client != exclude:
                self.send_to_client(client, message)
    
    def stop(self):
        self.running = False
        for client in self.clients:
            client.close()
        self.socket.close()

if __name__ == "__main__":
    server = ChessServer()
    try:
        server.start()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.stop()
