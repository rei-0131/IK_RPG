import pyxel
import json
from save import Save

class Setting:
    def __init__(self,x,y,ump):
        self.init_x = x
        self.init_y = y
        self.umplus10 = ump
        self.finger_pos = 0
        self.enter_pos = -1
        self.setting_finger = 1
        self.save_pos = 1
        with open("../configs/savedata.json",encoding="utf-8") as f:
            self.save_data = json.load(f)
        self.save = Save()

    def save_update(self):
        if pyxel.btnp(pyxel.KEY_UP) and self.setting_finger != 1:
            self.setting_finger -= 1
        if pyxel.btnp(pyxel.KEY_DOWN) and self.setting_finger != 20:
            self.setting_finger += 1
        if pyxel.btnp(pyxel.KEY_LEFT):
            self.enter_pos = -1
        if pyxel.btnp(pyxel.KEY_RETURN):
            print(self.setting_finger)

    def update(self):
        if self.enter_pos == -1:
            if pyxel.btnp(pyxel.KEY_UP):
                if self.finger_pos != 0:
                    self.finger_pos -= 11
            elif pyxel.btnp(pyxel.KEY_DOWN):
                if self.finger_pos != 77:
                    self.finger_pos += 11
            elif pyxel.btnp(pyxel.KEY_RETURN):
                self.enter_pos = self.finger_pos//11
                print(self.enter_pos)
        elif self.enter_pos == 7:
            pyxel.quit()
        elif self.enter_pos == 6:
            self.save_update()

    def save_draw(self):
        if self.setting_finger == self.save_pos + 4:
            self.save_pos += 1
        elif self.setting_finger == self.save_pos - 1:
            self.save_pos -= 1
        for i,l in zip(range(0,4),range(self.save_pos,4+self.save_pos)):
            if l == self.setting_finger:
                pyxel.rect(70,5+(48.75*(i)),self.init_x-70,48.75,1)
                pyxel.rectb(70,5+(48.75*(i)),self.init_x-70,48.75,7)
            else:
                pyxel.rect(70,5+(48.75*(i)),self.init_x-70,48.75,0)
                pyxel.rectb(70,5+(48.75*(i)),self.init_x-70,48.75,7)
            self.umplus10.draw_text(71,5+int(48.75*(i)),f"data {l}",7)
            if str(l) in self.save_data:
                self.umplus10.draw_text(200,6+int(48.75*(i)),f"time:{self.save_data[str(l)]['play_data']['time']}",7)
            else:
                self.umplus10.draw_text(125,25+int(48.75*(i)),f"保存データなし",7)
            # if str(l) in self.save_data:
            #     print(self.save_data[str(l)]["play_data"])
            # else:
            #     self.save_data[str(l)]["play_data"] = {}

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
        if self.enter_pos == 6:
            self.save_draw()