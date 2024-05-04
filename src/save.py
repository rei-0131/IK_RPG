import pyxel
import json
import time

#新しいセーブデータを作成する
class Save:
    def __init__(self,app = None):
        self.app = app
        with open("assets/scenes.json",encoding="utf-8") as f:
            self.scenes = json.load(f)

    def newsave(self,pos):
        with open("configs/savedata.json",encoding="utf-8") as f:
            save_data = json.load(f)

        #以下コードからAppクラスの変数にアクセス
        time_time = int(time.time() - self.app.game_time_start)
        old_time_h,old_time_m,old_time_s = map(int,self.app.game_time.split(":"))
        time_time += old_time_h * 3600
        time_time += old_time_m * 60
        time_time += old_time_s
        time_h = time_time // 3600
        time_m = (time_time % 3600) // 60
        time_s = (time_time % 3600 % 60)
        save_data[str(pos)] = {}
        save_data[str(pos)]["play_data"] = {
            "time":f"{str(time_h).zfill(2)}:{str(time_m).zfill(2)}:{str(time_s).zfill(2)}",
            "scene":self.scenes["MAIN_SCENE"],
            "x":self.app.player.x,
            "y":self.app.player.y,
        }
        with open("configs/savedata.json","w",encoding="utf-8") as f:
            json.dump(save_data,f,indent=4)