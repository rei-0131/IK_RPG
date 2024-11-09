import pyxel
import configparser
import json

config = configparser.ConfigParser(interpolation=None)
config.read("src/configs/config.ini",encoding="utf-8_sig")

init_x = int(config.get("basic","screen_x"))
init_y = int(config.get("basic","screen_y"))
FPS = int(config.get("basic","fps"))
name = config.get("basic","name")

pyxel.init(init_x,init_y,title=name,fps=FPS,quit_key=pyxel.KEY_F9)

class App:
    def __init__(self):
        self.scenes = json.load(open("assets/scenes.json","r",encoding="utf-8"))
        self.init_x = init_x
        self.init_y = init_y
        pyxel.load("assets/assets.pyxres")
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btn(pyxel.KEY_UP):
            self.coord[4] -= 2
        if pyxel.btn(pyxel.KEY_DOWN):
            self.coord[4] += 2
        if pyxel.btn(pyxel.KEY_LEFT):
            self.coord[3] -= 2
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.coord[3] += 2
        if pyxel.btn(pyxel.KEY_W):
            self.coord[6] -= 2
        if pyxel.btn(pyxel.KEY_S):
            self.coord[6] += 2
        if pyxel.btn(pyxel.KEY_A):
            self.coord[5] -= 2
        if pyxel.btn(pyxel.KEY_D):
            self.coord[5] += 2
        if pyxel.btn(pyxel.KEY_T):
            self.coord[1] -= 2
        if pyxel.btn(pyxel.KEY_G):
            self.coord[1] += 2
        if pyxel.btn(pyxel.KEY_F):
            self.coord[0] -= 2
        if pyxel.btn(pyxel.KEY_H):
            self.coord[0] += 2
        if pyxel.btn(pyxel.KEY_1):
            self.coord[8] -= 0.01
        if pyxel.btn(pyxel.KEY_2):
            self.coord[8] += 0.01

    def draw(self):
        pyxel.cls(0)
        self.coord = self.scenes["coordinate"][str(8)]
        self.scale = self.coord[8]
        print(f"{self.coord[0]} {self.coord[1]} {self.coord[3]} {self.coord[4]} {self.coord[5]} {self.coord[6]} {self.coord[8]}",end="\r")
        pyxel.bltm(self.coord[0],self.coord[1],self.coord[2],self.coord[3],self.coord[4],self.coord[5],self.coord[6],self.coord[7],scale = self.scale)


App()