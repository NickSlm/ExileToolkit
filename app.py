from utils import get_window_info
from PyQt5 import QtWidgets,QtGui
from PyQt5.QtWidgets import *
import win32gui
import sys
import os
import threading
from pynput import keyboard
from overlay import OverlayWindow
from settings import SettingsWindow
from config import Config
from utils import MapsDatabase


def listen_for_keypress(app):
    def on_press(key):
        if key == keyboard.Key.f8:
            app.toggle_visibility()

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

def application_exit():
    QApplication.instance().quit()
    
def application_settings():
    pass


def get_exe_path():
    if hasattr(sys, "_MEIPASS"):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(__file__)   
    
def main():
    hwnd = win32gui.FindWindow(None, "Microsoft Whiteboard")
    if hwnd == 0:
        print("Application is not running")
    else:
        WINDOW_INFO = get_window_info(hwnd=hwnd)
        # Load Configuration File
        dir_path = get_exe_path()
        config = Config(dir_path)
        config.load()

        # Create Database
        maps_database = MapsDatabase(config)
        
        app = QtWidgets.QApplication(sys.argv)
        tray_icon = QSystemTrayIcon()
        tray_icon.setIcon(QtGui.QIcon("D:\PathOfExile2Overlay\icons\poo_720914.png"))
        
        menu = QMenu()
        
        settings_action = QAction("Settings")
        settings_action.triggered.connect(application_settings)
        exit_action = QAction("Exit")
        exit_action.triggered.connect(application_exit)
        
        menu.addAction(settings_action)
        menu.addAction(exit_action)

        tray_icon.setContextMenu(menu)
        overlay = OverlayWindow(WINDOW_INFO ,hwnd)
        settings = SettingsWindow()
        
        listener_thread = threading.Thread(target=listen_for_keypress, args=(overlay,))
        listener_thread.daemon = True
        
        listener_thread.start()
        
        tray_icon.show()
        overlay.show()
        settings.show()
        sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()