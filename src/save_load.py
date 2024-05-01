import pyxel
import json
from save import Save

#セーブデータをロードする画面を表示する
class SaveLoad:
    def __init__(self,x,y,ump,over_load):
        self.init_x = x
        self.init_y = y
        self.umplus10 = ump
        self.finger_pos = 0
        self.enter_pos = -1
        self.setting_finger = 1
        self.save_pos = 1
        self.save = Save()
        self.over_load = over_load
        with open("../configs/savedata.json",encoding="utf-8") as f:
            self.save_data = json.load(f)

    def update(self):
        enter_pos = 1
        if pyxel.btnp(pyxel.KEY_UP) and self.setting_finger != 1:
            self.setting_finger -= 1
        if pyxel.btnp(pyxel.KEY_DOWN) and self.setting_finger != 20:
            self.setting_finger += 1
        if pyxel.btnp(pyxel.KEY_LEFT):
            enter_pos = -1
        if pyxel.btnp(pyxel.KEY_RETURN):
            print(self.setting_finger)
            if self.over_load:
                self.save.newsave(self.setting_finger)
        return enter_pos

    def t_update(self):
        enter_pos = 0
        if pyxel.btnp(pyxel.KEY_UP) and self.setting_finger != 1:
            self.setting_finger -= 1
        if pyxel.btnp(pyxel.KEY_DOWN) and self.setting_finger != 20:
            self.setting_finger += 1
        if pyxel.btnp(pyxel.KEY_LEFT):
            enter_pos = -1
        if pyxel.btnp(pyxel.KEY_RETURN):
            print(self.setting_finger)
            if self.over_load:
                self.save.newsave(self.setting_finger)
        return enter_pos

    def draw(self):
        pyxel.rect(70,5,self.init_x-70,self.init_y-5,0)
        pyxel.rectb(70,5,self.init_x-70,self.init_y-5,7)
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