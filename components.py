'''Contains functions for core game functionality'''
import json
import sys
import random

def initialise_board(size:int = 10) -> list[list]:
    '''Returns an empty grid of dimensions size'''
    #todo: exepction handling
    #todo: testing for these errors
    try:
        board = []
        for x in range(0,size):
            current_line = []
            for y in range(0,size):
                current_line.append(None)
            board.append(current_line)   
        return board
    except TypeError:
        raise TypeError("Initalise_board expects integer type")
    except ValueError:
        raise ValueError("Size of board cannot be negative")

    

def create_battleships(filename:str = "battleships.txt") -> dict:
    '''Reads in the battle ships from the filename passed'''
    #todo: exception handling
    #todo: testing these errors
    battleships={}
    f = open(filename,"r")
    for line in f:
        elements = line.split(":")
        battleships[elements[0]] = int(elements[1].strip())
    return battleships

def place_battleships(board:list[list] , ships: dict, algorithm:str = "simple") -> list[list]:
    '''Places the battle ships onto the board and returns this
    FINISH THIS DOCTSTRING!'''
    ##todo: error handling & tests
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
                print("Ship too long for board or too many ships for the simple algorithm")
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
                else:
                    # Check if all positions requred are empty
                    # if so change them
                    is_obstructed = False
                    for x in range(0,ship_length):
                        if direction == 0:
                            current_column = inital_column + x
                            # If a ship occupies the location break    
                            if(board[inital_row][current_column] is not None):
                                is_obstructed = True
                                break
                        else:
                            current_row = inital_row + x
                            if(board[current_row][inital_column] is not None):
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
    elif (algorithm.lower() == "custom"):
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
                # Check orientation of the ship
                if direction == 'h':
                    current_column = inital_column + x
                    board[inital_row][current_column] = current_ship_name
                else:
                    current_row = inital_row + x
                    board[current_row][inital_column] = current_ship_name

        ##TODO: ENSURE ALL SHIPS FIT ON THE GRID
    else:
        raise ValueError("Algorithm argument invald") # if parameter for algorithm is invalid, exception
    return board

if __name__ == "__main__":
    # ships_dict = create_battleships()
    # new_board = place_battleships(initialise_board(),ships_dict,algorithm="custom")
    print(initialise_board(-1))