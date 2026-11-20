import ctypes
import msvcrt
import time
import sys
from datetime import datetime

__version__ = "1.0.2"

# Windows API constants
ES_CONTINUOUS = 0x80000000
ES_SYSTEM_REQUIRED = 0x00000001
ES_DISPLAY_REQUIRED = 0x00000002
MOUSEEVENTF_MOVE = 0x0001

class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]

def get_mouse_position():
    pt = POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
    return pt.x, pt.y

def nudge_mouse():
    # Simulate a real hardware mouse move relative: move right by 2, then left by 2
    ctypes.windll.user32.mouse_event(MOUSEEVENTF_MOVE, 2, 0, 0, 0)
    time.sleep(0.05)
    ctypes.windll.user32.mouse_event(MOUSEEVENTF_MOVE, -2, 0, 0, 0)

def set_keep_awake(enabled: bool):
    try:
        if enabled:
            ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED)
        else:
            ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)
    except Exception as e:
        print(f"Warning: Failed to set thread execution state: {e}", file=sys.stderr)

def main():
    # Parse arguments
    if "--version" in sys.argv or "-v" in sys.argv:
        print(f"nosleep version {__version__}")
        sys.exit(0)

    test_mode = "--test" in sys.argv
    classic_mode = "--classic" in sys.argv
    interval = 5.0 if test_mode else 300.0  # 5 seconds in test mode, 5 minutes in production mode

    print("==================================================")
    print("                  NOSLEEP APP                     ")
    print("==================================================")
    print(f"version {__version__}")
    if test_mode:
        print("Mode: TEST MODE (moves cursor every 5 seconds)")
    elif classic_mode:
        print("Mode: Classic (moves cursor every 5 minutes, no 18:00 pause)")
    else:
        print("Mode: Normal (moves cursor every 5 minutes, pauses 18:00-18:15)")
    print("Press [ESC] in this console window to exit.")
    print("==================================================")

    # Set thread execution state to prevent sleep initially
    set_keep_awake(True)

    last_move_time = time.time()
    is_paused = False

    try:
        while True:
            # Non-blocking check for keyboard input
            if msvcrt.kbhit():
                key = msvcrt.getch()
                if key == b'\x1b':  # ESC key
                    print("\n[ESC] detected. Exiting nosleep cleanly...")
                    break

            time.sleep(0.1)

            # Check 18:00 to 18:15 pause window if not in classic mode
            now = datetime.now()
            in_pause_window = (not classic_mode) and (now.hour == 18 and now.minute < 15)

            if in_pause_window:
                if not is_paused:
                    is_paused = True
                    set_keep_awake(False)
                    print(f"[{now.strftime('%H:%M:%S')}] 18:00 reached. Pausing nosleep for 15 minutes...")
                continue
            else:
                if is_paused:
                    is_paused = False
                    set_keep_awake(True)
                    last_move_time = time.time()
                    print(f"[{now.strftime('%H:%M:%S')}] 18:15 reached. Resuming normal nosleep operation.")

            # Check elapsed time
            current_time = time.time()
            if current_time - last_move_time >= interval:
                try:
                    # Get cursor position for logging
                    x, y = get_mouse_position()

                    # Nudge mouse simulating hardware input
                    nudge_mouse()

                    time_str = datetime.now().strftime("%H:%M:%S")
                    print(f"[{time_str}] Mouse nudged (x: {x}, y: {y})")
                except Exception as e:
                    print(f"Warning: Failed to move mouse: {e}", file=sys.stderr)
                last_move_time = current_time

    except KeyboardInterrupt:
        print("\nCtrl+C detected. Exiting nosleep cleanly...")
    finally:
        # Restore default sleep settings
        set_keep_awake(False)

if __name__ == "__main__":
    main()
