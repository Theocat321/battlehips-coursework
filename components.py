'''Contains functions for core game functionality'''
import json
import sys
import random
import logging

logging.basicConfig(filename='main.log', encoding='utf-8', level=logging.DEBUG)

def initialise_board(size:int = 10) -> list[list]:
    '''Returns an empty grid of dimensions size'''
    try:
        if size < 1:
            # Raise value error and later raises general exception
            raise ValueError
        board = []
        for x in range(0,size):
            current_line = []
            for y in range(0,size):
                current_line.append(None)
            board.append(current_line)
        return board
    except TypeError as e:
        logging.error("Initalise board requires integer")
        raise TypeError("Initalise_board expects integer type") from e
    except ValueError as e:
        logging.error("Board size must be greater than 0")
        raise ValueError("Size of board cannot be 0 or negative") from e
    except Exception as e:
        logging.error("Unknown error when initalising board")
        raise Exception("Unknown exception has occured") from e

def create_battleships(filename:str = "battleships.txt") -> dict:
    '''Reads in the battle ships from the filename passed'''
    try:
        battleships={}
        f = open(filename,"r", encoding='utf-8')
        for line in f:
            elements = line.split(":")
            battleships[elements[0]] = int(elements[1].strip())
        return battleships
    except TypeError as e:
        logging.error("Filename in create battlehships requires string as parameter")
        raise TypeError("File name should be a string") from e
    except Exception as e:
        logging.error("Unknown error when creating battleships")
        raise Exception("Unknown exception has occured") from e

def place_battleships(board:list[list] , ships: dict, algorithm:str = "simple") -> list[list]:
    '''Places the battle ships onto the board and returns the outcome

    ---Parameters---
    board: List[List]
    ships: dictionary
    algorithm: string
    ---Return---
    List[list]
    '''
    def check_ship_fits(inital_row:int, inital_column:int,direction:int,ship_length:int) -> bool:
        # 0: hoz, 1:vert
        if (direction == 0):
            if ((inital_column + ship_length) > board_size-1):
                return False
            else:
                return True
        else:
            if((inital_row + ship_length) > board_size-1):
                return False
            else:
                return True
    if (algorithm.lower() == "simple"):
        row = 0
        for key,value in ships.items():
            try:
                for x in range(value):
                    board[row][x] = key
                row+=1 
            except IndexError: # catching if there is too many ships for the board or if ship to long
                logging.error("Ship too long for board or too many ships for the simple algorithm")
                sys.exit(1)
    elif (algorithm.lower() == "random"):     
        board_size = len(board) # square board
        # brute force method
        for ship_name, ship_length in ships.items():
            ship_placed = False
            while not ship_placed:
                inital_row = random.randint(0,board_size-1)
                inital_column = random.randint(0,board_size-1)
                direction = random.randint(0,1) # 0: hoz, 1:vert
                # Check ship fits
                ship_fits = check_ship_fits(inital_row,inital_column,direction,ship_length)
                if not ship_fits:
                    continue # next iteration and try again
                # Check if all positions requred are empty
                # if so change them
                is_obstructed = False
                for x in range(0,ship_length):
                    if direction == 0:
                        current_column = inital_column + x
                        # If a ship occupies the location break    
                        if board[inital_row][current_column] is not None:
                            is_obstructed = True
                            break
                    else:
                        current_row = inital_row + x
                        if board[current_row][inital_column] is not None:
                            is_obstructed = True
                            break
                # place the ship if not obstructed
                if not is_obstructed:
                    for x in range(0,ship_length):
                        if direction == 0:
                            current_column = inital_column + x
                            board[inital_row][current_column] = ship_name
                        else:
                            current_row = inital_row + x
                            board[current_row][inital_column] = ship_name
                    ship_placed = True
        return board
    elif algorithm.lower() == "custom":
        # open json
        with open("placement.json","r",encoding="UTF-8") as f:
            placement_lines = f.readline()
        place_ships = json.loads(placement_lines) # shipname:[x_coord, y_coord, orientation]
        # then put the ship on the board
        for current_ship_name,info_arr in place_ships.items():
            # get length of current ship
            current_ship_length = ships[current_ship_name]
            inital_column = int(info_arr[0])
            inital_row = int(info_arr[1])
            direction = info_arr[2]
            # Iterate through the length of current ship
            for x in range(current_ship_length):
                try:
                    # Check orientation of the ship
                    if direction == 'h':
                        current_column = inital_column + x
                        board[inital_row][current_column] = current_ship_name
                    else:
                        current_row = inital_row + x
                        board[current_row][inital_column] = current_ship_name
                except IndexError as e:
                    # Not using f string as errors arrised in logging and raising error
                    error_str = "Placement json error: %s doesn't fit" %current_ship_name 
                    logging.error(error_str)
                    raise IndexError(error_str) from e
                except Exception as e:
                    logging.error("Unknown exception occured")
                    raise Exception("Unknown exception occured") from e
    else:
        raise ValueError("Algorithm argument invald") # if parameter for algorithm is invalid
    return board

# if __name__ == "__main__":
#     ships_dict = create_battleships()
#     new_board = place_battleships(initialise_board(),ships_dict,algorithm="custom")
