import pyxel
import json
import numpy as np

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
        self.cd_blocks = [3,]

    def draw_map(self,num):
        """
        マップの描画

        Parameters:
        ----------
        num : int
            マップデータ番号
        """
        map_ = self.map_data[str(num)]
        for y in range(self.map_y):
            for x in range(self.map_x):
                pyxel.blt(16*x,16*y,1,map_[y][x]*16,0,16,16,0)

    def cd_check(self,x,y,dx,dy,num,key):
        """
        当たり判定の判定

        Parameters:
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
            マップデータ番号
        key : string
            wasdのどれが押されたか
            スマホやゲームパッドの場合はキーボードに相当するキー

        Returns:
        ----------
        Any : bool
            あたっている場合はTrue、そうでない場合はFalse
        """
        self.key = key
        map_ = self.map_data[str(num)]
        input_array = np.array(map_)
        enlarged_array = np.repeat(np.repeat(input_array, 16, axis=1), 16, axis=0)
        map_16 = enlarged_array.tolist()
        next_x = x + dx
        next_y = y + dy
        self.next_x = next_x
        self.next_y = next_y
        if key == "w" and (map_16[next_y][next_x+2] in self.cd_blocks or map_16[next_y][next_x+16-2] in self.cd_blocks):
            return True
        elif key == "s" and (map_16[next_y+16][next_x+2] in self.cd_blocks or map_16[next_y+16][next_x+16-2] in self.cd_blocks):
            return True
        elif key == "a" and (map_16[next_y+3][next_x] in self.cd_blocks or map_16[next_y+16-3][next_x] in self.cd_blocks):
            return True
        elif key == "d" and (map_16[next_y+3][next_x+16] in self.cd_blocks or map_16[next_y+16-3][next_x+16] in self.cd_blocks):
            return True
        else:
            return False
        # next_x = int((x + dx)/16)
        # next_y = int((y + dy)/16)
        # if map_[next_y][next_x] in self.cd_blocks or map_[next_y+1][next_x] in self.cd_blocks or map_[next_y][next_x+1] in self.cd_blocks or map_[next_y+1][next_x+1] in self.cd_blocks:
        #     return True
        # else:
        #     return False

    def cd_debug(self):
        """
        当たり判定のデバッグ\n
        現在のフレームの当たり判定の場所を表示
        """
        if self.key == "w":
            pyxel.line(self.next_x+2,self.next_y,self.next_x+2,self.next_y,0)
            pyxel.line(self.next_x+16-2,self.next_y,self.next_x+16-2,self.next_y,0)
        elif self.key == "s":
            pyxel.line(self.next_x+2,self.next_y+16,self.next_x+2,self.next_y+16,0)
            pyxel.line(self.next_x+16-2,self.next_y+16,self.next_x+16-2,self.next_y+16,0)
        elif self.key == "a":
            pyxel.line(self.next_x,self.next_y+3,self.next_x,self.next_y+3,0)
            pyxel.line(self.next_x,self.next_y+16-3,self.next_x,self.next_y+16-3,0)
        elif self.key == "d":
            pyxel.line(self.next_x+16,self.next_y+3,self.next_x+16,self.next_y+3,0)
            pyxel.line(self.next_x+16,self.next_y+16-3,self.next_x+16,self.next_y+16-3,0)