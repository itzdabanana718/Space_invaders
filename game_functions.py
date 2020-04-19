import pygame
import sys
from bullet import Bullet
from alien import Alien
from time import sleep
from game_stats import GameStats
from settings import Settings
from scoreboard import Scoreboard


ai_settings = Settings()
stats = GameStats(ai_settings)

def check_high_score(stats, sb):
	"""check to see if there is a new high score"""
	if stats.score > stats.high_score:
		stats.high_score = stats.score
		sb.prep_high_score()

def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
	"""check if aliens hit the bottom"""
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			#treat this the same as if alien hit ship
			alien.rect.y = 0
			
			#print("reached the bottom") 
			break

def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
	"""responds to the ship being hit by an alien"""
	if stats.ships_left > 0:
		#decrement ships_left
		stats.ships_left -= 1
	
	
		#update scoreboard
		sb.prep_ships()
		#empty alien and bullets list
		aliens.empty()
		bullets.empty()
	
		#create a new fleet and center ship
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()
		
		#pause
		sleep(0.5)
	else:
		ship.center_ship()
		stats.game_active = False
		pygame.mouse.set_visible(True)
def create_fleet(ai_settings, screen, ship, aliens):
	"""create a whole fleet"""
	#create an alie and find out how many aliens per row
	alien = Alien(ai_settings, screen)
	number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
	number_rows = get_number_rows(ai_settings, ship.rect.height,
		alien.rect.height)
	#create the first row of aliens
	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x):
			create_alien(ai_settings, screen, aliens, alien_number,
				row_number)
	
	
def get_number_rows(ai_settings, ship_height, alien_height):
	"""determin the number of rows that can fit on screen"""
	available_space_y = (ai_settings.screen_height - 
							(3 * alien_height) - ship_height)
	number_rows = int(available_space_y / (2 * alien_height))
	return number_rows
	
def get_number_aliens_x(ai_settings, alien_width):
		"""determine the number of aliens that fit in a row"""
		available_space_x = ai_settings.screen_width - 2 * alien_width
		number_aliens_x = int(available_space_x / (2 * alien_width))
		return number_aliens_x
		
def create_alien(ai_settings, screen, aliens, alien_number, row_number):
	alien = Alien(ai_settings, screen)
	alien_width = alien.rect.width
	alien.x = alien_width + 2 * alien_width * alien_number
	alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
	alien.rect.x = alien.x
	aliens.add(alien)

def check_keydown_events(event, ai_settings, screen, ship, bullets):
	"""responds to key presses"""
	if event.key == pygame.K_RIGHT:
		ship.moving_right = True
	elif event.key == pygame.K_LEFT:
		ship.moving_left = True
	elif event.key == pygame.K_SPACE:
		fire_bullet(ai_settings, screen, ship, bullets)	
	elif event.key == pygame.K_UP:
		ship.moving_up = True
	elif event.key == pygame.K_DOWN:
		ship.moving_down = True
	elif event.key == pygame.K_p:
		stats.game_still_active = True

def check_keyup_events(event, ship):
	"""responds to key releases"""
	if event.key ==	pygame.K_RIGHT:
		ship.moving_right = False
	elif event.key == pygame.K_LEFT:
		ship.moving_left = False
	elif event.key == pygame.K_ESCAPE:
		sys.exit()	
	elif event.key == pygame.K_UP:
		ship.moving_up = False
	elif event.key == pygame.K_DOWN:
		ship.moving_down = False

def fire_bullet(ai_settings, screen, ship, bullets):
	"""fire a bullet if the limit is not yet reached"""
	if len(bullets) < ai_settings.bullets_allowed:
		new_bullet = Bullet(ai_settings, screen, ship)
		bullets.add(new_bullet)	
def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
	"""update the position of bullets and get rid of old bullets"""
	#update bullet position
	bullets.update()
	#get rid of bullets once they disappear
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)
	
	check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
		aliens, bullets)	

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
	aliens, bullets):
	"""repond to bullet-alien collisions"""
	#remove any bullets and aliens that have collided	
	collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)	
	
	for aliens in collisions.values():
		stats.score += ai_settings.alien_points * len(aliens)
	sb.prep_score()
	if len(aliens) == 0:
		#destroy existing bullets and create a new fleet
		bullets.empty()
		ai_settings.increase_speed()
		create_fleet(ai_settings, screen, ship, aliens)
		#increase level
		stats.level += 1
		sb.prep_level()
		
		
	check_high_score(stats, sb)
def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
	#watch for keyboard and mouse events 
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
			
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event, ai_settings, screen, ship, bullets)
		
		elif event.type == pygame.KEYUP:
			check_keyup_events(event, ship)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			check_play_button(ai_settings, screen, stats, sb, play_button,
				ship, aliens, bullets, mouse_x, mouse_y)			
def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens,
		 bullets, mouse_x, mouse_y):
	"""start new game when player clicks start"""
	if play_button.rect.collidepoint(mouse_x, mouse_y) and not stats.game_active:
		#reset game stats
		ai_settings.initialize_dynamic_settings()
		pygame.mouse.set_visible(False)
		stats.reset_stats()
		stats.game_active = True
		
		sb.prep_score()
		sb.prep_high_score()
		sb.prep_level()
		sb.prep_ships()
		#empty aliens and bullets
		aliens.empty()
		bullets.empty()
		
		#create new alien fleet
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()			
def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
	screen.fill(ai_settings.bg_color)
	sb.show_score()
	#draw ship on
	ship.blitme()
	aliens.draw(screen)
	#redraw all bullets behind ship and aliens
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	#draw a button if game is inactive
	if not stats.game_active:
		play_button.draw_button()
	#make the most recently drawn screen visible
	pygame.display.flip()	
def update_aliens(ai_settings, screen, stats, sb, ships, aliens, bullets):
	check_fleet_edges(ai_settings, aliens)
	#check if aliens hit the bottom
	check_aliens_bottom(ai_settings, screen, stats, sb, ships, aliens, bullets)
	
	aliens.update()
	if pygame.sprite.spritecollideany(ships, aliens):
		ship_hit(ai_settings, screen, stats, sb, ships, aliens, bullets)
		
def change_fleet_direction(ai_settings, aliens):
	"""drop the entire fleet and change their direction"""
	ai_settings.fleet_direction *= -1
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed	
def check_fleet_edges(ai_settings, aliens):
	"""respond appropriatly if any aliens have reached an edge"""
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings, aliens)
			break

