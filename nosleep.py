import ctypes
import msvcrt
import time
import sys
from datetime import datetime

__version__ = "1.0.0"

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

def main():
    # Parse arguments
    if "--version" in sys.argv or "-v" in sys.argv:
        print(f"nosleep version {__version__}")
        sys.exit(0)

    test_mode = "--test" in sys.argv
    interval = 5.0 if test_mode else 300.0  # 5 seconds in test mode, 5 minutes in production mode


    print("==================================================")
    print("                  NOSLEEP APP                     ")
    print("==================================================")
    print("version 1.0.0")
    if test_mode:
        print("Mode: TEST MODE (moves cursor every 5 seconds)")
    else:
        print("Mode: Normal (moves cursor every 5 minutes)")
    print("Press [ESC] in this console window to exit.")
    print("==================================================")

    # Set thread execution state to prevent sleep
    try:
        ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED)
    except Exception as e:
        print(f"Warning: Failed to set thread execution state: {e}", file=sys.stderr)

    last_move_time = time.time()

    try:
        while True:
            # Non-blocking check for keyboard input
            if msvcrt.kbhit():
                key = msvcrt.getch()
                if key == b'\x1b':  # ESC key
                    print("\n[ESC] detected. Exiting nosleep cleanly...")
                    break

            time.sleep(0.1)
            
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
        try:
            ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)
        except Exception as e:
            print(f"Warning: Failed to restore thread execution state: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
