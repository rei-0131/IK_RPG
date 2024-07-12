import pyxel
import json
import time
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
        self.finger_pos = 0
        self.enter_pos = -1
        self.setting_finger = 1
        self.in_st_finger = 0
        self.in_eqse_finger = 0
        self.in_eqse_pos = 0
        self.in_eqst_finger = 0
        self.in_eqst_item = 0
        self.in_pqse_finger = 0
        self.in_eq_enter = -1
        self.equip_men = False
        self.equip_select = False
        self.equip_part = -1
        self.tool_names = []
        self.equip_dis = []
        self.move_fi = False
        self.move_to = 0
        self.save_pos = 1
        self.time_h= 0
        self.time_m = 0
        self.time_s = 0
        self.cloud = cloud_data(is_test=self.app.is_test)
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
        with open("assets/magic.json","r",encoding="utf-8") as f:
            self.magic = json.load(f)
        self.setting_sc = self.scenes["IN_SETTING_SCENE"]
        self.title_ac = self.scenes["TITLE_SCENE"]

    def clean(self):
        self.finger_pos = 0
        self.enter_pos = -1
        self.setting_finger = 1
        self.in_st_finger = 0
        self.in_st_pos = 0
        self.in_eqse_finger = 0
        self.in_eqse_pos = 0
        self.in_eqst_finger = 0
        self.in_eqst_item = 0
        self.in_pqse_finger = 0
        self.in_eq_enter = -1
        self.equip_men = False
        self.equip_select = False
        self.equip_part = -1
        self.tool_names = []
        self.equip_dis = []
        self.move_fi = False
        self.move_to = 0
        self.save_pos = 1
        self.time_h= 0
        self.time_m = 0
        self.time_s = 0

    def sort_update(self):
        len_ = len(self.app.chara_data.items())
        self.chara_keys = list(self.app.chara_data.keys())
        if pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
            self.enter_pos = -1
            self.in_st_finger = 0
            self.in_st_pos = 0
        if (pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP)) and self.in_st_finger + self.in_st_pos != 0:
            if self.in_st_finger == 0:
                self.in_st_pos -= 1
            elif self.in_st_finger != 0:
                self.in_st_finger -= 1
        if (pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN)) and self.in_st_finger + self.in_st_pos != len_ - 1:
            if self.in_st_finger == 3:
                self.in_st_pos += 1
            else:
                self.in_st_finger += 1
        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
            if not self.move_fi:
                self.move_to = self.in_st_finger + self.in_st_pos
                self.move_fi = True
            else:
                chara_data_be = {}
                tmp = self.chara_keys[self.in_st_finger + self.in_st_pos]
                self.chara_keys[self.in_st_finger + self.in_st_pos] = self.chara_keys[self.move_to]
                self.chara_keys[self.move_to] = tmp
                for i in self.chara_keys:
                    chara_data_be[i] = self.app.chara_data[i]
                self.app.chara_data = chara_data_be
                self.move_fi = False

    def item_update(self):
        len_ = len(self.app.item_codes.items())
        if pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
            self.enter_pos = -1
            self.in_st_finger = 0
            self.in_st_pos = 0
        if (pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP)) and self.in_st_finger + self.in_st_pos != 0:
            if self.in_st_finger == 0:
                self.in_st_pos -= 1
            elif self.in_st_finger != 0:
                self.in_st_finger -= 1
        if (pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN)) and self.in_st_finger + self.in_st_pos != len_ - 1:
            if self.in_st_finger == 3:
                self.in_st_pos += 1
            else:
                self.in_st_finger += 1
        if (pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B)):
            #アイテムを使用するときの処理など
            print(self.tools["basic"][list(self.app.item_codes.keys())[self.in_st_finger + self.in_st_pos]][0])

    def imp_update(self):
        len_ = len(self.app.imp_item_codes)
        if pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
            self.enter_pos = -1
            self.in_st_finger = 0
            self.in_st_pos = 0
        if (pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP)) and self.in_st_finger + self.in_st_pos != 0:
            if self.in_st_finger == 0:
                self.in_st_pos -= 1
            elif self.in_st_finger != 0:
                self.in_st_finger -= 1
        if (pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN)) and self.in_st_finger + self.in_st_pos != len_ - 1:
            if self.in_st_finger == 3:
                self.in_st_pos += 1
            else:
                self.in_st_finger += 1
        if (pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B)):
            print(self.tools["important"][self.app.imp_item_codes[self.in_st_finger + self.in_st_pos]][0])

    def sm_update(self,sm):
        if not self.equip_men:
            len_ = len(self.app.chara_data.items())
            if pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
                self.enter_pos = -1
            if (pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP)) and self.in_st_finger != 0:
                    self.in_st_finger -= 1
            if (pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN)) and self.in_st_finger != len_ - 1:
                self.in_st_finger += 1
            if (pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B)):
                self.in_eq_enter = self.in_st_finger
                self.in_eqse_finger = 0
                self.in_eqse_pos = 0
                self.equip_men = True
                self.equip_select = True
        else:
            len_eq = len(self.app.chara_data[list(self.app.chara_data.keys())[self.in_eq_enter]][f"{sm}_codes"])
            if len_eq >= 10:
                dis_num = 10
            else:
                dis_num = len_eq - self.in_eqst_item
            if pyxel.btnp(pyxel.KEY_A) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
                self.in_pqse_finger = 0
                self.in_eqst_item = 0
                self.equip_men = False
            if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
                if not (self.in_pqse_finger == 0 or self.in_pqse_finger == 1):
                    self.in_pqse_finger-=2
                elif self.in_eqst_item - 2 >= 0:
                    self.in_eqst_item -= 2
            if pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
                if self.in_pqse_finger != 8 and self.in_pqse_finger != 9:
                    if self.in_pqse_finger + 2 < dis_num:
                        self.in_pqse_finger += 2
                else:
                    if self.in_pqse_finger + self.in_eqst_item + 2 < len_eq:
                        self.in_eqst_item += 2
                    elif self.in_pqse_finger + self.in_eqst_item + 2 == len_eq and len_eq > 10:
                        self.in_eqst_item += 2
                        self.in_pqse_finger -= 1
            if pyxel.btnp(pyxel.KEY_RIGHT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
                if self.in_pqse_finger + 1 < dis_num and self.in_pqse_finger + self.in_eqst_item + 1 != len_eq:
                    self.in_pqse_finger += 1
                elif not self.in_eqst_item + 12 <= len_eq and self.in_eqst_item + 11 <= len_eq:
                    self.in_pqse_finger -= 1
                    self.in_eqst_item += 2
                elif self.in_eqst_item + 12 <= len_eq:
                    self.in_eqst_item += 2
            if pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
                if self.in_eqst_item != 0:
                    if self.in_pqse_finger == 0:
                        self.in_pqse_finger += 1
                        self.in_eqst_item -= 2
                    else:
                        self.in_pqse_finger -= 1
                else:
                    if self.in_pqse_finger != 0:
                        self.in_pqse_finger -= 1

    def equip_update(self):
        if not self.equip_men:
            len_ = len(self.app.chara_data.items())
            if pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
                self.enter_pos = -1
            if (pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP)) and self.in_st_finger != 0:
                    self.in_st_finger -= 1
            if (pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN)) and self.in_st_finger != len_ - 1:
                self.in_st_finger += 1
            if (pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B)):
                self.in_eq_enter = self.in_st_finger
                self.in_eqse_finger = 0
                self.in_eqse_pos = 0
                self.equip_men = True
                self.equip_select = True
        else:
            if self.equip_select:
                if pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
                    self.in_eq_enter = 0
                    self.equip_men = False
                if (pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP)):
                    if self.in_eqse_finger == 0 and self.in_eqse_pos != 0:
                        self.in_eqse_pos -= 1
                    elif self.in_eqse_finger != 0:
                        self.in_eqse_finger -= 1
                if (pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN)):
                    if self.in_eqse_finger == 3 and self.in_eqse_pos != 1:
                        self.in_eqse_pos += 1
                    elif self.in_eqse_finger != 3:
                        self.in_eqse_finger += 1
                if (pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B)):
                    self.equip_part = self.in_eqse_finger + self.in_eqse_pos
                    self.equip_select = False
            else:
                len_eq = len(self.app.loaddata["play_data"]["equip_codes"][self.tool_names[self.equip_part]])
                if pyxel.btnp(pyxel.KEY_A) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
                    self.equip_part = -1
                    self.in_pqse_finger = 0
                    self.in_eqst_item = 0
                    self.equip_select = True
                if len_eq > 2:
                    if (pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP)):
                        if self.in_pqse_finger != 0 and self.in_pqse_finger != 1:
                            self.in_pqse_finger -= 2
                        elif self.in_eqst_item != 0:
                            self.in_eqst_item -= 2
                    if (pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN)):
                        if len_eq // 2 + len_eq % 2 >= self.in_pqse_finger + 1:
                            self.in_pqse_finger += 2
                        else:
                            if len_eq // 2 >= self.in_eqst_item + 4:
                                self.in_eqst_item += 2
                            elif self.in_eqst_item + self.in_pqse_finger + 2 <= len_eq - 1:
                                self.in_eqst_item += 2
                            elif self.in_eqst_item + self.in_pqse_finger + 2 == len_eq and self.in_pqse_finger % 2 != 0:
                                self.in_eqst_item += 2
                                self.in_pqse_finger -= 1
                    if pyxel.btnp(pyxel.KEY_RIGHT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
                        if self.in_pqse_finger - 1 != len_eq // 2 and self.in_pqse_finger + self.in_eqst_item != len_eq - 1:
                            self.in_pqse_finger += 1
                        elif self.in_eqst_item + self.in_pqse_finger != len_eq + 1 and self.in_pqse_finger + self.in_eqst_item != len_eq - 1:
                            self.in_eqst_item += 2
                            if self.in_pqse_finger % 2 == 0:
                                self.in_pqse_finger += 1
                            else:
                                self.in_pqse_finger -= 1
                    if pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
                        if self.in_pqse_finger == 0 and self.in_eqst_item != 0:
                            self.in_eqst_item -= 2
                            self.in_pqse_finger += 1
                        elif self.in_eqst_item != 0:
                            self.in_pqse_finger -= 1
                        elif self.in_pqse_finger != 0:
                            self.in_pqse_finger -= 1
                else:
                    if pyxel.btnp(pyxel.KEY_RIGHT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
                        if self.in_pqse_finger != 1:
                            self.in_pqse_finger += 1
                    if pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
                        if self.in_pqse_finger != 0:
                            self.in_pqse_finger -= 1
                if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
                    select_equip = self.equip_dis[self.in_pqse_finger + self.in_eqst_item]
                    if select_equip[1] == 9:
                        if self.tool_names[self.equip_part] in self.app.loaddata["play_data"]["chara_data"][list(self.app.chara_data.keys())[self.in_eq_enter]]["equipments"]:
                            self.app.loaddata["play_data"]["chara_data"][select_equip[2]]["equipments"][self.tool_names[self.equip_part]] = self.app.loaddata["play_data"]["chara_data"][list(self.app.chara_data.keys())[self.in_eq_enter]]["equipments"][self.tool_names[self.equip_part]]
                        else:
                            del self.app.loaddata["play_data"]["chara_data"][select_equip[2]]["equipments"][self.tool_names[self.equip_part]]
                    self.app.loaddata["play_data"]["chara_data"][list(self.app.chara_data.keys())[self.in_eq_enter]]["equipments"][self.tool_names[self.equip_part]] = select_equip[0]

    def status_update(self):
        len_ = len(self.app.chara_data.items())
        if pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
            self.enter_pos = -1
        if (pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP)) and self.in_st_finger != 0:
                self.in_st_finger -= 1
        if (pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN)) and self.in_st_finger != len_ - 1:
            self.in_st_finger += 1
        if (pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B)):
            self.in_eq_enter = self.in_st_finger
            self.in_eqse_finger = 0
            self.in_eqse_pos = 0
            self.equip_men = True
            self.equip_select = True

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
                if self.finger_pos != 99:
                    self.finger_pos += 11
            elif pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
                self.in_st_finger = 0
                self.enter_pos = self.finger_pos//11
                print(self.enter_pos)
        elif self.enter_pos == 9:
            self.enter_pos = -1
            self.finger_pos = 0
            self.app.title_s.question_mark = 0
            self.app.now_scene = self.title_ac
        elif self.enter_pos == 8:
            self.enter_pos = self.save_load.update(self.enter_pos)
        elif self.enter_pos == 7:
            self.enter_pos = self.option.update(self.enter_pos)
        elif self.enter_pos == 6:
            self.sort_update()
        elif self.enter_pos == 5:
            self.status_update()
        elif self.enter_pos == 4:
            self.equip_update()
        elif self.enter_pos == 3:
            self.sm_update("skill")
        elif self.enter_pos == 2:
            self.sm_update("magic")
        elif self.enter_pos == 1:
            self.imp_update()
        elif self.enter_pos == 0:
            self.item_update()
        else:
            self.enter_pos = -1

    def item_draw(self):
        if len(self.app.item_codes) > 4:
            for i,kv in enumerate(list(self.app.item_codes.items())[self.in_st_pos:self.in_st_pos + 4]):
                if i == self.in_st_finger:
                    pyxel.rect(71,6+(48.75*i),self.init_x-72,48.75,1)
                pyxel.line(70,5+(48.75*i + 1),self.init_x,5+(48.75*i + 1),7)
                self.umplus10.draw_text(71,int(6+(49*i)),self.tools["basic"][kv[0]]["name"])
                self.umplus10.draw_text(170,int(6+(49*i)),f"個数: {kv[1]['value']}")
            pyxel.line(70,5+(48.75*(i + 1) + 1),self.init_x,5+(48.75*(i + 1) + 1),7)

        else:
            for i,kv in enumerate(self.app.item_codes.items()):
                if i == self.in_st_finger:
                    pyxel.rect(71,6+(48.75*i),self.init_x-72,48.75,1)
                pyxel.line(70,5+(48.75*i + 1),self.init_x,5+(48.75*i + 1),7)
                self.umplus10.draw_text(71,int(6+(49*i)),self.tools["basic"][kv[0]]["name"])
                self.umplus10.draw_text(170,int(6+(49*i)),f"個数: {kv[1]['value']}")
            pyxel.line(70,5+(48.75*(i + 1) + 1),self.init_x,5+(48.75*(i + 1) + 1),7)

    def imp_draw(self):
        if len(self.app.imp_item_codes) > 4:
            for i,v in enumerate(self.app.imp_item_codes[self.in_st_pos:self.in_st_pos + 4]):
                if i == self.in_st_finger:
                    pyxel.rect(71,6+(48.75*i),self.init_x-72,48.75,1)
                pyxel.line(70,5+(48.75*i + 1),self.init_x,5+(48.75*i + 1),7)
                self.umplus10.draw_text(71,int(6+(49*i)),self.tools["important"][v][0])
            pyxel.line(70,5+(48.75*(i + 1) + 1),self.init_x,5+(48.75*(i + 1) + 1),7)
        else:
            for i,v in enumerate(self.app.imp_item_codes):
                if i == self.in_st_finger:
                    pyxel.rect(71,6+(48.75*i),self.init_x-72,48.75,1)
                pyxel.line(70,5+(48.75*i + 1),self.init_x,5+(48.75*i + 1),7)
                self.umplus10.draw_text(71,int(6+(49*i)),self.tools["important"][v][0])
            pyxel.line(70,5+(48.75*(i + 1) + 1),self.init_x,5+(48.75*(i + 1) + 1),7)

    def sm_draw(self,sm):
        pyxel.rect(71,5,self.init_x-70,self.init_y-5,0)
        pyxel.rect(70,5,self.init_x-70,65,0)
        pyxel.rectb(70,5,self.init_x-70,65,7)
        pyxel.rect(70,70,self.init_x-70,65,0)
        pyxel.rectb(70,70,self.init_x-70,65,7)
        pyxel.rect(70,135,self.init_x-70,65,0)
        pyxel.rectb(70,135,self.init_x-70,65,7)
        self.umplus10.draw_text(71,6,"操作するキャラを選択",7)
        for i,t in zip(range(len(self.app.chara_data.items())),self.app.chara_data):
            if i == self.in_st_finger:
                pyxel.rect(71,17+(13*i),self.init_x-72,13,1)
            pyxel.line(70,16+(13*i + 1),300,16+(13*i + 1),7)
            self.umplus10.draw_text(71,int(18+(13*i)),t,7)
        pyxel.line(70,16+(13*(i + 1) + 1),300,16+(13*(i + 1) + 1),7)
        if self.equip_men:
            chara_data = self.app.chara_data[list(self.app.chara_data.keys())[self.in_eq_enter]]
            if len(chara_data[f"{sm}_codes"]) >= 10:
                for i,v in zip(range(0,10),enumerate(chara_data[f"{sm}_codes"][self.in_eqst_item:len(chara_data[f"{sm}_codes"])+self.in_eqst_item])):
                    w = i % 2
                    h = int(i // 2)
                    if i == self.in_pqse_finger:
                        pyxel.rect(71+(115*w),71+(13*h),114,13,1)
                    self.umplus10.draw_text(71+(115*w),71+(13*h),self.magic[sm][v[1]]["name"],7)
            else:
                for i,v in enumerate(chara_data[f"{sm}_codes"]):
                    w = i % 2
                    h = int(i // 2)
                    if i == self.in_pqse_finger:
                        pyxel.rect(71+(115*w),71+(13*h),115,13,1)
                    self.umplus10.draw_text(71+(115*w),71+(13*h),self.magic[sm][v]["name"],7)
            self.umplus10.draw_text(190,59,"※戻るにはAキーを押す",8)

    def equip_draw(self):
        pyxel.rect(71,5,self.init_x-70,self.init_y-5,0)
        pyxel.rect(70,5,self.init_x-70,65,0)
        pyxel.rectb(70,5,self.init_x-70,65,7)
        pyxel.rect(70,70,115,65,0)
        pyxel.rectb(70,70,115,65,7)
        pyxel.rect(185,70,115,65,0)
        pyxel.rectb(185,70,115,65,7)
        pyxel.rect(70,135,self.init_x-70,65,0)
        pyxel.rectb(70,135,self.init_x-70,65,7)
        if not self.equip_men:
            self.umplus10.draw_text(71,6,"操作するキャラを選択",7)
            for i,t in zip(range(len(self.app.chara_data.items())),self.app.chara_data):
                if i == self.in_st_finger:
                    pyxel.rect(71,71+(16*i),113,17,1)
                pyxel.line(70,70+(16*i + 1),185,70+(16*i + 1),7)
                self.umplus10.draw_text(71,int(71+(17*i)),t,7)
            pyxel.line(70,70+(16*(i + 1) + 1),185,70+(16*(i + 1) + 1),7)
        else:
            chara_data = self.app.chara_data[list(self.app.chara_data.keys())[self.in_eq_enter]]
            self.umplus10.draw_text(71,71,list(self.app.chara_data.keys())[self.in_eq_enter],7)
            self.umplus10.draw_text(71,82,f"Level {chara_data['Level']}",7)
            atk = chara_data["atk_ab"]
            atk_p = 0
            def_ = chara_data["def_ab"]
            def_p = 0
            self.tool_names = ["head","armor","leggings","boots"]
            weapon_names = ["sword","staff","shield","other"]
            for i in self.tool_names:
                if i in chara_data["equipments"]:
                    tool = self.tools[i][chara_data["equipments"][i]]
                    if tool[2] == "p":
                        def_p += int(def_ * (tool[3] / 100))
                    elif tool[2] == "f":
                        def_p += tool[3]
            for i in weapon_names:
                if i in chara_data["equipments"]:
                    weapon = self.tools[i][chara_data["equipments"][i]]
                    if i != "shield":
                        if weapon[2] == "p":
                            atk_p += int(atk * (weapon[3] / 100))
                        elif weapon[2] == "f":
                            atk_p += weapon[3]
                    else:
                        if weapon[2] == "p":
                            def_p += int(def_ * (weapon[3] / 100))
                        elif weapon[2] == "f":
                            def_p += weapon[3]
            self.umplus10.draw_text(71,93,f"ATK {atk + atk_p}",7)
            self.umplus10.draw_text(71,104,f"DEF {def_ + def_p}",7)
            self.tool_names_ = ["頭","胴","脚","足"]
            if chara_data["post"] == 1:
                self.tool_names.append("sword")
                self.tool_names_.append("剣")
            elif chara_data["post"] == 2 or chara_data["post"] == 3:
                self.tool_names.append("staff")
                self.tool_names_.append("杖")
            elif chara_data["post"] == 4:
                self.tool_names.append("shield")
                self.tool_names_.append("盾")
            elif chara_data["post"] == 5:
                self.tool_names.append("other")
                self.tool_names_.append("他")
            for i,v in zip(zip(range(0,4),range(self.in_eqse_pos,len(self.tool_names_)+self.in_eqse_pos)),self.tool_names[self.in_eqse_pos:len(self.tool_names)+self.in_eqse_pos]):
                tool = f"{self.tool_names_[i[1]]} "
                if v in chara_data["equipments"]:
                    tool += self.tools[v][chara_data["equipments"][v]][0]
                if i[0] == self.in_eqse_finger:
                    if v in chara_data["equipments"]:
                        if self.equip_select:
                            self.umplus10.draw_text(71,6,self.tools[v][chara_data["equipments"][v]][4],7)
                    pyxel.rect(186,71+(16*i[0]),113,17,1)
                pyxel.line(186,70+(16*i[0] + 1),300,70+(16*i[0] + 1),7)
                self.umplus10.draw_text(186,int(72+(17*i[0])),tool,7)
            pyxel.line(186,70+(16*(i[0] + 1) + 1),300,70+(16*(i[0] + 1) + 1),7)

            equip_team = []
            equip_in = []

            if not self.equip_select:
                if self.tool_names[self.equip_part] in self.app.loaddata["play_data"]["equip_codes"]:
                    for chara_name in self.app.loaddata["play_data"]["chara_data"]:
                        for equip in self.app.loaddata["play_data"]["chara_data"][chara_name]["equipments"]:
                            if equip in self.app.loaddata["play_data"]["chara_data"][chara_name]["equipments"] and self.tool_names[self.equip_part] == equip:
                                equip_team.append(self.app.loaddata["play_data"]["chara_data"][chara_name]["equipments"][equip])
                                equip_in.append(chara_name)

                    self.equip_dis = []
                    for i in self.app.loaddata["play_data"]["equip_codes"][self.tool_names[self.equip_part]]:
                        if i in equip_team:
                            self.equip_dis.append([i,9,equip_in[equip_team.index(i)]])
                            equip_in.remove(equip_in[equip_team.index(i)])
                            equip_team.remove(i)
                        else:
                            self.equip_dis.append([i,7])

                    if len(self.app.loaddata["play_data"]["equip_codes"][self.tool_names[self.equip_part]]) > 8:
                        item_len = len(self.app.loaddata["play_data"]["equip_codes"][self.tool_names[self.equip_part]])
                        if item_len - self.in_eqst_item <= 8:
                            for i,j in zip(enumerate(self.equip_dis[self.in_eqst_item:item_len]),range(self.in_eqst_item,item_len)):
                                h = int(i[0] // 2)
                                w = i[0] % 2
                                if j == self.in_pqse_finger + self.in_eqst_item:
                                    pyxel.rect(71+(114*w),136+(16*h),114,16,1)
                                if i[1][1] == 9:
                                    self.umplus10.draw_text(173+(114*w),139+(16*h),"使",i[1][1])
                                self.umplus10.draw_text(71+(114*w),139+(16*h),self.tools[self.tool_names[self.equip_part]][i[1][0]][0],i[1][1])
                        else:
                            for i,j in zip(enumerate(self.equip_dis[self.in_eqst_item:self.in_eqst_item+8]),range(self.in_eqst_item,self.in_eqst_item+8)):
                                h = int(i[0] // 2)
                                w = i[0] % 2
                                if j == self.in_pqse_finger + self.in_eqst_item:
                                    pyxel.rect(71+(114*w),136+(16*h),114,16,1)
                                if i[1][1] == 9:
                                    self.umplus10.draw_text(173+(114*w),139+(16*h),"使",i[1][1])
                                self.umplus10.draw_text(71+(114*w),139+(16*h),self.tools[self.tool_names[self.equip_part]][i[1][0]][0],i[1][1])
                    else:
                        for i,j in zip(enumerate(self.equip_dis),range(len(self.equip_dis))):
                            h = int(i[0] // 2)
                            w = i[0] % 2
                            if j == self.in_pqse_finger + self.in_eqst_item:
                                pyxel.rect(71+(114*w),136+(16*h),114,16,1)
                            if i[1][1] == 9:
                                    self.umplus10.draw_text(173+(114*w),139+(16*h),"使",i[1][1])
                            self.umplus10.draw_text(71+(114*w),139+(16*h),self.tools[self.tool_names[self.equip_part]][i[1][0]][0],i[1][1])
                    pyxel.rect(71,6,228,20,0)
                    self.umplus10.draw_text(115,93,"→",7)
                    self.umplus10.draw_text(115,104,"→",7)
                    if self.in_eqst_item + self.in_pqse_finger + 1 >= len(list(self.tools[self.tool_names[self.equip_part]].keys())):
                        equip_sum = (self.in_eqst_item + self.in_pqse_finger) % 4
                    else:
                        equip_sum = self.in_eqst_item + self.in_pqse_finger

                    if self.tool_names[self.equip_part] in chara_data["equipments"]:
                        if self.tools[self.tool_names[self.equip_part]][chara_data["equipments"][self.tool_names[self.equip_part]]][1] == "DEF":
                            if self.tools[self.tool_names[self.equip_part]][chara_data["equipments"][self.tool_names[self.equip_part]]][2] == "p":
                                mai_s = int(def_ * (self.tools[self.tool_names[self.equip_part]][chara_data["equipments"][self.tool_names[self.equip_part]]][3] / 100))
                            else:
                                mai_s = self.tools[self.tool_names[self.equip_part]][chara_data["equipments"][self.tool_names[self.equip_part]]][3]
                        else:
                            if self.tools[self.tool_names[self.equip_part]][chara_data["equipments"][self.tool_names[self.equip_part]]][2] == "p":
                                mai_s = int(atk * (self.tools[self.tool_names[self.equip_part]][chara_data["equipments"][self.tool_names[self.equip_part]]][3] / 100))
                            else:
                                mai_s = self.tools[self.tool_names[self.equip_part]][chara_data["equipments"][self.tool_names[self.equip_part]]][3]

                        equip_ = self.tools[self.tool_names[self.equip_part]][list(self.tools[self.tool_names[self.equip_part]].keys())[equip_sum]][3]
                        if self.tools[self.tool_names[self.equip_part]][list(self.tools[self.tool_names[self.equip_part]].keys())[equip_sum]][1] == "DEF":
                            if self.tools[self.tool_names[self.equip_part]][list(self.tools[self.tool_names[self.equip_part]].keys())[equip_sum]][2] == "p":
                                if int(def_ + def_p + def_ * (equip_ / 100)) - mai_s > def_ + def_p:
                                    self.umplus10.draw_text(125,104,f"{int(def_ + def_p + def_ * (equip_ / 100)) - mai_s}",11)
                                elif int(def_ + def_p + def_ * (equip_ / 100)) - mai_s == def_ + def_p:
                                    self.umplus10.draw_text(125,104,f"{int(def_ + def_p + def_ * (equip_ / 100)) - mai_s}",7)
                                else:
                                    self.umplus10.draw_text(125,104,f"{int(def_ + def_p + def_ * (equip_ / 100)) - mai_s}",8)
                            else:
                                if int(def_ + def_p + equip_) - mai_s > def_ + def_p:
                                    self.umplus10.draw_text(125,104,f"{int(def_ + def_p + equip_) - mai_s}",11)
                                elif int(def_ + def_p + equip_) - mai_s == def_ + def_p:
                                    self.umplus10.draw_text(125,104,f"{int(def_ + def_p + equip_) - mai_s}",7)
                                else:
                                    self.umplus10.draw_text(125,104,f"{int(def_ + def_p + equip_) - mai_s}",8)
                        else:
                            if self.tools[self.tool_names[self.equip_part]][list(self.tools[self.tool_names[self.equip_part]].keys())[equip_sum]][2] == "p":
                                if int(atk + atk_p + atk * (equip_ / 100)) - mai_s > atk + atk_p:
                                    self.umplus10.draw_text(125,93,f"{int(atk + atk_p + atk * (equip_ / 100)) - mai_s}",11)
                                elif int(atk + atk_p + atk * (equip_ / 100)) - mai_s == atk + atk_p:
                                    self.umplus10.draw_text(125,93,f"{int(atk + atk_p + atk * (equip_ / 100)) - mai_s}",7)
                                else:
                                    self.umplus10.draw_text(125,93,f"{int(atk + atk_p + atk * (equip_ / 100)) - mai_s}",8)
                            else:
                                if int(atk + atk_p + equip_) - mai_s > atk + atk_p:
                                    self.umplus10.draw_text(125,93,f"{int(atk + atk_p + equip_) - mai_s}",11)
                                elif int(atk + atk_p + equip_) - mai_s == atk + atk_p:
                                    self.umplus10.draw_text(125,93,f"{int(atk + atk_p + equip_) - mai_s}",7)
                                else:
                                    self.umplus10.draw_text(125,93,f"{int(atk + atk_p + equip_) - mai_s}",8)
                        self.umplus10.draw_text(71,6,self.tools[self.tool_names[self.equip_part]][self.equip_dis[self.in_pqse_finger + self.in_eqst_item][0]][4],7)
                self.umplus10.draw_text(190,59,"※戻るにはAキーを押す",8)

    def status_draw(self):
        pyxel.line(70,70,self.init_x,70,7)
        self.umplus10.draw_text(71,6,"操作するキャラを選択",7)
        for i,t in zip(range(len(self.app.chara_data.items())),self.app.chara_data):
            if i == self.in_st_finger:
                pyxel.rect(71,17+(13*i),self.init_x-72,13,1)
            pyxel.line(70,16+(13*i + 1),300,16+(13*i + 1),7)
            self.umplus10.draw_text(71,int(18+(13*i)),t,7)
        pyxel.line(70,16+(13*(i + 1) + 1),300,16+(13*(i + 1) + 1),7)

        chara_data = self.app.chara_data[list(self.app.chara_data.keys())[self.in_st_finger]]
        atk = 0
        def_ = 0
        atk += chara_data["atk_ab"]
        def_ += chara_data["def_ab"]
        isd_ = ["head","armor","leggings","boots","shield"]
        isa_ = ["sword","staff","other"]
        for i,v in chara_data["equipments"].items():
            if i in isd_:
                if self.tools[i][v][2] == "f":
                    def_ += self.tools[i][v][3]
                else:
                    def_ += chara_data["def_ab"] * (self.tools[i][v][3] / 100)
            elif i in isa_:
                if self.tools[i][v][2] == "f":
                    atk += self.tools[i][v][3]
                else:
                    atk += chara_data["atk_ab"] * (self.tools[i][v][3] / 100)
                    atk *= chara_data["atk_buff"] / 100
                    def_ *= chara_data["def_buff"] / 100
        self.umplus10.draw_text(71,71,list(self.app.chara_data.keys())[self.in_st_finger],7)
        self.umplus10.draw_text(150,71,f"Level {chara_data['Level']}     {chara_data['XP']}/XXXX",7)
        self.umplus10.draw_text(71,82,f"HP {chara_data['HP'][1]}/{chara_data['HP'][0]}",7)
        self.umplus10.draw_text(71,93,f"MP {chara_data['MP'][1]}/{chara_data['MP'][0]}",7)
        self.umplus10.draw_text(71,104,f"ATK {atk}",7)
        self.umplus10.draw_text(71,115,f"DEF {def_}",7)
        self.umplus10.draw_text(71,126,f"会心率 {chara_data['satisfaction'][0]}% 会心ダメ{chara_data['satisfaction'][1]}%",7)

    def sort_draw(self):
        if len(self.app.chara_data.items()) > 4:
            for i,t in enumerate(list(self.app.chara_data.keys())[self.in_st_pos:self.in_st_pos + 4]):
                if i == self.in_st_finger:
                    pyxel.rect(71,6+(48.75*i),self.init_x-72,48.75,1)
                pyxel.line(70,5+(48.75*i + 1),self.init_x,5+(48.75*i + 1),7)
                self.umplus10.draw_text(71,int(6+(49*i)),t,7)
            pyxel.line(70,5+(48.75*(i + 1) + 1),self.init_x,5+(48.75*(i + 1) + 1),7)
        else:
            for i,t in enumerate(self.app.chara_data):
                if i == self.in_st_finger:
                    pyxel.rect(71,6+(48.75*i),self.init_x-72,48.75,1)
                pyxel.line(70,5+(48.75*i + 1),self.init_x,5+(48.75*i + 1),7)
                self.umplus10.draw_text(71,int(6+(49*i)),t,7)
            pyxel.line(70,5+(48.75*(i + 1) + 1),self.init_x,5+(48.75*(i + 1) + 1),7)

    def draw(self):
        pyxel.cls(0)
        pyxel.rect(18,5,65,116,0)
        pyxel.rectb(18,5,65,116,7)
        pyxel.rect(5,self.init_y-75,66,75,0)
        pyxel.rectb(5,self.init_y-75,66,75,7)
        pyxel.rect(70,5,self.init_x-70,self.init_y-5,0)
        pyxel.rectb(70,5,self.init_x-70,self.init_y-5,7)
        pyxel.blt(0,5+self.finger_pos,0,15,0,15,15,0)
        self.umplus10.draw_text(19,6,"アイテム",7)
        self.umplus10.draw_text(19,17,"大切なもの",7)
        self.umplus10.draw_text(19,28,"魔法",7)
        self.umplus10.draw_text(19,39,"スキル",7)
        self.umplus10.draw_text(19,50,"装備",7)
        self.umplus10.draw_text(19,61,"ステータス",7)
        self.umplus10.draw_text(19,72,"並び替え",7)
        self.umplus10.draw_text(19,83,"オプション",7)
        self.umplus10.draw_text(19,94,"セーブ",7)
        self.umplus10.draw_text(19,105,"ゲーム終了",7)
        self.umplus10.draw_text(20,self.init_y-11,f"{str(self.time_h).zfill(2)}:{str(self.time_m).zfill(2)}:{str(self.time_s).zfill(2)}")
        if self.enter_pos == 8:
            self.save_load.draw()
        elif self.enter_pos == 7:
            self.option.draw()
        elif self.enter_pos == 6:
            self.sort_draw()
        elif self.enter_pos == 5:
            self.status_draw()
        elif self.enter_pos == 4:
            self.equip_draw()
        elif self.enter_pos == 3:
            self.sm_draw("skill")
        elif self.enter_pos == 2:
            self.sm_draw("magic")
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
        with open("assets/scenes.json",encoding="utf-8") as f:
            self.scenes = json.load(f)
        self.setting_sc = self.scenes["OUT_SETTING_SCENE"]
        self.title_sc = self.scenes["TITLE_SCENE"]
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