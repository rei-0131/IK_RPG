@echo off

chcp 65001

cd %~dp0
if not exist RPG_V (
	echo RPG_V.zipを解凍しています...
	tar -xf RPG_V.zip -C %~dp0
	echo RPG_V.zipの解凍が完了しました。
	del RPG_V.zip
	echo RPG_V.zipの削除が完了しました。
)

echo RPGを起動しています...
call RPG_V\Scripts\Activate
python -u "src/main.py"

PAUSE