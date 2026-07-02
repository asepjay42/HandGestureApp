from pathlib import Path

# ==========================
# Project Directory
# ==========================

ROOT_DIR = Path(__file__).parent
ASSET_DIR = ROOT_DIR / "assets"

# ==========================
# Audio
# ==========================

PHOTO_BLUR_MUSIC = ASSET_DIR / "foto_blur.mp3"
JOKOWI_MUSIC = ASSET_DIR / "jokowi.mp3"

# ==========================
# Camera
# ==========================

CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
CAMERA_FPS = 30

# ==========================
# MediaPipe
# ==========================

MIN_DETECTION_CONFIDENCE = 0.7
MIN_TRACKING_CONFIDENCE = 0.7
MAX_HANDS = 1

# ==========================
# Blur
# ==========================

BLUR_KERNEL = 25

# ==========================
# Edge Detection
# ==========================

EDGE_LOW = 50
EDGE_HIGH = 150

# ==========================
# Animation
# ==========================

TYPEWRITER_SPEED = 0.12
TYPEWRITER_FADE = 0.08
FADE_DURATION = 0.40

# ==========================
# Text
# ==========================

MAIN_FONT_SCALE = 2.0
STATUS_FONT_SCALE = 0.6

# ==========================
# Gesture
# ==========================

DEBOUNCE_FRAMES = 3