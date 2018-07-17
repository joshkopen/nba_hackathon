from settings import play_by_play_filename, needed_fields_play_by_play as needed_fields

class PlayByPlayReader():

	def __init__(self):
		self.file = open(play_by_play_filename, "r")
		self.dictionary_keys = []
		first_line = self.file.readline()
		for keyword in first_line.split():
			self.dictionary_keys.append(keyword)

		self.from_last_run_event = self._build_dict(self.file.readline())

	def get_next_game(self):
		if self.from_last_run_event is None:
			return False
		game_id = self.from_last_run_event["Game_id"]
		current_event = self.from_last_run_event
		return_list = []

		while current_event is not None and current_event["Game_id"] == game_id:
			return_list.append(current_event)
			current_event = self._build_dict(self.file.readline())

		self.from_last_run_event = current_event
		return return_list

	def _build_dict(self, line):
		if len(line.split()) == 0:
			return None
		play_dict = {}
		counter = 0
		for value in line.split():
			if self.dictionary_keys[counter] in needed_fields:
				play_dict[self.dictionary_keys[counter]] = value
			counter += 1
		return play_dict
