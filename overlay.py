from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import *
from PyQt5 import QtGui
from utils import get_window_info
from pynput import keyboard
from utils import add_to_json, init_db, remove_from_json
import json

class OverlayWidget(QWidget):
    def __init__(self, window_info, hwnd):
        super().__init__()
        self.target_hwnd = hwnd
        self.x = window_info.win_x
        self.y = window_info.win_y
        self.width = window_info.win_width
        self.height = window_info.win_height
        
        self.setWindowTitle("test window")
        self.setGeometry(
            self.x,
            self.y,
            self.width,
            self.height
            )
        
        self.setWindowFlags(Qt.Window|Qt.X11BypassWindowManagerHint|Qt.WindowStaysOnTopHint|Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.update_position()
        self.init_ui()
        
        timer = QTimer(self)
        timer.timeout.connect(self.update_position)
        timer.start(100)
    
    def init_ui(self):
        layout = QGridLayout()
        
        # Input Item To List
        input_layout_good = QHBoxLayout()
        input_layout_bad = QHBoxLayout()
        
        input_good = QLineEdit()
        input_bad = QLineEdit()
        
        submit_1 = QPushButton("Submit")
        submit_1.clicked.connect(lambda: self.add_item_button(input_good.text(), "Good"))
        submit_2 = QPushButton("Submit")
        submit_2.clicked.connect(lambda: self.add_item_button(input_bad.text(), "Bad"))
        
        self.good_maps = QListWidget()
        self.bad_maps = QListWidget()
        # 

        self.maps = init_db()
        
        for map, label in self.maps.items():
            if label == "Good":
                item = QListWidgetItem()
                item_widget = QWidget()
                line_text = QLabel(map)
                line_push_button = QPushButton()
                line_push_button.setFixedSize(16,16)
                line_push_button.setIcon(QtGui.QIcon("icons/square_14034319.png"))
                line_push_button.setObjectName(map)
                line_push_button.clicked.connect(self.remove_good_button)
                item_layout = QHBoxLayout()
                item_layout.addWidget(line_text)
                item_layout.addWidget(line_push_button)
                item_widget.setLayout(item_layout)
                item.setSizeHint(item_widget.sizeHint())
                self.good_maps.addItem(item)
                self.good_maps.setItemWidget(item, item_widget)
            else:
                item = QListWidgetItem()
                item_widget = QWidget()
                line_text = QLabel(map)
                line_push_button = QPushButton()
                line_push_button.setFixedSize(16,16)
                line_push_button.setIcon(QtGui.QIcon("icons/square_14034319.png"))
                line_push_button.setObjectName(map)
                line_push_button.clicked.connect(self.remove_bad_button)
                item_layout = QHBoxLayout()
                item_layout.addWidget(line_text)
                item_layout.addWidget(line_push_button)
                item_widget.setLayout(item_layout)
                item.setSizeHint(item_widget.sizeHint())
                self.bad_maps.addItem(item)
                self.bad_maps.setItemWidget(item, item_widget)

        layout.addWidget(self.good_maps, 0,0)
        layout.addWidget(self.bad_maps, 0,1)
        
        # Add Input Item To List To HBoxLayout
        input_layout_good.addWidget(input_good)
        input_layout_good.addWidget(submit_1)
        input_layout_bad.addWidget(input_bad)
        input_layout_bad.addWidget(submit_2)
        # 
        
        layout.addLayout(input_layout_good, 1,0)
        layout.addLayout(input_layout_bad, 1,1)

        
        self.setLayout(layout)

    def remove_good_button(self):
        sender = self.sender()    
        push_button = self.findChild(QPushButton, sender.objectName())
        
        # Iterate over the items in the list and find the one that matches the objectName of the push button
        for row in range(self.good_maps.count()):
            item = self.good_maps.item(row)
            widget = self.good_maps.itemWidget(item)
            
            if widget:
                button = widget.findChild(QPushButton)
                if button and button.objectName() == push_button.objectName():
                    # Remove the item from the list
                    self.good_maps.removeItemWidget(item)  # Remove the widget from the layout
                    self.good_maps.takeItem(row)  # Remove the item from the list

                    # Remove the associated data from the JSON
                    remove_from_json(push_button.objectName())
                    break

    def remove_bad_button(self):
        sender = self.sender()    
        push_button = self.findChild(QPushButton, sender.objectName())
        
        # Iterate over the items in the list and find the one that matches the objectName of the push button
        for row in range(self.bad_maps.count()):
            item = self.bad_maps.item(row)
            widget = self.bad_maps.itemWidget(item)
            
            if widget:
                button = widget.findChild(QPushButton)
                if button and button.objectName() == push_button.objectName():
                    # Remove the item from the list
                    self.bad_maps.removeItemWidget(item)  # Remove the widget from the layout
                    self.bad_maps.takeItem(row)  # Remove the item from the list

                    # Remove the associated data from the JSON
                    remove_from_json(push_button.objectName())
                    break

    def add_item_button(self, map, map_type):
        # Update the local database and add to real time list view
        add_to_json({map: map_type})
        if map_type == "Good":
            item = QListWidgetItem()
            item_widget = QWidget()
            line_text = QLabel(map)
            line_push_button = QPushButton()
            line_push_button.setFixedSize(16,16)
            line_push_button.setIcon(QtGui.QIcon("icons/square_14034319.png"))
            line_push_button.setObjectName(map)
            line_push_button.clicked.connect(self.remove_good_button)
            item_layout = QHBoxLayout()
            item_layout.addWidget(line_text)
            item_layout.addWidget(line_push_button)
            item_widget.setLayout(item_layout)
            item.setSizeHint(item_widget.sizeHint())
            self.good_maps.addItem(item)
            self.good_maps.setItemWidget(item, item_widget)
        else:
            item = QListWidgetItem()
            item_widget = QWidget()
            line_text = QLabel(map)
            line_push_button = QPushButton()
            line_push_button.setFixedSize(16,16)
            line_push_button.setIcon(QtGui.QIcon("icons/square_14034319.png"))
            line_push_button.setObjectName(map)
            line_push_button.clicked.connect(self.remove_bad_button)
            item_layout = QHBoxLayout()
            item_layout.addWidget(line_text)
            item_layout.addWidget(line_push_button)
            item_widget.setLayout(item_layout)
            item.setSizeHint(item_widget.sizeHint())
            self.bad_maps.addItem(item)
            self.bad_maps.setItemWidget(item, item_widget)
        
        
    def update_position(self):
        info = get_window_info(self.target_hwnd)
        self.setGeometry(info.win_x, info.win_y, info.win_width, info.win_height)
        
    def keyPressEvent(self, event):
        pass