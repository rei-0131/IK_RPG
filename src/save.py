import pyxel
import json

#新しいセーブデータを作成する
class Save:
    def __init__(self,app = None):
        self.app = app
        with open("../assets/scenes.json",encoding="utf-8") as f:
            self.scenes = json.load(f)

    def newsave(self,pos):
        with open("../configs/savedata.json",encoding="utf-8") as f:
            save_data = json.load(f)

        #以下コードからAppクラスの変数にアクセス
        save_data[str(pos)] = {}
        save_data[str(pos)]["play_data"] = {
            "time":"00:00:00",
            "scene":self.scenes["MAIN_SCENE"],
            "x":self.app.player.x,
            "y":self.app.player.y,
        }
        with open("../configs/savedata.json","w",encoding="utf-8") as f:
            json.dump(save_data,f,indent=4)

    def save_game(self,game_pos):
        pass