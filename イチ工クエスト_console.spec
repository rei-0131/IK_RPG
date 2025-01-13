# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['src\\main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['sklearn.multioutput','sklearn.neural_network'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

a.datas += [
    ('assets_info.json','.\\src\\assets\\assets_info.json','DATA'),
    ('assets.pyxres','.\\src\\assets\\assets.pyxres','DATA'),
    ('b16.bdf','.\\src\\assets\\b16.bdf','DATA'),
    ('b24.bdf','.\\src\\assets\\b24.bdf','DATA'),
    ('character_data.json','.\\src\\assets\\character_data.json','DATA'),
    ('classroom.png','.\\src\\assets\\classroom.png','DATA'),
    ('endroll.json','.\\src\\assets\\endroll.json','DATA'),
    ('enemy_info.json','.\\src\\assets\\enemy_info.json','DATA'),
    ('gamepad_op.png','.\\src\\assets\\gamepad_op.png','DATA'),
    ('init_data.json','.\\src\\assets\\init_data.json','DATA'),
    ('machine.png','.\\src\\assets\\machine.png','DATA'),
    ('magic.json','.\\src\\assets\\magic.json','DATA'),
    ('rpg.aibi','.\\src\\assets\\rpg.aibi','DATA'),
    ('scenes.json','.\\src\\assets\\scenes.json','DATA'),
    ('staffroom.png','.\\src\\assets\\staffroom.png','DATA'),
    ('story_flags.json','.\\src\\assets\\story_flags.json','DATA'),
    ('title_logo.png','.\\src\\assets\\title_logo.png','DATA'),
    ('tools.json','.\\src\\assets\\tools.json','DATA'),
    ('umplus_j10r.bdf','.\\src\\assets\\umplus_j10r.bdf','DATA'),
    ('way.png','.\\src\\assets\\way.png','DATA'),
    ('words.json','.\\src\\assets\\words.json','DATA'),
    ('config.ini','.\\src\\configs\\config.ini','DATA'),
    ('acceptable.json','.\\src\\assets\\sounds\\acceptable.json','DATA'),
    ('give.json','.\\src\\assets\\sounds\\give.json','DATA'),
    ('ok.json','.\\src\\assets\\sounds\\ok.json','DATA'),
    ('select.json','.\\src\\assets\\sounds\\select.json','DATA'),
    ('turn.json','.\\src\\assets\\sounds\\turn.json','DATA'),
    ('winner.json','.\\src\\assets\\sounds\\winner.json','DATA'),
    ('boss.ogg','.\\src\\assets\\sounds\\boss.ogg','DATA'),
    ('last_boss_1.ogg','.\\src\\assets\\sounds\\last_boss_1.ogg','DATA'),
    ('last_boss_2.ogg','.\\src\\assets\\sounds\\last_boss_2.ogg','DATA'),
    ('normal_battle.ogg','.\\src\\assets\\sounds\\normal_battle.ogg','DATA'),
    ('city.ogg','.\\src\\assets\\sounds\\city.ogg','DATA'),
    ('ed.ogg','.\\src\\assets\\sounds\\ed.ogg','DATA'),
    ('op.ogg','.\\src\\assets\\sounds\\op.ogg','DATA'),
    ('last_field.ogg','.\\src\\assets\\sounds\\last_field.ogg','DATA')
]

pyz = PYZ(a.pure)

Key = ['mkl']

def remove_from_list(input, keys):
    outlist = []
    for item in input:
        name, _, _ = item
        flag = 0
        for key_word in keys:
            if name.find(key_word) > -1:
                flag = 1
        if flag != 1:
            outlist.append(item)
    return outlist

a.binaries = remove_from_list(a.binaries, Key)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='イチ工クエスト_console',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['rpg_icon.ico'],
)
