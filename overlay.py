from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QObject
from PyQt5.QtGui import *
from PyQt5 import QtGui
from utils import get_window_info
from pynput import keyboard
import json
import os

class CustomDropMenu(QWidget):
    def __init__(self, config):
        super().__init__()
        self.combobox = QComboBox()
        with open(config.config["database_path"]) as file:
            try:
                maps = json.load(file)
            except json.JSONDecodeError:
                maps = {}
        
        for map, link in maps.items():
            self.combobox.addItem(map)
    
        layout = QVBoxLayout()
        layout.addWidget(self.combobox)
        self.setLayout(layout)  # Set layout for this widget
    def get_selected_item(self):
        return self.combobox.currentText()
    
class CustomListItem(QWidget):
    def __init__(self, map, url, config, button_callback, parent=None):
        super().__init__()
        
        self.line_text = QLabel(self)
        if url != "None":
            self.line_text.setToolTip(url.split("/")[-1])
            self.line_text.setText(f'<a href="{url}" style="color: white; text-decoration: none;">{map}</a>')
        else:
            self.line_text.setText(map)
        self.line_text.setOpenExternalLinks(True)
        self.line_push_button = QPushButton(self)
        self.line_push_button.setFixedSize(16,16)
        self.line_push_button.setIcon(QtGui.QIcon(os.path.join(config.config["assets_path"], config.config["icons"]["delete"])))
        self.line_push_button.setObjectName(map)
        
        self.notes_push_button = QPushButton(self)
        self.notes_push_button.setFixedSize(16,16)
        self.notes_push_button.setIcon(QtGui.QIcon(os.path.join(config.config["assets_path"], config.config["icons"]["note"])))
        self.notes_push_button.setObjectName("<objectName>")
        
        
        layout = QHBoxLayout(self)
        layout.addWidget(self.line_text)
        layout.addWidget(self.notes_push_button)
        layout.addWidget(self.line_push_button)
        self.setLayout(layout)

        self.line_push_button.clicked.connect(button_callback)

class OverlayWindow(QWidget):
    toggle_signal = pyqtSignal()
    def __init__(self, window_info, database, config, hwnd):
        super().__init__()
        
        self.toggle_signal.connect(self.toggle_visibility)
        
        self.x = window_info.win_x
        self.y = window_info.win_y
        self.width = window_info.win_width
        self.height = window_info.win_height
        
        self.database = database
        self.config = config
        
        self.target_hwnd = hwnd
        self.setGeometry(
            self.x,
            self.y,
            self.width,
            self.height
            )
        self.setWindowFlags(Qt.Window|Qt.X11BypassWindowManagerHint|Qt.WindowStaysOnTopHint|Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("""
                           QLabel {
                               background-color: rgba(0, 0, 0, 0);
                               color: rgba(255, 255, 255,255);
                               text-align: center;
                           }
                           QListWidget {
                               background-color: rgba(0, 0, 0, 204);
                           }
                           QLineEdit {
                               background-color: rgba(0, 0, 0, 204);
                               color: rgba(255, 255, 255, 255);
                           }

                           """)
        
        self.update_position()
        self.init_ui()
        timer = QTimer(self)
        timer.timeout.connect(self.update_position)
        timer.start(100)
    
    def init_ui(self):
        layout = QGridLayout()
        self.setFixedSize(600,400)
        input_layout_1_0 = QHBoxLayout()
        input_layout_1_1 = QHBoxLayout()
        
        # Create List Headers
        header_1 = QLabel("Good Map Bosses")
        header_1.setAlignment(Qt.AlignCenter)
        header_1.setStyleSheet("font-size: 16px;")
        header_2 = QLabel("Bad Map Bosses")
        header_2.setStyleSheet("font-size: 16px;")
        header_2.setAlignment(Qt.AlignCenter)
        # 
        
        layout.addWidget(header_1, 0, 0)
        layout.addWidget(header_2, 0, 1)

        self.good_maps = QListWidget()
        self.bad_maps = QListWidget()

        self.maps = self.database.maps

        layout.addWidget(self.good_maps, 1, 0)
        layout.addWidget(self.bad_maps, 1, 1)
        
        # Add "Input Item To List" To HBoxLayout
        combobox = CustomDropMenu(self.config)
        submit_1 = QPushButton("Good")
        submit_1.clicked.connect(lambda: self.add_item_button(combobox.get_selected_item(), "Good"))
        submit_2 = QPushButton("Bad")
        submit_2.clicked.connect(lambda: self.add_item_button(combobox.get_selected_item(), "Bad"))

        input_layout_1_0.addWidget(combobox)
        input_layout_1_1.addWidget(submit_1)
        input_layout_1_1.addWidget(submit_2)
        # 
        
        layout.addLayout(input_layout_1_0, 2, 0)
        layout.addLayout(input_layout_1_1, 2, 1)

        
        self.setLayout(layout)


        # Populate the Lists
        for map, map_type in self.maps.items():
            if map_type == "Good":
                custom_widget = CustomListItem(map, self.database.get(map), self.config, button_callback=lambda map=map, map_type=map_type:self.remove_item(map, map_type))
                list_item = QListWidgetItem(self.good_maps)
                list_item.setSizeHint(custom_widget.sizeHint())
                self.good_maps.addItem(list_item)
                self.good_maps.setItemWidget(list_item, custom_widget)
            else:
                custom_widget = CustomListItem(map, self.database.get(map), self.config, button_callback=lambda map=map, map_type=map_type:self.remove_item(map, map_type))
                list_item = QListWidgetItem(self.bad_maps)
                list_item.setSizeHint(custom_widget.sizeHint())
                self.bad_maps.addItem(list_item)
                self.bad_maps.setItemWidget(list_item, custom_widget)

    def remove_item(self, map, map_type):
        sender = self.sender()
        push_button = self.findChild(QPushButton, sender.objectName())  # Find the button using objectName
        
        map_list = self.good_maps if map_type == "Good" else self.bad_maps
        for row in range(map_list.count()):
            item = map_list.item(row)  
            widget = map_list.itemWidget(item)
            
            if widget:
                button = widget.findChild(QPushButton)  
                if button and button.objectName() == push_button.objectName():
                    map_list.removeItemWidget(item)
                    map_list.takeItem(row)  
                    
                    self.database.remove(push_button.objectName())
                    break

    def add_item_button(self, map, map_type):
        # Update the local database and add to real time list view
        if self.database.exist(map):
            print("map in cunt")
        else:
            self.database.add({map: map_type})
            if map_type == "Good":
                custom_widget = CustomListItem(map, self.database.get(map), self.config, button_callback=lambda map=map, map_type=map_type:self.remove_item(map, map_type))
                list_item = QListWidgetItem(self.good_maps)
                list_item.setSizeHint(custom_widget.sizeHint())
                self.good_maps.addItem(list_item)
                self.good_maps.setItemWidget(list_item, custom_widget)
            else:
                custom_widget = CustomListItem(map, self.database.get(map), self.config, button_callback=lambda map=map, map_type=map_type:self.remove_item(map, map_type))
                list_item = QListWidgetItem(self.bad_maps)
                list_item.setSizeHint(custom_widget.sizeHint())
                self.bad_maps.addItem(list_item)
                self.bad_maps.setItemWidget(list_item, custom_widget)
                
    def update_position(self):
        info = get_window_info(self.target_hwnd)
        self.setGeometry(info.win_x, info.win_y, info.win_width, info.win_height)
        
    def keyPressEvent(self, event):
        pass
    
    def toggle_visibility(self):
        if self.isVisible():
            self.hide()
        else:
            self.show()
            