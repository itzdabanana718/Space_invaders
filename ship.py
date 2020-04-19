import pygame
from pygame.sprite import Sprite



class Ship(Sprite):
	
	def __init__(self, ai_settings, screen):
		"""initialize the ship and its starting position"""
		super(Ship, self).__init__()
		self.screen = screen
		self.ai_settings = ai_settings
		#load the image and get its rect
		self.image = pygame.image.load('images/ship.bmp')
		self.health = pygame.image.load("images/health.png")
		self.health = pygame.transform.scale(self.health, (50, 30))
		self.health_rect = self.health.get_rect()
		self.rect = self.image.get_rect()
		self.screen_rect = screen.get_rect()
		self.health_rect = self.health.get_rect()
		
		#start each new ship at the bottom middle of the screen
		self.rect.centerx = self.screen_rect.centerx
		self.rect.bottom = self.screen_rect.bottom
		
		#store a decimal value for the ships center
		self.center = float(self.rect.centerx)
		self.middle = float(self.rect.centery)
		self.bottom = float(self.rect.bottom)
		
		#moving flag
		self.moving_right = False
		self.moving_left = False
		self.moving_up = False
		self.moving_down = False
		
	def update(self):
		"""update ships position based on movement flag"""
		if self.moving_right:
			self.center += self.ai_settings.ship_speed_factor
			
		if self.rect.left > self.screen_rect.right + 10:
			self.center = -10
		
		if self.rect.right < self.screen_rect.left - 10:
			self.center = self.screen_rect.right + 10
		
		if self.moving_left:
			self.center -= self.ai_settings.ship_speed_factor
		
		if self.moving_up and self.rect.top > 0:
			self.middle -= self.ai_settings.ship_speed_factor
		
		if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
			self.middle += self.ai_settings.ship_speed_factor
		#update rect object from self.center
		self.rect.centerx = self.center
		self.rect.centery = self.middle
	
	def blitme(self):
		"""draw the ship at its current location"""
		self.screen.blit(self.image, self.rect)

	def center_ship(self):
		"""center the ship on screen"""
		self.center = self.screen_rect.centerx
		self.middle = self.screen_rect.bottom - 20
		
