import json
from flask import Flask, request, render_template,jsonify
from components import create_battleships, initialise_board, place_battleships
from mp_game_engine import generate_attack
import game_engine as ge

app = Flask(__name__)

players = {}
ai_attacks = [] # list of ai attacks
user_attacks = [] # list of player attacks
ai_ships = create_battleships()
user_ships = create_battleships()

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
        return jsonify({'message': 'Received'}), 200
    elif request.method == "GET":
        return render_template('placement.html',board_size = len(initialise_board()), ships = ships)

@app.route("/attack",methods=['GET'])
def attack():
    global ai_ships, user_ships, ai_attack,players, user_attacks
    x = int(request.args.get('x'))
    y = int(request.args.get('y'))

    coordinates = (x,y)
    ## Check if user has already attacked this spot
    if coordinates in user_attacks:
        return
    user_attack = ge.attack(coordinates,players['ai']['board'],ai_ships)
    user_attacks.append(coordinates)

    ## Generate AI attack back at the user
    ai_coords = generate_attack(len(players['user']['board']))
    # Ensure square not hit before
    while ai_coords in ai_attacks:
        ai_coords = generate_attack(len(players['user']['board']))
    # Add hit to list
    ai_attacks.append(ai_coords)
    ai_attack = ge.attack(ai_coords,players['user']['board'],user_ships)

    # Check if anyone wins
    has_user_won = all(value == 0 for value in ai_ships.values())
    has_ai_won = all(value == 0 for value in user_ships.values())

    # Setting global ships for each to the changed values
    print("AI has hit: "+str(ai_attack))
    print("AO battle ships: "+str(ai_ships))
    print("user ships: "+str(user_ships))

    ## Finishing the game

    # If someone has won reset the ships
    if has_user_won:
        ai_ships = create_battleships()
        user_ships = create_battleships()
        players = {}
        ai_attack = []
        return jsonify({
            'hit': user_attack,
            'AI_Turn': ai_coords,
            'finished':'Game Over Player wins'
            })
    elif has_ai_won:
        ai_ships = create_battleships()
        user_ships = create_battleships()
        players = {}
        ai_attack = []
        return jsonify({
            'hit': user_attack,
            'AI_Turn': ai_coords,
            'finished':'Game Over, AI wins'
            })
    else:
        return jsonify({'hit': user_attack,
                'AI_Turn': ai_coords
                })

if __name__ == '__main__':
    app.run(debug=True)
