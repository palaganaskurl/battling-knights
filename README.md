# battling-knights

## How To Run
Please use Python 3.7+

* Please make sure that moves.txt exists and it has valid content.
* Run `python game.py`
* `final_state.json` is generated after running the program.

## Structure
### Arena
* Contains the rendering of arena and manipulation of the states and entities inside the game.
### Directions
* Enum containing the different directions a knight can move.
### Game
* Contains the initialization of arena and the entities of the game.
* Contains the reading of `moves.txt` and exporting to `final_state.json`
### Item
* Contains class that defines the item properties.
### Knight
* Contains class that defines the knight properties.

## Issues
* Items are rendered left align because I'm having a hard time rendering multiple items center align in a grid cell.

## Contributions
1. Install dev dependencies from Pipfile.
2. Run pre-commit install
3. (Optional) Run pre-commit run --all-files upon pre-commit install

## Sample Run
![carbon](https://user-images.githubusercontent.com/18252435/179399876-83900bf0-7c49-4279-a668-a83bcb7c62f6.png)
