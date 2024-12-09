import pyxel
import numpy as np
import json

class Endroll:
    def __init__(self,app,x,y,ump10,ump24):
        self.app = app
        self.init_x = x
        self.init_y = y
        self.umplus10 = ump10
        self.umplus24 = ump24
        self.endroll_msgs = json.load(open("assets/endroll.json","r",encoding="utf-8"))
        self.endroll_pos = []

    def crean(self):
        self.endroll_pos = np.array([200 + (i * 33) for i in range(len(self.endroll_msgs))],dtype = np.float64)

    def update(self):
        self.endroll_pos -= 0.3

    def draw(self):
        pyxel.cls(0)
        pyxel.line(self.init_x // 2,0,self.init_x // 2,self.init_y,7)
        pyxel.line(0,self.init_y // 2,self.init_x,self.init_y // 2,7)
        for text,pos in zip(self.endroll_msgs,self.endroll_pos):
            try:
                if text[2] == 1 and 0 <= int(pos) <= 176:
                    self.umplus24.draw_text(12,int(pos) + text[0],text[1].center(12,"　"),text[3])
                elif text[2] == 0 and 0 <= int(pos) <= 190:
                    self.umplus10.draw_text(11,int(pos) + text[0],text[1].center(28,"　"),text[3])
            except IndexError:
                pass