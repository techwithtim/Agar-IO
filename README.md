# Agar-IO
A duplication of the game Agar.io written in python

# Running on Local Network
Before you will be able to run this game you must make one minor change the to the file **client.py**. The *host* property from inside the __init__() method must be the local ip address of the machine that is running the server. To find this IP all you need to do is run *server.py* and read the output to see what IP it is on. Simply use that as the host property for the client.py file.

# Playing the Game
To run the game you must have an instance of *server.py* running. You can then connect as many clients as you'd like by running *game.py*.

# Game Mechanics
- Each game lasts 5 minutes
- The larger you are the slower you move
- Each player will lose mass at a rate proportional to their size (larger = faster loss)
- The game will be in "lobby" mode until started, this means all each player can do is move.
- The game will begin once a client connects on the same machine the server is running on

# Possible Erros
If you are having connections issues try diabsling the firewall on the server and client machines. 
