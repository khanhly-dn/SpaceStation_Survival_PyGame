"""
gesture_input.py - Nhận diện cử chỉ tay điều khiển game
Nhấn T trong game để bật/tắt.

CỬ CHỈ:
  ✊ FIST       → Bắn (left click)
  ✋ OPEN       → Mở cửa / Interact (phím E)  — xòe thẳng không nghiêng
  ✌️ PEACE      → Cheat máu GH               — ngón trỏ + giữa
  🤟 THREE      → Cheat đạn GT               — trỏ + giữa + nhẫn
  👈 TILT_LEFT  → Di chuyển trái (giữ A)
  👉 TILT_RIGHT → Di chuyển phải (giữ D)
"""

import threading
import time
import math
from collections import deque

# ── Trạng thái toàn cục ──────────────────────────────────────────────────────
gesture_mode_enabled  = False
_thread_started       = False
_last_gesture         = None
_current_frame_surf   = None
_pointer_norm         = (0.5, 0.5)
_status               = "Camera chua bat"

ACTION_EVENT        = 32877
ACTION_ATTACK       = "attack"
ACTION_CONTEXT      = "context"
ACTION_CONFIRM_ITEM = "confirm_item"
ACTION_PREV_ITEM    = "prev_item"
ACTION_NEXT_ITEM    = "next_item"

_virtual_keys_held: set = set()

# ── Landmark indices ──────────────────────────────────────────────────────────
WRIST      = 0
INDEX_MCP  = 5;  INDEX_PIP  = 6;  INDEX_TIP  = 8
MIDDLE_MCP = 9;  MIDDLE_PIP = 10; MIDDLE_TIP = 12
RING_MCP   = 13; RING_PIP   = 14; RING_TIP   = 16
PINKY_MCP  = 17; PINKY_PIP  = 18; PINKY_TIP  = 20
THUMB_TIP  = 4;  THUMB_IP   = 3;  THUMB_MCP  = 2

def _dist(a, b):
    return math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)

FINGER_UP_MARGIN = 0.08

def _finger_up(lm, tip, pip):
    return _dist(lm[tip], lm[WRIST]) > _dist(lm[pip], lm[WRIST]) + FINGER_UP_MARGIN

def _finger_down(lm, tip, mcp):
    return _dist(lm[tip], lm[mcp]) < _dist(lm[WRIST], lm[mcp]) * 0.85

# ── Cooldown ──────────────────────────────────────────────────────────────────
_cd: dict = {}
_CD = {
    "FIST":  0.30,
    "OPEN":  0.50,
    "PEACE": 2.0,
    "THREE": 2.0,
}

def _on_cd(name: str) -> bool:
    now = time.time()
    if now - _cd.get(name, 0) < _CD.get(name, 0):
        return True
    _cd[name] = now
    return False

# ── Gesture Smoothing ─────────────────────────────────────────────────────────
CONFIRM_FRAMES = 4
_gesture_history: deque = deque(maxlen=CONFIRM_FRAMES)
_confirmed_gesture = None

def _smooth_gesture(raw: str) -> str:
    global _confirmed_gesture
    _gesture_history.append(raw)
    if len(_gesture_history) < CONFIRM_FRAMES:
        return _confirmed_gesture or "NONE"
    if len(set(_gesture_history)) == 1:
        _confirmed_gesture = raw
    return _confirmed_gesture or "NONE"

# ── Phân loại cử chỉ ─────────────────────────────────────────────────────────
TILT_THRESHOLD = 0.08

def classify_gesture(lm) -> str:
    index_up  = _finger_up(lm, INDEX_TIP,  INDEX_PIP)
    middle_up = _finger_up(lm, MIDDLE_TIP, MIDDLE_PIP)
    ring_up   = _finger_up(lm, RING_TIP,   RING_PIP)
    pinky_up  = _finger_up(lm, PINKY_TIP,  PINKY_PIP)

    fingers_up = index_up + middle_up + ring_up + pinky_up

    # ── FIST: không ngón nào → Bắn ──
    if fingers_up == 0:
        return "FIST"

    # ── PEACE: chỉ trỏ + giữa → GH ──
    if index_up and middle_up and not ring_up and not pinky_up:
        return "PEACE"

    # ── THREE: trỏ + giữa + nhẫn → GT ──
    if index_up and middle_up and ring_up and not pinky_up:
        return "THREE"

    # ── TILT check trước: ≥ 3 ngón xòe + nghiêng rõ → di chuyển ──
    if fingers_up >= 3:
        dx = lm[MIDDLE_MCP].x - lm[WRIST].x
        dy = lm[MIDDLE_MCP].y - lm[WRIST].y

        if dx > TILT_THRESHOLD:
            return "TILT_LEFT"
        if dx < -TILT_THRESHOLD:
            return "TILT_RIGHT"

        # xòe thẳng không nghiêng → OPEN
        if fingers_up == 4:
            return "OPEN"
        return "NONE"

    return "NONE"

# ── Áp dụng cử chỉ ───────────────────────────────────────────────────────────
def _press_key(pg, key, char):
    pg.event.post(pg.event.Event(pg.KEYDOWN, {"key": key, "mod": 0, "unicode": char}))
    pg.event.post(pg.event.Event(pg.KEYUP,   {"key": key, "mod": 0, "unicode": char}))

def _press_combo(pg, key1, char1, key2, char2):
    """Nhấn 2 phím tuần tự 50ms như người thật gõ."""
    def _do():
        pg.event.post(pg.event.Event(pg.KEYDOWN, {"key": key1, "mod": 0, "unicode": char1}))
        pg.event.post(pg.event.Event(pg.KEYUP,   {"key": key1, "mod": 0, "unicode": char1}))
        time.sleep(0.05)
        pg.event.post(pg.event.Event(pg.KEYDOWN, {"key": key2, "mod": 0, "unicode": char2}))
        pg.event.post(pg.event.Event(pg.KEYUP,   {"key": key2, "mod": 0, "unicode": char2}))
    threading.Thread(target=_do, daemon=True).start()

def apply_gesture(gesture: str, lm):
    global _last_gesture, _pointer_norm

    import pygame as pg

    _pointer_norm = (
        max(0.0, min(1.0, lm[INDEX_TIP].x)),
        max(0.0, min(1.0, lm[INDEX_TIP].y)),
    )

    # Di chuyển
    if gesture == "TILT_LEFT":
        _virtual_keys_held.discard(pg.K_d)
        _virtual_keys_held.add(pg.K_a)
    elif gesture == "TILT_RIGHT":
        _virtual_keys_held.discard(pg.K_a)
        _virtual_keys_held.add(pg.K_d)
    else:
        _virtual_keys_held.discard(pg.K_a)
        _virtual_keys_held.discard(pg.K_d)

    # Bắn
    if gesture == "FIST" and not _on_cd("FIST"):
        pos = pg.mouse.get_pos()
        pg.event.post(pg.event.Event(pg.MOUSEBUTTONDOWN, {"pos": pos, "button": 1}))
        pg.event.post(pg.event.Event(pg.MOUSEBUTTONUP,   {"pos": pos, "button": 1}))

    # OPEN hand: chi di chuyen con tro, khong tu dong interact
    # Nguoi dung phai tu bam phim E tren ban phim de interact

    # GH — máu +100
    elif gesture == "PEACE" and not _on_cd("PEACE"):
        _press_combo(pg, pg.K_g, "g", pg.K_h, "h")

    # GT — vô hạn đạn
    elif gesture == "THREE" and not _on_cd("THREE"):
        _press_combo(pg, pg.K_g, "g", pg.K_t, "t")

    _last_gesture = gesture

# ── Camera thread ─────────────────────────────────────────────────────────────
def _camera_thread():
    global _current_frame_surf, _last_gesture, _thread_started, _status

    try:
        import cv2
    except Exception:
        _status = "Thieu opencv-python"
        _thread_started = False
        return

    try:
        import mediapipe as mp
        mp_hands  = mp.solutions.hands
        mp_draw   = mp.solutions.drawing_utils
        mp_styles = mp.solutions.drawing_styles
    except Exception:
        _status = "Thieu mediapipe"
        _thread_started = False
        return

    hands_model = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.75,
        min_tracking_confidence=0.65,
    )

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        _status = "Khong mo duoc webcam"
        _thread_started = False
        return

    _status = "Webcam OK"
    print("[Gesture] Webcam OK — nhan T de bat.")
    print("[Gesture] FIST=ban | OPEN=mo cua | PEACE=GH | THREE=GT | TILT=di chuyen")

    while True:
        if not gesture_mode_enabled:
            _virtual_keys_held.clear()
            _gesture_history.clear()
            time.sleep(0.1)
            continue

        ret, frame = cap.read()
        if not ret:
            time.sleep(0.033)
            continue

        frame  = cv2.flip(frame, 1)
        rgb    = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands_model.process(rgb)

        if result.multi_hand_landmarks:
            for hand_lm in result.multi_hand_landmarks:
                mp_draw.draw_landmarks(
                    frame, hand_lm, mp_hands.HAND_CONNECTIONS,
                    mp_styles.get_default_hand_landmarks_style(),
                    mp_styles.get_default_hand_connections_style(),
                )

            lm          = result.multi_hand_landmarks[0].landmark
            raw_gesture = classify_gesture(lm)
            gesture     = _smooth_gesture(raw_gesture)
            apply_gesture(gesture, lm)

            label = gesture
            if raw_gesture != gesture:
                label += f" (raw:{raw_gesture})"
            cv2.putText(frame, label, (8, 28),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 80), 2)

        else:
            _virtual_keys_held.clear()
            _gesture_history.clear()
            _last_gesture = None
            cv2.putText(frame, "NO HAND", (8, 28),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 80, 255), 2)

        try:
            import pygame as pg
            small = cv2.resize(frame, (200, 150))
            small_rgb = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)
            _current_frame_surf = pg.surfarray.make_surface(small_rgb.swapaxes(0, 1))
        except Exception:
            _current_frame_surf = None

        time.sleep(0.033)

    cap.release()

# ── API công khai ─────────────────────────────────────────────────────────────
def get_camera_surface():
    return _current_frame_surf

def get_pointer_position(width: int, height: int):
    x = max(0, min(width  - 1, int(_pointer_norm[0] * width)))
    y = max(0, min(height - 1, int(_pointer_norm[1] * height)))
    return x, y

def get_last_gesture():
    return _last_gesture

def get_hand_gestures():
    return "NO HAND", _last_gesture or "NO HAND"

def get_status():
    return _status

def is_enabled():
    return gesture_mode_enabled

def set_enabled(enabled: bool):
    global gesture_mode_enabled, _status
    gesture_mode_enabled = enabled
    _virtual_keys_held.clear()
    _gesture_history.clear()
    _status = "Dang bat camera" if enabled else "Camera da tat"
    print(f"[Gesture] {'BAT' if enabled else 'TAT'}")
    if enabled and not _thread_started:
        start()

def toggle():
    set_enabled(not gesture_mode_enabled)

def start():
    global _thread_started
    if _thread_started:
        return
    _thread_started = True
    t = threading.Thread(target=_camera_thread, daemon=True, name="GestureThread")
    t.start()
