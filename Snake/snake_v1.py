import random, pygame
from pygame.locals import *
import string

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

EZ_FPS   = 15
MED_FPS  = 20
HARD_FPS = 30

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

SMALL = 'small'
MEDIUM = 'medium'
LARGE = 'large'

# Directions
RIGHT = 'right'
LEFT = 'left'
UP = 'up'
DOWN = 'down'

DIRECTIONS = [RIGHT, LEFT, UP, DOWN]

# Music
pygame.mixer.music.load('game_music.ogg')
pygame.mixer.music.play(-1)
#GAME_MUSIC = pygame.mixer.Sound('game_music.wav')
#GAME_MUSIC.play(-1)
'''
EATING_FX = pygame.mixer.Sound('eating_fx.ogg')
APPLE_FX = pygame.mixer.Sound('apple_fx.ogg')
'''

# Icons and Title
ICON_IMAGE = pygame.image.load('icon.png')
TITLE = 'SNAKE!'

class Window(object):
	def __init__(self, size):
		self.size = size
		self.surface = pygame.display.set_mode(size)
		
		self.gridflag = False
		
		pygame.display.set_caption(TITLE)
		pygame.display.set_icon(ICON_IMAGE)
		
		self.fps_clock = pygame.time.Clock()
		self.fonts = {SMALL: SMALL_FONT, MEDIUM: MED_FONT, LARGE: LARGE_FONT}
		
	def update(self, state, apple = None, snake = None, score = 0, difficulty = EZ_FPS):
		if state == 'intro':
			self.display_intro()
		elif state == 'game_play':
			self.surface.fill(BG_COLOR)
			if self.gridflag:
				self.draw_grid()
			self.display_score(score)
			snake.draw(self.surface)
			apple.draw(self.surface)
		elif state == 'game_over':
			self.display_game_over()
			
		pygame.display.update()
		self.fps_clock.tick(difficulty)
		
	def display_intro(self):
		self.surface.fill(DARKGRAY)
		self.display_text("Welcome to Snake", GREEN, LARGE, -100)
		self.display_text("The objective of the game is to eat red apples and grow,", WHITE, y_disp = -30)
		self.display_text("The more apples you eat, the longer you get,", WHITE, y_disp = 10)
		self.display_text("If you run into yourself or the edges you lose.", WHITE, y_disp = 50)
		self.display_text("Press G for a grid and Q to quit.", WHITE, y_disp = 90)
		self.display_text("Press any key to continue...", WHITE, y_disp = 160)
	
	def display_game_over(self):
		self.surface.fill(DARKGRAY)
		self.display_text('GAME', GREEN, LARGE, -100)
		self.display_text('OVER', GREEN, LARGE)
		self.display_text('Press N to play again or Q to quit.', BLACK, y_disp = 150)
	
	def display_score(self, score):
		score_surf, score_rect = self.create_text("Score: %s" % score, WHITE, SMALL)
		score_rect.topleft = (10, 10)
		self.surface.blit(score_surf, score_rect)
		
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
	def __init__(self, color, accent, location):
		self.color = color
		self.accent = accent
		self.location = location
		
	def draw(self, surface):
		x, y = self.location
		x *= BLOCK_SIZE
		y *= BLOCK_SIZE
		pygame.draw.rect(surface, self.accent, (x, y, BLOCK_SIZE, BLOCK_SIZE))
		pygame.draw.rect(surface, self.color, (x + 2, y + 2, BLOCK_SIZE - 4, BLOCK_SIZE - 4))

class Snake(object):
	def __init__(self, color, accent, init_location):
		self.color = color
		self.accent = accent
		self.direction = random.choice(DIRECTIONS)
		
		# Check the direction that the snake starts in
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
	
	# move the snake by adding a segment in the direction that it will move
	# check if the snake will eat an apple. if it does then don't remove the
	# tail segment. if it doesn't then remove the tail 
	def move(self):
		head_x, head_y = self.snake_list[0]
		if self.direction == RIGHT:
			new_head = (head_x + 1, head_y)
		elif self.direction == LEFT:
			new_head = (head_x - 1, head_y)
		elif self.direction == UP:
			new_head = (head_x, head_y - 1)
		elif self.direction == DOWN:
			new_head = (head_x, head_y + 1)
		
		self.snake_list.insert(0, new_head)
		
	# checks if the snake eats an apple. returns True if it does, False if not
	# updates the length of the snake
	def eat(self, apple):
		head_x, head_y = self.snake_list[0]
		app_x, app_y = apple.location
		if head_x == app_x and head_y == app_y:
			self.length = len(self.snake_list)
			return True
		else:
			return False
		
class Game(object):
	def __init__(self, difficulty = EZ_FPS):
		self.difficulty = difficulty
		
		# Game has three states: intro, game_play, game_over
		self.state = 'intro'
		
		app_location = self.get_random_location('apple')
		snake_location = self.get_random_location('snake')
		self.apple = Apple(RED, DARKRED, (app_location))
		self.snake = Snake(GREEN, DARKGREEN, (snake_location))
		self.window = Window((WINDOW_WIDTH, WINDOW_HEIGHT))
		self.score = 0
		
	def check_key_press(self):
		events = pygame.event.get(KEYUP)
		if len(events) == 0:
			return False
		return True
	
	def terminate(self):
		pygame.quit()
		quit()
		
	def get_random_location(self, object_type):
		if object_type == 'apple':
			return (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
		elif object_type == 'snake':
			return (random.randint(7, GRID_WIDTH - 8), random.randint(5, GRID_HEIGHT - 6))
		else:
			print 'Only options are apple or snake'
			return (0, 0)
	
	def intro(self):
		while True:
			self.window.update(self.state)
			if self.check_key_press():
				self.state = 'game_play'
				return
	
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
					if event.key == K_q:
						self.terminate()
					if event.key == K_g:
						self.window.gridflag = not self.window.gridflag
				
			
					if event.key == K_UP and self.snake.direction is not DOWN:
						self.snake.direction = UP
						break
					if event.key == K_DOWN and self.snake.direction is not UP:
						self.snake.direction = DOWN
						break
					if event.key == K_LEFT and self.snake.direction is not RIGHT:
						self.snake.direction = LEFT
						break
					if event.key == K_RIGHT and self.snake.direction is not LEFT:
						self.snake.direction = RIGHT
						break
			
			head_x, head_y = self.snake.snake_list[0]
			if head_x <= -1 or head_x >= GRID_WIDTH or head_y <= -1 or head_y >= GRID_HEIGHT:
				self.state = 'game_over'
				return
			for segment in self.snake.snake_list[1:]:
				if segment[0] == head_x and segment[1] == head_y:
					self.state = 'game_over'
					return
				
			self.snake.move()
			if not self.snake.eat(self.apple):
				self.snake.snake_list.pop()
			else:
				app_location = self.get_random_location('apple')
				self.apple = Apple(RED, DARKRED, (app_location))
			self.score = self.snake.length - 3
			self.window.update(self.state, self.apple, self.snake, self.score, self.difficulty)			
			
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
			
game = Game()
game.run_game()