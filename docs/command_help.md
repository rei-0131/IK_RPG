## コマンド一覧

- /hp
- /mp
- /xp
- /kill
- /give
- /mode
- /debugmsg
- /battle

## 構文

- /hp (set or add or sub) chara_index value
- /mp (set or add or sub) chara_index value
- /xp chara_index value
- /kill (self or enemy) index
- /give type(basic or important or equips("head","armor","leggings","boots","sword","shield","staff","other")) code (num)
- /mode (init or debug)
- /debugmsg (true or false)
- /battle

## 使用例

- /hp add 0 50
- /mp sub 3 70
- /xp 0 1000
- /kill enemy @a
- /give basic 001 5
- /give leggings 005
- /mode init
- /debugmsg false
- /battle

## 注意

**web 版では@が打てないため 0 + Shift で対応**

/hp と/mp と /killに関しては対象設定で@a が使える

- /hp add @a 500

## その他

**give の code と type は src/assets/tools.json を参照**
