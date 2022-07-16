from dataclasses import dataclass, field
from enum import Enum
from typing import Union, Optional

from directions import Directions
from item import Item


class KnightDrowned(Exception):
    ...


class KnightStatus(str, Enum):
    LIVE = 'live'
    DEAD = 'dead'
    DROWNED = 'drowned'


@dataclass
class Knight:
    color: str
    current_pos_x: Union[int, None]
    current_pos_y: Union[int, None]
    item: Optional[Item] = None
    attack: int = 1
    defense: int = 1
    status: KnightStatus = KnightStatus.LIVE

    @property
    def total_attack(self):
        if self.status == KnightStatus.DEAD:
            return 0

        if self.item:
            return self.item.attack + self.attack

        return self.attack

    @property
    def total_defense(self):
        if self.status == KnightStatus.DEAD:
            return 0

        if self.item:
            return self.item.defense + self.defense

        return self.defense

    def __post_init__(self):
        self.representation = self.color[0]

    def move(self, direction):
        # TODO: n to Davy Jones' Locker - the item is left on
        #  the last valid tile that the knight was on.

        if direction == Directions.NORTH.value:
            self.current_pos_x -= 1

            if self.current_pos_x < 0:
                self.drown_knight()
        elif direction == Directions.SOUTH.value:
            self.current_pos_x += 1

            if self.current_pos_x > 7:
                self.drown_knight()
        elif direction == Directions.WEST.value:
            self.current_pos_y -= 1

            if self.current_pos_x < 0:
                self.drown_knight()
        elif direction == Directions.EAST.value:
            self.current_pos_y += 1

            if self.current_pos_x > 7:
                self.drown_knight()

    def drown_knight(self):
        self.current_pos_x = None
        self.current_pos_y = None
        self.status = KnightStatus.DROWNED

        raise KnightDrowned()

    def fight(self, knight):
        # Add 0.5 to attacker
        temporary_attack_damage = self.total_attack + 0.5

        return temporary_attack_damage > knight.total_defense
