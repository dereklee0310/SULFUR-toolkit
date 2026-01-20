"""
Parse ./tmp/data.json to generate json and spreadsheet.
"""

import json
import sys
from collections import defaultdict

import openpyxl
import pandas as pd
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.dimensions import ColumnDimension, DimensionHolder
from utils.utils import parse_json_args, setup_logger

DATA_PATH = "./tmp/data.json"
CATEGORY_PATH = "./tmp/category.json"
ID_MAPPING_PATH = "./tmp/mapping.json"
FILENAME_MAPPING_PATH = "./assets/data.json"
OIL_XLSX_OUTPUT_PATH = "./oils.xlsx"
OIL_JSON_OUTPUT_PATH = "./oils.json"
RECIPE_JSON_OUTPUT_PATH = "./recipes.json"
RECIPE_XLSX_OUTPUT_PATH = "./recipes.xlsx"
WEAPON_JSON_OUTPUT_PATH = "./weapons.json"
FINAL_RESULT_OUTPUT_PATH = "./results.json"


SCROLL_JSON_OUTPUT_PATH = "./scrolls.json"

RECIPE_DATABASE_ID = "3425407372818098406"

MAPPING = {
    "displayName": "Name",
    "includedInDemo": "Demo",
    "includedInEarlyAccess": "Early Access",
    "basePrice": "Base Price",
    "CostsDurability": "Costs Durability",
    "Kick": "Recoil",
    "Reload Speed": "Reload Speed",
    "Damage": "Damage",
    "Critical damage chance": "Crit Chance",
    "Disables aiming": "Disables Aiming",
    "Projectile drag multiplier": "Drag Mult",
    "Spread": "Spread",
    "Loot Chance Multiplier": "Loot Chance Multiplier",
    "Bullet bounces": "Bullet Bounces",
    "Time scale": "Bullet Speed",
    "Damage%": "Damage%",
    "Bullet size": "Bullet Size",
    "Bullet drop": "Bullet Drop",
    "No money drops": "No Money Drops",
    "Move speed": "Move Speed",
    "Rounds per minute": "RPM",
    "Bullet Penetration": "Bullet Penetration",
    "Jump power": "Jump Power",
    "Max Durability": "Max Durability",
    "Number of projectiles": "Projectile Amount",
    "Projectile bounciness": "Bullet Bounciness",
    "Chance this consumes ammo": "Ammo Consume Chance",
    "Chance to consume extra ammo": "Consume Extra Ammo Chance",
    "No organs drop": "No Organs Drop",
    "Durability Per Shot": "Durability Per Shot",
    "Projectile force multiplier": "Projectile Force Multiplier",
    "Accuracy when moving": "Accuracy When Moving",
    "Enchantment Random Oil": "Enchantment Random Oil",
    "MISC": "MISC",  # Not a built-in one, for sheet name conversion
    "artwork": "Artwork",
}

EFFECT_TYPES = list(MAPPING.values())[4:]

args = parse_json_args()
logger = setup_logger(args.logging_level)
cnt = 0


def build_enchantment_object(data, id_mapping, oil_id, filename_mapping):
    # Enchantment_*Oil
    oil_data = data[oil_id]
    global cnt
    cnt += 1
    logger.info(f"Parsing {cnt:>4} '%s'", oil_data["displayName"])
    result = {
        "displayName": oil_data["displayName"],
        "includedInDemo": oil_data["includedInDemo"],
        "includedInEarlyAccess": oil_data["includedInEarlyAccess"],
        "basePrice": oil_data["basePrice"],
        **get_oil_definition(
            data,
            id_mapping,
            id_mapping["enchantmentDefinition"][
                str(oil_data["appliesEnchantment"]["value"])
            ],
        ),
    }
    if args.dev:
        result["artwork"] = filename_mapping[str(oil_data["artwork"]["m_PathID"])]

    # df.rename and df.map are great, but we also want to dump a json file
    # so we need to format them here
    return {
        MAPPING[k] if k in MAPPING else k: (
            float(f"{v:.2f}") if isinstance(v, float) else v
        )
        for k, v in result.items()
    }


def get_oil_definition(data, mapping, oil_definition_id):
    # EnchantmentDefinition_*Oil
    definition_data = data[oil_definition_id]
    return {
        "CostsDurability": definition_data["CostsDurability"],
        **get_modifiers_definition(data, mapping, definition_data["modifiersApplied"]),
    }


def get_modifiers_definition(data, mapping, modifiers):
    results = {}
    for modifier in modifiers:
        # itemDescriptionName is not reliable, use label instead
        name = data[mapping["attributeModifier"][str(modifier["attribute"])]]["label"]
        # 100: boolean/add, 200: multiplier, 300: bullet size
        mod_type = modifier["modType"]
        value = modifier["value"]
        if name == "Damage" and mod_type == 200:
            results["Damage%"] = value
        else:
            results[name] = value
    return results


def get_oil_types(info):
    oil_types = []
    # Only reverse "Costs Durability"
    oil_types = [
        key
        for key in EFFECT_TYPES
        if (info.get(key, 0) != 0) ^ (key == "Costs Durability")
    ]
    return oil_types if oil_types else ["MISC"]


def adjust_width(filename):
    wb = openpyxl.load_workbook(filename)
    for worksheet in wb.sheetnames:
        ws = wb[worksheet]
        dim_holder = DimensionHolder(worksheet=ws)
        for col in range(ws.min_column, ws.max_column + 1):
            dim_holder[get_column_letter(col)] = ColumnDimension(
                ws, min=col, max=col, width=20
            )
        ws.column_dimensions = dim_holder
    wb.save(filename)


def dump_oil_xlsx(oil_infos, oil_groups):
    with pd.ExcelWriter(OIL_XLSX_OUTPUT_PATH, engine="openpyxl") as writer:
        df = pd.DataFrame(oil_infos)
        df.to_excel(writer, sheet_name="Comparison Chart", index=False)
        for group_name, oil_group_infos in oil_groups.items():
            df = pd.DataFrame(oil_group_infos)
            df.to_excel(writer, sheet_name=group_name, index=False)
    adjust_width(OIL_XLSX_OUTPUT_PATH)


def parse_oil_data(data, category, id_mapping, filename_mapping):
    oil_infos = [
        build_enchantment_object(data, id_mapping, oil_id, filename_mapping)
        for oil_id in category["enchantment"]["oil"]
    ]
    oil_groups = defaultdict(list)
    for oil_info in oil_infos:
        for type in get_oil_types(oil_info):
            oil_groups[type].append(oil_info)

    with open(OIL_JSON_OUTPUT_PATH, "w", encoding="utf8") as f:
        json.dump({"all": oil_infos} | oil_groups, f, ensure_ascii=False, indent=4)

    dump_oil_xlsx(oil_infos, oil_groups)

    return oil_infos


def parse_scroll_data(data, category, id_mapping, filename_mapping):
    scroll_infos = [
        build_enchantment_object(data, id_mapping, oil_id, filename_mapping)
        for oil_id in category["enchantment"]["scroll"]
    ]

    with open(SCROLL_JSON_OUTPUT_PATH, "w", encoding="utf8") as f:
        json.dump(scroll_infos, f, ensure_ascii=False, indent=4)
    return scroll_infos

def dump_recipe_xlsx(recipe_infos, recipes_of_items):
    with pd.ExcelWriter(RECIPE_XLSX_OUTPUT_PATH, engine="openpyxl") as writer:
        df = pd.DataFrame(recipe_infos)
        df.to_excel(writer, sheet_name="Recipes", index=False)
        df = pd.DataFrame.from_dict(recipes_of_items, orient="index")
        df.to_excel(writer, sheet_name="Recipes of Items")
    adjust_width(RECIPE_XLSX_OUTPUT_PATH)


def get_recipe_mapping(src_data):
    mapping = {}
    for k, v in src_data.items():
        # Use three keys to identify an actual item, wtf perfect random
        if "displayName" in v and "id" in v and "artwork" in v:
            mapping[v["id"]["value"]] = k
    return mapping


def build_recipe_object(src_data, id_mapping, recipe_data, filename_mapping):
    global cnt
    cnt += 1
    # Recipe doesn't have displayName
    logger.info(f"Parsing {cnt:>4} '%s'", recipe_data["name"])
    result = {
        "Recipe Name": recipe_data["name"],
        "Item Name": src_data[id_mapping[recipe_data["createsItem"]["value"]]][
            "displayName"
        ],
        "Quantity": recipe_data["quantityCreated"],
        "Items Needed": {},
    }

    if args.dev:
        result["Item Artwork"] = filename_mapping[
            str(
                src_data[id_mapping[recipe_data["createsItem"]["value"]]]["artwork"][
                    "m_PathID"
                ]
            )
        ]

    for item_data in recipe_data["itemsNeeded"]:
        real_item_data = src_data[id_mapping[item_data["item"]["value"]]]
        item_name = real_item_data["displayName"]

        if args.dev:
            try:
                result["Items Needed"][item_name] = {
                    "Quantity": item_data["quantity"],
                    "Artwork": filename_mapping[
                        str(real_item_data["artwork"]["m_PathID"])
                    ],
                }
                continue
            except KeyError:
                # Some items like cactus is not available now
                logger.warning(
                    "Artwork id not found: '%s'", real_item_data["artwork"]["m_PathID"]
                )
            result["Items Needed"][item_name] = item_data["quantity"]
    return result


def parse_recipe_data(data, filename_mapping):
    id_mapping = get_recipe_mapping(data)

    recipes = data[RECIPE_DATABASE_ID]["recipes"]
    recipe_infos = [
        build_recipe_object(data, id_mapping, recipe_data, filename_mapping)
        for recipe_data in recipes
    ]
    recipes_of_items = defaultdict(list)
    for recipe_info in recipe_infos:
        recipes_of_items[recipe_info["Item Name"]].append(
            {
                "Quantity": recipe_info["Quantity"],
                "Items Needed": recipe_info["Items Needed"],
            }
        )

    with open(RECIPE_JSON_OUTPUT_PATH, "w", encoding="utf8") as f:
        json.dump(
            {"all": recipe_infos} | recipes_of_items, f, ensure_ascii=False, indent=4
        )

    dump_recipe_xlsx(recipe_infos, recipes_of_items)
    return recipe_infos


def parse_weapon_data(data, filename_mapping):
    weapons = {}
    for k, v in data.items():
        if "slotType" in v and v["slotType"] == 7:
            weapons[v["displayName"]] = {
                "basePrice": v["basePrice"],
                "maxDurability": v["maxDurability"],
                "artwork": filename_mapping[str(v["artwork"]["m_PathID"])],
                # TODO
                "useType": v["useType"],
                "slotType": v["slotType"],
                # "damageType": 7,
                # "weaponType": 10,
                # "caliber": 5,
                # "damageMultiplier": 1.0,
                # "usableByPlayer": 1,
                # "projectileType": 1,
            }
    with open(WEAPON_JSON_OUTPUT_PATH, "w", encoding="utf8") as f:
        json.dump(weapons, f, ensure_ascii=False, indent=4)

    return weapons


if __name__ == "__main__":
    logger.info("Parsing file: '%s'", DATA_PATH)
    logger.info("Using category: '%s'", DATA_PATH)
    try:
        with open(DATA_PATH, "r", encoding="utf8") as f:
            data = json.load(f)
        with open(CATEGORY_PATH, "r", encoding="utf8") as f:
            category = json.load(f)
        with open(ID_MAPPING_PATH, "r", encoding="utf8") as f:
            id_mapping = json.load(f)
        filename_mapping = None
        if args.dev:
            with open(FILENAME_MAPPING_PATH, "r", encoding="utf8") as f:
                filename_mapping = json.load(f)
    except FileNotFoundError:
        logger.critical("'%s' not found! Please parse the game bundles first.")
        sys.exit()

    results = [
        parse_weapon_data(data, filename_mapping),
        parse_oil_data(data, category, id_mapping, filename_mapping),
        parse_scroll_data(data, category, id_mapping, filename_mapping),
    ]
    parse_recipe_data(data, filename_mapping)

    with open(FINAL_RESULT_OUTPUT_PATH, "w", encoding="utf8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)