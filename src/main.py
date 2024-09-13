import pyxel
import configparser
import json
import time
from utils.BDFRenderer import BDFRenderer
from utils.sound_manager import SoundManager
from title import Title
from save import Save
from save_load import SaveLoad
from setting import In_Setting, Out_Setting
from player import Player
from cloud_data import Cloud_data
from Map import Map
from battle import Battle
from words import Words
from option import Option

#dev only
from rpg_cmd import CMD

##########テスト環境かのbool
is_test = True
##########

#各ファイル読み込み
cloud = Cloud_data(is_test=is_test)
local = cloud.import_()

if local:
    import datetime as dt
    from zoneinfo import ZoneInfo

    config = configparser.ConfigParser(interpolation=None)
    config.read("src/configs/config.ini",encoding="utf-8_sig")
    with open("src/configs/savedata.json",encoding="utf-8") as f:
        save_data = json.load(f)
else:
    config = cloud.config_load()
    save_data = cloud.load()

with open("src/assets/init_data.json",encoding="utf-8") as f:
    init_data = json.load(f)

with open("src/assets/scenes.json",encoding="utf-8") as f:
    scenes = json.load(f)

with open("src/assets/words.json",encoding="utf-8") as f:
    words = json.load(f)

with open("src/assets/tools.json","r",encoding="utf-8") as f:
    tools = json.load(f)

with open("src/assets/magic.json","r",encoding="utf-8") as f:
    magic_codes = json.load(f)

with open("src/assets/enemy_info.json",encoding="utf-8") as f:
    enemy_info = json.load(f)

with open("src/assets/cd_block.json",encoding="utf-8") as f:
    collision_data = json.load(f)

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

START_SCENE = scenes["START_SCENE"]
TITLE_SCENE = scenes["TITLE_SCENE"]
MAIN_SCENE = scenes["MAIN_SCENE"]
IN_SETTING_SCENE = scenes["IN_SETTING_SCENE"]
OUT_SETTING_SCENE = scenes["OUT_SETTING_SCENE"]
LOAD_SCENE = scenes["LOAD_SCENE"]
BATTLE_SCENE = scenes["BATTLE_SCENE"]

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
        self.msg_id = "01"
        self.be_scene = 0
        self.now_map = 0
        self.is_test = is_test
        # self.disp_id = "None"
        self.disp_id = "None"
        self.in_word = False
        self.new_game = True
        self.from_load = False
        self.savedata = None
        self.loaddata = None
        self.in_battle = False
        self.load_write = False
        self.chara_data = init_data["chara_data"]
        self.item_codes = init_data["item_codes"]
        self.equip_codes = init_data["equip_codes"]
        self.imp_item_codes = init_data["imp_item_codes"]
        self.init_data = init_data
        self.config = config
        self.save_data = save_data
        self.scenes = scenes
        self.words = words
        self.tools = tools
        self.magic_codes = magic_codes
        self.enemy_info = enemy_info
        self.collision_data = collision_data
        self.start_loading = False
        self.load_msg = ""
        self.game_time = "00:00:00"
        self.game_time_start = None
        pyxel.load("assets/player.pyxres")
        # pyxel.load("../nakayubi-shiei.pyxres")
        pyxel.run(self.update, self.draw)

    def my_modules(self):
        """各クラスのインスタンス作成"""
        ld_st = time.time()
        if local:
            self.load_msg = f"[{dt.datetime.now(ZoneInfo('Asia/Tokyo')).strftime('%Y/%m/%d %H:%M:%S')}] Load start"
        else:
            self.load_msg = "Load start"
        print(self.load_msg)
        self.sound_manager = SoundManager()
        self.map = Map(self)
        self.cloud = cloud
        self.save = Save(self)
        self.save_load = SaveLoad(self.init_x,self.init_y,umplus10,False,left=False,load=True,app=self)
        self.option = Option(self,self.init_x,self.init_y,umplus10)
        self.setting_in = In_Setting(self,self.init_x,self.init_y,umplus10)
        self.setting_out = Out_Setting(self,self.init_x,self.init_y,umplus10)
        self.player = Player(self,self.init_x,self.init_y)
        self.title_s = Title(self,self.init_x,self.init_y,umplus10)
        self.words = Words(self,self.init_x,self.init_y,umplus10)
        self.battle = Battle(self.init_x, self.init_y,umplus10,self)
        self.cmd = CMD(self,self.init_x,self.init_y,umplus10)
        self.load_msg = "Load end"
        if local:
            self.load_msg = f"[{dt.datetime.now(ZoneInfo('Asia/Tokyo')).strftime('%Y/%m/%d %H:%M:%S')}] Load end"
        print(f"Load Time:{time.time() - ld_st}s")
        print(self.load_msg)

    def load_bgms(self):
        self.sound_manager.load_bgm("qnoheya","test")
        # self.sound_manager.play_bgm("test")

    def update(self):
        """基本処理"""
        if self.now_scene == TITLE_SCENE or self.now_scene == None:
            self.now_scene = self.title_s.update()
        elif self.now_scene == MAIN_SCENE:
            if self.new_game:
                if self.from_load:
                    if self.local:
                        with open("configs/savedata.json","r",encoding="utf-8") as f:
                            self.savedata = json.load(f)
                    else:
                        self.savedata = cloud.load()
                        time.sleep(0.3)
                    self.game_time_start = time.time()
                    print(self.save_load.setting_finger)
                    self.loaddata = self.savedata[str(self.save_load.setting_finger)]
                    self.game_time = self.savedata[str(self.save_load.setting_finger)]["play_data"]["time"]
                    self.player.x = self.savedata[str(self.save_load.setting_finger)]["play_data"]["x"]
                    self.player.y = self.savedata[str(self.save_load.setting_finger)]["play_data"]["y"]
                    self.chara_data = self.savedata[str(self.save_load.setting_finger)]["play_data"]["chara_data"]
                    self.item_codes = self.savedata[str(self.save_load.setting_finger)]["play_data"]["item_codes"]
                    self.imp_item_codes = self.savedata[str(self.save_load.setting_finger)]["play_data"]["imp_item_codes"]
                    self.equip_codes = self.savedata[str(self.save_load.setting_finger)]["play_data"]["equip_codes"]
                    self.from_load = False
                else:
                    print("new game")
                    self.loaddata = {
                        "play_data": {
                        "time": "00:00:00",
                        "scene": 1,
                        "x": 20,
                        "y": 200,
                        "chara_data":self.chara_data,
                        "item_codes":self.item_codes,
                        "imp_item_codes":self.imp_item_codes,
                        "equip_codes":self.equip_codes
                        }
                    }
                    self.game_time = self.loaddata["play_data"]["time"]
                    self.player.x = self.loaddata["play_data"]["x"]
                    self.player.y = self.loaddata["play_data"]["y"]
                    self.chara_data = init_data["chara_data"]
                    self.item_codes = init_data["item_codes"]
                    self.equip_codes = init_data["equip_codes"]
                    self.imp_item_codes = init_data["imp_item_codes"]
                self.new_game = False
            self.player.update()
            if self.in_word:
                self.msg_id, self.disp_id = self.words.update()
            if self.in_battle:
                self.battle.clean(self.now_scene)
                if self.is_test:
                    self.battle.debug_clean()
                self.battle.set_enemy(words["story"][self.disp_id]["battle"][0],words["story"][self.disp_id]["battle"][1])
                self.now_scene = 5
        elif self.now_scene == OUT_SETTING_SCENE:
            self.now_scene = self.setting_out.update()
        elif self.now_scene == IN_SETTING_SCENE:
            self.setting_in.update()
        elif self.now_scene == LOAD_SCENE:
            self.now_scene = self.save_load.update()
            if self.save_load.continue_game:
                self.from_load = True
        elif self.now_scene == START_SCENE:
            if not self.start_loading and self.load_write:
                self.start_loading = True
                self.my_modules()
                self.load_bgms()
                self.now_scene = 0
        if (pyxel.btnp(pyxel.KEY_TAB) or  pyxel.btnp(pyxel.GAMEPAD1_BUTTON_Y)) and (self.now_scene == MAIN_SCENE or self.now_scene == IN_SETTING_SCENE):
            if self.now_scene == IN_SETTING_SCENE:
                self.now_scene = self.be_scene
            elif self.now_scene != "cmd":
                self.setting_in.clean()
                self.be_scene = self.now_scene
                self.now_scene = IN_SETTING_SCENE
        if (pyxel.btnp(pyxel.KEY_B) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_X)) and (self.now_scene == MAIN_SCENE or self.now_scene == 5):
            if not self.now_scene == "cmd" and self.now_scene == 5:
                self.now_scene = self.be_scene
            elif self.now_scene == "cmd" and self.back_scene == 5:
                self.now_scene = self.be_scene
                self.battle.clean(self.now_scene)
                #以下、敵のランダムな数、敵の名称を決定するコード
                # enemy_num = random.randint(1,3)
                self.battle.set_enemy(4,[{"enemy_type":"general","enemy_code":"mob1"},{"enemy_type":"general","enemy_code":"mob1"},{"enemy_type":"general","enemy_code":"mob1"},{"enemy_type":"general","enemy_code":"mob1"}])
                self.now_scene = 5
            else:
                self.be_scene = self.now_scene
                self.battle.clean(self.now_scene)
                #以下、敵のランダムな数、敵の名称を決定するコード
                # enemy_num = random.randint(1,3)
                self.battle.set_enemy(4,[{"enemy_type":"general","enemy_code":"mob1"},{"enemy_type":"general","enemy_code":"mob1"},{"enemy_type":"general","enemy_code":"mob1"},{"enemy_type":"general","enemy_code":"mob1"}])
                self.now_scene = 5
        if pyxel.btnp(pyxel.KEY_C) and pyxel.btn(pyxel.KEY_CTRL) and self.is_test:
            if self.now_scene == "cmd":
                self.now_scene = self.back_scene
            else:
                self.cmd.start = True
                self.back_scene = self.now_scene
                self.now_scene = "cmd"
        if self.now_scene == 5:
            self.battle.update()
        elif self.now_scene == "cmd":
            self.cmd.update()

    def draw(self):
        """基本描画"""
        if self.now_scene == TITLE_SCENE or self.now_scene == None:
            self.title_s.draw()
        elif self.now_scene == MAIN_SCENE:
            pyxel.cls(0)
            pyxel.camera()
            pyxel.bltm(0,0,0,0,0,self.init_x,self.init_y,0)
            self.player.draw()
            if self.msg_id != self.disp_id:
                self.in_word = True
            else:
                self.in_word = False
            if self.in_word:
                self.words.dec_word(self.msg_id)
        elif self.now_scene == OUT_SETTING_SCENE:
            self.setting_out.draw()
        elif self.now_scene == IN_SETTING_SCENE:
            self.setting_in.draw()
        elif self.now_scene == LOAD_SCENE:
            self.save_load.draw()
        elif self.now_scene == START_SCENE:
            pyxel.cls(0)
            umplus24.draw_text(70,90,"Now Loading...",7)
            pyxel.text(150,190,self.load_msg,7)
            self.load_write = True
        # pyxel.blt(0,0,0,0,0,63,79,10)
        if self.now_scene == 5:
            self.battle.draw()
        elif self.now_scene == "cmd":
            self.cmd.draw()

App(init_x,init_y)