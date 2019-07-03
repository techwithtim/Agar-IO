import socket
from _thread import *
import _pickle as pickle
import time
import random
import math

S = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
S.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

SERVER = "10.50.160.213"
PORT = 5555

BALL_RADIUS = 5
START_RADIUS = 7

W, H = 1000, 700

SERVER_IP = socket.gethostbyname(SERVER)

try:
    S.bind((SERVER, PORT))

except socket.error as e:
    print(str(e))

S.listen(2)
print("Server Started, Waiting for a connection...")

players = {}
balls = []
connections = 0
_id = 0
colors = [(255,0,0), (255, 128, 0), (255,255,0), (128,255,0),(0,255,0),(0,255,128),(0,255,255),(0, 128, 255), (0,0,255), (0,0,255), (128,0,255),(255,0,255), (255,0,128),(128,128,128), (0,0,0)]
start = False
stat_time = 0
game_time = "Starting Soon"

def check_collision():
	global players, balls
	"""
	checks if any of the player have collided with any of the balls
	:param players: a dictonary of players
	:param balls: a list of balls
	:return: None
	"""
	to_delete = []
	for player in players:
		p = players[player]
		x = p["x"]
		y = p["y"]
		for ball in balls:
			bx = ball[0]
			by = ball[1]

			dis = math.sqrt((x - bx)**2 + (y-by)**2)
			if dis <= START_RADIUS + p["score"]:
				p["score"] = p["score"] + 1
				balls.remove(ball)


def create_balls(balls, n):
	for i in range(n):
		while True:
			stop = True
			x = random.randrange(0,W)
			y = random.randrange(0,H)
			for player in players:
				p = players[player]
				dis = math.sqrt((x - p["x"])**2 + (y-p["y"])**2)
				if dis <= START_RADIUS + p["score"]:
					stop = False
			if stop:
				break

		balls.append((x,y, random.choice(colors)))

def get_start_location(players):
	while True:
		stop = True
		x = random.randrange(0,W)
		y = random.randrange(0,H)
		for player in players:
			p = players[player]
			dis = math.sqrt((x - p["x"])**2 + (y-p["y"])**2)
			if dis <= START_RADIUS + p["score"]:
				stop = False
				break
		if stop:
			break
	return (x,y)

def threaded_client(conn):
	global _id, connections, players, balls, game_time

	current_id = _id

	# recieve a name from the client
	data = conn.recv(16)
	name = data.decode("utf-8")
	print("[LOG]", name, "connected to the server.")

	# Setup properties for each new player
	color = colors[current_id]
	x, y = get_start_location(players)
	players[current_id] = {"x":x, "y":y,"color":color,"score":0,"name":name}  # x, y color, score, name
	_id += 1

	# pickle data and send initial info to clients
	conn.send(str.encode(str(current_id)))

	# server will recieve basic commands from client
	# it will send back all of the other clients info
	'''
	commands start with:
	move
	jump
	get
	id - returns id of client
	'''
	while True:
		if start:
			game_time = time.time()-start_time()
		try:
			# Recieve data from client
			data = conn.recv(32)

			if not data:
				break

			data = data.decode("utf-8")
			#print("[DATA] Recieved", data, "from client id:", current_id)

			# look for specific commands from recieved data
			if data.split(" ")[0] == "move":
				split_data = data.split(" ")
				x = int(split_data[1])
				y = int(split_data[2])
				players[current_id]["x"] = x
				players[current_id]["y"] = y
				send_data = pickle.dumps((balls,players, game_time))
				if start:
					check_collision()
				if len(balls) < 50:
					create_balls(balls, 100)

			elif data.split(" ")[0] == "id":
				send_data = str.encode(str(current_id))

			elif data.split(" ")[0] == "jump":
				send_data = pickle.dumps((balls,players, game_time))
			else:
				# any other command just send back list of players
				send_data = pickle.dumps((balls,players, game_time))

			# send data back to clients
			conn.send(send_data)

		except Exception as e:
			print(e)
			break

	# When user disconnects	
	print("[DISCONNECT] Client Id:", current_id, "disconnected")
	connections -= 1 
	del players[current_id]
	conn.close()

# MAINLOOP
# keeps looking to accept new connections
create_balls(balls, 150)
while True:
	if not(start):
		host, addr = S.accept()
		connections += 1
		if connections > 2:
			start = True
			start_time = time.time()
		print("[CONNECTION] Connected to:", addr)
		start_new_thread(threaded_client,(host,))
