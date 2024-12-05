import pyxel
import configparser
import json
import time
import datetime as dt
from zoneinfo import ZoneInfo
import sklearn
import joblib
import numpy as np
import sys

from utils.BDFRenderer import BDFRenderer
from utils.sound_manager import SoundManager
import utils.scenes as scenes
from title import Title
from save import Save
from save_load import SaveLoad
from setting import Setting
from player import Player
from cloud_data import Cloud_data
from Map import Map
from battle import Battle
from words import Words
from mob import Mob
from trader import Trader

#dev only
from rpg_cmd import CMD

##########テスト環境
is_test = True
mode = "debug"
if mode == "debug":
    msg = True
else:
    msg = False
##########

#各ファイル読み込み
cloud = Cloud_data(is_test=is_test)
local = cloud.import_()

if local:
    config = configparser.ConfigParser(interpolation=None)
    config.read("src/configs/config.ini",encoding="utf-8_sig")
    save_data = json.load(open("src/configs/savedata.json","r",encoding="utf-8"))
else:
    config = cloud.config_load()
    save_data = cloud.load()

#["アタッカー","ヒーラー","バッファー","タンク","遊び人"]
init_data = json.load(open("src/assets/init_data.json","r",encoding="utf-8"))
scenes_ = json.load(open("src/assets/scenes.json","r",encoding="utf-8"))
words = json.load(open("src/assets/words.json","r",encoding="utf-8"))
tools = json.load(open("src/assets/tools.json","r",encoding="utf-8"))
magic_codes = json.load(open("src/assets/magic.json","r",encoding="utf-8"))
enemy_info = json.load(open("src/assets/enemy_info.json","r",encoding="utf-8"))
assets_info = json.load(open("src/assets/assets_info.json","r",encoding="utf-8"))
collision_data = assets_info["cd_block"]
character_data = json.load(open("src/assets/character_data.json","r",encoding="utf-8"))
story_flag_names = json.load(open("src/assets/story_flags.json","r",encoding="utf-8"))
#セーブ機能
#フラグの数とシーンのデータ、プレイ時間、仲間などのHP,MP、レベル情報などをjsonで保存


#呼び出す自作関数の中にあるファイル読み込みは自作関数があるディレクトリからカウントされる
#その他は、基本的にはファイルの実行ディレクトリからカウントされる


#各設定の読み込み
if local:
    init_x = int(config.get("basic","screen_x"))
    init_y = int(config.get("basic","screen_y"))
    FPS = int(config.get("basic","fps"))
    name = config.get("basic","name")
else:
    init_x = int(config["basic"]["screen_x"])
    init_y = int(config["basic"]["screen_y"])
    FPS = int(config["basic"]["fps"])
    name = config["basic"]["name"]
#BDFRendererのインスタンス作成より前にinitしないとエラーが発生する
pyxel.init(init_x,init_y,title=name,fps=FPS,quit_key=pyxel.KEY_F9)
#文字コードの読み込み
umplus10 = BDFRenderer("assets/umplus_j10r.bdf")
umplus24 = BDFRenderer("assets/b24.bdf")

que_height = 0

class App:
    """
    アプリケーションに関するクラス

    Parameters
    ----------
    x : int
        画面の大きさx
    y : int
        画面の大きさy
    """
    def __init__(self,x,y):
        self.init_x = x
        self.init_y = y
        self.local = local
        self.now_scene = -1
        self.back_scene = -1
        self.msg_id = None
        self.be_scene = 0
        self.now_map = 0
        self.is_test = is_test
        self.disp_id = None
        self.in_word = False
        self.new_game = True
        self.from_load = False
        self.savedata = None
        self.loaddata = None
        self.in_battle = False
        self.load_write = False
        self.mode = mode
        self.debug_msg = msg
        self.INIT_DATA = init_data
        self.chara_data = init_data[mode]["chara_data"]
        self.item_codes = init_data[mode]["item_codes"]
        self.equip_codes = init_data[mode]["equip_codes"]
        self.imp_item_codes = init_data[mode]["imp_item_codes"]
        self.init_data = init_data[mode]
        self.config = config
        self.save_data = save_data
        self.scenes = scenes_
        self.words_j = words
        self.tools = tools
        self.magic_codes = magic_codes
        self.enemy_info = enemy_info
        self.assets_info = assets_info
        self.collision_data = collision_data
        self.character_data = character_data
        self.start_loading = False
        self.load_msg = ""
        self.game_time = "00:00:00"
        self.money = 0
        self.game_time_start = None
        self.bgm_run = True
        self.scale = 0.4
        self.player_scale = 2
        self.coord = [0] * 8
        self.story_flags_tf = {i:False for i in story_flag_names["TF"]}
        self.story_flags_co = {i:0 for i in story_flag_names["COUNT"]}
        self.now_location = scenes.CLASS1_SCENE
        self.mobs = [[] for _ in range(len(list(self.scenes["code"].keys())) - 7)]
        self.scene_show = [False for _ in range(len(list(self.scenes["code"].keys())) - 7)]
        self.story_animation = False
        self.random_encount = False
        self.trade = False
        self.question_selects = {}
        self.class_room = pyxel.Image(1200,800)
        self.class_room.load(0,0,"assets/classroom.png")
        self.way = pyxel.Image(1200,800)
        self.way.load(0,0,"assets/way.png")
        self.machine = pyxel.Image(1200,800)
        self.machine.load(0,0,"assets/machine.png")
        self.staff_room = pyxel.Image(1200,800)
        self.staff_room.load(0,0,"assets/staffroom.png")
        pyxel.load("assets/assets.pyxres")
        # pyxel.load("../nakayubi-shiei.pyxres")
        pyxel.run(self.update, self.draw)

    def info(self,msg):
        print(f"[{dt.datetime.now(ZoneInfo('Asia/Tokyo')).strftime('%Y/%m/%d %H:%M:%S')}] {msg}")

    def my_modules(self):
        """各クラスのインスタンス作成"""
        ld_st = time.time()
        self.load_msg = f"[{dt.datetime.now(ZoneInfo('Asia/Tokyo')).strftime('%Y/%m/%d %H:%M:%S')}] Load start"
        print(self.load_msg)
        self.info("Loading SoundManager...")
        self.sound_manager = SoundManager()
        self.info("Loading Map...")
        self.map = Map(self)
        self.cloud = cloud
        self.info("Loading Save...")
        self.save = Save(self)
        self.info("Loading SaveLoad...")
        self.save_load = SaveLoad(self.init_x,self.init_y,umplus10,False,left=False,load=True,app=self)
        self.info("Loading Setting...")
        self.setting_in = Setting(self,self.init_x,self.init_y,umplus10)
        self.info("Loading Player...")
        self.player = Player(self,self.init_x,self.init_y)
        self.info("Loading Title...")
        self.title_s = Title(self,self.init_x,self.init_y,umplus10)
        self.info("Loading Words...")
        self.words = Words(self,self.init_x,self.init_y,umplus10)
        self.info("Loading Battle...")
        self.battle = Battle(self,self.init_x, self.init_y,umplus10)
        self.info("Loading CMD...")
        self.cmd = CMD(self,self.init_x,self.init_y,umplus10)
        self.info("Loading Trader...")
        self.trader = Trader(self,self.init_x,self.init_y,umplus10)
        self.version_info()
        self.load_msg = "Load end"
        self.load_msg = f"[{dt.datetime.now(ZoneInfo('Asia/Tokyo')).strftime('%Y/%m/%d %H:%M:%S')}] Load end"
        print(f"Load Time:{time.time() - ld_st}s")
        print(self.load_msg)

    def version_info(self):
        print("----------Module Versions----------")
        print(f"python version:{sys.version}")
        if not local:
            import pyodide # type: ignore
            print(f"pyodide version:{pyodide.__version__}")
        print(f"numpy version:{np.__version__}")
        print(f"scikit-learn version:{sklearn.__version__}")
        print(f"joblib version:{joblib.__version__}")
        print("-----------------------------------")

    def load_bgms(self):
        """BGMのロード"""
        self.sound_manager.load_bgm("q_c","test")

    def check_level(self):
        def xp_ck(cr) -> float:
            xp = 0
            level = self.chara_data[cr]["Level"] + 1
            if 0 <= level <= 16:
                xp = level ** 2 + 6 * level
            elif 17 <= level <= 30:
                xp = (5 / 2) * level ** 2 - (81 / 2) * level + 360
            elif 31 <= self.chara_data[cr]["Level"]:
                xp = (9 / 2) * level ** 2 - (325 / 2) * level + 2220
            return xp
        for i in self.chara_data.keys():
            try:
                while self.chara_data[i]["XP"] >= xp_ck(i):
                    xp_ = xp_ck(i)
                    self.chara_data[i]["XP"] -= xp_
                    self.chara_data[i]["Level"] += 1
                    # print(f"{self.chara_data[i]['Level']} {self.chara_data[i]['XP']} {xp_ck(i)}")
            except Exception:
                print("Check XP Error")

    def update(self):
        """基本処理"""
        #10秒に一回の検知
        if pyxel.frame_count % 300 == 0:
            self.check_level()
        if self.now_scene == scenes.TITLE_SCENE or self.now_scene == None:
            self.now_scene = self.title_s.update()
        elif self.now_scene == scenes.MAIN_SCENE:
            if self.new_game:
                if self.from_load:
                    if self.local:
                        self.savedata = json.load(open("configs/savedata.json","r",encoding="utf-8"))
                    else:
                        self.savedata = cloud.load()
                        time.sleep(0.3)
                    self.game_time_start = time.time()
                    print(f"{self.save_load.setting_finger=}")
                    self.loaddata = self.savedata[str(self.save_load.setting_finger)]
                    self.game_time = self.savedata[str(self.save_load.setting_finger)]["play_data"]["time"]
                    self.money = self.savedata[str(self.save_load.setting_finger)]["play_data"]["money"]
                    self.now_scene = self.savedata[str(self.save_load.setting_finger)]["play_data"]["scene"]
                    self.now_location = self.savedata[str(self.save_load.setting_finger)]["play_data"]["location"]
                    self.player.x = self.savedata[str(self.save_load.setting_finger)]["play_data"]["x"]
                    self.player.y = self.savedata[str(self.save_load.setting_finger)]["play_data"]["y"]
                    self.chara_data = self.savedata[str(self.save_load.setting_finger)]["play_data"]["chara_data"]
                    self.item_codes = self.savedata[str(self.save_load.setting_finger)]["play_data"]["item_codes"]
                    self.imp_item_codes = self.savedata[str(self.save_load.setting_finger)]["play_data"]["imp_item_codes"]
                    self.equip_codes = self.savedata[str(self.save_load.setting_finger)]["play_data"]["equip_codes"]
                    self.msg_id = self.savedata[str(self.save_load.setting_finger)]["play_data"]["words"]["msg_id"]
                    self.disp_id = self.savedata[str(self.save_load.setting_finger)]["play_data"]["words"]["disp_id"]
                    self.story_flags_tf = {k:bool(v) for k,v in self.savedata[str(self.save_load.setting_finger)]["play_data"]["story_flags_tf"].items()}
                    self.story_flags_co = {k:bool(v) for k,v in self.savedata[str(self.save_load.setting_finger)]["play_data"]["story_flags_co"].items()}
                    self.question_selects = self.savedata[str(self.save_load.setting_finger)]["play_data"]["question_selects"]
                    self.from_load = False
                else:
                    print("new game")
                    self.loaddata = {
                        "play_data": {
                        "time": "00:00:00",
                        "money": 1000,
                        "words":{
                            "msg_id":"01",
                            "disp_id":None
                        },
                        "scene": 1,
                        "location": 6,
                        "x": -100,
                        "y": -100,
                        "chara_data":self.chara_data,
                        "item_codes":self.item_codes,
                        "imp_item_codes":self.imp_item_codes,
                        "equip_codes":self.equip_codes,
                        "story_flags_tf":self.story_flags_tf,
                        "story_flags_co":self.story_flags_co,
                        "question_selects":self.question_selects
                        }
                    }
                    self.game_time = self.loaddata["play_data"]["time"]
                    self.money = self.loaddata["play_data"]["money"]
                    self.player.x = self.loaddata["play_data"]["x"]
                    self.player.y = self.loaddata["play_data"]["y"]
                    self.msg_id = self.loaddata["play_data"]["words"]["msg_id"]
                    self.disp_id = self.loaddata["play_data"]["words"]["disp_id"]
                    self.now_location = self.loaddata["play_data"]["location"]
                self.new_game = False
            if not self.scene_show[self.now_location - 6]:
                for k,v in self.assets_info["chara"].items():
                    for j,i in enumerate(v[4]):
                        if i[0] == self.now_location:
                            self.mobs[self.now_location - 6].append([Mob(self,self.assets_info["chara"][k][i[1][2]],i,self.player_scale,k,j),k,i])
                self.scene_show[self.now_location - 6] = True
                for mob in self.mobs[self.now_location - 6]:
                    mob[0].update()
            else:
                for mob in self.mobs[self.now_location - 6]:
                    mob[0].update()
            self.player.update()
            if not self.new_game:
                if self.in_word:
                    self.words.update()
                    if self.msg_id == "49":
                        self.story_flags_tf["ryoga_group"] = True

                if 270 <= self.player.x and 80 <= self.player.y <= 140:
                    if self.now_location == scenes.CLASS1_SCENE or self.now_location == scenes.CLASS2_SCENE:
                        if self.msg_id == "200" and self.now_location == scenes.CLASS1_SCENE:
                            self.msg_id = "201"
                            self.player.x = 268
                            self.player.key = "a"
                            self.player.walk_pos = 0
                            self.player.walk_num = 0
                        else:
                            if self.now_location == scenes.CLASS1_SCENE:
                                if self.disp_id == "36":
                                    self.msg_id = "37"
                                self.player.x = 20
                                self.player.y = 166
                            elif self.now_location == scenes.CLASS2_SCENE:
                                self.player.x = 265
                                self.player.y = 166
                            self.now_location = scenes.WAY_SCENE_12
                    elif self.now_location == scenes.CLASS3_SCENE:
                        self.player.x = 20
                        self.player.y = 166
                        self.now_location = scenes.WAY_SCENE_31
                if 12 <= self.player.x <= 55 and 171 <= self.player.y:
                    if self.now_location == scenes.WAY_SCENE_12:
                        self.now_location = scenes.CLASS1_SCENE
                        self.player.x = 265
                        self.player.y = 105
                    elif self.now_location == scenes.WAY_SCENE_31:
                        self.now_location = scenes.CLASS3_SCENE
                        self.player.x = 265
                        self.player.y = 105
                    elif self.now_location == scenes.WAY_SCENE_I:
                        self.now_location = scenes.STAFF_I_SCENE
                        self.player.x = 141
                        self.player.y = 155
                        if self.msg_id == "212":
                            self.msg_id = "213"
                        elif self.msg_id == "267":
                            self.msg_id = "268"
                    elif self.now_location == scenes.WAY_SCENE_E:
                        self.now_location = scenes.STAFF_E_SCENE
                        self.player.x = 141
                        self.player.y = 155
                        if self.msg_id == "141":
                            self.player.key = "w"
                            self.player.walk_pos = 0
                            self.player.walk_num = 0
                            self.msg_id = "142"
                if 250 <= self.player.x <= 278 and 171 <= self.player.y:
                    if self.now_location == scenes.WAY_SCENE_12:
                        self.now_location = scenes.CLASS2_SCENE
                        self.player.x = 265
                        self.player.y = 105
                        if 36 <= int(self.disp_id) < 52:
                            if self.story_flags_tf["ryoga_group"]:
                                self.msg_id = "52"
                            else:
                                self.msg_id = "71"
                            self.player.key = "a"
                            self.player.walk_pos = 0
                            self.player.walk_num = 0
                    elif self.now_location == scenes.WAY_SCENE_31:
                        self.now_location = scenes.WAY_SCENE_I
                        self.player.x = 272
                        self.player.y = 135
                    elif self.now_location == scenes.WAY_SCENE_I:
                        self.now_location = scenes.WAY_SCENE_E
                        self.player.x = 262
                        self.player.y = 138
                    elif self.now_location == scenes.WAY_SCENE_E:
                        self.now_location = scenes.WAY_SCENE_I
                        self.player.x = 262
                        self.player.y = 138
                if 275 <= self.player.x and 115 <= self.player.y <= 150:
                    if self.now_location == scenes.WAY_SCENE_12:
                        self.now_location = scenes.WAY_SCENE_31
                        self.player.x = 15
                        self.player.y = 135
                    elif self.now_location == scenes.WAY_SCENE_31:
                        self.now_location = scenes.MACHINE_SCENE
                        if self.disp_id == "115":
                            self.msg_id = "116"
                        self.player.x = 158
                        self.player.y = 155
                    elif self.now_location == scenes.WAY_SCENE_I:
                        self.now_location = scenes.WAY_SCENE_31
                        self.player.x = 262
                        self.player.y = 165
                if self.player.x <= 7 and 115 <= self.player.y <= 150:
                    if self.now_location == scenes.WAY_SCENE_31:
                        self.now_location = scenes.WAY_SCENE_12
                        self.player.x = 272
                        self.player.y = 135
                if 41 <= self.player.x <= 63 and 43 <= self.player.y <= 45 and self.now_location == scenes.MACHINE_SCENE:
                    self.now_location = scenes.STAFF_M_SCENE
                    self.player.x = 141
                    self.player.y = 155
                if 150 <= self.player.x <= 160 and 165 <= self.player.y <= 170 and self.now_location == scenes.MACHINE_SCENE:
                    self.now_location = scenes.WAY_SCENE_31
                    self.player.x = 272
                    self.player.y = 135
                if 133 <= self.player.x <= 151 and 166 <= self.player.y <= 169:
                    if self.now_location == scenes.STAFF_I_SCENE:
                        self.now_location = scenes.WAY_SCENE_I
                        self.player.x = 20
                        self.player.y = 146
                        if (self.msg_id == "152" or self.msg_id == "9000") and 3 <= self.story_flags_co["staff_it_search"]:
                            self.msg_id = "153"
                    elif self.now_location == scenes.STAFF_M_SCENE:
                        self.now_location = scenes.MACHINE_SCENE
                        self.player.x = 50
                        self.player.y = 48
                    elif self.now_location == scenes.STAFF_E_SCENE:
                        self.now_location = scenes.WAY_SCENE_E
                        self.player.x = 20
                        self.player.y = 146

                if self.msg_id == "21":
                    self.now_location = scenes.WAY_SCENE_12
                elif self.msg_id == "35":
                    self.player.x = 20
                    self.player.y = 166
                    self.player.key = "w"
                elif self.msg_id == "118":
                    self.player.x = 160
                    self.player.y = 120
                    self.player.key = "d"
                elif self.msg_id == "136":
                    self.player.key = "s"
                elif self.msg_id == "143":
                    self.player.x = 180
                    self.player.y = 110
                    self.player.key = "w"
                elif self.msg_id == "154":
                    self.player.x = 22
                    self.player.y = 100
                    self.player.key = "d"
                elif self.msg_id == "200":
                    if not self.story_flags_tf["200_speak"]:
                        self.story_flags_tf["200_speak"] = True
                elif self.msg_id == "170":
                    if "006" in self.imp_item_codes:
                        tmp = self.imp_item_codes.index("006")
                        self.imp_item_codes.pop(tmp)
                        tmp = self.imp_item_codes.index("007")
                        self.imp_item_codes.pop(tmp)
                        tmp = self.imp_item_codes.index("008")
                        self.imp_item_codes.pop(tmp)
                elif self.msg_id == "231":
                    self.player.x = 166
                    self.player.y = 110
                    self.player.key = "w"
                    self.player.walk_pos = 0
                    self.player.walk_num = 0
                    self.now_location = scenes.CLASS1_SCENE
                elif self.msg_id == "240":
                    self.player.x = 300
                    self.player.y = 0
                    self.player.walk_pos = 0
                    self.player.walk_num = 0
                elif self.msg_id == "259":
                    self.player.x = 166
                    self.player.y = 100
                    self.player.key = "a"
                    self.player.walk_pos = 0
                    self.player.walk_num = 0
                elif self.msg_id == "260" and self.now_location == scenes.WAY_SCENE_I and self.player.x <= 70 and self.player.y >= 150:
                    self.msg_id = "261"
                elif self.msg_id == "266":
                    self.player.x = 30
                    self.player.y = 120
                    self.player.key = "w"
                    self.player.walk_pos = 0
                    self.player.walk_num = 0
                elif self.msg_id == "297":
                    self.player.x = 165
                    self.player.y = 80
                    self.player.key = "a"
                    self.player.walk_pos = 0
                    self.player.walk_num = 0
                elif self.msg_id == "299":
                    self.player.x = 186
                    self.player.y = 95
                    self.player.key = "w"
                    self.player.walk_pos = 0
                    self.player.walk_num = 0
                elif self.msg_id == "316":
                    self.player.x = 300
                    self.player.y = 0
                elif self.msg_id == "324":
                    self.player.x = 186
                    self.player.y = 95
                    self.player.key = "d"
                    self.player.walk_pos = 0
                    self.player.walk_num = 0
            if self.in_battle and not self.random_encount:
                print("loading battle")
                self.battle.clean(self.now_scene)
                self.battle.save_chara(self.chara_data)
                if self.is_test:
                    self.battle.debug_clean()
                print(self.words_j["story"][self.disp_id]["battle"][0])
                self.battle.set_enemy(len(self.words_j["story"][self.disp_id]["battle"][0]),self.words_j["story"][self.disp_id]["battle"][0])
                self.be_scene = self.now_scene
                self.now_scene = scenes.BATTLE_SCENE
            if pyxel.btnp(pyxel.KEY_T) and self.is_test:
                self.trade = True
            if self.trade:
                self.trader.update()
        elif self.now_scene == scenes.IN_SETTING_SCENE:
            self.setting_in.update()
        elif self.now_scene == scenes.LOAD_SCENE:
            self.now_scene = self.save_load.update()
            if self.save_load.continue_game:
                self.from_load = True
        elif self.now_scene == scenes.START_SCENE:
            if not self.start_loading and self.load_write:
                self.start_loading = True
                self.my_modules()
                self.load_bgms()
                self.now_scene = 0
        if not self.now_scene == scenes.START_SCENE and not self.in_word:
            if (pyxel.btnp(pyxel.KEY_TAB) or  pyxel.btnp(pyxel.GAMEPAD1_BUTTON_Y)) and (self.now_scene == scenes.MAIN_SCENE or self.now_scene == scenes.IN_SETTING_SCENE):
                if self.now_scene == scenes.IN_SETTING_SCENE:
                    self.now_scene = self.be_scene
                elif self.now_scene != "cmd":
                    self.setting_in.clean()
                    self.be_scene = self.now_scene
                    self.now_scene = scenes.IN_SETTING_SCENE
        if not self.now_scene == scenes.START_SCENE:
            if pyxel.btnp(pyxel.KEY_C) and pyxel.btn(pyxel.KEY_CTRL) and self.is_test:
                if self.now_scene == "cmd":
                    self.now_scene = self.back_scene
                else:
                    self.cmd.start = True
                    self.back_scene = self.now_scene
                    self.now_scene = "cmd"
        if self.now_scene == scenes.BATTLE_SCENE:
            self.battle.update()
            if self.bgm_run and self.battle.win != "":
                self.sound_manager.stop()
                print("BGM STOP")
                self.bgm_run = False
                if self.battle.win == "player":
                    self.in_battle = False
                    if "battle" in self.words_j["story"][self.disp_id]:
                        self.msg_id = self.words_j["story"][self.disp_id]["battle"][1]
                    elif self.random_encount:
                        self.random_encount = False
        elif self.now_scene == "cmd":
            self.cmd.update()

    def draw(self):
        """基本描画"""
        if self.now_scene == scenes.TITLE_SCENE or self.now_scene == None:
            self.title_s.draw()
        elif self.now_scene == scenes.MAIN_SCENE:
            pyxel.cls(0)
            if not (self.msg_id == None or self.msg_id == "01" or self.msg_id == "15" or self.msg_id == "111" or self.msg_id == "187" or self.msg_id == "231" or self.msg_id == "240"):
                self.coord = self.scenes["coordinate"][str(self.now_location)]
                self.scale = self.coord[8]
                if self.msg_id == "15" or self.msg_id != "111" or self.msg_id != "187" or self.msg_id != "231" or self.msg_id == "240":
                    if scenes.CLASS1_SCENE <= self.now_location <= scenes.CLASS3_SCENE:
                        pyxel.blt(-150,-100,self.class_room,0,0,600,400,0,scale = 0.5)
                    elif scenes.STAFF_I_SCENE <= self.now_location <= scenes.STAFF_E_SCENE:
                        pyxel.blt(-150,-100,self.staff_room,0,0,600,400,0,scale = 0.5)
                    elif scenes.WAY_SCENE_12 <= self.now_location <= scenes.WAY_SCENE_E:
                        pyxel.blt(-150,-100,self.way,0,0,600,400,0,scale = 0.5)
                    elif self.now_location == scenes.MACHINE_SCENE:
                        pyxel.blt(-150,-100,self.machine,0,0,600,400,0,scale = 0.5)
                    else:
                        pyxel.bltm(self.coord[0],self.coord[1],self.coord[2],self.coord[3],self.coord[4],self.coord[5],self.coord[6],self.coord[7],scale = self.scale)
                    match self.now_location:
                        case scenes.CLASS1_SCENE:
                            umplus24.draw_text(260,20,"3-1",0)
                        case scenes.CLASS2_SCENE:
                            umplus24.draw_text(260,20,"3-2",0)
                        case scenes.CLASS3_SCENE:
                            umplus24.draw_text(260,20,"3-3",0)
                    if self.scene_show[self.now_location - 6]:
                        [mob[0].draw() for mob in self.mobs[self.now_location - 6] if mob[0].display[0]]
                    self.player.draw()
            match self.now_location:
                case scenes.WAY_SCENE_12:
                    pyxel.rect(12,194,43,6,0)
                    pyxel.rect(250,194,43,6,0)
                    pyxel.rect(290,120,10,43,0)
                    pyxel.text(25,188,"3-1",0)
                    pyxel.text(265,188,"3-2",0)
                case scenes.WAY_SCENE_31:
                    pyxel.rect(12,194,43,6,0)
                    pyxel.rect(250,194,43,6,0)
                    pyxel.rect(0,120,10,43,0)
                    pyxel.rect(290,120,10,43,0)
                    text = ["機","械","棟"]
                    [umplus10.draw_text(278,125 + i * 11,text[i],0) for i in range(3)]
                    pyxel.text(25,188,"3-3",0)
                    umplus10.draw_text(262,183,"1棟",0)
                case scenes.WAY_SCENE_I:
                    pyxel.rect(12,194,43,6,0)
                    pyxel.rect(250,194,43,6,0)
                    pyxel.rect(290,120,10,43,0)
                    text = ["２","棟"]
                    [umplus10.draw_text(278,130 + i * 11,text[i],0) for i in range(2)]
                    umplus10.draw_text(12,183,"IT職員室",0)
                    pyxel.text(267,188,"2F",0)
                case scenes.WAY_SCENE_E:
                    pyxel.rect(12,194,43,6,0)
                    pyxel.rect(250,194,43,6,0)
                    umplus10.draw_text(15,183,"E職員室",0)
                    pyxel.text(265,188,"1F",0)
                case scenes.MACHINE_SCENE:
                    umplus10.draw_text(180,178,"２棟",0)
                case scenes.STAFF_I_SCENE:
                    umplus24.draw_text(210,177,"I",0)
                case scenes.STAFF_M_SCENE:
                    umplus24.draw_text(210,177,"M",0)
                case scenes.STAFF_E_SCENE:
                    umplus24.draw_text(210,177,"E",0)
            if self.trade:
                self.trader.draw()
            if not self.new_game:
                if self.msg_id != self.disp_id:
                    self.in_word = True
                else:
                    self.in_word = False
                if self.in_word:
                    self.words.dec_word()
                if self.mode == "debug" and self.debug_msg:
                    pyxel.text(0,0,f"{self.player.x = }",0)
                    pyxel.text(0,11,f"{self.player.y = }",0)
                    pyxel.text(0,22,f"{self.player.dx = }",0)
                    pyxel.text(0,33,f"{self.player.dy = }",0)
                    pyxel.text(0,44,f"{self.player.key = }",0)
                    pyxel.text(0,55,f"{self.player.walk_pm = }",0)
                    pyxel.text(0,66,f"{self.player.walk_pos = }",0)
                    pyxel.text(0,77,f"{self.player.walk_num = }",0)
                    pyxel.text(0,88,f"{self.map.cd_check(self.player.x,self.player.y,self.player.dx,self.player.dy,self.now_map,self.player.key,self.scale,self.coord)}",0)
                    pyxel.text(0,121,f"{self.msg_id = } {self.disp_id = }",0)
        elif self.now_scene == scenes.IN_SETTING_SCENE:
            self.setting_in.draw()
        elif self.now_scene == scenes.LOAD_SCENE:
            self.save_load.draw()
        elif self.now_scene == scenes.START_SCENE:
            pyxel.cls(0)
            umplus24.draw_text(70,90,"Now Loading...",7)
            pyxel.text(150,190,self.load_msg,7)
            self.load_write = True
        # pyxel.blt(0,0,0,0,0,63,79,10)
        if self.now_scene == scenes.BATTLE_SCENE:
            self.battle.draw()
        elif self.now_scene == "cmd":
            self.cmd.draw()


App(init_x,init_y)