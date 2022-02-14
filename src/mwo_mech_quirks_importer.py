import contextlib
import logging
import pathlib
# import sqlite3


# noinspection PyPackageRequirements
import pysqlite3 as sqlite3


from aux_types import MechQuirks, OmniMechQuirks, StandardMechQuirks
import query


class MWOMechQuirksImporter:
    def __init__(self,
                 sqlite_db_name: pathlib.Path,
                 logger: logging.Logger = None):
        # const
        self._sqlite_db_name = sqlite_db_name
        self._logger = logger or logging.getLogger(self.__class__.__name__)

        # runtime
        self._connection = None

    def _create_tables(self) -> None:
        with contextlib.closing(self._connection.cursor()) as cursor:
            cursor.execute(query.CREATE_TABLE_MECH)
            cursor.execute(query.CREATE_TABLE_QUIRK)

    def _upsert_omnimech_mech_quirks(
            self,
            omnimech_mechs_quirks: tuple[OmniMechQuirks, ...]) -> None:
        with contextlib.closing(self._connection.cursor()) as cursor:
            for omnimech_mech_quirks in omnimech_mechs_quirks:
                for mech_model, info in omnimech_mech_quirks.quirks_by_configuration.items():
                    cursor.execute(
                        query.UPSERT_MECH,
                        (mech_model.mech_name, mech_model.mech_model, True))
                    mech_id = cursor.fetchone()["mech_id"]
                    cursor.executemany(
                        query.UPSERT_QUIRK,
                        (
                            (
                                mech_id,
                                info.omnipod_set_bonus_quirks.bonus_piece_count,
                                quirk.quirk_name,
                                quirk.quirk_value
                            )
                            for quirk in info.omnipod_set_bonus_quirks.quirks
                        ))
                    cursor.executemany(
                        query.UPSERT_QUIRK,
                        (
                            (
                                mech_id,
                                component_info.component_name,
                                quirk.quirk_name,
                                quirk.quirk_value
                            )
                            for component_info
                            in info.components_with_quirks.values()
                            for quirk in component_info.quirks
                        ))

    def _upsert_standard_mech_quirks(
            self,
            standard_mechs_quirks: tuple[StandardMechQuirks, ...]) -> None:
        with contextlib.closing(self._connection.cursor()) as cursor:
            for standard_mech_quirks in standard_mechs_quirks:
                for mech_model, quirks in standard_mech_quirks.quirks_by_configuration.items():
                    cursor.execute(
                        query.UPSERT_MECH,
                        (standard_mech_quirks.mech_name, mech_model, False))
                    mech_id = cursor.fetchone()["mech_id"]
                    cursor.executemany(
                        query.UPSERT_QUIRK,
                        (
                            (
                                mech_id, 'chassis',
                                quirk.quirk_name, quirk.quirk_value
                            )
                            for quirk in quirks
                        ))

    def __call__(self, quirks: MechQuirks):
        self._sqlite_db_name.parent.mkdir(exist_ok=True)
        with sqlite3.connect(self._sqlite_db_name) as self._connection:
            self._connection.row_factory = sqlite3.Row
            self._create_tables()
            self._upsert_standard_mech_quirks(quirks["std"])
            self._upsert_omnimech_mech_quirks(quirks["omni"])
