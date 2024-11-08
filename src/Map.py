import pyxel
import numpy as np


class Map:
    """
    マップに関するクラス

    Parameters
    ----------
    app : Any
        Appクラスのインスタンス
    """

    def __init__(self, app):
        self.app = app
        self.init_x = self.app.init_x
        self.init_y = self.app.init_y
        self.collision_data = self.app.collision_data
        self.map_x = 19
        self.map_y = 13
        self.key = ""
        self.next_x = 0
        self.next_y = 0
        self.player_scale = self.app.player_scale

    def check_pos(self, key, player_scale, x, y, scale, gap_x, gap_y) -> tuple[list, list]:
        point_n = 10
        check_x = [x - (self.init_x // 2 * (1 - scale) + (gap_x * scale)) - 8 * (player_scale - 1) for _ in range(point_n)]
        check_y = [y - (self.init_y // 2 * (1 - scale) + (gap_y * scale)) - 8 * (player_scale - 1) for _ in range(point_n)]
        check_x = np.array(check_x)
        check_y = np.array(check_y)
        # print([check_x[0], check_y[0]],end="\r")
        # 0,0 9,9 17,17 25,25
        if key == "w":
            check_x[0] += 2
            for i in range(1,point_n):
                check_x[i] += 2 + 12 / (point_n - 1) * i * player_scale
        elif key == "s":
            check_x[0] += 2
            for i in range(1,point_n):
                check_x[i] += 2 + 12 / (point_n - 1) * i * player_scale
            check_y += 16 * player_scale
        elif key == "a":
            check_x += 2
            check_y[0] += 0
            for i in range(1,point_n - 1):
                check_y[i] += 16 / (point_n - 2) * i * player_scale
            check_y[point_n - 1] += 16 * player_scale
        elif key == "d":
            for i in range(point_n):
                check_x[i] += 14 * player_scale
            check_y[0] += 0
            for i in range(1,point_n - 1):
                check_y[i] += 16 / (point_n - 2) * i * player_scale
            check_y[point_n - 1] += 16 * player_scale
        return check_x, check_y

    def cd_check(self, x, y, dx, dy, num, key, scale, gap_x = 0,gap_y = 0) -> tuple[bool,str]:
        """
        当たり判定の判定

        Parameters
        ----------
        x : int
            プレイヤーの現在位置x
        y : int
            プレイヤーの現在位置y
        dx : int
            次のフレームで動く距離x
        dy : int
            次のフレームで動く距離y
        num : int
            タイルマップデータ番号
        key : string
            wasdのどれが押されたか
            スマホやゲームパッドの場合はキーボードに相当するキー
        scale : float
            表示しているタイルマップのスケール
        gap_x : int
            タイルマップの初期表示座標x
        gap_y : int
            タイルマップの初期表示座標y

        Returns
        ----------
        Any : bool
            あたっている場合はTrue、そうでない場合はFalse
        Any : str
            あたったブロックのタイプ
        """
        self.next_x = x + dx
        self.next_y = y + dy
        self.key = key
        check_x, check_y = self.check_pos(self.key, self.player_scale, self.next_x, self.next_y, scale, gap_x, gap_y)
        pixel_size = 8 * scale
        pyxel.text(0, 99, f"{check_x}", 7)
        pyxel.text(0, 110, f"{check_y}", 7)
        cd = [i[0] for i in self.collision_data[str(num)]]
        cd_tf = [list(pyxel.tilemaps[num].pget(x // pixel_size, y // pixel_size)) in cd for x,y in zip(check_x, check_y)]
        if not True in cd_tf:
            return False,""
        else:
            xy_index = cd_tf.index(True)
            type_ = self.collision_data[str(num)][cd.index(list(pyxel.tilemaps[num].pget(check_x[xy_index] // pixel_size, check_y[xy_index] // pixel_size)))][1]
            return True, type_

    def cd_debug(self, x, y, key, scale, gap_x = 0,gap_y = 0):
        """
        当たり判定のデバッグ
        現在のフレームの当たり判定の場所を表示

        Parameters
        ----------
        x : int
            プレイヤーのx座標
        y : int
            プレイヤーのy座標
        key : string
            wasdのどれが押されたか
            スマホやゲームパッドの場合はキーボードに相当するキー
        scale : float
            表示しているタイルマップのスケール
        gap_x : int
            タイルマップの初期表示座標x
        gap_y : int
            タイルマップの初期表示座標y
        """
        check_x, check_y = self.check_pos(key, self.player_scale, x, y, scale, gap_x, gap_y)
        pyxel.line(x - (self.init_x // 2 * (1 - scale) + (gap_x * scale)) - 8 * (self.player_scale - 1),
                   y - (self.init_y // 2 * (1 - scale) + (gap_y * scale)) - 8 * (self.player_scale - 1),
                   x - (self.init_x // 2 * (1 - scale) + (gap_x * scale)) - 8 * (self.player_scale - 1),
                   y - (self.init_y // 2 * (1 - scale) + (gap_y * scale)) - 8 * (self.player_scale - 1),8)
        for x_,y_ in zip(check_x,check_y):
            pyxel.line(x_, y_, x_, y_, 0)
