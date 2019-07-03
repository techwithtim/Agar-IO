# small network game that has differnt blobs
# moving around the screen

import pygame
from client import Network
import random
pygame.font.init()

# Constants
PLAYER_RADIUS = 10
START_VEL = 7
BALL_RADIUS = 5

W, H = 1000, 700

NAME_FONT = pygame.font.SysFont("comicsans", 20)
TIME_FONT = pygame.font.SysFont("comicsans", 30)

COLORS = [(255,0,0), (255, 128, 0), (255,255,0), (128,255,0),(0,255,0),(0,255,128),(0,255,255),(0, 128, 255), (0,0,255), (0,0,255), (128,0,255),(255,0,255), (255,0,128),(128,128,128), (0,0,0)]

# Dynamic Variables
players = {}
balls = []

# FUNCTIONS

def redraw_window(players, balls, game_time):
	"""
	draws each frame
	:return: None
	"""
	WIN.fill((255,255,255)) # fill screen white, to clear old frames
	
		# draw all the orbs/balls
	for ball in balls:
		pygame.draw.circle(WIN, ball[2], (ball[0], ball[1]), BALL_RADIUS)

	# draw each player in the list
	for player in sorted(players):
		p = players[player]
		pygame.draw.circle(WIN, p["color"], (p["x"], p["y"]), PLAYER_RADIUS + p["score"])
		# render and draw name for each player
		text = NAME_FONT.render(p["name"], 1, (0,0,0))
		WIN.blit(text, (p["x"] - text.get_width()/2, p["y"] - text.get_height()/2))

	# draw time
	text = TIME_FONT.render("Time: " + str(game_time), 1, (0,0,0))
	WIN.blit(text,(10,10))


def main(name):
	global players
	"""
	function for running the game,
	includes the main loop of the game

	:param players: a list of dicts represting a player
	:return: None
	"""

	# start by connecting to the network
	server = Network()
	current_id = server.connect(name)
	balls, players, game_time = server.send("get")

	# setup the clock, limit to 30fps
	clock = pygame.time.Clock()

	run = True
	while run:
		player = players[current_id]
		vel = START_VEL - round(player["score"]/10)
		if vel <= 2:
			vel = 2

		clock.tick(30) # 30 fps max

		for event in pygame.event.get():
			# if user hits red x button close window
			if event.type == pygame.QUIT:
				run = False

			if event.type == pygame.KEYDOWN:
				# if user hits a escape key close program
				if event.key == pygame.K_ESCAPE:
					run = False

		# get key presses
		keys = pygame.key.get_pressed()

		data = ""
		# movement based on key presses
		if keys[pygame.K_LEFT]:
			if player["x"] - vel - PLAYER_RADIUS >= 0:
				player["x"] = player["x"] - vel

		if keys[pygame.K_RIGHT]:
			if player["x"] + vel + PLAYER_RADIUS <= W:
				player["x"] = player["x"] + vel

		if keys[pygame.K_UP]:
			if player["y"] - vel - PLAYER_RADIUS >= 0:
				player["y"] = player["y"] - vel

		if keys[pygame.K_DOWN]:
			if player["y"] + vel + PLAYER_RADIUS <= H:
				player["y"] = player["y"] + vel

		data = "move " + str(player["x"]) + " " + str(player["y"])

		# send data to server and recieve back all players information
		balls, players, game_time = server.send(data)

		# redraw window then update the frame
		redraw_window(players, balls, game_time)
		pygame.display.update()


	server.disconnect()
	pygame.quit()
	quit()


name = input("Please enter your name: ")
WIN = pygame.display.set_mode((W,H))
pygame.display.set_caption("Blobs")
main(name)