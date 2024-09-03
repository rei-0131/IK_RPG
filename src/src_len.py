def count_lines_chars(filename):
    lines = 0
    chars = 0
    with open(filename, 'r',encoding="utf-8_sig") as f:
        for line in f:
            lines += 1
            chars += len(line)
    return lines, chars


filenames = [
    'src/battle.py',
    'src/cloud_data.py',
    'src/main.py',
    'src/Map.py',
    'src/option.py',
    'src/player.py',
    'src/words.py',
    'src/save_load.py',
    'src/save.py',
    'src/save.py',
    'src/setting.py',
    'src/title.py',
    'src/assets/magic.json',
    'src/assets/map.json',
    'src/assets/scenes.json',
    'src/assets/tools.json',
    'src/assets/words.json',
    'src/assets/init_data.json',
    'src/configs/config.ini',
    "src/assets/enemy_info.json"]

all_line = 0
all_char = 0

for filename in filenames:
    lines, chars = count_lines_chars(filename)
    print(f'"{filename}" の行数: {lines}\t文字数: {chars}')
    all_line += lines
    all_char += chars

print(f"全てのファイルの行数: {all_line}\t文字数: {all_char}")
