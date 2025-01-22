from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QTimer,pyqtSignal
from PyQt5.QtGui import *
from PyQt5 import QtGui
import json

class SettingsWindow(QDialog):
    toggle_signal = pyqtSignal()
    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.toggle_signal.connect(self.appear)
        self.config = config 
        self.init_ui()
    
    def init_ui(self):
        self.layout = QVBoxLayout()
        
        self.setWindowTitle("Settings")
        self.setFixedSize(288, 224)
        
        self.tabs = QTabWidget()
        keybind_tab = self.keybind_tab()
        self.path_tab = QWidget()
        
        self.tabs.addTab(keybind_tab, "Keybinds")
        self.tabs.addTab(self.path_tab, "Directories")
    
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        
    def keybind_tab(self):
        tab = QWidget()
        tab.layout = QGridLayout()
        
        self.l_1 = QLabel("Open Overlay")
        self.l_2 = QLabel("Open Settings")
        self.l_3 = QLabel("Check Map")
        
        
        self.qkse_1 = QKeySequenceEdit(self.config.config["keybinds"]["overlay"])
        self.qkse_2 = QKeySequenceEdit(self.config.config["keybinds"]["settings"])
        self.qkse_3 = QKeySequenceEdit(self.config.config["keybinds"]["hover"])
        
        
        self.btn_clear_1 = QPushButton("clear")
        self.btn_clear_2 = QPushButton("clear")
        self.btn_clear_3 = QPushButton("clear")
        
        
        self.btn_clear_1.clicked.connect(self.qkse_1.clear)
        self.btn_clear_2.clicked.connect(self.qkse_2.clear)
        self.btn_clear_3.clicked.connect(self.qkse_3.clear)
        
        
        tab.layout.addWidget(self.l_1, 0,0)
        tab.layout.addWidget(self.l_2, 1,0)
        tab.layout.addWidget(self.l_3, 2,0)

        
        tab.layout.addWidget(self.qkse_1, 0,1)
        tab.layout.addWidget(self.qkse_2, 1,1)
        tab.layout.addWidget(self.qkse_3, 2,1)
        
        tab.layout.addWidget(self.btn_clear_1, 0,2)
        tab.layout.addWidget(self.btn_clear_2, 1,2)
        tab.layout.addWidget(self.btn_clear_3, 2,2)
        
        self.btn_save = QPushButton("Save")
        self.btn_cancel = QPushButton("Cancel")
        
        self.btn_save.clicked.connect(self.submit_form)
        self.btn_cancel.clicked.connect(self.hide)
        
        tab.layout.addWidget(self.btn_save, 3, 0)
        tab.layout.addWidget(self.btn_cancel, 3, 1)

        tab.setLayout(tab.layout)
        return tab
    
    def path_tab(self):
        pass
        
        
    def submit_form(self):
        keybinds = {
            "keybinds":
                {
            "overlay":self.qkse_1.keySequence().toString().lower(),
            "settings":self.qkse_2.keySequence().toString().lower(),
            "hover":self.qkse_3.keySequence().toString().lower()
            }
            }
        self.config.update(keybinds)
            
    def appear(self):
        if self.isVisible():
            self.hide() 
        else:
            self.show()
            
    def closeEvent(self, event):
        self.hide()
        event.ignore()