import pyxel
import utils.scenes as scenes

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
    ump : Any
        umplus10(日本語出力)
    """
    def __init__(self,app,x,y,ump):
        self.app = app
        self.x = 20
        self.y = y - 100
        self.umplus10 = ump
        self.dx = 0
        self.dy = 0
        self.init_x = x
        self.init_y = y
        self.rl = 1
        self.key = ""
        self.walk_speed = 2
        self.walk_num = 0
        self.question_mark = 0
        self.is_word = False
        self.map = self.app.map
        self.chara = self.app.assets_info["chara"]["ぼく"]
        self.walk_pos = 0
        self.walk_pm = "p"
        self.scale = self.app.player_scale
        self.story_flag_progress = []

    def update(self):
        """基本処理"""
        self.dx = 0
        self.dy = 0
        if not self.app.in_word and not self.app.trade:
            if (pyxel.btn(pyxel.KEY_RIGHT) and not pyxel.btn(pyxel.KEY_UP) and not pyxel.btn(pyxel.KEY_DOWN)) or (pyxel.btn(pyxel.KEY_D) and not pyxel.btn(pyxel.KEY_W) and not pyxel.btn(pyxel.KEY_S)) or (pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT) and not pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP) and not pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN)):
                self.dx += self.walk_speed
                self.rl = 1
                self.key = "d"
            if (pyxel.btn(pyxel.KEY_LEFT) and not pyxel.btn(pyxel.KEY_UP) and not pyxel.btn(pyxel.KEY_DOWN)) or (pyxel.btn(pyxel.KEY_A) and not pyxel.btn(pyxel.KEY_W) and not pyxel.btn(pyxel.KEY_S)) or (pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT) and not pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP) and not pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN)):
                self.dx -= self.walk_speed
                self.rl = -1
                self.key = "a"
            if (pyxel.btn(pyxel.KEY_UP) and not pyxel.btn(pyxel.KEY_LEFT) and not pyxel.btn(pyxel.KEY_RIGHT)) or (pyxel.btn(pyxel.KEY_W) and not pyxel.btn(pyxel.KEY_A) and not pyxel.btn(pyxel.KEY_D)) or (pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP) and not pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT) and not pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT)):
                self.dy -= self.walk_speed
                self.key = "w"
            if (pyxel.btn(pyxel.KEY_DOWN) and not pyxel.btn(pyxel.KEY_LEFT) and not pyxel.btn(pyxel.KEY_RIGHT)) or (pyxel.btn(pyxel.KEY_S) and not pyxel.btn(pyxel.KEY_A) and not pyxel.btn(pyxel.KEY_D)) or (pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN) and not pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT) and not pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT)):
                self.dy += self.walk_speed
                self.key = "s"
            if not (pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT) or pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT) or pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_W) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP) or pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.KEY_S) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN)):
                self.walk_num = 0
                self.walk_pos = 0
            elif (pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT) or pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT) or pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_W) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP) or pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.KEY_S) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN)):
                if self.walk_num % 3 == 0:
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
        else:
            if self.walk_num != 0 or self.walk_pos != 0:
                self.walk_num = 0
                self.walk_pos = 0
        cd_return = self.map.cd_check(self.x,self.y,self.dx,self.dy,self.app.now_map,self.key,self.app.scale,self.app.coord)
        if not cd_return[0]:
            self.x += self.dx
            self.y += self.dy
            if (self.dx != 0 or self.dy != 0) and not self.app.in_word:
                if self.app.now_location == scenes.CLASS3_SCENE:
                    #0.444%
                    if 1 <= pyxel.rndi(1,100000) <= 444:
                        self.app.random_encount = True
                        self.app.battle.clean(self.app.now_scene)
                        self.app.battle.save_chara(self.app.chara_data)
                        if self.app.is_test:
                            self.app.battle.debug_clean()
                        enemy_num = pyxel.rndi(1,4)
                        enemy_code = [pyxel.rndi(1,3) for _ in range(enemy_num)]
                        enemys = [{"enemy_type":"general","enemy_code":f"mob{i}"} for i in enemy_code]
                        self.app.battle.set_enemy(enemy_num,enemys)
                        self.app.be_scene = self.app.now_scene
                        self.app.now_scene = scenes.BATTLE_SCENE
                        if self.app.bgm_run:
                            self.app.sound_manager.stop()
                elif (self.app.now_location == scenes.WAY_SCENE_12 or
                        self.app.now_location == scenes.WAY_SCENE_31 or
                        self.app.now_location == scenes.WAY_SCENE_I or
                        self.app.now_location == scenes.WAY_SCENE_E):
                    #0.111%
                    if 1 <= pyxel.rndi(1,100000) <= 111:
                        self.app.random_encount = True
                        self.app.battle.clean(self.app.now_scene)
                        self.app.battle.save_chara(self.app.chara_data)
                        if self.app.is_test:
                            self.app.battle.debug_clean()
                        enemy_num = pyxel.rndi(1,4)
                        enemy_code = [pyxel.rndi(1,3) for _ in range(enemy_num)]
                        enemys = [{"enemy_type":"general","enemy_code":f"mob{i}"} for i in enemy_code]
                        self.app.battle.set_enemy(enemy_num,enemys)
                        self.app.be_scene = self.app.now_scene
                        self.app.now_scene = scenes.BATTLE_SCENE
                        if self.app.bgm_run:
                            self.app.sound_manager.stop()
        else:
            if not self.app.in_word and not self.app.trade:
                if pyxel.btnp(pyxel.KEY_F) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
                    if cd_return[1] == "mob":
                        if self.app.mobs[self.app.now_location - 6][cd_return[2]][2][2] != -1:
                            if self.app.mobs[self.app.now_location - 6][cd_return[2]][2][2] == "T":
                                self.app.trade = True
                                self.app.sound_manager.play_se("ok")
                            else:
                                story_f = True
                                if self.app.disp_id == "115" and self.app.mobs[self.app.now_location - 6][cd_return[2]][2][2] == 98:
                                    story_f = False
                                if self.app.story_flags_tf["200_speak"] and self.app.mobs[self.app.now_location - 6][cd_return[2]][2][3] == [[187,212]]:
                                    story_f = False
                                if story_f:
                                    if str(self.app.mobs[self.app.now_location - 6][cd_return[2]][2][2]) == self.app.msg_id:
                                        self.app.disp_id = str(int(self.app.disp_id) - 1)
                                    else:
                                        if str(self.app.mobs[self.app.now_location - 6][cd_return[2]][2][2]) == "9001":
                                            self.app.be_msg_id = self.app.msg_id
                                        self.app.msg_id = str(self.app.mobs[self.app.now_location - 6][cd_return[2]][2][2])
                                    self.app.sound_manager.play_se("ok")
                    elif cd_return[1] == "trash":
                        if 129 <= int(self.app.msg_id) <= 140 and self.app.now_location == scenes.STAFF_M_SCENE:
                            self.app.msg_id = "132"
                            self.app.sound_manager.play_se("ok")
                    elif "it_search" in cd_return[1] and (self.app.msg_id == "152" or self.app.msg_id == "9000") and cd_return[1] not in self.story_flag_progress:
                        self.app.story_flags_co["staff_it_search"] += 1
                        self.story_flag_progress.append(cd_return[1])
                        self.app.msg_id = "9000"
                        self.app.disp_id = "152"
                        self.app.sound_manager.play_se("ok")
                    elif "ch" in cd_return[1]:
                        if 191 <= int(self.app.msg_id) <= 198:
                            if cd_return[1] == "ch_2":
                                self.app.msg_id = "192"
                                if self.app.msg_id == self.app.disp_id:
                                    self.app.disp_id = "191"
                                self.app.sound_manager.play_se("ok")
                            elif cd_return[1] == "ch_4":
                                self.app.msg_id = "197"
                                self.app.sound_manager.play_se("ok")

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