## コマンド一覧

- /hp
- /mp
- /give

## 構文

- /hp (set or add or sub) chara_index value
- /mp (set or add or sub) chara_index value
- /give type(basic or important or equips("head","armor","leggings","boots","sword","shield","staff","other")) code (num)

## 使用例

- /hp add 0 50
- /mp sub 3 70
- /give basic 001 5
- /give leggings 005

## 注意

**web 版では@が打てないため 0 + Shift で対応**

/hp と/mp に関しては対象設定で@a が使える

- /hp add @a 500

## その他

**give の code と type は src/assets/tools.json を参照**
