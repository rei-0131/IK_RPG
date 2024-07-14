## IK RPG
2DRPG

[**現段階のmasterをプレイ**](https://tops-desired-hog.ngrok-free.app/IK_RPG)

## 使用モジュール
* pyxel
* configparser
* json
* time
* random
* BDFRenderer
* js
* pyodide.http
* urllib.request
* os
* scikit-learn

## 進捗
- [ ] メイン画面
- - [ ] マスとマスの間の線で止まれないようにする(正規のマップができたら)
- [x] タイトル画面
- - [x] ニューゲーム処理
- - [x] コンティニュー処理
- [x] 詳細設定にアクセス
- [x] 設定画面
- - [x] キャラクタを選択した際
- - - [x] 魔法
- - - [x] スキル
- - [x] アイテム一覧
- - [ ] 詳細設定
- - - [x] 音量調節(0 ~ 7)
- - [x] セーブデータ一覧(20個ほど?)
- - [x] チーム並び替え
- - [x] ゲーム終了
- [x] 質問機能
- [x] セーブ・ロード
- [ ] 戦闘画面
- - [ ] たたかう
- - [ ] まほう
- - [ ] どうぐ
- - [ ] にげる
- - [x] 敵AI
- [ ] セーブデータで何を保存するかの設定

. . . . . **今後も追加予定**

## セーブデータのフォーマット
```rb
{
  data_number:{
    "player_data":{
      "time":play_time,
      "scene":scene_number,
      "x":player_x,
      "y":player_y,
      "chara_data":{
        chara_name:{
          "post":post_num
          "Level":Level,
          "XP":XP,
          "HP":[MAX_HP,NOW_HP],
          "MP":[MAX_MP,NOW_MP],
          "magic_codes":[magic_code,...],
          "skill_codes":[skill_code,...],
          "atk_ab":atk_ab,
          "def_ab":def_ab,
          "satisfaction":[rate,damage],
          "atk_buff":atk_buff,
          "def_buff":def_buff,
          "equipments":{
            "head":equipment_head_code,
            "armor":equipment_armor_code,
            "leggings":equipment_leggings_code,
            "boots":equipment_boots_code
          }
        },
      },
      "item_codes":{
        item_code:item_num
      },
      "imp_item_codes":[imp_item_code],
      "equip_codes":{
        "head":[head_code,...],
        "armor":[armor_code,...],
        "leggings":[leggings_code,...],
        "boots":[boots_code,...],
        "sword":[sword_code,...],
        "shield":[shield_code,...],
        "staff":[staff_code,...],
        "other":[other_code,...]
      }
    }
  }
}
```

|    表記    |               意味                  |
|:----------:|:-----------------------------------:|
|data_number  |データ番号     　　　　   　　　　　　 |
|play_time    |プレイ時間        　　　　　　　　　　 |
|scene_number |シーン番号        　　　　　　　　　　 |
|player_x     |プレイヤーの座標x           　　　　   |
|player_y     |プレイヤーの座標y  　　　　　　　　　　 |
|chara_name   |キャラクターの名前 　　　　　　　　　　 |
|post_num     |職業コード                           |
|Level        |キャラクターのレベル　　　　　　　　　　|
|XP           |獲得XP量                             |
|MAX_HP       |最大HP           　　　　　　　　　　  |
|NOW_HP       |今のHP           　　　　　　　　　　  |
|MAX_MP       |最大MP          　　　　　　　　　　   |
|NOW_MP       |今のMP            　　　　　　　　　　 |
|magic_code   |magic.jsonに記述された魔法コード　　　　|
|skill_code   |magic.jsonに記述されたスキルコード　　　|
|item_code    |tools.jsonに記述された道具コード　　　　|
|imp_item_code|tools.jsonに既出された重要アイテムコード|
|item_num     |アイテムの所持数         　　　　       |
|atk_ab       |攻撃力            　　　　             |
|def_ab      |防御力          　　　　                |
|rate         |会心            　　　　               |
|damage       |会心率                   　　　　       |
|atk_buff     |攻撃力バフ               　　　　       |
|def_buff    |防御力バフ               　　　　        |
|equipment_head_code|頭装備                           |
|equipment_armor_code|胴装備                          |
|equipment_leggings_code|脚装備                       |
|equipment_boots_code|足装備                          |
|head_code    |頭装備の装備コード                      |
|armor_code   |胴装備の装備コード                      |
|leggings_code|脚装備の装備コード                      |
|boots_code   |足装備の装備コード                      |
|sword_code   |剣の装備コード                          |
|shield_code  |盾の装備コード                          |
|staff_code   |杖の装備コード                          |
|other_code   |その他の装備コード                      |
