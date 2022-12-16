set "temp_dir=C:\Temp\g\"
xcopy %cd%\g %temp_dir%* /S /Q /Y
start /b "" main.vbs
