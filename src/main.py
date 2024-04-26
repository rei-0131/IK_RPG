import pyxel
import configparser
import json
from BDFRenderer import BDFRenderer

config = configparser.ConfigParser(interpolation=None)
config.read("configs/config.ini")

with open("configs/scenes.json",encoding="utf-8") as f:
    scenes = json.loads(f.read())


with open("assets/words.json",encoding="utf-8") as f:
    words = json.load(f)


#セーブ機能
#フラグの数とシーンのデータ、プレイ時間、仲間などのHP,MP、レベル情報などをjsonで保存
#プレイ時にファイルの存在の確認
#複数のセーブデータの保存を可能に
#特定キーが押された際、セーブできるウィンドウや仲間のステータスや装備の表示
#改行ができるようにする \n を検知して改行する(2行まで)


#呼び出す自作関数の中にあるファイル読み込みは自作関数があるディレクトリからカウントされる
#その他は、基本的にはファイルの実行ディレクトリからカウントされる


def dec_question(msg_dis:int):
    """質問を表示するデコレーション

    Parameters:
    ----------
    msg_dis : int
        表示する文字列のDictionaryのKey
    """

    s = words["questions"][str(msg_dis)]
    pass


def dec_word(msg_dis:int,msg_num:int) -> tuple[int, int]:
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
    pyxel.rect(5,init_y-60,init_x-10,init_y-10,0)
    pyxel.rectb(5,init_y-60,init_x-10,init_y-10,7)
    pyxel.tri(init_x/2-5,init_y-12,init_x/2+5,init_y-12,init_x/2,init_y-8,7)
    # 13文字以内 2行以内
    umplus10.draw_text(5,init_y-55,s[msg_num],7)
    #質問w投げかけたときの処理
    if "question" in s[msg_num]:
        pass
    if pyxel.btnp(pyxel.KEY_N):
        print(f"{len(words)} {len(s)} {msg_num} {msg_dis}")
        if msg_num + 1 < len(s):
            msg_num += 1
        else:
            if len(words) - 1 == msg_dis + 1:
                msg_dis = -1
            elif len(words) - 1 > msg_dis + 1:
                msg_dis += 1
            msg_num = 0
        print(f"{len(words)} {len(s)} {msg_num} {msg_dis}")

    return msg_dis, msg_num


init_x = int(config.get("args","screen_x"))
init_y = int(config.get("args","screen_y"))
FPS = int(config.get("args","fps"))
#BDFRendererのインスタンス作成より前にinitしないとエラーが発生する
pyxel.init(init_x,init_y,"test",fps=FPS)
#文字コードの読み込み
umplus10 = BDFRenderer("../assets/umplus_j10r.bdf")

TITLE_SCENE = scenes["TITLE_SCENE"]
MAIN_SCENE = scenes["MAIN_SCENE"]


class Player:
    def __init__(self):
        self.x = 20
        self.y = init_y-100
        self.rl = 1
        self.vy = 0
        self.gravity = 0.98
        self.walk_img = 0
        self.walk_num = 0
        self.is_jump = False
        self.walk_pos = [0,0,16,16]

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        if pyxel.btn(pyxel.KEY_SPACE):
            if not self.is_jump:
                self.is_jump = True
                self.vy -= 10
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += 1
            self.rl = 1
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= 1
            self.rl = -1
        if not (pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_LEFT)) and not self.is_jump:
            self.walk_img = 0
            self.walk_num = 0
        elif (pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_LEFT)) and not self.is_jump:
            self.walk_img = 2
            if self.walk_num == 3:
                self.walk_num = 0
            else:
                self.walk_num += 1
        if self.is_jump:
            self.vy += self.gravity
            self.y += self.vy
            if self.y > init_y - 100:
                self.y = init_y - 100
                self.is_jump = False

    def draw(self):
        if self.is_jump:
            pyxel.blt(self.x,self.y - 15,1,0,0,15 * self.rl,15,0)
        else:
            pyxel.blt(self.x,self.y - 15,self.walk_img,self.walk_pos[self.walk_num],0, 14 * self.rl,15,0)


class App:
    def __init__(self):
        self.player = Player()
        #実行場所基準ではなくpyファイルの場所基準
        self.now_scene = 0
        self.msg_dis = 0
        self.msg_num = 0
        from title import Title
        self.title_s = Title()
        pyxel.load("../assets/player.pyxres")
        pyxel.run(self.update, self.draw)

    def update(self):
        if self.now_scene == TITLE_SCENE:
            self.now_scene = self.title_s.update()
        elif self.now_scene == MAIN_SCENE:
            self.player.update()

    def draw(self):
        if self.now_scene == TITLE_SCENE:
            self.title_s.draw()
        elif self.now_scene == MAIN_SCENE:
            pyxel.cls(0)
            if self.msg_dis == 0 and self.player.x < 350:
                self.msg_dis,self.msg_num = dec_word(self.msg_dis,self.msg_num)
            elif self.msg_dis == 1 and self.player.x >= 350:
                self.msg_dis,self.msg_num = dec_word(self.msg_dis,self.msg_num)
            pyxel.line(10,init_y-100,init_x-10,init_y-100,7)
            self.player.draw()


App()