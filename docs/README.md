## IK RPG

2DRPG

[**現段階の master をプレイ**](https://tops-desired-hog.ngrok-free.app/IK_RPG)

## 使用モジュール

- pyxel
- configparser
- json
- time
- datetime
- tzdata
- js
- pyodide.http
- urllib.request
- os
- scikit-learn
- copy

## 外部

- BDFRenderer
- [pyxel-tracker](https://github.com/shiromofufactory/pyxel-tracker)

## 進捗
ストーリー
- [x] ぼく転入
- [x] 桃井説明
- [ ] アイテム集め
- - [x] うちわへの道
- - [x] ペンライトへの道
- - [ ] タオルへの道
- - [ ] はっぴへの道
- - [ ] 痛バへの道
- [ ] 桃井覚醒
- [ ] ラスボス
- [ ] END

プログラム
- [x] タイトル画面
- - [x] ニューゲーム処理
- - [x] コンティニュー処理
- [x] 詳細設定にアクセス
- [x] 設定画面
- - [x] キャラクタを選択した際
- - - [x] 魔法
- - - [x] スキル
- - [x] アイテム一覧
- - [x] セーブデータ一覧(20 個ほど?)
- - [x] チーム並び替え
- - [x] ゲーム終了
- [x] 質問機能
- [x] セーブ・ロード
- [x] 戦闘画面
- - [x] たたかう
- - [x] まほう
- - [x] どうぐ
- - [x] にげる
- - [x] 敵 AI
- [ ] セーブデータで何を保存するかの設定

. . . . . **今後も追加予定**

## コマンドの使い方

[説明ファイル](https://github.com/rei-0131/IK_RPG/blob/master/docs/command_help.md)

## セーブデータのフォーマット

```rb
{
  data_number:{
    "player_data":{
      "time":play_time,
      "scene":scene_number,
      "words":{
          "msg_id":msg_id,
          "disp_id":disp_id
      },
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
      },
      "story_flags_tf":{
        "story_flag":0 or 1
      },
      "story_flags_co":{
        "story_flag":count
      }
    }
  }
}
```

|          表記           |                   意味                    |
| :---------------------: | :---------------------------------------: |
|       data_number       |                データ番号                 |
|        play_time        |                プレイ時間                 |
|      scene_number       |                シーン番号                 |
|         msg_id          |           表示予定メッセージ ID           |
|         disp_id         |             表示メッセージ ID             |
|        player_x         |            プレイヤーの座標 x             |
|        player_y         |            プレイヤーの座標 y             |
|       chara_name        |            キャラクターの名前             |
|        post_num         |                職業コード                 |
|          Level          |           キャラクターのレベル            |
|           XP            |                獲得 XP 量                 |
|         MAX_HP          |                  最大 HP                  |
|         NOW_HP          |                  今の HP                  |
|         MAX_MP          |                  最大 MP                  |
|         NOW_MP          |                  今の MP                  |
|       magic_code        |     magic.json に記述された魔法コード     |
|       skill_code        |    magic.json に記述されたスキルコード    |
|        item_code        |     tools.json に記述された道具コード     |
|      imp_item_code      | tools.json に既出された重要アイテムコード |
|        item_num         |             アイテムの所持数              |
|         atk_ab          |                  攻撃力                   |
|         def_ab          |                  防御力                   |
|          rate           |                   会心                    |
|         damage          |                  会心率                   |
|        atk_buff         |                攻撃力バフ                 |
|        def_buff         |                防御力バフ                 |
|   equipment_head_code   |                  頭装備                   |
|  equipment_armor_code   |                  胴装備                   |
| equipment_leggings_code |                  脚装備                   |
|  equipment_boots_code   |                  足装備                   |
|        head_code        |            頭装備の装備コード             |
|       armor_code        |            胴装備の装備コード             |
|      leggings_code      |            脚装備の装備コード             |
|       boots_code        |            足装備の装備コード             |
|       sword_code        |              剣の装備コード               |
|       shield_code       |              盾の装備コード               |
|       staff_code        |              杖の装備コード               |
|       other_code        |            その他の装備コード             |
|       story_flag        |            ストーリーフラグ               |
