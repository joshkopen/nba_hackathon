from settings import csvfilename

class CSVWriter():
	'''
	Writes the appropriate data to a 
	csv file for submission.
	'''
	def __init__(self):
		self.file = open(csvfilename, "w")
		#establishes the column names for the CSV
		self.file.write("Game_ID, Player_ID, Player_Plus/Minus\n")

	def write_to_csv(self, game_id, players_dict):
		'''
		Writes the next entry to the csv file.
		Takes the parameters of a single String game_id
		and a list of dictionaries with players_dict
		which maps players to their +/-
		'''
		for player in players_dict:
			self.file.write("{}, {}, {}\n".format(game_id, player, players_dict[player]))

	def close_file(self):
		'''Safely closes the file being written to'''
		self.file.close()
