from dataclasses import dataclass
from enum import Enum
from typing import Optional
from typing import Union

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
        if self.status != KnightStatus.LIVE:
            return 0

        if self.item:
            return self.item.attack + self.attack

        return self.attack

    @property
    def total_defense(self):
        if self.status != KnightStatus.LIVE:
            return 0

        if self.item:
            return self.item.defense + self.defense

        return self.defense

    def __post_init__(self):
        self.representation = self.color[0]

    def move(self, direction):
        if direction == Directions.NORTH.value:
            self.current_pos_x -= 1

            if self.current_pos_x < 0:
                self.drown_knight()

            if self.item:
                self.item.current_pos_x -= 1
        elif direction == Directions.SOUTH.value:
            self.current_pos_x += 1

            if self.current_pos_x > 7:
                self.drown_knight()

            if self.item:
                self.item.current_pos_x += 1
        elif direction == Directions.WEST.value:
            self.current_pos_y -= 1

            if self.current_pos_y < 0:
                self.drown_knight()

            if self.item:
                self.item.current_pos_y -= 1
        elif direction == Directions.EAST.value:
            self.current_pos_y += 1

            if self.current_pos_y > 7:
                self.drown_knight()

            if self.item:
                self.item.current_pos_y += 1

    def drown_knight(self):
        self.status = KnightStatus.DROWNED

        raise KnightDrowned()

    def fight(self, knight):
        # Add 0.5 to attacker
        temporary_attack_damage = self.total_attack + 0.5

        return temporary_attack_damage > knight.total_defense
