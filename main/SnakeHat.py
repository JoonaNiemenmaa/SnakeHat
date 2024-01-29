# Joona Niemenmaa 14/1/2024 SnakeHat.py
import sys
try:
	from sense_hat import SenseHat 
	import numpy as np
	import time as tm
	import random as rd
except OSError:
	print("Required libraries not found, exiting program.")
	sys.exit(0)

ROWS = 8
COLUMNS = 8

UPDATE_SPEED = 1

START_SIZE = 3 

UP = "up"
DOWN = "down"
RIGHT = "right"
LEFT = "left"
MIDDLE = "middle"

clear = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

class SNAKE_PART():
	direction = UP
	x = 0
	y = 0

class SCORE_POINT():
	picked_up = False # Set to true when the snake eats the score point
	x = 0
	y = 0

Sense = SenseHat()

def updateLED(LED_Matrix):
	LED_Array = []
	for i in range(ROWS):
		for j in range(COLUMNS):
			if (LED_Matrix[i][j] == 0):
				LED_Array.append(clear)
			if (LED_Matrix[i][j] == 1):
				LED_Array.append(green)
			if (LED_Matrix[i][j] == 2):
				LED_Array.append(blue)
	Sense.set_pixels(LED_Array)
	return None

def clearLED():
	LED_Array = []
	for i in range(ROWS):
		for j in range(COLUMNS):
			LED_Array.append(clear)
	Sense.set_pixels(LED_Array)
	return None

def updatePosition(snake_part):
	if (snake_part.direction == UP):
		if (snake_part.y == 0):
			snake_part.y = ROWS - 1
		else:
			snake_part.y = snake_part.y - 1
	elif (snake_part.direction == DOWN):
		if (snake_part.y == ROWS - 1):
			snake_part.y = 0
		else:
			snake_part.y = snake_part.y + 1
	elif (snake_part.direction == RIGHT):
		if (snake_part.x == COLUMNS - 1):
			snake_part.x = 0
		else:
			snake_part.x = snake_part.x + 1
	elif (snake_part.direction == LEFT):
		if (snake_part.x == 0):
			snake_part.x = COLUMNS - 1
		else:
			snake_part.x = snake_part.x - 1
	return snake_part 

def updateDirection(player, snake_parts, event):
	snake_parts[0].direction = player.direction
	for i in range(len(snake_parts) - 1):
		if (snake_parts[i + 1].y == 0 and snake_parts[i].y == ROWS - 1):
			snake_parts[i + 1].direction = UP
		elif (snake_parts[i + 1].y == ROWS - 1 and snake_parts[i].y == 0):
			snake_parts[i + 1].direction = DOWN
		elif (snake_parts[i + 1].x == 0 and snake_parts[i].x == COLUMNS - 1):
			snake_parts[i + 1].direction = LEFT
		elif (snake_parts[i + 1].x == COLUMNS - 1 and snake_parts[i].x == 0):
			snake_parts[i + 1].direction = RIGHT
		elif (snake_parts[i + 1].y > snake_parts[i].y):
			snake_parts[i + 1].direction = UP 
		elif (snake_parts[i + 1].y < snake_parts[i].y):
			snake_parts[i + 1].direction = DOWN
		elif (snake_parts[i + 1].x > snake_parts[i].x):
			snake_parts[i + 1].direction = LEFT 
		elif (snake_parts[i + 1].x < snake_parts[i].x):
			snake_parts[i + 1].direction = RIGHT
	if (player.direction != event.direction):
		if ((player.direction == UP or player.direction == DOWN) and (event.direction == LEFT or event.direction == RIGHT)):
			player.direction = event.direction
		elif ((player.direction == LEFT or player.direction == RIGHT) and (event.direction == DOWN or event.direction == UP)):
			player.direction = event.direction
	return player

def createScorePoint(player, snake_parts):
	accept = False
	score_point = SCORE_POINT()
	while (accept == False):
		score_point.x = rd.randrange(COLUMNS)
		score_point.y = rd.randrange(ROWS)
		print(score_point.x, score_point.y)
		if (player.x == score_point.x and player.y == score_point.y):
			continue
		for i in snake_parts:
			if (i.x == score_point.x and i.y == score_point.y):
				continue
		accept = True
	return score_point

def lengthenSnake(player, snake_parts):
	if (len(snake_parts) > 0):
		previous_part = snake_parts[len(snake_parts) - 1]
	else:
		previous_part = player
	snake_part = SNAKE_PART()
	snake_part.x = previous_part.x
	snake_part.y = previous_part.y
	if (previous_part.direction == UP):
		snake_part.y = snake_part.y + 1
	elif (previous_part.direction == DOWN):
		snake_part.y = snake_part.y - 1
	elif (previous_part.direction == RIGHT):
		snake_part.x = snake_part.x - 1
	elif (previous_part.direction == LEFT):
		snake_part.x = snake_part.x + 1
	if (snake_part.x == -1):
		snake_part.x = COLUMNS - 1
	elif (snake_part.x == COLUMNS):
		snake_part.x = 0
	elif (snake_part.y == -1):
		snake_part.y = ROWS - 1
	elif (snake_part.y == ROWS):
		snake_part.y = 0
	snake_parts.append(snake_part)
	return snake_parts

def main():
	# Initialize variables and stuff
	clearLED()
	score = 0
	score_point = SCORE_POINT()
	death = False
	player = SNAKE_PART()
	event = Sense.stick.wait_for_event()
	player.direction = event.direction
	# These two set the players starting position
	player.x = 4
	player.y = 4
	snake_parts = []
	for i in range(START_SIZE - 1):
		snake_parts = lengthenSnake(player, snake_parts)
	# The main game update loop is here
	while (event.direction != MIDDLE and death == False):
		start_time = round(tm.time(), 2)
		if (player.x == score_point.x and player.y == score_point.y):
			snake_parts = lengthenSnake(player, snake_parts)
			score_point = createScorePoint(player, snake_parts)
			score = score + 1
		player = updateDirection(player, snake_parts, event)
		player = updatePosition(player)
		for i in range(len(snake_parts)):
			snake_parts[i] = updatePosition(snake_parts[i])
		LED_Matrix = np.zeros((ROWS, COLUMNS), int)
		LED_Matrix[score_point.y][score_point.x] = 2
		LED_Matrix[player.y][player.x] = 1
		for i in range(len(snake_parts)):
			LED_Matrix[snake_parts[i].y][snake_parts[i].x] = 1
		updateLED(LED_Matrix)
		for i in range(len(snake_parts)):
			if (snake_parts[i].x == player.x and snake_parts[i].y == player.y):
				death = True
		if (death == True):
			break
		execution_time = round(tm.time() - start_time, 2)
		tm.sleep(1 - execution_time)
		eventList = Sense.stick.get_events()
		if (len(eventList) > 0):
			event = eventList[0]
	clearLED()
	printout = "You lost! Your score: {0}".format(score)
	Sense.show_message(printout)
	print(printout)
	print("Thank you for using the program.")
	return None
main()
# EOF

