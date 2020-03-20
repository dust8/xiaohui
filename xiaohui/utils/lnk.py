import os
import pathlib

import LnkParse3

PROGRAMS = {}


def find_programs(path=r"C:\ProgramData\Microsoft\Windows\Start Menu"):
    root = pathlib.Path(path)
    lnks = root.glob("**/*.lnk")
    for lnk in lnks:
        if ("uninstall" in lnk.stem.lower()) or ("卸载" in lnk.stem.lower()):
            continue

        lnk_parse = LnkParse3.lnk_file(open(str(lnk), "rb"))
        local_base_path = lnk_parse.loc_information.get("local_base_path", "")
        if not local_base_path:
            full_path = lnk_parse.extraBlocks.get(
                "ENVIRONMENTAL_VARIABLES_LOCATION_BLOCK", {}
            ).get("target_ansi", "")
            if not full_path:
                full_path = lnk_parse.extraBlocks.get("ICON_LOCATION_BLOCK", {}).get(
                    "target_ansi", ""
                )
                if not full_path:
                    continue
        else:
            common_path_suffix = lnk_parse.loc_information.get("common_path_suffix", "")
            full_path = local_base_path + common_path_suffix
        PROGRAMS[lnk.stem.lower()] = full_path


find_programs()
find_programs(
    os.path.join(
        os.environ["HOME"], r"AppData\Roaming\Microsoft\Windows\Start Menu\Programs"
    )
)

if __name__ == "__main__":
    from pprint import pprint

    pprint(PROGRAMS)

