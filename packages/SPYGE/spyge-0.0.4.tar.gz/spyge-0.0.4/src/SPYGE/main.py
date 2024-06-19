import pygame as pg
import os
import pathlib
    
def init(self):
    self.BASE_DIR = pathlib.Path(__file__).parent
    if not os.path.exists(self.BASE_DIR / "spyge_data_files/"):
        raise FileNotFoundError("Directory \"spyge_data_files/\" excpected")
