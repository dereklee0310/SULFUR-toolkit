# Object Definition
```
"C:\Program Files (x86)\Steam\steamapps\common\SULFUR\Sulfur_Data\StreamingAssets\aa\StandaloneWindows64"
```
## Enchantment_ActionOil
```json
{
    "m_GameObject": {
        "m_FileID": 0,
        "m_PathID": 0
    },
    "m_Enabled": 1,
    "m_Script": {
        "m_FileID": 1,
        "m_PathID": 386070880745911770
    },
    "m_Name": "Enchantment_ActionOil", // Object name
    "id": {
        "value": 43
    },
    "devNotes": "",
    "displayName": "Action Oil", // In-game display name
    "description": "+20% damage.", // In-game description
    "hasCustomDescription": 0,
    "flavor": "",
    "artwork": {
        "m_FileID": 2,
        "m_PathID": 2194594716051187737 // Sprite object
    },
    "artworkUnfoldedVariant": {
        "m_FileID": 0,
        "m_PathID": 0
    },
    "artworkWorldScale": 1.0,
    "shadowWorldScale": 1.0,
    "useType": 3,
    "useSounds": [],
    "consumeEffect": {
        "m_FileID": 0,
        "m_PathID": 0
    },
    "soundpack": {
        "m_FileID": 0,
        "m_PathID": 8356783863572835340
    },
    "includedInDemo": 0, // In demo or not 
    "includedInEarlyAccess": 1, // in early access or not
    "deprecated": 0,
    "prefab": {
        "m_FileID": 0,
        "m_PathID": 0
    },
    "showcasePrefab": {
        "m_FileID": 0,
        "m_PathID": 0
    },
    "includedInSpawnAllItems": 1,
    "excludeFromLocalization": 0,
    "purgeQuestsWithThisItem": 0,
    "isEndlessUpgrade": 0,
    "sellable": 1,
    "basePrice": 700, // In-game price
    "itemQuality": 2,
    "slotType": 0,
    "inventorySize": { // Size in the inventory, sometimes it's wrong
        "x": 1,
        "y": 1
    },
    "stackSize": 0,
    "usesResource": {
        "m_FileID": 0,
        "m_PathID": 0
    },
    "weightClass": 0,
    "maxDurability": 1000.0,
    "repairReductionCost": 0,
    "alwaysSpawnWithFullDurability": 0,
    "showCrosshair": 1,
    "automaticConsume": 0,
    "automaticPickup": 0,
    "slideTowardsPlayer": 0,
    "doNotAnnounce": 0,
    "doNotShowName": 0,
    "npcsCanPickup": 1,
    "modifiersOnEquipNew": [],
    "modifiersOnInventoryNew": [],
    "removeStatusOnConsume": [],
    "modifiersOnAttachToItem": [],
    "buffsOnConsume": [],
    "valueChangeOnItemConsume": [],
    "resourceOnConsume": [],
    "recipesTaughtOnConsume": [],
    "appliesEnchantment": {
        "m_FileID": 0,
        "m_PathID": 3916649743819863455 // Link to enchantment definition
    },
    "modifiesCaliber": { // For chamber chisel
        "m_FileID": 0,
        "m_PathID": 0
    },
    "unlocksCheckpointWhenBroughtToChurch": 0,
    "baseAttributes": [] // For guns
}
```

## EnchantmentDefinition_ActionOil
```json
{
    "m_GameObject": {
        "m_FileID": 0,
        "m_PathID": 0
    },
    "m_Enabled": 1,
    "m_Script": {
        "m_FileID": 1,
        "m_PathID": -7562350256701091521
    },
    "m_Name": "EnchantmentDefinition_ActionOil",
    "id": {
        "value": 1
    },
    "enchantmentName": "Action Oil",
    "backgroundTexture": {
        "m_FileID": 0,
        "m_PathID": 0
    },
    "textColor": {
        "r": 1.0,
        "g": 1.0,
        "b": 1.0,
        "a": 1.0
    },
    "CostsDurability": 1, // Increase durability loss or not (0 or 1)
    "IsElemental": 0, // It would be 1 for enchantments like Voodoo, Earch, ...
    "modifiersApplied": [
        {
            "attribute": {
                "m_FileID": 0,
                "m_PathID": 2153745275254426622 // Link to buff/debuff
            },
            "modType": 200,
            "value": 1.0
        },
        {
            "attribute": {
                "m_FileID": 0,
                "m_PathID": -4569392407707992584 // Link to buff/debuff
            },
            "modType": 200,
            "value": 0.4000000059604645 // magnification
        }
    ]
}
```

## KickMultiplier
```json
{
    "m_GameObject": {
        "m_FileID": 0,
        "m_PathID": 0
    },
    "m_Enabled": 1,
    "m_Script": {
        "m_FileID": 1,
        "m_PathID": 3473597342840454226
    },
    "m_Name": "KickMultiplier",
    "id": 19,
    "label": "Kick", // Usually the in-game name
    "itemDescriptionName": "Kick", // Sometimes name, sometimes description
    "showInItemDescription": 1, // It would be 0 for buffs on equipments
    "unitMeasure": "",
    "excludeFromLocalization": 0,
    "simplifiedModAmount": 0,
    "simplifiedIncreaseString": "",
    "simplifiedDecreaseString": "",
    "isBooleanAttribute": 0,
    "isPercentageAttribute": 0, // Is the attribute in percentage or a plain value 
    "overrideUnitName": "",
    "makesProjectileApplyAttribute": { // for enchantments that deal elemental damage
        "m_FileID": 0,
        "m_PathID": 0
    },
    "projectileEffect": { // for enchantments that deal elemental damage
        "m_FileID": 0,
        "m_PathID": 0
    },
    "applyAttributeModifier": {
        "attribute": {
            "m_FileID": 0,
            "m_PathID": 0
        },
        "modType": 0,
        "value": 0.0,
        "disableEffectActivation": 0,
        "applyItemDefinitionValue": 0,
        "procChance": 0.0
    },
    "spawnObjectOnUnitHit": [],
    "spawnObjectOnEnvironmentHit": [],
    "spawnObjectOnStartShoot": [],
    "replacesBloodPrefab": {
        "m_FileID": 0,
        "m_PathID": 0
    },
    "replacesBloodEffect": {
        "m_FileID": 0,
        "m_PathID": 0
    }
}
```

## Recipe_Mudcake_1 1
```json
{
    "m_GameObject": {
        "m_FileID": 0,
        "m_PathID": 0
    },
    "m_Enabled": 1,
    "m_Script": {
        "m_FileID": 1,
        "m_PathID": 3561183746538219434
    },
    "m_Name": "Recipe_Mudcake_1 1", // Recipe name
    "createsItem": {
        "m_FileID": 0,
        "m_PathID": -7885760137349746736 // Link to item it creates
    },
    "quantityCreated": 3, // Number of item it creates
    "itemsNeeded": [
        {
            "item": {
                "m_FileID": 0,
                "m_PathID": -82282651914463174 // Link to required item
            },
            "quantity": 1 // Required quantity
        },
        {
            "item": {
                "m_FileID": 0,
                "m_PathID": 1452232495277735399
            },
            "quantity": 1
        },
        {
            "item": {
                "m_FileID": 0,
                "m_PathID": -8199466475927202420
            },
            "quantity": 1
        },
        {
            "item": {
                "m_FileID": 0,
                "m_PathID": 8296372714667799805
            },
            "quantity": 1
        },
        {
            "item": {
                "m_FileID": 0,
                "m_PathID": 2858632851210039811
            },
            "quantity": 1
        }
    ],
    "canBeCrafted": 1 // All 1, not sure what it does
}
```