# Completed Features

### General features
All expected features have been implemented: simple game, multi player game, flask game. ALl of which the user can win by guessing ships and the AI (where applicable) can win. 

### Validation
Defensive programming and try except statements are implemented throughout the project.

### Additional Testing
I have written some tests which can be found in tests/test_by_me.py

### Logging
Logging is implemented throughout the project. See main.log for previous logs

### Optimal ship placement
I have added another algorithm to the place_battleships function which places the ships in the most optimal locations. As referenced here (Cite)[http://www.datagenetics.com/blog/december32011/] the most optimal placement puts ships adjacent to one another to confuse the user. This can be used in mp_game_engine.py by changing "custom" to "optimal" in the player board

### Hard mode
There is a constant in main.py named HARD_MODE. When true once the AI hits a shit it will hit the ship until sunk in consecutive turns. This is implemented in the enhanced_ai module.

# Battleships ReadMe

## Intro
This is the battleships course work for ECM1400. Battleships can be played via the command line or a web interface. An AI has been made to play against the player in multiplayer mode and online mode. In simple game mode you play against a pre generated board. 

## Prerequisites

Python packages required:
`blinker==1.7.0` <br>
`click==8.1.7`<br>
`Flask==3.0.0`<br>
`itsdangerous==2.1.2` <br>
`Jinja2==3.1.2`<br>
`MarkupSafe==2.1.3`<br>
`Werkzeug==3.0.1`<br>
`pytest==7.4.3`<br>
`pytest-cov==4.1.0`<br>
`pytest-dependency==0.5.1`<br>
`pytest-order==1.2.0`<br>

Can be seen in requirements.txt

battleships.txt should store the ships on each line:<br>
shipname:length

placement.json should store the ship placement on each line:<br>
shipname:[x_coord, y_coord, orientation] 

## Installation

`pip install -r requirements.txt` when in the root directory

OR

Indivually install each requirement
`pip install Flask`...

## Getting Started
1. Install all required packages

### Simple game mode
2. Run game_engine.py
3. Use CLI to answer promts and play the game
4. Game finishes once all ships are sunk

### Multi-player game mode
2. Alter battleships.txt and placement.json if required
    1. battleships.txt states what ships and their length can be used
    2. placement.json states where your ships will be placed on the board
        1. Placement as follows: shipname:[x_coord, y_coord, orientation]
3. Run mp_game_engine.py
4. Use CLI to answer promts and play the game
5. Game finishes once all ships are sunk

### GUI game mode
2. run main.py
3. Open a browser at 127.0.0.1:5000/placement
4. Use the browser to place your ships and continue
5. Use the grid to guess where the AI has placed their ships
6. Game finishes once all ships are sunk

For hard mode change the HARD_MODE constant to True.

## Testing
Tests can be seen in /tests. There are 4 testing files (`test_by_me.py`, `test_functionality.py`,` test_helper_functions.py` `test_students.py`) and 2 configuration files (`battleships.txt` and `placement.json`) followed by an `__init__.py`. Tests have been provided by academics for this project, other than tests in test_by_me.py. These have been written by me to test additional funcitonality. 

To run tests be in the root directory for the project in terminal and enter `pytest` in CLI

## Developer Documentation
Full documentation can be seen throughout the code base in comments and docstrings. There are docstrings for each function and module. 

For sphinx documentation open `docs/_build_html/index.html`<br>
*Note had issues generating the document so I moved things around in directories to get it to generate then it broke imports so I moved it all back later. Issue with the main module also*

To view logs open `main.log`. This stores any notable processes from the program.

#### Components.py
Key game functions used in each version of the game

#### game_engine.py
Single player game against the simple board placement. Can be run to play the simple version of the game

#### mp_game_engine.py
Multiplayer game against the AI. Your ships are placed using the placement.json and has additional functions to play against the AI

#### main.py
Development server to play against the AI. See intructions above. More function sot enable browser functionality.

#### enhanced_ai
Additional functionality to make the AI better - much much better!

## Details
Author: ********** <br>
License: MIT (License file)<br>
Course work for ECM1400, Due 15/12/23