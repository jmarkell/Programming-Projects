## Snake! 
## Another knock-off arcade game
## By J Markell with code concepts stolen from:
##
## http://inventwithpython.com/pygame
## Released under a "Simplified BSD" license

""" Nomenclature for the game:
	Window - This is where the game's surface will be contained. This will display all 
			 of the game's elements. It is broken into blocks and can be viewed as a grid.
	Apple - This is a single block that will be placed randomly somewhere in the window.
	Snake - This is a list of segmented blocks that is controlled by the player. The snake
			will always start with 3 segmented blocks.
	Game - This is the actual gameplay control and functionality. As the snake moves around 
		   eating the apples it will increase in length and increase the score. If the snake
		   moves off the screen or runs into itself the game will end.
"""

import random, pygame
from pygame.locals import *
import string

# Initialize pygame and the music mixer
pygame.init()
pygame.mixer.init()

################################################
#  Set up constants, colors, icons, and music  #
################################################

# Constants
BLOCK_SIZE = 20
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
assert WINDOW_WIDTH % BLOCK_SIZE == 0, "Window width must be a multiple of block size."
assert WINDOW_HEIGHT % BLOCK_SIZE == 0, "Window height must be a multiple of block size."

# These values can be used for a grid system based on block size
# to keep up with the snake and apples
GRID_WIDTH = int(WINDOW_WIDTH / BLOCK_SIZE)
GRID_HEIGHT = int(WINDOW_HEIGHT / BLOCK_SIZE)

FPS = 20

# Colors   	   R	G	 B
WHITE      = (255, 255, 255)
BLACK      = (  0,   0,   0)
RED        = (255,   0,   0)
GREEN      = (  0, 255,   0)
DARKRED    = (155,   0,   0)
DARKGREEN  = (  0, 155,   0)
DARKGRAY   = ( 50,  50,  50)
BG_COLOR   = BLACK

# Fonts
SMALL_FONT = pygame.font.Font("Retro.ttf", 25)
MED_FONT = pygame.font.Font("Retro.ttf", 50)
LARGE_FONT = pygame.font.Font("Retro.ttf", 80)

# Create constant names for the font sizes
SMALL = 'small'
MEDIUM = 'medium'
LARGE = 'large'

# Directions
RIGHT = 'right'
LEFT = 'left'
UP = 'up'
DOWN = 'down'

DIRECTIONS = [RIGHT, UP, LEFT, DOWN]

# Music - add in music and sound effects here
""" YOUR CODE HERE """


# Icons and Title
""" YOU MAY CHANGE THIS TO YOUR LIKING """


class Window(object):
	""" Window class: represents the game surface
			Atrributes: surface - type: pygame.display object - surface for the game to be displayed on
						size - type: tuple of integers - WINDOW_WIDTH x WINDOW_HEIGHT
						gridflag - type: bool - turns the grid on or off
						fps_clock - type: pygame.time.Clock object - use this to update the surface at a certain FPS
						fonts - type: dictionary of the small, med, and large fonts
	"""
	def __init__(self, size):
		""" YOUR CODE HERE """
		
		
		
	# This method will update the window depending on which game state the player is
	# in. The three game states are 'intro', 'game_play', 'game_over'. If in 'intro'
	# the window will display the intro screen. If in 'game_over' it will display the
	# game_over screen. 'game_play' will update based on the actual game play.
	def update(self, state = None, apple = None, snake = None, score = 0):
		# Delete this if statement once you have implemented the other methods in this class
		if state == None:
			print 'Other methods not implemented yet'
		
		""" YOUR CODE HERE """	
		pygame.display.update()
		self.fps_clock.tick(FPS)
		
	def display_intro(self):
		self.surface.fill(DARKGRAY)
		self.display_text("Welcome to Snake", GREEN, LARGE, -100)
		self.display_text("The objective of the game is to eat red apples and grow,", WHITE, y_disp = -30)
		self.display_text("The more apples you eat, the longer you get,", WHITE, y_disp = 10)
		self.display_text("If you run into yourself or the edges you lose.", WHITE, y_disp = 50)
		self.display_text("Press G for a grid and Q to quit.", WHITE, y_disp = 90)
		self.display_text("Press any key to continue...", WHITE, y_disp = 160)
	
	def display_game_over(self):
		""" YOUR CODE HERE """
		pass
		
	def display_score(self, score = 0):
		""" YOUR CODE HERE """
		pass
		
	def draw_grid(self):
		for x in xrange(0, WINDOW_WIDTH, BLOCK_SIZE):
			pygame.draw.line(self.surface, DARKGRAY, (x, 0), (x, WINDOW_HEIGHT))
		for y in xrange(0, WINDOW_HEIGHT, BLOCK_SIZE):
			pygame.draw.line(self.surface, DARKGRAY, (0, y), (WINDOW_WIDTH, y))
			
	def create_text(self, msg, color, size):
		font = self.fonts[size]
		text_surf = font.render(msg, True, color)
		return text_surf, text_surf.get_rect()
		
	def display_text(self, msg, color, size = SMALL, y_disp = 0):
		text_surf, text_rect = self.create_text(msg, color, size)
		text_rect.center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + y_disp)
		self.surface.blit(text_surf, text_rect)

class Apple(object):
	""" Apple class: represents an apple object
			Attributes: color - type: RGB tuple - main color of the apple
						accent - type: RGB tuple - shadow color of the apple 
						location - type: int tuple - location of the apple in terms of the grid
	"""
	def __init__(self, color, accent, location):
		""" YOUR CODE HERE """
		pass
		
	def draw(self, surface):
		""" YOUR CODE HERE """
		pass
		
class Snake(object):
	def __init__(self, color, accent, init_location):
		self.color = color
		self.accent = accent
		self.direction = random.choice(DIRECTIONS)
		
		# Check the direction that the snake starts in and
		# make sure that the body is aligned correctly
		init_x, init_y = init_location
		if self.direction == RIGHT:
			self.snake_list = [(    init_x, init_y),
							   (init_x - 1, init_y),
							   (init_x - 2, init_y)]
		
		if self.direction == LEFT:
			self.snake_list = [(    init_x, init_y),
							   (init_x + 1, init_y),
							   (init_x + 2, init_y)]
		
		if self.direction == UP:
			self.snake_list = [(init_x,     init_y),
							   (init_x, init_y + 1),
							   (init_x, init_y + 2)]
		
		if self.direction == DOWN:
			self.snake_list = [(init_x,     init_y),
							   (init_x, init_y - 1),
							   (init_x, init_y - 2)]
		
		self.length = len(self.snake_list)
	
	def draw(self, surface):
		for coord in self.snake_list:
			x = coord[0] * BLOCK_SIZE
			y = coord[1] * BLOCK_SIZE
			snake_seg_acc = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
			snake_seg = pygame.Rect(x + 2, y + 2, BLOCK_SIZE - 4, BLOCK_SIZE - 4)
			pygame.draw.rect(surface, self.accent, snake_seg_acc)
			pygame.draw.rect(surface, self.color, snake_seg)
	 
	def move(self):
		# move the snake by adding a segment in the direction that it will move
		""" YOUR CODE HERE """
		pass
		
	def eat(self, apple):
		# checks if the snake eats an apple. returns True if it does, False if not
		# updates the length of the snake
		""" YOUR CODE HERE """
		pass
		
class Game(object):
	def __init__(self):
		# Game has three states: intro, game_play, game_over
		self.state = 'intro'
		
		app_location = self.get_random_location('apple')
		snake_location = self.get_random_location('snake')
		
		""" YOU MAY CHANGE THE COLOR OF THE APPLE OR SNAKE HERE """
		self.apple = Apple(RED, DARKRED, (app_location))
		self.snake = Snake(GREEN, DARKGREEN, (snake_location))
		
		self.window = Window((WINDOW_WIDTH, WINDOW_HEIGHT))
		self.score = 0
		
	def check_key_press(self):
		# Check if there are any events that correspond with a key press
		events = pygame.event.get(KEYUP)
		if len(events) == 0:
			return False
		return True
	
	def terminate(self):
		pygame.quit()
		quit()
		
	def get_random_location(self, object_type):
		""" YOUR CODE HERE """
		# Delete the following line of code once your method is implemented.
		return (0, 0)
		'''if object_type == 'apple':
			return (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
		elif object_type == 'snake':
			return (random.randint(7, GRID_WIDTH - 8), random.randint(5, GRID_HEIGHT - 6))
		else:
			print 'Only options are apple or snake'
			return (0, 0)'''
	
	def intro(self):
		# This method will display the intro screen until a key is pressed
		""" YOUR CODE HERE """
		'''while True:
			self.window.update(self.state)
			if self.check_key_press():
				self.state = 'game_play'
				return
		'''
		pass
		
	def game_play(self):
		# re_initialize the score if playing the game again
		self.score = 0
		while True:
			for event in pygame.event.get():
				if event.type == QUIT:
					self.terminate()
					
				if event.type == KEYDOWN:
					if event.key == K_ESCAPE:
						self.terminate()
			
			""" YOUR CODE HERE """		
			
	def game_over(self):
		play_again = False
		while not play_again:
			self.window.update(self.state)
			for event in pygame.event.get():
				if event.type == QUIT:
					self.terminate()
				if event.type == KEYDOWN:
					if event.key == K_ESCAPE or event.key == K_q:
						self.terminate()
					if event.key == K_n:
						return True
						
		
	def run_game(self):		
		# Run the intro window until a key is pressed
		self.intro()
		
		# Play the game until the snake either hits a wall or itself
		self.game_play()
		
		# Display the game_over window until a new game is started or the player quits
		if self.game_over():
			self.__init__()
			self.run_game()

			
######################################################################

""" TEST CASES HELPERS HERE """
def quit_helper():
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			quit()
		if event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				pygame.quit()
				quit()

def display_tester(tstate = None, tapple = None, tsnake = None, tscore = 0):
	window = Window((WINDOW_WIDTH, WINDOW_HEIGHT))
	while True:
		timer = 0

		while timer < 10:
			quit_helper()
			window.update(state = 'intro', apple = tapple, snake = tsnake)
			timer += 1
		
		timer = 0
		while timer < 10:
			quit_helper()
			window.update(state = 'game_play', apple = tapple, snake = tsnake)
			timer += 1
			
		timer = 0
		while timer < 10:
			quit_helper()
			window.update(state = 'game_over', apple = tapple, snake = tsnake)
			timer += 1

def snake_tester(tstate = 'game_play', tsnake = None, tscore = 0):
	window = Window((WINDOW_WIDTH, WINDOW_HEIGHT))
	tapple = Apple(RED, DARKRED, (10, 15))
	direction = 0
	while True:
		quit_helper()
		tsnake.direction = DIRECTIONS[direction]
		for x in range(0, 5):
			tsnake.move()
		window.update(tstate, apple = tapple, snake = tsnake)
		if direction == 3:
			direction = 0
		else:
			direction += 1
		
#####################################################################
### TEST CASES FOR PART 1 - WINDOW, APPLE, SNAKE CLASS 
''' Uncomment each test case when you are ready '''

# Test case 1 -> Window update for intro and game_over
#display_tester()

# Test case 2 -> Window update for snake object
#snake2 = Snake(GREEN, DARKGREEN, (10,20))
#display_tester(tsnake = snake2)

# Test case 3 -> Window update for snake and apple objects
#snake3 = Snake(GREEN, DARKGREEN, (15,20))
#apple3 = Apple(RED, DARKRED, (5, 10))
#display_tester(tapple = apple3, tsnake = snake3)

# Test case 4 -> All displays
#snake4 = Snake(GREEN, DARKGREEN, (15,20))
#apple4 = Apple(RED, DARKRED, (5, 10))
#display_tester(tapple = apple4, tsnake = snake4)


