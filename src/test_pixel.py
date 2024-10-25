import pyxel
import configparser


config = configparser.ConfigParser(interpolation=None)
config.read("src/configs/config.ini",encoding="utf-8_sig")

init_x = int(config.get("basic","screen_x"))
init_y = int(config.get("basic","screen_y"))
FPS = int(config.get("basic","fps"))
name = config.get("basic","name")

pyxel.init(init_x,init_y,title=name,fps=FPS,quit_key=pyxel.KEY_F9)

class App:
    def __init__(self):
        pyxel.load("../mob2.pyxres")
        pyxel.run(self.update, self.draw)

    def update(self):
        pass

    def draw(self):
        pyxel.bltm(-450,-300,0,0,0,init_x * 4,init_y * 4,0,scale = 0.27)


App()