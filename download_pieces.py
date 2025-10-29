#!/usr/bin/env python3
"""
Script tạo hình quân cờ mẫu đơn giản
"""
import pygame
import os

def create_sample_pieces():
    """Tạo hình quân cờ mẫu đơn giản"""
    pygame.init()
    
    # Tạo thư mục nếu chưa có
    assets_dir = os.path.join('assets', 'pieces')
    os.makedirs(assets_dir, exist_ok=True)
    
    # Kích thước và màu
    size = 64
    white_color = (255, 255, 255)
    black_color = (50, 50, 50)
    
    # Font cho ký tự Unicode
    font = pygame.font.Font(None, 48)
    
    pieces = {
        'wK': ('♔', white_color), 'wQ': ('♕', white_color), 'wR': ('♖', white_color),
        'wB': ('♗', white_color), 'wN': ('♘', white_color), 'wP': ('♙', white_color),
        'bK': ('♚', black_color), 'bQ': ('♛', black_color), 'bR': ('♜', black_color),
        'bB': ('♝', black_color), 'bN': ('♞', black_color), 'bP': ('♟', black_color)
    }
    
    for piece_name, (symbol, color) in pieces.items():
        # Tạo surface trong suốt
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        
        # Vẽ ký tự
        text = font.render(symbol, True, color)
        text_rect = text.get_rect(center=(size//2, size//2))
        surface.blit(text, text_rect)
        
        # Lưu file
        filename = os.path.join(assets_dir, f'{piece_name}.png')
        pygame.image.save(surface, filename)
        print(f"Created {filename}")
    
    print(f"\nĐã tạo {len(pieces)} file hình quân cờ trong thư mục {assets_dir}/")
    print("Bạn có thể thay thế bằng hình đẹp hơn!")

if __name__ == "__main__":
    create_sample_pieces()
