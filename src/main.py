import pyxel
import configparser
import json
import time
from BDFRenderer import BDFRenderer
from question import Question
from title import Title
from save import Save
from save_load import SaveLoad
from setting import In_Setting, Out_Setting
from player import Player
from cloud_data import cloud_data

##########
is_test = True
##########

cloud = cloud_data(is_test=is_test)
local = cloud.import_()

if local:
    config = configparser.ConfigParser(interpolation=None)
    config.read("src/configs/config.ini")
else:
    config = cloud.config_load()

with open("src/assets/scenes.json",encoding="utf-8") as f:
    scenes = json.load(f)


with open("src/assets/words.json",encoding="utf-8") as f:
    words = json.load(f)

if local:
    with open("src/configs/savedata.json",encoding="utf-8") as f:
        save_data = json.load(f)
else:
    save_data = cloud.load()


#セーブ機能
#フラグの数とシーンのデータ、プレイ時間、仲間などのHP,MP、レベル情報などをjsonで保存


#呼び出す自作関数の中にあるファイル読み込みは自作関数があるディレクトリからカウントされる
#その他は、基本的にはファイルの実行ディレクトリからカウントされる


def dec_word(msg_dis:int,msg_num:int,question,is_question:bool) -> tuple[int, int]:
    """文字を表示するデコレーション

    Parameters:
    ----------
    msg_dis : int
        表示する文字列のDictionaryのKey
    msg_num : int
        sのインデックス番号
    Returns:
    ----------
    msg_dis : int
        表示する文字列のDictionaryのKey
    msg_num : int
        sのインデックス番号
    """

    s = words["words"][str(msg_dis)]
    #テキスト出力の囲いの描画
    pyxel.rect(5,init_y-60,init_x-10,55,0)
    pyxel.rectb(5,init_y-60,init_x-10,55,7)
    pyxel.tri(init_x/2-5,init_y-12,init_x/2+5,init_y-12,init_x/2,init_y-8,7)
    # 13文字以内 2行以内
    if "question" in str(s[msg_num]):
        is_question = True
        umplus10.draw_text(6,init_y-55,str(s[msg_num]).replace("question",""),7)
        question.dec_question(msg_dis)
    else:
        umplus10.draw_text(6,init_y-55,s[msg_num],7)
    if (not is_question and pyxel.btnp(pyxel.KEY_SPACE) or  pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B)) or (is_question and pyxel.btnp(pyxel.KEY_RETURN) or  pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B)):
        is_question = False
        print(f"{len(words['words'])} {len(s)} {msg_num} {msg_dis}")
        if msg_num + 1 < len(s):
            msg_num += 1
        else:
            if len(words["words"]) - 1 == msg_dis + 1:
                msg_dis = -1
            elif len(words["words"]) - 1 > msg_dis + 1:
                msg_dis += 1
            msg_num = 0
        print(f"{len(words['words'])} {len(s)} {msg_num} {msg_dis}")

    return msg_dis, msg_num, is_question

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
pyxel.init(init_x,init_y,name,fps=FPS)
#文字コードの読み込み
umplus10 = BDFRenderer("assets/umplus_j10r.bdf")

TITLE_SCENE = scenes["TITLE_SCENE"]
MAIN_SCENE = scenes["MAIN_SCENE"]
IN_SETTING_SCENE = scenes["IN_SETTING_SCENE"]
OUT_SETTING_SCENE = scenes["OUT_SETTING_SCENE"]
LOAD_SCENE = scenes["LOAD_SCENE"]
BATTLE_SCENE = scenes["BATTLE_SCENE"]

que_height = 0

class App:
    def __init__(self,x,y):
        self.init_x = x
        self.init_y = y
        self.local = local
        self.now_scene = 0
        self.msg_dis = 0
        self.msg_num = 0
        self.be_scene = 0
        self.is_question = False
        self.is_word = False
        self.new_game = True
        self.from_load = False
        self.savedata = None
        self.question = Question(self.init_x,self.init_y,umplus10)
        self.player = Player(self.init_x,self.init_y,self.question)
        self.title_s = Title(self,self.init_x,self.init_y)
        self.save = Save()
        self.save_load = SaveLoad(self.init_x,self.init_y,umplus10,False,left=False,load=True,app=self)
        self.setting_in = In_Setting(self,self.init_x,self.init_y,umplus10)
        self.setting_out = Out_Setting(self,self.init_x,self.init_y,umplus10)
        if self.local:
            self.volume = int(config.get("basic","volume"))
        else:
            self.volume = int(config["basic"]["volume"])
        self.game_time = "00:00:00"
        self.game_time_start = None
        pyxel.load("assets/player.pyxres")
        pyxel.run(self.update, self.draw)

    def update(self):
        if self.now_scene == TITLE_SCENE or self.now_scene == None:
            self.now_scene = self.title_s.update()
        elif self.now_scene == MAIN_SCENE:
            #savedata.jsonを初期化しないように変更すること
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
                    self.game_time = self.savedata[str(self.save_load.setting_finger)]["play_data"]["time"]
                    self.player.x = self.savedata[str(self.save_load.setting_finger)]["play_data"]["x"]
                    self.player.y = self.savedata[str(self.save_load.setting_finger)]["play_data"]["y"]
                    self.from_load = False
                else:
                    # with open("../assets/savedata.json","w",encoding="utf-8") as f:
                    #     json.dump({},f,indent=4)
                    print("new game")
                self.new_game = False
            self.player.update(self.is_question,self.is_word)
        elif self.now_scene == OUT_SETTING_SCENE:
            self.now_scene = self.setting_out.update()
        elif self.now_scene == IN_SETTING_SCENE:
            self.setting_in.update()
        elif self.now_scene == LOAD_SCENE:
            self.now_scene = self.save_load.update()
            if self.save_load.continue_game:
                self.from_load = True
        if self.is_question:
            self.question.update()
        if pyxel.btnp(pyxel.KEY_TAB) or  pyxel.btnp(pyxel.GAMEPAD1_BUTTON_X) and (self.now_scene == MAIN_SCENE or self.now_scene == IN_SETTING_SCENE):
            if self.now_scene == IN_SETTING_SCENE:
                self.now_scene = self.be_scene
            else:
                self.be_scene = self.now_scene
                self.now_scene = IN_SETTING_SCENE
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self):
        if self.now_scene == TITLE_SCENE or self.now_scene == None:
            self.title_s.draw()
        elif self.now_scene == MAIN_SCENE:
            pyxel.cls(0)
            pyxel.bltm(0,0,0,0,0,300,200,0)
            if (self.msg_dis == 0 and self.player.x < 175) or (self.msg_dis == 1 and self.player.x >= 175):
                self.is_word = True
            else:
                self.is_word = False
            self.player.draw()
            if self.is_word:
                self.msg_dis,self.msg_num,self.is_question = dec_word(self.msg_dis,self.msg_num,self.question,self.is_question)
            if self.is_question:
                self.question.draw()
        elif self.now_scene == OUT_SETTING_SCENE:
            self.setting_out.draw()
        elif self.now_scene == IN_SETTING_SCENE:
            self.setting_in.draw()
        elif self.now_scene == LOAD_SCENE:
            self.save_load.draw()

App(init_x,init_y)