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
    """
    def __init__(self,x,y,ump):
        self.init_x = x
        self.init_y = y
        self.username = "ぼく"
        self.umplus10 = ump
        self.user_data = {"ぼく":{"HP":[230,180],"MP":[140,130]},"アラオ":{"HP":[340,320],"MP":[120,30]},"アラオ2":{"HP":[230,230],"MP":[270,150]},"アラオ3":{"HP":[170,10],"MP":[560,430]}}
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
        for i,data in zip(range(1,1+len(self.user_data.items())),self.user_data):
            self.umplus10.draw_text(115,self.init_y//2+15+18*(i - 1),data,7)
            pyxel.text(172,self.init_y//2+14+18*(i - 1),"HP",7)
            pyxel.text(172,self.init_y//2+21+18*(i - 1),"MP",7)
            pyxel.rect(180,self.init_y//2+14+18*(i - 1),(self.user_data[data]["HP"][1]/self.user_data[data]["HP"][0])*100,5,11)
            pyxel.rectb(180,self.init_y//2+14+18*(i - 1),100,5,7)
            pyxel.text(281,self.init_y//2+14+18*(i - 1),f"{self.user_data[data]['HP'][1]}",11)
            pyxel.rect(180,self.init_y//2+21+18*(i - 1),(self.user_data[data]["MP"][1]/self.user_data[data]["MP"][0])*100,5,5)
            pyxel.rectb(180,self.init_y//2+21+18*(i - 1),100,5,7)
            pyxel.text(281,self.init_y//2+21+18*(i - 1),f"{self.user_data[data]['MP'][1]}",5)
        if self.select_num == 0:
            self.umplus10.draw_text(26,self.init_y//2+15,"たたかう",7)
            self.umplus10.draw_text(26,self.init_y//2+35,"まほう",7)
            self.umplus10.draw_text(26,self.init_y//2+55,"どうぐ",7)
            self.umplus10.draw_text(26,self.init_y//2+75,"にげる",7)
            pyxel.blt(7,self.init_y//2+15+(self.finger_pos),0,16,0,16,16,0)
        elif self.select_num == 1:
            pass