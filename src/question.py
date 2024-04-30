import pyxel
import json
from BDFRenderer import BDFRenderer

with open("assets/words.json",encoding="utf-8") as f:
    words = json.load(f)

class Question:
    def __init__(self,x,y,ump):
        self.question_mark = 0
        self.init_x = x
        self.init_y = y
        self.umplus10 = ump
        self.que_height = 0

    def dec_question(self,msg_dis:int):
        """質問を表示するデコレーション
        質問は1度に4つまで

        Parameters:
        ----------
        msg_dis : int
            表示する文字列のDictionaryのKey
        """

        s = words["questions"][str(msg_dis)]
        self.que_height = len(s) * 9
        pyxel.rect(self.init_x-50,self.init_y-60-self.que_height,45,self.que_height+1,0)
        pyxel.rectb(self.init_x-50,self.init_y-60-self.que_height,45,self.que_height+1,7)
        for i,h in zip(s,range(0,len(s)*9,9)):
            self.umplus10.draw_text(self.init_x-48,self.init_y-97+h+(36-self.que_height),i,7)

    def update(self):
        if pyxel.btnp(pyxel.KEY_DOWN):
            if self.question_mark != -27+(36-self.que_height):
                self.question_mark -= 9
        if pyxel.btnp(pyxel.KEY_UP):
            if self.question_mark != 0:
                self.question_mark += 9
        if pyxel.btnp(pyxel.KEY_RETURN):
            print(self.question_mark/9)

    def draw(self):
        pyxel.blt(self.init_x-67,self.init_y-96-self.question_mark+(36-self.que_height),0,15,0,30,15,0)