import pyxel
import numpy as np

import utils.scenes as scenes

class Words:
    def __init__(self,app,x,y,umplus10):
        self.app = app
        self.init_x = x
        self.init_y = y
        self.umplus10 = umplus10
        self.finger_pos = 0
        self.word = {}
        self.questions = "None"
        self.word_tri = [0,True]
        self.words = self.app.words_j
        self.finger_ad = self.app.assets_info["finger_ad"]
        self.frame_count = 0

    def _add_equip(self,chara_data):
        """装備を追加"""
        for k,v in chara_data["equipments"].items():
            self.app.equip_codes[k].append(v)

    def update(self):
        """基本処理"""
        #操作
        self.frame_count += 1
        if not self.app.story_animation:
            if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
                if self.app.msg_id == "38" and not self.app.story_flags_tf["energy_stu"]:
                    self.app.story_flags_tf["energy_stu"] = True
                if self.app.msg_id == "40" and not self.app.story_flags_tf["languid_stu"]:
                    self.app.story_flags_tf["languid_stu"] = True
                if self.app.msg_id == "42" and not self.app.story_flags_tf["ill_humour_stu"]:
                    self.app.story_flags_tf["ill_humour_stu"] = True
                if self.app.msg_id == "43" and not self.app.story_flags_tf["kindness_stu"]:
                    self.app.story_flags_tf["kindness_stu"] = True
                if self.app.msg_id == "50" and not self.app.story_flags_tf["quiet_stu"]:
                    self.app.story_flags_tf["quiet_stu"] = True
                if self.app.msg_id == "130" and not self.app.story_flags_tf["longhair_stu"]:
                    self.app.story_flags_tf["longhair_stu"] = True
                if self.app.msg_id == "192" and not self.app.story_flags_tf["sleepy_stu"]:
                    self.app.story_flags_tf["sleepy_stu"] = True
                if self.app.msg_id == "193" and not self.app.story_flags_tf["serious_stu"]:
                    self.app.story_flags_tf["serious_stu"] = True
                if self.app.msg_id == "196" and not self.app.story_flags_tf["gentle_stu"]:
                    self.app.story_flags_tf["gentle_stu"] = True
                if self.app.msg_id == "197" and not self.app.story_flags_tf["earphone_stu"]:
                    self.app.story_flags_tf["earphone_stu"] = True
        if self.questions != "None":
            if pyxel.btnp(pyxel.KEY_DOWN,hold = 8,repeat=8) or pyxel.btnp(pyxel.KEY_S,hold = 8,repeat=8) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN,hold = 8,repeat=8):
                if self.finger_pos != (len(self.questions) - 1) * -10:
                    self.finger_pos -= 10
                else:
                    self.finger_pos = 0
            if pyxel.btnp(pyxel.KEY_UP,hold = 8,repeat=8) or pyxel.btnp(pyxel.KEY_W,hold = 8,repeat=8) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP,hold = 8,repeat=8):
                if self.finger_pos != 0:
                    self.finger_pos += 10
                else:
                    self.finger_pos = (len(self.questions) - 1) * -10
            if not self.app.story_animation:
                if (pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B)) and self.frame_count > 8:
                    self.app.question_selects[self.app.msg_id] = abs(self.finger_pos // 10)
                    if "item" in self.word:
                        if self.word["item"][0] == "basic":
                            if self.word["item"][1] in self.app.item_codes.keys():
                                self.app.item_codes[self.word["item"][1]]["value"] += int(self.word["item"][2])
                            else:
                                self.app.item_codes[self.word["item"][1]] = {
                                    "value": int(self.word["item"][2]),
                                    "battle": self.app.tools[self.word["item"][0]][self.word["item"][1]]["battle"]
                                }
                        elif self.word["item"][0] == "important":
                            self.app.imp_item_codes.append(self.word["item"][1])
                        elif self.word["item"][0] in ["head","armor","leggings","boots","sword","shield","staff","other"]:
                            self.app.equip_codes[self.word["item"][0]].append(self.word["item"][1])
                    if self.word["to"] != "None":
                        if type(self.word["to"]) is list:
                            if self.app.msg_id == "431" and self.app.question_selects[self.app.msg_id] == 1:
                                self.app.msg_id = "430"
                            else:
                                self.app.msg_id = self.word["to"][self.app.question_selects[self.app.msg_id]]
                        else:
                            self.app.msg_id = self.word["to"]
                    else:
                        if "battle" in self.word:
                            self.app.in_battle = True
                        self.app.disp_id = self.app.msg_id
                    self.finger_pos = 0
                    self.frame_count = 0
        else:
            if not self.app.story_animation:
                if (pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B)) and self.frame_count > 8:
                    if self.app.msg_id == "432":
                        self.app.now_location = scenes.CLASS1_SCENE
                        self.app.player.x = 330
                        self.app.player.y = 0
                        self.app.sound_manager.play_se("turn")
                    elif self.app.msg_id == "479":
                        self.app.endroll.clean()
                        self.app.be_scene = self.app.now_scene
                        self.app.now_scene = "Endroll"
                    if "item" in self.word:
                        if self.word["item"][0] == "basic":
                            if self.word["item"][1] in self.app.item_codes.keys():
                                self.app.item_codes[self.word["item"][1]]["value"] += int(self.word["item"][2])
                            else:
                                self.app.item_codes[self.word["item"][1]] = {
                                    "value": int(self.word["item"][2]),
                                    "battle": self.app.tools[self.word["item"][0]][self.word["item"][1]]["battle"]
                                }
                        elif self.word["item"][0] == "important":
                            self.app.imp_item_codes.append(self.word["item"][1])
                        elif self.word["item"][0] in ["head","armor","leggings","boots","sword","shield","staff","other"]:
                            self.app.equip_codes[self.word["item"][0]].append(self.word["item"][1])
                    if "chara" in self.word:
                        if type(self.word["chara"]) is list:
                            for ch in self.word["chara"]:
                                self.app.chara_data[ch] = self.app.character_data[ch]
                                self._add_equip(self.app.chara_data[ch])
                        else:
                            self.app.chara_data[self.word["chara"]] = self.app.character_data[self.word["chara"]]
                            self._add_equip(self.app.chara_data[self.word["chara"]])
                    if self.word["to"] != "None":
                        self.app.msg_id = self.word["to"]
                    else:
                        if "battle" in self.word:
                            self.app.in_battle = True
                        key = str([int(k) for k, v in self.words["story"].items() if v == self.word][np.abs(np.asarray([int(k) for k, v in self.words["story"].items() if v == self.word]) - int(self.app.msg_id)).argmin()]).zfill(2)
                        print(f"{[int(k) for k, v in self.words['story'].items() if v == self.word]} {key}")
                        self.app.disp_id = key
                    self.frame_count = 0

        if self.word_tri[1]:
            if self.word_tri[0] < 3:
                self.word_tri[0] += 0.15
            else:
                self.word_tri[1] = False
        else:
            if self.word_tri[0] > -1:
                self.word_tri[0] -= 0.15
            else:
                self.word_tri[1] = True

    def dec_word(self):
        """
        言葉を装飾

        Parameters
        -----------
        msg_id : int
            メッセージID
        """
        #文字を出力
        self.word = self.words["story"][self.app.msg_id]
        if "questions" in self.word:
            self.questions = self.word["questions"]
        else:
            self.questions = "None"
        pyxel.rect(5,self.init_y-60,self.init_x-10,60,0)
        pyxel.rectb(5,self.init_y-60,self.init_x-10,60,7)
        sp_len = len(self.word["speaker"]) * 11
        pyxel.rect(5,self.init_y-71,sp_len,12,0)
        pyxel.rectb(5,self.init_y-71,sp_len,12,7)
        self.umplus10.draw_text(7,self.init_y-70,self.word["speaker"],7)
        if type(self.word["word"]) is str:
            # self.umplus10.draw_text(7,self.init_y-59,self.word["word"],7)
            if len(self.word["word"]) > 28:
                for i,j in zip(range(0,len(self.word["word"]),28),range(5)):
                    self.umplus10.draw_text(7,self.init_y-59 + 11 * j,self.word["word"][i:i + 28],7)
            else:
                self.umplus10.draw_text(7,self.init_y-59,self.word["word"],7)
        elif type(self.word["word"]) is list:
            for i,j in enumerate(self.word["word"]):
                if type(j) is not list:
                    self.umplus10.draw_text(7,self.init_y-59 + (11 * i),j,7)
        # elif type(self.word["word"]) is list:
        #     for i,n in enumerate(self.word["word"]):
        #         self.umplus10.draw_text(7,self.init_y-59+i*11,n,7)
        if self.word["to"] != "None":
            pyxel.tri(self.init_x/2-5,self.init_y-10+self.word_tri[0],self.init_x/2+5,self.init_y-10+self.word_tri[0],self.init_x/2,self.init_y-6+self.word_tri[0],7)
        if self.questions != "None":
            que_height = len(self.questions) * 12
            max_str = 0
            for i in self.questions:
                if max_str < len(i) * 11:
                    max_str = len(i) * 11
            pyxel.blt(self.init_x-max_str - 22,self.init_y-98-self.finger_pos+(39-que_height),self.finger_ad[0],self.finger_ad[1],self.finger_ad[2],self.finger_ad[3],self.finger_ad[4],self.finger_ad[5])
            pyxel.rect(self.init_x-max_str-5,self.init_y-61-que_height,max_str,que_height+2,0)
            pyxel.rectb(self.init_x-max_str-5,self.init_y-61-que_height,max_str,que_height+2,7)
            for i,h in zip(self.questions,range(0,len(self.questions)*12,11)):
                self.umplus10.draw_text(self.init_x-max_str - 3,self.init_y-98+h+(39-que_height),i,7)