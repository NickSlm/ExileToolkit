from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QTimer,pyqtSignal
from PyQt5.QtGui import *
from PyQt5 import QtGui
import json

class SettingsWindow(QDialog):
    toggle_signal = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.toggle_signal.connect(self.appear)
        
        self.init_ui()
    
    def init_ui(self):
        self.layout = QVBoxLayout()
        
        self.setWindowTitle("Settings")
        self.setFixedSize(288, 224)
        
        self.tabs = QTabWidget()
        self.keybind_tab = QWidget()
        self.path_tab = QWidget()
        
        self.tabs.addTab(self.keybind_tab, "Keybinds")
        self.tabs.addTab(self.path_tab, "Directories")
        
        # Keybinds Tab
        self.keybind_tab.layout = QGridLayout()
        
        self.l_1 = QLabel("Open Overlay")
        self.l_2 = QLabel("Open Settings")
        self.l_3 = QLabel("Check Map")
        
        self.qkse_1 = QKeySequenceEdit()
        self.qkse_2 = QKeySequenceEdit()
        self.qkse_3 = QKeySequenceEdit()
        
        self.btn_clear_1 = QPushButton("clear")
        self.btn_clear_2 = QPushButton("clear")
        self.btn_clear_3 = QPushButton("clear")
        
        self.btn_clear_1.clicked.connect(self.qkse_1.clear)
        self.btn_clear_2.clicked.connect(self.qkse_2.clear)
        self.btn_clear_3.clicked.connect(self.qkse_3.clear)
        
        self.keybind_tab.layout.addWidget(self.l_1, 0,0)
        self.keybind_tab.layout.addWidget(self.l_2, 1,0)
        self.keybind_tab.layout.addWidget(self.l_3, 2,0)

        
        self.keybind_tab.layout.addWidget(self.qkse_1, 0,1)
        self.keybind_tab.layout.addWidget(self.qkse_2, 1,1)
        self.keybind_tab.layout.addWidget(self.qkse_3, 2,1)
        
        
        self.keybind_tab.layout.addWidget(self.btn_clear_1, 0,2)
        self.keybind_tab.layout.addWidget(self.btn_clear_2, 1,2)
        self.keybind_tab.layout.addWidget(self.btn_clear_3, 2,2)
        
        
        self.keybind_tab.layout.addWidget(QPushButton("Save"), 3, 0)
        self.keybind_tab.layout.addWidget(QPushButton("Cancel"), 3, 1)

        self.keybind_tab.setLayout(self.keybind_tab.layout)
    
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
    
    
    def appear(self):
        if self.isVisible():
            self.hide() 
        else:
            self.show()