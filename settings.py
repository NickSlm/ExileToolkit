from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import *
from PyQt5 import QtGui
import json


class SettingsWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Settings")
        label1 = QLabel("1")
        label2 = QLabel("2")
        self.setFixedSize(600, 500)
        
        btns = QDialogButtonBox()
        btns.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Save)
        layout = QGridLayout()
        layout.addWidget(label1,0,0)
        layout.addWidget(label2,0,1)
        layout.addWidget(btns,1,0)
        self.setLayout(layout)
        