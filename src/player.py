import pyxel

class Player:
    def __init__(self,x,y,question):
        self.x = 20
        self.y = y-100
        self.init_x = x
        self.init_y = y
        self.rl = 1
        self.walk_img = 0
        self.walk_num = 0
        self.question_mark = 0
        self.question = question
        self.is_word = False
        self.walk_pos = [0,0,16,16]

    def update(self,is_question,is_word):
        if not is_question and not is_word:
            if pyxel.btn(pyxel.KEY_RIGHT) or  pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
                self.x += 1
                self.rl = 1
            if pyxel.btn(pyxel.KEY_LEFT) or  pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
                self.x -= 1
                self.rl = -1
            if pyxel.btn(pyxel.KEY_UP) or  pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
                self.y -= 1
            if pyxel.btn(pyxel.KEY_DOWN) or  pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
                self.y += 1
            if not (pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT) or pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT) or pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP) or pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN)):
                self.walk_img = 0
                self.walk_num = 0
            elif (pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT) or pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT) or pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP) or pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN)):
                self.walk_img = 2
                if self.walk_num == 3:
                    self.walk_num = 0
                else:
                    self.walk_num += 1

    def draw(self):
        pyxel.blt(self.x,self.y - 15,self.walk_img,self.walk_pos[self.walk_num],0, 14 * self.rl,15,0)
