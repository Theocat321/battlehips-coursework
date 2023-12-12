'''Run this file when playing against the AI in the CLI'''
import logging
import random
import game_engine as ge
import components as cp

logging.basicConfig(filename='main.log', encoding='utf-8', level=logging.DEBUG)

players = {} # key = name, value = [board, battleships dict]

def generate_attack(board_size:int=10) -> tuple:
    '''
    Generates a tuple with coordinates within the board
    '''
    x = random.randint(0,board_size-1)
    y = random.randint(0,board_size-1)
    return (x,y)

def ai_opponent_game_loop() ->  None:
    '''
    Starts the game via the CLI against AI
    '''
    print("Welcome to battleships")
    logging.debug("Multiplayer game started")
    battleships = cp.create_battleships()
    # Init user
    user_board = cp.place_battleships(cp.initialise_board(),battleships,"custom")
    user_dict = {'board':user_board,'battleships':battleships}
    players['user'] = user_dict

    # Init AI
    ai_board = cp.place_battleships(cp.initialise_board(),battleships,"random")
    ai_dict = {'board':ai_board,'battleships':battleships}
    players['ai'] = ai_dict

    # Playing the game
    game_over = False
    player_ships_hit = 0
    ai_ships_hit = 0
    total_hits_required = 0
    # Calculating hits required to end the game
    for value in battleships.values():
        total_hits_required += value
    while not game_over:
        player_invalid_attack = True
        while player_invalid_attack:
            user_coords = ge.cli_coordinates_input()
            if user_coords == tuple:
                logging.warning("Bad user input from CLI")
                continue
            elif (user_coords[0] < len(user_board) and user_coords[0] > -1 and
                    user_coords[1] > -1 and user_coords[1] < len(user_board)):
                player_invalid_attack = False
            else:
                warning_str = ("Invalid integer input: Must be between 0 and %s"
                                + str(len(user_board)))
                logging.warning(warning_str)
        user_attack = ge.attack(user_coords,players["ai"]['board'],players["ai"]['battleships'])
        if user_attack:
            print("You have hit!")
            player_ships_hit += 1
        else:
            print("You have missed")
        ai_coords = generate_attack(len(user_board))
        ai_attack = ge.attack(ai_coords,players["user"]['board'],players["user"]['battleships'])
        if ai_attack:
            print("AI hit you")
            ai_ships_hit += 1
        else:
            print("AI has missed")

        # Prints the players board in Ascii
        pretty_print_board(players["user"]['board'])

        # Check if game is over
        if player_ships_hit == total_hits_required:
            game_over = True
        elif ai_ships_hit == total_hits_required:
            game_over = True
    logging.debug("Game over")
    if player_ships_hit == 17:
        logging.debug("Player has won")
    else:
        logging.debug("AI has won")

def pretty_print_board(board:list[list]) -> None:
    '''
    Prints 2D array (board) like a table into terminal
    For pretty output ensure terminal window is large
    '''
    print("    0 1 2 3 4 5 6 7 8 9")
    for i, row in enumerate(board):
        line = str(i) + "  "
        for j, cell in enumerate(board):
            if board[i][j] is None:
                line += " ~"
            else:
                line += " x"
        print(line)

if __name__ == "__main__":
    ai_opponent_game_loop()
