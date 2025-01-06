import win32gui
from dataclass import WindowInfo
import json
import os

def get_window_info(hwnd):
    window_info = WindowInfo()
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    window_info.win_x = left
    window_info.win_y = top
    window_info.win_width = right - left
    window_info.win_height = bottom - top


    left, top, right, bottom = win32gui.GetClientRect(hwnd)
    window_info.client_width = right - left
    window_info.client_height = bottom - top
    return window_info

def init_db():
    if not os.path.exists("maps.json") or os.path.getsize("maps.json") == 0:
        maps = {}
    else:
        with open("maps.json") as file:
            try:
                maps = json.load(file)
            except json.JSONDecodeError:
                maps = {}
    return maps

def check_if_exists(map, map_type):
    maps = init_db()
    if map in maps.keys():
        print(map, maps[map])

def add_to_json(new_data):
    maps = init_db()  
    maps.update(new_data)
    # update the json with the updated dict
    with open("maps.json", 'w') as file:    
        json.dump(maps, file, indent = 4)

def remove_from_json(map):
    maps = init_db()
    maps.pop(map)
    with open("maps.json", 'w') as file:
        json.dump(maps, file, indent = 4)