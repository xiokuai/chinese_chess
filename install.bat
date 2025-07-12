@echo off
pyinstaller -F chinese_chess\main.py -n chinese_chess --icon=chinese_chess\logo.ico --uac-admin
xcopy chinese_chess\audio dist\audio /E /I /H /Y
xcopy chinese_chess\audio dist\data /E /I /H /Y
copy x64\Release\alpha_beta_search.dll dist
copy logo.ico dist
pause