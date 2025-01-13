import win32gui
from dataclass import WindowInfo
import json
import os
import sys


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

class MapsDatabase:
    def __init__(self, config):
        self.config = config
        self.maps_path = self.config["maps_path"]
        self.database_path = self.config["database_path"]
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
        
        
# def create_database_of_maps(data):
#     if not os.path.exists("map_database.json") or os.path.getsize("map_database.json") == 0:
#         maps = {}
#     else:
#         with open("map_database.json") as file:
#             try:
#                 maps = json.load(file)
#             except json.JSONDecodeError:
#                 maps = {}
#     maps.update(data)
#     with open("map_database.json","w") as file:
#         json.dump(maps, file, indent=4)

# data = {
#     "Abyss": "https://www.poe2wiki.net/wiki/Zar_Wali,_the_Bone_Tyrant",
#     "Augury": "None",
#     "Backwash": "https://www.poe2wiki.net/wiki/Yaota,_the_Loathsome",
#     "Bloodwood": "None",
#     "Blooming Field": "https://www.poe2wiki.net/wiki/The_Black_Crow",
#     "Burial Bog": "https://www.poe2wiki.net/wiki/Grudgelash,_Vile_Ent",
#     "Canal Hideout": "None",
#     "Cenotes": "None",
#     "Channel": "https://www.poe2wiki.net/wiki/Hask,_the_Fallen_Son",
#     "Creek":"https://www.poe2wiki.net/wiki/Tierney,_the_Hateful",
#     "Crimson Shores":"None",
#     "Crypt":"https://www.poe2wiki.net/wiki/Meltwax,_Mockery_of_Faith",
#     "Decay":"https://www.poe2wiki.net/wiki/The_Rotten_Druid",
#     "Deserted":"None",
#     "Felled Hideout":"None",
#     "Forge":"https://www.poe2wiki.net/wiki/Vastweld,_the_Colossal_Guardian",
#     "Fortress":"https://www.poe2wiki.net/wiki/Pirasha,_the_Forgotten_Prisoner",
#     "Gothic City":"None",
#     "Headland":"None",
#     "Hidden Grotto":"None",
#     "Hive":"None",
#     "Limestone Hideout":"None",
#     "Lofty Summit":"None",
#     "Lost Towers":"https://www.poe2wiki.net/wiki/Oloton,_the_Remorseless",
#     "Mineshaft":"https://www.poe2wiki.net/wiki/Rudja,_the_Dread_Engineer",
#     "Mire":"https://www.poe2wiki.net/wiki/Riona,_Winter%27s_Cackle",
#     "Moment of Zen":"None",
#     "Necropolis":"https://www.poe2wiki.net/wiki/Tycho,_the_Black_Praetor",
#     "Oasis":"None",
#     "Penitentiary":"https://www.poe2wiki.net/wiki/Incarnation_of_Death",
#     "Ravine":"None",
#     "Riverside":"https://www.poe2wiki.net/wiki/Zekoa,_The_Headcrusher",
#     "Rustbowl":"https://www.poe2wiki.net/wiki/Gozen,_Rebellious_Rustlord",
#     "Savannah":"https://www.poe2wiki.net/wiki/Caedron,_the_Hyena_Lord",
#     "Sandpit":"None",
#     "Seepage":"https://www.poe2wiki.net/wiki/The_Fungus_Behemoth",
#     "Slick":"None",
#     "Spider Woods":"https://www.poe2wiki.net/wiki/Rootgrasp,_the_Hateful_Forest",
#     "Steaming Springs":"https://www.poe2wiki.net/wiki/Manassa,_the_Serpent_Queen",
#     "Sulphuric Caverns":"https://www.poe2wiki.net/wiki/Lord_of_the_Pit",
#     "Steppe":"None",
#     "Sump":"https://www.poe2wiki.net/wiki/The_Eater_of_Children",
#     "The Copper Citadel":"https://www.poe2wiki.net/wiki/Jamanra,_the_Abomination",
#     "The Iron Citadel":"https://www.poe2wiki.net/wiki/Count_Geonor",
#     "The Stone Citadel":"https://www.poe2wiki.net/wiki/Doryani,_Royal_Thaumaturge",
#     "Untainted Paradise":"None",
#     "Vaal Foundry":"None",
#     "Vaal Factory":"https://www.poe2wiki.net/wiki/Tetzcatl,_the_Blazing_Guardian",
#     "Vaults of Kamasa":"None",
#     "Willow":"https://www.poe2wiki.net/wiki/Connal,_the_Tormented",
#     "Woodland":"https://www.poe2wiki.net/wiki/Tierney,_the_Hateful"
# }
# create_database_of_maps(data)


