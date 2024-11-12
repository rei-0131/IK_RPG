import pyxel

class Player:
    """プレイヤーに関するクラス

    Parameter:
    ----------
    app : Any
        Appクラスのインスタンス
    x : int
        画面の大きさx
    y : int
        画面の大きさy
    """
    def __init__(self,app,x,y):
        self.app = app
        self.x = 20
        self.y = y - 100
        self.dx = 0
        self.dy = 0
        self.init_x = x
        self.init_y = y
        self.rl = 1
        self.key = ""
        self.walk_speed = 1
        self.walk_num = 0
        self.question_mark = 0
        self.is_word = False
        self.map = self.app.map
        self.chara = self.app.assets_info["chara"]["ぼく"]
        self.walk_pos = 0
        self.walk_pm = "p"
        self.scale = self.app.player_scale

    def update(self):
        """基本処理"""
        self.dx = 0
        self.dy = 0
        if not self.app.in_word:
            if (pyxel.btn(pyxel.KEY_RIGHT) and not pyxel.btn(pyxel.KEY_UP) and not pyxel.btn(pyxel.KEY_DOWN)) or (pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT) and not pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP) and not pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN)):
                self.dx += self.walk_speed
                self.rl = 1
                self.key = "d"
            if (pyxel.btn(pyxel.KEY_LEFT) and not pyxel.btn(pyxel.KEY_UP) and not pyxel.btn(pyxel.KEY_DOWN)) or (pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT) and not pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP) and not pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN)):
                self.dx -= self.walk_speed
                self.rl = -1
                self.key = "a"
            if (pyxel.btn(pyxel.KEY_UP) and not pyxel.btn(pyxel.KEY_LEFT) and not pyxel.btn(pyxel.KEY_RIGHT)) or (pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP) and not pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT) and not pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT)):
                self.dy -= self.walk_speed
                self.key = "w"
            if (pyxel.btn(pyxel.KEY_DOWN) and not pyxel.btn(pyxel.KEY_LEFT) and not pyxel.btn(pyxel.KEY_RIGHT)) or (pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN) and not pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT) and not pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT)):
                self.dy += self.walk_speed
                self.key = "s"
            if not (pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT) or pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT) or pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP) or pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN)):
                self.walk_num = 0
                self.walk_pos = 0
            elif (pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT) or pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT) or pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP) or pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN)):
                if self.walk_num % 10 == 0:
                    if self.walk_pm == "p":
                        self.walk_pos += 1
                    else:
                        self.walk_pos -= 1
                    self.walk_num = 0
                if self.walk_pm == "p":
                    if self.walk_pos >= 2:
                        self.walk_pos -= 1
                        self.walk_pm = "m"
                else:
                    if self.walk_pos <= -2:
                        self.walk_pos += 1
                        self.walk_pm = "p"
                self.walk_num += 1
        cd_return = self.map.cd_check(self.x,self.y,self.dx,self.dy,self.app.now_map,self.key,self.app.scale,self.app.coord)
        if not cd_return[0]:
            self.x += self.dx
            self.y += self.dy
        else:
            if not self.app.in_word:
                if pyxel.btnp(pyxel.KEY_F) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
                    if cd_return[1] == "mob":
                        if self.app.mobs[self.app.now_location - 6][cd_return[2]][2][2] != -1:
                            if str(self.app.mobs[self.app.now_location - 6][cd_return[2]][2][2]) == self.app.msg_id:
                                self.app.disp_id = str(int(self.app.disp_id) - 1)
                            else:
                                self.app.msg_id = str(self.app.mobs[self.app.now_location - 6][cd_return[2]][2][2])

    def draw(self):
        """基本描画"""
        if self.key == "d":
            if self.walk_pos == -1:
                pyxel.blt(self.x,self.y,self.chara[1][0],self.chara[1][1] - (self.walk_pos + 2) * 16,self.chara[1][2],self.chara[1][3],self.chara[1][4],self.chara[1][5],scale=self.scale)
            else:
                pyxel.blt(self.x,self.y,self.chara[1][0],self.chara[1][1] - self.walk_pos * 16,self.chara[1][2],self.chara[1][3],self.chara[1][4],self.chara[1][5],scale=self.scale)
        elif self.key == "a":
            if self.walk_pos == -1:
                pyxel.blt(self.x,self.y,self.chara[1][0],self.chara[1][1] - (self.walk_pos + 2) * 16,self.chara[1][2],self.chara[1][3] * -1,self.chara[1][4],self.chara[1][5],scale=self.scale)
            else:
                pyxel.blt(self.x,self.y,self.chara[1][0],self.chara[1][1] - self.walk_pos * 16,self.chara[1][2],self.chara[1][3] * -1,self.chara[1][4],self.chara[1][5],scale=self.scale)
        elif self.key == "w":
            if self.walk_pos == -1:
                pyxel.blt(self.x,self.y,self.chara[2][0],self.chara[2][1] - (self.walk_pos + 2) * 16,self.chara[2][2],self.chara[2][3] * -1,self.chara[2][4],self.chara[2][5],scale=self.scale)
            else:
                pyxel.blt(self.x,self.y,self.chara[2][0],self.chara[2][1] - self.walk_pos * 16,self.chara[2][2],self.chara[2][3],self.chara[2][4],self.chara[2][5],scale=self.scale)
        elif self.key == "s":
            if self.walk_pos == -1:
                pyxel.blt(self.x,self.y,self.chara[0][0],self.chara[0][1] - (self.walk_pos + 2) * 16,self.chara[0][2],self.chara[0][3] * -1,self.chara[0][4],self.chara[0][5],scale=self.scale)
            else:
                pyxel.blt(self.x,self.y,self.chara[0][0],self.chara[0][1] - self.walk_pos * 16,self.chara[0][2],self.chara[0][3],self.chara[0][4],self.chara[0][5],scale=self.scale)
        else:
            pyxel.blt(self.x,self.y,self.chara[0][0],self.chara[0][1] - self.walk_pos * 16,self.chara[0][2],self.chara[0][3],self.chara[0][4],self.chara[0][5],scale=self.scale)