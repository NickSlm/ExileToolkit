from PyQt5 import QtWidgets,QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread, pyqtSignal
import sys
import os
import threading
from pynput import keyboard
from overlay import OverlayWindow, TooltipApp
from settings import SettingsWindow
from config import Config
from utils import MapsDatabase


ascii_fix = {
            '\x01': 'a', 
            '\x02': 'b', 
            '\x03': 'c', 
            '\x04': 'd', 
            '\x05': 'e', 
            '\x06': 'f', 
            '\x07': 'g',  
            '\x08': 'h', 
            '\x09': 'i', 
            '\x0a': 'j', 
            '\x0b': 'k', 
            '\x0c': 'l', 
            '\x0d': 'm', 
            '\x0e': 'n', 
            '\x0f': 'o', 
            '\x10': 'p', 
            '\x11': 'q', 
            '\x12': 'r', 
            '\x13': 's', 
            '\x14': 't', 
            '\x15': 'u', 
            '\x16': 'v', 
            '\x17': 'w', 
            '\x18': 'x', 
            '\x19': 'y', 
            '\x1a': 'z', 
            }

def on_key_press(key, config, handlers):
    keybinds = load_keybinds(config)
    for action, keybind in keybinds.items():
        
        if key == keybind:
            handler = handlers.get(action)
            if handler:
                if hasattr(handler, "__func__"):
                    if handler.__func__.__name__ == "show_tooltip":
                        handler()
                    else:
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

    keybinds = {}
    for action, keybind in config.config["keybinds"].items():
        try:
            if hasattr(keyboard.Key, keybind) or isinstance(keybind, str):
                keybinds[action] = keybind
        except ArithmeticError:
            raise ValueError(f"Invalid keybind: {keybind}")
    return keybinds

class KeyListenerThread(QThread):
    key_pressed = pyqtSignal(str)
    def __init__(self, handlers):
        super().__init__()
        self.handlers = handlers
        self.pressed_keys = set()
        self.modifiers = {"ctrl_l", "shift", "alt_l"}

    def run(self):
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()
            
    def get_key_name(self, key):
        if isinstance(key, keyboard.KeyCode) and key.char is not None:
            key_name = key.char
            if self.pressed_keys.intersection(self.modifiers):
                key_name = chr(key.vk)
        elif isinstance(key, keyboard.Key):
            key_name = key.name       
        return key_name.lower()
    
    def on_press(self, key):
        key_name = self.get_key_name(key)
        if key_name:
            self.pressed_keys.add(key_name)
            
        pressed_modifiers = self.pressed_keys.intersection(self.modifiers)
        modifiers_str = '+'.join(pressed_modifiers) if pressed_modifiers else ''
        if pressed_modifiers and key_name not in pressed_modifiers:
            self.key_pressed.emit(f'{modifiers_str}+{key_name}')
        else:
            self.key_pressed.emit(key_name)


    def on_release(self, key):
        key_name = self.get_key_name(key)
        if key_name:
            self.pressed_keys.discard(key_name)

def main():
        
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
    overlay = OverlayWindow(maps_database, config)
    tooltip = TooltipApp(maps_database, config)
    
    handlers = {"settings":settings.appear,
                "overlay": overlay.toggle_visibility,
                "hover": tooltip.show_tooltip}
    
    listener_thread = KeyListenerThread(handlers)
    listener_thread.key_pressed.connect(lambda key_name: on_key_press(key_name, config, handlers))
    listener_thread.start()
    
    
    tray_icon.show()
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()