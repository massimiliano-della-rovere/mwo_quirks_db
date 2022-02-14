import os
import pathlib
import platform


match platform.system():
    case "Linux":
        PROGRAM_FILES_DIR = pathlib.Path("/media/data/Program Files (x86)")
        LOCAL_DIR = pathlib.Path(os.path.expanduser("~/.local"))
    case "Windows":
        PROGRAM_FILES_DIR = pathlib.Path("C:\\Program Files (x86)")
        LOCAL_DIR = pathlib.Path(os.path.expandvars("%LOCALAPPDATA%"))
    case "Darwin":
        raise NotImplementedError
    case _:
        raise NotImplementedError


MWO_DIR_NAME = pathlib.Path("MechWarrior Online")
STEAM_DIR = PROGRAM_FILES_DIR / "Steam"
MWO_STEAM_DIR = STEAM_DIR / "steamapps" / "common" / MWO_DIR_NAME
MWO_STANDALONE_DIR = PROGRAM_FILES_DIR / MWO_DIR_NAME

if STEAM_DIR.exists() and MWO_STEAM_DIR.exists():
    MWO_DIR = MWO_STEAM_DIR
elif MWO_STANDALONE_DIR.exists():
    MWO_DIR = MWO_STANDALONE_DIR
else:
    raise FileNotFoundError("MWO install directory")

MWO_MECHS_ARCHIVES_DIR = MWO_DIR / "Game" / "mechs"
MECH_ARCHIVE_FILE_SUFFIXES = (".pak",)
MECH_DATA_FILE_SUFFIXES = (".mdf", ".xml")
OMNIPODS_FILENAME_TEMPLATE = "{mech_name}-omnipods.xml"


MWO_DB_DIR = LOCAL_DIR / "mwo"
MWO_DB_FILE = MWO_DB_DIR / "mech_quirks.db"
