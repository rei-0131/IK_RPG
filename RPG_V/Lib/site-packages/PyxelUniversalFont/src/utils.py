from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os
import importlib.resources as pkg_resources

def list_font_files(directory):
    result = []
    with os.scandir(directory) as it:
        for entry in it:
            if not entry.name.startswith('.') and entry.is_file():
                if entry.name.endswith('.ttf') or entry.name.endswith('.otf'):
                    result.append(entry.name)
    return sorted(result)

def get_pixel_representation(
        text, 
        font_path, 
        font_size,
        font_color=0,
        background_color=7,
        show_image=False,
    ):
    
    try:
        font = ImageFont.truetype(font_path, font_size)
    except OSError:
        print("指定されたフォントやサイズが正しくないか、ファイルが見つかりません。")
        return None
    
    image = Image.new('RGB', (font_size*len(text), font_size), color="white")
    draw = ImageDraw.Draw(image)

    draw.text((0, 0), text, font=font, fill='black')

    pixels = np.array(image.getdata())
    
    pixels = np.where(pixels.sum(axis=-1) < (255*3/2), font_color, background_color)
    pixels = pixels.reshape((font_size, font_size*len(text)))
    
    if show_image:
        image.show()
    
    return pixels

def get_data_path(dir="fonts"):
    if __package__:
        return str(pkg_resources.files('PyxelUniversalFont').joinpath(dir))
    else:
        return dir

if __name__ == "__main__":
    get_pixel_representation(
        text="テスト/試験運用",
        font_path="fonts/IPA_Gothic.ttf",
        font_size=48,
        show_image=True
    )