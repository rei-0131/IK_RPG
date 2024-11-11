import pyxel

import utils.rpg_str as rpg_str


#try文の細分化
class CMD:
    """プレイヤーに関するクラス

    Parameter:
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
        self.in_str = ""
        self.equips = ["head","armor","leggings","boots","sword","shield","staff","other"]
        self.start = True
        self.str_lod_count = 1
        self.log = ""
        self.log_type = "str"

    def hmp(self,arg):
        #/hp (set or add or sub) index value
        try:
            if arg[2] != "@a":
                print(self.app.chara_data[list(self.app.chara_data.keys())[int(arg[2])]][arg[0].upper()])
            if arg[1] == "set":
                if arg[2] == "@a":
                    for i in self.app.chara_data.keys():
                        self.app.chara_data[i][arg[0].upper()][1] = int(arg[3])
                else:
                    self.app.chara_data[list(self.app.chara_data.keys())[int(arg[2])]][arg[0].upper()][1] = int(arg[3])
            elif arg[1] == "add":
                if arg[2] == "@a":
                    for i in self.app.chara_data.keys():
                        self.app.chara_data[i][arg[0].upper()][1] += int(arg[3])
                else:
                    self.app.chara_data[list(self.app.chara_data.keys())[int(arg[2])]][arg[0].upper()][1] += int(arg[3])
            elif arg[1] == "sub":
                if arg[2] == "@a":
                    for i in self.app.chara_data.keys():
                        self.app.chara_data[i][arg[0].upper()][1] -= int(arg[3])
                else:
                    self.app.chara_data[list(self.app.chara_data.keys())[int(arg[2])]][arg[0].upper()][1] -= int(arg[3])
            for i in self.app.chara_data.keys():
                if arg[0].upper() == "HP":
                    if self.app.chara_data[i]["HP"][1] > self.app.chara_data[i]["HP"][0]:
                        self.app.chara_data[i]["HP"][1] = self.app.chara_data[i]["HP"][0]
                elif arg[0].upper() == "MP":
                    if self.app.chara_data[i]["MP"][1] > self.app.chara_data[i]["MP"][0]:
                        self.app.chara_data[i]["MP"][1] = self.app.chara_data[i]["MP"][0]
            if arg[2] != "@a":
                print(self.app.chara_data[list(self.app.chara_data.keys())[int(arg[2])]][arg[0].upper()])
            if arg[1] == "set":
                if arg[2] == "@a":
                    self.log = f"全員の{arg[0].upper()}を{arg[3]}にしました。"
                else:
                    self.log = f"{list(self.app.chara_data.keys())[int(arg[2])]}の{arg[0].upper()}を{arg[3]}にしました。"
            elif arg[1] == "add":
                if arg[2] == "@a":
                    self.log = f"全員の{arg[0].upper()}に{arg[3]}加算しました。"
                else:
                    self.log = f"{list(self.app.chara_data.keys())[int(arg[2])]}の{arg[0].upper()}に{arg[3]}加算しました。"
            elif arg[1] == "sub":
                if arg[2] == "@a":
                    self.log = f"全員の{arg[0].upper()}に{arg[3]}減算しました。"
                else:
                    self.log = f"{list(self.app.chara_data.keys())[int(arg[2])]}の{arg[0].upper()}に{arg[3]}減算しました。"
            else:
                self.log = f"第2引数の{arg[1]}は間違っています。"
            self.log_type = "str"
        except Exception as e:
            print(e)
            self.log = str(e)
            self.log_type = "ex"


    def give(self,arg):
        #/give type code (num)
        try:
            if arg[1] == "basic":
                print(self.app.item_codes)
                if arg[2] in self.app.item_codes.keys():
                    self.app.item_codes[arg[2]]["value"] += int(arg[3])
                else:
                    self.app.item_codes[arg[2]] = {
                        "value": int(arg[3]),
                        "battle":self.app.tools[arg[1]][arg[2]]["battle"]
                    }
                print(self.app.item_codes)
            elif arg[1] == "important":
                print(self.app.imp_item_codes)
                if arg[2] not in self.app.imp_item_codes:
                    self.app.imp_item_codes.append(arg[2])
                print(self.app.imp_item_codes)
            elif arg[1] in self.equips:
                print(self.app.equip_codes)
                self.app.equip_codes[arg[1]].append(arg[2])
                print(self.app.equip_codes)
            if arg[1] == "basic":
                self.log = f"{arg[1]}の{arg[2]}を{arg[3]}個与えました。"
            else:
                self.log = f"{arg[1]}の{arg[2]}を与えました。"
            self.log_type = "str"
        except Exception as e:
            print(e)
            self.log = str(e)
            self.log_type = "ex"

    def battle(self):
        self.battle_ = self.app.battle
        print(f"{self.battle_.init_x = }")
        print(f"{self.battle_.init_y = }")
        print(f"{self.battle_.be_scene = }")
        print(f"{self.battle_.select_chara = }")
        print(f"{self.battle_.select_num1 = }")
        print(f"{self.battle_.finger_pos1 = }")
        print(f"{self.battle_.select_num2 = }")
        print(f"{self.battle_.finger_pos2 = }")
        print(f"{self.battle_.finger_pos3 = }")
        print(f"{self.battle_.select_num3 = }")
        print(f"{self.battle_.item_num = }")
        print(f"{self.battle_.item_pos = }")
        print(f"{self.battle_.dis_num = }")
        print(f"{self.battle_.enemy_type = }")
        print(f"{self.battle_.enemy_num = }")
        print(f"{self.battle_.enemy_code = }")
        print(f"{self.battle_.operation_player = }")
        print(f"{self.battle_.player_op = }")
        print(f"{self.battle_.enemy_op = }")
        print(f"{self.battle_.finger_pos4 = }")
        print(f"{self.battle_.target_pos = }")
        print(f"{self.battle_.enemy_status = }")
        print(f"{self.battle_.battle_action = }")
        print(f"{self.battle_.target_team = }")
        print(f"{self.battle_.finger_pos5 = }")
        print(f"{self.battle_.select_num5 = }")
        print(f"{self.battle_.player_effect = }")
        print(f"{self.battle_.enemy_effect = }")
        print(f"{self.battle_.battle_effect = }")
        print(f"{self.battle_.damage_pos = }")
        print(f"{self.battle_.in_battle = }")
        print(f"{self.battle_.battle_item = }")
        print(f"{self.battle_.sp_now = }")
        print(f"{self.battle_.attack_count = }")
        print(f"{self.battle_.enemy_animation = }")
        print(f"{self.battle_.vibe_enemy = }")
        print(f"{self.battle_.vibe_count = }")
        print(f"{self.battle_.player_animation = }")
        print(f"{self.battle_.vibe_player = }")
        print(f"{self.battle_.ai_action = }")
        print(f"{self.battle_.win = }")
        print(f"{self.battle_.none_count = }")
        print(f"{self.battle_.effect_info = }")
        print(f"{self.battle_.turn = }")
        print(f"{self.battle_.ai_turn = }")
        print(f"{self.battle_.play_effect_info = }")
        print(f"{self.battle_.chara_data = }")
        self.log_type = "str"
        self.log = "正常に実行されました"

    def main_(self):
        #appクラス
        pass

    def setting(self):
        #settingクラス
        pass

    def xp(self,arg):
        try:
            self.app.chara_data[list(self.app.chara_data.keys())[int(arg[1])]]["XP"] = int(arg[2])
            self.log = f"{list(self.app.chara_data.keys())[int(arg[1])]}に{int(arg[2])}xp与えました。"
            self.log_type = "str"
            try:
                self.app.battle.chara_data[list(self.app.chara_data.keys())[int(arg[1])]]["XP"] = int(arg[2])
            except Exception as e:
                self.log_type = "ex"
                self.log = str(e)
        except Exception as e:
            self.log_type = "ex"
            self.log = str(e)

    def kill(self,arg):
        if arg[1] == "self":
            if arg[2] == "@a":
                for i in range(len(list(self.app.chara_data.keys()))):
                    self.app.chara_data[list(self.app.chara_data.keys())[i]]["HP"][1] = 0
                self.log_type = "str"
                self.log = "すべての味方をキルしました"
            else:
                self.app.chara_data[list(self.app.chara_data.keys())[int(arg[2])]]["HP"][1] = 0
                self.log_type = "str"
                self.log = f"{list(self.app.chara_data.keys())[int(arg[2])]}をキルしました"
        elif arg[1] == "enemy":
            if arg[2] == "@a":
                for i in range(len(self.app.battle.enemy_status)):
                    self.app.battle.enemy_status[i]["HP"][1] = 0
                self.log_type = "str"
                self.log = "すべての敵をキルしました"
            else:
                self.app.battle.enemy_status[int(arg[2])]["HP"][1] = 0
                self.log_type = "str"
                self.log = f"インデックス{arg[2]}の敵ををキルしました"
        else:
            self.log_type = "str"
            self.log = "存在しない対象です"

    def mode(self,arg):
        self.log_type = "str"
        if arg[1] == "init":
            self.app.mode = arg[1]
            self.app.init_data = self.app.INIT_DATA[self.app.mode]
            self.app.chara_data = self.app.init_data["chara_data"]
            self.app.item_codes = self.app.init_data["item_codes"]
            self.app.equip_codes = self.app.init_data["equip_codes"]
            self.app.imp_item_codes = self.app.init_data["imp_item_codes"]
            self.app.loaddata = {
                "play_data": {
                "time": "00:00:00",
                "words":{
                    "msg_id":None,
                    "disp_id":None
                },
                "scene": 1,
                "x":136,
                "y": 182,
                "chara_data":self.app.chara_data,
                "item_codes":self.app.item_codes,
                "imp_item_codes":self.app.imp_item_codes,
                "equip_codes":self.app.equip_codes
                }
            }
            self.app.game_time = self.app.loaddata["play_data"]["time"]
            self.app.player.x = self.app.loaddata["play_data"]["x"]
            self.app.player.y = self.app.loaddata["play_data"]["y"]
            self.app.msg_id = self.app.loaddata["play_data"]["words"]["msg_id"]
            self.app.disp_id = self.app.loaddata["play_data"]["words"]["disp_id"]
            self.log = "initに設定しました"
        else:
            self.log = "存在しないモードです"

    def update(self):
        if pyxel.btnp(pyxel.KEY_RETURN):
            print(self.in_str)
            cmd_config = self.in_str.split()
            if cmd_config[0][0] == "/":
                cmd_config[0] = cmd_config[0][1:]
                if cmd_config[0] == "hp" or cmd_config[0] == "mp":
                    self.hmp(cmd_config)
                elif cmd_config[0] == "give":
                    self.give(cmd_config)
                elif cmd_config[0] == "battle":
                    self.battle()
                elif cmd_config[0] == "main":
                    self.main_()
                elif cmd_config[0] == "setting":
                    self.setting()
                elif cmd_config[0] == "xp":
                    self.xp(cmd_config)
                elif cmd_config[0] == "kill":
                    self.kill(cmd_config)
                elif cmd_config[0] == "mode":
                    self.mode(cmd_config)
                else:
                    self.log_type = "ex"
                    self.log = f"Not found command '{cmd_config[0]}'"
            self.in_str = ""
        else:
            tmp = rpg_str.get_str()
            if tmp != None:
                if tmp == "back":
                    self.in_str = self.in_str[:len(self.in_str) - 1]
                else:
                    self.in_str += tmp
            if self.start:
                self.in_str = ""
                self.start = False

    def draw(self):
        pyxel.rect(5,self.init_y-30,self.init_x-10,30,0)
        pyxel.rectb(5,self.init_y-30,self.init_x-10,30,7)
        pyxel.rect(5,self.init_y-60,self.init_x-10,30,0)
        pyxel.rectb(5,self.init_y-60,self.init_x-10,30,7)
        if self.log_type == "str":
            if len(self.log) > 28:
                for i,j in zip(range(0,len(self.log),28),range(2)):
                    self.umplus10.draw_text(6,self.init_y-59+11*j,self.log[i:i + 28],7)
            else:
                self.umplus10.draw_text(6,self.init_y-59,self.log,7)
        else:
            if len(self.log) > 45:
                for i,j in zip(range(0,len(self.log),45),range(2)):
                    self.umplus10.draw_text(6,self.init_y-59+11*j,self.log[i:i + 45],7)
            else:
                self.umplus10.draw_text(6,self.init_y-59,self.log,7)
        if len(self.in_str) > 45:
            for i,j in zip(range(0,len(self.in_str),45),range(2)):
                self.umplus10.draw_text(6,self.init_y-29+11*j,self.in_str[i:i + 45],7)
                if self.str_lod_count < 20:
                    pyxel.rect(7 + 6 * len(self.in_str[i:i + 45]),self.init_y-29+11*j,1,10,7)
        else:
            self.umplus10.draw_text(6,self.init_y-29,self.in_str,7)
            if self.str_lod_count < 20:
                pyxel.rect(7 + 6 * len(self.in_str),self.init_y-29,1,10,7)
        if self.str_lod_count > 40:
            self.str_lod_count = 1
        else:
            self.str_lod_count += 1