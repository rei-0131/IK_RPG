import pyxel
import configparser
import json
from BDFRenderer import BDFRenderer

config = configparser.ConfigParser(interpolation=None)
config.read("configs/config.ini")

with open("configs/scenes.json",encoding="utf-8") as f:
    scenes = json.load(f)


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
    質問は1度に4つまで

    Parameters:
    ----------
    msg_dis : int
        表示する文字列のDictionaryのKey
    """

    s = words["questions"][str(msg_dis)]
    que_height = len(s) * 9
    pyxel.rect(init_x-50,init_y-60-que_height,45,que_height+1,0)
    pyxel.rectb(init_x-50,init_y-60-que_height,45,que_height+1,7)
    for i,h in zip(s,range(0,len(s)*9,9)):
        umplus10.draw_text(init_x-48,init_y-97+h+(36-que_height),i,7)


def dec_word(msg_dis:int,msg_num:int) -> tuple[int, int]:
    global is_question
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
        dec_question(msg_dis)
    else:
        umplus10.draw_text(6,init_y-55,s[msg_num],7)
    if (not is_question and pyxel.btnp(pyxel.KEY_N)) or (is_question and pyxel.btnp(pyxel.KEY_RETURN)):
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

is_question = False
is_answer = False

que_height = 0


class Player:
    def __init__(self):
        self.x = 20
        self.y = init_y-100
        self.rl = 1
        self.vy = 0
        self.gravity = 0.98
        self.walk_img = 0
        self.walk_num = 0
        self.question_mark = 0
        self.is_jump = False
        self.walk_pos = [0,0,16,16]

    def update(self):
        global is_question, is_answer
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        if not is_question:
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
        else:
            if pyxel.btnp(pyxel.KEY_DOWN):
                if self.question_mark != -27:
                    self.question_mark -= 9
            if pyxel.btnp(pyxel.KEY_UP):
                if self.question_mark != 0:
                    self.question_mark += 9
            if pyxel.btnp(pyxel.KEY_RETURN):
                print(self.question_mark/9)
                is_answer = True
        if self.is_jump:
            self.vy += self.gravity
            self.y += self.vy
            if self.y > init_y - 100:
                self.y = init_y - 100
                self.is_jump = False

    def draw(self):
        if is_question:
            pyxel.blt(init_x-67,init_y-96-self.question_mark,self.walk_img,15,0, 30,15,0)
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
            if self.msg_dis == 0 and self.player.x < 175:
                self.msg_dis,self.msg_num = dec_word(self.msg_dis,self.msg_num)
            elif self.msg_dis == 1 and self.player.x >= 175:
                self.msg_dis,self.msg_num = dec_word(self.msg_dis,self.msg_num)
            pyxel.line(10,init_y-100,init_x-10,init_y-100,7)
            self.player.draw()


App()