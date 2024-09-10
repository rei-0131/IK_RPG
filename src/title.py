import pyxel
import time
import json
from save_load import SaveLoad

class Title:
    """
    タイトルに関するクラス

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
        self.question_mark = 0
        self.game_start = -1
        self.umplus10 = ump
        self.scenes = self.app.scenes
        self.MAIN_SCENE = self.scenes["MAIN_SCENE"]
        self.TITLE_SCENE = self.scenes["TITLE_SCENE"]
        self.Continue = self.scenes["LOAD_SCENE"]
        self.setting_scene = self.scenes["OUT_SETTING_SCENE"]
        self.save_load = SaveLoad(self.init_x,self.init_y,self.umplus10,False,app=self.app)
        self.save_data = None
        self.enter_pos = 1
        self.setting = self.app.setting_out

    def update(self):
        """基本処理"""
        if pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
            if self.question_mark != -18:
                self.question_mark -= 9
        if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
            if self.question_mark != 0:
                self.question_mark += 9
        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B) or pyxel.btnp(pyxel.KEY_RIGHT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
            self.enter_pos = self.question_mark // 9
            if self.enter_pos == 0:
                self.app.new_game = True
                self.app.game_time_start = time.time()
                return self.MAIN_SCENE
            elif self.enter_pos == -1:
                self.app.save_load.save_data = self.app.save_data
                self.app.new_game = True
                return self.Continue
            elif self.enter_pos == -2:
                self.app.setting_out.option.now_volume = self.app.volume
                self.app.setting_out.option.vol_finger = self.app.volume
                return self.setting_scene

    def draw(self):
        """基本描画"""
        pyxel.cls(0)
        self.umplus10.draw_text(90,100,"     一工クエスト     ",7)
        self.umplus10.draw_text(103,110,"-   New Game   -",7)
        self.umplus10.draw_text(103,120,"-   Continue   -",7)
        self.umplus10.draw_text(103,130,"-   Settings   -",7)
        self.umplus10.draw_text(103,150,"-  PRESS Enter -",7)
        pyxel.blt(self.init_x-217,self.init_y-88-self.question_mark,0,15,0,15,15,0)