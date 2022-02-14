# mwo_quirks_db
Extract the MWO mech quirks into a SQLite DB


It's an early pre alpha-release.
I'll add command-line options in the next push.

If necessary change the PROGRAM_FILES_DIR constant in constants.py, then run (python3.10+ only) the mwo_quirks_export.py file.
```python3.10 mwo_quirks_export.py```
The SQLite DB will be created in ~/.local/mwo on Linux and %LOCALAPPDATA%\mwo on Windows.

I have no knowledge if the game runs on MacOS and how MacOS call its equivalent of constants.py#PROGRAM_FILES_DIR and constants.py#LOCAL_DIR.
