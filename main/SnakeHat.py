# Joona Niemenmaa 14/1/2024 SnakeHat.py
import sys
try:
	from sense_hat import SenseHat 
	import numpy as np
	import time as tm
except OSError:
	print("Tarvittavia kirjastoja ei löydy, lopetetaan.")
	sys.exit(0)

RIVEJA = 8
SARAKKEITA = 8

UPDATE_SPEED = 1

UP = "up"
DOWN = "down"
RIGHT = "right"
LEFT = "left"

clear = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

class POSITION():
	x = 0
	y = 0
class PLAYER():
	position = POSITION()
	direction = UP 

Sense = SenseHat()

def updateLED(LED_Matrix):
	LED_Array = []
	for i in range(RIVEJA):
		for j in range(SARAKKEITA):
			if (LED_Matrix[i][j] == 0):
				LED_Array.append(clear)
			if (LED_Matrix[i][j] == 1):
				LED_Array.append(blue)
	Sense.set_pixels(LED_Array)
	return None

def clearLED():
	LED_Array = []
	for i in range(RIVEJA):
		for j in range(SARAKKEITA):
			LED_Array.append(clear)
	Sense.set_pixels(LED_Array)
	return None

def updatePosition(player):
	if (player.direction == UP):
		if (player.position.y == 0):
			player.position.y = RIVEJA - 1
		else:
			player.position.y = player.position.y - 1
	elif (player.direction == DOWN):
		if (player.position.y == RIVEJA - 1):
			player.position.y = 0
		else:
			player.position.y = player.position.y + 1
	elif (player.direction == RIGHT):
		if (player.position.x == SARAKKEITA - 1):
			player.position.x = 0
		else:
			player.position.x = player.position.x + 1
	elif (player.direction == LEFT):
		if (player.position.x == 0):
			player.position.x = SARAKKEITA - 1
		else:
			player.position.x = player.position.x - 1
	return player 

def updateDirection(player, event):
	if (player.direction != event.direction):
		if ((player.direction == UP or player.direction == DOWN) and (event.direction == LEFT or event.direction == RIGHT)):
			player.direction = event.direction
		elif ((player.direction == LEFT or player.direction == RIGHT) and (event.direction == DOWN or event.direction == UP)):
			player.direction = event.direction
	return player 

def paaohjelma():
	player = PLAYER()
	event = Sense.stick.wait_for_event()
	while (event.direction != "middle"):
		player = updateDirection(player, event)
		player = updatePosition(player)
		LED_Matrix = np.zeros((RIVEJA, SARAKKEITA), int)
		LED_Matrix[player.position.y][player.position.x] = 1
		updateLED(LED_Matrix)
		tm.sleep(1)
		eventList = Sense.stick.get_events()
		if (len(eventList) > 0):
			event = eventList[0]
	clearLED()
	print("Kiitos ohjelman käytöstä.")
	return None
paaohjelma()
# EOF

