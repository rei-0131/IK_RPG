import pyxel
import json
import numpy as np

#19x13
class Map:
    def __init__(self):
        with open("assets/map.json",encoding="utf-8") as f:
            self.map_data = json.load(f)
        self.map_x = 19
        self.map_y = 13
        self.cd_blocks = [3,]

    def draw_map(self,num):
        map_ = self.map_data[str(num)]
        for y in range(self.map_y):
            for x in range(self.map_x):
                pyxel.blt(16*x,16*y,1,map_[y][x]*16,0,16,16,0)

    def cd_check(self,x,y,dx,dy,num):
        map_ = self.map_data[str(num)]
        input_array = np.array(map_)
        enlarged_array = np.repeat(np.repeat(input_array, 16, axis=1), 16, axis=0)
        map_16 = enlarged_array.tolist()
        next_x = x + dx + 1
        next_y = y + dy - 2
        if map_16[next_y][next_x] in self.cd_blocks or map_16[next_y+16][next_x] in self.cd_blocks or map_16[next_y][next_x+16] in self.cd_blocks or map_16[next_y+16][next_x+16] in self.cd_blocks:
            return True
        else:
            return False
        # next_x = int((x + dx)/16)
        # next_y = int((y + dy)/16)
        # if map_[next_y][next_x] in self.cd_blocks or map_[next_y+1][next_x] in self.cd_blocks or map_[next_y][next_x+1] in self.cd_blocks or map_[next_y+1][next_x+1] in self.cd_blocks:
        #     return True
        # else:
        #     return False