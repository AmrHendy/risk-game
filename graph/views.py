from django.shortcuts import render
from riskGame.classes.parser.parser import Parser
from riskGame.classes.agent.human import Human
import json


# Create your views here.
def index(request):
    #this is the shape of the request add your logic here based on that.
    dict = request.POST.dict()
    if 'json' in dict:
        data = dict['json']
        type = dict['type']
        dic = json.loads(data)
        if type == "state":
            # dic from frontend for the initial state
            parser = Parser()
            parser.parse_json_to_state(dic)
            initial_state = parser.get_initial_state()
            agents = []
            agents.append(parser.get_agent(1))
            agents.append(parser.get_agent(2))
            prev_state = None
            current_state = initial_state
        elif type == "turn":
            if current_state.get_winner() is None:
                player_turn = current_state.get_player_turn_number()
                if isinstance(agents[player_turn], type(Human)):
                    # get dic from front end for the move
                    move, errors = parser.parse_json_to_move(current_state, dic)
                    if move:
                        prev_state = current_state
                        current_state = agents[player_turn].play(current_state, move)
                    dic = parser.parse_state_to_json(current_state, errors)
                else:
                    # get request to represent get the next turn state
                    prev_state = current_state
                    current_state = agents[player_turn].play(current_state)
                    dic = parser.parse_state_to_json(current_state, [])
                return render(dic, 'index.html')
                # send dic to front end
            else:
                response = {"status":"winner", "winner": "Player " + str(current_state.get_winner().get_name() + 1)}
                return render(response, 'index.html')

        #TODO:: check this. (not good solution.)
        return render(response, 'index.html')
    return render(request, 'index.html')
