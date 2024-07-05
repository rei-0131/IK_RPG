import pyxel
import json
import numpy as np
import random as ran
from sklearn.decomposition import PCA
from sklearn.multioutput import MultiOutputRegressor
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler

#攻撃される際の防御力の適用

class Battle:
    """
    バトルに関するクラス

    Parameters:
    x :int
        画面の大きさx
    y : int
        画面の大きさy
    ump : Any
        umplus10(日本語出力)
    app : Any
        Appクラスのインスタンス
    """
    def __init__(self,x,y,ump,app):
        self.app = app
        self.init_x = x
        self.init_y = y
        self.select_chara = ""
        self.umplus10 = ump
        self.select_num1 = -1
        self.finger_pos1 = 0
        self.select_num2 = -1
        self.finger_pos2 = 0
        self.finger_pos3 = 0
        self.select_num3 = -1
        self.item_num = 0
        self.item_pos = 0
        self.dis_num = 0
        self.enemy_type = ""
        self.enemy_num = 0
        self.enemy_code = []
        self.operation_player = True
        self.player_op = []
        self.enemy_op = []
        self.finger_pos4 = 0
        self.target_pos = -1
        self.enemy_status = []
        self.battle_action = []
        self.target_team = ""
        self.finger_pos5 = 0
        self.select_num5 = -1
        self.player_effect = []
        self.enemy_effect = []
        self.battle_effect = {
            "buff_up":0
        }
        self.damage_pos = 0
        self.in_battle = True
        self.battle_item = {}
        #防御などターンを通しての効果などを表記
        self.sp_now = {}
        self.attack_count = 0
        self.enemy_animation = True
        self.vibe_enemy = []
        self.vibe_count = 0
        self.player_animation = True
        self.vibe_player = []
        self.ai_action = None
        self.first_ai_action = False
        self.win = ""
        self.none_count = 0
        self.effect_info = True
        with open("assets/tools.json","r",encoding="utf-8") as f:
            self.tools = json.load(f)
        with open("assets/magic.json","r",encoding="utf-8") as f:
            self.magic_codes = json.load(f)
        with open("assets/enemy_info.json",encoding="utf-8") as f:
            self.enemy_info = json.load(f)
        self.AI = self.create_AI()
        self.ai_data = []

    def clean(self):
        self.select_chara = ""
        self.select_num1 = -1
        self.finger_pos1 = 0
        self.select_num2 = -1
        self.finger_pos2 = 0
        self.finger_pos3 = 0
        self.select_num3 = -1
        self.item_num = 0
        self.item_pos = 0
        self.dis_num = 0
        self.enemy_num = 0
        self.enemy_code = []
        self.enemy_status = []
        self.operation_player = True
        self.player_op = []
        self.enemy_op = []
        self.finger_pos4 = 0
        self.target_pos = -1
        self.battle_action = []
        self.sp_now = {}
        self.finger_pos5 = 0
        self.select_num5 = -1
        self.player_effect = []
        self.enemy_effect = []
        self.battle_effect = {
            "buff_up":0
        }
        self.damage_pos = 0
        self.in_battle = True
        self.attack_count = 0
        self.vibe_count = 0
        self.enemy_animation = True
        self.vibe_enemy = []
        self.player_animation = True
        self.vibe_player = []
        self.ai_action = None
        self.first_ai_action = False
        self.win = ""
        self.none_count = 0
        self.effect_info = True
        self.battle_item = {i[0]:i[1] for i in self.app.item_codes.items() if i[1]["battle"] == "true"}
        for _ in range(len(self.app.chara_data)):
            self.player_effect.append({
                "atk_buff":0,
                "def_buff":0,
                "basic_atk_buff":0,
                "basic_def_buff":0,
                "atk_dbuff":0,
                "def_dbuff":0,
                "atk_invalid":False,
                "recovery_turn":0,
                "recovery_info":[],
                "02_use":True
                #ほか追加？
            })
            self.vibe_player.append({
                "total":0,
                "value":0,
                "move":"p"
            })

    def set_enemy(self,enemy_num,enemy_code):
        self.enemy_num = enemy_num
        self.enemy_code = enemy_code
        for i in range(self.enemy_num):
            #以下、enemy_infoから敵の情報を引っ張って来て書き込む
            self.enemy_status.append({
                "enemy_name":self.enemy_code[i],
                "HP":[1000,1000],
                "MP":[100,100],
                "atk_ab": 100,
                "def_ab": 100,
                "satisfaction": [
                    1.5,
                    120
                ],
                "atk_buff": 100,
                "def_buff": 100
                })
            self.enemy_effect.append({
                "atk_buff":0,
                "def_buff":0,
                "atk_dbuff":0,
                "def_dbuff":0
                })
            self.vibe_enemy.append({
                "total":0,
                "value":0,
                "move":"p"
            })

    def create_AI(self):
        #first_aiに入っているデータはセットアップデータ
        #continueではfirst_ai+プレイヤーから取得した学習データを使用
        data = []
        ai_answer =[]
        with open("assets/first_ai.txt","r",encoding="utf-8") as f:
            ai_data_ = []
            for line in f:
                line = line.rstrip()
                tmp = line.split()
                for i in range(len(tmp)):
                    tmp[i] = float(tmp[i])
                ai_data_.append([])

                pl_ = int(tmp[0])
                tmp_len_ = len(tmp)
                tmp_len = len(ai_data_)
                for i in range(pl_):
                    ai_data_[tmp_len - 1].append(tmp[1+i*3:1+(i+1)*3])
                for i in range(4-pl_):
                    ai_data_[tmp_len - 1].append([0,0,0])
                en_ = int(tmp[int(tmp[0])*3+1])
                for i in range(en_):
                    tm = [0,tmp[(int(tmp[0])*3+2)+i*2],tmp[(int(tmp[0])*3+2)+i*2+1]]
                    ai_data_[tmp_len - 1].append(tm)
                for i in range(3-en_):
                    ai_data_[tmp_len - 1].append([0,0,0])
                c = tmp[tmp_len_ - 3]
                c = [0,0,c]
                ai_data_[tmp_len - 1].append(c)
                d = tmp[tmp_len_ - 2:tmp_len_]
                nd_ = np.array([])
                ai_data_[tmp_len - 1] = np.append(nd_,ai_data_[tmp_len-1]).tolist()
                ai_answer.append(d)

        data = np.array(ai_data_)
        data_answer = np.array(ai_answer)

        pca = PCA(n_components = 20, whiten = False)
        pca.fit(data)
        data = pca.fit_transform(data)
        scaler = StandardScaler()
        data = scaler.fit_transform(data)


        clf = MultiOutputRegressor(MLPClassifier(alpha=0.00001, hidden_layer_sizes=(300,100,300),max_iter=1000,random_state=0,early_stopping=True))
        clf.fit(data , data_answer)

        return clf

    def enemy_target_select_update(self):
        if self.finger_pos4 == 0:
            self.finger_pos4 = self.enemy_info["enemy_pos"][str(self.enemy_num)][0]
        if pyxel.btnp(pyxel.KEY_A) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
            self.select_num2 = -1
            self.select_num3 = -1
            self.finger_pos2 = 0
            self.finger_pos4 = 0
        if pyxel.btnp(pyxel.KEY_RIGHT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
            if self.enemy_info["enemy_pos"][str(self.enemy_num)].index(self.finger_pos4) != self.enemy_num - 1:
                self.finger_pos4 = self.enemy_info["enemy_pos"][str(self.enemy_num)][self.enemy_info["enemy_pos"][str(self.enemy_num)].index(self.finger_pos4) + 1]
            else:
                self.finger_pos4 = self.enemy_info["enemy_pos"][str(self.enemy_num)][0]
        if pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
            live_e = []
            for len_,v in enumerate(self.enemy_status):
                if  v["HP"][1] > 0:
                    live_e.append(len_)
            if self.enemy_info["enemy_pos"][str(self.enemy_num)].index(self.finger_pos4) != live_e[0]:
                self.finger_pos4 = self.enemy_info["enemy_pos"][str(self.enemy_num)][self.enemy_info["enemy_pos"][str(self.enemy_num)].index(self.finger_pos4) - 1]
            else:
                self.finger_pos4 = self.enemy_info["enemy_pos"][str(self.enemy_num)][self.enemy_num - 1]

        try:
            while self.enemy_status[self.enemy_info["enemy_pos"][str(self.enemy_num)].index(self.finger_pos4)]["HP"][1] <= 0:
                if self.enemy_info["enemy_pos"][str(self.enemy_num)].index(self.finger_pos4) != self.enemy_num - 1:
                    self.finger_pos4 = self.enemy_info["enemy_pos"][str(self.enemy_num)][self.enemy_info["enemy_pos"][str(self.enemy_num)].index(self.finger_pos4) + 1]
                else:
                    self.finger_pos4 = self.enemy_info["enemy_pos"][str(self.enemy_num)][0]
        except ValueError:
            pass

        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
            if self.enemy_status[self.enemy_info["enemy_pos"][str(self.enemy_num)].index(self.finger_pos4)]["HP"][1] > 0:
                if self.select_num1 == 0:
                    sm = "None"
                    self.player_op.append({"player_pos":self.select_num2,"target":self.enemy_info["enemy_pos"][str(self.enemy_num)].index(self.finger_pos4),"sm":"None","sm_code":"None","target_team":"enemy"})
                elif self.select_num1 == 1:
                    sm = "skill"
                    self.player_op.append({"player_pos":self.select_num2,"target":self.enemy_info["enemy_pos"][str(self.enemy_num)].index(self.finger_pos4),"sm":sm,"sm_code":self.app.chara_data[self.select_chara][f"{sm}_codes"][self.item_pos + self.finger_pos3],"target_team":self.target_team})
                elif self.select_num1 == 2:
                    sm = "magic"
                    self.player_op.append({"player_pos":self.select_num2,"target":self.enemy_info["enemy_pos"][str(self.enemy_num)].index(self.finger_pos4),"sm":sm,"sm_code":self.app.chara_data[self.select_chara][f"{sm}_codes"][self.item_pos + self.finger_pos3],"target_team":self.target_team})

                live_num = 0
                for i in self.app.chara_data:
                    if self.app.chara_data[i]["HP"][1] != 0:
                        live_num += 1
                if len(self.player_op) != live_num:
                    self.select_num1 = -1
                    self.select_num2 = -1
                self.finger_pos1 = 0
                self.finger_pos2 = 0
                self.finger_pos3 = 0
                self.select_num3 = -1
                self.finger_pos4 = 0

    def self_target_select_update(self):
        if self.select_num5 == -1:
            if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
                if self.finger_pos5 != 0:
                    self.finger_pos5 -= 18
            if pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
                if self.finger_pos5 != (len(self.app.chara_data.items()) - 1) * 18:
                    self.finger_pos5 += 18
            if pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
                self.select_num5 = -1
                self.finger_pos5 = 0
                self.select_num3 = -1
            if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B) or pyxel.btnp(pyxel.KEY_RIGHT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
                if self.app.chara_data[list(self.app.chara_data.keys())[self.finger_pos5//18]]["HP"][1] > 0:
                    self.select_num5 = int(self.finger_pos5 // 18)
                    print(self.select_num5)
                    if self.select_num1 == 1:
                        sm = "skill"
                        self.player_op.append({"player_pos":self.select_num2,"target":self.select_num5,"sm":sm,"sm_code":self.app.chara_data[self.select_chara][f"{sm}_codes"][self.item_pos + self.finger_pos3],"target_team":self.target_team})
                    elif self.select_num1 == 2:
                        sm = "magic"
                        self.player_op.append({"player_pos":self.select_num2,"target":self.select_num5,"sm":sm,"sm_code":self.app.chara_data[self.select_chara][f"{sm}_codes"][self.item_pos + self.finger_pos3],"target_team":self.target_team})

                    live_num = 0
                    for i in self.app.chara_data:
                        if self.app.chara_data[i]["HP"][1] != 0:
                            live_num += 1
                    if len(self.player_op) != live_num:
                        self.select_num1 = -1
                        self.select_num2 = -1
                    self.finger_pos1 = 0
                    self.finger_pos2 = 0
                    self.finger_pos3 = 0
                    self.select_num3 = -1
                    self.finger_pos4 = 0
                    self.select_num5 = -1
                    self.finger_pos5 = 0
                    self.item_pos = 0
                    self.dis_num = 0

    def none_target_select_update(self):
        self.player_op.append({"player_pos":self.select_num2,"target":"None","sm":"skill","sm_code":self.app.chara_data[self.select_chara][f"skill_codes"][self.item_pos + self.finger_pos3],"target_team":self.target_team})
        live_num = 0
        for i in self.app.chara_data:
            if self.app.chara_data[i]["HP"][1] != 0:
                live_num += 1
        if len(self.player_op) != live_num:
            self.select_num1 = -1
            self.select_num2 = -1
        self.finger_pos1 = 0
        self.finger_pos2 = 0
        self.finger_pos3 = 0
        self.select_num3 = -1

    def sm_update(self,sm):
        if self.select_num3 == -1:
            if pyxel.btnp(pyxel.KEY_A) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
                self.select_num2 = -1
                self.finger_pos3 = 0
                self.item_pos = 0
            if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
                if not (self.finger_pos3 == 0 or self.finger_pos3 == 1):
                    self.finger_pos3-=2
                elif self.item_pos - 2 >= 0:
                    self.item_pos -= 2
            if pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
                if self.finger_pos3 != 8 and self.finger_pos3 != 9:
                    if self.finger_pos3 + 2 < self.dis_num:
                        self.finger_pos3 += 2
                else:
                    if self.finger_pos3 + self.item_pos + 2 < self.item_num:
                        self.item_pos += 2
                    elif self.finger_pos3 + self.item_pos + 3 == self.item_num and self.item_num > 10:
                        self.item_pos += 2
                        self.finger_pos3 -= 1
            if pyxel.btnp(pyxel.KEY_RIGHT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
                if self.finger_pos3 + 1 < self.dis_num:
                    self.finger_pos3 += 1
                elif not self.item_pos + 12 <= self.item_num and self.item_pos + 11 <= self.item_num:
                    self.finger_pos3 -= 1
                    self.item_pos += 2
                elif self.item_pos + 12 <= self.item_num:
                    self.item_pos += 2
            if pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
                if self.item_pos != 0:
                    if self.finger_pos3 == 0:
                        self.finger_pos3 += 1
                        self.item_pos -= 2
                    else:
                        self.finger_pos3 -= 1
                else:
                    if self.finger_pos3 != 0:
                        self.finger_pos3 -= 1
            if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
                use_sm = self.magic_codes[sm][self.app.chara_data[self.select_chara][f"{sm}_codes"][self.item_pos + self.finger_pos3]]
                if use_sm["req_MP"] <= self.app.chara_data[self.select_chara]["MP"][1]:
                    if not (use_sm["name"] == "一刀両断" and not self.player_effect[self.select_num2]["02_use"]):
                        if sm == "skill":
                            #共通処理
                            if use_sm["content"] == "atk":
                                self.target_team = "enemy"
                            elif use_sm["content"] == "tank" or use_sm["content"] == "buff" or use_sm["content"] == "heal":
                                self.target_team = "self"
                            elif use_sm["content"] == "play" or use_sm["content"] == "all_tank" or use_sm["content"] == "buff_up":
                                self.target_team = "none"
                        else:
                            if use_sm["content"] == "atk" or use_sm["content"] == "dbf":
                                self.target_team = "enemy"
                            elif use_sm["content"] == "tank" or use_sm["content"] == "buff" or use_sm["content"] == "heal":
                                self.target_team = "self"
                            elif use_sm["content"] == "play":
                                self.target_team = "one"
                        #魔法名出力
                        self.select_num3 = 0
                        self.finger_pos4 = 0
                        print(use_sm["name"])

    def play_magic(self,magic_code,atk,action):
        if 1 <= magic_code <= 15:
            sm_info = self.magic_codes[action["sm"]][action["sm_code"]]
            magic_atk = atk * ((100 + sm_info["atk_amount"]) / 100)
            self.enemy_status[action["target"]]["HP"][1] -= magic_atk
            self.app.chara_data[list(self.app.chara_data.keys())[action["player_pos"]]]["MP"][1] -= sm_info["req_MP"]
        elif magic_code == 16:
            sm_info = self.magic_codes[action["sm"]][action["sm_code"]]
            if sm_info["recovery_amount"][0] == "p":
                self.app.chara_data[list(self.app.chara_data.keys())[action["player_pos"]]]["HP"][1] += self.app.chara_data[list(self.app.chara_data.keys())[action["player_pos"]]]["HP"][0] * (sm_info["recovery_amount"][1] / 100)
            else:
                self.app.chara_data[list(self.app.chara_data.keys())[action["player_pos"]]]["HP"][1] += sm_info["recovery_amount"][1]
        elif 17 <= magic_code <= 18:
            pass
        elif 19 <= magic_code <= 20:
            pass

    def hp_int(self,target) -> str:
        if target != "none":
            self.app.chara_data[list(self.app.chara_data.keys())[target]]["HP"][1] = int(self.app.chara_data[list(self.app.chara_data.keys())[target]]["HP"][1])
        else:
            for i in self.app.chara_data.keys():
                self.app.chara_data[i]["HP"][1] = int(self.app.chara_data[i]["HP"][1])

    def atk_def_sum(self,action) -> tuple[float,float]:
        action_p = self.app.chara_data[list(self.app.chara_data.keys())[action["player_pos"]]]
        atk = 0
        def_ = 0
        atk += action_p["atk_ab"] * ((self.player_effect[action["player_pos"]]["basic_atk_buff"] + 100) / 100)
        def_ += action_p["def_ab"] * ((self.player_effect[action["player_pos"]]["basic_def_buff"] + 100) / 100)
        isd_ = ["head","armor","leggings","boots","shield"]
        isa_ = ["sword","staff","other"]
        for i,v in action_p["equipments"].items():
            if i in isd_:
                if self.tools[i][v][2] == "f":
                    def_ += self.tools[i][v][3]
                else:
                    def_ += action_p["def_ab"] * (self.tools[i][v][3] / 100)
            elif i in isa_:
                if self.tools[i][v][2] == "f":
                    atk += self.tools[i][v][3]
                else:
                    atk += action_p["atk_ab"] * (self.tools[i][v][3] / 100)
            atk *= (action_p["atk_buff"] + self.player_effect[action["player_pos"]]["atk_buff"] - self.player_effect[action["player_pos"]]["atk_dbuff"]) / 100
            def_ *= (action_p["def_buff"] + self.player_effect[action["player_pos"]]["def_buff"] - self.player_effect[action["player_pos"]]["def_dbuff"]) / 100
        return atk,def_

    def target_attack_update(self):
        try:
            action = self.player_op[self.attack_count]
            if action["target"] != "None":
                if self.enemy_status[action["target"]]["HP"][1] <= 0:
                    live_e = []
                    for len_,v in enumerate(self.enemy_status):
                        if  v["HP"][1] > 0:
                            live_e.append(len_)
                    if len(live_e) == 0:
                        action["target"] = -1
                    else:
                        action["target"] = live_e[ran.randint(0,len(live_e) - 1)]
        except Exception:
            pass
        if not self.enemy_animation:
            action = self.player_op[self.attack_count]
            atk,def_ = self.atk_def_sum(action)
            print(f"{action=}\n{self.player_effect[action['player_pos']]=}\n{atk=} {def_=}\n\n\n")
            if action["target"] != "None":
                while True:
                    if self.enemy_status[action["target"]]["HP"][1] <= 0:
                        live_e = []
                        for len_,v in enumerate(self.enemy_status):
                            if  v["HP"][1] > 0:
                                live_e.append(len_)
                        if len(live_e) == 0:
                            action["target"] = -1
                        else:
                            action["target"] = live_e[ran.randint(0,len(live_e) - 1)]
                    else:
                        break
            if action["target"] != -1:
                if action["sm_code"] != "None":
                    int_code = int(action["sm_code"])
                if action["target_team"] == "enemy":
                    if action["sm"] == "None":
                        self.enemy_status[action["target"]]["HP"][1] -= atk
                    elif action["sm"] == "skill":
                        sm_info = self.magic_codes[action["sm"]][action["sm_code"]]
                        if action["sm_code"] == "01":
                            for _ in range(sm_info["other"]["atk_num"]):
                                self.enemy_status[action["target"]]["HP"][1] -= atk
                        elif action["sm_code"] == "02":
                            cri_atk = atk * (self.app.chara_data[list(self.app.chara_data.keys())[action["player_pos"]]]["satisfaction"][1] / 100)
                            self.enemy_status[action["target"]]["HP"][1] -= cri_atk
                            self.player_effect[action["player_pos"]]["02_use"] = False
                        self.app.chara_data[list(self.app.chara_data.keys())[action["player_pos"]]]["MP"][1] -= sm_info["req_MP"]
                    elif action["sm"] == "magic":
                        if 1 <= int_code <= 15:
                            sm_info = self.magic_codes[action["sm"]][action["sm_code"]]
                            magic_atk = atk * sm_info["atk_amount"] / 100
                            self.enemy_status[action["target"]]["HP"][1] -= magic_atk
                        elif 17 <= int_code <= 18:
                            sm_info = self.magic_codes[action["sm"]][action["sm_code"]]
                            if sm_info["dbuff_type"] == "atk":
                                self.enemy_effect[action["target"]]["atk_dbuff"] += sm_info["dbuff_amount"]
                            elif sm_info["dbuff_type"] == "def":
                                self.enemy_effect[action["target"]]["def_dbuff"] += sm_info["dbuff_amount"]
                        self.app.chara_data[list(self.app.chara_data.keys())[action["player_pos"]]]["MP"][1] -= sm_info["req_MP"]
                    if self.enemy_status[action["target"]]["HP"][1] < 0:
                        self.enemy_status[action["target"]]["HP"][1] = 0
                    self.enemy_effect[action["player_pos"]]["atk_buff"] = 0
                    self.enemy_effect[action["player_pos"]]["def_buff"] = 0
                    self.enemy_effect[action["player_pos"]]["basic_atk_buff"] = 0
                    self.enemy_effect[action["player_pos"]]["basic_def_buff"] = 0
                elif action["target_team"] == "self":
                    if action["sm"] == "skill":
                        sm_info = self.magic_codes[action["sm"]][action["sm_code"]]
                        if action["sm_code"] == "03":
                            if sm_info["recovery_amount"][0] == "p":
                                self.app.chara_data[list(self.app.chara_data.keys())[action["target"]]]["HP"][1] += self.app.chara_data[list(self.app.chara_data.keys())[action["player_pos"]]]["HP"][0] * (sm_info["recovery_amount"][1] / 100)
                            else:
                                self.app.chara_data[list(self.app.chara_data.keys())[action["target"]]]["HP"][1] += sm_info["recovery_amount"][1]
                        elif action["sm_code"] == "04":
                            self.player_effect[action["target"]]["recovery_turn"] = sm_info["other"]["continue_turn"]
                            self.player_effect[action["target"]]["recovery_info"] = sm_info["recovery_amount"]
                            self.player_effect[action["target"]]["recovery_info"][1] -= 1
                            if self.player_effect[action["target"]]["recovery_info"][0] == "p":
                                self.app.chara_data[list(self.app.chara_data.keys())[action["target"]]]["HP"][1] += self.app.chara_data[list(self.app.chara_data.keys())[action["player_pos"]]]["HP"][0] * (self.player_effect[action["target"]]["recovery_info"][1] / 100)
                            else:
                                self.app.chara_data[list(self.app.chara_data.keys())[action["target"]]]["HP"][1] += self.player_effect[action["target"]]["recovery_info"][1]
                        elif action["sm_code"] == "05":
                            self.player_effect[action["target"]]["atk_invalid"] = True
                        elif action["sm_code"] == "07":
                            self.battle_effect["buff_up"] += sm_info["buff_amount"]
                        self.app.chara_data[list(self.app.chara_data.keys())[action["player_pos"]]]["MP"][1] -= sm_info["req_MP"]
                    elif action["sm"] == "magic":
                        sm_info = self.magic_codes[action["sm"]][action["sm_code"]]
                        if action["sm_code"] == "16":
                            if sm_info["recovery_amount"][0] == "p":
                                self.app.chara_data[list(self.app.chara_data.keys())[action["target"]]]["HP"][1] += self.app.chara_data[list(self.app.chara_data.keys())[action["player_pos"]]]["HP"][0] * (sm_info["recovery_amount"][1] / 100)
                            else:
                                self.app.chara_data[list(self.app.chara_data.keys())[action["target"]]]["HP"][1] += sm_info["recovery_amount"][1]
                        elif 19 <= int_code <= 20:
                            if sm_info["buff_type"] == "atk":
                                self.player_effect[action["target"]]["basic_atk_buff"] += sm_info["buff_amount"] + self.battle_effect["buff_up"]
                            elif sm_info["buff_type"] == "def":
                                self.player_effect[action["target"]]["basic_def_buff"] += sm_info["buff_amount"] + self.battle_effect["buff_up"]
                            self.battle_effect["buff_up"] = 0
                        self.app.chara_data[list(self.app.chara_data.keys())[action["player_pos"]]]["MP"][1] -= sm_info["req_MP"]
                    self.hp_int(action["target"])
                elif action["target_team"] == "none":
                    sm_info = self.magic_codes["skill"][action["sm_code"]]
                    if action["sm_code"] == "06":
                        for i in range(len(self.player_effect)):
                            self.player_effect[i]["atk_invalid"] = True
                    elif action["sm_code"] == "08":
                        if 1 <= ran.randint(1,100) <= 10:
                            random_magic = ran.randint(1,20)
                            if random_magic < 10:
                                random_magic = f"0{random_magic}"
                            self.play_magic(random_magic,atk,action)
                    elif action["sm_code"] == "09":
                        if 1 <= ran.randint(1,100) <= 5:
                            self.player_effect[action["player_pos"]]["atk_buff"] += 3
                    self.app.chara_data[list(self.app.chara_data.keys())[action["player_pos"]]]["MP"][1] -= sm_info["req_MP"]
            for i in self.app.chara_data.keys():
                if self.app.chara_data[i]["HP"][1] >= self.app.chara_data[i]["HP"][0]:
                    self.app.chara_data[i]["HP"][1] = self.app.chara_data[i]["HP"][0]
            self.attack_count += 1
            self.enemy_animation = True
        else:
            live_e = []
            for len_,v in enumerate(self.enemy_status):
                if  v["HP"][1] > 0:
                    live_e.append(len_)
            print(f"{self.attack_count=} {len(self.player_op)=}")
            if self.attack_count == len(self.player_op):
                self.player_op = []
                self.operation_player = False
                self.first_ai_action = True
                self.attack_count = 0
            if self.operation_player:
                if not (self.player_op[self.attack_count]["target"] != -1 and self.player_op[self.attack_count]["target_team"] == "enemy"):
                    self.enemy_animation = False
                else:
                    self.vibe_count = self.player_op[self.attack_count]["target"]
                    if self.vibe_enemy[self.vibe_count]["total"] >= 10:
                        self.enemy_animation = False
                        self.vibe_enemy[self.vibe_count] = {
                            "total":0,
                            "value":0,
                            "move":"p"
                        }
                        self.damage_pos = 0
                    elif self.vibe_enemy[self.vibe_count]["total"] < 10:
                        action = self.player_op[self.attack_count]
                        atk,def_ = self.atk_def_sum(action)
                        damage = False
                        damage_amount = 0
                        if action["sm"] == "None":
                            damage = True
                            damage_amount = atk
                        elif action["sm"] == "skill":
                            sm_info = self.magic_codes[action["sm"]][action["sm_code"]]
                            if action["sm_code"] == "01":
                                damage = True
                                damage_amount = atk * 2
                            elif action["sm_code"] == "02":
                                damage = True
                                cri_atk = atk * (self.app.chara_data[list(self.app.chara_data.keys())[action["player_pos"]]]["satisfaction"][1] / 100)
                                damage_amount = cri_atk
                        elif action["sm"] == "magic":
                            int_code = int(action["sm_code"])
                            sm_info = self.magic_codes[action["sm"]][action["sm_code"]]
                            if 1 <= int_code <= 15:
                                damage = True
                                magic_atk = atk * sm_info["atk_amount"] / 100
                                damage_amount = magic_atk
                        if damage:
                            enemy_interval = self.enemy_info["enemy_pos"][str(self.enemy_num)]
                            self.umplus10.draw_text(enemy_interval[action["target"]] + 12,50 + self.damage_pos,str(int(damage_amount)),8)
                            self.damage_pos -= 2
                        vibe = self.vibe_enemy[self.vibe_count]
                        if vibe["move"] == "p":
                            if vibe["value"] < 2:
                                vibe["value"] += 2
                            else:
                                vibe["move"] = "m"
                                vibe["value"] -= 2
                        else:
                            if vibe["value"] > -2:
                                vibe["value"] -= 2
                            else:
                                vibe["move"] = "p"
                                vibe["value"] += 2
                        vibe["total"] += 1

    def item_update(self):
        if self.select_num3 == -1:
            if pyxel.btnp(pyxel.KEY_A) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
                self.select_num1 = -1
            if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
                if not (self.finger_pos3 == 0 or self.finger_pos3 == 1):
                    self.finger_pos3-=2
                elif self.item_pos - 2 >= 0:
                    self.item_pos -= 2
            if pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
                if self.finger_pos3 != 8 and self.finger_pos3 != 9:
                    if self.finger_pos3 + 2 < self.dis_num:
                        self.finger_pos3 += 2
                else:
                    if self.finger_pos3 + self.item_pos + 2 < self.item_num:
                        self.item_pos += 2
                    elif self.finger_pos3 + self.item_pos + 3 == self.item_num and self.item_num > 10:
                        self.item_pos += 2
                        self.finger_pos3 -= 1
            if pyxel.btnp(pyxel.KEY_RIGHT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
                if self.finger_pos3 + 1 < self.dis_num:
                    self.finger_pos3 += 1
                elif not self.item_pos + 12 <= self.item_num and self.item_pos + 11 <= self.item_num:
                    self.finger_pos3 -= 1
                    self.item_pos += 2
                elif self.item_pos + 12 <= self.item_num:
                    self.item_pos += 2
            if pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
                if self.item_pos != 0:
                    if self.finger_pos3 == 0:
                        self.finger_pos3 += 1
                        self.item_pos -= 2
                    else:
                        self.finger_pos3 -= 1
                else:
                    if self.finger_pos3 != 0:
                        self.finger_pos3 -= 1
            if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
                use_item = self.tools["basic"][list(self.battle_item.items())[self.item_pos + self.finger_pos3][0]]
                #アイテムの効果を発動
                print(use_item)

    def update(self):
        if self.in_battle:
            if self.operation_player:
                if self.select_num1 == -1:
                    if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
                        if self.finger_pos1 != 0:
                            self.finger_pos1 -= 15
                        else:
                            self.finger_pos1 = 60
                    if pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
                        if self.finger_pos1 != 60:
                            self.finger_pos1 += 15
                        else:
                            self.finger_pos1 = 0
                    if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B) or pyxel.btnp(pyxel.KEY_RIGHT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
                        self.select_num1 = int(self.finger_pos1 // 15)
                        print(self.select_num1)
                        self.select_num2 = -1
                elif self.select_num1 != 4:
                    if self.select_num2 == -1:
                        if 0 <= self.select_num1 <= 2:
                            if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
                                if self.finger_pos2 != 0:
                                    self.finger_pos2 -= 18
                                else:
                                    self.finger_pos2 = (len(self.app.chara_data.items()) - 1) * 18
                            if pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
                                if self.finger_pos2 != (len(self.app.chara_data.items()) - 1) * 18:
                                    self.finger_pos2 += 18
                                else:
                                    self.finger_pos2 = 0
                            if pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
                                self.select_num1 = -1
                                self.finger_pos2 = 0
                                self.select_num2 = -1
                            if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B) or pyxel.btnp(pyxel.KEY_RIGHT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
                                self.select_num2 = int(self.finger_pos2 // 18)
                                if self.app.chara_data[list(self.app.chara_data.keys())[self.select_num2]]["HP"][1] > 0:
                                    self.select_chara = list(self.app.chara_data.keys())[self.select_num2]
                                    if self.select_num1 == 1:
                                        self.finger_pos3 = 0
                                        self.item_num = 0
                                        self.item_pos = 0
                                        self.dis_num = 0
                                else:
                                    self.select_num2 = -1
                        elif self.select_num1 == 3:
                            self.item_update()
                    else:
                        live_num = 0
                        for i in self.app.chara_data:
                            if self.app.chara_data[i]["HP"][1] != 0:
                                live_num += 1
                        pl_pos = [i["player_pos"] for i in self.player_op]
                        for i in pl_pos:
                            if pl_pos.count(i) >= 2:
                                self.player_op.pop(i)
                                pl_pos.pop(i)
                        if len(self.player_op) == live_num:
                            if self.effect_info:
                                if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
                                    self.effect_info = False
                                    self.select_num1 = -1
                                    self.select_num2 = -1
                            else:
                                self.target_attack_update()
                        else:
                            self.effect_info = True
                            self.attack_count = 0
                            if self.select_num1 == 0:
                                self.enemy_target_select_update()
                            elif self.select_num1 == 1:
                                if self.select_num3 == -1:
                                    self.sm_update("skill")
                                else:
                                    if self.target_team == "enemy":
                                        self.sm_update("skill")
                                        self.enemy_target_select_update()
                                    elif self.target_team == "self":
                                        self.self_target_select_update()
                                    elif self.target_team == "none":
                                        self.none_target_select_update()
                            elif self.select_num1 == 2:
                                if self.select_num3 == -1:
                                    self.sm_update("magic")
                                else:
                                    if self.target_team == "enemy":
                                        self.sm_update("magic")
                                        self.enemy_target_select_update()
                                    elif self.target_team == "self":
                                        self.self_target_select_update()
                                    elif self.target_team == "none":
                                        self.none_target_select_update()
            else:
                ai_input_data = []
                live_enemy = []
                for i in range(self.enemy_num):
                    if self.enemy_status[i]["HP"][1] > 0:
                        live_enemy.append(i)
                if len(live_enemy) != 0:
                    #以下敵AIの行動をプレイヤーに適用
                    live_p = []
                    for len_,i in enumerate(self.app.chara_data):
                        if self.app.chara_data[i]["HP"][1] > 0:
                            live_p.append(len_)
                    if self.first_ai_action:
                        for x in range(len(live_enemy)):
                            write_str = f"{len(self.app.chara_data)} "
                            for i in self.app.chara_data.keys():
                                write_str += f'{self.app.chara_data[i]["post"]} {(self.app.chara_data[i]["HP"][1]/self.app.chara_data[i]["HP"][0]):.4f} {(self.app.chara_data[i]["MP"][1]/self.app.chara_data[i]["MP"][0]):.4f} '
                            write_str += f"{self.enemy_num} "
                            for i in live_enemy:
                                write_str += f'{(self.enemy_status[i]["HP"][1]/self.enemy_status[i]["HP"][0]):.4f} {(self.enemy_status[i]["MP"][1]/self.enemy_status[i]["MP"][0]):.4f} '
                            write_str += f"{x}"
                            write_str = write_str.split()
                            for i in range(len(write_str)):
                                write_str[i] = float(write_str[i])
                            ai_input_data.append([])
                            pl_ = int(write_str[0])
                            tmp_len_ = len(write_str)
                            tmp_len = len(ai_input_data)
                            for i in range(pl_):
                                ai_input_data[tmp_len - 1].append(write_str[1+i*3:1+(i+1)*3])
                            for i in range(4-pl_):
                                ai_input_data[tmp_len - 1].append([0,0,0])
                            en_ = int(write_str[int(write_str[0])*3+1])
                            for i in range(en_):
                                tm = [0,write_str[(len(live_enemy)*3+2)+i*2],write_str[(len(live_enemy)*3+2)+i*2+1]]
                                ai_input_data[tmp_len - 1].append(tm)
                            for i in range(3-en_):
                                ai_input_data[tmp_len - 1].append([0,0,0])
                            c = write_str[tmp_len_ - 3]
                            c = [0,0,c]
                            ai_input_data[tmp_len - 1].append(c)
                            nd_ = np.array([])
                            ai_input_data[tmp_len - 1] = np.append(nd_,ai_input_data[tmp_len-1]).tolist()
                        inp_data = 0
                        l = len(ai_input_data)
                        for i in range(20-l):
                            ai_input_data.append(ai_input_data[inp_data])
                            if inp_data + 1 == l:
                                inp_data = 0

                        ai_input_data = np.array(ai_input_data)
                        pca = PCA(n_components = 20,whiten = False)
                        pca.fit(ai_input_data)
                        ai_input_data = pca.fit_transform(ai_input_data)
                        ai_input_data = ai_input_data[0:len(live_enemy)]
                        scaler = StandardScaler()
                        ai_input_data = scaler.fit_transform(ai_input_data)
                        self.ai_action = self.AI.predict(ai_input_data)
                        self.first_ai_action = False
                    i = self.attack_count
                    ai_ac = self.ai_action[i]
                    if not self.player_animation:
                        if i < len(live_enemy):
                            if int(ai_ac[0]) >= len(list(self.app.chara_data.keys())):
                                ai_ac[0] = len(list(self.app.chara_data.keys())) - 1
                            while True:
                                if self.app.chara_data[list(self.app.chara_data.keys())[int(ai_ac[0])]]["HP"][1] <= 0:
                                    ai_ac[0] = live_p[ran.randint(0,len(live_p) - 1)]
                                else:
                                    break
                            if not self.player_effect[int(ai_ac[0])]["atk_invalid"]:
                                if ai_ac[1] == 1:
                                    self.app.chara_data[list(self.app.chara_data.keys())[int(ai_ac[0])]]["HP"][1] -= self.enemy_status[live_enemy[i]]["atk_ab"]
                                else:
                                    self.app.chara_data[list(self.app.chara_data.keys())[int(ai_ac[0])]]["HP"][1] -= self.enemy_status[live_enemy[i]]["atk_ab"]
                                if self.app.chara_data[list(self.app.chara_data.keys())[int(ai_ac[0])]]["HP"][1] < 0:
                                    self.app.chara_data[list(self.app.chara_data.keys())[int(ai_ac[0])]]["HP"][1] = 0
                        self.attack_count += 1
                        self.player_animation = True
                        if self.attack_count == len(self.ai_action):
                            self.operation_player = True
                            self.attack_count = 0
                            print(self.player_effect)
                            for n,effect in enumerate(self.player_effect):
                                if effect["recovery_turn"] != 0:
                                    self.app.chara_data[list(self.app.chara_data.keys())[n]]["HP"][1]
                                    if effect["recovery_info"][0] == "p":
                                        self.app.chara_data[list(self.app.chara_data.keys())[n]]["HP"][1] += self.app.chara_data[list(self.app.chara_data.keys())[n]]["HP"][0] * (effect["recovery_info"][1] / 100)
                                    else:
                                        self.app.chara_data[list(self.app.chara_data.keys())[n]]["HP"][1] += effect["recovery_info"][1]
                                    effect["recovery_turn"] -= 1
                                if effect["atk_invalid"]:
                                    effect["atk_invalid"] = False
                    else:
                        if self.attack_count == len(live_p):
                            self.attack_count = 0
                        if self.vibe_player[int(ai_ac[0])]["total"] >= 10:
                            self.player_animation = False
                            self.vibe_player[int(ai_ac[0])] = {
                                "total":0,
                                "value":0,
                                "move":"p"
                            }
                        else:
                            vibe = self.vibe_player[int(ai_ac[0])]
                            if not self.player_effect[int(ai_ac[0])]["atk_invalid"]:
                                if vibe["move"] == "p":
                                    if vibe["value"] < 2:
                                        vibe["value"] += 2
                                    else:
                                        vibe["move"] = "m"
                                        vibe["value"] -= 2
                                else:
                                    if vibe["value"] > -2:
                                        vibe["value"] -= 2
                                    else:
                                        vibe["move"] = "p"
                                        vibe["value"] += 2
                            vibe["total"] += 1
                    self.hp_int("none")

    def sm_draw(self,sm):
        pyxel.rect(110,self.init_y//2+10,185,75,0)
        pyxel.rectb(110,self.init_y//2+10,185,75,7)
        pyxel.rect(25,self.init_y//2-20,270,25,0)
        pyxel.rectb(25,self.init_y//2-20,270,25,7)
        self.umplus10.draw_text(26,self.init_y//2-19,self.magic_codes[sm][self.app.chara_data[self.select_chara][f"{sm}_codes"][self.item_pos + self.finger_pos3]]["info"],7)
        self.umplus10.draw_text(190,self.init_y-12,"※戻るにはAキーを押す",8)
        self.item_num = len(self.app.chara_data[self.select_chara][f"{sm}_codes"])
        if self.item_num >= self.item_pos + 11:
            self.dis_num = 10
            for i,item in zip(range(10),self.app.chara_data[self.select_chara][f"{sm}_codes"][self.item_pos:self.item_pos + 10]):
                h = int(i // 2)
                w = i % 2
                if i == self.finger_pos3:
                    pyxel.rect(111+(w*91),self.init_y//2+11+(h*14.4),92,15,1)

                if self.magic_codes[sm][item]["name"] == "一刀両断" and not self.player_effect[self.select_num2]["02_use"]:
                    self.umplus10.draw_text(111+(w*93),self.init_y//2+12+(h*15),self.magic_codes[sm][item]["name"],8)
                else:
                    self.umplus10.draw_text(111+(w*93),self.init_y//2+12+(h*15),self.magic_codes[sm][item]["name"],7)

                if self.magic_codes[sm][item]["req_MP"] > self.app.chara_data[self.select_chara]["MP"][1]:
                    self.umplus10.draw_text(190+(w*93),self.init_y//2+12+(h*15),str(self.magic_codes[sm][item]["req_MP"]),8)
                else:
                    self.umplus10.draw_text(190+(w*93),self.init_y//2+12+(h*15),str(self.magic_codes[sm][item]["req_MP"]),5)
        else:
            self.dis_num = self.item_num - self.item_pos
            for i,item in zip(range(self.item_num-self.item_pos),self.app.chara_data[self.select_chara][f"{sm}_codes"][self.item_pos:self.item_num]):
                h = int(i // 2)
                w = i % 2
                if i == self.finger_pos3:
                    pyxel.rect(111+(w*91),self.init_y//2+11+(h*14.4),92,15,1)

                if self.magic_codes[sm][item]["name"] == "一刀両断" and not self.player_effect[self.select_num2]["02_use"]:
                    self.umplus10.draw_text(111+(w*93),self.init_y//2+12+(h*15),self.magic_codes[sm][item]["name"],8)
                else:
                    self.umplus10.draw_text(111+(w*93),self.init_y//2+12+(h*15),self.magic_codes[sm][item]["name"],7)

                if self.magic_codes[sm][item]["req_MP"] > self.app.chara_data[self.select_chara]["MP"][1]:
                    self.umplus10.draw_text(190+(w*93),self.init_y//2+12+(h*15),str(self.magic_codes[sm][item]["req_MP"]),8)
                else:
                    self.umplus10.draw_text(190+(w*93),self.init_y//2+12+(h*15),str(self.magic_codes[sm][item]["req_MP"]),5)

    def item_draw(self):
        pyxel.rect(110,self.init_y//2+10,185,75,0)
        pyxel.rectb(110,self.init_y//2+10,185,75,7)
        self.item_num = len(self.battle_item.items())
        if self.item_num >= self.item_pos + 11:
            self.dis_num = 10
            for i,item in enumerate(self.battle_item.items()):
                h = int(i // 2)
                w = i % 2
                if i == self.finger_pos3:
                    pyxel.rect(111+(w*91),self.init_y//2+11+(h*14.4),92,15,1)
                self.umplus10.draw_text(111+(w*93),self.init_y//2+12+(h*15),self.tools["basic"][item[0]]["name"],7)
        else:
            self.dis_num = self.item_num - self.item_pos
            for i,item in enumerate(list(self.battle_item.items())[self.item_pos:self.item_num]):
                h = int(i // 2)
                w = i % 2
                if i == self.finger_pos3:
                    pyxel.rect(111+(w*91),self.init_y//2+11+(h*14.4),92,15,1)
                self.umplus10.draw_text(111+(w*93),self.init_y//2+12+(h*15),self.tools["basic"][item[0]]["name"],7)


    def enemy_target_select_draw(self):
        self.umplus10.draw_text(190,self.init_y-12,"※戻るにはAキーを押す",8)
        pyxel.blt(self.finger_pos4 - 8,2,0,32,0,16,16,0)

    def self_target_select_draw(self):
        pyxel.rect(110,self.init_y//2+10,185,75,0)
        pyxel.rectb(110,self.init_y//2+10,185,75,7)
        live_num = 0
        live_p = []
        for len_,i in enumerate(self.app.chara_data):
            if self.app.chara_data[i]["HP"][1] > 0:
                live_num += 1
                live_p.append(len_)

        for i,data in zip(range(1,1+len(self.app.chara_data.items())),enumerate(self.app.chara_data)):
            height = 18*(i - 1)
            if self.select_num1 != 0 and self.select_num1 != 1 and self.select_num1 != 2:
                if data[0] in live_p:
                    self.umplus10.draw_text(115,self.init_y//2+15+height,data[1],7)
                else:
                    self.umplus10.draw_text(115,self.init_y//2+15+height,data[1],8)
            else:
                if data[0] in live_p:
                    self.umplus10.draw_text(130,self.init_y//2+15+height,data[1],7)
                else:
                    self.umplus10.draw_text(130,self.init_y//2+15+height,data[1],8)
            pyxel.text(170,self.init_y//2+14+height,"HP",7)
            pyxel.text(170,self.init_y//2+21+height,"MP",7)
            pyxel.rect(178,self.init_y//2+14+height,(self.app.chara_data[data[1]]["HP"][1]/self.app.chara_data[data[1]]["HP"][0])*100,5,11)
            pyxel.rectb(178,self.init_y//2+14+height,100,5,7)
            pyxel.text(279,self.init_y//2+14+height,f"{self.app.chara_data[data[1]]['HP'][1]}",11)
            pyxel.rect(178,self.init_y//2+21+height,(self.app.chara_data[data[1]]["MP"][1]/self.app.chara_data[data[1]]["MP"][0])*100,5,5)
            pyxel.rectb(178,self.init_y//2+21+height,100,5,7)
            pyxel.text(279,self.init_y//2+21+height,f"{self.app.chara_data[data[1]]['MP'][1]}",5)
        pyxel.blt(115,self.init_y//2+15+(self.finger_pos5),0,16,0,16,16,0)

    def none_target_select_draw(self):
        pass

    def target_attack_draw(self):
        pass

    def draw(self):
        pyxel.cls(0)
        pyxel.rect(25,self.init_y//2+10,75,75,0)
        pyxel.rectb(25,self.init_y//2+10,75,75,7)
        pyxel.rect(50,self.init_y//2+10,25,4,0)
        pyxel.rect(110,self.init_y//2+10,185,75,0)
        pyxel.rectb(110,self.init_y//2+10,185,75,7)
        live_num = 0
        live_p = []
        for len_,i in enumerate(self.app.chara_data):
            if self.app.chara_data[i]["HP"][1] > 0:
                live_num += 1
                live_p.append(len_)
        live_e = []
        for len_,v in enumerate(self.enemy_status):
            if  v["HP"][1] > 0:
                live_e.append(len_)
        if len(live_e) == 0:
            self.win = "player"
            self.in_battle = False
        elif len(live_p) == 0:
            self.win = "enemy"
            self.in_battle = False

        for i,data,ch_i in zip(range(1,1+len(self.app.chara_data.items())),enumerate(self.app.chara_data),range(len(self.app.chara_data.keys()))):
            height = 18*(i - 1)
            op_player = False
            for i in self.player_op:
                if i["player_pos"] == data[0]:
                    op_player = True
                    break
            if self.select_num1 != 0 and self.select_num1 != 1 and self.select_num1 != 2:
                if data[0] in live_p:
                    if op_player:
                        self.umplus10.draw_text(115,self.init_y//2+15+height,data[1],10)
                    else:
                        self.umplus10.draw_text(115,self.init_y//2+15+height,data[1],7)
                else:
                    self.umplus10.draw_text(115,self.init_y//2+15+height,data[1],8)
            else:
                if data[0] in live_p:
                    if op_player:
                        self.umplus10.draw_text(130,self.init_y//2+15+height,data[1],10)
                    else:
                        self.umplus10.draw_text(130,self.init_y//2+15+height,data[1],7)
                else:
                    self.umplus10.draw_text(130,self.init_y//2+15+height,data[1],8)
            pyxel.text(170,self.init_y//2+14+height,"HP",7)
            pyxel.text(170,self.init_y//2+21+height,"MP",7)
            pyxel.rect(178 + self.vibe_player[ch_i]["value"],self.init_y//2+14+height,(self.app.chara_data[data[1]]["HP"][1] / self.app.chara_data[data[1]]["HP"][0]) * 100,5,11)
            pyxel.rectb(178 + self.vibe_player[ch_i]["value"],self.init_y//2+14+height,100,5,7)
            pyxel.text(279,self.init_y//2+14+height,f"{self.app.chara_data[data[1]]['HP'][1]}",11)
            pyxel.rect(178 + self.vibe_player[ch_i]["value"],self.init_y//2+21+height,(self.app.chara_data[data[1]]["MP"][1] / self.app.chara_data[data[1]]["MP"][0]) * 100,5,5)
            pyxel.rectb(178 + self.vibe_player[ch_i]["value"],self.init_y//2+21+height,100,5,7)
            pyxel.text(279,self.init_y//2+21+height,f"{self.app.chara_data[data[1]]['MP'][1]}",5)
        for n,i in enumerate(self.enemy_code):
            if n in live_e:
                enemy_data = self.enemy_info[i["enemy_type"]][i["enemy_code"]]
                enemy_interval = self.enemy_info["enemy_pos"][str(self.enemy_num)]
                pyxel.text(enemy_interval[n] - 34,14,"HP",7)
                pyxel.rect(enemy_interval[n] - 25,15,(self.enemy_status[n]["HP"][1] / self.enemy_status[n]["HP"][0]) * 100 / 2,3,11)
                pyxel.rectb(enemy_interval[n] - 25,15,50,3,7)
                pyxel.blt(enemy_interval[n] - 32 + self.vibe_enemy[n]["value"],20,enemy_data[0],enemy_data[1][0],enemy_data[1][1],enemy_data[2][0],enemy_data[2][1],enemy_data[3])
        self.umplus10.draw_text(53,self.init_y//2+5,"行動",7)
        self.umplus10.draw_text(26,self.init_y//2+15,"たたかう",7)
        self.umplus10.draw_text(26,self.init_y//2+30,"スキル",7)
        self.umplus10.draw_text(26,self.init_y//2+45,"まほう",7)
        self.umplus10.draw_text(26,self.init_y//2+60,"どうぐ",7)
        self.umplus10.draw_text(26,self.init_y//2+75,"にげる",7)
        if self.in_battle:
            if live_num == 0:
                self.in_battle = False
            else:
                if len(self.player_op) == live_num:
                    if self.effect_info:
                        use_magic = []
                        for i,n in enumerate(self.player_op):
                            if n["sm"] == "skill":
                                if 5 <= int(n["sm_code"]) <= 7:
                                    use_magic.append(n)
                            elif n["sm"] == "magic":
                                if 19 <= int(n["sm_code"]) <= 20:
                                    use_magic.append(n)
                        # print(use_magic)
                        if use_magic != []:
                            pyxel.rect(50,self.init_y//2+20,200,60,0)
                            pyxel.rectb(50,self.init_y//2+20,200,60,7)
                        for i,n in enumerate(use_magic):
                            if n["sm"] == "skill":
                                if n["sm_code"] == "05":
                                    self.umplus10.draw_text(51,self.init_y//2+20+(i*15),f"{list(self.app.chara_data.keys())[n['target']]}への攻撃を1ターン無効",7)
                                elif n["sm_code"] == "06":
                                    self.umplus10.draw_text(51,self.init_y//2+20+(i*15),"全ての味方への攻撃を1ターン無効",7)
                                elif n["sm_code"] == "07":
                                    self.umplus10.draw_text(51,self.init_y//2+20+(i*15),"魔法ののステータスアップ率を+3%",7)
                            elif n["sm"] == "magic":
                                if n["sm_code"] == "19":
                                    self.umplus10.draw_text(51,self.init_y//2+20+(i*15),f"{list(self.app.chara_data.keys())[n['target']]}の防御力を15%アップ",7)
                                elif n["sm_code"] == "20":
                                    self.umplus10.draw_text(51,self.init_y//2+20+(i*15),f"{list(self.app.chara_data.keys())[n['target']]}の攻撃力を15%アップ",7)
                    else:
                        self.target_attack_update()
                else:
                    pyxel.blt(7,self.init_y//2+15+(self.finger_pos1),0,16,0,16,16,0)
                    if self.select_num1 == 0:
                        pyxel.blt(112,self.init_y//2+15+(self.finger_pos2),0,16,0,16,16,0)
                        if self.select_num2 != -1:
                            self.enemy_target_select_draw()
                    elif self.select_num1 == 1:
                        pyxel.blt(112,self.init_y//2+15+(self.finger_pos2),0,16,0,16,16,0)
                        if self.select_num2 != -1:
                            if self.select_num3 == -1:
                                self.sm_draw("skill")
                            else:
                                if self.target_team == "enemy":
                                    self.sm_draw("skill")
                                    self.enemy_target_select_draw()
                                elif self.target_team == "self":
                                    self.self_target_select_draw()
                                elif self.target_team == "none":
                                    self.none_target_select_draw()
                    elif self.select_num1 == 2:
                        pyxel.blt(112,self.init_y//2+15+(self.finger_pos2),0,16,0,16,16,0)
                        if self.select_num2 != -1:
                            if self.select_num3 == -1:
                                self.sm_draw("magic")
                            else:
                                if self.target_team == "enemy":
                                    self.sm_draw("magic")
                                    self.enemy_target_select_draw()
                                elif self.target_team == "self":
                                    self.self_target_select_draw()
                                elif self.target_team == "none":
                                    self.none_target_select_draw()
                    elif self.select_num1 == 3:
                        self.item_draw()
                    elif self.select_num1 == 4:
                        pass
        else:
            if self.win == "enemy":
                pyxel.rect(self.init_x//2 - 90, self.init_y//2 - 30,180,60,0)
                self.umplus10.draw_text(self.init_x//2 - 60, self.init_y//2 - 5,"Enemy Win",7)
            else:
                pyxel.rect(self.init_x//2 - 90, self.init_y//2 - 30,180,60,0)
                self.umplus10.draw_text(self.init_x//2 - 60, self.init_y//2 - 5,"Player Win",7)