from ..util import *


class Item(IntEnum):
    CAPSULE = 0x00
    BOX = 0x01
    BARREL = 0x02
    EGG = 0x03
    PARTY_BALL = 0x04
    BARREL_CANNON = 0x05
    BOB_OMB = 0x06
    MR_SATURN = 0x07
    HEART_CONTAINER = 0x08
    MAXIM_TOMATO = 0x09
    STARMAN = 0x0A
    HOME_RUN_BAT = 0x0B
    BEAM_SWORD = 0x0C
    PARASOL = 0x0D
    GREEN_SHELL_1 = 0x0E
    RED_SHELL_1 = 0x0F
    RAY_GUN = 0x10
    FREEZIE = 0x11
    FOOD = 0x12
    PROXIMITY_MINE = 0x13
    FLIPPER = 0x14
    SUPER_SCOPE = 0x15
    STAR_ROD = 0x16
    LIP_STICK = 0x17
    FAN = 0x18
    FIRE_FLOWER = 0x19
    SUPER_MUSHROOM = 0x1A
    WARP_STAR = 0x1D
    SCREW_ATTACK = 0x1E
    BUNNY_HOOD = 0x1F
    METAL_BOX = 0x20
    CLOAKING_DEVICE = 0x21
    POKE_BALL = 0x22

    # ITEM RELATED
    RAY_GUN_RECOIL_EFFECT = 0x23
    STAR_ROD_STAR = 0x24
    LIP_STICK_DUST = 0x25
    SUPER_SCOPE_BEAM = 0x26
    RAY_GUN_BEAM = 0x27
    HAMMER_HEAD = 0x28
    FLOWER = 0x29
    YOSHI_EGG_1 = 0x2A

    # MONSTERS
    GOOMBA = 0x2B
    REDEAD = 0x2C
    OCTAROK = 0x2D
    OTTOSEA = 0x2E
    STONE = 0x2F

    # CHARACTER RELATED
    MARIO_FIRE = 0x30
    DR_MARIO_PILL = 0x31
    KIRBY_CUTTER_BEAM = 0x32
    KIRBY_HAMMER = 0x33
    FOX_LASER = 0x36
    FALCO_LASER = 0x37
    FOX_SHADOW = 0x38
    FALCO_SHADOW = 0x39
    LINK_BOMB = 0x3A
    YOUNG_LINK_BOMB = 0x3B
    LINK_BOOMERANG = 0x3C
    YOUNG_LINK_BOOMERANG = 0x3D
    LINK_HOOKSHOT = 0x3E
    YOUNG_LINK_HOOKSHOT = 0x3F
    LINK_ARROW_1 = 0x40
    YOUNG_LINK_FIRE_ARROW = 0x41
    NESS_PK_FIRE = 0x42
    NESS_PK_FLASH_1 = 0x43
    NESS_PK_FLASH_2 = 0x44
    NESS_PK_THUNDER_1 = 0x45
    NESS_PK_THUNDER_2 = 0x46
    NESS_PK_THUNDER_3 = 0x47
    NESS_PK_THUNDER_4 = 0x48
    NESS_PK_THUNDER_5 = 0x49
    FOX_BLASTER = 0x4A
    FALCO_BLASTER = 0x4B
    LINK_ARROW_2 = 0x4C
    YOUNG_LINK_ARROW = 0x4D
    NESS_PK_FLASH_3 = 0x4E
    SHEIK_NEEDLE_1 = 0x4F
    SHEIK_NEEDLE_2 = 0x50
    PIKACHU_THUNDER_1 = 0x51
    PICHU_THUNDER_1 = 0x52
    MARIO_CAPE = 0x53
    DR_MARIO_CAPE = 0x54
    SHEIK_SMOKE = 0x55
    YOSHI_EGG_2 = 0x56
    YOSHI_TONGUE_1 = 0x57
    YOSHI_STAR = 0x58
    PIKACHU_THUNDER_2 = 0x59
    PIKACHU_THUNDER_3 = 0x5A
    PICHU_THUNDER_2 = 0x5B
    PICHU_THUNDER_3 = 0x5C
    SAMUS_BOMB = 0x5D
    SAMUS_CHARGESHOT = 0x5E
    SAMUS_MISSILE = 0x5F
    SAMUS_GRAPPLE_BEAM = 0x60
    SHEIK_CHAIN = 0x61
    PEACH_TURNIP = 0x63
    BOWSER_FLAME = 0x64
    NESS_BAT = 0x65
    NESS_YOYO = 0x66
    PEACH_PARASOL = 0x67
    PEACH_TOAD = 0x68
    LUIGI_FIRE = 0x69
    ICE_CLIMBERS_ICE = 0x6A
    ICE_CLIMBERS_BLIZZARD = 0x6B
    ZELDA_FIRE_1 = 0x6C
    ZELDA_FIRE_2 = 0x6D
    PEACH_TOAD_SPORE = 0x6F
    MEWTWO_SHADOWBALL = 0x70
    ICE_CLIMBERS_UP_B = 0x71
    GAME_AND_WATCH_PESTICIDE = 0x72
    GAME_AND_WATCH_MANHOLE = 0x73
    GAME_AND_WATCH_FIRE = 0x74
    GAME_AND_WATCH_PARACHUTE = 0x75
    GAME_AND_WATCH_TURTLE = 0x76
    GAME_AND_WATCH_SPERKY = 0x77
    GAME_AND_WATCH_JUDGE = 0x78
    GAME_AND_WATCH_SAUSAGE = 0x7A
    GAME_AND_WATCH_MILK = 0x7B
    GAME_AND_WATCH_FIREFIGHTER = 0x7C
    MASTER_HAND_LASER = 0x7D
    MASTER_HAND_BULLET = 0x7E
    CRAZY_HAND_LASER = 0x7F
    CRAZY_HAND_BULLET = 0x80
    CRAZY_HAND_BOMB = 0x81
    KIRBY_COPY_MARIO_FIRE = 0x82
    KIRBY_COPY_DR_MARIO_PILL = 0x83
    KIRBY_COPY_LUIGI_FIRE = 0x84
    KIRBY_COPY_ICE_CLIMBERS_ICE = 0x85
    KIRBY_COPY_PEACH_TOAD = 0x86
    KIRBY_COPY_TOAD_SPORE = 0x87
    KIRBY_COPY_FOX_LASER = 0x88
    KIRBY_COPY_FALCO_LASER = 0x89
    KIRBY_COPY_FOX_BLASTER = 0x8A
    KIRBY_COPY_FALCO_BLASTER = 0x8B
    KIRBY_COPY_LINK_ARROW_1 = 0x8C
    KIRBY_COPY_YOUNG_LINK_ARROW_1 = 0x8D
    KIRBY_COPY_LINK_ARROW_2 = 0x8E
    KIRBY_COPY_YOUNG_LINK_ARROW_2 = 0x8F
    KIRBY_COPY_MEWTWO_SHADOWBALL = 0x90
    KIRBY_COPY_PK_FLASH = 0x91
    KIRBY_COPY_PK_FLASH_EXPLOSION = 0x92
    KIRBY_COPY_PIKACHU_THUNDER_1 = 0x93
    KIRBY_COPY_PIKACHU_THUNDER_2 = 0x94
    KIRBY_COPY_PICHU_THUNDER_1 = 0x95
    KIRBY_COPY_PICHU_THUNDER_2 = 0x96
    KIRBY_COPY_SAMUS_CHARGESHOT = 0x97
    KIRBY_COPY_SHEIK_NEEDLE_1 = 0x98
    KIRBY_COPY_SHEIK_NEEDLE_2 = 0x99
    KIRBY_COPY_BOWSER_FLAME = 0x9A
    KIRBY_COPY_GAME_AND_WATCH_SAUSAGE = 0x9B
    YOSHI_TONGUE_2 = 0x9D
    MARIO_LUIGI_COIN = 0x9F

    # POKEMON
    RANDOM_POKEMON = 0xA0
    GOLDEEN = 0xA1
    CHICORITA = 0xA2
    SNORLAX = 0xA3
    BLASTOISE = 0xA4
    WEEZING = 0xA5
    CHARIZARD = 0xA6
    MOLTRES = 0xA7
    ZAPDOS = 0xA8
    ARTICUNO = 0xA9
    WOBBUFFET = 0xAA
    SCIZOR = 0xAB
    UNOWN = 0xAC
    ENTEI = 0xAD
    RAIKOU = 0xAE
    SUICUNE = 0xAF
    BELLOSSOM = 0xB0
    ELECTRODE = 0xB1
    LUGIA = 0xB2
    HO_OH = 0xB3
    DITTO = 0xB4
    CLEFAIRY = 0xB5
    TOGEPI = 0xB6
    MEW = 0xB7
    CELEBI = 0xB8
    STARYU = 0xB9
    CHANSEY = 0xBA
    PORYGON = 0xBB
    CYNDAQUIL = 0xBC
    MARILL = 0xBD
    VENUSAUR = 0xBE

    # POKEMON RELATED
    CHICORITA_LEAF = 0xBF
    BLASTOISE_WATER = 0xC0
    WEEZING_GAS_1 = 0xC1
    WEEZING_GAS_2 = 0xC2
    CHARIZARD_BREATH_1 = 0xC3
    CHARIZARD_BREATH_2 = 0xC4
    CHARIZARD_BREATH_3 = 0xC5
    CHARIZARD_BREATH_4 = 0xC6
    MINI_UNOWNS = 0xC7
    LUGIA_AEROBLAST_1 = 0xC8
    LUGIA_AEROBLAST_2 = 0xC9
    LUGIA_AEROBLAST_3 = 0xCA
    HO_OH_FLAME = 0xCB
    STARYU_STAR = 0xCC
    HEALING_EGG = 0xCD
    CYNDAQUIL_FIRE = 0xCE

    # MONSTERS
    OLD_GOOMBA = 0xD0
    TARGET = 0xD1
    SHYGUY = 0xD2
    KOOPA_1 = 0xD3
    KOOPA_2 = 0xD4
    LIKE_LIKE = 0xD5
    OLD_OTTOSEA = 0xD8
    WHITE_BEAR = 0xD9
    KLAP = 0xDA
    GREEN_SHELL_2 = 0xDB
    RED_SHELL_2 = 0xDC

    # STAGE SPECIFIC
    TINGLE = 0xDD
    APPLE = 0xE1
    HEALING_APPLE = 0xE2
    TOOL = 0xE6
    BIRDO = 0xE9
    ARWING_LASER = 0xEA
    GREAT_FOX_LASER = 0xEB
    BIRDO_EGG = 0xEC


class TurnipFace(IntEnum):
    # TODO verify this
    SMILEY = 0
    BORED = 1
    SLEEPY = 2
    SHOCKED = 3
    LAUGHING = 4
    WINK = 5
    DOT = 6
    STITCH = 7
