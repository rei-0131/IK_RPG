import pyxel
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn import svm
from sklearn.decomposition import PCA

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
        self.username = "ぼく"
        self.umplus10 = ump
        self.select_num1 = -1
        self.finger_pos1 = 0
        self.select_num2 = -1
        self.finger_pos2 = 0
        self.AI = self.create_AI("")

    def create_AI(self,add_data):
        #first_aiに入っているデータはセットアップデータ
        #continueではfirst_ai+プレイヤーから取得した学習データを使用
        data = []
        ai_answer =[]
        with open("src/rpg_parameters.txt","r",encoding="utf-8") as f:
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
                for i in range(4-en_):
                    ai_data_[tmp_len - 1].append([0,0,0])
                for i in range(3):
                    ai_data_[tmp_len - 1].append([0,0,0])
                c = tmp[tmp_len_ - 3]
                c = [0,0,c]
                ai_data_[tmp_len - 1].append(c)
                d = tmp[tmp_len_ - 1]
                nd_ = np.array([])
                ai_data_[tmp_len - 1] = np.append(nd_,ai_data_[tmp_len-1]).tolist()
                ai_answer.append(d)

        if add_data != "":
            for line in f:
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
                for i in range(4-en_):
                    ai_data_[tmp_len - 1].append([0,0,0])
                for i in range(3):
                    ai_data_[tmp_len - 1].append([0,0,0])
                c = tmp[tmp_len_ - 3]
                c = [0,0,c]
                ai_data_[tmp_len - 1].append(c)
                d = tmp[tmp_len_ - 1]
                nd_ = np.array([])
                ai_data_[tmp_len - 1] = np.append(nd_,ai_data_[tmp_len-1]).tolist()
                ai_answer.append(d)

        data = np.array(ai_data_)
        data_answer = np.array(ai_answer)

        pca = PCA(n_components = 3, whiten = False)
        pca.fit(data)
        data = pca.fit_transform(data)
        scaler = StandardScaler()
        data = scaler.fit_transform(data)

        clf = svm.LinearSVC()
        clf.fit(data ,data_answer)

        return clf

    def fight_update(self):
        if pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
            self.select_num2 = -1

    def magic_update(self):
        if pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
            self.select_num2 = -1

    def item_update(self):
        if pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
            self.select_num1 = -1

    def update(self):
        if self.select_num1 == -1:
            if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
                if self.finger_pos1 != 0:
                    self.finger_pos1 -= 20
            if pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
                if self.finger_pos1 != 60:
                    self.finger_pos1 += 20
            if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B) or pyxel.btnp(pyxel.KEY_RIGHT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
                self.select_num1 = int(self.finger_pos1 // 20)
                self.select_num2 = -1
                print(self.select_num1)
        elif self.select_num1 != 3:
            if self.select_num2 == -1:
                if self.select_num1 == 0 or self.select_num1 == 1:
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
                        print(self.select_num2)
                elif self.select_num1 == 2:
                    self.item_update()
            else:
                if self.select_num1 == 0:
                    self.fight_update()
                elif self.select_num1 == 1:
                    self.magic_update()

    def fight_draw(self):
        pyxel.rect(110,self.init_y//2+10,185,75,0)
        pyxel.rectb(110,self.init_y//2+10,185,75,7)

    def magic_draw(self):
        pyxel.rect(110,self.init_y//2+10,185,75,0)
        pyxel.rectb(110,self.init_y//2+10,185,75,7)

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
            if self.select_num1 != 0 and self.select_num1 != 1:
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
        self.umplus10.draw_text(26,self.init_y//2+35,"まほう",7)
        self.umplus10.draw_text(26,self.init_y//2+55,"どうぐ",7)
        self.umplus10.draw_text(26,self.init_y//2+75,"にげる",7)
        pyxel.blt(7,self.init_y//2+15+(self.finger_pos1),0,16,0,16,16,0)
        if self.select_num1 == 0:
            pyxel.blt(112,self.init_y//2+15+(self.finger_pos2),0,16,0,16,16,0)
            if self.select_num2 != -1:
                self.fight_draw()
        elif self.select_num1 == 1:
            pyxel.blt(112,self.init_y//2+15+(self.finger_pos2),0,16,0,16,16,0)
            if self.select_num2 != -1:
                self.magic_draw()
        elif self.select_num1 == 2:
            self.item_draw()
        elif self.select_num1 == 3:
            pass