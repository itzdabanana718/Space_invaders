import sys
import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


def run_game():
	"""initialize pygame, settings and screen object"""
	pygame.init()
	ai_settings = Settings()
	screen = pygame.display.set_mode(
		(ai_settings.screen_width, ai_settings.screen_height))
	pygame.display.set_caption("Alien Invasion")
	stats = GameStats(ai_settings)
	sb = Scoreboard(ai_settings, screen, stats)
	
	#make the play button  
	play_button = Button(ai_settings, screen, "Play")
	
	# make a ship
	ship = Ship(ai_settings, screen)
	#make a group to hold the bullets
	bullets = Group()
	#make an alien
	aliens = Group()
	death = Group()
	#create a fleet of aliens
	gf.create_fleet(ai_settings, screen, ship, aliens)
	#create an instance to store game stats and create a scoreboard
	stats = GameStats(ai_settings)
	sb = Scoreboard(ai_settings, screen, stats)
	#start the main loop for the game
	sb = Scoreboard(ai_settings, screen, stats)
	while True:
		sb = Scoreboard(ai_settings, screen, stats)
		gf.check_events(ai_settings, screen, stats, sb, play_button,
			ship, aliens, bullets)
		if stats.game_active:
			
			ship.update()
			gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
			gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets)
		
		gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)
		

		
		
run_game()
