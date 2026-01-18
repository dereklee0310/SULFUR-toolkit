# Object Definition
```
"C:\Program Files (x86)\Steam\steamapps\common\SULFUR\Sulfur_Data\StreamingAssets\aa\StandaloneWindows64"
```
## Enchantment_ActionOil
```json
{
	"m_CorrespondingSourceObject": { "m_FileID": 0, "m_PathID": 0 },
	"m_EditorClassIdentifier": "",
	"m_EditorHideFlags": 0,
	"m_Enabled": 1,
	"m_GameObject": { "m_FileID": 0, "m_PathID": 0 },
	"m_HideFlags": 0,
	"m_Name": "Enchantment_BlackFridayOil",
	"m_PrefabAsset": { "m_FileID": 0, "m_PathID": 0 },
	"m_PrefabInstance": { "m_FileID": 0, "m_PathID": 0 },
	"m_Script": { "m_FileID": 1, "m_PathID": 386070880745911770 },
	"m_Structure": {
		"id": {
			"value": 64
		},
		"excludeFromDatabase": 0,
		"devNotes": "",
		"displayName": "Black Friday Oil",
		"description": "+20% damage.",
		"hasCustomDescription": 0,
		"flavor": "",
		"artwork": { "m_FileID": 0, "m_PathID": -95530692827490188 },
		"artworkUnfoldedVariant": { "m_FileID": 0, "m_PathID": 0 },
		"artworkWorldScale": 1,
		"shadowWorldScale": 1,
		"useType": 3,
		"useSounds": [],
		"consumeEffect": { "m_FileID": 0, "m_PathID": 0 },
		"soundpack": { "m_FileID": 0, "m_PathID": 8356783863572835340 },
		"includedInDemo": 0,
		"includedInEarlyAccess": 1,
		"deprecated": 0,
		"prefab": { "m_FileID": 0, "m_PathID": 0 },
		"showcasePrefab": { "m_FileID": 0, "m_PathID": 0 },
		"includedInSpawnAllItems": 1,
		"excludeFromLocalization": 0,
		"purgeQuestsWithThisItem": 0,
		"isEndlessUpgrade": 0,
		"sellable": 1,
		"basePrice": 300,
		"itemQuality": 2,
		"slotType": 0,
		"inventorySize": {
			"x": 1,
			"y": 1
		},
		"stackSize": 0,
		"usesResource": 0,
		"weightClass": 0,
		"maxDurability": 1000,
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
			"value": 22
		},
		"modifiesCaliber": 0,
		"unlocksCheckpointWhenBroughtToChurch": 0,
		"baseAttributes": []
	}
}
```

## EnchantmentDefinition_BlackFridayOil
```json
{
	"m_CorrespondingSourceObject": { "m_FileID": 0, "m_PathID": 0 },
	"m_EditorClassIdentifier": "",
	"m_EditorHideFlags": 0,
	"m_Enabled": 1,
	"m_GameObject": { "m_FileID": 0, "m_PathID": 0 },
	"m_HideFlags": 0,
	"m_Name": "EnchantmentDefinition_BlackFridayOil",
	"m_PrefabAsset": { "m_FileID": 0, "m_PathID": 0 },
	"m_PrefabInstance": { "m_FileID": 0, "m_PathID": 0 },
	"m_Script": { "m_FileID": 1, "m_PathID": -7562350256701091521 },
	"m_Structure": {
		"id": {
			"value": 22
		},
		"enchantmentName": "Black Friday Oil",
		"backgroundTexture": { "m_FileID": 0, "m_PathID": 0 },
		"textColor": {
			"r": 1,
			"g": 1,
			"b": 1,
			"a": 1
		},
		"CostsDurability": 1,
		"IsElemental": 0,
		"modifiersApplied": [
			{
				"attribute": 21,
				"modType": 200,
				"value": -0.33
			},
			{
				"attribute": 22,
				"modType": 200,
				"value": 1
			},
			{
				"attribute": 6,
				"modType": 200,
				"value": -0.15
			}
		]
	}
}
```

## KickMultiplier
```json
{
	"m_CorrespondingSourceObject": { "m_FileID": 0, "m_PathID": 0 },
	"m_EditorClassIdentifier": "",
	"m_EditorHideFlags": 0,
	"m_Enabled": 1,
	"m_GameObject": { "m_FileID": 0, "m_PathID": 0 },
	"m_HideFlags": 0,
	"m_Name": "KickMultiplier",
	"m_PrefabAsset": { "m_FileID": 0, "m_PathID": 0 },
	"m_PrefabInstance": { "m_FileID": 0, "m_PathID": 0 },
	"m_Script": { "m_FileID": 1, "m_PathID": 3473597342840454226 },
	"m_Structure": {
		"id": 19,
		"label": "Kick",
		"itemDescriptionName": "Kick",
		"showInItemDescription": 1,
		"unitMeasure": "",
		"excludeFromLocalization": 0,
		"simplifiedModAmount": 0,
		"simplifiedIncreaseString": "",
		"simplifiedDecreaseString": "",
		"isBooleanAttribute": 0,
		"isPercentageAttribute": 0,
		"overrideUnitName": "",
		"makesProjectileApplyAttribute": 0,
		"projectileEffect": { "m_FileID": 0, "m_PathID": 0 },
		"applyAttributeModifier": {
			"attribute": 0,
			"modType": 0,
			"value": 0,
			"disableEffectActivation": 0,
			"applyItemDefinitionValue": 0,
			"procChance": 0
		},
		"spawnObjectOnUnitHit": [],
		"spawnObjectOnEnvironmentHit": [],
		"spawnObjectOnStartShoot": [],
		"replacesBloodEffect": { "m_FileID": 0, "m_PathID": 0 }
	}
}
```

## Recipe_Mudcake_1 1 (In RecipeDatabase)
```json
{
    "id": {
        "value": 864
    },
    "name": "Recipe_Mudcake_1 1",
    "type": 1,
    "createsItem": {
        "value": 568
    },
    "quantityCreated": 3,
    "itemsNeeded": [
        {
            "item": {
                "value": 440
            },
            "quantity": 1
        },
        {
            "item": {
                "value": 560
            },
            "quantity": 1
        },
        {
            "item": {
                "value": 375
            },
            "quantity": 1
        },
        {
            "item": {
                "value": 708
            },
            "quantity": 1
        },
        {
            "item": {
                "value": 456
            },
            "quantity": 1
        }
    ],
    "canBeCrafted": 1
}
```