import json
import os 
import sys 

class Config:
    def __init__(self, dir_path):
        dir_path = dir_path
        file_path = "config\config.json"
        self.file_name = os.path.join(dir_path, file_path)
        self.config = None
    
    def load(self):
        if self.config is None:
            with open(self.file_name, 'r') as file:
                self.config = json.load(file)
    
    def get(self, key):
        if self.config is None:
            raise RuntimeError("Configuration not loaded. Call Config.load")
        return self.config[key]
    
