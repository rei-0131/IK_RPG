import pyxel


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

    def cd_check(self, x, y, dx, dy, num, key, scale, gap_x = 0,gap_y = 0) -> tuple[bool,str]:
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
        scale : float
            表示しているタイルマップのスケール

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
        check_x = [self.next_x - (self.init_x // 2 * (1 - scale) + (gap_x * scale)) for _ in range(3)]
        check_y = [self.next_y - (self.init_y // 2 * (1 - scale) + (gap_y * scale)) for _ in range(3)]
        print([check_x[0], check_y[0]],end="\r")
        if self.key == "w":
            check_x[0] += 2
            check_x[1] += 7
            check_x[2] += 12
        elif self.key == "s":
            check_x[0] += 2
            check_x[1] += 7
            check_x[2] += 12
            check_y[0] += 14
            check_y[1] += 14
            check_y[2] += 14
        elif self.key == "a":
            check_y[0] += 3
            check_y[1] += 8
            check_y[2] += 13
        elif self.key == "d":
            check_x[0] += 12
            check_x[1] += 12
            check_x[2] += 12
            check_y[0] += 3
            check_y[1] += 8
            check_y[2] += 13
        pixel_size = 8 * scale
        pyxel.text(0,99,f"cd_block1{str(list(pyxel.tilemaps[num].pget(check_x[0]//pixel_size, check_y[0]//pixel_size)))}",7)
        pyxel.text(0,110,f"cd_block2{str(list(pyxel.tilemaps[num].pget(check_x[1]//pixel_size, check_y[1]//pixel_size)))}",7)
        pyxel.text(0,121,f"cd_block3{str(list(pyxel.tilemaps[num].pget(check_x[2]//pixel_size, check_y[2]//pixel_size)))}",7)
        pyxel.text(0, 132, f"{check_x}", 7)
        pyxel.text(0, 143, f"{check_y}", 7)
        cd = [i[0] for i in self.collision_data[str(num)]]
        if (list(pyxel.tilemaps[num].pget(check_x[0] // pixel_size, check_y[0] // pixel_size)) not in cd
            and list(pyxel.tilemaps[num].pget(check_x[1] // pixel_size, check_y[1] // pixel_size)) not in cd
            and list(pyxel.tilemaps[num].pget(check_x[2] // pixel_size, check_y[2] // pixel_size)) not in cd):
            return False,""
        else:
            type_ = ""
            if list(pyxel.tilemaps[num].pget(check_x[0] // pixel_size, check_y[0] // pixel_size)) in cd:
                type_ = self.collision_data[str(num)][cd.index(list(pyxel.tilemaps[num].pget(check_x[0] // pixel_size, check_y[0] // pixel_size)))][1]
            elif list(pyxel.tilemaps[num].pget(check_x[1] // pixel_size, check_y[1] // pixel_size)) in cd:
                type_ = self.collision_data[str(num)][cd.index(list(pyxel.tilemaps[num].pget(check_x[1] // pixel_size, check_y[1] // pixel_size)))][1]
            elif list(pyxel.tilemaps[num].pget(check_x[2] // pixel_size, check_y[2] // pixel_size)) in cd:
                type_ = self.collision_data[str(num)][cd.index(list(pyxel.tilemaps[num].pget(check_x[2] // pixel_size, check_y[2] // pixel_size)))][1]
            return True,type_

    def cd_debug(self):
        """
        当たり判定のデバッグ
        現在のフレームの当たり判定の場所を表示
        """
        if self.key == "w":
            pyxel.line(self.next_x + 2, self.next_y, self.next_x + 2, self.next_y, 0)
            pyxel.line(self.next_x + 8, self.next_y, self.next_x + 8, self.next_y, 0)
            pyxel.line(self.next_x + 16 - 4, self.next_y, self.next_x + 16 - 4, self.next_y, 0)
        elif self.key == "s":
            pyxel.line(self.next_x + 2, self.next_y + 14, self.next_x + 2, self.next_y + 14, 0)
            pyxel.line(self.next_x + 8, self.next_y + 14, self.next_x + 8, self.next_y + 14, 0)
            pyxel.line(self.next_x + 16 - 2,self.next_y + 14,self.next_x + 16 - 2,self.next_y + 14,0)
        elif self.key == "a":
            pyxel.line(self.next_x, self.next_y + 3, self.next_x, self.next_y + 3, 0)
            pyxel.line(self.next_x, self.next_y + 8, self.next_x, self.next_y + 8, 0)
            pyxel.line(self.next_x, self.next_y + 16 - 3, self.next_x, self.next_y + 16 - 3, 0)
        elif self.key == "d":
            pyxel.line(self.next_x + 12, self.next_y + 3, self.next_x + 12, self.next_y + 3, 0)
            pyxel.line(self.next_x + 12, self.next_y + 8, self.next_x + 12, self.next_y + 8, 0)
            pyxel.line(self.next_x + 12,self.next_y + 16 - 3,self.next_x + 12,self.next_y + 16 - 3,0)
