import pyxel
import utils.rpg_str as rpg_str


class CMD:
    def __init__(self,app,x,y,ump):
        self.app = app
        self.init_x = x
        self.init_y = y
        self.umplus10 = ump
        self.in_str = ""
        self.equips = ["head","armor","leggings","boots","sword","shield","staff","other"]
        self.writing = True
        self.start = True

    def hmp(self,arg):
        #/hp (set or add or sub) index value
        print(self.app.chara_data[list(self.app.chara_data.keys())[int(arg[2])]][arg[0].upper()])
        if arg[1] == "set":
            if arg[2] == "@a":
                for i in self.app.chara_data.keys():
                    self.app.chara_data[i][arg[0].upper()][1] = int(arg[3])
            else:
                self.app.chara_data[list(self.app.chara_data.keys())[int(arg[2])]][arg[0].upper()][1] = int(arg[3])
        elif arg[1] == "add":
            if arg[2] == "@a":
                for i in self.app.chara_data.keys():
                    self.app.chara_data[i][arg[0].upper()][1] += int(arg[3])
            else:
                self.app.chara_data[list(self.app.chara_data.keys())[int(arg[2])]][arg[0].upper()][1] += int(arg[3])
        elif arg[1] == "sub":
            if arg[2] == "@a":
                for i in self.app.chara_data.keys():
                    self.app.chara_data[i][arg[0].upper()][1] -= int(arg[3])
            else:
                self.app.chara_data[list(self.app.chara_data.keys())[int(arg[2])]][arg[0].upper()][1] -= int(arg[3])
        for i in self.app.chara_data.keys():
            if arg[0].upper() == "HP":
                if self.app.chara_data[i]["HP"][1] > self.app.chara_data[i]["HP"][0]:
                    self.app.chara_data[i]["HP"][1] = self.app.chara_data[i]["HP"][0]
            elif arg[0].upper() == "MP":
                if self.app.chara_data[i]["MP"][1] > self.app.chara_data[i]["MP"][0]:
                    self.app.chara_data[i]["MP"][1] = self.app.chara_data[i]["MP"][0]
        print(self.app.chara_data[list(self.app.chara_data.keys())[int(arg[2])]][arg[0].upper()])


    def give(self,arg):
        #/give type code (num)
        if arg[1] == "basic":
            print(self.app.item_codes)
            if arg[2] in self.app.item_codes.keys():
                self.app.item_codes[arg[2]]["value"] += int(arg[3])
            else:
                self.app.item_codes[arg[2]] = {
                    "value": int(arg[3]),
                    "battle":self.app.tools[arg[1]][arg[2]]["battle"]
                }
            print(self.app.item_codes)
        elif arg[1] == "important":
            print(self.app.imp_item_codes)
            if arg[2] not in self.app.imp_item_codes:
                self.app.imp_item_codes.append(arg[2])
            print(self.app.imp_item_codes)
        elif arg[1] in self.equips:
            print(self.app.equip_codes)
            self.app.equip_codes[arg[1]].append(arg[2])
            print(self.app.equip_codes)

    def update(self):
        if pyxel.btnp(pyxel.KEY_RETURN):
            print(self.in_str)
            cmd_config = self.in_str.split()
            if cmd_config[0][0] == "/":
                cmd_config[0] = cmd_config[0][1:]
                if cmd_config[0] == "hp" or cmd_config[0] == "mp":
                    self.hmp(cmd_config)
                elif cmd_config[0] == "give":
                    self.give(cmd_config)
            self.in_str = ""
        else:
            tmp = rpg_str.get_str()
            if tmp != None:
                if tmp == "back":
                    self.in_str = self.in_str[:len(self.in_str) - 1]
                else:
                    self.in_str += tmp
            if self.start:
                self.in_str = ""
                self.start = False

    def draw(self):
        pyxel.rect(5,self.init_y-30,self.init_x-10,30,0)
        pyxel.rectb(5,self.init_y-30,self.init_x-10,30,7)
        if len(self.in_str) > 40:
            for i,j in zip(range(0,len(self.in_str),40),range(5)):
                self.umplus10.draw_text(6,self.init_y-29+11*j,self.in_str[i:i + 40],7)
        else:
            self.umplus10.draw_text(6,self.init_y-29,self.in_str,7)