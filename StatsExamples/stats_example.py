from pathlib import Path
from math import isclose
import timeit

from slippi import *

file = Path(r"Modern Replays/ACTI#799 (Falcon) vs NUT#356 (Falco) on FoD - 12-15-22 02.06am .slp")

replay = Game(file)

thing = StatsComputer()
thing.prime_replay(file)
thing.stats_compute("NUT#356")

left = [wavedash for wavedash in thing.data.wavedash if wavedash.direction == event.Direction.LEFT]
right = [wavedash for wavedash in thing.data.wavedash if wavedash.direction == event.Direction.RIGHT]

lsum = 0
rsum = 0

for wavedash in left:
    lsum += wavedash.angle

lsum = lsum / len(left)

for wavedash in right:
    rsum += wavedash.angle

rsum = rsum / len(right)

print(len(left), lsum)
print(len(right), rsum)
# print("KB angle: ", thing.sdis[i].knockback_angle)
# print("KB Velocity: ", thing.sdis[i].knockback_velocity)
# print("DI angle: ", thing.sdis[i].di_angle)
# print("Max DI Angles: ", common.max_di_angles(thing.sdis[i].knockback_angle))
# print("Final Knockback Angle: ", thing.sdis[i].final_knockback_angle)
# print("Final Knockback Velocity: ", thing.sdis[i].final_knockback_velocity)