import pyxel
import json

#新しいセーブデータを作成する
class Save:
    def __init__(self):
        pass

    def newsave(self,pos):
        with open("../configs/savedata.json",encoding="utf-8") as f:
            save_data = json.load(f)

        save_data[str(pos)] = {}
        #以下データフォーマット

    def save_game(self,game_pos):
        pass