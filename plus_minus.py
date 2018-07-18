#import statements
from play_by_play_reader import PlayByPlayReader
from game_lineup_reader import LineupReader
from csv_writer import CSVWriter

def create_plus_minus_dict():
    play_by_play_reader = PlayByPlayReader()
    game_lineup_reader = LineupReader()
    csv_writer = CSVWriter()

    for game in range(50):
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
                team_for = event["Team_id"]
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

            #substitution
            elif event["Event_Msg_Type"] in ["8","11"]:

                team = event["Team_id"]
                old_player = event["Person1"]
                new_player = event["Person2"]
                players_on_court = on_court[team]
                player_idx = players_on_court.index(old_player)

                '''
                when the substitution happens before a free throw,
                update the plus/minus of players on the court when
                the foul occurred for the free throw event before
                updating the players on the court
                '''
                time_of_sub = event["PC_Time"]
                while(event["PC_Time"] == time_of_sub):
                    if int(event["Option1"]) == 1:
                        points = 1
                        team_for = event["Team_id"]
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
                        counter += 1

                #swap new player in
                players_on_court[player_idx] = new_player
                on_court[team] = players_on_court
                #make sure new player is in plus minus dictionary
                if new_player not in plus_minus.keys():
                    plus_minus[new_player] = 0

            #free throw
            elif event["Event_Msg_Type"] == 3:
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

            #start period -- *import module for function
            if event["Event_Msg_Type"] == 12:
                on_court = game_lineup_reader.get_next_quarter()

                #make sure all players on court are in plus minus dictionary
                for team in on_court.keys():
                    for player in on_court[team]:
                        if player not in plus_minus.keys():
                            plus_minus[player] = 0
        
            counter += 1
        write_csv(game_id, plus_minus)



# def write_csv(game_id, plus_minus_dict):
#     with open("cameron_coders.csv", 'wb') as csvfile:
#         writer = csv.writer(csvfile)
#         header = ["Game_id","Player","Plus/Minus"]
#         writer.writerow(header)
#         for player in plus_minus_dict.keys():
#             plus_minus_score = plus_minus_dict[player]
#             writer.writerow([game_id,player,plus_minus_score])

            #LAST THING TO DO: should I make a plus minus updater function -- pass it dictionary, points, etc. and it will update
                
