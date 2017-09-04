Paradigms Final Project
=======================

##### By *Chris "Scary" Scaramella* (cscarame) and *Jamie Maher* (jmaher5)

### Game Description

Our game is a two player Tron-style game. When the game begins, you are greeted with a welcome screen that tells you when you are connected to the server. Once connected, you are able to select 'begin'. Once the start button is pressed, each player is prompted to pick a color. There are four colors to choose from, red, yellow, blue, or green. When both players have picked a color, the game begins. There is a small pause before the game starts animating to show each player their starting position. Then the game takes off! Each player uses their keyboard to change the direction of their tron-stream. It is similar to Snake in the way that the players can't run back over their own stream or into the walls. What makes this game more competitive is that you also can't run over your opponet's stream. This means that each player has to strategically find a path that can somehow trap the other player. The first player to run over a stream or hit the wall loses, and the other player wins! After the game is over, the players are prompted to either restart or quit. If they choose to restart, they can repick their colors. If they quit, the game exits gracefully.

### Controls

Use the mouse to click on the buttons, and use the arrow keys to navigate your player. *Secret Controls:* In order to move more quickly, tap the direction you are moving in!  This could help you gain an edge over an opponent!

### How to Run

The server is running currently on ash.  In order for the game to work, the server must be running and the game clients must be configured to the server.  If a computer other than ash.campus.nd.edu is used to run the server, then the tron.py file must be modified.  The URL variable must be changed to match the server name.  If you want to run both games locally, use "localhost"

In one player's window, run

`$ python tron.py`

And in a second window, run

`$ python tron.py`

### System Requirements

Your computer must have Python 2.6 at least and also have the pygame and twisted libraries installed.

