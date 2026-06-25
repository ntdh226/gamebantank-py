# constants.py
# Screen dimensions
SCREEN_WIDTH = 780
SCREEN_HEIGHT = 780
FPS = 60

# Map grid
TILE_SIZE = 30
COLS = SCREEN_WIDTH // TILE_SIZE  # 25
ROWS = SCREEN_HEIGHT // TILE_SIZE  # 18

# Tank
TANK_SIZE = TILE_SIZE  # Tank chiếm đúng 1 ô → 30px
TANK_SPEED = 3  # pixels/frame (chia hết cho 3 để align đẹp vào lưới)

# --- Game states (trạng thái màn hình) ---
STATE_START = "START"  # Màn hình chờ bắt đầu
STATE_PLAYING = "PLAYING"  # Đang chơi
STATE_GAMEOVER = "GAMEOVER"  # Thua, hỏi chơi lại / thoát
