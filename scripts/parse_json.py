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
OIL_XLSX_OUTPUT_PATH = "./oils.xlsx"
OIL_JSON_OUTPUT_PATH = "./oils.json"
RECIPE_JSON_OUTPUT_PATH = "./recipes.json"
RECIPE_XLSX_OUTPUT_PATH = "./recipes.xlsx"

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
    "artwork": "Artwork"
}

EFFECT_TYPES = list(MAPPING.values())[4:]

args = parse_json_args()
logger = setup_logger(args.logging_level)
cnt = 0


def build_oil_object(data, oil_id):
    # Enchantment_*Oil
    oil_data = data[oil_id]
    global cnt
    cnt += 1
    logger.info(f"Parsing {cnt:>4} %s", oil_data["displayName"])
    result = {
        "displayName": oil_data["displayName"],
        "includedInDemo": oil_data["includedInDemo"],
        "includedInEarlyAccess": oil_data["includedInEarlyAccess"],
        "basePrice": oil_data["basePrice"],
        **get_oil_definition(data, str(oil_data["appliesEnchantment"]["m_PathID"])),
    }
    if args.dev:
        result["artwork"] = oil_data["artwork"]["m_PathID"]

    # df.rename and df.map are great, but we also want to dump a json file
    # so we need to format them here
    return {
        MAPPING[k]: (float(f"{v:.2f}") if isinstance(v, float) else v)
        for k, v in result.items()
    }


def get_oil_definition(data, oil_definition_id):
    # EnchantmentDefinition_*Oil
    definition_data = data[oil_definition_id]
    return {
        "CostsDurability": definition_data["CostsDurability"],
        **get_modifiers_definition(data, definition_data["modifiersApplied"]),
    }


def get_modifiers_definition(data, modifiers):
    results = {}
    for modifier in modifiers:
        # itemDescriptionName is not reliable, use label instead
        name = data[str(modifier["attribute"]["m_PathID"])]["label"]
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


def parse_oil_data(data):
    oil_infos = [build_oil_object(data, oil_id) for oil_id in data["oil_ids"]]
    oil_groups = defaultdict(list)
    for oil_info in oil_infos:
        for type in get_oil_types(oil_info):
            oil_groups[type].append(oil_info)

    with open(OIL_JSON_OUTPUT_PATH, "w", encoding="utf8") as f:
        json.dump({"all": oil_infos} | oil_groups, f, ensure_ascii=False, indent=4)

    dump_oil_xlsx(oil_infos, oil_groups)


def build_recipe_object(data, recipe_id):
    recipe_data = data[recipe_id]
    global cnt
    cnt += 1
    # Recipe doesn't have displayName
    logger.info(f"Parsing {cnt:>4} %s", recipe_data["m_Name"])
    result = {
        "Recipe Name": recipe_data["m_Name"],
        "Item Name": data[str(recipe_data["createsItem"]["m_PathID"])]["displayName"],
        "Quantity": recipe_data["quantityCreated"],
        "Items Needed": {},
    }

    if args.dev:
        result["Item Artwork"] = data[str(recipe_data["createsItem"]["m_PathID"])]["artwork"]["m_PathID"]

    for item_data in recipe_data["itemsNeeded"]:
        real_item_data = data[str(item_data["item"]["m_PathID"])]
        item_name = real_item_data["displayName"]

        if args.dev:
            result["Items Needed"][item_name] = {
                "Quantity": item_data["quantity"],
                "Artwork": real_item_data["artwork"]["m_PathID"]
            }
        else:
            result["Items Needed"][item_name] = item_data["quantity"]
    return result


def dump_recipe_xlsx(recipe_infos, recipes_of_items):
    with pd.ExcelWriter(RECIPE_XLSX_OUTPUT_PATH, engine="openpyxl") as writer:
        df = pd.DataFrame(recipe_infos)
        df.to_excel(writer, sheet_name="Recipes", index=False)
        df = pd.DataFrame.from_dict(recipes_of_items, orient="index")
        df.to_excel(writer, sheet_name="Recipes of Items")
    adjust_width(RECIPE_XLSX_OUTPUT_PATH)


def parse_recipe_data(data):
    recipe_infos = [
        build_recipe_object(data, recipe_id) for recipe_id in data["recipe_ids"]
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


if __name__ == "__main__":
    logger.info("Parsing json file: %s", DATA_PATH)
    try:
        with open(DATA_PATH, "r", encoding="utf8") as f:
            data = json.load(f)
    except FileNotFoundError:
        logger.critical("%s not found! Please parse the game bundles first.")
        sys.exit()
    parse_oil_data(data)
    parse_recipe_data(data)
