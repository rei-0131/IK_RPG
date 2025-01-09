import pyxel
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import copy
import joblib


class Battle:
    """
    バトルに関するクラス

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
        self.sp_now = {}
        self.attack_count = 0
        self.enemy_animation = True
        self.vibe_enemy = []
        self.vibe_count = 0
        self.player_animation = True
        self.vibe_player = []
        self.ai_action = None
        self.win = ""
        self.none_count = 0
        self.effect_info = True
        self.turn = 0
        self.ai_turn = -1
        self.play_effect_info = True
        self.chara_data = {}
        self.tools = self.app.tools
        self.magic_codes = self.app.magic_codes
        self.enemy_info = self.app.enemy_info
        self.finger_ad = self.app.assets_info["finger_ad"]
        self.finger_ws = self.app.assets_info["finger_ws"]
        if self.app.exefile:
            self.AI = joblib.load(self.app.resource_path("rpg.aibi"))
        else:
            self.AI = joblib.load("assets/rpg.aibi")
        self.xp_up = {}
        self.xp_get = False
        self.xp_stop = False
        self.status_diff = {}
        self.levelup_data = self.app.INIT_DATA["levelup"]
        self.save_chara_data = {}
        self.escape = False
        self.escape_rate = 25
        self.in_boss = False
        self.escape_count = 0
        self.get_item = []
        self.wl_sound = False
        self.sm_level = False
        self.add_sm = {}
        self.win_show = False
        self.add_sm_tf = False

    def clean(self,scene):
        """初期化"""
        self.be_scene = scene
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
        self.win = ""
        self.none_count = 0
        self.effect_info = True
        self.turn = 0
        self.ai_turn = -1
        self.play_effect_info = True
        self.random_range = 0
        self.chara_data = {}
        if len(self.app.chara_data.items()) > 4:
            for k,v in self.app.chara_data.items():
                self.chara_data[k] = v
                if len(self.chara_data) == 4:
                    break
        else:
            self.chara_data = self.app.chara_data
        self.battle_item = {i[0]:i[1] for i in self.app.item_codes.items() if i[1]["battle"]}
        for _ in range(len(self.chara_data)):
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
                "02_use":True,
                "dmg_replace":False
                #ほか追加？
            })
            self.vibe_player.append({
                "total":0,
                "value":0,
                "move":"p"
            })
        self.xp_get = False
        self.xp_up = {i:[0,False,None] for i in self.chara_data.keys()}
        self.xp_stop = False
        self.status_diff = {i:{
            "HP":0,
            "MP":0,
            "atk_ab":0,
            "def_ab":0,
            "satisfaction":[
                0,
                0
            ]} for i in self.chara_data.keys()}
        self.levelup_data = self.app.INIT_DATA["levelup"]
        self.escape = False
        self.escape_rate = 25
        self.in_boss = False
        self.escape_count = 0
        self.get_item = []
        self.wl_sound = False
        self.sm_level = False
        self.add_sm = {}
        self.win_show = False
        self.add_sm_tf = False

        # 経験値確認用
        # self.in_battle = False
        # self.win = "player"

    def save_chara(self,chara):
        """
        キャラデータを保存

        Parameters
        ----------
        chara : dict
            キャラデータ
        """
        self.save_chara_data = copy.deepcopy(chara)

    def debug_clean(self):
        """
        デバッグ用初期化
        """
        for i in range(len(self.chara_data)):
            self.chara_data[list(self.chara_data.keys())[i]]["HP"][1] = self.chara_data[list(self.chara_data.keys())[i]]["HP"][0]
            self.chara_data[list(self.chara_data.keys())[i]]["MP"][1] = self.chara_data[list(self.chara_data.keys())[i]]["MP"][0]

    def check_level(self):
        def xp_ck(cr) -> float:
            """
            必要xp計算

            Parameters
            ----------
            cr : str
                キャラ名
            """
            xp = 0
            level = self.chara_data[cr]["Level"] + 1
            if 0 <= level <= 16:
                xp = level ** 2 + 6 * level
            elif 17 <= level <= 30:
                xp = (5 / 2) * level ** 2 - (81 / 2) * level + 360
            elif 31 <= self.chara_data[cr]["Level"]:
                xp = (9 / 2) * level ** 2 - (325 / 2) * level + 2220
            return xp
        """
        レベルチェック
        """
        for i in self.chara_data.keys():
            try:
                while self.chara_data[i]["XP"] >= xp_ck(i):
                    xp_ = xp_ck(i)
                    self.chara_data[i]["XP"] -= xp_
                    self.chara_data[i]["Level"] += 1
                    # print(f"{self.chara_data[i]['Level']} {self.chara_data[i]['XP']} {xp_ck(i)}")
            except Exception:
                print("Check XP Error")

    def set_enemy(self,enemy_num,enemy_code):
        """
        敵設定

        Parameters
        ----------
        enemy_num : int
            敵の数
        enemy_code : Any
            敵の情報
        """
        self.enemy_num = enemy_num
        self.enemy_code = enemy_code
        self.enemy_status = []
        self.enemy_effect = []
        self.vibe_enemy = []
        self.get_item = []
        for i in range(self.enemy_num):
            self.enemy_status.append(copy.deepcopy(self.enemy_info[self.enemy_code[i]["enemy_type"]][self.enemy_code[i]["enemy_code"]]["status"]))
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

        print(self.enemy_status)
        if self.app.random_encount:
            levels = [self.chara_data[j]["Level"] for j in self.chara_data.keys()]
            ava_level = sum(levels) / len(levels)
            ten = ava_level // 10 + 1
            for i in range(len(self.enemy_status)):
                self.enemy_status[i]["HP"][0] += int(ava_level * self.levelup_data["HP"] * 0.85)
                self.enemy_status[i]["HP"][1] += int(ava_level * self.levelup_data["HP"] * 0.85)
                self.enemy_status[i]["MP"][0] += int(ava_level * self.levelup_data["MP"] * 0.85)
                self.enemy_status[i]["MP"][1] += int(ava_level * self.levelup_data["MP"] * 0.85)
                self.enemy_status[i]["atk_ab"] += int(ava_level * self.levelup_data["atk_ab"] * 0.85)
                self.enemy_status[i]["def_ab"] += int(ava_level * self.levelup_data["def_ab"] * 0.85)
                self.enemy_status[i]["satisfaction"][0] += int(ten * self.levelup_data["satisfaction"][0] * 0.85)
                self.enemy_status[i]["satisfaction"][1] += int(ten * self.levelup_data["satisfaction"][1] * 0.85)
                self.enemy_status[i]["xp"] = int(self.enemy_status[i]["xp"] * (ava_level * 0.85))
                self.enemy_status[i]["money"] = int(self.enemy_status[i]["money"] * (ten * 0.85))
            print(self.enemy_status)

        for i in self.enemy_status:
            if i["enemy_name"]["enemy_type"] == "boss":
                self.in_boss = True
            if "drop" in i:
                if "item" in i["drop"]:
                    for j in i["drop"]["item"]:
                        if 0 <= pyxel.rndi(0,1000) <= j[1]:
                            self.get_item.append(j[0])

    def player_op_over(self):
        """プレイヤー行動チェック"""
        #同じプレイヤーが行動しようとしていないかチェック
        pl_pos = [i["player_pos"] for i in self.player_op]
        for j,i in enumerate(pl_pos):
            if pl_pos.count(i) >= 2:
                for n,x in enumerate(self.player_op):
                    if i == x["player_pos"]:
                        self.player_op.pop(n)
                        break
                pl_pos.pop(j)

    def enemy_target_select_update(self):
        """攻撃ターゲット設定"""
        if self.finger_pos4 == 0:
            self.finger_pos4 = self.enemy_info["enemy_pos"][str(self.enemy_num)][0]
        if pyxel.btnp(pyxel.KEY_ESCAPE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
            self.select_num2 = -1
            self.select_num3 = -1
            self.finger_pos2 = 0
            self.finger_pos4 = 0
            self.app.sound_manager.play_se("select")
        if pyxel.btnp(pyxel.KEY_RIGHT,hold = 8,repeat=8) or pyxel.btnp(pyxel.KEY_D,hold = 8,repeat = 8) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT,hold = 8,repeat=8):
            if self.enemy_info["enemy_pos"][str(self.enemy_num)].index(self.finger_pos4) != self.enemy_num - 1:
                self.finger_pos4 = self.enemy_info["enemy_pos"][str(self.enemy_num)][self.enemy_info["enemy_pos"][str(self.enemy_num)].index(self.finger_pos4) + 1]
            else:
                self.finger_pos4 = self.enemy_info["enemy_pos"][str(self.enemy_num)][0]
            self.app.sound_manager.play_se("select")
        if pyxel.btnp(pyxel.KEY_LEFT,hold = 8,repeat=8) or pyxel.btnp(pyxel.KEY_A,hold = 8,repeat = 8) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT,hold = 8,repeat=8):
            live_e = []
            for len_,v in enumerate(self.enemy_status):
                if  v["HP"][1] > 0:
                    live_e.append(len_)
            if self.enemy_info["enemy_pos"][str(self.enemy_num)].index(self.finger_pos4) != live_e[0]:
                self.finger_pos4 = self.enemy_info["enemy_pos"][str(self.enemy_num)][self.enemy_info["enemy_pos"][str(self.enemy_num)].index(self.finger_pos4) - 1]
            else:
                self.finger_pos4 = self.enemy_info["enemy_pos"][str(self.enemy_num)][self.enemy_num - 1]
            self.app.sound_manager.play_se("select")

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
                k_ran = pyxel.rndi(1,1000)
                kaisin = False
                if self.chara_data[list(self.chara_data.keys())[self.select_num2]]["satisfaction"][0] * 10 >= k_ran:
                    kaisin = True
                if self.select_num1 == 0:
                    sm = "None"
                    self.player_op.append({"player_pos":self.select_num2,"target":self.enemy_info["enemy_pos"][str(self.enemy_num)].index(self.finger_pos4),"sm":"None","sm_code":"None","target_team":"enemy","kaisin":kaisin})
                elif self.select_num1 == 1:
                    sm = "skill"
                    self.player_op.append({"player_pos":self.select_num2,"target":self.enemy_info["enemy_pos"][str(self.enemy_num)].index(self.finger_pos4),"sm":sm,"sm_code":self.chara_data[self.select_chara][f"{sm}_codes"][self.item_pos + self.finger_pos3],"target_team":self.target_team,"kaisin":kaisin})
                elif self.select_num1 == 2:
                    sm = "magic"
                    self.player_op.append({"player_pos":self.select_num2,"target":self.enemy_info["enemy_pos"][str(self.enemy_num)].index(self.finger_pos4),"sm":sm,"sm_code":self.chara_data[self.select_chara][f"{sm}_codes"][self.item_pos + self.finger_pos3],"target_team":self.target_team,"kaisin":kaisin})

                self.player_op_over()
                live_num = 0
                for i in self.chara_data:
                    if self.chara_data[i]["HP"][1] != 0:
                        live_num += 1
                if len(self.player_op) != live_num:
                    self.select_num1 = -1
                    self.select_num2 = -1
                self.finger_pos1 = 0
                self.finger_pos2 = 0
                self.finger_pos3 = 0
                self.select_num3 = -1
                self.finger_pos4 = 0
                self.app.sound_manager.play_se("ok")

    def self_target_select_update(self):
        """味方ターゲット設定"""
        if self.select_num5 == -1:
            if pyxel.btnp(pyxel.KEY_UP,hold = 8,repeat=8) or pyxel.btnp(pyxel.KEY_W,hold = 8,repeat = 8) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP,hold = 8,repeat=8):
                if self.finger_pos5 != 0:
                    self.finger_pos5 -= 18
                else:
                    self.finger_pos5 = (len(self.chara_data.items()) - 1) * 18
                self.app.sound_manager.play_se("select")
            if pyxel.btnp(pyxel.KEY_DOWN,hold = 8,repeat=8) or pyxel.btnp(pyxel.KEY_S,hold = 8,repeat = 8) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN,hold = 8,repeat=8):
                if self.finger_pos5 != (len(self.chara_data.items()) - 1) * 18:
                    self.finger_pos5 += 18
                else:
                    self.finger_pos5 = 0
                self.app.sound_manager.play_se("select")
            if pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.KEY_A) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
                self.select_num5 = -1
                self.finger_pos5 = 0
                self.select_num3 = -1
                self.app.sound_manager.play_se("select")
            if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B) or pyxel.btnp(pyxel.KEY_RIGHT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
                if self.chara_data[list(self.chara_data.keys())[self.finger_pos5//18]]["HP"][1] > 0:
                    self.select_num5 = int(self.finger_pos5 // 18)
                    print(f"{self.select_num5=}")
                    if self.select_num1 == 1:
                        sm = "skill"
                        self.player_op.append({"player_pos":self.select_num2,"target":self.select_num5,"sm":sm,"sm_code":self.chara_data[self.select_chara][f"{sm}_codes"][self.item_pos + self.finger_pos3],"target_team":self.target_team})
                    elif self.select_num1 == 2:
                        sm = "magic"
                        self.player_op.append({"player_pos":self.select_num2,"target":self.select_num5,"sm":sm,"sm_code":self.chara_data[self.select_chara][f"{sm}_codes"][self.item_pos + self.finger_pos3],"target_team":self.target_team})

                    self.player_op_over()
                    live_num = 0
                    for i in self.chara_data:
                        if self.chara_data[i]["HP"][1] != 0:
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
                    self.app.sound_manager.play_se("ok")

    def none_target_select_update(self):
        """選択のない行動"""
        k_ran = pyxel.rndi(1,1000)
        kaisin = False
        if self.chara_data[list(self.chara_data.keys())[self.select_num2]]["satisfaction"][0] * 10 >= k_ran:
            kaisin = True
        if self.chara_data[self.select_chara][f"skill_codes"][self.item_pos + self.finger_pos3] == "08" or self.chara_data[self.select_chara][f"skill_codes"][self.item_pos + self.finger_pos3] == "09":
            self.player_op.append({"player_pos":self.select_num2,"target":"None","sm":"skill","sm_code":self.chara_data[self.select_chara][f"skill_codes"][self.item_pos + self.finger_pos3],"target_team":self.target_team,"effect_invoke":False,"effect_name":"","effect_check":False,"effect_type":"","kaisin":kaisin})
        else:
            self.player_op.append({"player_pos":self.select_num2,"target":"None","sm":"skill","sm_code":self.chara_data[self.select_chara][f"skill_codes"][self.item_pos + self.finger_pos3],"target_team":self.target_team,"kaisin":kaisin})
        self.player_op_over()
        live_num = 0
        for i in self.chara_data:
            if self.chara_data[i]["HP"][1] != 0:
                live_num += 1
        if len(self.player_op) != live_num:
            self.select_num1 = -1
            self.select_num2 = -1
        self.finger_pos1 = 0
        self.finger_pos2 = 0
        self.finger_pos3 = 0
        self.select_num3 = -1

    def sm_update(self,sm):
        """
        魔法・スキルの表示と選択

        Parameters
        -----------
        sm : str
            魔法かスキル
        """
        if self.select_num3 == -1:
            if pyxel.btnp(pyxel.KEY_ESCAPE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
                self.select_num2 = -1
                self.finger_pos3 = 0
                self.item_pos = 0
                self.app.sound_manager.play_se("select")
            if len(self.chara_data[self.select_chara][f"{sm}_codes"]) > 0:
                if pyxel.btnp(pyxel.KEY_UP,hold = 8,repeat=8) or pyxel.btnp(pyxel.KEY_W,hold = 8,repeat = 8) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP,hold = 8,repeat=8):
                    if not (self.finger_pos3 == 0 or self.finger_pos3 == 1):
                        self.finger_pos3-=2
                    elif self.item_pos - 2 >= 0:
                        self.item_pos -= 2
                    self.app.sound_manager.play_se("select")
                if pyxel.btnp(pyxel.KEY_DOWN,hold = 8,repeat=8) or pyxel.btnp(pyxel.KEY_S,hold = 8,repeat = 8) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN,hold = 8,repeat=8):
                    if self.finger_pos3 != 8 and self.finger_pos3 != 9:
                        if self.finger_pos3 + 2 < self.dis_num:
                            self.finger_pos3 += 2
                            self.app.sound_manager.play_se("select")
                    else:
                        if self.finger_pos3 + self.item_pos + 2 < self.item_num:
                            self.item_pos += 2
                            self.app.sound_manager.play_se("select")
                        elif self.finger_pos3 + self.item_pos + 2 == self.item_num and self.item_num > 10:
                            self.item_pos += 2
                            self.finger_pos3 -= 1
                            self.app.sound_manager.play_se("select")
                if pyxel.btnp(pyxel.KEY_RIGHT,hold = 8,repeat=8) or pyxel.btnp(pyxel.KEY_D,hold = 8,repeat = 8) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT,hold = 8,repeat=8):
                    if self.finger_pos3 + 1 < self.dis_num and self.finger_pos3 % 2 == 0:
                        self.finger_pos3 += 1
                        self.app.sound_manager.play_se("select")
                    elif not self.item_pos + 13 <= self.item_num and self.finger_pos3 % 2 != 0 and self.item_pos + 2 < self.item_num:
                        self.finger_pos3 -= 1
                        self.item_pos += 2
                        self.app.sound_manager.play_se("select")
                    elif self.item_pos + 12 <= self.item_num:
                        self.finger_pos3 -= 1
                        self.item_pos += 2
                        self.app.sound_manager.play_se("select")
                if pyxel.btnp(pyxel.KEY_LEFT,hold = 8,repeat=8) or pyxel.btnp(pyxel.KEY_A,hold = 8,repeat = 8) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT,hold = 8,repeat=8):
                    if self.item_pos != 0:
                        if self.finger_pos3 == 0:
                            self.finger_pos3 += 1
                            self.item_pos -= 2
                        else:
                            self.finger_pos3 -= 1
                        self.app.sound_manager.play_se("select")
                    else:
                        if self.finger_pos3 != 0:
                            self.finger_pos3 -= 1
                            self.app.sound_manager.play_se("select")
                if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
                    use_sm = self.magic_codes[sm][self.chara_data[self.select_chara][f"{sm}_codes"][self.item_pos + self.finger_pos3]]
                    if use_sm["req_MP"] <= self.chara_data[self.select_chara]["MP"][1]:
                        if not (use_sm["name"] == "一刀両断" and not self.player_effect[self.select_num2]["02_use"]):
                            if sm == "skill":
                                #共通処理
                                if use_sm["content"] == "atk":
                                    self.target_team = "enemy"
                                elif use_sm["content"] == "tank" or use_sm["content"] == "buff" or use_sm["content"] == "heal":
                                    self.target_team = "self"
                                elif use_sm["content"] == "play" or use_sm["content"] == "all_tank" or use_sm["content"] == "buff_up" or use_sm["content"] == "tank_replace":
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
                            print(f"{use_sm['name']=}")
                            self.app.sound_manager.play_se("ok")

    def hp_int(self,target):
        """
        HPをint型に変換

        Parameters
        ---------------
        target : string
            HPを変換するターゲット
        """
        if target != "none":
            self.chara_data[list(self.chara_data.keys())[target]]["HP"][1] = int(self.chara_data[list(self.chara_data.keys())[target]]["HP"][1])
        else:
            for i in self.chara_data.keys():
                self.chara_data[i]["HP"][1] = int(self.chara_data[i]["HP"][1])

    def atk_sum(self,action) -> tuple[float,float]:
        """
        攻撃力計算

        Parameters
        -----------
        action : dict
            アクションデータ
        Returns
        -----------
        atk : tuple[float,float]
            攻撃力
        """
        action_p = self.chara_data[list(self.chara_data.keys())[action["player_pos"]]]
        atk = 0
        atk += action_p["atk_ab"] * ((self.player_effect[action["player_pos"]]["basic_atk_buff"] + 100) / 100)
        isa_ = ["sword","staff","other"]
        for i,v in action_p["equipments"].items():
            if i in isa_:
                if self.tools[i][v][2] == "f":
                    atk += self.tools[i][v][3]
                else:
                    atk += action_p["atk_ab"] * (self.tools[i][v][3] / 100)
        atk *= (action_p["atk_buff"] + self.player_effect[action["player_pos"]]["atk_buff"] - self.player_effect[action["player_pos"]]["atk_dbuff"]) / 100
        return atk

    def target_attack_update(self):
        """敵攻撃"""
        try:
            action = self.player_op[self.attack_count]
            if action["target"] != "None" and action["sm"] != "item" and action["target_team"] != "self" and action["target"] != "none":
                if self.enemy_status[action["target"]]["HP"][1] <= 0:
                    live_e = []
                    for len_,v in enumerate(self.enemy_status):
                        if  v["HP"][1] > 0:
                            live_e.append(len_)
                    if len(live_e) == 0:
                        action["target"] = -1
                    else:
                        action["target"] = live_e[pyxel.rndi(0,len(live_e) - 1)]
        except Exception:
            pass
        if not self.enemy_animation:
            action = self.player_op[self.attack_count]
            atk = self.atk_sum(action)
            print(f"{action=}\n{self.player_effect[action['player_pos']]=}\n{atk=}\n\n\n")
            if action["target"] != "None" and action["sm"] != "item" and action["target_team"] != "self" and action["target"] != "none":
                while True:
                    if self.enemy_status[action["target"]]["HP"][1] <= 0:
                        live_e = []
                        for len_,v in enumerate(self.enemy_status):
                            if  v["HP"][1] > 0:
                                live_e.append(len_)
                        if len(live_e) == 0:
                            action["target"] = -1
                        else:
                            action["target"] = live_e[pyxel.rndi(0,len(live_e) - 1)]
                    else:
                        break
            if action["target"] != -1:
                if action["sm"] != "item":
                    if action["sm_code"] != "None":
                        int_code = int(action["sm_code"])
                    if action["target_team"] == "enemy":
                        def_ = self.enemy_status[action["target"]]["def_ab"] * ((100 + self.enemy_effect[action["target"]]["def_buff"] - self.enemy_effect[action["target"]]["def_dbuff"]) / 100)
                        kaisin_p = 1
                        if action["kaisin"]:
                            kaisin_p = self.chara_data[list(self.chara_data.keys())[action["player_pos"]]]["satisfaction"][1] // 100
                        if action["sm"] == "None":
                            if (atk - def_) * kaisin_p >= 0:
                                self.enemy_status[action["target"]]["HP"][1] -= (atk - def_) * kaisin_p
                        elif action["sm"] == "skill":
                            sm_info = self.magic_codes[action["sm"]][action["sm_code"]]
                            if action["sm_code"] == "01":
                                for _ in range(sm_info["other"]["atk_num"]):
                                    if (atk - def_) * kaisin_p >= 0:
                                        self.enemy_status[action["target"]]["HP"][1] -= (atk - def_) * kaisin_p
                            elif action["sm_code"] == "02":
                                cri_atk = atk * (self.chara_data[list(self.chara_data.keys())[action["player_pos"]]]["satisfaction"][1] / 100)
                                if cri_atk - def_ >= 0:
                                    self.enemy_status[action["target"]]["HP"][1] -= cri_atk - def_
                                self.player_effect[action["player_pos"]]["02_use"] = False
                            self.chara_data[list(self.chara_data.keys())[action["player_pos"]]]["MP"][1] -= sm_info["req_MP"]
                        elif action["sm"] == "magic":
                            if 1 <= int_code <= 15 or int_code == 21:
                                sm_info = self.magic_codes[action["sm"]][action["sm_code"]]
                                magic_atk = atk * sm_info["atk_amount"] / 100
                                if (magic_atk - def_) * kaisin_p >= 0:
                                    self.enemy_status[action["target"]]["HP"][1] -= (magic_atk - def_) * kaisin_p
                            elif 17 <= int_code <= 18:
                                sm_info = self.magic_codes[action["sm"]][action["sm_code"]]
                                if sm_info["dbuff_type"] == "atk":
                                    self.enemy_effect[action["target"]]["atk_dbuff"] += sm_info["dbuff_amount"]
                                elif sm_info["dbuff_type"] == "def":
                                    self.enemy_effect[action["target"]]["def_dbuff"] += sm_info["dbuff_amount"]
                            self.chara_data[list(self.chara_data.keys())[action["player_pos"]]]["MP"][1] -= sm_info["req_MP"]
                        if self.enemy_status[action["target"]]["HP"][1] < 0:
                            self.enemy_status[action["target"]]["HP"][1] = 0
                        self.player_effect[action["player_pos"]]["atk_buff"] = 0
                        self.player_effect[action["player_pos"]]["atk_dbuff"] = 0
                        self.player_effect[action["player_pos"]]["basic_atk_buff"] = 0
                        self.enemy_effect[action["target"]]["def_buff"] = 0
                        self.enemy_effect[action["target"]]["def_dbuff"] = 0
                    elif action["target_team"] == "self":
                        if action["sm"] == "skill":
                            sm_info = self.magic_codes[action["sm"]][action["sm_code"]]
                            if action["sm_code"] == "03":
                                if sm_info["recovery_amount"][0] == "p":
                                    self.chara_data[list(self.chara_data.keys())[action["target"]]]["HP"][1] += self.chara_data[list(self.chara_data.keys())[action["player_pos"]]]["HP"][0] * (sm_info["recovery_amount"][1] / 100)
                                else:
                                    self.chara_data[list(self.chara_data.keys())[action["target"]]]["HP"][1] += sm_info["recovery_amount"][1]
                            elif action["sm_code"] == "04":
                                self.player_effect[action["target"]]["recovery_turn"] = sm_info["other"]["continue_turn"]
                                self.player_effect[action["target"]]["recovery_info"] = sm_info["recovery_amount"]
                                self.player_effect[action["target"]]["recovery_turn"] -= 1
                                if self.player_effect[action["target"]]["recovery_info"][0] == "p":
                                    self.chara_data[list(self.chara_data.keys())[action["target"]]]["HP"][1] += self.chara_data[list(self.chara_data.keys())[action["player_pos"]]]["HP"][0] * (self.player_effect[action["target"]]["recovery_info"][1] / 100)
                                else:
                                    self.chara_data[list(self.chara_data.keys())[action["target"]]]["HP"][1] += self.player_effect[action["target"]]["recovery_info"][1]
                            elif action["sm_code"] == "05":
                                self.player_effect[action["target"]]["atk_invalid"] = True
                            elif action["sm_code"] == "07":
                                self.battle_effect["buff_up"] += sm_info["buff_amount"]
                            self.chara_data[list(self.chara_data.keys())[action["player_pos"]]]["MP"][1] -= sm_info["req_MP"]
                            if self.chara_data[list(self.chara_data.keys())[action["target"]]]["HP"][1] >= self.chara_data[list(self.chara_data.keys())[action["target"]]]["HP"][0]:
                                self.chara_data[list(self.chara_data.keys())[action["target"]]]["HP"][1] = self.chara_data[list(self.chara_data.keys())[action["target"]]]["HP"][0]
                        elif action["sm"] == "magic":
                            sm_info = self.magic_codes[action["sm"]][action["sm_code"]]
                            if action["sm_code"] == "16":
                                if sm_info["recovery_amount"][0] == "p":
                                    print(f'heal:{self.chara_data[list(self.chara_data.keys())[action["target"]]]["HP"][0] * (sm_info["recovery_amount"][1] / 100)}')
                                    self.chara_data[list(self.chara_data.keys())[action["target"]]]["HP"][1] += self.chara_data[list(self.chara_data.keys())[action["target"]]]["HP"][0] * (sm_info["recovery_amount"][1] / 100)
                                else:
                                    self.chara_data[list(self.chara_data.keys())[action["target"]]]["HP"][1] += sm_info["recovery_amount"][1]
                            elif 19 <= int_code <= 20:
                                if sm_info["buff_type"] == "atk":
                                    self.player_effect[action["target"]]["basic_atk_buff"] += sm_info["buff_amount"] + self.battle_effect["buff_up"]
                                elif sm_info["buff_type"] == "def":
                                    self.player_effect[action["target"]]["basic_def_buff"] += sm_info["buff_amount"] + self.battle_effect["buff_up"]
                                self.battle_effect["buff_up"] = 0
                            self.chara_data[list(self.chara_data.keys())[action["player_pos"]]]["MP"][1] -= sm_info["req_MP"]
                        self.hp_int(action["target"])
                    elif action["target_team"] == "none":
                        sm_info = self.magic_codes["skill"][action["sm_code"]]
                        if action["sm_code"] == "06":
                            for i in range(len(self.player_effect)):
                                self.player_effect[i]["atk_invalid"] = True
                        elif action["sm_code"] == "08":
                            if action["effect_invoke"]:
                                sm_info = self.magic_codes["magic"][action["effect_name"]]
                                if action["effect_type"] == "atk":
                                    def_ = self.enemy_status[action["target"]]["def_ab"] * (100 + self.enemy_effect[action["target"]]["def_buff"] - self.enemy_effect[action["target"]]["def_dbuff"]) / 100
                                    magic_atk = atk * sm_info["atk_amount"] / 100
                                    kaisin_p = 1
                                    if action["kaisin"]:
                                        kaisin_p = self.chara_data[list(self.chara_data.keys())[action["player_pos"]]]["satisfaction"][1] // 100
                                    if (magic_atk - def_) * kaisin_p >= 0:
                                        self.enemy_status[action["target"]]["HP"][1] -= (magic_atk - def_) * kaisin_p
                                elif action["effect_type"] == "rec":
                                    if sm_info["recovery_amount"][0] == "p":
                                        self.chara_data[list(self.chara_data.keys())[action["target"]]]["HP"][1] += self.chara_data[list(self.chara_data.keys())[action["target"]]]["HP"][0] * (sm_info["recovery_amount"][1] / 100)
                                    else:
                                        self.chara_data[list(self.chara_data.keys())[action["target"]]]["HP"][1] += sm_info["recovery_amount"][1]
                                elif action["effect_type"] == "dbuff":
                                    if sm_info["dbuff_type"] == "atk":
                                        self.enemy_effect[action["target"]]["atk_dbuff"] += sm_info["dbuff_amount"]
                                    elif sm_info["dbuff_type"] == "def":
                                        self.enemy_effect[action["target"]]["def_dbuff"] += sm_info["dbuff_amount"]
                                elif action["effect_type"] == "buff":
                                    if sm_info["buff_type"] == "atk":
                                        self.player_effect[action["target"]]["basic_atk_buff"] += sm_info["buff_amount"] + self.battle_effect["buff_up"]
                                    elif sm_info["buff_type"] == "def":
                                        self.player_effect[action["target"]]["basic_def_buff"] += sm_info["buff_amount"] + self.battle_effect["buff_up"]
                                    self.battle_effect["buff_up"] = 0
                        elif action["sm_code"] == "09":
                            self.random_range = pyxel.rndi(1,100)
                            if 1 <= self.random_range <= 5:
                                self.player_op[self.attack_count]["effect_invoke"] = True
                                self.player_op[self.attack_count]["effect_name"] = "atk_buff"
                                self.player_effect[action["player_pos"]]["atk_buff"] += 3
                        else:
                            for i in range(len(self.player_effect)):
                                self.player_effect[i]["atk_invalid"] = True
                                self.player_effect[i]["dmg_replace"] = True
                        self.chara_data[list(self.chara_data.keys())[action["player_pos"]]]["MP"][1] -= sm_info["req_MP"]
                else:
                    if (action["sm_code"]["type"] == "revival" and self.chara_data[action["target"]]["HP"][1] <= 0) or action["sm_code"]["type"] != "revival":
                        if action["sm_code"]["type"] == "HP":
                            size = pyxel.rndi(action["sm_code"]["effect"][0],action["sm_code"]["effect"][1])
                            self.chara_data[action["target"]]["HP"][1] += size
                            if self.chara_data[action["target"]]["HP"][1] > self.chara_data[action["target"]]["HP"][0]:
                                self.chara_data[action["target"]]["HP"][1] = self.chara_data[action["target"]]["HP"][0]
                        elif action["sm_code"]["type"] == "MP":
                            size = pyxel.rndi(action["sm_code"]["effect"][0],action["sm_code"]["effect"][1])
                            self.chara_data[action["target"]]["MP"][1] += size
                            if self.chara_data[action["target"]]["MP"][1] > self.chara_data[action["target"]]["MP"][0]:
                                self.chara_data[action["target"]]["MP"][1] = self.chara_data[action["target"]]["MP"][0]
                        elif action["sm_code"]["type"] == "revival":
                            self.chara_data[action["target"]]["HP"][1] = int(self.chara_data[action["target"]]["HP"][0] * (action["sm_code"]["effect"] / 100))
                            self.player_op.append({"player_pos":list(self.chara_data.keys()).index(action["target"]),"target":-1,"sm":"None","sm_code":"None"})
                        self.battle_item[list(self.battle_item.keys())[action["use_num"]]]["value"] -= 1
                        if self.app.item_codes[list(self.battle_item.keys())[action["use_num"]]]["value"] == 0:
                            self.app.item_codes.pop(list(self.battle_item.keys())[action["use_num"]])
                            self.battle_item.pop(list(self.battle_item.keys())[action["use_num"]])
                        print(f"{action['sm_code']=}")
            for i in self.chara_data.keys():
                if self.chara_data[i]["HP"][1] > self.chara_data[i]["HP"][0]:
                    self.chara_data[i]["HP"][1] = self.chara_data[i]["HP"][0]
            self.attack_count += 1
            self.enemy_animation = True
        else:
            live_e = [len_ for len_,v in enumerate(self.enemy_status) if  v["HP"][1] > 0]
            if self.attack_count == len(self.player_op):
                self.operation_player = False
                self.attack_count = 0
                self.select_num1 = -1
                self.select_num2 = -1
            if self.operation_player:
                if not (self.player_op[self.attack_count]["target"] != -1 and self.player_op[self.attack_count]["target_team"] == "enemy") and not (self.player_op[self.attack_count]["sm"] == "skill" and self.player_op[self.attack_count]["sm_code"] == "08"):
                    self.enemy_animation = False
                else:
                    if self.player_op[self.attack_count]["sm"] == "skill" and self.player_op[self.attack_count]["sm_code"] == "08" and not self.player_op[self.attack_count]["effect_check"]:
                        self.random_range = pyxel.rndi(1,100)
                        if 1 <= self.random_range <= 10:
                            random_magic = pyxel.rndi(1,20)
                            if random_magic < 10:
                                random_magic = f"0{random_magic}"
                            else:
                                random_magic = str(random_magic)
                            live_e = [len_ for len_,v in enumerate(self.enemy_status) if  v["HP"][1] > 0]
                            live_p = [len_ for len_,i in enumerate(self.chara_data) if self.chara_data[i]["HP"][1] > 0]
                            ran_p = live_p[pyxel.rndi(0,len(live_p) - 1)]
                            ran_e = live_e[pyxel.rndi(0,len(live_e) - 1)]
                            int_code = int(random_magic)
                            self.player_op[self.attack_count]["effect_invoke"] = True
                            self.player_op[self.attack_count]["effect_name"] = random_magic
                            if 1 <= int_code <= 15 or int_code == 21:
                                self.player_op[self.attack_count]["effect_type"] = "atk"
                                self.player_op[self.attack_count]["target"] = ran_e
                            elif int_code == 16:
                                self.player_op[self.attack_count]["effect_type"] = "rec"
                                self.player_op[self.attack_count]["target"] = ran_p
                            elif 17 <= int_code <= 18:
                                self.player_op[self.attack_count]["effect_type"] = "dbuff"
                                self.player_op[self.attack_count]["target"] = ran_e
                            elif 19 <= int_code <= 20:
                                self.player_op[self.attack_count]["effect_type"] = "buff"
                                self.player_op[self.attack_count]["target"] = ran_p
                        self.player_op[self.attack_count]["effect_check"] = True
                        if self.player_op[self.attack_count]["effect_type"] == "atk":
                            self.vibe_count = self.player_op[self.attack_count]["target"]
                        else:
                            self.vibe_count = "none"
                            self.enemy_animation = False
                    else:
                        self.vibe_count = self.player_op[self.attack_count]["target"]
                    if type(self.vibe_count) is int:
                        if self.vibe_enemy[self.vibe_count]["total"] >= 30:
                            self.enemy_animation = False
                            self.vibe_enemy[self.vibe_count] = {
                                "total":0,
                                "value":0,
                                "move":"p"
                            }
                            self.damage_pos = 0
                        elif self.vibe_enemy[self.vibe_count]["total"] < 30:
                            action = self.player_op[self.attack_count]
                            atk = self.atk_sum(action)
                            def_ = self.enemy_status[action["target"]]["def_ab"] * (100 + self.enemy_effect[action["target"]]["def_buff"] - self.enemy_effect[action["target"]]["def_dbuff"]) / 100
                            damage = False
                            damage_amount = 0
                            kaisin_p = 1
                            ####
                            #ダメージ計算
                            #遊び人のスキルによる魔法発動時のダメージ
                            ####
                            if action["kaisin"]:
                                kaisin_p = self.chara_data[list(self.chara_data.keys())[action["player_pos"]]]["satisfaction"][1] / 100
                            if action["sm"] == "None":
                                damage = True
                                damage_amount = (atk - def_) * kaisin_p
                            elif action["sm"] == "skill":
                                sm_info = self.magic_codes[action["sm"]][action["sm_code"]]
                                if action["sm_code"] == "01":
                                    damage = True
                                    damage_amount = (atk - def_) * kaisin_p * 2
                                elif action["sm_code"] == "02":
                                    damage = True
                                    cri_atk = atk * (self.chara_data[list(self.chara_data.keys())[action["player_pos"]]]["satisfaction"][1] / 100)
                                    damage_amount = cri_atk - def_
                                elif action["sm_code"] == "08":
                                    if action["effect_invoke"] and action["effect_type"] == "atk":
                                        sm_info = self.magic_codes["magic"][action["effect_name"]]
                                        damage = True
                                        magic_atk = atk * sm_info["atk_amount"] / 100
                                        damage_amount = (magic_atk - def_) * kaisin_p
                            elif action["sm"] == "magic":
                                int_code = int(action["sm_code"])
                                sm_info = self.magic_codes[action["sm"]][action["sm_code"]]
                                if 1 <= int_code <= 15 or int_code == 21:
                                    damage = True
                                    magic_atk = atk * sm_info["atk_amount"] / 100
                                    damage_amount = (magic_atk - def_) * kaisin_p
                            if damage:
                                enemy_interval = self.enemy_info["enemy_pos"][str(self.enemy_num)]
                                if damage_amount > 0:
                                    if action["kaisin"]:
                                        if self.damage_pos < -30:
                                            self.umplus10.draw_text(enemy_interval[action["target"]] + 12,20,str(int(damage_amount)),10)
                                        else:
                                            self.umplus10.draw_text(enemy_interval[action["target"]] + 12,50 + self.damage_pos,str(int(damage_amount)),10)
                                    else:
                                        if self.damage_pos < -30:
                                            self.umplus10.draw_text(enemy_interval[action["target"]] + 12,20,str(int(damage_amount)),8)
                                        else:
                                            self.umplus10.draw_text(enemy_interval[action["target"]] + 12,50 + self.damage_pos,str(int(damage_amount)),8)
                                else:
                                    if action["kaisin"]:
                                        if self.damage_pos < -30:
                                            self.umplus10.draw_text(enemy_interval[action["target"]] + 12,20,"0",10)
                                        else:
                                            self.umplus10.draw_text(enemy_interval[action["target"]] + 12,50 + self.damage_pos,"0",10)
                                    else:
                                        if self.damage_pos < -30:
                                            self.umplus10.draw_text(enemy_interval[action["target"]] + 12,20,"0",8)
                                        else:
                                            self.umplus10.draw_text(enemy_interval[action["target"]] + 12,50 + self.damage_pos,"0",8)
                                self.damage_pos -= 2
                            if self.vibe_enemy[self.vibe_count]["total"] == 0:
                                if action["kaisin"]:
                                    self.app.sound_manager.play_se("damage_enemy")
                                else:
                                    self.app.sound_manager.play_se("damage_enemy")
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
        """アイテム表示・選択"""
        if self.select_num2 == -1:
            if pyxel.btnp(pyxel.KEY_UP,hold = 8,repeat=8) or pyxel.btnp(pyxel.KEY_W,hold = 8,repeat = 8) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP,hold = 8,repeat=8):
                if self.finger_pos5 != 0:
                    self.finger_pos5 -= 18
                    self.app.sound_manager.play_se("select")
            if pyxel.btnp(pyxel.KEY_DOWN,hold = 8,repeat=8) or pyxel.btnp(pyxel.KEY_S,hold = 8,repeat = 8) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN,hold = 8,repeat=8):
                if self.finger_pos5 != (len(self.chara_data.items()) - 1) * 18:
                    self.finger_pos5 += 18
                    self.app.sound_manager.play_se("select")
            if pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.KEY_A,hold = 8,repeat = 8) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
                self.finger_pos5 = 0
                self.select_num3 = -1
                self.app.sound_manager.play_se("select")
            if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
                self.select_num2 = (self.finger_pos2 // 18)
                self.app.sound_manager.play_se("ok")
        else:
            if self.select_num3 == -1:
                if pyxel.btnp(pyxel.KEY_ESCAPE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
                    self.select_num1 = -1
                    self.app.sound_manager.play_se("select")
                if pyxel.btnp(pyxel.KEY_UP,hold = 8,repeat=8) or pyxel.btnp(pyxel.KEY_W,hold = 8,repeat = 8) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP,hold = 8,repeat=8):
                    if not (self.finger_pos3 == 0 or self.finger_pos3 == 1):
                        self.finger_pos3 -= 2
                        self.app.sound_manager.play_se("select")
                    elif self.item_pos - 2 >= 0:
                        self.item_pos -= 2
                        self.app.sound_manager.play_se("select")
                if pyxel.btnp(pyxel.KEY_DOWN,hold = 8,repeat=8) or pyxel.btnp(pyxel.KEY_S,hold = 8,repeat = 8) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN,hold = 8,repeat=8):
                    if self.finger_pos3 != 8 and self.finger_pos3 != 9:
                        if self.finger_pos3 + 2 < self.dis_num:
                            self.finger_pos3 += 2
                            self.app.sound_manager.play_se("select")
                    else:
                        if self.finger_pos3 + self.item_pos + 2 < self.item_num:
                            self.item_pos += 2
                            self.app.sound_manager.play_se("select")
                        elif self.finger_pos3 + self.item_pos + 2 == self.item_num and self.item_num > 10:
                            self.item_pos += 2
                            self.finger_pos3 -= 1
                            self.app.sound_manager.play_se("select")
                if pyxel.btnp(pyxel.KEY_RIGHT,hold = 8,repeat=8) or pyxel.btnp(pyxel.KEY_D,hold = 8,repeat = 8) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT,hold = 8,repeat=8):
                    if self.finger_pos3 + 1 < self.dis_num:
                        self.finger_pos3 += 1
                        self.app.sound_manager.play_se("select")
                    elif not self.item_pos + 13 <= self.item_num and self.finger_pos3 % 2 != 0:
                        self.finger_pos3 -= 1
                        self.item_pos += 2
                        self.app.sound_manager.play_se("select")
                    elif self.item_pos + 12 <= self.item_num:
                        self.finger_pos3 -= 1
                        self.item_pos += 2
                        self.app.sound_manager.play_se("select")
                if pyxel.btnp(pyxel.KEY_LEFT,hold = 8,repeat=8) or pyxel.btnp(pyxel.KEY_A,hold = 8,repeat = 8) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT,hold = 8,repeat=8):
                    if self.item_pos != 0:
                        if self.finger_pos3 == 0:
                            self.finger_pos3 += 1
                            self.item_pos -= 2
                        else:
                            self.finger_pos3 -= 1
                        self.app.sound_manager.play_se("select")
                    else:
                        if self.finger_pos3 != 0:
                            self.finger_pos3 -= 1
                            self.app.sound_manager.play_se("select")
                if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
                    if len(list(self.battle_item.keys())) > 0:
                        self.select_num3 = self.item_pos + self.finger_pos3
                        self.app.sound_manager.play_se("ok")
            else:
                if pyxel.btnp(pyxel.KEY_UP,hold = 8,repeat=8) or pyxel.btnp(pyxel.KEY_W,hold = 8,repeat = 8) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP,hold = 8,repeat=8):
                    if self.finger_pos5 != 0:
                        self.finger_pos5 -= 18
                        self.app.sound_manager.play_se("select")
                if pyxel.btnp(pyxel.KEY_DOWN,hold = 8,repeat=8) or pyxel.btnp(pyxel.KEY_S,hold = 8,repeat = 8) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN,hold = 8,repeat=8):
                    if self.finger_pos5 != (len(self.chara_data.items()) - 1) * 18:
                        self.finger_pos5 += 18
                        self.app.sound_manager.play_se("select")
                if pyxel.btnp(pyxel.KEY_LEFT,hold = 8,repeat=8) or pyxel.btnp(pyxel.KEY_A,hold = 8,repeat = 8) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A,hold = 8,repeat=8):
                    self.finger_pos5 = 0;
                    self.select_num3 = -1
                    self.app.sound_manager.play_se("select")
                if pyxel.btnp(pyxel.KEY_RETURN,hold = 8,repeat=8) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B,hold = 8,repeat=8):
                    use_item = self.tools["basic"][list(self.battle_item.items())[self.select_num3][0]]
                    use_player = list(self.chara_data.keys())[int(self.finger_pos5 // 18)]
                    if (use_item["type"] == "revival" and self.chara_data[use_player]["HP"][1] <= 0) or (use_item["type"] != "revival" and self.chara_data[use_player]["HP"][1] > 0):
                        tf = True
                        for x in self.player_op:
                            if x["target"] == use_player and x["sm_code"]["type"] == "revival":
                                tf = False
                        if tf:
                            self.player_op.append({"player_pos":self.select_num2,"target":use_player,"sm":"item","sm_code":use_item,"target_team":"self","use_num":self.select_num3})
                            self.player_op_over()
                            live_num = 0
                            for i in self.chara_data:
                                if self.chara_data[i]["HP"][1] != 0:
                                    live_num += 1
                            if len(self.player_op) != live_num:
                                self.select_num1 = -1
                                self.select_num2 = -1
                            self.finger_pos1 = 0
                            self.finger_pos2 = 0
                            self.finger_pos3 = 0
                            self.select_num3 = -1
                            self.finger_pos5 = 0
                            self.select_num5 = -1
                            self.app.sound_manager.play_se("ok")

    def update(self):
        """基本処理"""
        if self.in_battle:
            if self.operation_player:
                if self.select_num1 == -1:
                    if pyxel.btnp(pyxel.KEY_UP,hold = 8,repeat=8) or pyxel.btnp(pyxel.KEY_W,hold = 8,repeat = 8) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP,hold = 8,repeat=8):
                        if self.finger_pos1 != 0:
                            self.finger_pos1 -= 15
                        else:
                            self.finger_pos1 = 60
                        self.app.sound_manager.play_se("select")
                    if pyxel.btnp(pyxel.KEY_DOWN,hold = 8,repeat=8) or pyxel.btnp(pyxel.KEY_S,hold = 8,repeat = 8) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN,hold = 8,repeat=8):
                        if self.finger_pos1 != 60:
                            self.finger_pos1 += 15
                        else:
                            self.finger_pos1 = 0
                        self.app.sound_manager.play_se("select")
                    if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B) or pyxel.btnp(pyxel.KEY_RIGHT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
                        self.select_num1 = int(self.finger_pos1 // 15)
                        print(f"{self.select_num1=}")
                        self.select_num2 = -1
                        self.app.sound_manager.play_se("ok")
                elif self.select_num1 != 4:
                    if self.select_num2 == -1:
                        if 0 <= self.select_num1 <= 3:
                            if pyxel.btnp(pyxel.KEY_UP,hold = 8,repeat=8) or pyxel.btnp(pyxel.KEY_W,hold = 8,repeat = 8) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP,hold = 8,repeat=8):
                                if self.finger_pos2 != 0:
                                    self.finger_pos2 -= 18
                                else:
                                    self.finger_pos2 = (len(self.chara_data.items()) - 1) * 18
                                self.app.sound_manager.play_se("select")
                            if pyxel.btnp(pyxel.KEY_DOWN,hold = 8,repeat=8) or pyxel.btnp(pyxel.KEY_S,hold = 8,repeat = 8) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN,hold = 8,repeat=8):
                                if self.finger_pos2 != (len(self.chara_data.items()) - 1) * 18:
                                    self.finger_pos2 += 18
                                else:
                                    self.finger_pos2 = 0
                                self.app.sound_manager.play_se("select")
                            if pyxel.btnp(pyxel.KEY_ESCAPE) or pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.KEY_A) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
                                self.select_num1 = -1
                                self.finger_pos2 = 0
                                self.select_num2 = -1
                                self.app.sound_manager.play_se("select")
                            if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B) or pyxel.btnp(pyxel.KEY_RIGHT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
                                self.select_num2 = int(self.finger_pos2 // 18)
                                if self.chara_data[list(self.chara_data.keys())[self.select_num2]]["HP"][1] > 0:
                                    self.select_chara = list(self.chara_data.keys())[self.select_num2]
                                    if self.select_num1 == 1:
                                        self.finger_pos3 = 0
                                        self.item_num = 0
                                        self.item_pos = 0
                                        self.dis_num = 0
                                else:
                                    self.select_num2 = -1
                                self.app.sound_manager.play_se("ok")
                    else:
                        live_num = 0
                        for i in self.chara_data:
                            if self.chara_data[i]["HP"][1] > 0:
                                live_num += 1
                        if len(self.player_op) == live_num:
                            self.play_effect_info = True
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
                            elif self.select_num1 == 3:
                                self.item_update()
            else:
                if self.play_effect_info:
                    if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
                        self.play_effect_info = False
                        self.player_op = []
                        self.app.sound_manager.play_se("ok")
                else:
                    ai_input_data = []
                    live_enemy = [i for i in range(self.enemy_num) if self.enemy_status[i]["HP"][1] > 0]
                    live_p = [len_ for len_,i in enumerate(self.chara_data) if self.chara_data[i]["HP"][1] > 0]
                    if len(live_enemy) != 0:
                        #以下敵AIの行動をプレイヤーに適用
                        if self.ai_turn != self.turn:
                            for x in range(len(live_enemy)):
                                live_p = [len_ for len_,i in enumerate(self.chara_data) if self.chara_data[i]["HP"][1] > 0]
                                live_enemy = [i for i in range(self.enemy_num) if self.enemy_status[i]["HP"][1] > 0]
                                write_str = f"{len(self.chara_data)} "
                                for i in self.chara_data.keys():
                                    write_str += f'{self.chara_data[i]["post"]} {(self.chara_data[i]["HP"][1]/self.chara_data[i]["HP"][0]):.4f} {(self.chara_data[i]["MP"][1]/self.chara_data[i]["MP"][0]):.4f} '
                                write_str += f"{len(live_enemy)} "
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
                                ai_input_data[tmp_len - 1].append([0,0,pl_])
                                for i in range(pl_):
                                    ai_input_data[tmp_len - 1].append(write_str[1+i*3:1+(i+1)*3])
                                for i in range(4-pl_):
                                    ai_input_data[tmp_len - 1].append([0,0,0])
                                en_ = int(write_str[int(write_str[0])*3+1])
                                ai_input_data[tmp_len - 1].append([0,0,en_])
                                for i in range(en_):
                                    tm = [0,write_str[(len(live_p)*3+2)+i*2],write_str[(len(live_p)*3+2)+i*2+1]]
                                    ai_input_data[tmp_len - 1].append(tm)
                                for i in range(4-en_):
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
                            self.ai_action[:,0] -= 1
                            self.ai_turn = self.turn
                            print(f"{self.ai_action}")
                        i = self.attack_count
                        ai_ac = self.ai_action[i]
                        if int(ai_ac[0]) >= len(list(self.chara_data.keys())) or self.chara_data[list(self.chara_data.keys())[int(ai_ac[0])]]["HP"][1] <= 0:
                            ai_ac[0] = live_p[pyxel.rndi(0,len(live_p) - 1)]
                        if not self.player_animation:
                            if i < len(live_enemy):
                                action_p = self.chara_data[list(self.chara_data.keys())[int(ai_ac[0])]]
                                def_ = 0
                                isd_ = ["head","armor","leggings","boots","shield"]
                                dmg_target = int(ai_ac[0])
                                if True in [n["dmg_replace"] for n in self.player_effect]:
                                    for m,n in enumerate(self.player_effect):
                                        if n["dmg_replace"]:
                                            dmg_target = m
                                            break
                                def_ += action_p["def_ab"] * ((self.player_effect[dmg_target]["basic_def_buff"] + 100) / 100)
                                for x,v in action_p["equipments"].items():
                                    if x in isd_:
                                        if self.tools[x][v][2] == "f":
                                            def_ += self.tools[x][v][3]
                                        else:
                                            def_ += action_p["def_ab"] * (self.tools[x][v][3] / 100)
                                    def_ *= (action_p["def_buff"] + self.player_effect[dmg_target]["def_buff"] - self.player_effect[dmg_target]["def_dbuff"]) / 100
                                if 0 <= pyxel.rndi(0,100) <= self.enemy_status[live_enemy[i]]["satisfaction"][0]:
                                    atk = self.enemy_status[live_enemy[i]]["atk_ab"] * (100 + self.enemy_effect[live_enemy[i]]["atk_buff"] - self.enemy_effect[live_enemy[i]]["atk_dbuff"]) / 100 * (self.enemy_status[live_enemy[i]]["satisfaction"][1] / 100)
                                else:
                                    atk = self.enemy_status[live_enemy[i]]["atk_ab"] * (100 + self.enemy_effect[live_enemy[i]]["atk_buff"] - self.enemy_effect[live_enemy[i]]["atk_dbuff"]) / 100
                                if not self.player_effect[int(ai_ac[0])]["atk_invalid"]:
                                    if int(ai_ac[1]) == 1:
                                        if atk - def_ >= 0:
                                            self.chara_data[list(self.chara_data.keys())[int(ai_ac[0])]]["HP"][1] -= atk - def_
                                    else:
                                        print(f'enemy_mp:{self.enemy_status[live_enemy[i]]["MP"][1]} atk:{atk} def:{def_}')
                                        if self.enemy_status[live_enemy[i]]["MP"][1] >= 30:
                                            if (atk * 2) - def_ >= 0:
                                                self.chara_data[list(self.chara_data.keys())[int(ai_ac[0])]]["HP"][1] -= (atk * 2) - def_
                                            self.enemy_status[live_enemy[i]]["MP"][1] -= 30
                                        else:
                                            if atk - def_ >= 0:
                                                self.chara_data[list(self.chara_data.keys())[int(ai_ac[0])]]["HP"][1] -= atk - def_
                                    if self.chara_data[list(self.chara_data.keys())[int(ai_ac[0])]]["HP"][1] < 0:
                                        self.chara_data[list(self.chara_data.keys())[int(ai_ac[0])]]["HP"][1] = 0
                                    self.player_effect[int(ai_ac[0])]["def_buff"] = 0
                                    self.player_effect[int(ai_ac[0])]["def_dbuff"] = 0
                                    self.player_effect[int(ai_ac[0])]["basic_def_buff"] = 0
                                    self.enemy_effect[live_enemy[i]]["atk_buff"] = 0
                                    self.enemy_effect[live_enemy[i]]["atk_dbuff"] = 0
                                    self.player_animation = True
                                elif True in [n["dmg_replace"] for n in self.player_effect]:
                                    for m,n in enumerate(self.player_effect):
                                        if n["dmg_replace"]:
                                            if ai_ac[1] == 1:
                                                if atk - def_ >= 0:
                                                    self.chara_data[list(self.chara_data.keys())[m]]["HP"][1] -= atk - def_
                                            else:
                                                print(f'enemy_mp:{self.enemy_status[live_enemy[i]]["MP"][1]} atk:{atk} def:{def_}')
                                                if self.enemy_status[live_enemy[i]]["MP"][1] >= 30:
                                                    if (atk * 2) - def_ >= 0:
                                                        self.chara_data[list(self.chara_data.keys())[m]]["HP"][1] -= (atk * 2) - def_
                                                    self.enemy_status[live_enemy[i]]["MP"][1] -= 30
                                                else:
                                                    if atk - def_ >= 0:
                                                        self.chara_data[list(self.chara_data.keys())[m]]["HP"][1] -= atk - def_
                                            if self.chara_data[list(self.chara_data.keys())[m]]["HP"][1] < 0:
                                                self.chara_data[list(self.chara_data.keys())[m]]["HP"][1] = 0
                                            if len(self.ai_action) - 1 == i:
                                                self.player_effect[m]["dmg_replace"] = False
                                            self.player_effect[int(ai_ac[0])]["atk_invalid"] = False
                            self.attack_count += 1
                            if self.attack_count == len(self.ai_action):
                                self.operation_player = True
                                self.attack_count = 0
                                self.attack_count = 0
                                self.turn += 1
                                print(f"{self.player_effect=}")
                                for n,effect in enumerate(self.player_effect):
                                    if effect["recovery_turn"] != 0:
                                        if effect["recovery_info"][0] == "p":
                                            self.chara_data[list(self.chara_data.keys())[n]]["HP"][1] += self.chara_data[list(self.chara_data.keys())[n]]["HP"][0] * (effect["recovery_info"][1] / 100)
                                        else:
                                            self.chara_data[list(self.chara_data.keys())[n]]["HP"][1] += effect["recovery_info"][1]
                                        if self.chara_data[list(self.chara_data.keys())[n]]["HP"][1] >= self.chara_data[list(self.chara_data.keys())[n]]["HP"][0]:
                                            self.chara_data[list(self.chara_data.keys())[n]]["HP"][1] = self.chara_data[list(self.chara_data.keys())[n]]["HP"][0]
                                        self.player_effect[n]["recovery_turn"] -= 1
                                    if effect["atk_invalid"]:
                                        self.player_effect[n]["atk_invalid"] = False
                        else:
                            if self.vibe_player[int(ai_ac[0])]["total"] >= 10:
                                self.player_animation = False
                                self.vibe_player[int(ai_ac[0])] = {
                                    "total":0,
                                    "value":0,
                                    "move":"p"
                                }
                            else:
                                if int(ai_ac[0]) < len(self.vibe_player):
                                    if self.vibe_player[int(ai_ac[0])]["total"] == 0:
                                        if int(ai_ac[1]) == 2 and self.enemy_status[live_enemy[i]]["MP"][1] >= 30:
                                            self.vibe_player[int(ai_ac[0])]["strength"] = True
                                            self.vibe_player[int(ai_ac[0])]["strength_count"] = 0
                                        else:
                                            self.vibe_player[int(ai_ac[0])]["strength"] = False
                                        self.app.sound_manager.play_se("damage_self")
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
                                    else:
                                        self.vibe_player[int(ai_ac[0])]["total"] = 10
                                    vibe["total"] += 1
                        self.hp_int("none")
        else:
            if self.win == "player":
                if not self.wl_sound:
                    self.app.sound_manager.stop()
                    print("win_sound")
                    self.app.bgm_run = False
                    self.app.sound_manager.play_bgm("battle_win",loop=False)
                    self.app.bgm_run = True
                    self.wl_sound = True
                if not self.xp_stop:
                    if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
                        while not self.xp_stop:
                            for i,k in enumerate(self.chara_data.keys()):
                                be_level_ten = 0
                                no_level_ten = 0
                                if not self.xp_get:
                                    self.xp_up[k][2] = self.chara_data[k]["Level"]
                                xp = 0
                                level = self.chara_data[k]["Level"] + 1
                                if 0 <= level <= 16:
                                    xp = level ** 2 + 6 * level
                                elif 17 <= level <= 30:
                                    xp = (5 / 2) * level ** 2 - (81 / 2) * level + 360
                                elif 31 <= level:
                                    xp = (9 / 2) * level ** 2 - (325 / 2) * level + 2220
                                if self.chara_data[k]["XP"] >= xp:
                                    self.chara_data[k]["Level"] += 1
                                    self.chara_data[k]["XP"] -= xp
                                    if len(str(self.xp_up[k][2])) > 1:
                                        be_level_ten = int(str(self.xp_up[k][2])[-2])
                                    if len(str(self.chara_data[k]["Level"])) > 1:
                                        no_level_ten = int(str(self.chara_data[k]["Level"])[-2])
                                    if be_level_ten < no_level_ten:
                                        ten_level = no_level_ten - be_level_ten
                                        self.status_diff[k]["satisfaction"][0] = self.levelup_data["satisfaction"][0] * ten_level
                                        self.status_diff[k]["satisfaction"][1] = self.levelup_data["satisfaction"][1] * ten_level
                                    self.status_diff[k]["HP"] += self.levelup_data["HP"]
                                    self.status_diff[k]["MP"] += self.levelup_data["MP"]
                                    self.status_diff[k]["atk_ab"] += self.levelup_data["atk_ab"]
                                    self.status_diff[k]["def_ab"] += self.levelup_data["def_ab"]
                                if not self.xp_stop:
                                    if self.xp_up[k][0] >= 15:
                                        self.chara_data[k]["XP"] += 15
                                        self.xp_up[k][0] -= 15
                                    else:
                                        self.chara_data[k]["XP"] += self.xp_up[k][0]
                                        self.xp_up[k][0] = 0
                                    for j in self.xp_up:
                                        if self.xp_up[j][0] == 0:
                                            self.xp_stop = True
                                        else:
                                            self.xp_stop = False
                        self.check_level()
                        self.xp_stop = True
                        self.app.sound_manager.play_se("ok")
                else:
                    if not self.win_show:
                        if not self.sm_level:
                            for sm in ["magic","skill"]:
                                for chara in self.chara_data.keys():
                                    if chara in self.app.chara_levelup[sm]:
                                        for level_j in self.app.chara_levelup[sm][chara].keys():
                                            base_level = self.chara_data[chara]["Level"] - self.status_diff[chara]["HP"] // self.levelup_data["HP"]
                                            if base_level < int(level_j) <= self.chara_data[chara]["Level"]:
                                                for sm_code in self.app.chara_levelup[sm][chara][level_j]["add"]:
                                                    if sm_code not in self.chara_data[chara][f"{sm}_codes"]:
                                                        print(f"add player:{chara} {sm}:{sm_code}")
                                                        if sm not in self.add_sm.keys():
                                                            self.add_sm[sm] = {}
                                                        if chara not in self.add_sm[sm].keys():
                                                            self.add_sm[sm][chara] = []
                                                        self.add_sm[sm][chara].append(sm_code)
                                                        self.chara_data[chara][f"{sm}_codes"].append(sm_code)
                                                if "remove" in self.app.chara_levelup[sm][chara][level_j]:
                                                    for sm_code in self.app.chara_levelup[sm][chara][level_j]["remove"]:
                                                        if sm_code in self.chara_data[chara][f"{sm}_codes"]:
                                                            print(f"remove player:{chara} {sm}:{sm_code}")
                                                            self.chara_data[chara][f"{sm}_codes"].remove(sm_code)
                            # self.add_sm = {
                            #     "magic":{
                            #         "ぼく":["01","03","05"],
                            #         "リョウガ":["02","04"]
                            #     },
                            #     "skill":{
                            #         "ぼく":["01","03","05"],
                            #         "リョウガ":["02","04"]
                            #     }
                            # }
                            self.sm_level = True
                        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
                            for i in self.xp_up:
                                self.chara_data[i]["XP"] += self.xp_up[i][0]
                                self.xp_up[i][0] -= 0
                                self.chara_data[i]["HP"][0] += self.status_diff[i]["HP"]
                                self.chara_data[i]["MP"][0] += self.status_diff[i]["MP"]
                                self.chara_data[i]["atk_ab"] += self.status_diff[i]["atk_ab"]
                                self.chara_data[i]["def_ab"] += self.status_diff[i]["def_ab"]
                                self.chara_data[i]["satisfaction"][0] += self.status_diff[i]["satisfaction"][0]
                                self.chara_data[i]["satisfaction"][1] += self.status_diff[i]["satisfaction"][1]
                            money = 0
                            for i in self.enemy_status:
                                money += i["money"]
                            for i in self.get_item:
                                item = self.app.tools["basic"][i]
                                if i in self.app.item_codes:
                                    self.app.item_codes[i]["value"] += 1
                                else:
                                    self.app.item_codes[i] = {
                                        "value":1,
                                        "battle":item["battle"]
                                    }
                            for i in self.chara_data.keys():
                                if self.chara_data[i]["HP"][1] <= 0:
                                    self.chara_data[i]["HP"][1] = 1
                                self.chara_data[i] = self.chara_data[i]
                            self.app.money += money
                            self.win_show = True
                            if self.add_sm != {}:
                                self.add_sm_tf = True
                            if not self.add_sm_tf:
                                self.app.now_scene = self.be_scene
                                self.app.in_battle = False
                                if "battle" in self.app.words_j["story"][self.app.disp_id]:
                                    self.app.msg_id = self.app.words_j["story"][self.app.disp_id]["battle"][1]
                                elif self.app.random_encount:
                                    self.app.random_encount = False
                                self.app.sound_manager.stop()
                                self.app.sound_manager.play_se("ok")
                                self.app.bgm_run = False
                    elif self.add_sm_tf:
                        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
                            self.app.now_scene = self.be_scene
                            self.app.in_battle = False
                            if "battle" in self.app.words_j["story"][self.app.disp_id]:
                                self.app.msg_id = self.app.words_j["story"][self.app.disp_id]["battle"][1]
                            elif self.app.random_encount:
                                self.app.random_encount = False
                            self.app.sound_manager.stop()
                            self.app.sound_manager.play_se("ok")
                            self.app.bgm_run = False
            else:
                if not self.wl_sound:
                    self.app.sound_manager.stop()
                    self.app.bgm_run = False
                    self.wl_sound = True
                if self.select_num1 == -1:
                    if pyxel.btnp(pyxel.KEY_UP,hold = 8,repeat=8) or pyxel.btnp(pyxel.KEY_W,hold = 8,repeat = 8) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP,hold = 8,repeat=8):
                        if self.finger_pos1 != 0:
                            self.finger_pos1 -= 11
                        else:
                            self.finger_pos1 = 11
                        self.app.sound_manager.play_se("select")
                    if pyxel.btnp(pyxel.KEY_DOWN,hold = 8,repeat=8) or pyxel.btnp(pyxel.KEY_S,hold = 8,repeat = 8) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN,hold = 8,repeat=8):
                        if self.finger_pos1 != 11:
                            self.finger_pos1 += 11
                        else:
                            self.finger_pos1 = 0
                        self.app.sound_manager.play_se("select")
                    if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
                        self.select_num1 = self.finger_pos1 // 11
                        self.app.sound_manager.play_se("ok")
                else:
                    if self.select_num1 == 0:
                        self.app.chara_data = copy.deepcopy(self.save_chara_data)
                        self.clean(self.be_scene)
                        self.set_enemy(self.enemy_num,self.enemy_code)
                    elif self.select_num1 == 1:
                        self.app.save_load.update(over_load=False,left=False,load=True,battle_load = True)

    def sm_draw(self,sm):
        """
        魔法・スキル描画

        Parameters
        -----------
        sm : str
            魔法かスキル
        """
        pyxel.rect(110,self.init_y//2+10,185,75,0)
        pyxel.rectb(110,self.init_y//2+10,185,75,7)
        pyxel.rect(25,self.init_y//2-20,270,25,0)
        pyxel.rectb(25,self.init_y//2-20,270,25,7)
        if len(self.chara_data[self.select_chara][f"{sm}_codes"]) > 0:
            if len(self.magic_codes[sm][self.chara_data[self.select_chara][f"{sm}_codes"][self.item_pos + self.finger_pos3]]["info"]) > 27:
                for i,j in zip(range(0,len(self.magic_codes[sm][self.chara_data[self.select_chara][f"{sm}_codes"][self.item_pos + self.finger_pos3]]["info"]),27),range(5)):
                    self.umplus10.draw_text(26,self.init_y//2-19 + 11 * j,self.magic_codes[sm][self.chara_data[self.select_chara][f"{sm}_codes"][self.item_pos + self.finger_pos3]]["info"][i:i + 27],7)
            else:
                self.umplus10.draw_text(26,self.init_y//2-19,self.magic_codes[sm][self.chara_data[self.select_chara][f"{sm}_codes"][self.item_pos + self.finger_pos3]]["info"],7)
            self.umplus10.draw_text(110,self.init_y-12,"※戻るにはESCキーまたはＡボタンを押す",8)
            self.item_num = len(self.chara_data[self.select_chara][f"{sm}_codes"])
            if self.item_num >= self.item_pos + 11:
                self.dis_num = 10
                for i,item in zip(range(10),self.chara_data[self.select_chara][f"{sm}_codes"][self.item_pos:self.item_pos + 10]):
                    h = int(i // 2)
                    w = i % 2
                    if i == self.finger_pos3:
                        pyxel.rect(111+(w*91),self.init_y//2+11+(h*14.4),92,15,1)

                    if self.magic_codes[sm][item]["name"] == "一刀両断" and not self.player_effect[self.select_num2]["02_use"]:
                        self.umplus10.draw_text(111+(w*93),self.init_y//2+12+(h*15),self.magic_codes[sm][item]["name"],8)
                    else:
                        self.umplus10.draw_text(111+(w*93),self.init_y//2+12+(h*15),self.magic_codes[sm][item]["name"],7)

                    if self.magic_codes[sm][item]["req_MP"] > self.chara_data[self.select_chara]["MP"][1]:
                        self.umplus10.draw_text(190+(w*93),self.init_y//2+12+(h*15),str(self.magic_codes[sm][item]["req_MP"]).rjust(2," "),8)
                    else:
                        self.umplus10.draw_text(190+(w*93),self.init_y//2+12+(h*15),str(self.magic_codes[sm][item]["req_MP"]).rjust(2," "),5)
            else:
                self.dis_num = self.item_num - self.item_pos
                for i,item in zip(range(self.item_num-self.item_pos),self.chara_data[self.select_chara][f"{sm}_codes"][self.item_pos:self.item_num]):
                    h = int(i // 2)
                    w = i % 2
                    if i == self.finger_pos3:
                        pyxel.rect(111+(w*91),self.init_y//2+11+(h*14.4),92,15,1)

                    if self.magic_codes[sm][item]["name"] == "一刀両断" and not self.player_effect[self.select_num2]["02_use"]:
                        self.umplus10.draw_text(111+(w*93),self.init_y//2+12+(h*15),self.magic_codes[sm][item]["name"],8)
                    else:
                        self.umplus10.draw_text(111+(w*93),self.init_y//2+12+(h*15),self.magic_codes[sm][item]["name"],7)

                    if self.magic_codes[sm][item]["req_MP"] > self.chara_data[self.select_chara]["MP"][1]:
                        self.umplus10.draw_text(190+(w*93),self.init_y//2+12+(h*15),str(self.magic_codes[sm][item]["req_MP"]).rjust(2," "),8)
                    else:
                        self.umplus10.draw_text(190+(w*93),self.init_y//2+12+(h*15),str(self.magic_codes[sm][item]["req_MP"]).rjust(2," "),5)

    def item_draw(self):
        """アイテムの描画"""
        pyxel.rect(110,self.init_y//2+10,185,75,0)
        pyxel.rectb(110,self.init_y//2+10,185,75,7)
        pyxel.rect(25,self.init_y//2-20,270,25,0)
        pyxel.rectb(25,self.init_y//2-20,270,25,7)
        self.umplus10.draw_text(110,self.init_y-12,"※戻るにはESCキーまたはＡボタンを押す",8)
        if len(list(self.battle_item.keys())) > 0:
            self.umplus10.draw_text(26,self.init_y//2-19,self.tools["basic"][list(self.battle_item.keys())[self.item_pos + self.finger_pos3]]["info"],7)
            self.item_num = len(self.battle_item.items())
            if self.item_num >= self.item_pos + 11:
                self.dis_num = 10
                for i,item in enumerate(self.battle_item.items()):
                    h = int(i // 2)
                    w = i % 2
                    if i == self.finger_pos3:
                        pyxel.rect(111+(w*91),self.init_y//2+11+(h*14.4),92,15,1)
                    self.umplus10.draw_text(111+(w*93),self.init_y//2+12+(h*15),self.tools["basic"][item[0]]["name"],7)
                    self.umplus10.draw_text(190+(w*93),self.init_y//2+13+(h*15),str(item[1]["value"]).rjust(2," "),7)
            else:
                self.dis_num = self.item_num - self.item_pos
                for i,item in enumerate(list(self.battle_item.items())[self.item_pos:self.item_num]):
                    h = int(i // 2)
                    w = i % 2
                    if i == self.finger_pos3:
                        pyxel.rect(111+(w*91),self.init_y//2+11+(h*14.4),92,15,1)
                    self.umplus10.draw_text(111+(w*93),self.init_y//2+12+(h*15),self.tools["basic"][item[0]]["name"],7)
                    self.umplus10.draw_text(190+(w*93),self.init_y//2+13+(h*15),str(item[1]["value"]).rjust(2," "),7)


    def enemy_target_select_draw(self):
        """敵ターゲット選択描画"""
        self.umplus10.draw_text(110,self.init_y-12,"※戻るにはESCキーまたはＡボタンを押す",8)
        pyxel.blt(self.finger_pos4 - 8,2,self.finger_ws[0],self.finger_ws[1],self.finger_ws[2],self.finger_ws[3],self.finger_ws[4],self.finger_ws[5])

    def self_target_select_draw(self,fin = 5):
        """
        味方ターゲット選択描画

        Parameters
        -----------
        fin : Any
            不明
        """
        pyxel.rect(110,self.init_y//2+10,185,75,0)
        pyxel.rectb(110,self.init_y//2+10,185,75,7)
        live_num = 0
        live_p = []
        for len_,i in enumerate(self.chara_data):
            if self.app.chara_data[i]["HP"][1] > 0:
                live_num += 1
                live_p.append(len_)

        for i,data in zip(range(1,1+len(self.chara_data.items())),enumerate(self.chara_data)):
            op_player = False
            for j in self.player_op:
                if j["player_pos"] == data[0]:
                    op_player = True
                    break
            height = 18*(i - 1)
            if self.select_num1 != 0 and self.select_num1 != 1 and self.select_num1 != 2 and self.select_num1 != 3:
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
            pyxel.rect(178,self.init_y//2+14+height,(self.chara_data[data[1]]["HP"][1]/self.chara_data[data[1]]["HP"][0])*100,5,11)
            pyxel.rectb(178,self.init_y//2+14+height,100,5,7)
            pyxel.text(279,self.init_y//2+14+height,f"{self.chara_data[data[1]]['HP'][1]}",11)
            pyxel.rect(178,self.init_y//2+21+height,(self.chara_data[data[1]]["MP"][1]/self.chara_data[data[1]]["MP"][0])*100,5,5)
            pyxel.rectb(178,self.init_y//2+21+height,100,5,7)
            pyxel.text(279,self.init_y//2+21+height,f"{self.chara_data[data[1]]['MP'][1]}",5)
        if fin == 5:
            pyxel.blt(115,self.init_y//2+15+(self.finger_pos5),self.finger_ad[0],self.finger_ad[1],self.finger_ad[2],self.finger_ad[3],self.finger_ad[4],self.finger_ad[5])
        elif fin == "5_":
            self.umplus10.draw_text(210,self.init_y-12,"※対象を選択",8)
            pyxel.blt(115,self.init_y//2+15+(self.finger_pos5),self.finger_ad[0],self.finger_ad[1],self.finger_ad[2],self.finger_ad[3],self.finger_ad[4],self.finger_ad[5])
        elif fin == 2:
            self.umplus10.draw_text(210,self.init_y-12,"※使用者を選択",8)
            pyxel.blt(115,self.init_y//2+15+(self.finger_pos2),self.finger_ad[0],self.finger_ad[1],self.finger_ad[2],self.finger_ad[3],self.finger_ad[4],self.finger_ad[5])

    def draw(self):
        """基本描画"""
        pyxel.cls(0)
        pyxel.rect(25,self.init_y//2+10,75,75,0)
        pyxel.rectb(25,self.init_y//2+10,75,75,7)
        pyxel.rect(50,self.init_y//2+10,25,4,0)
        pyxel.rect(110,self.init_y//2+10,185,75,0)
        pyxel.rectb(110,self.init_y//2+10,185,75,7)
        live_num = 0
        live_p = []
        for len_,i in enumerate(self.chara_data):
            if self.chara_data[i]["HP"][1] > 0:
                live_num += 1
                live_p.append(len_)
        live_e = [len_ for len_,v in enumerate(self.enemy_status) if  v["HP"][1] > 0]
        if self.win == "":
            if len(live_e) == 0:
                self.win = "player"
                self.in_battle = False
            elif len(live_p) == 0:
                self.win = "enemy"
                self.finger_pos1 = 0
                self.select_num1 = -1
                self.in_battle = False

        for i,data,ch_i in zip(range(1,1+len(self.chara_data.items())),enumerate(self.chara_data),range(len(self.chara_data.keys()))):
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
            pyxel.rect(178 + self.vibe_player[ch_i]["value"],self.init_y//2+14+height,(self.chara_data[data[1]]["HP"][1] / self.chara_data[data[1]]["HP"][0]) * 100,5,11)
            pyxel.rectb(178 + self.vibe_player[ch_i]["value"],self.init_y//2+14+height,100,5,7)
            pyxel.text(279,self.init_y//2+14+height,f"{self.chara_data[data[1]]['HP'][1]}",11)
            pyxel.rect(178 + self.vibe_player[ch_i]["value"],self.init_y//2+21+height,(self.chara_data[data[1]]["MP"][1] / self.chara_data[data[1]]["MP"][0]) * 100,5,5)
            pyxel.rectb(178 + self.vibe_player[ch_i]["value"],self.init_y//2+21+height,100,5,7)
            pyxel.text(279,self.init_y//2+21+height,f"{self.chara_data[data[1]]['MP'][1]}",5)
            if "strength" in self.vibe_player[ch_i]:
                if self.vibe_player[ch_i]["strength"] and self.vibe_player[ch_i]["strength_count"] <= 60:
                    self.umplus10.draw_text(5,0,"敵が強化攻撃を使用した".center(28,"　"),7)
                    self.vibe_player[ch_i]["strength_count"] += 1
        for n,i in enumerate(self.enemy_code):
            if n in live_e:
                enemy_data = self.enemy_info[i["enemy_type"]][i["enemy_code"]]["basis"]
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
            if self.operation_player:
                if live_num == 0:
                    self.in_battle = False
                else:
                    if len(self.player_op) == live_num:
                        if self.effect_info:
                            use_magic = []
                            for i,n in enumerate(self.player_op):
                                if n["sm"] == "skill":
                                    if 5 <= int(n["sm_code"]) <= 7 or int(n["sm_code"]) == 10:
                                        use_magic.append(n)
                                elif n["sm"] == "magic":
                                    if 19 <= int(n["sm_code"]) <= 20:
                                        use_magic.append(n)
                                elif n["sm"] == "item":
                                    use_magic.append(n)
                            # print(use_magic)
                            if use_magic != []:
                                pyxel.rect(35,self.init_y//2+20,230,60,0)
                                pyxel.rectb(35,self.init_y//2+20,230,60,7)
                                for i,n in enumerate(use_magic):
                                    if n["sm"] == "skill":
                                        if n["sm_code"] == "05":
                                            self.umplus10.draw_text(36,self.init_y//2+20+(i*15),f"{list(self.chara_data.keys())[n['target']]}への攻撃を１ターン無効",7)
                                        elif n["sm_code"] == "06":
                                            self.umplus10.draw_text(36,self.init_y//2+20+(i*15),"全ての味方への攻撃を１ターン無効",7)
                                        elif n["sm_code"] == "07":
                                            self.umplus10.draw_text(36,self.init_y//2+20+(i*15),"魔法ののステータスアップ率を＋３％",7)
                                        elif n["sm_code"] == "10":
                                            self.umplus10.draw_text(36,self.init_y//2+20+(i*15),"味方全員に対する攻撃を肩代わり",7)
                                    elif n["sm"] == "magic":
                                        if n["sm_code"] == "19":
                                            self.umplus10.draw_text(36,self.init_y//2+20+(i*15),f"{list(self.chara_data.keys())[n['target']]}の防御力を３０％アップ",7)
                                        elif n["sm_code"] == "20":
                                            self.umplus10.draw_text(36,self.init_y//2+20+(i*15),f"{list(self.chara_data.keys())[n['target']]}の攻撃力を３０％アップ",7)
                                    elif n["sm"] == "item":
                                        self.umplus10.draw_text(36,self.init_y//2+20+(i*15),f"{list(self.chara_data.keys())[n['player_pos']]}が{[n['target']][0]}に{n['sm_code']['name']}を使用した",7)
                            else:
                                self.effect_info = False
                        else:
                            self.target_attack_update()
                    else:
                        pyxel.blt(7,self.init_y//2+15+(self.finger_pos1),self.finger_ad[0],self.finger_ad[1],self.finger_ad[2],self.finger_ad[3],self.finger_ad[4],self.finger_ad[5])
                        if self.select_num1 == 0:
                            pyxel.blt(112,self.init_y//2+15+(self.finger_pos2),self.finger_ad[0],self.finger_ad[1],self.finger_ad[2],self.finger_ad[3],self.finger_ad[4],self.finger_ad[5])
                            if self.select_num2 != -1:
                                self.enemy_target_select_draw()
                        elif self.select_num1 == 1:
                            pyxel.blt(112,self.init_y//2+15+(self.finger_pos2),self.finger_ad[0],self.finger_ad[1],self.finger_ad[2],self.finger_ad[3],self.finger_ad[4],self.finger_ad[5])
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
                            pyxel.blt(112,self.init_y//2+15+(self.finger_pos2),self.finger_ad[0],self.finger_ad[1],self.finger_ad[2],self.finger_ad[3],self.finger_ad[4],self.finger_ad[5])
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
                            pyxel.blt(112,self.init_y//2+15+(self.finger_pos2),self.finger_ad[0],self.finger_ad[1],self.finger_ad[2],self.finger_ad[3],self.finger_ad[4],self.finger_ad[5])
                            if self.select_num2 != -1:
                                if self.select_num3 == -1:
                                    self.item_draw()
                                else:
                                    self.self_target_select_draw(fin="5_")
                            else:
                                self.self_target_select_draw(fin=2)
                        elif self.select_num1 == 4:
                            if self.in_boss:
                                self.escape = True
                                self.select_num1 = -1
                            else:
                                if 1 <= pyxel.rndi(1,100) <= self.escape_rate:
                                    self.app.now_scene = self.be_scene
                                    self.app.random_encount = False
                                    self.app.sound_manager.stop()
                                    self.app.bgm_run = False
                                else:
                                    self.escape = True
                                    self.escape_rate += 25
                                    self.select_num1 = -1
                            if not self.in_boss:
                                self.select_num1 = -1
                                self.operation_player = False
            else:
                if self.play_effect_info:
                    play_ef = []
                    for i in self.player_op:
                        if "effect_invoke" in i:
                            if i["effect_invoke"]:
                                play_ef.append([i["effect_name"],i["sm_code"],i["player_pos"]])
                            else:
                                play_ef.append(["none",i["sm_code"],i["player_pos"]])
                    if play_ef != []:
                        pyxel.rect(35,self.init_y//2+20,230,60,0)
                        pyxel.rectb(35,self.init_y//2+20,230,60,7)
                        for i,n in enumerate(play_ef):
                            p_name = list(self.chara_data.keys())[n[2]]
                            magic_name = self.magic_codes["skill"][n[1]]["name"]
                            if n[0] == "atk_buff":
                                self.umplus10.draw_text(36,self.init_y//2+20+(i*15),f"{p_name}が口笛を吹いて攻撃力が３％アップした",7)
                            elif n[0] == "none":
                                if magic_name == "口笛":
                                    self.umplus10.draw_text(36,self.init_y//2+20+(i*15),f"{p_name}が口笛を吹いたが何も起こらなかった",7)
                                else:
                                    self.umplus10.draw_text(36,self.init_y//2+20+(i*15),f"{p_name}が遊んだが何も起こらなかった",7)
                            else:
                                magic_info = self.magic_codes["magic"][n[0]]
                                self.umplus10.draw_text(36,self.init_y//2+20+(i*15),f"{p_name}が遊んで{magic_info['name']}を発動した",7)
                    else:
                        self.play_effect_info = False
                        self.player_op = []
            if self.escape or self.escape_count != 0:
                if self.escape_count < 60:
                    pyxel.rect(40,177,220,15,0)
                    pyxel.rectb(40,177,220,15,7)
                    if self.in_boss:
                        self.umplus10.draw_text(5,180,"逃げてはいけないような気がする".center(28,"　"))
                    else:
                        self.umplus10.draw_text(5,180,"しかし、逃げられなかった".center(28,"　"))
                    self.escape_count += 1
                else:
                    self.escape_count = 0
                    self.escape = False
        else:
            if self.win == "enemy":
                pyxel.rect(99,88,95,45,0)
                pyxel.rectb(99,88,95,45,7)
                self.umplus10.draw_text(122,89,"YOU LOSE",7)
                self.umplus10.draw_text(124,100,"CONTINUE",7)
                self.umplus10.draw_text(115,111,"セーブのロード",7)
                pyxel.blt(100,100 + self.finger_pos1,self.finger_ad[0],self.finger_ad[1],self.finger_ad[2],self.finger_ad[3],self.finger_ad[4],self.finger_ad[5])
                if self.select_num1 == 1:
                    pyxel.cls(0)
                    self.app.save_load.draw()
            else:
                pyxel.rect(5, 5,self.init_x - 10,self.init_y - 10,0)
                pyxel.rectb(5, 5,self.init_x - 10,self.init_y - 10,7)
                self.umplus10.draw_text(9,6,"YOU WIN".center(30,"　"),7)
                if not self.win_show:
                    self.umplus10.draw_text(6,43,"ＨＰ".rjust(5,"　"),7)
                    self.umplus10.draw_text(6,54,"ＭＰ".rjust(5,"　"),7)
                    self.umplus10.draw_text(6,65,"ＡＴＫ".rjust(5,"　"),7)
                    self.umplus10.draw_text(6,76,"ＤＥＦ".rjust(5,"　"),7)
                    self.umplus10.draw_text(6,87,"会心率".rjust(5,"　"),7)
                    self.umplus10.draw_text(6,98,"会心ダメ".rjust(5,"　"),7)
                    if not self.xp_get:
                        for i in self.enemy_status:
                            for j in self.xp_up:
                                self.xp_up[j][0] += i["xp"]
                                xp = 0
                                level = self.chara_data[j]["Level"] + 1
                                if 0 <= level <= 16:
                                    xp = level ** 2 + 6 * level
                                elif 17 <= level <= 30:
                                    xp = (5 / 2) * level ** 2 - (81 / 2) * level + 360
                                elif 31 <= level:
                                    xp = (9 / 2) * level ** 2 - (325 / 2) * level + 2220
                                if self.chara_data[j]["XP"] + self.xp_up[j][0] >= xp:
                                    self.xp_up[j][1] = True
                        print(f"get xp:{self.xp_up}")
                    for i,k in enumerate(self.chara_data.keys()):
                        be_level_ten = 0
                        no_level_ten = 0
                        if not self.xp_get:
                            self.xp_up[k][2] = self.chara_data[k]["Level"]
                        chara = self.chara_data[k]
                        self.umplus10.draw_text(58 + 61 * i,43,str(chara["HP"][0]).rjust(4,' '),7)
                        self.umplus10.draw_text(58 + 61 * i,54,str(chara["MP"][0]).rjust(4,' '),7)
                        self.umplus10.draw_text(58 + 61 * i,65,str(chara["atk_ab"]).rjust(4,' '),7)
                        self.umplus10.draw_text(58 + 61 * i,76,str(chara["def_ab"]).rjust(4,' '),7)
                        self.umplus10.draw_text(58 + 61 * i,87,str(chara["satisfaction"][0]).rjust(4,' '),7)
                        self.umplus10.draw_text(58 + 61 * i,98,str(chara["satisfaction"][1]).rjust(4,' '),7)
                        self.umplus10.draw_text(62 * i + 51,17,str(k).center(5,"　"),7)
                        xp = 0
                        level = self.chara_data[k]["Level"] + 1
                        if 0 <= level <= 16:
                            xp = level ** 2 + 6 * level
                        elif 17 <= level <= 30:
                            xp = (5 / 2) * level ** 2 - (81 / 2) * level + 360
                        elif 31 <= level:
                            xp = (9 / 2) * level ** 2 - (325 / 2) * level + 2220
                        if self.chara_data[k]["XP"] >= xp:
                            self.chara_data[k]["Level"] += 1
                            self.chara_data[k]["XP"] -= xp
                            if len(str(self.xp_up[k][2])) > 1:
                                be_level_ten = int(str(self.xp_up[k][2])[-2])
                            if len(str(self.chara_data[k]["Level"])) > 1:
                                no_level_ten = int(str(self.chara_data[k]["Level"])[-2])
                            if be_level_ten < no_level_ten:
                                ten_level = no_level_ten - be_level_ten
                                self.status_diff[k]["satisfaction"][0] = self.levelup_data["satisfaction"][0] * ten_level
                                self.status_diff[k]["satisfaction"][1] = self.levelup_data["satisfaction"][1] * ten_level
                            self.status_diff[k]["HP"] += self.levelup_data["HP"]
                            self.status_diff[k]["MP"] += self.levelup_data["MP"]
                            self.status_diff[k]["atk_ab"] += self.levelup_data["atk_ab"]
                            self.status_diff[k]["def_ab"] += self.levelup_data["def_ab"]
                        if self.xp_up[k][2] != None:
                            if self.status_diff[k]["satisfaction"][0] != 0:
                                self.umplus10.draw_text(84 + 61 * i,87,f"→{str(chara['satisfaction'][0] + self.status_diff[k]['satisfaction'][0]).rjust(2,' ')}",11)
                                self.umplus10.draw_text(84 + 61 * i,98,f"→{str(chara['satisfaction'][1] + self.status_diff[k]['satisfaction'][1]).rjust(2,' ')}",11)
                            self.umplus10.draw_text(84 + 61 * i,43,f"→{str(chara['HP'][0] + self.status_diff[k]['HP']).rjust(2,' ')}",11)
                            self.umplus10.draw_text(84 + 61 * i,54,f"→{str(chara['MP'][0] + self.status_diff[k]['MP']).rjust(2,' ')}",11)
                            self.umplus10.draw_text(84 + 61 * i,65,f"→{str(chara['atk_ab'] + self.status_diff[k]['atk_ab']).rjust(2,' ')}",11)
                            self.umplus10.draw_text(84 + 61 * i,76,f"→{str(chara['def_ab'] + self.status_diff[k]['def_ab']).rjust(2,' ')}",11)
                        self.umplus10.draw_text(61 * i + 56,28,"Lv ",7)
                        self.umplus10.draw_text(61 * i + 71,28,str(self.chara_data[k]['Level']),7)
                        pyxel.rect(61 * i + 56,39,int(self.chara_data[k]["XP"] / xp * 100 * 0.5),4,11)
                        pyxel.rectb(61 * i + 56,39,50,4,7)
                        if not self.xp_stop:
                            if self.xp_up[k][0] >= 15:
                                self.chara_data[k]["XP"] += 15
                                self.xp_up[k][0] -= 15
                            else:
                                self.chara_data[k]["XP"] += self.xp_up[k][0]
                                self.xp_up[k][0] = 0
                            for j in self.xp_up:
                                if self.xp_up[j][0] == 0:
                                    self.xp_stop = True
                                else:
                                    self.xp_stop = False
                    self.xp_get = True
                    money = 0
                    for i in self.enemy_status:
                        money += i["money"]
                    self.umplus10.draw_text(100,130,"お金",7)
                    self.umplus10.draw_text(130,130,f"￥{self.app.money}",7)
                    self.umplus10.draw_text(146 + len(str(self.app.money)) * 5,130,f"→￥{self.app.money + money}",11)
                    if self.get_item != []:
                        self.umplus10.draw_text(0,150,f"手に入れたアイテム".rjust(15,"　"))
                        ind = 0
                        for j,i in enumerate(self.get_item):
                            if j != 0:
                                if j / 3 == 0:
                                    ind += 1
                            item = self.app.tools["basic"][i]
                            self.umplus10.draw_text(120 + 66 * ind,150 + (j * 11),item["name"])
                    # self.umplus10.draw_text(self.init_x//2 - 60, self.init_y//2 - 5,"Player Win",7)
                elif self.add_sm_tf:
                    for i,j in enumerate(self.chara_data.keys()):
                        self.umplus10.draw_text(62 * i + 51,17,str(j).center(5,"　"),7)
                    for i,chara in enumerate(list(self.chara_data.keys())):
                        for j,sm in enumerate(list(self.add_sm.keys())):
                            max_ = max([len(self.add_sm["magic"][n]) for n in [m for m in list(self.chara_data.keys())] if n in self.add_sm["magic"].keys()])
                            if sm == "magic":
                                self.umplus10.draw_text(6,43 + 11 * j,"獲得魔法".rjust(5,"　"),7)
                            else:
                                self.umplus10.draw_text(6,43 + 11 * (j + max_ + 1),"獲得スキル".rjust(5,"　"),7)
                            if chara in self.add_sm[sm].keys():
                                for k,sm_code in enumerate(self.add_sm[sm][chara]):
                                    if sm == "magic":
                                        self.umplus10.draw_text(58 + 61 * i,43 + 11 * k,self.magic_codes[sm][sm_code]["name"].rjust(4,' '),7)
                                    else:
                                        self.umplus10.draw_text(58 + 61 * i,43 + 11 * (k + max_ + 2),self.magic_codes[sm][sm_code]["name"].rjust(4,' '),7)