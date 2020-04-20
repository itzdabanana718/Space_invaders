
class Settings():
	"""a class to store all the settings for Alien invasion"""
	def __init__(self):
		"""initialize the game's settings"""
		
		#screen settings
		self.screen_width = 1200
		self.screen_height = 800
		self.bg_color = (230, 230, 230)

		#ship settings
		
		self.ship_limit = 3
		self.ship_speed_factor = 5
		#bullet settings
		
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_color = (60, 60, 60)
		self.bullets_allowed = 3
		self.bullet_speed_factor = 3
		#alien settings
		self.fleet_drop_speed = 10
		self.fleet_direction = 1
		self.alien_speed_factor = 1

		#how quickly the game speeds up
		self.speedup_scale = 1.2
		#how quickly the aliens points increase
		self.score_scale = 1.5
		
		self.initialize_dynamic_settings()
		
		#scoring
		self.alien_points = 10
	
	def initialize_dynamic_settings(self):
		"""inititalize settings that change throughout the game"""
		self.bullet_speed_factor = 3
		self.ship_speed_factor = 1.5
		#fleet direction 1 represents right; -1 represents left
		self.fleet_direction = 1
		self.alien_speed_factor = 1

	def increase_speed(self):
		"""increase speed settings"""
		self.bullet_speed_factor *= self.speedup_scale
		self.ship_speed_factor *= self.speedup_scale
		self.alien_speed_factor *= self.speedup_scale
		
		self.alien_points = int(self.alien_points * self.score_scale)
