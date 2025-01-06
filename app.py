from utils import get_window_info
from PyQt5 import QtWidgets
import win32gui
import sys
from overlay import OverlayWidget
import threading

def main():
    hwnd = win32gui.FindWindow(None, "Microsoft Whiteboard")
    if hwnd == 0:
        print("Application is not running")
    else:
        window_info = get_window_info(hwnd=hwnd)
        app = QtWidgets.QApplication(sys.argv)
        overlay = OverlayWidget(window_info, hwnd)
        overlay.show()
        sys.exit(app.exec_())
    
if __name__ == "__main__":
    main() 