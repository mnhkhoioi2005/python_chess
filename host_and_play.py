#!/usr/bin/env python3
"""
Host and Play - Tạo server và tự động mở bàn cờ để chơi
"""
import threading
import time
import socket
from game.network_server import ChessServer
from game.online_game import OnlineChessGame

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "localhost"

def start_server_thread(host, port):
    """Chạy server trong thread riêng"""
    server = ChessServer(host, port)
    try:
        server.start()
    except Exception as e:
        print(f"Server error: {e}")

def main():
    print("=== HOST AND PLAY CHESS ===")
    
    # Lấy IP
    local_ip = get_local_ip()
    print(f"Your IP: {local_ip}")
    
    # Chọn host option
    host_choice = input("Host on (1) localhost or (2) LAN IP? [1/2]: ").strip()
    
    if host_choice == "2":
        host = local_ip
        print(f"Share this IP with your friend: {local_ip}")
    else:
        host = "localhost"
    
    port = 12345
    
    print(f"Starting server on {host}:{port}")
    
    # Khởi động server trong thread riêng
    server_thread = threading.Thread(target=start_server_thread, args=(host, port), daemon=True)
    server_thread.start()
    
    # Đợi server khởi động
    time.sleep(1)
    
    print("Server started! Opening chess board...")
    print("Waiting for opponent to connect...")
    
    # Mở game client để chơi
    try:
        print("Creating OnlineChessGame...")
        game = OnlineChessGame(host)
        print("Starting game...")
        game.run()
    except Exception as e:
        print(f"Game error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
