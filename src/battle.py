import pyxel

#バトル画面の表示と処理
class Battle:
    """
    バトルに関するクラス

    Parameters:
    x :int
        画面の大きさx
    y : int
        画面の大きさy
    ump : Any
        umplus10(日本語出力)
    app : Any
        Appクラスのインスタンス
    """
    def __init__(self,x,y,ump,app):
        self.init_x = x
        self.init_y = y
        self.username = "ぼく"
        self.umplus10 = ump
        self.chara_data = app.chara_data
        self.select_num = 0
        self.finger_pos = 0

    def update(self):
        if pyxel.btnp(pyxel.KEY_UP):
            if self.finger_pos != 0:
                self.finger_pos -= 20
        if pyxel.btnp(pyxel.KEY_DOWN):
            if self.finger_pos != 60:
                self.finger_pos += 20

    def draw(self):
        pyxel.cls(0)
        pyxel.rect(25,self.init_y//2+10,75,75,0)
        pyxel.rectb(25,self.init_y//2+10,75,75,7)
        pyxel.rect(30,self.init_y//2+10,65,4,0)
        pyxel.rect(110,self.init_y//2+10,185,75,0)
        pyxel.rectb(110,self.init_y//2+10,185,75,7)
        for i,data in zip(range(1,1+len(self.chara_data.items())),self.chara_data):
            height = 18*(i - 1)
            self.umplus10.draw_text(115,self.init_y//2+15+height,data,7)
            pyxel.text(172,self.init_y//2+14+height,"HP",7)
            pyxel.text(172,self.init_y//2+21+height,"MP",7)
            pyxel.rect(180,self.init_y//2+14+height,(self.chara_data[data]["HP"][1]/self.chara_data[data]["HP"][0])*100,5,11)
            pyxel.rectb(180,self.init_y//2+14+height,100,5,7)
            pyxel.text(281,self.init_y//2+14+height,f"{self.chara_data[data]['HP'][1]}",11)
            pyxel.rect(180,self.init_y//2+21+height,(self.chara_data[data]["MP"][1]/self.chara_data[data]["MP"][0])*100,5,5)
            pyxel.rectb(180,self.init_y//2+21+height,100,5,7)
            pyxel.text(281,self.init_y//2+21+height,f"{self.chara_data[data]['MP'][1]}",5)
        if self.select_num == 0:
            self.umplus10.draw_text(26,self.init_y//2+15,"たたかう",7)
            self.umplus10.draw_text(26,self.init_y//2+35,"まほう",7)
            self.umplus10.draw_text(26,self.init_y//2+55,"どうぐ",7)
            self.umplus10.draw_text(26,self.init_y//2+75,"にげる",7)
            pyxel.blt(7,self.init_y//2+15+(self.finger_pos),0,16,0,16,16,0)
        elif self.select_num == 1:
            pass