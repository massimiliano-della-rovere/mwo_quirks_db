"""Test script to extract Mech stats from MWO .pak files"""


import logging
import os
import tempfile


from constants import MWO_DB_FILE
from mwo_mech_quirks_converter import MWOMechQuirksConverter
from mwo_mech_quirks_extractor import MWOMechQuirksExtractor
from mwo_mech_quirks_importer import MWOMechQuirksImporter


def main():
    logging.basicConfig(
        encoding="utf-8",
        level=os.environ.get("LOGLEVEL", "DEBUG"),
        datefmt="%Y-%m-%d %H:%M:%S %z",
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    with tempfile.TemporaryDirectory(prefix="MWOExtractor_") as workdir:
        mech_info = MWOMechQuirksExtractor(workdir=workdir)()
        quirks = MWOMechQuirksConverter(workdir=workdir)(mech_info=mech_info)
    MWOMechQuirksImporter(sqlite_db_name=MWO_DB_FILE)(quirks=quirks)
    print(quirks)


if __name__ == "__main__":
    main()
