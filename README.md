## IK RPG
2DRPG

[**現段階のmasterをプレイ**](https://tops-desired-hog.ngrok-free.app/IK_RPG)

## 使用モジュール
* pyxel
* configparser
* json
* time
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
- [ ] 設定画面
- - [ ] キャラクタを選択した際
- - - [ ] スキル 
- - - [ ] アイテム一覧
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
          "Level":Level,    
          "HP":[MAX_HP,NOW_HP],     
          "MP":[MAX_MP,NOW_MP],
          "magic_codes":{
            "magic_code"
          }          
        },        
      }      
    }   
  }
}
```

|    表記    |       意味                  |
|:----------:|:---------------------------:|
|data_number |データ番号        　　　　　　 |
|play_time   |プレイ時間        　　　　　　 |
|scene_number|シーン番号        　　　　　　 |
|player_x    |プレイヤーの座標x              |
|player_y    |プレイヤーの座標y  　　　　　　 |
|chara_name  |キャラクターの名前 　　　　　　 |
|Level       |キャラクターのレベル　　　　　　|
|MAX_HP      |最大HP           　　　　　　  |
|NOW_HP      |今のHP           　　　　　　  |
|MAX_MP      |最大MP          　　　　　　   |
|NOW_MP      |今のMP            　　　　　　 |
|magic_code  |magic.jsonに記述された魔法コード|
