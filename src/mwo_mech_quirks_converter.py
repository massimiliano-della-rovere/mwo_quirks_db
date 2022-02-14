import logging
import xml.etree.cElementTree as cXML


from aux_types import (
    MechModel, Quirk, MechData, MechQuirks, MechInfo,
    OmnipodQuirks, OmnipodSetQuirks, OmniMechConfigurationQuirks,
    OmniMechQuirks, StandardMechQuirks)


class MWOMechQuirksConverter:
    def __init__(self,
                 workdir: str,
                 logger: logging.Logger = None):
        # const
        self._workdir = workdir
        self._logger = logger or logging.getLogger(self.__class__.__name__)

    @staticmethod
    def _extract_omnipod_set_bonus(mech_model: MechModel,
                                   mech_configuration_node) -> OmnipodSetQuirks:
        bonus_node = mech_configuration_node.find("./SetBonuses/Bonus")
        return OmnipodSetQuirks(
            mech_model=mech_model,
            bonus_piece_count=int(bonus_node.attrib["PieceCount"]),
            quirks=tuple(
                Quirk(
                    quirk_name=quirk_node.attrib["name"],
                    quirk_value=float(quirk_node.attrib["value"]))
                for quirk_node in bonus_node.iterfind("./Quirk")))

    @staticmethod
    def _extract_components_with_quirks(
            mech_model: MechModel,
            mech_configuration_node) -> dict[str, OmnipodQuirks]:
        return {
            (component_name := component_node.attrib["name"]): OmnipodQuirks(
                mech_model=mech_model,
                component_name=component_name,
                quirks=tuple(
                    Quirk(
                        quirk_name=quirk_node.attrib["name"],
                        quirk_value=float(quirk_node.attrib["value"]))
                    for quirk_node in component_node.iterfind("./Quirk")))
            for component_node in mech_configuration_node.iterfind("./component")
        }

    def _omnipods_mech_quirks(self, mech_data: MechData) -> OmniMechQuirks:
        mech_name = mech_data.mech_name
        root = cXML.parse(mech_data.files[0])
        quirks_by_configuration = {}
        for mech_configuration_node in root.iterfind("./Set"):
            configuration_id = mech_configuration_node.attrib["name"]
            mech_model = MechModel(
                mech_name=mech_name,
                mech_model=configuration_id)
            quirks_by_configuration[mech_model] = OmniMechConfigurationQuirks(
                mech_model=mech_model,
                omnipod_set_bonus_quirks=self._extract_omnipod_set_bonus(
                    mech_model=mech_model,
                    mech_configuration_node=mech_configuration_node),
                components_with_quirks=self._extract_components_with_quirks(
                    mech_model=mech_model,
                    mech_configuration_node=mech_configuration_node))
        return OmniMechQuirks(
            mech_name=mech_name,
            quirks_by_configuration=quirks_by_configuration)

    @staticmethod
    def _standard_mech_quirks(mech_data: MechData) -> StandardMechQuirks:
        return StandardMechQuirks(
            mech_name=mech_data.mech_name,
            quirks_by_configuration={
                file_path.stem: tuple(
                    Quirk(
                        quirk_name=quirk_node.attrib["name"],
                        quirk_value=float(quirk_node.attrib["value"]))
                    for quirk_node in cXML.parse(file_path)
                                          .iterfind("./QuirkList/Quirk")
                )
                for file_path in mech_data.files
            })

    def __call__(self, mech_info: MechInfo) -> MechQuirks:
        ret = {"std": [], "omni": []}
        for mech_name, mech_data in mech_info.items():
            if mech_data.has_omnipods:
                ret["omni"].append(self._omnipods_mech_quirks(mech_data))
            else:
                ret["std"].append(self._standard_mech_quirks(mech_data))
        return {k: tuple(v) for k, v in ret.items()}
