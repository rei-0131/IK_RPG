import pyxel
import json
import time
import os

import utils.scenes as scenes
from save import Save
from cloud_data import Cloud_data

#セーブデータをロードする画面を表示する
class SaveLoad:
    """
    セーブデータロード画面を表示

    Parameters
    ----------
    x : int
        画面のinit_x
    y : int
        画面のinit_y
    ump : Any
        umplus10(日本語出力)
    over_load : bool
        セーブデータの上書きが可能か
    left : bool
        左キーを押した際一つ前の動作に戻るかタイトルに戻るか
    load : bool
        セーブデータ、ロードオンリーかどうか
    app : Any
        Appクラスのself
    """
    def __init__(self,x,y,ump,over_load,left=True,load=False,app = None):
        self.app = app
        self.init_x = x
        self.init_y = y
        self.umplus10 = ump
        self.finger_pos = 0
        self.enter_pos = -1
        self.setting_finger = 1
        self.save_pos = 1
        self.save = Save(self.app)
        self.left = left
        self.over_load = over_load
        self.continue_game = False
        self.load = load
        self.cloud = Cloud_data(self.app.is_test)
        self.over_tf = False
        self.save_enter = -1
        self.save_path = os.path.join(self.app.base_path,"save/savedata.json")
        if self.app.local:
            if self.app.exefile:
                self.save_data = json.load(open(self.save_path,"r",encoding="utf-8"))
            else:
                self.save_data = json.load(open("../save/savedata.json","r",encoding="utf-8"))
        else:
            self.save_data = self.cloud.load()
        self.first_show = True
        self.load = scenes.LOAD_SCENE
        self.title = scenes.TITLE_SCENE
        self.main = scenes.MAIN_SCENE

    def update(self,ent=None,battle_load = False) -> int:
        """
        基本処理

        Parameters
        ent:int
            不明
        """
        if not battle_load:
            if self.first_show:
                if self.app.local:
                    if self.app.exefile:
                        self.save_data = json.load(open(self.save_path,"r",encoding="utf-8"))
                    else:
                        self.save_data = json.load(open("../save/savedata.json","r",encoding="utf-8"))
                else:
                    self.save_data = self.cloud.load()
                self.first_show = False
            if self.left:
                enter_pos = ent
                if self.save_enter == -1:
                    if pyxel.btnp(pyxel.KEY_ESCAPE) or pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.KEY_A) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
                        enter_pos = -1
                        self.first_show = True
                        self.app.sound_manager.play_se("select")
                    if pyxel.btnp(pyxel.KEY_UP,hold = 8,repeat=8) or pyxel.btnp(pyxel.KEY_W,hold = 8,repeat=8) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP,hold = 8,repeat=8):
                        if self.setting_finger != 1:
                            self.setting_finger -= 1
                            self.app.sound_manager.play_se("select")
                    if pyxel.btnp(pyxel.KEY_DOWN,hold = 8,repeat=8) or pyxel.btnp(pyxel.KEY_S,hold = 8,repeat=8) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN,hold = 8,repeat=8):
                        if self.setting_finger != 20:
                            self.setting_finger += 1
                            self.app.sound_manager.play_se("select")
                    if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
                        print(f"{self.setting_finger=}")
                        if self.over_load:
                            if str(self.setting_finger) in self.save_data:
                                self.save_enter = self.setting_finger
                            else:
                                self.save.newsave(self.setting_finger)
                                if self.app.local:
                                    if self.app.exefile:
                                        self.save_data = json.load(open(self.save_path,"r",encoding="utf-8"))
                                    else:
                                        self.save_data = json.load(open("../save/savedata.json","r",encoding="utf-8"))
                                else:
                                    self.save_data = self.cloud.load()
                            self.app.sound_manager.play_se("ok")
                else:
                    if pyxel.btnp(pyxel.KEY_ESCAPE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
                        self.save_enter = -1
                        self.app.sound_manager.play_se("select")
                    if pyxel.btnp(pyxel.KEY_RIGHT,hold = 8,repeat=8) or pyxel.btnp(pyxel.KEY_D,hold = 8,repeat=8) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT,hold = 8,repeat=8):
                        if self.over_tf:
                            self.over_tf = False
                        else:
                            self.over_tf = True
                        self.app.sound_manager.play_se("select")
                    if pyxel.btnp(pyxel.KEY_LEFT,hold = 8,repeat=8) or pyxel.btnp(pyxel.KEY_A,hold = 8,repeat=8) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT,hold = 8,repeat=8):
                        if self.over_tf:
                            self.over_tf = False
                        else:
                            self.over_tf = True
                        self.app.sound_manager.play_se("select")
                    if (pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B)):
                        if self.over_tf:
                            self.save.newsave(self.save_enter)
                            if self.app.local:
                                if self.app.exefile:
                                    self.save_data = json.load(open(self.save_path,"r",encoding="utf-8"))
                                else:
                                    self.save_data = json.load(open("../save/savedata.json","r",encoding="utf-8"))
                            else:
                                self.save_data = self.cloud.load()
                        self.save_enter = -1
                        self.app.sound_manager.play_se("ok")
                return enter_pos
            else:
                enter_pos = self.load
                if self.save_enter == -1:
                    if pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.KEY_ESCAPE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
                        enter_pos = self.title
                        self.first_show = True
                        self.app.sound_manager.play_se("select")
                    if pyxel.btnp(pyxel.KEY_UP,hold = 8,repeat=8) or pyxel.btnp(pyxel.KEY_W,hold = 8,repeat=8) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP,hold = 8,repeat=8):
                        if self.setting_finger != 1:
                            self.setting_finger -= 1
                            self.app.sound_manager.play_se("select")
                    if pyxel.btnp(pyxel.KEY_DOWN,hold = 8,repeat=8) or pyxel.btnp(pyxel.KEY_S,hold = 8,repeat=8) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN,hold = 8,repeat=8):
                        if self.setting_finger != 20:
                            self.setting_finger += 1
                            self.app.sound_manager.play_se("select")
                    if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
                        print(f"{self.setting_finger=}")
                        if self.load:
                            if str(self.setting_finger) in self.save_data:
                                self.continue_game = True
                                enter_pos = self.main
                        if self.over_load:
                            if str(self.setting_finger) in self.save_data:
                                self.save_enter = self.setting_finger
                            else:
                                self.save.newsave(self.setting_finger)
                        self.app.sound_manager.play_se("ok")
                else:
                    if pyxel.btnp(pyxel.KEY_ESCAPE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
                        self.save_enter = -1
                        self.app.sound_manager.play_se("select")
                    if pyxel.btnp(pyxel.KEY_RIGHT,hold = 8,repeat=8) or pyxel.btnp(pyxel.KEY_D,hold = 8,repeat=8) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT,hold = 8,repeat=8):
                        if self.over_tf:
                            self.over_tf = False
                        else:
                            self.over_tf = True
                        self.app.sound_manager.play_se("select")
                    if pyxel.btnp(pyxel.KEY_LEFT,hold = 8,repeat=8) or pyxel.btnp(pyxel.KEY_A,hold = 8,repeat=8) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT,hold = 8,repeat=8):
                        if self.over_tf:
                            self.over_tf = False
                        else:
                            self.over_tf = True
                        self.app.sound_manager.play_se("select")
                    if (pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B)):
                        if self.over_tf:
                            self.save.newsave(self.setting_finger)
                            if self.app.local:
                                if self.app.exefile:
                                    self.save_data = json.load(open(self.save_path,"r",encoding="utf-8"))
                                else:
                                    self.save_data = json.load(open("../save/savedata.json","r",encoding="utf-8"))
                            else:
                                self.save_data = self.cloud.load()
                        self.save_enter = -1
                        self.app.sound_manager.play_se("ok")
                return enter_pos
        else:
            if self.first_show:
                if self.app.local:
                    if self.app.exefile:
                        self.save_data = json.load(open(self.save_path,"r",encoding="utf-8"))
                    else:
                        self.save_data = json.load(open("../save/savedata.json","r",encoding="utf-8"))
                else:
                    self.save_data = self.cloud.load()
                self.first_show = False
            if pyxel.btnp(pyxel.KEY_ESCAPE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
                self.app.battle.select_num1 = -1
                self.first_show = True
                self.app.sound_manager.play_se("select")
            if pyxel.btnp(pyxel.KEY_UP,hold = 8,repeat=8) or pyxel.btnp(pyxel.KEY_W,hold = 8,repeat=8) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP,hold = 8,repeat=8):
                if self.setting_finger != 1:
                    self.setting_finger -= 1
                    self.app.sound_manager.play_se("select")
            if pyxel.btnp(pyxel.KEY_DOWN,hold = 8,repeat=8) or pyxel.btnp(pyxel.KEY_S,hold = 8,repeat=8) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN,hold = 8,repeat=8):
                if self.setting_finger != 20:
                    self.setting_finger += 1
                    self.app.sound_manager.play_se("select")
            if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
                if str(self.setting_finger) in self.save_data:
                    if self.app.local:
                        if self.app.exefile:
                            self.save_data = json.load(open(self.save_path,"r",encoding="utf-8"))
                        else:
                            self.save_data = json.load(open("../save/savedata.json","r",encoding="utf-8"))
                    else:
                        self.savedata = self.app.cloud.load()
                        time.sleep(0.3)
                    self.game_time_start = time.time()
                    print(f"{self.setting_finger=}")
                    self.app.loaddata = self.app.savedata[str(self.setting_finger)]
                    self.app.game_time = self.app.savedata[str(self.setting_finger)]["play_data"]["time"]
                    self.app.money = self.app.savedata[str(self.setting_finger)]["play_data"]["money"]
                    self.app.now_scene = self.app.savedata[str(self.setting_finger)]["play_data"]["scene"]
                    self.app.now_location = self.app.savedata[str(self.setting_finger)]["play_data"]["location"]
                    self.app.player.x = self.app.savedata[str(self.setting_finger)]["play_data"]["x"]
                    self.app.player.y = self.app.savedata[str(self.setting_finger)]["play_data"]["y"]
                    self.app.chara_data = self.app.savedata[str(self.setting_finger)]["play_data"]["chara_data"]
                    self.app.item_codes = self.app.savedata[str(self.setting_finger)]["play_data"]["item_codes"]
                    self.app.imp_item_codes = self.app.savedata[str(self.setting_finger)]["play_data"]["imp_item_codes"]
                    self.app.equip_codes = self.app.savedata[str(self.setting_finger)]["play_data"]["equip_codes"]
                    self.app.msg_id = self.app.savedata[str(self.setting_finger)]["play_data"]["words"]["msg_id"]
                    self.app.disp_id = self.app.savedata[str(self.setting_finger)]["play_data"]["words"]["disp_id"]
                    self.app.story_flags_tf = {k:bool(v) for k,v in self.app.savedata[str(self.setting_finger)]["play_data"]["story_flags_tf"].items()}
                    self.app.story_flags_co = {k:bool(v) for k,v in self.app.savedata[str(self.setting_finger)]["play_data"]["story_flags_co"].items()}
                    self.question_selects = self.savedata[str(self.save_load.setting_finger)]["play_data"]["question_selects"]
                    self.app.in_battle = False
                    self.app.sound_manager.play_se("ok")

    def draw(self):
        """基本描画"""
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
        if self.save_enter != -1:
            pyxel.rect(90,80,110,40,0)
            pyxel.rectb(90,80,110,40,7)
            self.umplus10.draw_text(107,81,"上書きしますか？",7)
            if self.over_tf:
                pyxel.rect(95,102,33,11,1)
            else:
                pyxel.rect(150,102,33,11,1)
            self.umplus10.draw_text(101,102,"はい",7)
            self.umplus10.draw_text(151,102,"いいえ",7)