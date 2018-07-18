#import statements
from play_by_play_reader import PlayByPlayReader
from game_lineup_reader import LineupReader
from csv_writer import CSVWriter
from settings import num_of_games

def get_team_for(on_court, player_id):
    '''
    Retrives the team of a given player
    who performed an action
    '''
    for team in on_court:
        if player_id in on_court[team]:
            return team
    raise Exception("Player {} not found on team".format(player_id))

def swap_players_in(on_court, players_subbing_in, players_subbing_out):
    '''
    Takes the dictionary on_court and swaps
    all players_subbing_out for players_subbing_in
    '''
    for i in range(len(players_subbing_in)):
        team = get_team_for(on_court, players_subbing_out[i])
        on_court[team].remove(players_subbing_out[i])
        on_court[team].append(players_subbing_in[i])
    return on_court

def update_plus_minus(plus_minus, team_for, on_court, points):
    '''
    Updates all players in on_court
    player entries in the plus minus dictionary
    using points and team_for
    '''
    for team in on_court.keys():
                    #updating plus minus for players on team that scored
                    if team == team_for:
                        players_on_court = on_court[team]
                        for player in players_on_court:
                            if player in plus_minus.keys():
                                plus_minus[player] += points
                            else:
                                plus_minus[player] = points
                    else:
                        #updating plus minus for players on team that got scored on
                        players_on_court = on_court[team]
                        for player in players_on_court:
                            if player in plus_minus.keys():
                                plus_minus[player] -= points
                            else:
                                plus_minus[player] = points * -1
    return plus_minus

def create_plus_minus_dict():
    '''
    The main method responsible for the major
    logic of the program
    '''
    play_by_play_reader = PlayByPlayReader()
    game_lineup_reader = LineupReader()
    csv_writer = CSVWriter()

    for game in range(num_of_games):
        plus_minus = {}
        game_events = play_by_play_reader.get_next_game()
        game_id = game_events[0]["Game_id"]
        counter = 0
        while(counter < len(game_events)):
            event = game_events[counter]
            #handle each event type
            #made shot
            if event["Event_Msg_Type"] == "1":
                points = int(event["Option1"])
                team_for = get_team_for(on_court, event["Person1"])

                plus_minus = update_plus_minus(plus_minus, team_for, on_court, points)

            #substitution
            elif event["Event_Msg_Type"] == "8":
                '''
                when the substitution happens before a free throw,
                update the plus/minus of players on the court when
                the foul occurred for the free throw event before
                updating the players on the court
                '''
                players_subbing_out = []
                players_subbing_in = []
                time_of_sub = event["PC_Time"]
                while(event["PC_Time"] == time_of_sub):
                    if event["Event_Msg_Type"] == "8":
                        players_subbing_out.append(event["Person1"])
                        players_subbing_in.append(event["Person2"])
                    elif event["Event_Msg_Type"] == "3":
                        points = int(event["Option1"])
                        if points > 0:
                            team_for = get_team_for(on_court, event["Person1"])
                            plus_minus = update_plus_minus(plus_minus, team_for, on_court, points)
                    counter += 1
                    event = game_events[counter]
                counter -= 1
                #swap new player in
                on_court = swap_players_in(on_court, players_subbing_in, players_subbing_out)
                #make sure new player is in plus minus dictionary
                for player in players_subbing_in:
                    if player not in plus_minus.keys():
                        plus_minus[player] = 0

            #free throw
            elif event["Event_Msg_Type"] == "3":
                points = int(event["Option1"])
                if points > 0:
                    team_for = get_team_for(on_court, event["Person1"])
                    plus_minus = update_plus_minus(plus_minus, team_for, on_court, points)


            #start period
            elif event["Event_Msg_Type"] == "12":
                on_court = game_lineup_reader.get_next_quarter()

                #make sure all players on court are in plus minus dictionary
                for team in on_court.keys():
                    for player in on_court[team]:
                        if player not in plus_minus.keys():
                            plus_minus[player] = 0
        
            counter += 1
        csv_writer.write_to_csv(game_id, plus_minus)
    csv_writer.close_file()

create_plus_minus_dict()
                
