@echo off

pyinstaller --onefile --icon=Assets/favicon.ico main.py
ren "dist\main.exe" "unityextract.exe"
move "dist\unityextract.exe" ".\"

rmdir /Q /S dist
rmdir /Q /S build
del main.spec