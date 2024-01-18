# Joona Niemenmaa 14/1/2024 SnakeHat.py
from sense_hat import SenseHat 
import numpy as np
import time as tm

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
	direction = "RIGHT"

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
			player.position.y = player.position.y - 1
		elif (player.direction == DOWN):
			player.position.y = player.position.y + 1
		elif (player.direction == RIGHT):
			player.position.x = player.position.x + 1
		elif (player.direction == LEFT):
			player.position.x = player.position.x - 1
	return player 

def updateDirection():
	pass
	return None

def paaohjelma():
	player = PLAYER()
	event = Sense.stick.wait_for_event()
	while (event.direction != "middle"):
		player.direction = event.direction
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

