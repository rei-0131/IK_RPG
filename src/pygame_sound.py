import pygame
import pyxel
import os
import sys

import utils.scenes as scenes


exefile = False

def resource_path(self,relative_path):
    """
    パスチェック

    Parameters
    ----------
    relative_path : str
        パス

    Returns
    ----------
    Any : str
        パス
    """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

base_path = os.path.dirname(os.path.abspath(sys.argv[0]))


class pygame_sound:
    def __init__(self,app):
        self.app = app
        self.filename = ""
        self.now_music = ""
        self.stop_ = False
        pygame.mixer.init()

    def loop(self,filename=None):
        pos = pygame.mixer.music.get_pos()

        if int(pos) == -1 or self.stop_ or filename is not None:
            if filename is not None:
                self.filename = filename
            pygame.mixer.music.load(self.filename)
            pygame.mixer.music.play(-1)
            self.stop_ = False

    def stop(self):
        pygame.mixer.music.stop()
        self.stop_ = True

    def update(self):
        if self.app.now_scene == scenes.TITLE_SCENE or None:
            if self.now_music != "op":
                pygame.mixer.music.set_volume(0.4)
                self.loop("assets/sounds/op.mp3")
                self.now_music = "op"
        elif self.app.now_scene == scenes.LOAD_SCENE:
            if not self.stop_:
                self.stop()
                self.now_music = ""
        elif self.app.now_scene == "Endroll":
            if self.now_music != "endroll":
                self.loop("assets/sounds/endroll.mp3")
                self.now_music = "endroll"
        elif self.app.now_scene == scenes.MAIN_SCENE:
            if self.now_music != "city":
                self.loop("assets/sounds/city.mp3")
                self.now_music = "city"
        elif self.app.now_scene == scenes.BATTLE_SCENE:
            if self.app.battle.win == "":
                if self.app.battle.in_boss:
                    status = [i["enemy_name"]["enemy_code"] for i in self.app.battle.enemy_status][0]
                    if "momonoi" in status:
                        if "1" in status:
                            if self.now_music != "boss1":
                                self.loop("assets/sounds/last_boss_1.mp3")
                                self.now_music = "boss1"
                        elif "2" in status:
                            if self.now_music != "boss2":
                                self.loop("assets/sounds/last_boss_2.mp3")
                                self.now_music = "boss2"
                    else:
                        if self.now_music != "boss":
                            self.loop("assets/sounds/boss.mp3")
                            self.now_music = "boss"
                else:
                    if self.now_music != "battle":
                        self.loop("assets/sounds/normal_battle.mp3")
                        self.now_music = "battle"
            else:
                if not self.stop_:
                    self.stop()
                    self.now_music = ""