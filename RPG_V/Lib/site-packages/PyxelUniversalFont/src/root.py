import pyxel
import os
import platform
import subprocess
import sys
import random

from .utils import *

FONTS_DIR = get_data_path()

class Writer:
    def __init__(self, font_name) -> None:
        self.font_path = FONTS_DIR+f"/{font_name}"
        self.lib = dict()
        
    def draw(self, x, y, text, font_size=16, font_color=0, background_color=-1):
        if len(text) > 0:
            key = f"{text}|{font_size}|{font_color}|{background_color}"
            if not key in self.lib:
                pixels = get_pixel_representation(
                    text = text,
                    font_path = self.font_path,
                    font_size = font_size,
                    font_color = font_color,
                    background_color = background_color,
                )
                self.lib[key] = pixels
            else:
                pixels = self.lib[key]
                
            if pixels is not None:
                for y_number, raw in enumerate(pixels):
                    for x_number, pixel_color in enumerate(raw):
                        if pixel_color == 16:
                            pixel_color = random.choice([i for i in range(16) if i != 7])
                        
                        if pixel_color == -1:
                            pass
                        else:
                            pyxel.pset(
                                x = x + x_number,
                                y = y + y_number,
                                col = pixel_color,
                            )
        else:
            pass

def get_available_fonts():
    return list_font_files(FONTS_DIR)
        
def get_writers():
    writers = dict()
    for font_name in get_available_fonts():
        writers[font_name] = Writer(
            font_name=font_name,
        )
    return writers

def edit_fonts(path=FONTS_DIR):
    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":
        subprocess.run(["open", path])
    elif platform.system() == "Linux":
        subprocess.run(["xdg-open", path])
    else:
        raise ValueError("Unsupported OS")
    
if __name__ == "__main__":
    if sys.argv[1] == "edit":
        edit_fonts()