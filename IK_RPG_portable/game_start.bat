@echo off

chcp 65001

cd %~dp0

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
python.exe -u "src/main.py"

PAUSE