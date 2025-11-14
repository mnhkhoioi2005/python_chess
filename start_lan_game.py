#!/usr/bin/env python3
"""
LAN Chess Game Launcher
"""
import subprocess
import sys
import os
from lan_discovery import LANDiscovery
import threading
import time

def get_local_ip():
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "localhost"

def host_game():
    print("=== HOST GAME ===")
    local_ip = get_local_ip()
    print(f"Your IP: {local_ip}")
    print("Starting server and broadcasting on LAN...")
    
    # Start discovery broadcast
    discovery = LANDiscovery()
    broadcast_thread = threading.Thread(
        target=discovery.broadcast_server, 
        args=("Chess Game",), 
        daemon=True
    )
    broadcast_thread.start()
    
    # Start server and open game
    subprocess.run([sys.executable, "host_and_play.py"])

def join_game():
    print("=== JOIN GAME ===")
    discovery = LANDiscovery()
    
    print("Scanning for games...")
    servers = discovery.scan_for_servers(timeout=3)
    
    if not servers:
        print("No games found!")
        ip = input("Enter server IP manually: ").strip()
        if ip:
            start_client(ip)
        return
    
    print(f"\nFound {len(servers)} game(s):")
    for i, server in enumerate(servers, 1):
        print(f"{i}. {server['name']} - {server['ip']}")
    
    try:
        choice = int(input("Select game (number): ")) - 1
        if 0 <= choice < len(servers):
            start_client(servers[choice]['ip'])
    except:
        print("Invalid choice")

def start_client(ip):
    print(f"Connecting to {ip}...")
    # Set environment variable for auto-connect
    os.environ['CHESS_AUTO_IP'] = ip
    subprocess.run([sys.executable, "main.py"])

def main():
    print("=== LAN CHESS GAME ===")
    print("1. Host Game")
    print("2. Join Game") 
    print("3. Exit")
    
    choice = input("Choose option [1-3]: ").strip()
    
    if choice == "1":
        host_game()
    elif choice == "2":
        join_game()
    elif choice == "3":
        print("Goodbye!")
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()
