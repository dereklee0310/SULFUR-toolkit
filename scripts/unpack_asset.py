"""
Extract Sprites & Texture2D from spritesitems_assets_all_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.bundle
"""

import json
import re
import sys
from pathlib import Path

import UnityPy
from utils.utils import parse_asset_args, setup_logger

OUTPUT_DIR = Path("./assets")
# Some items have incorrect m_Name that matches with this regex, don't want to touch this shit now ;)
OIL_NAME_REGEX = re.compile(r"Enchantment_(.*)Oil")

args = parse_asset_args()
logger = setup_logger(args.logging_level)
print(logger.level)


def get_bundles():
    # Use spritesitems and gamedefinitions
    bundles = list(str(x) for x in Path("./").glob("*.bundle"))
    for bundle in bundles:
        logger.info("Found '%s'", bundle)
    if not bundles:
        logger.critical(".bundle file not found, please put it in the same directory")
        sys.exit()
    return bundles


def unpack_asset():
    id_table = {}
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    env = UnityPy.Environment()
    for bundle in get_bundles():
        env.load_file(bundle)

    cnt = 0
    for obj in env.objects:
        if (
            (obj.type.name not in ["Texture2D", "Sprite"])
            or (args.sprite and obj.type.name == "Texture2D")
            or (args.texture and obj.type.name == "Sprite")
            or not obj.peek_name() # Skip when there's no name for UnityPy
        ):
            logger.debug(f"Skipping  {obj.type.name:>14}: %s", obj.peek_name())
            continue

        tree = obj.parse_as_object()  # m_Structure is unpacked by UnityPy temporarily

        # Some sprites has no texture
        if obj.type.name == "Sprite" and tree.m_RD.texture.path_id == 0:
            logger.debug(f"Skipping  {obj.type.name:>14}: %s", obj.peek_name())
            continue

        item_id = str(obj.path_id)
        item_name = tree.m_Name
        cnt += 1
        logger.info(f"Unpacking {obj.type.name:>14} {cnt:>4}: '%s'", item_name)
        id_table[item_id] = item_name
        tree.image.save(OUTPUT_DIR / f"{item_name}.png")

    with open(OUTPUT_DIR / "data.json", "w", encoding="utf8") as f:
        json.dump(id_table, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    unpack_asset()
