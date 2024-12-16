import json
import sys
import os

exefile = False

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

if exefile:
    scenes = json.load(open(resource_path("scenes.json"),"r",encoding="utf-8"))
else:
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
CLASS3_SCENE = scenes["code"]["CLASS3_SCENE"]
STAFF_I_SCENE = scenes["code"]["STAFF_I_SCENE"]
STAFF_M_SCENE = scenes["code"]["STAFF_M_SCENE"]
STAFF_E_SCENE = scenes["code"]["STAFF_E_SCENE"]
WAY_SCENE_12 = scenes["code"]["WAY_SCENE_12"]
WAY_SCENE_31 = scenes["code"]["WAY_SCENE_31"]
WAY_SCENE_I = scenes["code"]["WAY_SCENE_I"]
WAY_SCENE_E = scenes["code"]["WAY_SCENE_E"]
MACHINE_SCENE = scenes["code"]["MACHINE_SCENE"]