'''Test functions written by Adam'''
import mp_game_engine as mp
import game_engine as ge
import components as co

def test_generate_attack_within_board():
    '''
    Test if generate_attack returns a tuple with contents within size of the board
    '''
    # Size of the board
    size = 10
    # Call the function
    generated_attack = mp.generate_attack(size)
    # Check coordinates are within the board size
    assert generated_attack[0] < size
    assert generated_attack[1] < size

def test_cli_coords_return_type(monkeypatch):
    '''
    Tests if the cli_coordinates_input returned tuple is of integers
    '''
    # Forces input CLI to 0 
    monkeypatch.setattr('builtins.input', lambda _: 0)

    # Call function
    returned_coords = ge.cli_coordinates_input()
    # Ensure integers are returned
    assert isinstance(returned_coords[0],int)
    assert isinstance(returned_coords[1],int)

def test_cli_coords_incorrect_input(monkeypatch):
    '''
    Tests if the cli_coordinates_input returns an empty tuple on incorrect inputs
    '''
    # Forces input CLI to a string
    monkeypatch.setattr('builtins.input', lambda _: "String!!!")
    # Call function
    returned_coords = ge.cli_coordinates_input()
    # Ensure integers are returned
    assert returned_coords == tuple

    # Forces input CLI to a an empty string
    monkeypatch.setattr('builtins.input', lambda _: "")
    # Call function
    returned_coords = ge.cli_coordinates_input()
    # Ensure integers are returned
    assert returned_coords == tuple

def test_initalise_board():
    '''Testing edge cases and intended function of initalize board'''
    # Testing indended funciton of the board
    size = 10
    assert len(co.initialise_board(size)) == size
    # Testing negative board sizes fail 
