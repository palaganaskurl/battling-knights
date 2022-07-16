from dataclasses import dataclass


@dataclass
class Item:
    name: str
    attack: int
    defense: int
    current_pos_x: int
    current_pos_y: int

    def __post_init__(self):
        self.representation = self.name[0]
