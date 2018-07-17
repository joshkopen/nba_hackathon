from settings import game_lineup_filename

class EndOfFileException(Exception):
	''' Exception raised when
	the file has ended and no
	more can be read'''
	def __init__(self,*args,**kwargs):
		Exception.__init__(self,*args,**kwargs)

class LineupReader():

	def __init__(self):
		self.file = open(game_lineup_filename, "r")
		#sets up the dictionary keys for line reading
		#utilizing the first line in the file
		self.dictionary_keys = []
		first_line = self.file.readline()
		for keyword in first_line.split():
			self.dictionary_keys.append(keyword)

	def get_next_quarter(self):
		'''
		Returns the starting lineup for the next
		quarter of play
		'''
		team_dict = {}

		#it's 10 for the number of players on the court
		try:
			for i in range(10):
				individual_dict = self._parse_to_dict(self.file.readline())
				#checks if team already in the team_dict, if so appended,
				#if not, it's added
				if individual_dict['Team_id'] in team_dict:
					team_dict[individual_dict['Team_id']].append(individual_dict['Person_id'])
				else:
					team_dict[individual_dict['Team_id']] = [individual_dict['Person_id']]
			return team_dict
		except EndOfFileException:
			return False

	def _parse_to_dict(self, line):
		'''
		Uses pre-established dictionary keys from __init__
		to create dictionary
		'''
		if len(line.split()) == 0:
			raise EndOfFileException('There are no more lines left')
		individual_dict = {}
		counter = 0
		for value in line.split():
			individual_dict[self.dictionary_keys[counter]] = value
			counter += 1
		return individual_dict