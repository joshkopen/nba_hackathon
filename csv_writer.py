
class CSVWriter():
	'''
	Writes the appropriate data to a 
	csv file for submission.
	'''
	def __init__(self):
		self.file = open("Cameron_Coders_Q1_BBALL", "w")
		self.file.write("Game_ID, Player_ID, Player_Plus/Minus\n")

	def write_to_csv(self, game_id, player_dict):
		for player in player_dict:
			self.file.write("{}, {}, {}\n".format(game_id, player, player_dict[player]))

	def close_file(self):
		self.file.close()
