"""
Extract oil & recipe data.
"""

import json
import re
import sys
from pathlib import Path

import UnityPy
from utils.utils import parse_bundle_args, setup_logger

OUTPUT_DIR = Path("./tmp")
# OIL_NAME_REGEX = re.compile(r"Enchantment_(.*)Oil")
WEAPON_NAME_REGEX = re.compile(r"Weapon_(?!Gun_Shot)(.*)")  # ...Gun_Shot for npc weapon

# Some of them have incorrect artwork or name, could be a deprecated or new item
BLACKLIST = set(
    [
        "Weapon_WyattPulsarNotUse",
        "Weapon_Arbiter2NotUse",
        "Weapon_Chat-Pardeur98",
        "Weapon_Warpig",
        "Enchantment_TestOil",
        "Enchantment_TestOil2",
        "Enchantment_Satiety",
        "Enchantment_Flutter",
        "Enchantment_Duality",
        "Triple Oil",
        "Enchantment_Slayer",
        "Enchantment_FastForwardOil",
        "Enchantment_Steam",
        "Enchantment_EternalOil",
        "Enchantment_SlowMoOil",
        "Enchantment_UnlabeledOil",
        "Weapon_RamshackOld_NOT_USED"
    ]
)

args = parse_bundle_args()
logger = setup_logger(args.logging_level)


def get_bundle():
    bundles = list(str(x) for x in Path("./").glob("onstartup_assets_all_*.bundle"))
    for bundle in bundles:
        logger.info("Found '%s'", bundle)

    if not bundles:
        logger.critical(".bundle file not found, please put it in the same directory")
        sys.exit()
    if len(bundles) > 1:
        logger.warning("Found multiple .bundle files, will use the first one it found")
    return bundles[0]


def parse_bundle():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    data = {}
    category = {
        "weapon": [],
        "enchantment": {"oil": [], "scroll": []},
        "attachment": {
            "muzzle": [],
            "scope": [],
            "laserSight": [],
            "chamber": [],
            "insurance": [],
        },
        "chamberChisel": [],
    }
    mapping = {"item": {}, "enchantmentDefinition": {}, "attributeModifier": {}}

    env = UnityPy.load(get_bundle())
    cnt = 0
    for obj in env.objects:
        if obj.type.name != "MonoBehaviour" or not obj.peek_name():
            continue

        tree = obj.parse_as_dict()  # m_Structure is unpacked by UnityPy temporarily
        item_id = str(obj.path_id)
        item_name = tree["m_Name"]
        logger.debug("Parsing '%s'", item_name)

        if item_name in BLACKLIST:
            logger.warning("Skipping '%s'", item_name)
            continue
        data[item_id] = tree

        # Use three keys to identify an actual item, wtf perfect random
        if "displayName" in tree and "id" in tree and "artwork" in tree:
            mapping["item"][tree["id"]["value"]] = item_id

        if "enchantmentName" in tree:
            mapping["enchantmentDefinition"][tree["id"]["value"]] = item_id
        elif "applyAttributeModifier" in tree:
            mapping["attributeModifier"][tree["id"]] = item_id

        cnt += 1
        if item_name.startswith("Enchantment_"):
            logger.info(f"Found    enchantment {cnt:>3}: '%s'", item_name)
            if item_name.endswith("Oil"):
                category["enchantment"]["oil"].append(item_id)
            else:
                category["enchantment"]["scroll"].append(item_id)
        elif item_name.startswith("Attachment_"):
            logger.info(f"Found     attachment {cnt:>3}: '%s'", item_name)

            if not tree["modifiersOnAttachToItem"]:
                category["attachment"]["insurance"].append(item_id)
                continue

            attachment_type = tree["modifiersOnAttachToItem"][0]["attribute"]
            if attachment_type in (57, 58):  # 57: silence, 58: spead
                category["attachment"]["muzzle"].append(item_id)
            elif attachment_type == 5:  # crit chance
                category["attachment"]["scope"].append(item_id)
            elif attachment_type == 1:  # accuracy while moving
                category["attachment"]["laserSight"].append(item_id)
            elif attachment_type == 14:  # firing mode
                # 1 for gun crank, -1 for priming bolt
                # Priming bolt also have spread and damage, ignore it for now
                category["attachment"]["chamber"].append(item_id)
        elif WEAPON_NAME_REGEX.match(item_name):
            logger.info(f"Found         weapon {cnt:>3}: '%s'", item_name)
            category["weapon"].append(item_id)
        elif item_name.startswith("Consumable_ChamberChisel"):
            logger.info(f"Found chamber chisel {cnt:>3}: '%s'", item_name)
            category["chamberChisel"].append(item_id)
        else:
            cnt -= 1

    with open(OUTPUT_DIR / "category.json", "w", encoding="utf8") as f:
        json.dump(category, f, ensure_ascii=False, indent=4)

    with open(OUTPUT_DIR / "data.json", "w", encoding="utf8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    with open(OUTPUT_DIR / "mapping.json", "w", encoding="utf8") as f:
        json.dump(mapping, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    parse_bundle()
