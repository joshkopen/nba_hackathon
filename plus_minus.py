#import statements

def create_plus_minus_dict():
    for game in range(50):
        #game_events = get_next_game() -- gives a list of dictionaries
        for quarter in range(4):
            #on_court = get_on_court() -- gives a dictionary with pairs teamID : [players,on,court]
            for event in game_events:
                #handle each event type
                #made shot
                if event[]
                #free throw
                #substitution -- account for FT edge case (keep reading events until time is different and then update on court)
                #quarter end -- 'continue' to next quarter
                
