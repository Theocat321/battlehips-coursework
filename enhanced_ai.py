'''
Enhanced AI for playing against the player. Warning much harder to beat!
'''
import mp_game_engine as mp

def check_attack(coordinates:tuple, board:list[list]) -> bool:
    '''
    Checks if battle ship at coordinate provided
    '''
    # get value in coordianate
    x = coordinates[1]
    y = coordinates[0]
    current_value = board[x][y]
    # check if ship hit on board
    if current_value is not None:
        return True
    # if not hit
    return False

def generate_attack_improved(board:list[list], attack_stack:list[tuple]) -> tuple[tuple,list[tuple]] :
    '''
    Generates an attack. If the previous attack has hit a ship, it will
    continue to hit this ship until it has sunk
    '''
    if attack_stack != []:
        # harder attack
        attack_coords = attack_stack.pop()
        return attack_coords, attack_stack
    # If no attack stack
    # Generate coords
    attack_coords = mp.generate_attack(len(board))
    # Check if ship will hit
    has_hit = check_attack(attack_coords,board)
    if has_hit:
        ## Create the new attack stack
        attack_stack = []
        # iterate through the board locating ships
        x = attack_coords[1]
        y = attack_coords[0]
        ship_name = board[x][y]
        for y,row in enumerate(board):
            for x,cell in enumerate(row):
                if cell == ship_name:
                    attack_stack.append((x,y))
        # attack_stack.remove(attack_coords)
        return attack_coords, attack_stack
    # else return coords
    return attack_coords, attack_stack
