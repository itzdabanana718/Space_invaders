from pygame.sprite import Group
import pygame.font

from ship import Ship

class Scoreboard():
	"""a class to report score information"""
	
	def __init__(self, ai_settings, screen, stats):
		"""initialize scorekeeping attributes"""
		self.screen = screen
		self.screen_rect = screen.get_rect()
		self.ai_settings = ai_settings
		self.stats = stats
		
		#font settings
		self.text_color = (30, 30, 30)
		self.font = pygame.font.SysFont(None, 48)
		
		#prepare the initial score image
		self.prep_score()
		self.prep_high_score()
		self.prep_level()
		self.prep_ships()
		
		
	def prep_ships(self):
		"""show how many ships are left"""
		self.ships = Group()
		for ship_number in range(self.stats.ships_left):
			ship = Ship(self.ai_settings, self.screen)
			ship.rect.x = ship_number * ship.rect.width
			ship.rect.y = 10
			self.ships.add(ship)
		
		
		
		
	def prep_score(self):
		"""turn score into a rendered image"""
		rounded_score = int(round(self.stats.score, -1))
		score_str = "{:,}".format(rounded_score)
		score_str = str(self.stats.score)
		self.score_image = self.font.render(score_str, True, self.text_color,
			self.ai_settings.bg_color)
		self.score_rect = self.score_image.get_rect()
		
		#display the score in the top right
		self.score_rect = self.score_image.get_rect()
		self.score_rect.right = self.screen_rect.right - 5
		self.score_rect.top = 1
		
		
	def show_score(self):
		"""draw score to the game"""
		self.screen.blit(self.score_image, self.score_rect)
		self.screen.blit(self.high_score_image, self.high_score_rect)
		
		self.screen.blit(self.level_image, self.level_rect)
		#draw ships
		self.ships.draw(self.screen)
		
	def prep_high_score(self):
		"""turn the highscore into an image"""
		high_score = int(round(self.stats.high_score, -1))
		high_score_str = "{:,}".format(high_score)
		self.high_score_image = self.font.render(high_score_str, True,
			self.text_color, self.ai_settings.bg_color)
			
		#center the highscore at the top of the screen
		self.high_score_rect = self.high_score_image.get_rect()
		self.high_score_rect.centerx = self.screen_rect.centerx
		self.high_score_rect.top = self.high_score_rect.top
	
	def prep_level(self):
		"""turn the level into a rendered image"""
		self.level_image = self.font.render(str(self.stats.level), True,
				self.text_color, self.ai_settings.bg_color)
				
		#position the level below the score
		self.level_rect = self.level_image.get_rect()
		self.level_rect.right = self.screen_rect.right
		self.level_rect.top = self.score_rect.bottom + 10
