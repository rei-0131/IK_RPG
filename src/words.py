import pyxel
import json

class Words:
    def __init__(self,app,x,y,umplus10):
        self.app = app
        self.init_x = x
        self.init_y = y
        self.umplus10 = umplus10
        self.msg_id = ""
        self.disp_id = ""
        self.word = {}
        self.questions = {}
        with open("assets/words.json",encoding="utf-8") as f:
            self.words = json.load(f)

    def update(self):
        if self.question["exist"] != False:
            pass
        else:
            if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
                if self.word["to"] != "None":
                    self.msg_id = self.word["to"]
                else:
                    self.disp_id = self.msg_id

        return self.msg_id, self.disp_id

    def dec_word(self,msg_id):
        self.msg_id = msg_id
        self.word = self.words["words"][msg_id]
        self.question = self.word["question"]
        pyxel.rect(5,self.init_y-60,self.init_x-10,55,0)
        pyxel.rectb(5,self.init_y-60,self.init_x-10,55,7)
        pyxel.rect(5,self.init_y-71,60,12,0)
        pyxel.rectb(5,self.init_y-71,60,12,7)
        self.umplus10.draw_text(7,self.init_y-70,self.word["speaker"],7)
        if type(self.word["word"]) == str:
            self.umplus10.draw_text(7,self.init_y-59,self.word["word"],7)
        elif type(self.word["word"]) == list:
            for i,n in enumerate(self.word["word"]):
                self.umplus10.draw_text(7,self.init_y-59+i*11,n,7)
        if self.word["to"] != "None":
            pyxel.tri(self.init_x/2-5,self.init_y-12,self.init_x/2+5,self.init_y-12,self.init_x/2,self.init_y-8,7)
        if self.question["exist"]:
            que_height = len(self.question["questions"]) * 11
            pyxel.rect(self.init_x-50,self.init_y-61-que_height,45,que_height+2,0)
            pyxel.rectb(self.init_x-50,self.init_y-61-que_height,45,que_height+2,7)
            for i,h in zip(self.question["questions"],range(0,len(self.question["questions"])*11,11)):
                self.umplus10.draw_text(self.init_x-48,self.init_y-98+h+(39-que_height),i,7)