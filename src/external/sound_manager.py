import json
import pyxel
import sys

class SoundManager:
    def __init__(self):
        self.bgms = {}  # BGMを格納する辞書
        self.ses = {}  # SEを格納する辞書
        self.seStack = 63  # 使用可能なサウンドバンクの数
        self.tick = None  # 現在の再生位置
        self.se = ""  # 現在再生中のSE名
        self.bgm = ""  # 現在再生中のBGM名
        self.isLoop = True  # BGMがループ再生するかどうか
        self.seChannel = 2 # SEが再生されるチャンネル

    def set_seChannel(self, ch: int):
        """SEを再生するチャンネルを指定"""
        self.seChannel = ch

    def load_bgm(self, path: str, name: str):
        """指定されたパスからBGMを読み込み、辞書に格納する"""
        try:
            with open(f"./sounds/{path}.json", "rt") as fin:
                self.bgms[name] = json.loads(fin.read())
        except FileNotFoundError:
            raise FileNotFoundError(f"Error: File '{path}.json' not found")

    def load_se(self, path: str, name: str):
        """指定されたパスからSEを読み込み、サウンドバンクにセットする"""
        if self.seStack > 3:
            try:
                with open(f"./sounds/{path}.json", "rt") as fin:
                    se = json.loads(fin.read())
                for ch, sound in enumerate(se):
                    if ch == 0:
                        pyxel.sound(self.seStack).set(*sound)
                self.ses[name] = self.seStack
                self.seStack -= 1
            except FileNotFoundError:
                raise FileNotFoundError(f"Error: File '{path}.json' not found")
        else:
            raise OverflowError("Error: Sound Bank is overflow!!")

    def set_se(self, name: str, snd_num: int):
        """pyxresのsnd_numを登録"""
        self.ses[name] = snd_num

    def play_bgm(self, name: str, loop: bool = True):
        """指定された名前のBGMを再生する"""
        if self.tick is None:
            if self._isExist(name, self.bgms):
                self.tick = 0
                self.isLoop = loop
                for ch, sound in enumerate(self.bgms[name]):
                    pyxel.sound(ch).set(*sound)
                    pyxel.play(ch, ch, loop=loop)
        else:
            self.tick = self._get_crt_tick()
            self._back_to_bgm()

    def play_se(self, name: str):
        """指定された名前のSEを再生する"""
        if self._isExist(name, self.ses):
            pyxel.play(self.seChannel, self.ses[name])

    def stop(self):
        """全てのサウンドを停止する"""
        pyxel.stop()

    def _back_to_bgm(self):
        """SE再生後にBGMに戻る"""
        if pyxel.play_pos(self.seChannel) is None:  # SEが鳴り終わったら
            pyxel.play(self.seChannel, [self.seChannel], self.tick, self.isLoop)  # 再びBGMを鳴らす

    def _get_crt_tick(self) -> int:
        """現在の再生位置を取得する"""
        for i in range(4):
            if pyxel.play_pos(i) is not None:
                self.tick = pyxel.play_pos(i)[1]
                return self.tick
        raise RuntimeError("All channels are stopped!")

    def _isExist(self, name: str, sound_dict: dict) -> bool:
        """指定された名前の音声が存在するかチェックする"""
        if name not in sound_dict:
            raise KeyError(f"Cannot find '{name}'")
        return True

