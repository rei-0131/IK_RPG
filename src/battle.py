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
        self.user_data = {"ぼく":{"HP":[100,80],"MP":[100,80]},"アラオ":{"HP":[100,80],"MP":[100,80]},"アラオ2":{"HP":[100,80],"MP":[100,80]},"アラオ3":{"HP":[100,80],"MP":[100,80]}}

    def update(self):
        pass

    def draw(self):
        pyxel.rect(25,self.init_y//2+10,75,75,0)
        pyxel.rectb(25,self.init_y//2+10,75,75,7)
        pyxel.rect(30,self.init_y//2+10,65,4,0)
        pyxel.rect(110,self.init_y//2+10,185,75,0)
        pyxel.rectb(110,self.init_y//2+10,185,75,7)
        for i,data in zip(range(1,1+len(self.user_data.items())),self.user_data):
            self.umplus10.draw_text(115,self.init_y//2+15+18*(i - 1),data,7)
            pyxel.text(182,self.init_y//2+14+18*(i - 1),"HP",7)
            pyxel.text(182,self.init_y//2+21+18*(i - 1),"MP",7)
            pyxel.rect(190,self.init_y//2+16+18*(i - 1),(self.user_data[data]["HP"][1]/self.user_data[data]["HP"][0])*100,3,11)
            pyxel.rectb(190,self.init_y//2+16+18*(i - 1),100,3,7)
            pyxel.rect(190,self.init_y//2+20+18*(i - 1),(self.user_data[data]["MP"][1]/self.user_data[data]["MP"][0])*100,3,5)
            pyxel.rectb(190,self.init_y//2+20+18*(i - 1),100,3,7)