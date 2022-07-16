from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Union, List

from directions import Directions
from item import Item
from knight import Knight, KnightDrowned, KnightStatus


@dataclass
class ArenaPosition:
    x: int
    y: int
    knight: Optional[Knight] = None
    items: List[Item] = field(default_factory=list)

    def remove_item(self, remove_item: Item):
        updated_items = []

        for item in self.items:
            if item.representation == remove_item.representation:
                continue

            updated_items.append(item)

        self.items = updated_items


class Arena:
    def __init__(self, knights: list[Knight], items: list[Item]):
        self.row = 8
        self.col = 8
        self.knights = {
            knight.representation: knight for knight in knights
        }
        self.items = {
            item.representation: item for item in items
        }
        self.board = self._generate_board()

        self._set_knights_initial_state()
        self._set_items_initial_state()

    def _generate_board(self) -> list[list[ArenaPosition]]:
        board = []

        for i in range(self.row):
            board.append([])

            for j in range(self.col):
                board[i].append(ArenaPosition(x=i, y=j))

        return board

    def _set_knights_initial_state(self):
        for knight in self.knights.values():
            self.board[knight.current_pos_x][knight.current_pos_y] = ArenaPosition(
                x=knight.current_pos_x, y=knight.current_pos_y, knight=knight
            )

    def _set_items_initial_state(self):
        for item in self.items.values():
            self.board[item.current_pos_x][item.current_pos_y] = ArenaPosition(
                x=item.current_pos_x, y=item.current_pos_y, items=[item]
            )

    def _move_knight(self, knight: Knight, direction: str) -> Knight:
        # Set the position where the knight came from to None
        self.board[knight.current_pos_x][knight.current_pos_y].knight = None

        knight.move(direction)

        print('Moving knight', knight)
        print('Entity in position to move', self.board[knight.current_pos_x][knight.current_pos_y])

        current_entity_in_position_to = self.board[knight.current_pos_x][knight.current_pos_y]

        if len(current_entity_in_position_to.items) == 1 and knight.item is None:
            knight.item = current_entity_in_position_to.items[0]

            # Remove the item from the position where the item was retrieved.
            self.board[knight.current_pos_x][knight.current_pos_y].remove_item(knight.item)
        elif len(current_entity_in_position_to.items) > 1 and knight.item is None:
            best_items = {}

            for item in current_entity_in_position_to.items:
                item_score_mapping = {
                    'A': 4,
                    'M': 3,
                    'D': 2,
                    'H': 1
                }
                best_items[item_score_mapping[item.representation]] = item

            best_item_key = max(best_items.keys())
            best_item = best_items[best_item_key]

            knight.item = best_item

            # Set the position where the item came from to None
            self.board[knight.current_pos_x][knight.current_pos_y].remove_item(knight.item)

        # TODO: Knights that
        #  drown throw their item to the bank before sinking down to Davy Jones' Locker - the item is left on
        #  the last valid tile that the knight was on.

        if isinstance(current_entity_in_position_to.knight, Knight) \
                and current_entity_in_position_to.knight.status == KnightStatus.LIVE:
            win = knight.fight(current_entity_in_position_to.knight)

            losing_knight = self.board[knight.current_pos_x][knight.current_pos_y].knight if win else knight
            print('Attacker', knight)
            print('Defender', current_entity_in_position_to.knight)

            if losing_knight.item:
                self.board[knight.current_pos_x][knight.current_pos_y].items.append(losing_knight.item)

            losing_knight.status = KnightStatus.DEAD
            losing_knight.item = None
            self.knights[losing_knight.representation] = losing_knight

        self.board[knight.current_pos_x][knight.current_pos_y] = ArenaPosition(
            x=knight.current_pos_x, y=knight.current_pos_y, knight=knight
        )

        return knight

    def move(self, knight: str, direction: str):
        try:
            self._move_knight(self.knights[knight], direction)
        except KnightDrowned:
            pass

    def __str__(self):
        arena = ' _ _ _ _ _ _ _ _\n'

        for arena_position_row in self.board:
            for position in arena_position_row:
                if position.items:
                    representations = ''

                    for item in position.items:
                        representations += item.representation

                    arena += f'|{representations}'
                elif position.knight:
                    arena += f'|{position.knight.representation}'
                else:
                    arena += '|_'

            arena += '|\n'

        return arena
