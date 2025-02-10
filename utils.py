import win32gui
import json
import os
import sys
import re


def multi_replace_regex(text, replacements):
    pattern = "|".join(map(re.escape, replacements.keys()))
    return re.sub(pattern, lambda m: replacements[m.group()], text)

class MapsDatabase:
    def __init__(self, config):
        self.config = config
        self.maps_path = self.config.config["maps_path"]
        self.database_path = self.config.config["database_path"]
        self.maps = {}
        
        self.init_db()
            
    def init_db(self):
        with open(self.maps_path, 'r') as file:
            try:
                self.maps = json.load(file)
            except json.JSONDecodeError as e:
                raise RuntimeError(f"Error Loading Configuration File:{e}")

    def add(self, new_map):
        self.maps.update(new_map)
        with open(self.maps_path, 'w') as file:
            json.dump(self.maps, file, indent=4)
            
    def remove(self, map):
        self.maps.pop(map)
        with open(self.maps_path, 'w') as file:
            json.dump(self.maps, file, indent=4)
    
    def get(self, map):
        with open(self.database_path) as file:
            try:
                maps = json.load(file)
            except json.JSONDecodeError as e:
                raise RuntimeError(f"Error Loading Database File:{e}")
        link = maps[map]
        return link

    def exist(self, map):
        if map in self.maps.keys():
            return True
        else:
            return False
        
    def get_map_type(self, map):
        map = re.sub(r"[^a-zA-Z\s]", '', map)
        map = map.strip()
        if self.exist(map):
            return self.maps[map]
        else:
            return "NO SUCH MAP"
        
