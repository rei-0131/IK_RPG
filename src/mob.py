import pyxel

class Mob:
    def __init__(self,app,data,show,scale,name):
        self.app = app
        self.data = data
        self.show = show
        self.scale = scale
        self.name = name
        self.display = True

    def update(self):
        if self.app.now_location == 6:
            pass
        elif self.app.now_location == 7:
            pass
        elif self.app.now_location == 8:
            if self.app.story_flags["ryoga_group"] and self.name == "リョウガ":
                self.display = False

    def draw(self):
        if self.display:
            pyxel.blt(self.show[0],self.show[1],self.data[0],self.data[1],self.data[2],self.data[3],self.data[4],self.data[5],scale=self.scale)