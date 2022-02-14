import copy
import logging
import os
import pathlib
import typing
import zipfile


from aux_types import MechData, MechInfo
from constants import (
    MWO_MECHS_ARCHIVES_DIR,
    MECH_ARCHIVE_FILE_SUFFIXES, MECH_DATA_FILE_SUFFIXES,
    OMNIPODS_FILENAME_TEMPLATE)


class MWOMechQuirksExtractor:
    def __init__(
            self,
            workdir: str,
            mech_archives_dir: pathlib.Path = MWO_MECHS_ARCHIVES_DIR,
            archive_file_suffixes: tuple[str, ...] = MECH_ARCHIVE_FILE_SUFFIXES,
            data_file_suffixes: tuple[str, ...] = MECH_DATA_FILE_SUFFIXES,
            logger: logging.Logger = None):
        # const
        self._workdir = workdir
        self._mech_archives_dir = mech_archives_dir
        self._archive_file_suffixes = archive_file_suffixes
        self._data_file_suffixes = data_file_suffixes
        self._logger = logger or logging.getLogger(self.__class__.__name__)

        # runtime
        self._mech_info: MechInfo = {}

    @property
    def mech_info(self) -> MechInfo:
        return copy.deepcopy(self._mech_info)

    @staticmethod
    def _omnipods_filename(mech_name: str) -> str:
        return OMNIPODS_FILENAME_TEMPLATE.format(mech_name=mech_name)

    def _find_data_files_in_archive(
            self,
            archive: zipfile.ZipFile,
            archive_path: pathlib.Path) -> tuple[str, ...]:
        files_in_archive = archive.infolist()
        omnipods_filename = self._omnipods_filename(mech_name=archive_path.stem)
        for zip_info in files_in_archive:
            if zip_info.filename.endswith(omnipods_filename):
                return zip_info.filename,
        else:
            return tuple(
                filename
                for zip_info in files_in_archive
                if os.path.splitext(filename := zip_info.filename)[1] == ".mdf")

    def _store_mech_data(self,
                         archive_path: pathlib.Path,
                         extracted_files: tuple[str, ...]) -> None:
        mech_name = archive_path.stem
        omnipods_filename = self._omnipods_filename(mech_name)
        self._mech_info[archive_path.name] = MechData(
            archive_path=archive_path,
            mech_name=mech_name,
            files=tuple(
                pathlib.Path(self._workdir) / extracted_file
                for extracted_file in extracted_files),
            has_omnipods=any(
                filename.endswith(omnipods_filename)
                for filename in extracted_files))

    def _extract_mech_info_files(self,
                                 archive_path: pathlib.Path) -> tuple[str, ...]:
        with zipfile.ZipFile(archive_path) as archive:
            files_to_extract = self._find_data_files_in_archive(
                archive_path=archive_path,
                archive=archive)
            self._logger.info("\n".join(files_to_extract))
            archive.extractall(
                path=self._workdir,
                members=files_to_extract)
            return files_to_extract

    def _filter_mechs_archives(
            self) -> typing.Generator[pathlib.Path, None, None]:
        for archive_path in self._mech_archives_dir.glob("*"):
            if archive_path.suffix in self._archive_file_suffixes:
                yield archive_path

    def __call__(self) -> MechInfo:
        self._mech_info.clear()
        self._logger.info(f"extraction directory: {self._workdir}")
        for archive_path in self._filter_mechs_archives():
            self._logger.info(archive_path)
            extracted_files = self._extract_mech_info_files(
                archive_path=archive_path)
            self._store_mech_data(
                archive_path=archive_path,
                extracted_files=extracted_files)
        return self._mech_info
