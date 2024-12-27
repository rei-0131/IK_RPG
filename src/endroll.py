import pyxel
import numpy as np
import json
from utils.BDFRenderer import BDFRenderer

import utils.scenes as scenes

class Endroll:
    """
    エンドロールクラス

    Parameters
    ----------
    app : Any
        appクラスのインスタンス
    x : int
        画面の大きさx
    y : int
        画面の大きさy
    ump10 : Any
        umplus10(日本語出力)
    ump24 : Any
        umplus24(日本語出力)
    """
    def __init__(self,app,x,y,ump10,ump24):
        self.app = app
        self.init_x = x
        self.init_y = y
        self.umplus10 = ump10
        self.umplus24 = ump24
        if self.app.exefile:
            self.endroll_msgs = json.load(open(self.app.resource_path("endroll.json"),"r",encoding="utf-8"))
            self.umplus16 = BDFRenderer(self.app.resource_path("b16.bdf"))
        else:
            self.endroll_msgs = json.load(open("assets/endroll.json","r",encoding="utf-8"))
            self.umplus16 = BDFRenderer("assets/b16.bdf")
        self.roll = True
        self.endroll_pos = []

    def clean(self):
        """初期化"""
        self.endroll_pos = np.array([200 + (i * 33) for i in range(len(self.endroll_msgs))],dtype = np.float64)

    def update(self):
        """基本処理"""
        if self.roll:
            self.endroll_pos -= 0.6
        elif pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
            self.app.now_scene = scenes.MAIN_SCENE
            self.app.player.x = 200
            self.app.player.y = 95
            self.app.msg_id = "480"
            self.app.disp_id = "480"
            self.app.sound_manager.play_se("ok")
        if not True in (self.endroll_pos[0:len(self.endroll_pos) - 1] > 0):
            self.roll = False

    def draw(self):
        """基本描画"""
        pyxel.cls(0)
        for text,pos in zip(self.endroll_msgs,self.endroll_pos):
            try:
                if text[2] == 2 and 0 <= int(pos) <= 176:
                    if len(text) > 4:
                        if int(pos) + text[0] < 88:
                            self.umplus24.draw_text(12 + text[0],88,text[1].center(12,"　"),text[3])
                        else:
                            self.umplus24.draw_text(12 + text[0],int(pos),text[1].center(12,"　"),text[3])
                    else:
                        self.umplus24.draw_text(12 + text[0],int(pos),text[1].center(12,"　"),text[3])
                elif text[2] == 1 and 0 <= int(pos) <= 184:
                    self.umplus16.draw_text(12 + text[0],int(pos),text[1].center(18,"　"),text[3])
                elif text[2] == 0 and 0 <= int(pos) <= 190:
                    self.umplus10.draw_text(16 + text[0],int(pos),text[1].center(28,"　"),text[3])
            except IndexError:
                pass