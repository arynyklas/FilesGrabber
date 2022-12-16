Dim oShell: Set oShell = CreateObject("WScript.Shell")
oShell.CurrentDirectory = "C:\Temp\g"
oShell.Run "main.exe", 0, True
