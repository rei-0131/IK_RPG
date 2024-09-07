import json
import time
#新しいセーブデータを作成する
class Save:
    """
    セーブに関するクラス

    Parameters
    ----------
    app : Any
        Appクラスのインスタンス
    """
    def __init__(self,app = None):
        self.app = app
        self.cloud = self.app.cloud
        self.scenes = self.app.scenes

    def newsave(self,pos):
        """新しいセーブ"""
        if self.app.local:
            with open("configs/savedata.json",encoding="utf-8") as f:
                save_data = json.load(f)
        else:
            save_data = self.cloud.load()

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
            "chara_data":self.app.chara_data,
            "item_codes":self.app.item_codes,
            "imp_item_codes":self.app.imp_item_codes,
            "equip_codes":self.app.equip_codes
        }
        if self.app.local:
            with open("configs/savedata.json","w",encoding="utf-8") as f:
                json.dump(save_data,f,indent=4,ensure_ascii=False)
        else:
            self.cloud.save(save_data)