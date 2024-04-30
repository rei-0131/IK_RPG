import pyxel
import json
from BDFRenderer import BDFRenderer

class Title:
    def __init__(self,x,y):
        self.init_x = x
        self.init_y = y
        self.question_mark = 0
        self.game_start = -1
        self.umplus10 = BDFRenderer("../assets/umplus_j10r.bdf")
        with open("../assets/scenes.json",encoding="utf-8") as f:
            self.scenes = json.loads(f.read())
        self.MAIN_SCENE = self.scenes["MAIN_SCENE"]
        self.TITLE_SCENE = self.scenes["TITLE_SCENE"]

    def update(self):
        if pyxel.btnp(pyxel.KEY_DOWN):
            if self.question_mark != -9:
                self.question_mark -= 9
        if pyxel.btnp(pyxel.KEY_UP):
            if self.question_mark != 0:
                self.question_mark += 9
        if pyxel.btnp(pyxel.KEY_RETURN):
            if self.question_mark // 9 == 0:
                self.game_start = 0
            elif self.game_start // 9 == 1:
                self.game_start = 1
        if pyxel.btnp(pyxel.KEY_RETURN):
            return self.MAIN_SCENE
        else:
            return self.TITLE_SCENE

    def draw(self):
        pyxel.cls(0)
        self.umplus10.draw_text(100,100,"     Title     ",7)
        self.umplus10.draw_text(100,110,"-   New Game  -",7)
        self.umplus10.draw_text(100,120,"-   Continue  -",7)
        self.umplus10.draw_text(100,150,"- PRESS Enter -",7)
        pyxel.blt(self.init_x-220,self.init_y-88-self.question_mark,0,15,0,30,15,0)