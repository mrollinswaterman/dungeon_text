#item compendium

#tag, id, (num dice, dice type, crit)
WEAPONS_DICTIONARY = [
    (("WP"), "Battleaxe", "1d8,x2"),
    (("WP"), "Light Flail", "1d8,x2"),
    (("WP"), "Scimitar", "1d6,x3,18"),
    (("WP"), "Trident", "1d10,x2"),
    (("WP"), "Mace", "1d8,x2"),
    (("WP"), "Greatsword", "2d6,x2"),
    (("WP"), "Glaive", "1d10,x3"),
    (("WP"), "Greataxe", "1d12,x3"),
    (("WP"), "Scythe", "2d4,x5"),
    (("WP"), "Halberd", "1d10,x3")
]

#tag, id, weight class, armor bonus (none is default --> determined by rarity and class)
ARMOR_DICTIONARY = [
    (("AR"), "Studded Leather", ("Light", None)),
    (("AR"), "Haramaki", ("None", 1)),
    (("AR"), "Chain Shirt", ("Light", None)),
    (("AR"), "Breastplate", ("Medium", None)),
    (("AR"), "Chainmail", ("Medium", 6)),
    (("AR"), "Armored Coat", ("Medium", None)),
    (("AR"), "Scale Mail", ("Medium", None)),
    (("AR"), "Half-plate", ("Heavy", None)),
    (("AR"), "Stoneplate", ("Heavy", 9)),
    (("AR"), "Branded Mail", ("Heavy", None)),
    (("AR"), "Full-plate", ("Heavy", 9)),
]
