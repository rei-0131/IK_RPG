import pyxel
from save import Save

class Setting:
    def __init__(self,x,y,ump):
        self.init_x = x
        self.init_y = y
        self.umplus10 = ump
        self.finger_pos = 0
        self.enter_pos = -1
        self.save = Save()

    def update(self):
        if pyxel.btnp(pyxel.KEY_UP):
            if self.finger_pos != 0:
                self.finger_pos -= 11
        elif pyxel.btnp(pyxel.KEY_DOWN):
            if self.finger_pos != 77:
                self.finger_pos += 11
        elif pyxel.btnp(pyxel.KEY_RETURN):
            self.enter_pos = self.finger_pos//11
            print(self.enter_pos)
            if self.enter_pos == 7:
                pyxel.quit()

    def draw(self):
        pyxel.cls(0)
        pyxel.rect(18,5,65,95,0)
        pyxel.rectb(18,5,65,95,7)
        pyxel.rect(70,5,self.init_x-70,self.init_y-5,0)
        pyxel.rectb(70,5,self.init_x-70,self.init_y-5,7)
        pyxel.blt(0,5+self.finger_pos,0,15,0,30,15,0)
        self.umplus10.draw_text(18,6,"アイテム",7)
        self.umplus10.draw_text(18,17,"スキル",7)
        self.umplus10.draw_text(18,28,"装備",7)
        self.umplus10.draw_text(18,39,"ステータス",7)
        self.umplus10.draw_text(18,50,"並び替え",7)
        self.umplus10.draw_text(18,61,"オプション",7)
        self.umplus10.draw_text(18,72,"セーブ",7)
        self.umplus10.draw_text(18,83,"ゲーム終了",7)