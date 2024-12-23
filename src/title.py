import pyxel
import time

import utils.scenes as scenes
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
        self.MAIN_SCENE = scenes.MAIN_SCENE
        self.TITLE_SCENE = scenes.TITLE_SCENE
        self.Continue = scenes.LOAD_SCENE
        self.setting_scene = scenes.OUT_SETTING_SCENE
        self.save_load = SaveLoad(self.init_x,self.init_y,self.umplus10,False,app=self.app)
        self.save_data = None
        self.enter_pos = 1
        self.finger_ad = self.app.assets_info["finger_ad"]

    def update(self):
        """基本処理"""
        if pyxel.btnp(pyxel.KEY_DOWN,hold = 8,repeat=8) or pyxel.btnp(pyxel.KEY_S,hold = 8,repeat=8) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN,hold = 8,repeat=8):
            if self.question_mark != -15:
                self.question_mark -= 15
            else:
                self.question_mark = 0
            self.app.sound_manager.play_se("select")
        if pyxel.btnp(pyxel.KEY_UP,hold = 8,repeat=8) or pyxel.btnp(pyxel.KEY_W,hold = 8,repeat=8) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP,hold = 8,repeat=8):
            if self.question_mark != 0:
                self.question_mark += 15
            else:
                self.question_mark = -15
            self.app.sound_manager.play_se("select")
        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B) or pyxel.btnp(pyxel.KEY_RIGHT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
            self.enter_pos = self.question_mark // 15
            if self.enter_pos == 0:
                self.app.new_game = True
                self.app.game_time_start = time.time()
                self.app.sound_manager.play_se("ok")
                return self.MAIN_SCENE
            elif self.enter_pos == -1:
                self.app.save_load.save_data = self.app.save_data
                self.app.new_game = True
                self.app.sound_manager.play_se("ok")
                return self.Continue

    def draw(self):
        """基本描画"""
        pyxel.cls(0)
        pyxel.blt(-426,-300,self.app.title_logo,0,0,1153,769,scale = 0.1)
        self.umplus10.draw_text(103,110,"-   New Game   -",7)
        self.umplus10.draw_text(103,125,"-   Continue   -",7)
        self.umplus10.draw_text(103,150,"-  PRESS Enter -",7)
        pyxel.blt(self.init_x-217,self.init_y-90-self.question_mark,self.finger_ad[0],self.finger_ad[1],self.finger_ad[2],self.finger_ad[3],self.finger_ad[4],self.finger_ad[5])