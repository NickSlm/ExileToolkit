from utils import get_window_info
from PyQt5 import QtWidgets,QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread, pyqtSignal
import win32gui
import sys
import os
import threading
from pynput import keyboard
from overlay import OverlayWindow
from settings import SettingsWindow
from config import Config
from utils import MapsDatabase

def on_key_press(key, config, handlers):
    keybinds = load_keybinds(config)
    for action, keybind in keybinds.items():
        if key == keybind:
            handler = handlers.get(action)
            if handler:
                handler()
            return

def application_exit():
    QApplication.instance().quit()

def get_exe_path():
    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
        if "_internal" in base_path:
            return base_path
    else:
        return os.path.dirname(__file__)   
    
def load_keybinds(config):
    # Reload the config file for changes that might accured
    config.reload()
    # 
    keybinds = {}
    for action, keybind in config.config["keybinds"].items():
        try:
            if hasattr(keyboard.Key, keybind):
                keybinds[action] = keybind
        except ArithmeticError:
            raise ValueError(f"Invalid keybind: {keybind}")
    return keybinds

class KeyListenerThread(QThread):
    key_pressed = pyqtSignal(str)
    def __init__(self, handlers):
        super().__init__()
        self.handlers = handlers
    
    def run(self):
        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()
            
    def on_press(self, key):
        try:
            if isinstance(key, keyboard.KeyCode) and key.char is not None:
                key_name = key.char if hasattr(key, 'char') else str(key)
            elif isinstance(key, keyboard.Key):
                key_name = key.name
            else:
                key_name = str(key)
            self.key_pressed.emit(key_name)
        except Exception as e:
            print(f"Error handling key press: {e}")

def main():
    hwnd = win32gui.FindWindow(None, "Microsoft Whiteboard")
    if hwnd == 0:
        print("Application is not running")
    else:
        window_info = get_window_info(hwnd=hwnd)
        
        # Load Configuration File
        dir_path = get_exe_path()
        config = Config(dir_path)
        
        # Create Database
        maps_database = MapsDatabase(config)
        
        app = QApplication(sys.argv)
        tray_icon = QSystemTrayIcon()
        tray_icon.setIcon(QtGui.QIcon(os.path.join(config.config["assets_path"], config.config["icons"]["tray"])))
        
        menu = QMenu()
        settings = SettingsWindow(config)
        settings_action = QAction("Settings")
        settings_action.triggered.connect(settings.appear)
        exit_action = QAction("Exit")
        exit_action.triggered.connect(application_exit)
        
        menu.addAction(settings_action)
        menu.addAction(exit_action)
        

        tray_icon.setContextMenu(menu)
        overlay = OverlayWindow(window_info, maps_database, config ,hwnd)
        
        handlers = {"settings":settings.appear,
                    "overlay": overlay.toggle_visibility}
        
        listener_thread = KeyListenerThread(handlers)
        listener_thread.key_pressed.connect(lambda key_name: on_key_press(key_name, config, handlers))
        
        listener_thread.start()
        
        
        tray_icon.show()
        sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()