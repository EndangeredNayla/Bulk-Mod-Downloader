@echo off
rmdir bin /s /q
pyinstaller --onefile --icon=icon.ico --noupx main.py
REN dist bin
cd bin && REN main.exe MCHDL.exe && cd ..
PAUSE