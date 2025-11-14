# Game Cờ Vua Python

Game cờ vua với giao diện đồ họa pygame, có thể kéo thả quân cờ.

## Cài đặt và chạy trên VSCode

### 1. Mở project trong VSCode
```bash
code /home/lnmk/chess_game
```

### 2. Cài đặt Python extension
- Mở Extensions (Ctrl+Shift+X)
- Tìm và cài "Python" của Microsoft

### 3. Chọn Python interpreter
- Ctrl+Shift+P → "Python: Select Interpreter"
- Chọn `./venv/bin/python`

### 4. Chạy game
**Cách 1: Debug/Run**
- Mở `main.py`
- Nhấn F5 hoặc Ctrl+F5

**Cách 2: Terminal**
- Ctrl+` (mở terminal)
- Chạy: `./run_game.sh`

**Cách 3: Terminal thủ công**
```bash
source venv/bin/activate
python main.py
```

## Thay đổi hình quân cờ

### Cách 1: Tự tạo/tải hình
1. Đặt file PNG vào thư mục `assets/pieces/`
2. Tên file: `wK.png`, `wQ.png`, `bK.png`, etc.
3. Kích thước khuyến nghị: 64x64 hoặc 128x128 pixels
4. Nền trong suốt (PNG)

### Cách 2: Dùng hình mẫu
```bash
# Tạo hình mẫu đơn giản
source venv/bin/activate
python download_pieces.py
```

### Danh sách file cần:
- **Quân trắng**: wK.png, wQ.png, wR.png, wB.png, wN.png, wP.png
- **Quân đen**: bK.png, bQ.png, bR.png, bB.png, bN.png, bP.png

### Nguồn hình đẹp:
- [Chess.com pieces](https://www.chess.com)
- [Lichess pieces](https://lichess.org)
- Tự vẽ hoặc tải từ internet

**Lưu ý**: Nếu không có file hình, game sẽ dùng ký tự Unicode mặc định.

- ✅ Giao diện đồ họa với pygame
- ✅ Kéo thả quân cờ
- ✅ Tọa độ bàn cờ (a-h, 1-8)
- ✅ Logic di chuyển đầy đủ
- ✅ Highlight ô được chọn
- ✅ Hiệu ứng shadow cho quân cờ

## Cách chơi
- Click và kéo quân cờ để di chuyển
- Thả vào ô muốn đi
- Luân phiên trắng-đen
- ESC hoặc đóng cửa sổ để thoát


T1
python host_and_play.py
T2
python quick_connect.py

Chạy file main.py

