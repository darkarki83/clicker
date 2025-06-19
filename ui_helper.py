import win32gui
import win32con
import time
import pyautogui
from pywinauto import Desktop

def focus_and_click_center(window_title_part):
    windows = Desktop(backend="uia").windows()
    target_window = None

    for w in windows:
        if window_title_part in w.window_text():
            target_window = w
            break

    if not target_window:
        print("❌ Window not found.")
        return None

    print("✅ Window found!")

    try:
        hwnd = target_window.handle
        win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
        time.sleep(0.5)
        win32gui.SetForegroundWindow(hwnd)
        print("📌 Window brought to the foreground.")
        time.sleep(0.5)

        rect = target_window.rectangle()
        center_x = rect.left + rect.width() // 2
        center_y = rect.top + rect.height() // 2

        pyautogui.moveTo(center_x, center_y, duration=0.2)
        pyautogui.click()
        return target_window

    except Exception as e:
        print("⚠️ Error while trying to focus:", e)
        return None