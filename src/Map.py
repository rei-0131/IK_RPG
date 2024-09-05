import pyxel
import json

class Map:
    """
    マップに関するクラス
    """
    def __init__(self):
        with open("assets/map.json",encoding="utf-8") as f:
            self.map_data = json.load(f)
        self.map_x = 19
        self.map_y = 13
        self.key = ""
        self.next_x = 0
        self.next_y = 0

    def cd_check(self,x,y,dx,dy,num,key):
        """
        当たり判定の判定

        Parameters
        ----------
        x : float
            プレイヤーの現在位置x
        y : float
            プレイヤーの現在位置y
        dx : float
            次のフレームで動く距離x
        dy : float
            次のフレームで動く距離y
        num : int
            タイルマップデータ番号
        key : string
            wasdのどれが押されたか
            スマホやゲームパッドの場合はキーボードに相当するキー

        Returns
        ----------
        Any : bool
            あたっている場合はTrue、そうでない場合はFalse
        """
        self.next_x = x + dx
        self.next_y = y + dy
        self.key = key
        check_x = [self.next_x,self.next_x]
        check_y = [self.next_y,self.next_y]
        if self.key == "w":
            check_x[0] += 2
            check_x[1] += 14
        elif self.key == "s":
            check_x[0] += 2
            check_x[1] += 14
            check_y[0] += 14
            check_y[1] += 14
        elif self.key == "a":
            check_y[0] += 3
            check_y[1] += 13
        elif self.key == "d":
            check_x[0] += 14
            check_x[1] += 14
            check_y[0] += 3
            check_y[1] += 13
        if pyxel.tilemaps[num].pget(check_x[0]//8, check_y[0]//8) != (0,2) and pyxel.tilemaps[num].pget(check_x[1]//8, check_y[1]//8) != (0,2):
            return False
        else:
            return True

    def cd_debug(self):
        """
        当たり判定のデバッグ
        現在のフレームの当たり判定の場所を表示
        """
        if self.key == "w":
            pyxel.line(self.next_x+2,self.next_y,self.next_x+2,self.next_y,0)
            pyxel.line(self.next_x+16-2,self.next_y,self.next_x+16-2,self.next_y,0)
        elif self.key == "s":
            pyxel.line(self.next_x+2,self.next_y+14,self.next_x+2,self.next_y+14,0)
            pyxel.line(self.next_x+16-2,self.next_y+14,self.next_x+16-2,self.next_y+14,0)
        elif self.key == "a":
            pyxel.line(self.next_x,self.next_y+3,self.next_x,self.next_y+3,0)
            pyxel.line(self.next_x,self.next_y+16-3,self.next_x,self.next_y+16-3,0)
        elif self.key == "d":
            pyxel.line(self.next_x+14,self.next_y+3,self.next_x+14,self.next_y+3,0)
            pyxel.line(self.next_x+14,self.next_y+16-3,self.next_x+14,self.next_y+16-3,0)