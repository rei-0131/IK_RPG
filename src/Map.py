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

    def check_pos(self, key, player_scale, x, y, scale, coord) -> tuple[np.ndarray, np.ndarray]:
        """
        画面当たり判定座標計算

        Parameters
        ----------
        key : str
            進むキー
        player_scale : float
            プレイヤーの大きさ
        x : int
            プレイヤー座標x
        y : int
            プレイヤー座標y
        scale : float
            マップスケール
        coord : list
            マップ情報

        Returns
        ----------
        check_x : np.ndarray
            当たり判定座標x
        check_y : np.ndarray
            当たり判定座標y
        """
        gap_x = coord[0]
        gap_y = coord[1]
        point_n = 10
        check_x = [x - (self.init_x // 2 * (1 - scale) + gap_x * scale - coord[3] * scale) - 8 * (player_scale - 1) for _ in range(point_n)]
        check_y = [y - (self.init_y // 2 * (1 - scale) + gap_y * scale - coord[4] * scale) - 8 * (player_scale - 1) for _ in range(point_n)]
        check_x = np.array(check_x)
        check_y = np.array(check_y)
        # print([check_x[0], check_y[0]],end="\r")
        # 0,0 9,9 17,17 25,25
        if key == "w":
            check_x[0] += 3
            for i in range(1,point_n - 1):
                check_x[i] += 2 + 12 / (point_n - 1) * i * player_scale
            check_y += player_scale * 9
        elif key == "s":
            check_x[0] += 3
            for i in range(1,point_n - 1):
                check_x[i] += 2 + 12 / (point_n - 1) * i * player_scale
            check_y += 16 * player_scale
        elif key == "a":
            check_x += 2
            for i in range(8):
                check_y[i] += 12 / (point_n - 2) * 7 * player_scale
            for i in range(8,point_n - 1):
                check_y[i] += 12 / (point_n - 2) * i * player_scale
            check_y[point_n - 1] += 16 * player_scale
        elif key == "d":
            for i in range(point_n):
                check_x[i] += 12 * player_scale
            for i in range(8):
                check_y[i] += 12 / (point_n - 2) * 7 * player_scale
            for i in range(8,point_n - 1):
                check_y[i] += 12 / (point_n - 2) * i * player_scale
            check_y[point_n - 1] += 16 * player_scale
        return check_x, check_y

    def check_b(self, key, player_scale, x, y) -> tuple[np.ndarray, np.ndarray]:
        """
        マップ当たり判定座標計算

        Parameters
        ----------
        key : str
            進むキー
        player_scale : float
            プレイヤーの大きさ
        x : int
            プレイヤー座標x
        y : int
            プレイヤー座標y

        Returns
        ----------
        check_x : np.ndarray
            当たり判定座標x
        check_y : np.ndarray
            当たり判定座標y
        """
        point_n = 10
        check_x = [x for _ in range(point_n)]
        check_y = [y for _ in range(point_n)]
        check_x = np.array(check_x)
        check_y = np.array(check_y)
        # print([check_x[0], check_y[0]],end="\r")
        # 0,0 9,9 17,17 25,25
        if key == "w":
            check_x[0] += 2
            for i in range(1,point_n - 1):
                check_x[i] += 2 + 10 / (point_n - 1) * i * player_scale
            check_y -= (player_scale - 1) * 7
        elif key == "s":
            check_x[0] += 2
            for i in range(1,point_n - 1):
                check_x[i] += 2 + 10 / (point_n - 1) * i * player_scale
            check_y += 12 * player_scale
        elif key == "a":
            check_x -= 2
            for i in range(1,point_n - 1):
                check_y[i] += 12 / (point_n - 2) * i * player_scale
            check_y[point_n - 1] += 12 * player_scale
        elif key == "d":
            for i in range(point_n):
                check_x[i] += 9 * player_scale
            for i in range(1,point_n - 1):
                check_y[i] += 12 / (point_n - 2) * i * player_scale
            check_y[point_n - 1] += 12 * player_scale
        return check_x, check_y

    def cd_check(self, x, y, dx, dy, num, key, scale, coord) -> tuple[bool,str,int]:
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
        coord : list
            タイルマップの座標系

        Returns
        ----------
        Any : bool
            あたっている場合はTrue、そうでない場合はFalse
        Any : str
            あたったブロックのタイプ
        Any : int
            モブに当たった際のモブインデックス
        """
        self.next_x = x + dx
        self.next_y = y + dy
        self.key = key
        if not (pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT) or pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT) or pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_W) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP) or pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.KEY_S) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN)):
            if self.key == "w":
                self.next_y -= self.app.player.walk_speed
            elif self.key == "s":
                self.next_y += self.app.player.walk_speed
            elif self.key == "a":
                self.next_x -= self.app.player.walk_speed
            elif self.key == "d":
                self.next_x += self.app.player.walk_speed
        check_x, check_y = self.check_pos(self.key, self.player_scale, self.next_x, self.next_y, scale, coord)
        pixel_size = 8 * scale
        if self.app.debug_msg:
            pyxel.text(0, 99, f"{check_x}", 0)
            pyxel.text(0, 110, f"{check_y}", 0)
        cd = [i[0] for i in self.collision_data[str(num)]]
        co_3 = coord[3] * scale
        co_4 = coord[4] * scale
        checkb_x,checkb_y = self.check_b(self.key, self.player_scale, self.next_x, self.next_y)
        if 6 <= self.app.now_location <= 8:
            check_x += 3
        elif 9 <= self.app.now_location <= 11:
            check_x += 3
        elif self.app.now_location == 16:
            check_x += 4
        # for x_,y_ in zip(checkb_x,checkb_y):
        #     pyxel.pset(x_,y_,0)
        cd_tf = [list(pyxel.tilemaps[num].pget(check[0] // pixel_size, check[1] // pixel_size)) in cd or not 0 <= b[0] <= 300 or not 0 <= b[1] <= 200 for check,b in zip(zip(check_x, check_y),zip(checkb_x, checkb_y))]
        if True in cd_tf:
            xy_index = cd_tf.index(True)
            try:
                type_ = self.collision_data[str(num)][cd.index(list(pyxel.tilemaps[num].pget(check_x[xy_index] // pixel_size, check_y[xy_index] // pixel_size)))][1]
            except ValueError:
                type_ = ""
            if self.next_x <= 81 and 42 <= self.next_y <= 48 and 9 <= self.app.now_location <= 11:
                return True, "trash", 0
            return True, type_, 0
        else:
            for i,mob in enumerate(self.app.mobs[self.app.now_location - 6]):
                if mob[0].display[0]:
                    mob_x = [mob[0].show[0] - 6 * (self.player_scale - 1) for _ in range(4)]
                    mob_y = [mob[0].show[1] - 8 * (self.player_scale - 1) for _ in range(4)]
                    mob_x[1] += 14 * self.player_scale
                    mob_x[3] += 14 * self.player_scale
                    mob_y[2] += 15 * self.player_scale
                    mob_y[3] += 15 * self.player_scale
                    # for xx, yy in zip(mob_x,mob_y):
                    #     pyxel.pset(xx,yy,0)
                    for x_, y_ in zip(checkb_x, checkb_y):
                        if mob_x[0] <= x_ <= mob_x[1] and mob_y[0] <= y_ <= mob_y[2]:
                            return True, "mob", i
            return False, "" , 0