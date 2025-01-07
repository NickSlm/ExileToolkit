from utils import get_window_info
from PyQt5 import QtWidgets
import win32gui
import sys
import threading
from pynput import keyboard
from overlay import OverlayWidget


def listen_for_keypress(app):
    def on_press(key):
        if key == keyboard.Key.f8:
            app.toggle_visibility()

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

def main():
    hwnd = win32gui.FindWindow(None, "Microsoft Whiteboard")
    if hwnd == 0:
        print("Application is not running")
    else:
        window_info = get_window_info(hwnd=hwnd)
        app = QtWidgets.QApplication(sys.argv)
        overlay = OverlayWidget(window_info, hwnd)
        
        listener_thread = threading.Thread(target=listen_for_keypress, args=(overlay,))
        listener_thread.daemon = True
        
        listener_thread.start()
        
        overlay.show()
        sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()