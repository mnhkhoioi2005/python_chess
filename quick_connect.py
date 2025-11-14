#!/usr/bin/env python3
"""
Quick Connect - Nhập IP và chuyển thẳng vào game
"""
import os
import sys
from game.online_game import OnlineChessGame

def main():
    print("=== QUICK CONNECT TO CHESS GAME ===")
    
    # Nhập IP
    ip = input("Enter server IP (Enter for localhost): ").strip()
    if not ip:
        ip = "localhost"
    
    print(f"Connecting to {ip}...")
    
    try:
        # Chuyển thẳng vào game
        print("Creating OnlineChessGame...")
        game = OnlineChessGame(ip)
        print("Game created, starting...")
        game.run()
        print("Game finished normally")
    except Exception as e:
        print(f"Connection failed: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
