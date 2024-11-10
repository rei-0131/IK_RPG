import pyxel

class Mob:
    def __init__(self,app,data,info,scale,name):
        self.app = app
        self.data = data
        self.info = info
        self.show = self.info[1]
        self.scale = scale
        self.name = name
        self.display = True

    def update(self):
        disp = [False,-1]
        for i,info in enumerate(self.info[3]):
            if info[0] <= int(self.app.disp_id) <= info[1]:
                disp = [True,i]
        self.display = disp

        if self.app.now_location == 6:
            pass
        elif self.app.now_location == 7:
            pass
        elif self.app.now_location == 8:
            pass
        elif self.app.now_location == 9:
            if self.app.story_flags["ryoga_group"] and self.name == "リョウガ":
                self.display = [False,-1]

    def draw(self):
        if self.display[0]:
            pyxel.blt(self.show[0],self.show[1],self.data[0],self.data[1],self.data[2],self.data[3] * self.info[3],self.data[4],self.data[5],scale=self.scale)