import pyxel

class Mob:
    def __init__(self,app,data,info,scale,name,index_info):
        self.app = app
        self.data = data
        self.info = info
        self.index_info = index_info
        self.show = self.info[1]
        self.scale = scale
        self.name = name
        self.display = [True,-1]
        self.walk_speed = 1.5
        self.key = ""
        self.x = 0
        self.y = 0
        self.dx = 0
        self.dy = 0
        self.index = 0
        self.walk_pos = 0
        self.walk_pm = "p"
        self.walk_num = 0

    def update(self):
        disp = [False,-1]
        for i,info in enumerate(self.info[3]):
            if self.app.msg_id != None:
                if info[0] <= int(self.app.msg_id) <= info[1] :
                    disp = [True,i]
                elif len(self.info) > 6:
                    if self.info[6] == int(self.app.msg_id):
                        disp = [True,i]
        self.display = disp

        if self.app.now_location == 6:
            pass
        elif self.app.now_location == 7:
            pass
        elif self.app.now_location == 8:
            pass
        elif self.app.now_location == 9:
            if self.app.story_flags_tf["ryoga_group"] and self.name == "リョウガ":
                self.display = [False,-1]
        #[6,[166,80,0,1],98,[[52,115]],115,[[166,105],[305,105]]]
        if len(self.info) > 4:
            if self.app.msg_id == str(self.info[4]):
                self.move_plan = self.info[5]
                if self.show[0] > self.move_plan[self.index][0]:
                    self.dx = - self.walk_speed
                    self.dy = 0
                    self.key = "a"
                elif self.show[0] < self.move_plan[self.index][0]:
                    self.dx = self.walk_speed
                    self.dy = 0
                    self.key = "d"
                elif self.show[1] > self.move_plan[self.index][1]:
                    self.dx = 0
                    self.dy = - self.walk_speed
                    self.key = "w"
                elif self.show[1] < self.move_plan[self.index][1]:
                    self.dx = 0
                    self.dy = self.walk_speed
                    self.key = "s"

                if self.key == "":
                    self.walk_num = 0
                    self.walk_pos = 0
                else:
                    if self.walk_num % 5 == 0:
                        if self.walk_pm == "p":
                            self.walk_pos += 1
                        else:
                            self.walk_pos -= 1
                        self.walk_num = 0
                    if self.walk_pm == "p":
                        if self.walk_pos >= 2:
                            self.walk_pos -= 1
                            self.walk_pm = "m"
                    else:
                        if self.walk_pos <= -2:
                            self.walk_pos += 1
                            self.walk_pm = "p"
                    self.walk_num += 1

                if not self.app.story_animation:
                    self.app.story_animation = True
                    self.x = self.show[0]
                    self.y = self.show[1]
                    self.index = 0
                else:
                    if self.index == len(self.move_plan) - 1:
                        if (self.move_plan[self.index][0] - (self.walk_speed + 1) <= self.x <= self.move_plan[self.index][0] + (self.walk_speed + 1) and
                                self.move_plan[self.index][1] - (self.walk_speed + 1) <= self.y <= self.move_plan[self.index][1] + (self.walk_speed + 1)):
                            self.app.story_animation = False
                            self.x = self.move_plan[self.index][0]
                            self.y = self.move_plan[self.index][1]
                            self.index = 0
                            self.show[0] = self.x
                            self.show[1] = self.y
                            if self.key == "w":
                                self.show[2] = 2
                            elif self.key == "s":
                                self.show[2] = 0
                            elif self.key == "a":
                                self.show[2] = 1
                                self.show[3] = -1
                            elif self.key == "d":
                                self.show[2] = 1
                                self.show[3] = 1
                            self.data = self.app.assets_info["chara"][self.name][self.show[2]]
                            self.x = 0
                            self.y = 0
                            self.dx = 0
                            self.dy = 0
                            self.key = ""
                            self.info = self.info[0:4]
                            print(f"{self.move_plan[self.index]}    {self.move_plan[self.index][0] - (self.walk_speed + 1)} {self.x} {self.move_plan[self.index][0] + (self.walk_speed + 1)}    {self.move_plan[self.index][1] - (self.walk_speed + 1)} {self.y} {self.move_plan[self.index][1] + (self.walk_speed + 1)}")
                        else:
                            self.x += self.dx
                            self.y += self.dy
                    else:
                        if (self.move_plan[self.index][0] - (self.walk_speed + 1) <= self.x <= self.move_plan[self.index][0] + (self.walk_speed + 1) and
                                self.move_plan[self.index][1] - (self.walk_speed + 1) <= self.y <= self.move_plan[self.index][1] + (self.walk_speed + 1)):
                            self.x = self.move_plan[self.index][0]
                            self.y = self.move_plan[self.index][1]
                            self.show[0] = self.x
                            self.show[1] = self.y
                            self.index += 1
                            print(f"{self.move_plan[self.index]}    {self.move_plan[self.index][0] - (self.walk_speed + 1)} {self.x} {self.move_plan[self.index][0] + (self.walk_speed + 1)}    {self.move_plan[self.index][1] - (self.walk_speed + 1)} {self.y} {self.move_plan[self.index][1] + (self.walk_speed + 1)}")
                        else:
                            self.x += self.dx
                            self.y += self.dy

    def draw(self):
        if self.display[0]:
            if not self.app.story_animation:
                pyxel.blt(self.show[0],self.show[1],self.data[0],self.data[1],self.data[2],self.data[3] * self.show[3],self.data[4],self.data[5],scale=self.scale)
            else:
                data = self.app.assets_info["chara"][self.name]
                if self.key == "":
                    pyxel.blt(self.x,self.y,self.data[0],self.data[1],self.data[2],self.data[3] * self.show[3],self.data[4],self.data[5],scale=self.scale)
                elif self.key == "w":
                    if self.walk_pos == -1:
                        pyxel.blt(self.x,self.y,data[2][0],data[2][1] - (self.walk_pos + 2) * 16,data[2][2],data[2][3] * self.show[3],data[2][4],data[2][5],scale=self.scale)
                    else:
                        pyxel.blt(self.x,self.y,data[2][0],data[2][1] - self.walk_pos * 16,data[2][2],data[2][3] * self.show[3],data[2][4],data[2][5],scale=self.scale)
                elif self.key == "s":
                    if self.walk_pos == -1:
                        pyxel.blt(self.x,self.y,data[0][0],data[0][1] - (self.walk_pos + 2) * 16,data[0][2],data[0][3] * self.show[3],data[0][4],data[0][5],scale=self.scale)
                    else:
                        pyxel.blt(self.x,self.y,data[0][0],data[0][1] - self.walk_pos * 16,data[0][2],data[0][3] * self.show[3],data[0][4],data[0][5],scale=self.scale)
                elif self.key == "a":
                    if self.walk_pos == -1:
                        pyxel.blt(self.x,self.y,data[1][0],data[1][1] - (self.walk_pos + 2) * 16,data[1][2],data[1][3] * -1,data[1][4],data[1][5],scale=self.scale)
                    else:
                        pyxel.blt(self.x,self.y,data[1][0],data[1][1] - self.walk_pos * 16,data[1][2],data[1][3] * -1,data[1][4],data[1][5],scale=self.scale)
                elif     self.key == "d":
                    if self.walk_pos == -1:
                        pyxel.blt(self.x,self.y,data[1][0],data[1][1] - (self.walk_pos + 2) * 16,data[1][2],data[1][3],data[1][4],data[1][5],scale=self.scale)
                    else:
                        pyxel.blt(self.x,self.y,data[1][0],data[1][1] - self.walk_pos * 16,data[1][2],data[1][3],data[1][4],data[1][5],scale=self.scale)