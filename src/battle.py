import pyxel
import sklearn

#バトル画面の表示と処理
class Battle:
    """
    バトルに関するクラス

    Parameters:
    x :int
        画面の大きさx
    y : int
        画面の大きさy
    ump : Any
        umplus10(日本語出力)
    app : Any
        Appクラスのインスタンス
    """
    def __init__(self,x,y,ump,app):
        self.app = app
        self.init_x = x
        self.init_y = y
        self.username = "ぼく"
        self.umplus10 = ump
        self.select_num1 = -1
        self.finger_pos1 = 0
        self.select_num2 = -1
        self.finger_pos2 = 0

    def fight_update(self):
        if pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
            self.select_num2 = -1

    def magic_update(self):
        if pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
            self.select_num2 = -1

    def item_update(self):
        if pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
            self.select_num1 = -1

    def update(self):
        if self.select_num1 == -1:
            if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
                if self.finger_pos1 != 0:
                    self.finger_pos1 -= 20
            if pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
                if self.finger_pos1 != 60:
                    self.finger_pos1 += 20
            if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B) or pyxel.btnp(pyxel.KEY_RIGHT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
                self.select_num1 = int(self.finger_pos1 // 20)
                self.select_num2 = -1
                print(self.select_num1)
        elif self.select_num1 != 3:
            if self.select_num2 == -1:
                if self.select_num1 == 0 or self.select_num1 == 1:
                    if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
                        if self.finger_pos2 != 0:
                            self.finger_pos2 -= 18
                    if pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
                        if self.finger_pos2 != (len(self.app.chara_data.items()) - 1) * 18:
                            self.finger_pos2 += 18
                    if pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
                        self.select_num1 = -1
                    if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B) or pyxel.btnp(pyxel.KEY_RIGHT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
                        self.select_num2 = int(self.finger_pos2 // 18)
                        print(self.select_num2)
                elif self.select_num1 == 2:
                    self.item_update()
            else:
                if self.select_num1 == 0:
                    self.fight_update()
                elif self.select_num1 == 1:
                    self.magic_update()

    def fight_draw(self):
        pyxel.rect(110,self.init_y//2+10,185,75,0)
        pyxel.rectb(110,self.init_y//2+10,185,75,7)

    def magic_draw(self):
        pyxel.rect(110,self.init_y//2+10,185,75,0)
        pyxel.rectb(110,self.init_y//2+10,185,75,7)

    def item_draw(self):
        pyxel.rect(110,self.init_y//2+10,185,75,0)
        pyxel.rectb(110,self.init_y//2+10,185,75,7)

    def draw(self):
        pyxel.cls(0)
        pyxel.rect(25,self.init_y//2+10,75,75,0)
        pyxel.rectb(25,self.init_y//2+10,75,75,7)
        pyxel.rect(30,self.init_y//2+10,65,4,0)
        pyxel.rect(110,self.init_y//2+10,185,75,0)
        pyxel.rectb(110,self.init_y//2+10,185,75,7)
        for i,data in zip(range(1,1+len(self.app.chara_data.items())),self.app.chara_data):
            height = 18*(i - 1)
            if self.select_num1 != 0 and self.select_num1 != 1:
                self.umplus10.draw_text(115,self.init_y//2+15+height,data,7)
            else:
                self.umplus10.draw_text(130,self.init_y//2+15+height,data,7)
            pyxel.text(172,self.init_y//2+14+height,"HP",7)
            pyxel.text(172,self.init_y//2+21+height,"MP",7)
            pyxel.rect(180,self.init_y//2+14+height,(self.app.chara_data[data]["HP"][1]/self.app.chara_data[data]["HP"][0])*100,5,11)
            pyxel.rectb(180,self.init_y//2+14+height,100,5,7)
            pyxel.text(281,self.init_y//2+14+height,f"{self.app.chara_data[data]['HP'][1]}",11)
            pyxel.rect(180,self.init_y//2+21+height,(self.app.chara_data[data]["MP"][1]/self.app.chara_data[data]["MP"][0])*100,5,5)
            pyxel.rectb(180,self.init_y//2+21+height,100,5,7)
            pyxel.text(281,self.init_y//2+21+height,f"{self.app.chara_data[data]['MP'][1]}",5)
        self.umplus10.draw_text(26,self.init_y//2+15,"たたかう",7)
        self.umplus10.draw_text(26,self.init_y//2+35,"まほう",7)
        self.umplus10.draw_text(26,self.init_y//2+55,"どうぐ",7)
        self.umplus10.draw_text(26,self.init_y//2+75,"にげる",7)
        pyxel.blt(7,self.init_y//2+15+(self.finger_pos1),0,16,0,16,16,0)
        if self.select_num1 == 0:
            pyxel.blt(112,self.init_y//2+15+(self.finger_pos2),0,16,0,16,16,0)
            if self.select_num2 != -1:
                self.fight_draw()
        elif self.select_num1 == 1:
            pyxel.blt(112,self.init_y//2+15+(self.finger_pos2),0,16,0,16,16,0)
            if self.select_num2 != -1:
                self.magic_draw()
        elif self.select_num1 == 2:
            self.item_draw()
        elif self.select_num1 == 3:
            pass