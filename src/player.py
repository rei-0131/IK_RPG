import pyxel
from Map import Map

class Player:
    """プレイヤーに関するクラス

    Parameter:
    ----------
    x : int
        画面の大きさx
    y : int
        画面の大きさy
    question : Any
        Questionクラスのインスタンス
    """
    def __init__(self,app,x,y,question):
        self.app = app
        self.x = 20
        self.y = y-100
        self.dx = 0
        self.dy = 0
        self.init_x = x
        self.init_y = y
        self.rl = 1
        #self.walk_speed = 1.1
        self.walk_speed = 1
        self.walk_img = 0
        self.walk_num = 0
        self.question_mark = 0
        self.question = question
        self.is_word = False
        self.map = Map()
        self.walk_pos = [0,0,0,0,0,16,16,16,16,16]

    def update(self,is_question,is_word):
        self.dx = 0
        self.dy = 0
        key = ""
        if not is_question and not is_word:
            if (pyxel.btn(pyxel.KEY_RIGHT) and not pyxel.btn(pyxel.KEY_UP) and not pyxel.btn(pyxel.KEY_DOWN)) or (pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT) and not pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP) and not pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN)):
                if self.x < 286:
                    self.dx += self.walk_speed
                self.rl = 1
                key = "d"
            if (pyxel.btn(pyxel.KEY_LEFT) and not pyxel.btn(pyxel.KEY_UP) and not pyxel.btn(pyxel.KEY_DOWN)) or (pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT) and not pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP) and not pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN)):
                if self.x > 0:
                    self.dx -= self.walk_speed
                self.rl = -1
                key = "a"
            if (pyxel.btn(pyxel.KEY_UP) and not pyxel.btn(pyxel.KEY_LEFT) and not pyxel.btn(pyxel.KEY_RIGHT)) or (pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP) and not pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT) and not pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT)):
                if self.y > 0:
                    self.dy -= self.walk_speed
                key = "w"
            if (pyxel.btn(pyxel.KEY_DOWN) and not pyxel.btn(pyxel.KEY_LEFT) and not pyxel.btn(pyxel.KEY_RIGHT)) or (pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN) and not pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT) and not pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT)):
                if self.y < 184:
                    self.dy += self.walk_speed
                key = "s"
            if not (pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT) or pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT) or pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP) or pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN)):
                self.walk_img = 0
                self.walk_num = 0
            elif (pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT) or pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT) or pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP) or pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN)):
                self.walk_img = 2
                if self.walk_num == 9:
                    self.walk_num = 0
                else:
                    self.walk_num += 1
        if not self.map.cd_check(self.x,self.y,self.dx,self.dy,self.app.now_map,key):
            self.x += self.dx
            self.y += self.dy

    def draw(self):
        pyxel.blt(self.x,self.y,self.walk_img,self.walk_pos[self.walk_num],0, 14 * self.rl,15,0)
        self.map.cd_debug()