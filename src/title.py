import pyxel
import json
from BDFRenderer import BDFRenderer

class Title:
    def __init__(self):
        self.umplus10 = BDFRenderer("../assets/umplus_j10r.bdf")
        with open("../configs/scenes.json",encoding="utf-8") as f:
            self.scenes = json.loads(f.read())
        self.MAIN_SCENE = self.scenes["MAIN_SCENE"]
        self.TITLE_SCENE = self.scenes["TITLE_SCENE"]

    def update(self):
        if pyxel.btn(pyxel.KEY_RETURN):
            return self.MAIN_SCENE
        else:
            return self.TITLE_SCENE

    def draw(self):
        pyxel.cls(0)
        self.umplus10.draw_text(250,200,"     Title     ",7)
        self.umplus10.draw_text(250,300,"- PRESS Enter -")