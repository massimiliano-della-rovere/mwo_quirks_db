import pathlib
import typing


class MechData(typing.NamedTuple):
    archive_path: pathlib.Path
    mech_name: str
    files: tuple[pathlib.Path, ...]
    has_omnipods: bool


MechInfo = dict[str, MechData]


class Quirk(typing.NamedTuple):
    quirk_name: str
    quirk_value: float


class MechModel(typing.NamedTuple):
    mech_name: str
    mech_model: str


class OmnipodQuirks(typing.NamedTuple):
    mech_model: MechModel
    component_name: str
    quirks: tuple[Quirk, ...]


class OmnipodSetQuirks(typing.NamedTuple):
    mech_model: MechModel
    bonus_piece_count: int
    quirks: tuple[Quirk, ...]


class OmniMechConfigurationQuirks(typing.NamedTuple):
    mech_model: MechModel
    omnipod_set_bonus_quirks: OmnipodSetQuirks
    components_with_quirks: dict[str, OmnipodQuirks]


class OmniMechQuirks(typing.NamedTuple):
    mech_name: str
    quirks_by_configuration: dict[MechModel, OmniMechConfigurationQuirks]


class StandardMechQuirks(typing.NamedTuple):
    mech_name: str
    quirks_by_configuration: dict[MechModel, tuple[Quirk]]


class MechQuirks(typing.TypedDict):
    std: tuple[StandardMechQuirks, ...]
    omni: tuple[OmniMechQuirks, ...]
