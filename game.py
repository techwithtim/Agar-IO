# small network game that has differnt blobs
# moving around the screen

import contextlib
with contextlib.redirect_stdout(None):
    import pygame
from client import Network
import random
import os
pygame.font.init()

# Constants
PLAYER_RADIUS = 10
START_VEL = 9
BALL_RADIUS = 5

W, H = 1600, 830

NAME_FONT = pygame.font.SysFont("comicsans", 20)
TIME_FONT = pygame.font.SysFont("comicsans", 30)
SCORE_FONT = pygame.font.SysFont("comicsans", 26)

COLORS = [(255,0,0), (255, 128, 0), (255,255,0), (128,255,0),(0,255,0),(0,255,128),(0,255,255),(0, 128, 255), (0,0,255), (0,0,255), (128,0,255),(255,0,255), (255,0,128),(128,128,128), (0,0,0)]

# Dynamic Variables
players = {}
balls = []

# FUNCTIONS
def convert_time(t):
	"""
	converts a time given in seconds to a time in
	minutes

	:param t: int
	:return: string
	"""
	if type(t) == str:
		return t

	if int(t) < 60:
		return str(t) + "s"
	else:
		minutes = str(t // 60)
		seconds = str(t % 60)

		if int(seconds) < 10:
			seconds = "0" + seconds

		return minutes + ":" + seconds


def redraw_window(players, balls, game_time, score):
	"""
	draws each frame
	:return: None
	"""
	WIN.fill((255,255,255)) # fill screen white, to clear old frames
	
		# draw all the orbs/balls
	for ball in balls:
		pygame.draw.circle(WIN, ball[2], (ball[0], ball[1]), BALL_RADIUS)

	# draw each player in the list
	for player in sorted(players, key=lambda x: players[x]["score"]):
		p = players[player]
		pygame.draw.circle(WIN, p["color"], (p["x"], p["y"]), PLAYER_RADIUS + round(p["score"]))
		# render and draw name for each player
		text = NAME_FONT.render(p["name"], 1, (0,0,0))
		WIN.blit(text, (p["x"] - text.get_width()/2, p["y"] - text.get_height()/2))

	# draw scoreboard
	sort_players = list(reversed(sorted(players, key=lambda x: players[x]["score"])))
	title = TIME_FONT.render("Scoreboard", 1, (0,0,0))
	start_y = 25
	x = W - title.get_width() - 10
	WIN.blit(title, (x, 5))

	ran = min(len(players), 3)
	for count, i in enumerate(sort_players[:ran]):
		text = SCORE_FONT.render(str(count+1) + ". " + str(players[i]["name"]), 1, (0,0,0))
		WIN.blit(text, (x, start_y + count * 20))

	# draw time
	text = TIME_FONT.render("Time: " + convert_time(game_time), 1, (0,0,0))
	WIN.blit(text,(10,10))
	# draw score
	text = TIME_FONT.render("Score: " + str(round(score)),1,(0,0,0))
	WIN.blit(text,(10,15 + text.get_height()))


def main(name):
	"""
	function for running the game,
	includes the main loop of the game

	:param players: a list of dicts represting a player
	:return: None
	"""
	global players

	# start by connecting to the network
	server = Network()
	current_id = server.connect(name)
	balls, players, game_time = server.send("get")

	# setup the clock, limit to 30fps
	clock = pygame.time.Clock()

	run = True
	while run:
		clock.tick(30) # 30 fps max
		player = players[current_id]
		vel = START_VEL - round(player["score"]/14)
		if vel <= 1:
			vel = 1

		# get key presses
		keys = pygame.key.get_pressed()

		data = ""
		# movement based on key presses
		if keys[pygame.K_LEFT] or keys[pygame.K_a]:
			if player["x"] - vel - PLAYER_RADIUS - player["score"] >= 0:
				player["x"] = player["x"] - vel

		if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
			if player["x"] + vel + PLAYER_RADIUS + player["score"] <= W:
				player["x"] = player["x"] + vel

		if keys[pygame.K_UP] or keys[pygame.K_w]:
			if player["y"] - vel - PLAYER_RADIUS - player["score"] >= 0:
				player["y"] = player["y"] - vel

		if keys[pygame.K_DOWN] or keys[pygame.K_s]:
			if player["y"] + vel + PLAYER_RADIUS + player["score"] <= H:
				player["y"] = player["y"] + vel

		data = "move " + str(player["x"]) + " " + str(player["y"])

		# send data to server and recieve back all players information
		balls, players, game_time = server.send(data)

		for event in pygame.event.get():
			# if user hits red x button close window
			if event.type == pygame.QUIT:
				run = False

			if event.type == pygame.KEYDOWN:
				# if user hits a escape key close program
				if event.key == pygame.K_ESCAPE:
					run = False


		# redraw window then update the frame
		redraw_window(players, balls, game_time, player["score"])
		pygame.display.update()


	server.disconnect()
	pygame.quit()
	quit()


# get users name
while True:
 	name = input("Please enter your name: ")
 	if  0 < len(name) < 20:
 		break
 	else:
 		print("Error, this name is not allowed (must be between 1 and 19 characters [inclusive])")

# make window start in top left hand corner
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,30)

# setup pygame window
WIN = pygame.display.set_mode((W,H))
pygame.display.set_caption("Blobs")

# start game
main(name)