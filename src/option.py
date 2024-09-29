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
        return enter_pos

    def draw(self):
        """オプション描画"""
        pyxel.rect(71,6+self.select_pos,self.init_x-72,11,1)