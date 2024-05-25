import pyxel
import json
import time
from save import Save
from save_load import SaveLoad
from option import Option
from cloud_data import cloud_data

class In_Setting:
    """
    プレイしているときの設定のクラス

    Parameters:
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
        self.cloud = cloud_data(is_test=self.app.is_test)
        self.finger_pos = 0
        self.enter_pos = -1
        self.setting_finger = 1
        self.in_st_finger = 0
        self.move_fi = False
        self.move_to = 0
        self.save_pos = 1
        self.time_h= 0
        self.time_m = 0
        self.time_s = 0
        self.save_load = SaveLoad(self.init_x,self.init_y,self.umplus10,True,app = self.app)
        self.option = Option(self.app,self.init_x,self.init_y,self.umplus10)
        if self.app.local:
            with open("configs/savedata.json",encoding="utf-8") as f:
                self.save_data = json.load(f)
        else:
            self.save_data = self.cloud.load()
        with open("assets/scenes.json",encoding="utf-8") as f:
            self.scenes = json.load(f)
        with open("assets/tools.json","r",encoding="utf-8") as f:
            self.tools = json.load(f)
        self.setting_sc = self.scenes["IN_SETTING_SCENE"]
        self.title_ac = self.scenes["TITLE_SCENE"]

    def sort_update(self):
        len_ = len(self.app.chara_data.items())
        self.chara_keys = list(self.app.chara_data.keys())
        if pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
            self.enter_pos = -1
        if (pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP)) and self.in_st_finger != 0:
                self.in_st_finger -= 1
        if (pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN)) and self.in_st_finger != len_ - 1:
            self.in_st_finger += 1
        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
            if not self.move_fi:
                self.move_to = self.in_st_finger
                self.move_fi = True
            else:
                chara_data_be = {}
                tmp = self.chara_keys[self.in_st_finger]
                self.chara_keys[self.in_st_finger] = self.chara_keys[self.move_to]
                self.chara_keys[self.move_to] = tmp
                for i in self.chara_keys:
                    chara_data_be[i] = self.app.chara_data[i]
                self.app.chara_data = chara_data_be
                self.move_fi = False

    def item_update(self):
        len_ = len(self.app.item_codes.items())
        if pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
            self.enter_pos = -1
        if (pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP)) and self.in_st_finger != 0:
                self.in_st_finger -= 1
        if (pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN)) and self.in_st_finger != len_ - 1:
            self.in_st_finger += 1
        if (pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B)):
            #アイテムを使用するときの処理など
            print(self.tools["basic"][list(self.app.item_codes.keys())[self.in_st_finger]][0])

    def imp_update(self):
        len_ = len(self.app.imp_item_codes)
        if pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
            self.enter_pos = -1
        if (pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP)) and self.in_st_finger != 0:
                self.in_st_finger -= 1
        if (pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN)) and self.in_st_finger != len_ - 1:
            self.in_st_finger += 1
        if (pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B)):
            print(self.tools["important"][self.app.imp_item_codes[self.in_st_finger]][0])

    def update(self):
        time_time = int(time.time() - self.app.game_time_start)
        old_time_h,old_time_m,old_time_s = map(int,self.app.game_time.split(":"))
        time_time += old_time_h * 3600
        time_time += old_time_m * 60
        time_time += old_time_s
        self.time_h = time_time // 3600
        self.time_m = (time_time % 3600) // 60
        self.time_s = (time_time % 3600 % 60)
        if self.enter_pos == -1:
            if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
                if self.finger_pos != 0:
                    self.finger_pos -= 11
            elif pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
                if self.finger_pos != 88:
                    self.finger_pos += 11
            elif pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
                self.in_st_finger = 0
                self.enter_pos = self.finger_pos//11
                print(self.enter_pos)
        elif self.enter_pos == 8:
            self.enter_pos = -1
            self.finger_pos = 0
            self.app.title_s.question_mark = 0
            self.app.now_scene = self.title_ac
        elif self.enter_pos == 7:
            self.enter_pos = self.save_load.update(self.enter_pos)
        elif self.enter_pos == 6:
            self.enter_pos = self.option.update(self.enter_pos)
        elif self.enter_pos == 5:
            self.sort_update()
        elif self.enter_pos == 1:
            self.imp_update()
        elif self.enter_pos == 0:
            self.item_update()
        else:
            self.enter_pos = -1

    def item_draw(self):
        for i,kv in enumerate(self.app.item_codes.items()):
            if i == self.in_st_finger:
                pyxel.rect(71,6+(48.75*i),self.init_x-72,48.75,1)
            pyxel.line(70,5+(48.75*i + 1),self.init_x,5+(48.75*i + 1),7)
            self.umplus10.draw_text(71,int(6+(49*i)),self.tools["basic"][kv[0]][0])
            self.umplus10.draw_text(170,int(6+(49*i)),f"個数: {kv[1]}")
        pyxel.line(70,5+(48.75*(i + 1) + 1),self.init_x,5+(48.75*(i + 1) + 1),7)

    def imp_draw(self):
        for i,v in enumerate(self.app.imp_item_codes):
            if i == self.in_st_finger:
                pyxel.rect(71,6+(48.75*i),self.init_x-72,48.75,1)
            pyxel.line(70,5+(48.75*i + 1),self.init_x,5+(48.75*i + 1),7)
            self.umplus10.draw_text(71,int(6+(49*i)),self.tools["important"][v][0])
        pyxel.line(70,5+(48.75*(i + 1) + 1),self.init_x,5+(48.75*(i + 1) + 1),7)

    def sort_draw(self):
        for i,t in zip(range(len(self.app.chara_data.items())),self.app.chara_data):
            if i == self.in_st_finger:
                pyxel.rect(71,6+(48.75*i),self.init_x-72,48.75,1)
            pyxel.line(70,5+(48.75*i + 1),self.init_x,5+(48.75*i + 1),7)
            self.umplus10.draw_text(71,int(6+(49*i)),t,7)
        pyxel.line(70,5+(48.75*(i + 1) + 1),self.init_x,5+(48.75*(i + 1) + 1),7)

    def draw(self):
        pyxel.cls(0)
        pyxel.rect(18,5,65,105,0)
        pyxel.rectb(18,5,65,105,7)
        pyxel.rect(5,self.init_y-75,65,75,0)
        pyxel.rectb(5,self.init_y-75,65,75,7)
        pyxel.rect(70,5,self.init_x-70,self.init_y-5,0)
        pyxel.rectb(70,5,self.init_x-70,self.init_y-5,7)
        pyxel.blt(0,5+self.finger_pos,0,15,0,15,15,0)
        self.umplus10.draw_text(19,6,"アイテム",7)
        self.umplus10.draw_text(19,17,"大切なもの",7)
        self.umplus10.draw_text(19,28,"スキル",1)
        self.umplus10.draw_text(19,39,"装備",1)
        self.umplus10.draw_text(19,50,"ステータス",1)
        self.umplus10.draw_text(19,61,"並び替え",7)
        self.umplus10.draw_text(19,72,"オプション",7)
        self.umplus10.draw_text(19,83,"セーブ",7)
        self.umplus10.draw_text(19,94,"ゲーム終了",7)
        self.umplus10.draw_text(20,self.init_y-11,f"{str(self.time_h).zfill(2)}:{str(self.time_m).zfill(2)}:{str(self.time_s).zfill(2)}")
        if self.enter_pos == 7:
            self.save_load.draw()
        elif self.enter_pos == 6:
            self.option.draw()
        elif self.enter_pos == 5:
            self.sort_draw()
        elif self.enter_pos == 1:
            self.imp_draw()
        elif self.enter_pos == 0:
            self.item_draw()


class Out_Setting:
    """
    プレイしていないときの設定

    Parameters:
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
        self.finger_pos = 0
        self.enter_pos = -1
        self.setting_finger = 1
        self.save_pos = 1
        self.option = Option(self.app,self.init_x,self.init_y,self.umplus10)

    def update(self):
        if self.enter_pos == -1:
            if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
                if self.finger_pos != 0:
                    self.finger_pos -= 11
            elif pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
                if self.finger_pos != 11:
                    self.finger_pos += 11
            elif pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
                self.enter_pos = self.finger_pos//11
            elif pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
                return self.title_sc
            return self.setting_sc
        elif self.enter_pos == 1:
            pyxel.quit()
        elif self.enter_pos == 0:
            self.enter_pos = self.option.update(self.enter_pos)
            return self.setting_sc

    def draw(self):
        pyxel.cls(0)
        pyxel.rect(18,5,65,95,0)
        pyxel.rectb(18,5,65,95,7)
        pyxel.rect(70,5,self.init_x-70,self.init_y-5,0)
        pyxel.rectb(70,5,self.init_x-70,self.init_y-5,7)
        pyxel.blt(0,5+self.finger_pos,0,15,0,15,15,0)
        self.umplus10.draw_text(19,6,"オプション",7)
        self.umplus10.draw_text(19,17,"ゲーム終了",7)
        if self.enter_pos == 0:
            self.option.draw()