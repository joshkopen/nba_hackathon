#import statements


#create dictionary with key for each unique person_id and value of 0
def initialize_plus_minus_dict():
    plus_minus = {}
    #NEED LINEUP ELSE I CAN JUST TEST TO SEE IF PLAYER IN DICT ALREADY AND GET RID OF THIS METHOD
    for player in lineup:
        plus_minus[player] = 0
    return plus_minus

def create_plus_minus_dict():
    for game in range(50):
        plus_minus = {}
        #plus_minus = initialize_plus_minus_dict()
        #game_events = get_next_game() -- gives a list of dictionaries
        for event in game_events:
            #handle each event type
            #start period -- *import module for function
            if event["Event_Msg_Type"] == 12:
                on_court = get_on_court()

            #made shot
            if event["Event_Msg_Type"] == 1:
                points = event["Option1"]
                team_for = event["Team_id"]
                for team in on_court:
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

            #substitution
            if event["Event_Msg_Type"] == 8:
                #STILL NEED TO HANDLE FOR FREE THROW EDGE CASE
                team = event["Team_id"]
                old_player = event["Person1"]
                new_player = event["Person2"]
                players_on_court = on_court[team]
                player_idx = players_on_court.index(old_player)
                players_on_court[player_idx] = new_player
                on_court[team] = players_on_court

            #free throw
            if event["Event_Msg_Type"] == 3:
                if event["Option1"] == 0:
                    pass
                else:
                    points = event["Option1"]
                    team_for = event["Team_id"]
                    for team in on_court:
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

            #free throw -- "no shot"??
            #substitution -- account for FT edge case (keep reading events until time is different and then update on court) 
            #NEED TO HANDLE FOR EJECTION??? -- is player 1 and player 2 same as if it was a substitution?? -- if so then can just lump in with substitution
            #should I make a plus minus updater function -- pass it dictionary, points, etc. and it will update
                
