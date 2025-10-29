#!/usr/bin/env python3
"""
Chess Server - Chạy server để 2 người chơi online
"""

from game.network_server import ChessServer
import socket

def get_local_ip():
    """Lấy IP local của máy"""
    try:
        # Kết nối đến một địa chỉ bên ngoài để lấy IP local
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "localhost"

def main():
    print("=== CHESS SERVER ===")
    
    # Lấy IP của máy
    local_ip = get_local_ip()
    print(f"Your IP address: {local_ip}")
    print("Share this IP with your friend to connect!")
    print()
    
    # Tùy chọn host
    host_choice = input("Host on (1) localhost or (2) LAN IP? [1/2]: ").strip()
    
    if host_choice == "2":
        host = local_ip
    else:
        host = "localhost"
    
    port = 12345
    
    print(f"Starting server on {host}:{port}")
    print("Waiting for 2 players to connect...")
    print("Press Ctrl+C to stop server")
    print("-" * 40)
    
    server = ChessServer(host, port)
    
    try:
        server.start()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.stop()
        print("Server stopped.")

if __name__ == "__main__":
    main()
