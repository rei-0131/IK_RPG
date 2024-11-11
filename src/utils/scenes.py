import json

scenes = json.load(open("src/assets/scenes.json","r",encoding="utf-8"))

START_SCENE = scenes["code"]["START_SCENE"]
TITLE_SCENE = scenes["code"]["TITLE_SCENE"]
MAIN_SCENE = scenes["code"]["MAIN_SCENE"]
IN_SETTING_SCENE = scenes["code"]["IN_SETTING_SCENE"]
OUT_SETTING_SCENE = scenes["code"]["OUT_SETTING_SCENE"]
LOAD_SCENE = scenes["code"]["LOAD_SCENE"]
BATTLE_SCENE = scenes["code"]["BATTLE_SCENE"]
CLASS1_SCENE = scenes["code"]["CLASS1_SCENE"]
CLASS2_SCENE = scenes["code"]["CLASS2_SCENE"]
STAFF_SCENE = scenes["code"]["STAFF_SCENE"]
WAY_SCENE = scenes["code"]["WAY_SCENE"]