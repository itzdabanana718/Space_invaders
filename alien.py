import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
	"""A class to represent a single alien in the fleet"""
	
	def __init__(self, ai_settings, screen):
		"""initialize the alien and its starting position"""
		super(Alien, self).__init__()
		self.screen = screen
		self.ai_settings = ai_settings
		
		#Load the alien image and set its rect attribute
		self.image = pygame.image.load('images/alien.bmp')
		self.rect = self.image.get_rect()
		
		#start each new alien near the top of the screen
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height
		
		#store the aliens exact position
		self.x = float(self.rect.x)
		self.y = float(self.rect.y)
		
	def blitme(self):
		"""draw the alien at its current location"""
		self.screen.blit(self.image, self.rect)
	def check_edges(self):
		"""return True if an alien is at the edge of the screen"""
		screen_rect = self.screen.get_rect()
		if self.rect.right >= screen_rect.right:
			return True
		elif self.rect.left <= 0:
			return True	
		
		
	def update(self):
		"""move the alien left or right"""
		self.x += (self.ai_settings.alien_speed_factor *
						self.ai_settings.fleet_direction)
		self.rect.x = self.x
