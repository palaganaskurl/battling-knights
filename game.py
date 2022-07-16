import json

from arena import Arena
from item import Item
from knight import Knight


class Game:
    def __init__(self):
        initial_knights = [
            Knight(color='Red', current_pos_x=0, current_pos_y=0),
            Knight(color='Blue', current_pos_x=7, current_pos_y=0),
            Knight(color='Green', current_pos_x=7, current_pos_y=7),
            Knight(color='Yellow', current_pos_x=0, current_pos_y=7)
        ]
        initial_items = [
            Item(name='Axe', attack=2, defense=0, current_pos_x=2, current_pos_y=2),
            Item(name='Dagger', attack=1, defense=0, current_pos_x=2, current_pos_y=5),
            Item(name='Helmet', attack=0, defense=1, current_pos_x=5, current_pos_y=2),
            Item(name='MagicStaff', attack=1, defense=1, current_pos_x=5, current_pos_y=5),
        ]
        self.arena = Arena(initial_knights, initial_items)

        print(self.arena)

    def run(self):
        with open('moves2.txt', 'r') as f:
            moves = f.read().splitlines()
            moves = moves[1:-1]

            print(moves)

            for move in moves:
                parsed_move = move.split(':')
                knight = parsed_move[0]
                direction = parsed_move[1]

                self.arena.move(knight, direction)

    def export(self):
        json_data = {}

        for knight in self.arena.knights.values():
            print('knight', knight)

            json_data[knight.color] = [
                [knight.current_pos_x, knight.current_pos_y],
                knight.status,
                knight.item.name if knight.item else None,
                knight.total_attack,
                knight.total_defense
            ]

        with open('final_state.json', 'w') as f:
            json.dump(json_data, f, indent=4)


if __name__ == '__main__':
    game = Game()
    game.run()
    print(game.arena)

    from pprint import pprint
    pprint(game.arena.knights)

    game.export()
