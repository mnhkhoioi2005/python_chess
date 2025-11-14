#!/usr/bin/env python3
"""
LAN Discovery - Tự động tìm game server trong mạng LAN
"""
import socket
import threading
import time
import json

class LANDiscovery:
    def __init__(self, port=12346):
        self.port = port
        self.servers = {}
        
    def broadcast_server(self, server_name="Chess Game"):
        """Server broadcast thông tin của mình"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        
        # Lấy IP local
        local_ip = self.get_local_ip()
        
        message = {
            'type': 'chess_server',
            'name': server_name,
            'ip': local_ip,
            'port': 12345
        }
        
        try:
            while True:
                sock.sendto(json.dumps(message).encode(), ('<broadcast>', self.port))
                time.sleep(2)  # Broadcast mỗi 2 giây
        except:
            pass
        finally:
            sock.close()
    
    def scan_for_servers(self, timeout=5):
        """Client scan tìm servers"""
        self.servers = {}
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('', self.port))
        sock.settimeout(1)
        
        start_time = time.time()
        
        print("Scanning for Chess servers on LAN...")
        
        while time.time() - start_time < timeout:
            try:
                data, addr = sock.recvfrom(1024)
                message = json.loads(data.decode())
                
                if message['type'] == 'chess_server':
                    server_id = f"{message['ip']}:{message['port']}"
                    self.servers[server_id] = {
                        'name': message['name'],
                        'ip': message['ip'],
                        'port': message['port'],
                        'last_seen': time.time()
                    }
                    print(f"Found: {message['name']} at {message['ip']}")
                    
            except socket.timeout:
                continue
            except:
                break
        
        sock.close()
        return list(self.servers.values())
    
    def get_local_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "localhost"

if __name__ == "__main__":
    discovery = LANDiscovery()
    
    choice = input("(1) Broadcast server or (2) Scan for servers? [1/2]: ")
    
    if choice == "1":
        name = input("Server name (default: Chess Game): ").strip() or "Chess Game"
        print(f"Broadcasting '{name}' on LAN...")
        print("Press Ctrl+C to stop")
        try:
            discovery.broadcast_server(name)
        except KeyboardInterrupt:
            print("\nStopped broadcasting")
    else:
        servers = discovery.scan_for_servers()
        if servers:
            print(f"\nFound {len(servers)} server(s):")
            for i, server in enumerate(servers, 1):
                print(f"{i}. {server['name']} - {server['ip']}:{server['port']}")
        else:
            print("No servers found")
