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

echo アプリ実行エイリアスを削除します。
if exist "C:\Users\%USERNAME%\AppData\Local\Microsoft\WindowsApps\python.exe" (
	echo python.exeを削除...
	del "C:\Users\%USERNAME%\AppData\Local\Microsoft\WindowsApps\python.exe"
)
if exist "C:\Users\%USERNAME%\AppData\Local\Microsoft\WindowsApps\python3.exe" (
	echo python3.exeを削除...
	del "C:\Users\%USERNAME%\AppData\Local\Microsoft\WindowsApps\python3.exe"
)

echo RPGを起動しています...
call RPG_V\Scripts\Activate
python -u "src/main.py"

PAUSE