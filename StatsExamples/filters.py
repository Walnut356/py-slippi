from typing import List

from slippi import event, combo

def filter_direction(stats: List, direction: event.Direction) -> List:
    if hasattr(stats[0], "direction"):
        return [stat for stat in stats if stat.direction == direction]
    else:
        return stats

def filter_length(combos: List[combo.ComboData], min_length: int=0, max_length: int=100) -> List[combo.ComboData]:
    return [combo for combo in combos if min_length <= len(combo.moves) <= max_length]

def filter_damage(combos: List[combo.ComboData], min_damage: int=0, max_damage: int=1000) -> List[combo.ComboData]:
    return [combo for combo in combos if min_damage <= combo.total_damage() <= max_damage]
