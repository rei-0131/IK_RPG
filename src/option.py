import pyxel

class Option:
    def __init__(self,x,y,ump):
        self.init_x = x
        self.init_y = y
        self.umplus10 = ump

    def update(self,enter_pos):
        if pyxel.btnp(pyxel.KEY_LEFT):
            enter_pos = -1
        return enter_pos

    def draw(self):
        self.umplus10.draw_text(70,6,"音量",7)