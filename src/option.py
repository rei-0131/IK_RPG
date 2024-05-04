import pyxel
import configparser
from cloud_data import cloud_data

class Option:
    def __init__(self,app,x,y,ump):
        self.app = app
        self.init_x = x
        self.init_y = y
        self.umplus10 = ump
        self.select_pos = 0
        self.enter_pos = -1
        self.cloud = cloud_data(is_test=True)
        if self.app.local:
            self.config = configparser.ConfigParser(interpolation=None)
            self.config.read("configs/config.ini")
            self.now_volume = int(self.config.get("basic","volume"))
        else:
            self.config = self.cloud.config_load()
            self.now_volume = int(self.config["basic"]["volume"])
        self.vol_pos = self.now_volume - 2
        self.vol_finger = self.now_volume

    def volume_update(self):
        if pyxel.btnp(pyxel.KEY_UP or pyxel.GAMEPAD1_BUTTON_DPAD_UP):
            if self.vol_finger != 0:
                self.vol_finger -= 1
        if pyxel.btnp(pyxel.KEY_DOWN or pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
            if self.vol_finger != 7:
                self.vol_finger += 1
        if pyxel.btnp(pyxel.KEY_LEFT or pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
            self.enter_pos = -1
        if pyxel.btnp(pyxel.KEY_RETURN or pyxel.GAMEPAD1_BUTTON_B):
            print(self.vol_finger)
            self.now_volume = self.vol_finger
            if self.app.local:
                self.config.set("basic","volume",str(self.now_volume))
                with open("configs/config.ini","w",encoding="utf-8") as f:
                    self.config.write(f)
            else:
                self.config["basic"]["volume"] = self.now_volume
                self.cloud.config_save(self.config)
            self.app.volume = self.now_volume
            self.enter_pos = -1

    def update(self,enter_pos):
        if self.enter_pos == -1:
            if pyxel.btnp(pyxel.KEY_LEFT or pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
                enter_pos = -1
            if pyxel.btnp(pyxel.KEY_UP or pyxel.GAMEPAD1_BUTTON_DPAD_UP):
                if self.select_pos != 0:
                    self.select_pos -= 11
            if pyxel.btnp(pyxel.KEY_DOWN or pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
                if self.select_pos != 0:
                    self.select_pos += 11
            if pyxel.btnp(pyxel.KEY_RETURN or pyxel.GAMEPAD1_BUTTON_B):
                self.enter_pos = self.select_pos // 11
        elif self.enter_pos == 0:
            self.volume_update()
        return enter_pos

    def volume_draw(self):
        pyxel.rect(self.init_x//2-29,self.init_y//2-25,66,50,0)
        pyxel.rectb(self.init_x//2-29,self.init_y//2-25,66,50,7)
        if self.vol_finger == self.vol_pos + 3:
            self.vol_pos += 1
        elif self.vol_finger == self.vol_pos - 1:
            self.vol_pos -= 1
        for i,l in zip(range(0,3),range(self.vol_pos,4+self.vol_pos)):
            if l == self.vol_finger:
                pyxel.rect(self.init_x//2-29,self.init_y//2-25+(16.66*(i)),66,16.66,1)
                pyxel.rectb(self.init_x//2-29,self.init_y//2-25+(16.66*(i)),66,16.66,7)
            else:
                pyxel.rect(self.init_x//2-29,self.init_y//2-25+(16.66*(i)),66,16.66,0)
                pyxel.rectb(self.init_x//2-29,self.init_y//2-25+(16.66*(i)),66,16.66,7)
            self.umplus10.draw_text(self.init_x//2-29,self.init_y//2-22+int(16.66*(i)),f"     {l}     ",7)

    def draw(self):
        pyxel.rect(71,6+self.select_pos,self.init_x-72,11,1)
        self.umplus10.draw_text(70,6,"音量",7)
        self.umplus10.draw_text(self.init_x-15,6,str(self.now_volume),7)
        if self.enter_pos == 0:
            self.volume_draw()