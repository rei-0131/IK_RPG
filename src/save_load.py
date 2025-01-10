import pyxel
import json
import time
import os

import utils.scenes as scenes
from save import Save
from cloud_data import Cloud_data

try:
    from js import document, FileReader, window, Blob, URL
    from pyodide.ffi import create_proxy # type: ignore
except Exception:
    pass

#セーブデータをロードする画面を表示する
class SaveLoad:
    """
    セーブデータロード画面を表示

    Parameters
    ----------
    x : int
        画面のinit_x
    y : int
        画面のinit_y
    ump : Any
        umplus10(日本語出力)
    over_load : bool
        セーブデータの上書きが可能か
    left : bool
        左キーを押した際一つ前の動作に戻るかタイトルに戻るか
    load : bool
        セーブデータ、ロードオンリーかどうか
    app : Any
        Appクラスのself
    """
    def __init__(self,x,y,ump,app = None):
        self.app = app
        self.init_x = x
        self.init_y = y
        self.umplus10 = ump
        self.finger_pos = 0
        self.enter_pos = -1
        self.setting_finger = 1
        self.save_pos = 1
        self.save = Save(self.app)
        self.continue_game = False
        self.cloud = Cloud_data(self.app.is_test)
        self.over_tf = False
        self.save_enter = -1
        self.save_path = os.path.join(self.app.base_path,"save/savedata.json")
        if self.app.local:
            if self.app.exefile:
                self.save_data = json.load(open(self.save_path,"r",encoding="utf-8"))
            else:
                self.save_data = json.load(open("../save/savedata.json","r",encoding="utf-8"))
        else:
            self.save_data = self.cloud.load()
            document.body.addEventListener('dragover', create_proxy(self.on_dragover))
            document.body.addEventListener('drop', create_proxy(self.on_drop))
        self.first_show = True
        self.text = ""
        self.info_show = False
        self.info_count = 0
        self.info_text = ""
        self.load = scenes.LOAD_SCENE
        self.title = scenes.TITLE_SCENE
        self.main = scenes.MAIN_SCENE

    def clean(self):
        self.finger_pos = 0
        self.enter_pos = -1
        self.setting_finger = 1
        self.save_pos = 1
        self.save_enter = -1

    def save_download(self):
        data = [str(self.save_data)]
        blob = Blob.new(data, {'type': 'text/plain'})
        blob_url = URL.createObjectURL(blob)
        a = document.createElement('a')
        a.href = blob_url
        a.download = 'savedata.json'
        document.body.appendChild(a)
        a.click()
        document.body.removeChild(a)
        URL.revokeObjectURL(blob_url)

    def save_change(self,error = False):
        if error:
            self.info_text = "読み込みに失敗しました。バイナリデータの可能性があります。"
        else:
            try:
                self.save_data = json.loads(self.text)
                self.app.save_data = self.save_data
                if self.app.local:
                    if self.app.exefile:
                        json.dump(self.save_data,open(self.save_path,"w",encoding="utf-8"),indent=4,ensure_ascii=False)
                    else:
                        json.dump(self.save_data,open("../save/savedata.json","w",encoding="utf-8"),indent=4,ensure_ascii=False)
                else:
                    self.cloud.save(self.app.save_data)
                self.info_text = "セーブデータをアップロードしました"
            except Exception:
                self.info_text = "dict型への変換に失敗しました。"
        self.info_count = 0
        self.info_show = True

    def open_file_dialog(self):
        file_input = document.createElement('input')
        file_input.type = 'file'

        def on_change(event):
            files = file_input.files
            if files.length > 0:
                file = files.item(0)
                reader = FileReader.new()
                def on_load(event):
                    try:
                        self.text = reader.result
                        self.save_change()
                    except Exception:
                        self.save_change(True)
                reader.onload = on_load
                reader.readAsText(file)

        file_input.addEventListener('change', create_proxy(on_change))
        file_input.click()

    def on_dragover(self, e):
        e.preventDefault()

    def on_drop(self, e):
        go = False
        if self.app.now_scene == scenes.BATTLE_SCENE and self.app.battle.in_battle and self.app.battle.win != "player" and self.app.battle.select_num1 == 1:
            go = True
        elif self.app.now_scene == scenes.LOAD_SCENE:
            go = True
        elif self.app.setting.enter_pos == 8:
            go = True
        if go:
            e.preventDefault()
            files = e.dataTransfer.files
            for file in files:
                reader = FileReader.new()
                def on_load(e):
                    try:
                        self.text = reader.result
                        self.save_change()
                    except Exception:
                        self.save_change(True)
                reader.onload = on_load
                reader.readAsText(file)
                break

    def update(self,over_load,ent=None,battle_load = False,left=True,load=False) -> int:
        """
        基本処理

        Parameters
        ent:int
            不明
        """
        if self.setting_finger == self.save_pos + 4:
            self.save_pos += 1
        elif self.setting_finger == self.save_pos - 1:
            self.save_pos -= 1
        if self.info_show:
            if 60 > self.info_count:
                self.info_count += 1
            else:
                self.info_count = 0
                self.info_show = False
                self.info_text = ""
        if not battle_load:
            if left:
                enter_pos = ent
                if self.save_enter == -1:
                    if pyxel.btnp(pyxel.KEY_ESCAPE) or pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.KEY_A) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
                        enter_pos = -1
                        self.app.sound_manager.play_se("select")
                    if pyxel.btnp(pyxel.KEY_UP,hold = 8,repeat=8) or pyxel.btnp(pyxel.KEY_W,hold = 8,repeat=8) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP,hold = 8,repeat=8):
                        if self.setting_finger != 1:
                            self.setting_finger -= 1
                            self.app.sound_manager.play_se("select")
                        else:
                            if self.app.local:
                                self.setting_finger = 20
                                self.save_pos = 17
                            else:
                                self.setting_finger = 22
                                self.save_pos = 19
                    if pyxel.btnp(pyxel.KEY_DOWN,hold = 8,repeat=8) or pyxel.btnp(pyxel.KEY_S,hold = 8,repeat=8) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN,hold = 8,repeat=8):
                        if self.app.local:
                            if self.setting_finger != 20:
                                self.setting_finger += 1
                            else:
                                self.setting_finger = 1
                                self.save_pos = 1
                        else:
                            if self.setting_finger != 22:
                                self.setting_finger += 1
                            else:
                                self.setting_finger = 1
                                self.save_pos = 1
                        self.app.sound_manager.play_se("select")
                    if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
                        print(f"{self.setting_finger=}")
                        if not self.app.local and self.setting_finger == 21:
                            self.open_file_dialog()
                        elif not self.app.local and self.setting_finger == 22:
                            self.save_download()
                        else:
                            if over_load:
                                if str(self.setting_finger) in self.save_data:
                                    self.save_enter = self.setting_finger
                                else:
                                    self.save.newsave(self.setting_finger)
                                    if self.app.local:
                                        if self.app.exefile:
                                            self.save_data = json.load(open(self.save_path,"r",encoding="utf-8"))
                                        else:
                                            self.save_data = json.load(open("../save/savedata.json","r",encoding="utf-8"))
                                    else:
                                        self.save_data = self.cloud.load()
                                    self.app.save_data = self.save_data
                        self.app.sound_manager.play_se("ok")
                else:
                    if pyxel.btnp(pyxel.KEY_ESCAPE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
                        self.save_enter = -1
                        self.app.sound_manager.play_se("select")
                    if pyxel.btnp(pyxel.KEY_RIGHT,hold = 8,repeat=8) or pyxel.btnp(pyxel.KEY_D,hold = 8,repeat=8) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT,hold = 8,repeat=8):
                        if self.over_tf:
                            self.over_tf = False
                        else:
                            self.over_tf = True
                        self.app.sound_manager.play_se("select")
                    if pyxel.btnp(pyxel.KEY_LEFT,hold = 8,repeat=8) or pyxel.btnp(pyxel.KEY_A,hold = 8,repeat=8) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT,hold = 8,repeat=8):
                        if self.over_tf:
                            self.over_tf = False
                        else:
                            self.over_tf = True
                        self.app.sound_manager.play_se("select")
                    if (pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B)):
                        if self.over_tf:
                            self.save.newsave(self.save_enter)
                            if self.app.local:
                                if self.app.exefile:
                                    self.save_data = json.load(open(self.save_path,"r",encoding="utf-8"))
                                else:
                                    self.save_data = json.load(open("../save/savedata.json","r",encoding="utf-8"))
                            else:
                                self.save_data = self.cloud.load()
                            self.app.save_data = self.save_data
                        self.save_enter = -1
                        self.app.sound_manager.play_se("ok")
                return enter_pos
            else:
                enter_pos = self.load
                if self.save_enter == -1:
                    if pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.KEY_ESCAPE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
                        enter_pos = self.title
                        self.app.sound_manager.play_se("select")
                    if pyxel.btnp(pyxel.KEY_UP,hold = 8,repeat=8) or pyxel.btnp(pyxel.KEY_W,hold = 8,repeat=8) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP,hold = 8,repeat=8):
                        if self.setting_finger != 1:
                            self.setting_finger -= 1
                            self.app.sound_manager.play_se("select")
                        else:
                            if self.app.local:
                                self.setting_finger = 20
                                self.save_pos = 17
                            else:
                                self.setting_finger = 22
                                self.save_pos = 19
                    if pyxel.btnp(pyxel.KEY_DOWN,hold = 8,repeat=8) or pyxel.btnp(pyxel.KEY_S,hold = 8,repeat=8) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN,hold = 8,repeat=8):
                        if self.app.local:
                            if self.setting_finger != 20:
                                self.setting_finger += 1
                            else:
                                self.setting_finger = 1
                                self.save_pos = 1
                        else:
                            if self.setting_finger != 22:
                                self.setting_finger += 1
                            else:
                                self.setting_finger = 1
                                self.save_pos = 1
                        self.app.sound_manager.play_se("select")
                    if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
                        print(f"{self.setting_finger=}")
                        if not self.app.local and self.setting_finger == 21:
                            self.open_file_dialog()
                        elif not self.app.local and self.setting_finger == 22:
                            self.save_download()
                        else:
                            if self.load:
                                if str(self.setting_finger) in self.save_data:
                                    self.continue_game = True
                                    enter_pos = self.main
                            if over_load:
                                if str(self.setting_finger) in self.save_data:
                                    self.save_enter = self.setting_finger
                                else:
                                    self.save.newsave(self.setting_finger)
                        self.app.sound_manager.play_se("ok")
                else:
                    if pyxel.btnp(pyxel.KEY_ESCAPE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
                        self.save_enter = -1
                        self.app.sound_manager.play_se("select")
                    if pyxel.btnp(pyxel.KEY_RIGHT,hold = 8,repeat=8) or pyxel.btnp(pyxel.KEY_D,hold = 8,repeat=8) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT,hold = 8,repeat=8):
                        if self.over_tf:
                            self.over_tf = False
                        else:
                            self.over_tf = True
                        self.app.sound_manager.play_se("select")
                    if pyxel.btnp(pyxel.KEY_LEFT,hold = 8,repeat=8) or pyxel.btnp(pyxel.KEY_A,hold = 8,repeat=8) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT,hold = 8,repeat=8):
                        if self.over_tf:
                            self.over_tf = False
                        else:
                            self.over_tf = True
                        self.app.sound_manager.play_se("select")
                    if (pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B)):
                        if self.over_tf:
                            self.save.newsave(self.setting_finger)
                            if self.app.local:
                                if self.app.exefile:
                                    self.save_data = json.load(open(self.save_path,"r",encoding="utf-8"))
                                else:
                                    self.save_data = json.load(open("../save/savedata.json","r",encoding="utf-8"))
                            else:
                                self.save_data = self.cloud.load()
                            self.app.save_data = self.save_data
                        self.save_enter = -1
                        self.app.sound_manager.play_se("ok")
                return enter_pos
        else:
            if pyxel.btnp(pyxel.KEY_ESCAPE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
                self.app.battle.select_num1 = -1
                self.app.sound_manager.play_se("select")
            if pyxel.btnp(pyxel.KEY_UP,hold = 8,repeat=8) or pyxel.btnp(pyxel.KEY_W,hold = 8,repeat=8) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP,hold = 8,repeat=8):
                if self.setting_finger != 1:
                    self.setting_finger -= 1
                    self.app.sound_manager.play_se("select")
                else:
                    if self.app.local:
                        self.setting_finger = 20
                        self.save_pos = 17
                    else:
                        self.setting_finger = 22
                        self.save_pos = 19
            if pyxel.btnp(pyxel.KEY_DOWN,hold = 8,repeat=8) or pyxel.btnp(pyxel.KEY_S,hold = 8,repeat=8) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN,hold = 8,repeat=8):
                if self.app.local:
                    if self.setting_finger != 20:
                        self.setting_finger += 1
                    else:
                        self.setting_finger = 1
                        self.save_pos = 1
                else:
                    if self.setting_finger != 22:
                        self.setting_finger += 1
                    else:
                        self.setting_finger = 1
                        self.save_pos = 1
                self.app.sound_manager.play_se("select")
            if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
                if not self.app.local and self.setting_finger == 21:
                    self.open_file_dialog()
                elif not self.app.local and self.setting_finger == 22:
                    self.save_download()
                else:
                    if str(self.setting_finger) in self.save_data:
                        if self.app.local:
                            if self.app.exefile:
                                self.save_data = json.load(open(self.save_path,"r",encoding="utf-8"))
                            else:
                                self.save_data = json.load(open("../save/savedata.json","r",encoding="utf-8"))
                        else:
                            self.savedata = self.app.cloud.load()
                            time.sleep(0.3)
                        self.app.save_data = self.save_data
                        self.game_time_start = time.time()
                        print(f"{self.setting_finger=}")
                        self.app.loaddata = self.app.save_data[str(self.setting_finger)]
                        self.app.game_time = self.app.save_data[str(self.setting_finger)]["play_data"]["time"]
                        self.app.money = self.app.save_data[str(self.setting_finger)]["play_data"]["money"]
                        self.app.now_scene = self.app.save_data[str(self.setting_finger)]["play_data"]["scene"]
                        self.app.now_location = self.app.save_data[str(self.setting_finger)]["play_data"]["location"]
                        self.app.player.x = self.app.save_data[str(self.setting_finger)]["play_data"]["x"]
                        self.app.player.y = self.app.save_data[str(self.setting_finger)]["play_data"]["y"]
                        self.app.chara_data = self.app.save_data[str(self.setting_finger)]["play_data"]["chara_data"]
                        self.app.item_codes = self.app.save_data[str(self.setting_finger)]["play_data"]["item_codes"]
                        self.app.imp_item_codes = self.app.save_data[str(self.setting_finger)]["play_data"]["imp_item_codes"]
                        self.app.equip_codes = self.app.save_data[str(self.setting_finger)]["play_data"]["equip_codes"]
                        self.app.msg_id = self.app.save_data[str(self.setting_finger)]["play_data"]["words"]["msg_id"]
                        self.app.disp_id = self.app.save_data[str(self.setting_finger)]["play_data"]["words"]["disp_id"]
                        self.app.story_flags_tf = {k:bool(v) for k,v in self.app.save_data[str(self.setting_finger)]["play_data"]["story_flags_tf"].items()}
                        self.app.story_flags_co = {k:bool(v) for k,v in self.app.save_data[str(self.setting_finger)]["play_data"]["story_flags_co"].items()}
                        self.app.question_selects = self.app.save_data[str(self.setting_finger)]["play_data"]["question_selects"]
                        self.app.in_battle = False
                self.app.sound_manager.play_se("ok")

    def draw(self):
        """基本描画"""
        pyxel.rect(70,5,self.init_x-70,self.init_y-5,0)
        pyxel.rectb(70,5,self.init_x-70,self.init_y-5,7)
        for i,l in zip(range(0,4),range(self.save_pos,4+self.save_pos)):
            if l == self.setting_finger:
                pyxel.rect(70,5+(48.75*(i)),self.init_x-70,48.75,1)
                pyxel.rectb(70,5+(48.75*(i)),self.init_x-70,48.75,7)
            else:
                pyxel.rect(70,5+(48.75*(i)),self.init_x-70,48.75,0)
                pyxel.rectb(70,5+(48.75*(i)),self.init_x-70,48.75,7)
            if l != 21 and l != 22:
                self.umplus10.draw_text(71,5+int(48.75*(i)),f"data {l}",7)
            if str(l) in self.app.save_data:
                self.umplus10.draw_text(200,6+int(48.75*(i)),f"time:{self.app.save_data[str(l)]['play_data']['time']}",7)
            else:
                if l == 21:
                    self.umplus10.draw_text(125,25+int(48.75*(i)),f"ファイルをアップロード",7)
                elif l == 22:
                    self.umplus10.draw_text(125,25+int(48.75*(i)),f"ファイルをダウンロード",7)
                else:
                    self.umplus10.draw_text(125,25+int(48.75*(i)),f"保存データなし",7)
        if self.save_enter != -1:
            pyxel.rect(90,80,110,40,0)
            pyxel.rectb(90,80,110,40,7)
            self.umplus10.draw_text(107,81,"上書きしますか？",7)
            if self.over_tf:
                pyxel.rect(95,102,33,11,1)
            else:
                pyxel.rect(150,102,33,11,1)
            self.umplus10.draw_text(101,102,"はい",7)
            self.umplus10.draw_text(151,102,"いいえ",7)
        if self.info_show:
            self.umplus10.draw_text(5,0,f"{self.info_text}".center(28,"　"),7)