import pyxel
from cloud_data import Cloud_data
import configparser

class Option:
    """
    詳細設定に関するクラス

    Parameters
    ----------
    app : Any
        Appクラスのインスタンス
    x : int
        画面の大きさx
    y : int
        画面の大きさy
    ump : Any
        umplus10(日本語出力)
    """
    def __init__(self,app,x,y,ump):
        self.app = app
        self.init_x = x
        self.init_y = y
        self.umplus10 = ump
        self.select_pos = 0
        self.enter_pos = -1
        self.cloud = Cloud_data(self.app.is_test)
        self.config = self.app.config
        if self.app.local:
            self.config = configparser.ConfigParser(interpolation=None)
            self.config.read("configs/config.ini",encoding="utf-8_sig")
            self.now_volume = int(self.config.get("basic","volume"))
        else:
            self.config = self.cloud.config_load()
            self.now_volume = int(self.config["basic"]["volume"])
        self.vol_pos = self.now_volume - 2
        self.vol_finger = self.now_volume

    def volume_update(self):
        """音量操作の処理"""
        if pyxel.btnp(pyxel.KEY_UP,hold = 8,repeat=8) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP,hold = 8,repeat=8):
            if self.vol_finger != 0:
                self.vol_finger -= 1
        if pyxel.btnp(pyxel.KEY_DOWN,hold = 8,repeat=8) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN,hold = 8,repeat=8):
            if self.vol_finger != 7:
                self.vol_finger += 1
        if pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
            print(self.vol_finger)
            self.now_volume = self.vol_finger
            if self.app.local:
                self.config.set("basic","volume",str(self.now_volume))
                with open("configs/config.ini","w",encoding="utf-8") as f:
                    self.config.write(f)
            else:
                self.config["basic"]["volume"] = self.now_volume
                self.cloud.config_save(self.config)
            self.app.cloud = self.cloud
            self.app.volume = self.now_volume
            self.enter_pos = -1

    def update(self,enter_pos) -> int:
        """オプション更新"""
        if self.enter_pos == -1:
            if pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
                enter_pos = -1
            if pyxel.btnp(pyxel.KEY_UP,hold = 8,repeat=8) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP,hold = 8,repeat=8):
                if self.select_pos != 0:
                    self.select_pos -= 11
            if pyxel.btnp(pyxel.KEY_DOWN,hold = 8,repeat=8) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN,hold = 8,repeat=8):
                if self.select_pos != 0:
                    self.select_pos += 11
            if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
                self.enter_pos = self.select_pos // 11
        elif self.enter_pos == 0:
            self.volume_update()
        return enter_pos

    def volume_draw(self):
        """音量操作の描画"""
        pyxel.rect(71,6+self.select_pos,self.init_x-72,11,1)
        self.umplus10.draw_text(70,6,"音量",7)
        self.umplus10.draw_text(self.init_x-15,6,str(self.vol_finger),7)
        if self.vol_finger == 7:
            pyxel.tri(self.init_x-18,6,self.init_x-8,6,self.init_x-13,3,7)
        elif self.vol_finger == 0:
            pyxel.tri(self.init_x-18,16,self.init_x-8,16,self.init_x-13,18,7)
        else:
            pyxel.tri(self.init_x-18,6,self.init_x-8,6,self.init_x-13,3,7)
            pyxel.tri(self.init_x-18,16,self.init_x-8,16,self.init_x-13,18,7)

    def draw(self):
        """オプション描画"""
        pyxel.rect(71,6+self.select_pos,self.init_x-72,11,1)
        self.umplus10.draw_text(70,6,"音量",7)
        self.umplus10.draw_text(self.init_x-15,6,str(self.now_volume),7)
        if self.enter_pos == 0:
            self.volume_draw()