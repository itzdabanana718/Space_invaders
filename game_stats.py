class GameStats():
	"""track statistics for Alien Invasion"""
	
	def __init__(self, ai_settings):
		"""initialize statistics"""
		#start the game in an inactive state
		self.game_active = False
		self.ai_settings = ai_settings
		self.reset_stats()
		#highscore should never be reset
		self.high_score = 0
		self.level = 1

	def reset_stats(self):
		"""initialize stats that can change during the game"""
		self.ships_left = self.ai_settings.ship_limit
		self.score = 0


