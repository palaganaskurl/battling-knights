from copy import deepcopy
from dataclasses import dataclass
from dataclasses import field
from typing import List
from typing import Optional

from item import Item
from knight import Knight
from knight import KnightDrowned
from knight import KnightStatus


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
        self.knights = {knight.representation: knight for knight in knights}
        self.items = {item.representation: item for item in items}
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
            self.board[knight.current_pos_x][
                knight.current_pos_y
            ] = ArenaPosition(
                x=knight.current_pos_x, y=knight.current_pos_y, knight=knight
            )

    def _set_items_initial_state(self):
        for item in self.items.values():
            current_arena_position = self.board[item.current_pos_x][
                item.current_pos_y
            ]

            if isinstance(current_arena_position, ArenaPosition):
                self.board[item.current_pos_x][
                    item.current_pos_y
                ].items.append(item)
            else:
                self.board[item.current_pos_x][
                    item.current_pos_y
                ] = ArenaPosition(
                    x=item.current_pos_x, y=item.current_pos_y, items=[item]
                )

    def _move_knight(self, knight: Knight, direction: str):
        # Set the position where the knight came from to None
        self.board[knight.current_pos_x][knight.current_pos_y].knight = None
        last_pos_x = knight.current_pos_x
        last_pos_y = knight.current_pos_y

        try:
            knight.move(direction)
        except KnightDrowned:
            if knight.item:
                self.board[last_pos_x][last_pos_y].items.append(knight.item)

            self.knights[knight.representation].item = None

            return

        try:
            current_entity_in_position_to = self.board[knight.current_pos_x][
                knight.current_pos_y
            ]
        except IndexError:
            return

        if (
            len(current_entity_in_position_to.items) == 1
            and knight.item is None
        ):
            knight.item = current_entity_in_position_to.items[0]

            # Remove the item from the position where the item was retrieved.
            self.board[knight.current_pos_x][knight.current_pos_y].remove_item(
                knight.item
            )
            self.items[knight.item.representation].equipped = True
        elif (
            len(current_entity_in_position_to.items) > 1
            and knight.item is None
        ):
            best_items = {}

            for item in current_entity_in_position_to.items:
                item_score_mapping = {'A': 4, 'M': 3, 'D': 2, 'H': 1}
                best_items[item_score_mapping[item.representation]] = item

            best_item_key = max(best_items.keys())
            best_item = best_items[best_item_key]

            knight.item = best_item

            # Set the position where the item came from to None
            self.board[knight.current_pos_x][knight.current_pos_y].remove_item(
                knight.item
            )
            self.items[knight.item.representation].equipped = True

        if (
            isinstance(current_entity_in_position_to.knight, Knight)
            and current_entity_in_position_to.knight.status
            == KnightStatus.LIVE
        ):
            win = knight.fight(current_entity_in_position_to.knight)

            losing_knight = (
                self.board[knight.current_pos_x][knight.current_pos_y].knight
                if win
                else knight
            )

            if losing_knight.item:
                self.board[knight.current_pos_x][
                    knight.current_pos_y
                ].items.append(losing_knight.item)

            losing_knight.status = KnightStatus.DEAD
            losing_knight.item = None
            self.knights[losing_knight.representation] = losing_knight

        self.board[knight.current_pos_x][knight.current_pos_y].knight = knight

    def move(self, knight: str, direction: str):
        self._move_knight(self.knights[knight], direction)

    def __str__(self):
        arena = '      '
        rendered_knights = {}
        knights_copy = deepcopy(self.knights)

        for i, arena_position_row in enumerate(self.board):
            if i == 0:
                for col in range(self.col):
                    has_drown = False

                    for knight in list(knights_copy.values()):
                        if (
                            knight.current_pos_y == col
                            and knight.current_pos_x == -1
                            and knight.status == KnightStatus.DROWNED
                            and not rendered_knights.get(knight.representation)
                        ):
                            arena += f'  ({knight.representation.lower()}) '
                            has_drown = True
                            rendered_knights[knight.representation] = True
                            del knights_copy[knight.representation]

                    if not has_drown:
                        arena += '      '

                arena += (
                    '\n      --------------------------'
                    '-----------------------\n'
                )

            for j, position in enumerate(arena_position_row):
                has_drown = False

                for knight in list(knights_copy.values()):
                    if (
                        knight.current_pos_x == i
                        and knight.current_pos_y == -1
                        and knight.status == KnightStatus.DROWNED
                        and not rendered_knights.get(knight.representation)
                    ):
                        arena += f'  ({knight.representation.lower()}) '
                        has_drown = True
                        rendered_knights[knight.representation] = True
                        del knights_copy[knight.representation]

                if not has_drown and j == 0:
                    arena += '      '

                if position.items:
                    representations = ''

                    for item in position.items:
                        representations += f'{item.representation}'

                    space_mapping = {4: 1, 3: 2, 2: 3, 1: 4}
                    spaces = ''.join(
                        [' '] * space_mapping[len(position.items)]
                    )
                    arena += f'|{representations}{spaces}'
                elif position.knight:
                    arena += f'|  {position.knight.representation}  '
                else:
                    arena += '|     '

            arena += '|'

            for knight in list(knights_copy.values()):
                if (
                    knight.current_pos_x == i
                    and knight.current_pos_y == 8
                    and knight.status == KnightStatus.DROWNED
                    and not rendered_knights.get(knight.representation)
                ):
                    arena += f'  ({knight.representation.lower()}) '
                    rendered_knights[knight.representation] = True
                    del knights_copy[knight.representation]

            arena += (
                '\n      -------------------------------------------------\n'
            )

            if i == self.col - 1:
                arena += '      '

                for col in range(self.col):
                    has_dead = False

                    for knight in list(knights_copy.values()):
                        if (
                            knight.current_pos_y == col
                            and knight.current_pos_x == 8
                            and knight.status == KnightStatus.DROWNED
                            and not rendered_knights.get(knight.representation)
                        ):
                            arena += f'  ({knight.representation.lower()}) '
                            has_dead = True

                    if not has_dead:
                        arena += '      '

        return arena
