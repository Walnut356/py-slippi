# These IDs (and other very useful info for this project) came from the SSBM Data Sheet: https://docs.google.com/spreadsheets/d/1JX2w-r2fuvWuNgGb6D3Cs4wHQKLFegZe2jhbBuIhCG8

from .util import *

# Use reference: https://docs.google.com/spreadsheets/d/1JX2w-r2fuvWuNgGb6D3Cs4wHQKLFegZe2jhbBuIhCG8/edit#gid=13

# To check if an action state is zero-indexed:https://github.com/altf4/libmelee/blob/master/melee/actiondata.csv
# I might add some form of check in here, but for now i just handle it manually.

class ActionState(IntEnum):
# ID Ranges - used to simplify checks for stat calculators
    DAMAGE_START = 75
    DAMAGE_END = 91
    CAPTURE_START = 223
    CAPTURE_END = 232
    GUARD_START = 178
    GUARD_END = 182
    GUARD_BREAK_START = 205
    GUARD_BREAK_END = 211
    GROUNDED_CONTROL_START = 14
    GROUNDED_CONTROL_END = 24
    LEDGE_ACTION_START = 252
    LEDGE_ACTION_END = 263
    SQUAT_START = 39
    SQUAT_END = 41
    DOWN_START = 183
    DOWN_END = 198
    TECH_START = 199
    TECH_END = 204
    DODGE_START = 233
    DODGE_END = 236
    DYING_START = 0
    DYING_END = 10
    CONTROLLED_JUMP_START = 24
    CONTROLLED_JUMP_END = 34
    GROUND_ATTACK_START = 44
    GROUND_ATTACK_END = 64
    AERIAL_ATTACK_START = 65
    AERIAL_ATTACK_END = 74
# Command Grabs
    COMMAND_GRAB_RANGE1_START = 266
    COMMAND_GRAB_RANGE1_END = 304

    COMMAND_GRAB_RANGE2_START = 327
    COMMAND_GRAB_RANGE2_END = 338

# Individual IDs
    DEAD_DOWN = 0 # Bottom blast zone death
    DEAD_LEFT = 1 # Left blast zone death
    DEAD_RIGHT = 2 # Right blast zone death
    DEAD_UP = 3 # Up blast zone death used in 1P "Team Kirby", etc.
    DEAD_UP_STAR = 4 # Standard star KO
    DEAD_UP_STAR_ICE = 5 # Star KO while encased in ice
    DEAD_UP_FALL = 6 # 64-esque front fall, likely unused per OG Modders
    DEAD_UP_FALL_HIT_CAMERA = 7
    DEAD_UP_FALL_HIT_CAMERA_FLAT = 8
    DEAD_UP_FALL_ICE = 9
    DEAD_UP_FALL_HIT_CAMERA_ICE = 10

    SLEEP = 11 # "Nothing" state, probably - used as shiek/zelda state when the other is active

    REBIRTH = 12 # Entering on halo
    REBIRTH_WAIT = 13 # Waiting on halo

    WAIT = 14 # Default standing state
    WALK_SLOW = 15
    WALK_MIDDLE = 16
    WALK_FAST = 17
    TURN = 18
    TURN_RUN = 19 # Slow sliding turnaround when in full run
    DASH = 20
    RUN = 21
    RUN_DIRECT = 22
    RUN_BRAKE = 23
    KNEE_BEND = 24 # Jumpsquat
    JUMP_F = 25 # First jump, forward
    JUMP_B = 26 # First jump, backwards
    JUMP_AERIAL_F = 27 # Aerial jump forward
    JUMP_AERIAL_B = 28 # Aerial jump backward
    FALL = 29 # Default fall
    FALL_F = 30 # Fall forward DI
    FALL_B = 31 # Fall backward DI
    FALL_AERIAL = 32 # Fall after second jump
    FALL_AERIAL_F = 33 # Fall after second jump, forward DI
    FALL_AERIAL_B = 34 # Fall after second jump, backward DI
    FALL_SPECIAL = 35 # Non-actionable fall used after Up B, air dodge, and some B moves
    FALL_SPECIAL_F = 36 # Non-actionable fall, forward DI
    FALL_SPECIAL_B = 37 # Non-actionable fall, backward DI
    DAMAGE_FALL = 38 # Tumble
    SQUAT = 39 # Stand -> Crouch
    SQUAT_WAIT = 40 # Full crouch
    SQUAT_RV = 41 # Crouch -> Stand
    LAND = 42 # Universal no-action landing lag, fully interruptable
    LAND_FALL_SPECIAL = 43 # Landing from FALL_SPECIAL[_F/B]

    ATTACK_11 = 44 # Jab 1
    ATTACK_12 = 45 # Jab 2
    ATTACK_13 = 46 # Jab 3
    ATTACK_100_START = 47 # Rapid jab start
    ATTACK_100_LOOP = 48 # Rapid jab loop
    ATTACK_100_END = 49 # Rapid jab end
    ATTACK_DASH = 50 # Dash attack
    ATTACK_S_3_HI = 51 # Up-angled Ftilt
    ATTACK_S_3_HI_S = 52 # Slight up-angled F-tilt
    ATTACK_S_3_S = 53 # No angle Ftilt
    ATTACK_S_3_LW_S = 54 # Slight down-angled Ftilt
    ATTACK_S_3_LW = 55 # Down-angled Ftilt
    ATTACK_HI_3 = 56 # Utilt
    ATTACK_LW_3 = 57 # Dtilt
    ATTACK_S_4_HI = 58 # Up-angled Fsmash
    ATTACK_S_4_HI_S = 59 # Slight up-angled Fsmash
    ATTACK_S_4_S = 60 # No angle Fsmash
    ATTACK_S_4_LW_S = 61 # Slight down-angled Fsmash
    ATTACK_S_4_LW = 62 # Down-angled Fsmash
    ATTACK_HI_4 = 63 # Usmash
    ATTACK_LW_4 = 64 # Dsmash
    ATTACK_AIR_N = 65 # Nair
    ATTACK_AIR_F = 66 # Fair
    ATTACK_AIR_B = 67 # Bair
    ATTACK_AIR_HI = 68 # Uair
    ATTACK_AIR_LW = 69 # Dair
    LANDING_AIR_N = 70 # Nair landing animation
    LANDING_AIR_F = 71 # Fair landing animation
    LANDING_AIR_B = 72 # Bair landing animation
    LANDING_AIR_HI = 73 # Uair landing animation
    LANDING_AIR_LW = 74 # Dair landing animation

    DAMAGE_HI_1 = 75 # Start of generic damage animations
    DAMAGE_HI_2 = 76
    DAMAGE_HI_3 = 77
    DAMAGE_N_1 = 78
    DAMAGE_N_2 = 79
    DAMAGE_N_3 = 80
    DAMAGE_LW_1 = 81
    DAMAGE_LW_2 = 82
    DAMAGE_LW_3 = 83
    DAMAGE_AIR_1 = 84
    DAMAGE_AIR_2 = 85
    DAMAGE_AIR_3 = 86
    DAMAGE_FLY_HI = 87
    DAMAGE_FLY_N = 88
    DAMAGE_FLY_LW = 89
    DAMAGE_FLY_TOP = 90
    DAMAGE_FLY_ROLL = 91 # End of generic damage animations

    LIGHT_GET = 92 # Picking up most items
    HEAVY_GET = 93 # Picking up heavy items (Barrel)
    LIGHT_THROW_F = 94 # Start of item throw
    LIGHT_THROW_B = 95
    LIGHT_THROW_HI = 96
    LIGHT_THROW_LW = 97
    LIGHT_THROW_DASH = 98
    LIGHT_THROW_DROP = 99
    LIGHT_THROW_AIR_F = 100
    LIGHT_THROW_AIR_B = 101
    LIGHT_THROW_AIR_HI = 102
    LIGHT_THROW_AIR_LW = 103
    HEAVY_THROW_F = 104
    HEAVY_THROW_B = 105
    HEAVY_THROW_HI = 106
    HEAVY_THROW_LW = 107
    LIGHT_THROW_F_4 = 108 # Smash throw start
    LIGHT_THROW_B_4 = 109
    LIGHT_THROW_HI_4 = 110
    LIGHT_THROW_LW_4 = 111
    LIGHT_THROW_AIR_F_4 = 112
    LIGHT_THROW_AIR_B_4 = 113
    LIGHT_THROW_AIR_HI_4 = 114
    LIGHT_THROW_AIR_LW_4 = 115
    HEAVY_THROW_F_4 = 116
    HEAVY_THROW_B_4 = 117
    HEAVY_THROW_HI_4 = 118
    HEAVY_THROW_LW_4 = 119 # End of item throw
    SWORD_SWING_1 = 120 # Start of item-specific animations
    SWORD_SWING_3 = 121
    SWORD_SWING_4 = 122
    SWORD_SWING_DASH = 123
    BAT_SWING_1 = 124
    BAT_SWING_3 = 125
    BAT_SWING_4 = 126
    BAT_SWING_DASH = 127
    PARASOL_SWING_1 = 128
    PARASOL_SWING_3 = 129
    PARASOL_SWING_4 = 130
    PARASOL_SWING_DASH = 131
    HARISEN_SWING_1 = 132
    HARISEN_SWING_3 = 133
    HARISEN_SWING_4 = 134
    HARISEN_SWING_DASH = 135
    STAR_ROD_SWING_1 = 136
    STAR_ROD_SWING_3 = 137
    STAR_ROD_SWING_4 = 138
    STAR_ROD_SWING_DASH = 139
    LIP_STICK_SWING_1 = 140
    LIP_STICK_SWING_3 = 141
    LIP_STICK_SWING_4 = 142
    LIP_STICK_SWING_DASH = 143
    ITEM_PARASOL_OPEN = 144
    ITEM_PARASOL_FALL = 145
    ITEM_PARASOL_FALL_SPECIAL = 146
    ITEM_PARASOL_DAMAGE_FALL = 147
    L_GUN_SHOOT = 148
    L_GUN_SHOOT_AIR = 149
    L_GUN_SHOOT_EMPTY = 150
    L_GUN_SHOOT_AIR_EMPTY = 151
    FIRE_FLOWER_SHOOT = 152
    FIRE_FLOWER_SHOOT_AIR = 153
    ITEM_SCREW = 154
    ITEM_SCREW_AIR = 155
    DAMAGE_SCREW = 156
    DAMAGE_SCREW_AIR = 157
    ITEM_SCOPE_START = 158
    ITEM_SCOPE_RAPID = 159
    ITEM_SCOPE_FIRE = 160
    ITEM_SCOPE_END = 161
    ITEM_SCOPE_AIR_START = 162
    ITEM_SCOPE_AIR_RAPID = 163
    ITEM_SCOPE_AIR_FIRE = 164
    ITEM_SCOPE_AIR_END = 165
    ITEM_SCOPE_START_EMPTY = 166
    ITEM_SCOPE_RAPID_EMPTY = 167
    ITEM_SCOPE_FIRE_EMPTY = 168
    ITEM_SCOPE_END_EMPTY = 169
    ITEM_SCOPE_AIR_START_EMPTY = 170
    ITEM_SCOPE_AIR_RAPID_EMPTY = 171
    ITEM_SCOPE_AIR_FIRE_EMPTY = 172
    ITEM_SCOPE_AIR_END_EMPTY = 173 # End of item-specific animations

    LIFT_WAIT = 174 # Not sure what these 4 are
    LIFT_WALK_1 = 175
    LIFT_WALK_2 = 176
    LIFT_TURN = 177

    GUARD_ON = 178 # Raising shield
    GUARD = 179 # Holding shield
    GUARD_OFF = 180 # Releasing shield
    GUARD_SET_OFF = 181 # Shield stun
    GUARD_REFLECT = 182 # Powershield

    DOWN_BOUND_U = 183 # Missed tech bounce, facing upwards
    DOWN_WAIT_U = 184 # Downed, facing up
    DOWN_DAMAGE_U = 185 # Jab reset while laying facing up
    DOWN_STAND_U = 186 # Neutral getup, facing up
    DOWN_ATTACK_U = 187 # Getup attack, facing up
    DOWN_FOWARD_U = 188 # Missed tech roll forward
    DOWN_BACK_U = 189 # Missed tech roll backward
    DOWN_SPOT_U = 190 # Does not appear to be used
    DOWN_BOUND_D = 191 # Missed tech bounce, facing down
    DOWN_WAIT_D = 192 # Downed, facing down
    DOWN_DAMAGE_D = 193 # Hit while laying on ground, facing down
    DOWN_STAND_D = 194 # Neutral getup, facing down
    DOWN_ATTACK_D = 195 # Getup attack, facing down
    DOWN_FOWARD_D = 196 # Missed tech roll forward
    DOWN_BACK_D = 197 # Missed tech roll backward
    DOWN_SPOT_D = 198 # Does not appear to be used
    PASSIVE = 199 # Neutral tech
    PASSIVE_STAND_F = 200 # Forward tech
    PASSIVE_STAND_B = 201 # Backward tech
    PASSIVE_WALL = 202 # Wall tech
    PASSIVE_WALL_JUMP = 203 # Walljump and Walljump tech
    PASSIVE_CEIL = 204 # Ceiling tech

    SHIELD_BREAK_FLY = 205 # Initial bounce when shield is broken
    SHIELD_BREAK_FALL = 206 # Fall during shield break
    SHIELD_BREAK_DOWN_U = 207
    SHIELD_BREAK_DOWN_D = 208
    SHIELD_BREAK_STAND_U = 209
    SHIELD_BREAK_STAND_D = 210
    FURA_FURA = 211 # Shield break totter

    CATCH = 212 # Grab
    CATCH_PULL = 213 # Successful grab, pulling opponent in
    CATCH_DASH = 214 # Dash grab
    CATCH_DASH_PULL = 215 # Successful dash grab, pulling opponent in
    CATCH_WAIT = 216 # Grab hold
    CATCH_ATTACK = 217 # Pummel
    CATCH_CUT = 218 # Grab release
    THROW_F = 219 # Fthrow
    THROW_B = 220 # Bthrow
    THROW_HI = 221 # Uthrow
    THROW_LW = 222 # Dthrow
    CAPTURE_PULLED_HI = 223
    CAPTURE_WAIT_HI = 224
    CAPTURE_DAMAGE_HI = 225
    CAPTURE_PULLED_LW = 226 # Being grabbed and pulled
    CAPTURE_WAIT_LW = 227 # Grabbed and held
    CAPTURE_DAMAGE_LW = 228 # Pummeled
    CAPTURE_CUT = 229 # Grab release
    CAPTURE_JUMP = 230 # Jumping mash out
    CAPTURE_NECK = 231 # Does not appear to be used
    CAPTURE_FOOT = 232 # Does not appear to be used

    ESCAPE_F = 233 # Shield roll forward
    ESCAPE_B = 234 # Shield roll backward
    ESCAPE = 235 # Spot dodge
    ESCAPE_AIR = 236 # Airdodge

    REBOUND_STOP = 237
    REBOUND = 238

    THROWN_F = 239 # Receiving Fthrow
    THROWN_B = 240 # Receiving Bthrow
    THROWN_HI = 241 # Receiving Uthrow
    THROWN_LW = 242 # Receiving Dthrow
    THROWN_LW_WOMEN = 243

    PASS = 244 # Drop through platform
    OTTOTTO = 245 # Ledge teeter
    OTTOTTO_WAIT = 246 # Teeter loop?
    FLY_REFLECT_WALL = 247 # Missed walltech
    FLY_REFLECT_CEIL = 248 # Missed ceiling tech
    STOP_WALL = 249 # Wall bonk
    STOP_CEIL = 250 # Ceiling bonk
    MISS_FOOT = 251 # Backward shield slideoff

    # Ledge actions
    CLIFF_CATCH = 252 # Ledge grab
    CLIFF_WAIT = 253 # Ledge hang
    CLIFF_CLIMB_SLOW = 254 # Regular getup >100%
    CLIFF_CLIMB_QUICK = 255 # Regular getup <100%
    CLIFF_ATTACK_SLOW = 256 # Ledge attack >100%
    CLIFF_ATTACK_QUICK = 257 # Ledge attack <100%
    CLIFF_ESCAPE_SLOW = 258 # Ledge roll >100%
    CLIFF_ESCAPE_QUICK = 259 # Ledge roll <100%
    CLIFF_JUMP_SLOW_1 = 260 # Ledge jump >100%
    CLIFF_JUMP_SLOW_2 = 261 # Ledge jump >100%
    CLIFF_JUMP_QUICK_1 = 262 # Ledge jump <100%
    CLIFF_JUMP_QUICK_2 = 263 # Ledge jump <100%

    APPEAL_R = 264 # Taunt facing right
    APPEAL_L = 265 # Taunt facing left

    # Command grabs
    SHOULDERED_WAIT = 266 # DK cargo carry
    SHOULDERED_WALK_SLOW = 267
    SHOULDERED_WALK_MIDDLE = 268
    SHOULDERED_WALK_FAST = 269
    SHOULDERED_TURN = 270
    THROWN_F_F = 271 # DK cargo throws
    THROWN_F_B = 272
    THROWN_F_HI = 273
    THROWN_F_LW = 274

    CAPTURE_CAPTAIN = 275 # Falcon up B grab
    CAPTURE_YOSHI = 276 # TODO Yoshi Z grab?
    YOSHI_EGG = 277 # Yoshi neutral b grab?
    CAPTURE_KOOPA = 278 # Koopa claw
    CAPTURE_DAMAGE_KOOPA = 279
    CAPTURE_WAIT_KOOPA = 280
    THROWN_KOOPA_F = 281
    THROWN_KOOPA_B = 282
    CAPTURE_KOOPA_AIR = 283
    CAPTURE_DAMAGE_KOOPA_AIR = 284
    CAPTURE_WAIT_KOOPA_AIR = 285
    THROWN_KOOPA_AIR_F = 286
    THROWN_KOOPA_AIR_B = 287
    CAPTURE_KIRBY = 288 # Kirby succ
    CAPTURE_WAIT_KIRBY = 289
    THROWN_KIRBY_STAR = 290 # Kirby spit
    THROWN_COPY_STAR = 291 # Kirby swallow?
    THROWN_KIRBY = 292
    BARREL_WAIT = 293 # I think this is used for the barrel on DK jungle 64?

    BURY = 294 # Stuck in ground by DK side b or similar
    BURY_WAIT = 295
    BURY_JUMP = 296

    DAMAGE_SONG = 297 # Put to sleep by Jiggs sing or similar
    DAMAGE_SONG_WAIT = 298
    DAMAGE_SONG_RV = 299

    DAMAGE_BIND = 300 # Hit by Mewtwo disable
    CAPTURE_MEWTWO = 301 # Does not appear to be used
    CAPTURE_MEWTWO_AIR = 302 # Does not appear to be used
    THROWN_MEWTWO = 303 # Hit by Mewtwo confusion
    THROWN_MEWTWO_AIR = 304 # Hit by Mewtwo's confusion in the air

    # Item specific actions
    WARP_STAR_JUMP = 305
    WARP_STAR_FALL = 306
    HAMMER_WAIT = 307
    HAMMER_WALK = 308
    HAMMER_TURN = 309
    HAMMER_KNEE_BEND = 310
    HAMMER_FALL = 311
    HAMMER_JUMP = 312
    HAMMER_LANDING = 313
    KINOKO_GIANT_START = 314 #super/poison mushroom states
    KINOKO_GIANT_START_AIR = 315
    KINOKO_GIANT_END = 316
    KINOKO_GIANT_END_AIR = 317
    KINOKO_SMALL_START = 318
    KINOKO_SMALL_START_AIR = 319
    KINOKO_SMALL_END = 320
    KINOKO_SMALL_END_AIR = 321

    ENTRY = 322 # Beginning of the match warp in
    ENTRY_START = 323
    ENTRY_END = 324

    DAMAGE_ICE = 325
    DAMAGE_ICE_JUMP = 326
    CAPTURE_MASTER_HAND = 327
    CAPTURE_DAMAGE_MASTER_HAND = 328
    CAPTURE_WAIT_MASTER_HAND = 329
    THROWN_MASTER_HAND = 330
    CAPTURE_KIRBY_YOSHI = 331
    KIRBY_YOSHI_EGG = 332
    CAPTURE_REDEAD = 333
    CAPTURE_LIKE_LIKE = 334

    DOWN_REFLECT = 335 # A very rare action state where the character transitions from a DownBoundU or DownBoundD (missed tech) state
                       # into a wall bounce. This state is not techable and neither is the probable next floor hit. 
                       # Most commonly encountered on Pokémon Stadium

    CAPTURE_CRAZY_HAND = 336
    CAPTURE_DAMAGE_CRAZY_HAND = 337
    CAPTURE_WAIT_CRAZY_HAND = 338
    THROWN_CRAZY_HAND = 339
    BARREL_CANNON_WAIT = 340
    
    # No general action states past this point used, it's all character-specific action states
    WAIT_1 = 341
    WAIT_2 = 342
    WAIT_3 = 343
    WAIT_4 = 344
    WAIT_ITEM = 345
    SQUAT_WAIT_1 = 346
    SQUAT_WAIT_2 = 347
    SQUAT_WAIT_ITEM = 348
    GUARD_DAMAGE = 349
    ESCAPE_N = 350
    ATTACK_S_4_HOLD = 351
    HEAVY_WALK_1 = 352
    HEAVY_WALK_2 = 353
    ITEM_HAMMER_WAIT = 354
    ITEM_HAMMER_MOVE = 355
    ITEM_BLIND = 356
    DAMAGE_ELEC = 357
    FURA_SLEEP_START = 358
    FURA_SLEEP_LOOP = 359
    FURA_SLEEP_END = 360
    WALL_DAMAGE = 361
    CLIFF_WAIT_1 = 362
    CLIFF_WAIT_2 = 363
    SLIP_DOWN = 364
    SLIP = 365
    SLIP_TURN = 366
    SLIP_DASH = 367
    SLIP_WAIT = 368
    SLIP_STAND = 369
    SLIP_ATTACK = 370
    SLIP_ESCAPE_F = 371
    SLIP_ESCAPE_B = 372
    APPEAL_S = 373
    ZITABATA = 374
    CAPTURE_KOOPA_HIT = 375
    THROWN_KOOPA_END_F = 376
    THROWN_KOOPA_END_B = 377
    CAPTURE_KOOPA_AIR_HIT = 378
    THROWN_KOOPA_AIR_END_F = 379
    THROWN_KOOPA_AIR_END_B = 380
    THROWN_KIRBY_DRINK_S_SHOT = 381
    THROWN_KIRBY_SPIT_S_SHOT = 382


class CSSCharacter(IntEnum):
    CAPTAIN_FALCON = 0
    DONKEY_KONG = 1
    FOX = 2
    GAME_AND_WATCH = 3
    KIRBY = 4
    BOWSER = 5
    LINK = 6
    LUIGI = 7
    MARIO = 8
    MARTH = 9
    MEWTWO = 10
    NESS = 11
    PEACH = 12
    PIKACHU = 13
    ICE_CLIMBERS = 14
    JIGGLYPUFF = 15
    SAMUS = 16
    YOSHI = 17
    ZELDA = 18
    SHEIK = 19
    FALCO = 20
    YOUNG_LINK = 21
    DR_MARIO = 22
    ROY = 23
    PICHU = 24
    GANONDORF = 25
    MASTER_HAND = 26
    WIREFRAME_MALE = 27
    WIREFRAME_FEMALE = 28
    GIGA_BOWSER = 29
    CRAZY_HAND = 30
    SANDBAG = 31
    POPO = 32

    @classmethod
    def from_internal_id(cls, internal_id):
        char = InGameCharacter(internal_id)
        if char is InGameCharacter.NANA or char is InGameCharacter.POPO:
            return cls.ICE_CLIMBERS
        else:
            return cls[char.name]


class InGameCharacter(IntEnum):
    MARIO = 0
    FOX = 1
    CAPTAIN_FALCON = 2
    DONKEY_KONG = 3
    KIRBY = 4
    BOWSER = 5
    LINK = 6
    SHEIK = 7
    NESS = 8
    PEACH = 9
    POPO = 10
    NANA = 11
    PIKACHU = 12
    SAMUS = 13
    YOSHI = 14
    JIGGLYPUFF = 15
    MEWTWO = 16
    LUIGI = 17
    MARTH = 18
    ZELDA = 19
    YOUNG_LINK = 20
    DR_MARIO = 21
    FALCO = 22
    PICHU = 23
    GAME_AND_WATCH = 24
    GANONDORF = 25
    ROY = 26
    MASTER_HAND = 27
    CRAZY_HAND = 28
    WIREFRAME_MALE = 29
    WIREFRAME_FEMALE = 30
    GIGA_BOWSER = 31
    SANDBAG = 32


class Stage(IntEnum):
    FOUNTAIN_OF_DREAMS = 2
    POKEMON_STADIUM = 3
    PRINCESS_PEACHS_CASTLE = 4
    KONGO_JUNGLE = 5
    BRINSTAR = 6
    CORNERIA = 7
    YOSHIS_STORY = 8
    ONETT = 9
    MUTE_CITY = 10
    RAINBOW_CRUISE = 11
    JUNGLE_JAPES = 12
    GREAT_BAY = 13
    HYRULE_TEMPLE = 14
    BRINSTAR_DEPTHS = 15
    YOSHIS_ISLAND = 16
    GREEN_GREENS = 17
    FOURSIDE = 18
    MUSHROOM_KINGDOM_I = 19
    MUSHROOM_KINGDOM_II = 20
    VENOM = 22
    POKE_FLOATS = 23
    BIG_BLUE = 24
    ICICLE_MOUNTAIN = 25
    ICETOP = 26
    FLAT_ZONE = 27
    DREAM_LAND_N64 = 28
    YOSHIS_ISLAND_N64 = 29
    KONGO_JUNGLE_N64 = 30
    BATTLEFIELD = 31
    FINAL_DESTINATION = 32


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
