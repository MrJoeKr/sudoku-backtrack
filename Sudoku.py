import os
import pygame
from pygame import *
import time
import math
import random
import threading


# NUMBERS on solution not showing how I want


pygame.init()
WIDTH, HEIGHT = 600, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Sudoku by MrJoeKr')
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (243, 117, 13)
GREY = (161, 161, 161)
GREEN = (31, 213, 8)
RED = (230, 11, 11)
BLUE = (29, 167,236)

# Time for visualization
SLEEP_TIME = 0.09

FONT = pygame.font.SysFont('Arial', 30)

# Images
CROSS = os.path.join("imgs", "cross.jpg")
CHECK = os.path.join("imgs", "check.jpg")
ICON = pygame.image.load(os.path.join('imgs', 'icon.png'))
pygame.display.set_icon(ICON)

FPS = 60


def draw_image(img, x, y, scale):
	own = pygame.image.load(img)
	own = pygame.transform.scale(own, (scale, scale))
	WIN.blit(own, (x, y))


def draw_crosses(wrong_ans):
	for i in range(wrong_ans):
		draw_image(CROSS, WIDTH - 70, 0 + i*HEIGHT // 4.5 + 50, 70)


def draw_check():
	start_time = time.time()
	elapsed = 0
	while elapsed < 3:
		elapsed = time.time() - start_time
		draw_image(CHECK, 0, 110, 70)


def get_font(fontname, size):
	return pygame.font.SysFont(fontname, size)


def draw_window():
	WIN.fill(WHITE)


def draw_text(text, font, color, surface, x, y):
	textobj = font.render(text, 1, color)
	textrect = textobj.get_rect()
	textrect.topleft = (x, y)
	surface.blit(textobj, textrect)


def draw_rect(x,y,w,h,color=BLACK):
	rect = pygame.Rect(x,y,w,h)
	pygame.draw.rect(WIN, color, rect)
	# return pygame.draw.rect(WIN, color, rect)


def is_user_done(grid):
	for row in grid:
		for cell in row:
			if cell.correct_value == 0:
				return False
	return True

# -----------------------------------------
# BACKTRACK ALGORITHM
# -----------------------------------------
# returning array of nums in box
def get_box(grid, x, y):
	box_x = x//3
	box_y = y//3
	start_x = box_x * 3
	end_x = start_x + 3
	start_y = box_y * 3
	end_y = start_y + 3
	l = []
	for i in range(start_y, end_y):
		for j in range(start_x, end_x):
				l.append(grid[i][j])
	return l


# Returning boolean value
def check_box(grid, x, y, n):
	arr = get_box(grid, x, y)
	return n in arr


# check row
def check_row(grid, y, n):
	# n -> the number we are checking
	x = 0
	con = False
	while x < len(grid[0]):
		# our grid here has been changed so we have to put another position
		if grid[y][x] == n:
			con = True
			break
		x += 1

	return con


# check column
def check_col(grid, x, n):
	# n -> the number we are checking
	y = 0
	con = False
	while y < len(grid):
		if grid[y][x] == n:
			con = True
			break
		y += 1
	
	return con



def is_valid(grid, x, y, n):
	if (not check_col(grid, x, n) and 
		not check_box(grid, x, y, n) and 
		not check_row(grid, y, n)):
		return True

	return False
	

def is_clue(grid, x, y):
	return grid[y][x] != 0


def solve_sudoku(grid):
	if find_solution(grid, 0, 0):
		# print_solution(grid)
		return grid

	return False


def find_solution(grid, x, y):

	# Go one row down if x is out of bounds
	if x == len(grid[0]):
		x = 0
		y += 1

	# Terminal case
	if x == 0 and y == len(grid):
		return True

	# Go to next number if it's clue
	if is_clue(grid, x, y):
		if find_solution(grid, x+1, y):
			return True
		return False

	for n in range(1,10):
		if is_valid(grid, x, y, n):
			grid[y][x] = n
			if find_solution(grid, x+1, y):
				return True

			# if it wasn't the right number
			grid[y][x] = 0

	return False

# -----------------------------------------
# VISUALIZATION OF ALGORITHM
# -----------------------------------------


def is_clue_visualize(grid, x, y):
	return grid[y][x].clue


def fill_cells_main(grid):
	for row in grid:
		for cell in row:
			if cell.green:
				cell.fill_green()
			if cell.red and not cell.correct:
				cell.fill_red()
			if cell.blue and cell.visualize:
				cell.fill_blue()


def solve_sudoku_visualize(grid):
	if find_solution_visualize(grid, 0, 0):
		return True

	return False


def cell_not_correct(grid, x, y):
	grid[y][x].showing_value = 0
	grid[y][x].try_value = 0
	grid[y][x].correct = False
	grid[y][x].red = True
	grid[y][x].green = False


def find_solution_visualize(grid, x, y):
	# Go one row down if x is out of bounds

	if x == len(grid[0]):
		x = 0
		y += 1

	# print(x, y, len(grid))

	# Terminal case
	if x == 0 and y == len(grid):
		# print('done')
		return True

	# Go to next number if it's clue
	if is_clue_visualize(grid, x, y):
		# Fill blue if it's a clue
		grid[y][x].blue = True
		grid[y][x].visualize = True
		time.sleep(SLEEP_TIME)
		if find_solution_visualize(grid, x+1, y):
			return True
		return False

	for n in range(1, 10):
		grid[y][x].visualize = True
		grid[y][x].green = True
		grid[y][x].showing_value = n
		time.sleep(SLEEP_TIME)
		if is_valid(grid, x, y, n):
			grid[y][x].try_value = n
			grid[y][x].correct = True

			if find_solution_visualize(grid, x+1, y):
				return True

			# if it wasn't the right number
			time.sleep(SLEEP_TIME)
			cell_not_correct(grid, x, y)

	# Write this function again for the very last
	# cell it tested on
	time.sleep(SLEEP_TIME)
	cell_not_correct(grid, x, y)
	
	return False


def is_grid_full(grid):
	for row in grid:
		if 0 in row:
			return False
	return True


# -----------------------------------------
# SUDOKU GENERATING PART
# -----------------------------------------
def fill_grid(grid, x, y):

	# Good solution

	# Go one row down if x is out of bounds
	if x == len(grid[0]):
		x = 0
		y += 1

	# Terminal case
	if x == 0 and y == len(grid):
		return True

	tries = [i for i in range(1, 10)]
	random.shuffle(tries)
	for n in tries:
		if is_valid(grid, x, y, n):
			grid[y][x] = n
			if fill_grid(grid, x+1, y):
				return True

			# if it wasn't the right number
			grid[y][x] = 0

	return False


def remove_from_grid(grid, clues_num):
	positions = [(x, y) for x in range(9) for y in range(9)]
	i = 0
	zeros_num = 9*9 - clues_num
	checked_positions = []
	while i < zeros_num:
		x, y = random.choice(positions)
		grid[y][x] = 0

		if solve_sudoku(grid):
			positions.remove((x, y))
			checked_positions.append((x, y))

			# Get all the postitions back to the grid
			for x1, y1 in checked_positions:
				grid[y1][x1] = 0

			i += 1


	return grid


def generate_sudoku(clues_num):
	# Initialize grid
	grid = [[0 for i in range(9)] for i in range(9)]
	done = fill_grid(grid, 0, 0)
	grid = remove_from_grid(grid, clues_num)
	return grid


class Cell:
	def __init__(self):
		self.w = 45
		self.x = None
		self.y = None
		self.highlighted = False
		# The number which will be in grey color and not submitted
		self.pencil_value = 0
		# The number which will be written to the cell
		self.real_value = 0
		# Value which user put and it's correct
		self.correct_value = 0
		# If user presses ENTER
		self.submitted = False
		# If user's submit is correct
		self.correct = False
		#
		self.clue = False
		# For visualization algorithm
		self.recorrected = False
		self.visited = False
		self.red = False
		self.green = False
		self.blue = False
		self.visualize = False
		self.showing_value = 0
		self.try_value = 0

	def __eq__(self, other):
		if isinstance(other, int):
			return self.try_value == other
		return None

	def draw(self):
		cell = pygame.Rect(self.x,self.y,self.w,self.w)
		pygame.draw.rect(WIN, WHITE, cell)

	def is_correct(self):
		print(self.pencil_value, self.real_value)
		if self.pencil_value == self.real_value:
			self.correct = True
		return self.pencil_value == self.real_value

	def highlight(self):
		outline = pygame.Rect(self.x,self.y,self.w,self.w)
		s = 4
		cell = pygame.Rect(self.x+s//2,self.y+s//2,self.w-s,self.w-s)
		pygame.draw.rect(WIN, ORANGE, outline)
		pygame.draw.rect(WIN, WHITE, cell)
		self.highlighted = True
		return self.highlighted

	def is_hightlighted(self):
		return self.highlighted

	def not_highlighted(self):
		self.highlighted = False
		return self.highlighted

	def get_rect(self):
		return pygame.Rect(self.x,self.y,self.w,self.w)

	def get_width(self):
		return self.w

	def put_pencil_value(self, number):
		self.pencil_value = number
		return self.pencil_value

	def fill_green(self):
		if self.green:
			cell = pygame.Rect(self.x, self.y, self.w, self.w)
			pygame.draw.rect(WIN, GREEN, cell)

	def fill_red(self):
		if self.red:
			cell = pygame.Rect(self.x, self.y, self.w, self.w)
			pygame.draw.rect(WIN, RED, cell)

	def fill_blue(self):
		if self.blue:
			cell = pygame.Rect(self.x, self.y, self.w, self.w)
			pygame.draw.rect(WIN, BLUE, cell)




def create_grid():
	l = []
	for i in range(9):
		sub_l = []
		for j in range(9):
			cell = Cell()
			sub_l.append(cell)
		l.append(sub_l)
	return l


def draw_values(grid):
	# gets the grid with cells and draws a number if it's not zero
	for row in grid:
		for cell in row:
			if cell.pencil_value != 0 and not cell.correct:
				draw_text(str(cell.pencil_value), get_font('Arial', 30), GREY, 
					WIN, cell.x + cell.w - 20, cell.y - 5)

			elif cell.clue:
				draw_text(str(cell.real_value), get_font('Arial', 40), BLACK, 
					WIN, cell.x + cell.w//2 - 10, cell.y - 3)

			elif cell.correct:
				draw_text(str(cell.real_value), get_font('Arial', 40), BLACK, 
					WIN, cell.x + cell.w//2 - 10, cell.y - 3)

			elif not cell.correct and cell.red:
				draw_text(str(cell.showing_value), get_font('Arial', 40), BLACK, 
					WIN, cell.x + cell.w//2 - 10, cell.y - 3)

			elif cell.visualize:
				draw_text(str(cell.showing_value), get_font('Arial', 40), BLACK, 
					WIN, cell.x + cell.w//2 - 10, cell.y - 3)

	return


def remove_pencil_value(grid):
	for row in grid:
		for cell in row:
			if cell.highlighted:
				cell.pencil_value = 0


def draw_grid(grid, start_x, start_y):
	space = 2
	# drawing the background
	draw_rect(start_x-6,start_y-6,441,HEIGHT-58)
	y = start_y
	x = start_x
	for row_pos, row in enumerate(grid):
		for pos, cell in enumerate(row):
			cell.x = x
			cell.y = y
			cell.draw()
			if pos % 3 == 2:
				# print(pos)
				space = 6
			else:
				space = 2
			x += cell.get_width() + space

		if row_pos % 3 == 2:
			space = 6
		else:
			space = 2
		y += cell.get_width() + space
		x = start_x


def make_tuple(arr):
	if not isinstance(arr[0], int):
		for i, row in enumerate(arr):
			arr[i] = tuple(row)

		return tuple(arr)


def put_attributes(grid, grid_values, grid_solution):
	for y, row in enumerate(grid_solution):
		for x, num in enumerate(row):
			if grid_values[y][x] != 0:
				grid[y][x].clue = True

			grid[y][x].real_value = num

			if grid[y][x].clue:
				grid[y][x].correct_value = grid[y][x].real_value


	return grid


def main(clues_num):
	clock = pygame.time.Clock()
	running = True
	# Creates cells with no 0 values
	grid = create_grid()
	# Values which are in the start
	grid_values = generate_sudoku(clues_num)
	# The solution to the grid
	grid_solution = list(grid_values)
	grid_values = make_tuple(grid_values)
	solve_sudoku(grid_solution)
	grid = put_attributes(grid, grid_values, grid_solution)

	start_time = time.time()
	elapsed = 0
	click = False
	clicks = []
	key_nums = [f'K_{i}' for i in range(1, 10)]
	clicked_key = False

	pencil_value_input = 0
	wrong_ans = 0
	submitted = False

	# For visualization of Algorithm
	get_solution = False
	started_visualize = False
	done_filling = False

	space_pressed = True
	space_count = 0

	user_lost = False
	user_win = False

	while running:

		draw_window()
		mx, my = pygame.mouse.get_pos()

		# Recreating grid for BackTrack Algorithm

		# Draw grid, cells also get their x and y
		draw_grid(grid, 90, 10)

		# Counting time
		if not user_lost and not user_win and not done_filling:
			elapsed = time.time() - start_time
			draw_text(f'Time: {math.floor(elapsed)}', FONT, BLUE, WIN, 5, HEIGHT-45)

		# Managing text in the bottom of the window
		if not user_lost and not user_win and not done_filling:
			if space_count == 0:
				s = 'Stuck? Press SPACE for solution'
				draw_text(s, FONT, BLACK, WIN, WIDTH//5, HEIGHT-45)
			elif space_count == 1:
				s = 'Do you really want to get the solution?'
				draw_text(s, FONT, BLACK, WIN, WIDTH-len(s)*11-1, HEIGHT-45)
			else:
				s = 'Now, watch the beauty of this algorithm!'
				draw_text(s, FONT, BLACK, WIN, WIDTH//5-20, HEIGHT-45)
		elif user_win:
			s = f'You won in time {round(elapsed, 1)}! Get yourself a cake or try again! (SPACE)'
			draw_text(s, get_font('Arial', 25), GREEN, WIN, 10, HEIGHT-45)
		elif done_filling:
			s = f'Well, the algorithm did it by itself. Want to try by yourself? (SPACE)'
			draw_text(s, get_font('Arial', 24), BLUE, WIN, 10, HEIGHT-45)
		else:
			s = 'You Lost. But you can try again! (SPACE)'
			draw_text(s, FONT, RED, WIN, WIDTH-len(s)*11-83, HEIGHT-45)

		# Solve using Algorithm with visualization
		if get_solution:
			# Put the values which are shown on the screen to try_values
			grid_solution = []
			for row in grid:
				for cell in row:
					if cell.clue:
						cell.try_value = cell.real_value

			thread_solution = threading.Thread(target=solve_sudoku_visualize, args=(grid,))
			thread_solution.start()
			started_visualize = True
			get_solution = False

		# Fill colors of cells which are being worked on
		if started_visualize:
			fill_cells_main(grid)
			draw_values(grid)
			# Check if grid is full to write a bottom text
			done_filling = is_grid_full(grid)

		# Highlighting Cells
		if click and not started_visualize:
			for row in grid:
				for cell in row:
					for c in clicks:
						# Can't highlight if it's clue
						if cell.get_rect().collidepoint(c) and not cell.clue:
							cell.highlight()
						else:
							cell.not_highlighted()


		# clear clicks after finding highlight
		clicks = []
		if not started_visualize:
			for row in grid:
				for cell in row:
					# If the cell is highlighted
					if cell.is_hightlighted():
						cell.highlight()

						# Put the pencil value into the cell
						if pencil_value_input != 0:
							cell.pencil_value = pencil_value_input
							# print(cell, cell.pencil_value)

						# If value is submitted
						if submitted and cell.is_correct():
							cell.correct_value = cell.pencil_value
							cell.clue = True
							drawing_check = threading.Thread(target=draw_check)
							drawing_check.start()

						# If user presses enter and not correct
						elif (submitted and 
							not cell.correct and 
							cell.pencil_value != 0 and
							wrong_ans < 3):
							wrong_ans += 1
							print(wrong_ans)


		# If users input is wrong
		draw_crosses(wrong_ans)

		if wrong_ans == 3:
			user_lost = True

		# Put pencil values, clues and correct values into highlighted cell
		# when user didn't ask for solution
		if not started_visualize:
			draw_values(grid)

		# Checks if user's done
		if not started_visualize:
			user_win = is_user_done(grid)


		clock.tick(FPS)

		# Values which are reset each cycle
		click = False
		clicked_key = False
		pencil_value_input = 0
		submitted = False

		for event in pygame.event.get():
			if event.type == QUIT:
				running = False

			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					running = False

				if event.key == K_BACKSPACE:
					remove_pencil_value(grid)

				if event.key == K_RETURN:
					submitted = True

				if event.key == K_SPACE:

					# Only one time event
					if space_pressed:
						space_count += 1
						if space_count == 2:
							get_solution = True
							space_pressed = False

				for KEY in key_nums:
					KEY = getattr(pygame, KEY)
					if event.key == KEY:
						clicked_key = True
						pencil_value_input = KEY - 48 #It's K + 48 for some reason
						# print(pencil_value_input)

				if user_win or user_lost or done_filling:
						# RESETTING ALL VARIABLES
						grid = create_grid()
						# Values which are in the start
						grid_values = generate_sudoku(clues_num)
						# The solution to the grid
						grid_solution = list(grid_values)
						grid_values = make_tuple(grid_values)
						solve_sudoku(grid_solution)
						grid = put_attributes(grid, grid_values, grid_solution)

						start_time = time.time()
						elapsed = 0
						click = False
						clicks = []
						key_nums = [f'K_{i}' for i in range(1, 10)]
						clicked_key = False

						pencil_value_input = 0
						wrong_ans = 0
						submitted = False

						# For visualization of Algorithm
						get_solution = False
						started_visualize = False
						done_filling = False

						space_pressed = True
						space_count = 0

						user_lost = False
						user_win = False


			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					click = True
					clicks.append((mx, my))

		pygame.display.update()


	pygame.quit()


if __name__ == '__main__':
	# clues_num = int(input("Number of clues:\n"))
	while True:
		print("Choose difficulty:")
		print("Type number:")
		print("Easy(1) - Medium(2) - Hard(3) - Very Hard(4)")
		clues_num = input()
		if clues_num == '1':
			clues_num = random.randint(60, 70)
		elif clues_num == '2':
			clues_num = random.randint(45,59)
		elif clues_num == '3':
			clues_num = random.randint(30,40)
		elif clues_num == '4':
			clues_num = random.randint(17,23)
		else:
			print("Choose from 1-4, please.")
			continue
		break
	# clues_num = 40
	main(clues_num)
	