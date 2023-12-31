'''Run this file when playing the simple battleships in CLI'''
import logging
import components

def attack(coordinates:tuple, board:list[list], battleships:dict) -> bool:
    '''
    Checks if battle ship at coordinate provided
    If there is:
        Decrements the battleship
        Changes board at coordinates to none
        Checks if sunk
        Returns true
    if not:
        Returns false
    '''
    # get value in coordianate
    y = coordinates[0]
    x = coordinates[1]
    current_value = board[x][y]

    # check if ship hit on board
    if current_value is not None:
        # Change board to None in location
        board[x][y] = None
        # decrement dict
        battleships[current_value] -= 1
        # check if game over
        if battleships[current_value] == 0:
            logging.debug("sunk ship!")
            print("sunk!")
        return True
    # if not hit
    return False

def  cli_coordinates_input()->tuple[int,int]:
    '''
    Prompts user to input x and y coordinates to attack with via CLI
    '''
    try:
        user_x = int(input("Input the x coordinate: "))
        user_y = int(input("Input the y coordinate: "))
    except ValueError:
        logging.warning("Cannot input string coordinates: returning empty tuple")
        return tuple
    except Exception:
        logging.warning("Unknown exception in cli input: returning empty tuple")
        return tuple
    return (user_x,user_y)

def simple_game_loop()-> None:
    '''
    Starts the game via the CLI with simple placement of ships
    '''
    print("Welcome to Battleships!")
    logging.debug("Game started")
    empty_board = components.initialise_board()
    battleships = components.create_battleships()
    board = components.place_battleships(board=empty_board,ships=battleships)
    ships_hit = 0
    total_hits_required = 0
    # Calculating hits required to end the game
    for value in battleships.values():
        total_hits_required += value
    while ships_hit < total_hits_required:
        player_invalid_attack = True
        while player_invalid_attack:
            current_coordinates = cli_coordinates_input()
            if current_coordinates == tuple:
                logging.warning("Bad input to CLI")
                continue
            elif (current_coordinates[0] < len(board) and current_coordinates[0] > -1 and
                    current_coordinates[1] > -1 and current_coordinates[1] < len(board)):
                player_invalid_attack = False
            else:
                warning_str = "Invalid integer input: Must be between 0 and %s" + str(len(board))
                logging.warning(warning_str)
        current_move = attack(current_coordinates,board,battleships)
        if current_move:
            print("HIT!!")
            ships_hit += 1
        else:
            print("Miss :(")
    logging.debug("Game Over!")
    print("Game Over!")

if __name__ == "__main__":
    simple_game_loop()
