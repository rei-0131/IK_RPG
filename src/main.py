import pyxel
import configparser
import json
from BDFRenderer import BDFRenderer

config = configparser.ConfigParser(interpolation=None)
config.read("configs/config.ini")

with open("configs/scenes.json",encoding="utf-8") as f:
    scenes = json.loads(f.read())


def dec(s_1,s_2):
    """文字を表示するデコレーション

    Parameters:
    ----------
    x : Any
        1行目に表示する文字列
    y : Any
        2行目に表示する文字列
    """

    pyxel.rect(5,10,init_x-10,30,0)
    pyxel.rectb(5,10,init_x-10,30,7)
    # 13文字以内 2行以内
    umplus10.draw_text(5,15,s_1,7)
    umplus10.draw_text(5,25,s_2,7)


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
        if not (pyxel.btn(pyxel.KEY_SPACE) or pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_LEFT)) and not self.is_jump:
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
            dec("こんにちは 初めまして XX","AIUEO aiueo あいうえお")
            pyxel.line(10,init_y-100,init_x-10,init_y-100,7)
            self.player.draw()


App()