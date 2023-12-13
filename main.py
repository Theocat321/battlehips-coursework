'''Module runs a development server to play against the AI

Start by running this file, navigate to 127.0.0.1:5000 in a browser
Place your ships
Guess where the AI has placed their ships
'''
import json
import logging
from flask import Flask, request, render_template,jsonify
from components import create_battleships, initialise_board, place_battleships
from mp_game_engine import generate_attack
from enhanced_ai import generate_attack_improved
import game_engine as ge

app = Flask(__name__)

# Logging config
logging.basicConfig(filename='main.log', encoding='utf-8', level=logging.DEBUG)

players = {}
ai_attacks = [] # list of ai attacks
user_attacks = [] # list of player attacks
ai_ships = create_battleships()
user_ships = create_battleships()
ai_attack_stack = [] # this is only used when using harder AI
HARD_MODE = True

@app.route('/',methods=['GET'])
def root():
    '''
    Root url
    This given data by /placement url and returns the 
    template of the front end with the player board on.
    '''
    return render_template('main.html',player_board=players['user']['board'])

@app.route('/placement', methods=['GET', 'POST'])
def placement_interface():
    '''
    This url takes GET and POST requests.
    POST:
        recives data from browser and places the ships placed onto the board, then confirms this
    GET:   
        Renders template for placing ships with the ships from battleships.txt and the board size
    '''
    ships = create_battleships()
    if request.method == 'POST':
        data = request.get_json() # {'name':[x,y,direction] , ...}
        with open('placement.json','w',encoding='UTF-8') as f:
            json.dump(data,f)
        # Setting up the dictionaries
        user_board = place_battleships(initialise_board(),ships=ships,algorithm="custom")
        ai_board = place_battleships(initialise_board(),ships=ships,algorithm="random")
        ai_dict = {'board':ai_board}
        user_dict = {'board':user_board}
        players['ai'] = ai_dict
        players['user'] = user_dict
        logging.debug("User board recieved")
        return jsonify({'message': 'Received'}), 200
    elif request.method == "GET":
        return render_template('placement.html',board_size = len(initialise_board()), ships = ships)

@app.route("/attack",methods=['GET'])
def attack():
    '''
    Accepts GET requests

    x and y coorinates should be passed in the request.
    These coordinates are used to process an attack on the AI board

    AI attack is generated and used against the player. 

    Checks are completed to see if the game is finished

    Returns json response to the front end
    '''
    global ai_ships, user_ships, ai_attack,players, user_attacks, ai_attack_stack
    x = int(request.args.get('x'))
    y = int(request.args.get('y'))

    coordinates = (x,y)
    ## Check if user has already attacked this spot
    if coordinates in user_attacks:
        logging.warning("User cannot select same square more tha once")
        return
    user_attack = ge.attack(coordinates,players['ai']['board'],ai_ships)
    user_attacks.append(coordinates)

    ## Generate AI attack back at the user
    if not HARD_MODE:
        ai_coords = generate_attack(len(players['user']['board']))
    else:
        ## HARDER ATTACK VERSION - uncomment above for normal and comment below
        ai_coords, ai_attack_stack = generate_attack_improved(players['user']['board'],ai_attack_stack)
    # Ensure square not hit before
    while ai_coords in ai_attacks:
        if not HARD_MODE:
            ai_coords = generate_attack(len(players['user']['board']))
        else:
            # HARDER ATTACK VERSION
            ai_coords, ai_attack_stack = generate_attack_improved(players['user']['board'],ai_attack_stack)
    # Add hit to list
    ai_attacks.append(ai_coords)
    ai_attack = ge.attack(ai_coords,players['user']['board'],user_ships)

    # Check if anyone wins
    has_user_won = all(value == 0 for value in ai_ships.values())
    has_ai_won = all(value == 0 for value in user_ships.values())

    ## Finishing the game
    # If someone has won reset the ships
    if has_user_won:
        reset_globals()
        logging.debug("User has won the game")
        return jsonify({
            'hit': user_attack,
            'AI_Turn': ai_coords,
            'finished':'Game Over Player wins'
            })
    elif has_ai_won:
        reset_globals()
        logging.debug("AI has won the game")
        return jsonify({
            'hit': user_attack,
            'AI_Turn': ai_coords,
            'finished':'Game Over, AI wins'
            })
    else:
        return jsonify({'hit': user_attack,
                'AI_Turn': ai_coords
                })
    
def reset_globals() -> None:
    '''Utility procedure for reseting the global variables'''
    global players, ai_attacks, user_attacks, ai_ships, user_ships, ai_attack_stack
    players = {}
    ai_ships = create_battleships()
    user_ships = create_battleships()
    ai_attack_stack = []
    ai_attacks = []
    user_attacks = []

if __name__ == '__main__':
    app.run(debug=True)
