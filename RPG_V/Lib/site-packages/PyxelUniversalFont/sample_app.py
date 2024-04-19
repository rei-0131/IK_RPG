import pyxel
import random

from .src import root as puf

class App:
    def __init__(self) -> None:
        self.count = -1
        self.fps = 60
        self.interval = 30
        
        pyxel.init(800, 500, fps=self.fps)
        
        self.writers = puf.get_writers()
        
        self.font_size = 32
        self.font_add = 1
        self.paused = False
        
        pyxel.run(self.update, self.draw)
        
    def update(self):
        self.count += 1
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.paused = not self.paused
        
        if not self.paused and self.count%self.interval==0:
            if self.font_size >= 48 or self.font_size <= 16:
                self.font_add *= -1
            self.font_size += self.font_add
            self.font_color, self.background_color = random.sample(range(16), 2)
    
    def draw(self):
        if not self.paused and self.count%self.interval==0:
            pyxel.cls(self.background_color)
            
            text_list = [
                "現在の設定は、",
                f"文字の大きさが{self.font_size}、",
                f"文字の色が{self.font_color}番、",
                f"背景の色が{self.background_color}番です！",
                f"設定を見たい場合は、",
                f"スペースキーを押すと",
                f"一時停止できます！！！",
                f"フォントが追加されました〜",
                f"もう一つ追加でお得情報？",
                f"文字/背景の色に-1を設定すると、",
                f"透明にできる！！",
            ]
            
            for i, (font_name, writer) in enumerate(self.writers.items()):
                font_name = font_name.split(".")[0]
                writer.draw(
                    x = 0,
                    y = i*(self.font_size+2),
                    text = f"({font_name})" + text_list[i],
                    font_size = self.font_size,
                    font_color = self.font_color,
                    background_color = self.background_color,
                )

def start_app():
    App()

if __name__ == "__main__": 
    start_app()