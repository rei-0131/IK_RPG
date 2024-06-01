import pyxel
import json
import numpy as np
from sklearn.decomposition import PCA
from sklearn.multioutput import MultiOutputRegressor
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler

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
        self.app = app
        self.init_x = x
        self.init_y = y
        self.select_chara = ""
        self.umplus10 = ump
        self.select_num1 = -1
        self.finger_pos1 = 0
        self.select_num2 = -1
        self.finger_pos2 = 0
        self.finger_pos3 = 0
        self.item_num = 0
        self.item_pos = 0
        self.dis_num = 0
        with open("assets/magic.json","r",encoding="utf-8") as f:
            self.magic_codes = json.load(f)
        self.AI = self.create_AI()
        self.ai_data = []

    def create_AI(self):
        #first_aiに入っているデータはセットアップデータ
        #continueではfirst_ai+プレイヤーから取得した学習データを使用
        data = []
        ai_answer =[]
        with open("assets/first_ai.txt","r",encoding="utf-8") as f:
            ai_data_ = []
            for line in f:
                line = line.rstrip()
                tmp = line.split()
                for i in range(len(tmp)):
                    tmp[i] = float(tmp[i])
                ai_data_.append([])

                pl_ = int(tmp[0])
                tmp_len_ = len(tmp)
                tmp_len = len(ai_data_)
                for i in range(pl_):
                    ai_data_[tmp_len - 1].append(tmp[1+i*3:1+(i+1)*3])
                for i in range(4-pl_):
                    ai_data_[tmp_len - 1].append([0,0,0])
                en_ = int(tmp[int(tmp[0])*3+1])
                for i in range(en_):
                    tm = [0,tmp[(int(tmp[0])*3+2)+i*2],tmp[(int(tmp[0])*3+2)+i*2+1]]
                    ai_data_[tmp_len - 1].append(tm)
                for i in range(3-en_):
                    ai_data_[tmp_len - 1].append([0,0,0])
                c = tmp[tmp_len_ - 3]
                c = [0,0,c]
                ai_data_[tmp_len - 1].append(c)
                d = tmp[tmp_len_ - 2:tmp_len_]
                nd_ = np.array([])
                ai_data_[tmp_len - 1] = np.append(nd_,ai_data_[tmp_len-1]).tolist()
                ai_answer.append(d)

        data = np.array(ai_data_)
        data_answer = np.array(ai_answer)

        pca = PCA(n_components = 20, whiten = False)
        pca.fit(data)
        data = pca.fit_transform(data)
        scaler = StandardScaler()
        data = scaler.fit_transform(data)


        clf = MultiOutputRegressor(MLPClassifier(alpha=0.00001, hidden_layer_sizes=(300,100,300),max_iter=1000,random_state=0,early_stopping=True))
        clf.fit(data , data_answer)

        return clf

    def fight_update(self):
        if pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
            self.select_num2 = -1

    def sm_update(self,sm):
        if pyxel.btnp(pyxel.KEY_A) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
            self.select_num2 = -1
        if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
            if not (self.finger_pos3 == 0 or self.finger_pos3 == 1):
                self.finger_pos3-=2
            elif self.item_pos - 2 >= 0:
                self.item_pos -= 2
        if pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
            if self.finger_pos3 != 8 and self.finger_pos3 != 9:
                if self.finger_pos3 + 2 < self.dis_num:
                    self.finger_pos3 += 2
            else:
                if self.finger_pos3 + self.item_pos + 2 < self.item_num:
                    self.item_pos += 2
                elif self.finger_pos3 + self.item_pos + 2 == self.item_num and self.item_num > 10:
                    self.item_pos += 2
                    self.finger_pos3 -= 1
        if pyxel.btnp(pyxel.KEY_RIGHT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
            if self.finger_pos3 + 1 < self.dis_num:
                self.finger_pos3 += 1
            elif not self.item_pos + 12 <= self.item_num and self.item_pos + 11 <= self.item_num:
                self.finger_pos3 -= 1
                self.item_pos += 2
            elif self.item_pos + 12 <= self.item_num:
                self.item_pos += 2
        if pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
            if self.item_pos != 0:
                if self.finger_pos3 == 0:
                    self.finger_pos3 += 1
                    self.item_pos -= 2
                else:
                    self.finger_pos3 -= 1
            else:
                if self.finger_pos3 != 0:
                    self.finger_pos3 -= 1
        if pyxel.btnp(pyxel.KEY_RETURN):
            #魔法名出力
            print(self.magic_codes[sm][self.app.chara_data[self.select_chara][f"{sm}_codes"][self.item_pos + self.finger_pos3]][0])

    def item_update(self):
        if pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
            self.select_num1 = -1

    def update(self):
        if self.select_num1 == -1:
            if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
                if self.finger_pos1 != 0:
                    self.finger_pos1 -= 15
            if pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
                if self.finger_pos1 != 60:
                    self.finger_pos1 += 15
            if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B) or pyxel.btnp(pyxel.KEY_RIGHT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
                self.select_num1 = int(self.finger_pos1 // 15)
                print(self.select_num1)
                self.select_num2 = -1
        elif self.select_num1 != 4:
            if self.select_num2 == -1:
                if 0 <= self.select_num1 <= 2:
                    if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
                        if self.finger_pos2 != 0:
                            self.finger_pos2 -= 18
                    if pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
                        if self.finger_pos2 != (len(self.app.chara_data.items()) - 1) * 18:
                            self.finger_pos2 += 18
                    if pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
                        self.select_num1 = -1
                    if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B) or pyxel.btnp(pyxel.KEY_RIGHT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
                        self.select_num2 = int(self.finger_pos2 // 18)
                        self.select_chara = list(self.app.chara_data.keys())[self.select_num2]
                        if self.select_num1 == 1:
                            self.finger_pos3 = 0
                            self.item_num = 0
                            self.item_pos = 0
                            self.dis_num = 0
                elif self.select_num1 == 3:
                    self.item_update()
            else:
                if self.select_num1 == 0:
                    self.fight_update()
                elif self.select_num1 == 1:
                    self.sm_update("skill")
                elif self.select_num1 == 2:
                    self.sm_update("magic")
                #self.ai_data.append([])

    def fight_draw(self):
        pyxel.rect(110,self.init_y//2+10,185,75,0)
        pyxel.rectb(110,self.init_y//2+10,185,75,7)

    def sm_draw(self,sm):
        pyxel.rect(110,self.init_y//2+10,185,75,0)
        pyxel.rectb(110,self.init_y//2+10,185,75,7)
        self.umplus10.draw_text(190,self.init_y-12,"※戻るにはAキーを押す",8)
        self.item_num = len(self.app.chara_data[self.select_chara][f"{sm}_codes"])
        if self.item_num >= self.item_pos + 11:
            self.dis_num = 10
            for i,item in zip(range(10),self.app.chara_data[self.select_chara][f"{sm}_codes"][self.item_pos:self.item_pos + 10]):
                h = int(i // 2)
                w = i % 2
                if i == self.finger_pos3:
                    pyxel.rect(111+(w*91),self.init_y//2+11+(h*14.3),92,15,1)
                else:
                    pyxel.rect(111+(w*91),self.init_y//2+11+(h*14.3),92,15,0)
                self.umplus10.draw_text(111+(w*93),self.init_y//2+12+(h*15),self.magic_codes[sm][item][0],7)
        else:
            self.dis_num = self.item_num - self.item_pos
            for i,item in zip(range(self.item_num-self.item_pos),self.app.chara_data[self.select_chara][f"{sm}_codes"][self.item_pos:self.item_num]):
                h = int(i // 2)
                w = i % 2
                if i == self.finger_pos3:
                    pyxel.rect(111+(w*91),self.init_y//2+11+(h*14.3),92,15,1)
                else:
                    pyxel.rect(111+(w*91),self.init_y//2+11+(h*14.3),92,15,0)
                self.umplus10.draw_text(111+(w*93),self.init_y//2+12+(h*15),self.magic_codes[sm][item][0],7)

    def item_draw(self):
        pyxel.rect(110,self.init_y//2+10,185,75,0)
        pyxel.rectb(110,self.init_y//2+10,185,75,7)

    def draw(self):
        pyxel.cls(0)
        pyxel.rect(25,self.init_y//2+10,75,75,0)
        pyxel.rectb(25,self.init_y//2+10,75,75,7)
        pyxel.rect(30,self.init_y//2+10,65,4,0)
        pyxel.rect(110,self.init_y//2+10,185,75,0)
        pyxel.rectb(110,self.init_y//2+10,185,75,7)
        for i,data in zip(range(1,1+len(self.app.chara_data.items())),self.app.chara_data):
            height = 18*(i - 1)
            if self.select_num1 != 0 and self.select_num1 != 1 and self.select_num1 != 2:
                self.umplus10.draw_text(115,self.init_y//2+15+height,data,7)
            else:
                self.umplus10.draw_text(130,self.init_y//2+15+height,data,7)
            pyxel.text(172,self.init_y//2+14+height,"HP",7)
            pyxel.text(172,self.init_y//2+21+height,"MP",7)
            pyxel.rect(180,self.init_y//2+14+height,(self.app.chara_data[data]["HP"][1]/self.app.chara_data[data]["HP"][0])*100,5,11)
            pyxel.rectb(180,self.init_y//2+14+height,100,5,7)
            pyxel.text(281,self.init_y//2+14+height,f"{self.app.chara_data[data]['HP'][1]}",11)
            pyxel.rect(180,self.init_y//2+21+height,(self.app.chara_data[data]["MP"][1]/self.app.chara_data[data]["MP"][0])*100,5,5)
            pyxel.rectb(180,self.init_y//2+21+height,100,5,7)
            pyxel.text(281,self.init_y//2+21+height,f"{self.app.chara_data[data]['MP'][1]}",5)
        self.umplus10.draw_text(26,self.init_y//2+15,"たたかう",7)
        self.umplus10.draw_text(26,self.init_y//2+30,"スキル",7)
        self.umplus10.draw_text(26,self.init_y//2+45,"まほう",7)
        self.umplus10.draw_text(26,self.init_y//2+60,"どうぐ",7)
        self.umplus10.draw_text(26,self.init_y//2+75,"にげる",7)
        pyxel.blt(7,self.init_y//2+15+(self.finger_pos1),0,16,0,16,16,0)
        if self.select_num1 == 0:
            pyxel.blt(112,self.init_y//2+15+(self.finger_pos2),0,16,0,16,16,0)
            if self.select_num2 != -1:
                self.fight_draw()
        elif self.select_num1 == 1:
            pyxel.blt(112,self.init_y//2+15+(self.finger_pos2),0,16,0,16,16,0)
            if self.select_num2 != -1:
                self.sm_draw("skill")
        elif self.select_num1 == 2:
            pyxel.blt(112,self.init_y//2+15+(self.finger_pos2),0,16,0,16,16,0)
            if self.select_num2 != -1:
                self.sm_draw("magic")
        elif self.select_num1 == 3:
            self.item_draw()
        elif self.select_num1 == 4:
            pass