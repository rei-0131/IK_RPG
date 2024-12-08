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
        self.endroll_pos = np.array([290 + (i * 33) for i in range(len(self.endroll_msgs))],dtype = np.float64)

    def update(self):
        self.endroll_pos -= 0.3

    def draw(self):
        pyxel.cls(0)
        for text,pos in zip(self.endroll_msgs,self.endroll_pos):
            try:
                if 0 <= int(pos) <= 290:
                    if text[1] == 1:
                        self.umplus24.draw_text(10,int(pos),text[0].center(12,"　"),text[2])
                    elif text[1] == 0:
                        self.umplus10.draw_text(5,int(pos),text[0].center(28,"　"),text[2])
            except IndexError:
                pass