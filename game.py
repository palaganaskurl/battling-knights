import json

from arena import Arena
from item import Item
from knight import Knight
from knight import KnightStatus


class Game:
    def __init__(self):
        initial_knights = [
            Knight(color='Red', current_pos_x=0, current_pos_y=0),
            Knight(color='Blue', current_pos_x=7, current_pos_y=0),
            Knight(color='Green', current_pos_x=7, current_pos_y=7),
            Knight(color='Yellow', current_pos_x=0, current_pos_y=7),
        ]
        initial_items = [
            Item(
                name='Axe',
                attack=2,
                defense=0,
                current_pos_x=2,
                current_pos_y=2,
            ),
            Item(
                name='Dagger',
                attack=1,
                defense=0,
                current_pos_x=2,
                current_pos_y=5,
            ),
            Item(
                name='Helmet',
                attack=0,
                defense=1,
                current_pos_x=5,
                current_pos_y=5,
            ),
            Item(
                name='MagicStaff',
                attack=1,
                defense=1,
                current_pos_x=5,
                current_pos_y=2,
            ),
        ]
        # # Tester for multiple initial items on same x and y coordinates.
        # initial_items = [
        #     Item(
        #         name='Axe',
        #         attack=2,
        #         defense=0,
        #         current_pos_x=5,
        #         current_pos_y=5,
        #     ),
        #     Item(
        #         name='Dagger',
        #         attack=1,
        #         defense=0,
        #         current_pos_x=5,
        #         current_pos_y=5,
        #     ),
        #     Item(
        #         name='Helmet',
        #         attack=0,
        #         defense=1,
        #         current_pos_x=5,
        #         current_pos_y=5,
        #     ),
        #     Item(
        #         name='MagicStaff',
        #         attack=1,
        #         defense=1,
        #         current_pos_x=5,
        #         current_pos_y=5,
        #     ),
        # ]
        self.arena = Arena(initial_knights, initial_items)

    def run(self):
        with open('moves.txt', 'r') as f:
            moves = f.read().splitlines()
            moves = moves[1:-1]

            for move in moves:
                parsed_move = move.split(':')
                knight = parsed_move[0]
                direction = parsed_move[1]

                self.arena.move(knight, direction)

    def export(self):
        json_data = {}

        for knight in self.arena.knights.values():
            if knight.status == KnightStatus.DROWNED:
                position = None
            else:
                position = [knight.current_pos_x, knight.current_pos_y]

            json_data[knight.color] = [
                position,
                knight.status,
                knight.item.name if knight.item else None,
                knight.total_attack,
                knight.total_defense,
            ]

        for item in self.arena.items.values():
            json_data[item.name] = [
                [item.current_pos_x, item.current_pos_y],
                item.equipped,
            ]

        with open('final_state.json', 'w') as f:
            json.dump(json_data, f, indent=4)


if __name__ == '__main__':
    game = Game()

    print('Initial Arena')
    print(game.arena)

    game.run()

    print('Arena After Running Game')
    print(game.arena)

    game.export()
