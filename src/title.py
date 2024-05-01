import pyxel
import json
from BDFRenderer import BDFRenderer
from save_load import SaveLoad
from setting import Out_Setting

class Title:
    def __init__(self,x,y):
        self.init_x = x
        self.init_y = y
        self.question_mark = 0
        self.game_start = -1
        self.umplus10 = BDFRenderer("../assets/umplus_j10r.bdf")
        with open("../assets/scenes.json",encoding="utf-8") as f:
            self.scenes = json.load(f)
        self.MAIN_SCENE = self.scenes["MAIN_SCENE"]
        self.TITLE_SCENE = self.scenes["TITLE_SCENE"]
        self.save_load = SaveLoad(self.init_x,self.init_y,self.umplus10,False)
        self.save_data = None
        self.enter_pos = 1
        self.setting = Out_Setting(self.init_x,self.init_y,self.umplus10)

    def update(self):
        if pyxel.btnp(pyxel.KEY_DOWN):
            if self.question_mark != -18:
                self.question_mark -= 9
        if pyxel.btnp(pyxel.KEY_UP):
            if self.question_mark != 0:
                self.question_mark += 9
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.enter_pos = self.question_mark // 9
            if self.enter_pos == 0:
                return 1
            elif self.enter_pos == -1:
                return 3
            elif self.enter_pos == -2:
                return 2

    def draw(self):
        pyxel.cls(0)
        self.umplus10.draw_text(100,100,"     Title     ",7)
        self.umplus10.draw_text(100,110,"-   New Game  -",7)
        self.umplus10.draw_text(100,120,"-   Continue  -",7)
        self.umplus10.draw_text(100,130,"-   Settings  -",7)
        self.umplus10.draw_text(100,150,"- PRESS Enter -",7)
        pyxel.blt(self.init_x-220,self.init_y-88-self.question_mark,0,15,0,30,15,0)