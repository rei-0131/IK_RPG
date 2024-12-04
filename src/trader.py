import pyxel

class Trader:
    def __init__(self,app,x,y,ump):
        self.app = app
        self.init_x = x
        self.init_y = y
        self.umplus10 = ump
        self.buy_equip_type = False
        self.buy_question = False
        self.finger_ad = self.app.assets_info["finger_ad"]
        self.equip_en = ["head","armor","leggings","boots","sword","shield","staff","other"]
        self.equip_jp = ["ヘルメット","アーマー","レギンス","ブーツ","剣","盾","杖","他"]
        self.finger_pos = 0
        self.buy_select = 0
        self.conf = True
        self.type = 0
        self.disp_select = 0

    def update(self):
        if not self.buy_equip_type:
            if pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
                self.app.trade = False
            if (pyxel.btnp(pyxel.KEY_UP,hold = 8,repeat=8) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP,hold = 8,repeat=8)):
                if self.finger_pos == 0:
                    self.finger_pos = 77
                else:
                    self.finger_pos -= 11
            if (pyxel.btnp(pyxel.KEY_DOWN,hold = 8,repeat=8) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN,hold = 8,repeat=8)):
                if self.finger_pos == 77:
                    self.finger_pos = 0
                else:
                    self.finger_pos += 11
            if (pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B)):
                self.buy_equip_type = True
                if self.finger_pos == 0:
                    self.type = 0
                else:
                    self.type = self.finger_pos // 11
        else:
            if not self.buy_question:
                if pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
                    self.buy_equip_type = False
                if (pyxel.btnp(pyxel.KEY_UP,hold = 8,repeat=8) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP,hold = 8,repeat=8)):
                    if self.buy_select != 0:
                        self.buy_select -= 1
                        if self.disp_select != 0:
                            self.disp_select -= 1
                if (pyxel.btnp(pyxel.KEY_DOWN,hold = 8,repeat=8) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN,hold = 8,repeat=8)):
                    if self.buy_select != len(list(self.app.tools[self.equip_en[self.type]].keys())) - 1:
                        self.buy_select += 1
                        if self.disp_select != 3:
                            self.disp_select += 1
                if (pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B)):
                    self.buy_question = True
            else:
                if pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
                    self.buy_question = False
                if pyxel.btnp(pyxel.KEY_RIGHT,hold = 8,repeat=8) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT,hold = 8,repeat=8):
                    if self.conf:
                        self.conf = False
                    else:
                        self.conf = True
                if pyxel.btnp(pyxel.KEY_LEFT,hold = 8,repeat=8) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT,hold = 8,repeat=8):
                    if self.conf:
                        self.conf = False
                    else:
                        self.conf = True
                if (pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B)):
                    if self.conf:
                        self.app.money -= self.app.tools[self.equip_en[self.type]][self.buy_select][5]
                        self.app.equip_codes[self.equip_en[self.type]].append(self.app.tools[self.equip_en[self.type]][self.buy_select][0])
                    else:
                        self.buy_question = False

    def draw(self):
        pyxel.rect(18,5,65,89,0)
        pyxel.rectb(18,5,65,89,7)
        for i,j in enumerate(self.equip_jp):
            self.umplus10.draw_text(19,6 + i * 11,j,7)
        pyxel.blt(0,5+self.finger_pos,self.finger_ad[0],self.finger_ad[1],self.finger_ad[2],self.finger_ad[3],self.finger_ad[4],self.finger_ad[5])
        pyxel.rect(5,self.init_y-12,66,12,0)
        pyxel.rectb(5,self.init_y-12,66,12,7)
        pyxel.rect(70,5,self.init_x-70,self.init_y-5,0)
        pyxel.rectb(70,5,self.init_x-70,self.init_y-5,7)
        self.umplus10.draw_text(5,self.init_y-11,f"￥{self.app.money}".rjust(8,"　"),7)
        if len(list(self.app.tools[self.equip_en[self.type]].keys())) > 4:
            for i,t in enumerate(list(self.app.tools[self.equip_en[self.type]].keys())[self.buy_select - self.disp_select:self.buy_select + 4 - self.disp_select]):
                info = self.app.tools[self.equip_en[self.type]][t]
                if i == self.disp_select:
                    pyxel.rect(70,5+(48.75*(i)),self.init_x-70,48.75,1)
                    pyxel.rectb(70,5+(48.75*(i)),self.init_x-70,48.75,7)
                else:
                    pyxel.rect(70,5+(48.75*(i)),self.init_x-70,48.75,0)
                    pyxel.rectb(70,5+(48.75*(i)),self.init_x-70,48.75,7)
                self.umplus10.draw_text(71,int(6 + (49 * i)),info[0],7)
        else:
            for i,t in enumerate(self.app.tools[self.equip_en[self.type]]):
                info = self.app.tools[self.equip_en[self.type]][t]
                if i == self.disp_select:
                    pyxel.rect(70,5+(48.75*(i)),self.init_x-70,48.75,1)
                    pyxel.rectb(70,5+(48.75*(i)),self.init_x-70,48.75,7)
                else:
                    pyxel.rect(70,5+(48.75*(i)),self.init_x-70,48.75,0)
                    pyxel.rectb(70,5+(48.75*(i)),self.init_x-70,48.75,7)
                self.umplus10.draw_text(71,int(6 + (49 * i)),info[0],7)
        if self.buy_question:
            pyxel.rect(100,80,100,40,0)
            pyxel.rectb(100,80,100,40,7)
            self.umplus10.draw_text(101,81,"購入しますか？",7)
            self.umplus10.draw_text(101,102,"はい",7)
            self.umplus10.draw_text(151,102,"いいえ",7)