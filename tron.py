#!/usr/bin/env python




import pygame
from pygame.locals import *
import sys
import math

### START client code

from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from twisted.internet.defer import DeferredQueue


URL = "ash.campus.nd.edu"

class ConnectionGroup():
    def __init__(self):
        self.command = None
    	self.data = None
        self.gs = None

class TestConnection(Protocol):
    def __init__(self):
        self.address = "Unknown"
        self.player = 0
        return
    def connectionMade(self):
        print "New Connection Made\n"
        return
    def dataReceived(self,data):
        print data
        if data == "quit":
            reactor.stop()
            quit()
        return
    def connectionLost(self, reason):
        print "Connection Lost\n"
        return
    def addAddress(self, address):
        self.address = address
        return

class CommandConnection(Protocol):
    def __init__(self,group):
        self.player = 0
        self.group = group
    def connectionMade(self):
        print "Command Connection Established"
        self.group.command = self
    def dataReceived(self,data):
        print "Command: " + data
        info = data.split(" ")
        if info[0] == "listen":
            self.player = 1
            reactor.listenTCP(int(info[1]), ClientConnectionFactory("data", self.group))
        elif info[0] == "connect":
            self.player = 2
            reactor.connectTCP(info[2], int(info[1]), ClientConnectionFactory("data", self.group))
        self.transport.write("Player " + str(self.player) + " reporting in!")
    def connectionLost(self, reason):
        print "Command Connection Lost"



class DataConnection(Protocol):
    def __init__(self,group):
        self.group = group
        self.data = None
    def connectionMade(self):
        self.group.data = self
        self.group.command.group = self.group
        self.player = self.group.command.player
        print "Data Connection Established"
        print "I am player " + str(self.player)
        self.group.gs.player = self.player
        self.group.gs.other_player_num = (self.player % 2) + 1 
        self.group.gs.data_conn = self
        try:
        	self.group.gs.main()
        except:
                pass
    def dataReceived(self,data):
        self.data = data
        print data
    def connectionLost(self, reason):
        print "Connection Lost"
    def getData(self):
        return self.data
        
        
class ClientConnectionFactory(ClientFactory):
    def __init__(self, connection_type, group):
        self.connection_type = connection_type
        self.test_conn = TestConnection()
        self.command = CommandConnection(group)
        self.data = DataConnection(group)
        return
    def buildProtocol(self,addr):
        if self.connection_type == "command":
            return self.command
        elif self.connection_type == "data":
            return self.data
        else:
            return self.test_conn


### END client code

class Block:
	def __init__(self, x, y, c):
		self.color = c
		if c == 'r':
			self.image = pygame.image.load("red.png")
		elif c == 'b':
			self.image = pygame.image.load("blue.png")
		elif c == 'y':
			self.image = pygame.image.load("yellow.png")
		elif c == 'g':
			self.image = pygame.image.load("green.png")
		else:
			self.image = pygame.image.load("white.png")

		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

class Player:
	def __init__(self, c):
		self.color = c
		self.dir = 'r'
		if c == 'r':
			self.image = pygame.image.load("red.png")
		elif c == 'b':
			self.image = pygame.image.load("blue.png")
		elif c == 'y':
			self.image = pygame.image.load("yellow.png")
		elif c == 'g':
			self.image = pygame.image.load("green.png")
		else:
			self.image = pygame.image.load("white.png")

		self.rect = self.image.get_rect()
		self.visited = []

	def tick(self):
		if self.dir == 'l':

                        self.rect.x -= 8
		elif self.dir == 'r':
			self.rect.x +=8
		elif self.dir == 'u':
			self.rect.y -= 8
		else:
			self.rect.y +=8


class GameSpace:
	def premain(self):
                pygame.init()
		self.size = self.width, self.height = 800, 800
		self.screen = pygame.display.set_mode(self.size)
		self.color1 = 'r'
		self.color2 = 'b'
                # Display menu screen
		self.menuimage = pygame.image.load("menu_connecting.png")
		self.screen.blit(self.menuimage, self.menuimage.get_rect())
		pygame.display.flip()
		# Wait to display begin button until finished connecting
                self.other_player = None
                self.data_conn = None
		group = ConnectionGroup()
                group.gs = self
		reactor.connectTCP(URL, 40052, ClientConnectionFactory("command", group), 5)
                print "Started listening for a connection\n"
                reactor.run()
                        

                # Finish connecting, and continue with game, now self.player = 1 or 2 and self.data_conn is the connection to the game

	def menu(self):
                self.menuimage2 = pygame.image.load("menu.png")
                self.screen.blit(self.menuimage2, self.menuimage2.get_rect())
                self.button_press_image = pygame.image.load("button_pressed.png")
                self.button_press_image.set_colorkey(self.button_press_image.get_at((0,0)))
                pygame.display.flip()
		# Start click detection
                click = 0
		while 1:
			for event in pygame.event.get():
				if event.type == pygame.QUIT: sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					pos = pygame.mouse.get_pos()
					if (pos[0] > 270 and pos[0] < 270+260 and pos[1] > 560 and pos[1] < 560+80):
						click = 1
                                                self.screen.blit(self.button_press_image, self.button_press_image.get_rect())
                                                pygame.display.flip()
                                elif event.type == pygame.MOUSEBUTTONUP and click == 1:
                                        pos = pygame.mouse.get_pos()
					if (pos[0] > 270 and pos[0] < 270+260 and pos[1] > 560 and pos[1] < 560+80):
						return
                                        else:
                                                click = 0
                                                self.screen.blit(self.menuimage2, self.menuimage2.get_rect())
                                                pygame.display.flip()
                                                        


	def playerSelect(self):
                # Display next screen
		self.colorimage = pygame.image.load("colorselect.png")
		self.screen.blit(self.colorimage, self.colorimage.get_rect())
		pygame.display.flip()
                self.p1picking = pygame.image.load("p1small.png")
                # Player 1 picking.  If Player 1, pick as normal.  If player 2, wait for player 1 to pick	
		while 1:
	                if self.player == 1:
                                # if cont_var = 1, continue
                                cont_var = 0
				for event in pygame.event.get():
                                        if event.type == pygame.QUIT: self.game_exit()
                                        if event.type == pygame.MOUSEBUTTONUP:
                                                pos = pygame.mouse.get_pos()
                                                if (pos[0] > 447 and pos[0] < 447+180 and pos[1] > 457 and pos[1] < 457+180):
							self.color1 = 'y'
							self.screen.blit(self.p1picking, [447, 457])
                                                        cont_var = 1
						if (pos[0] > 200 and pos[0] < 200+180 and pos[1] > 180 and pos[1] < 180+180):
							self.color1 = 'r'
							self.screen.blit(self.p1picking, [200, 180])
                                                        cont_var = 1
						if (pos[0] > 450 and pos[0] < 450+180 and pos[1] > 180 and pos[1] < 180+180):
							self.color1 = 'g'
							self.screen.blit(self.p1picking, [450, 180])
                                                        cont_var = 1
						if (pos[0] > 200 and pos[0] < 200+180 and pos[1] > 457 and pos[1] < 457+180):
							self.color1 = 'b'
							self.screen.blit(self.p1picking, [200, 457])
                                                        cont_var = 1
                                        	pygame.display.flip()
                                if cont_var:
                                        self.data_conn.transport.write(self.color1)
                                        break
        	        elif self.player == 2:
                                while 1:
                        		for event in pygame.event.get():
						if event.type == pygame.QUIT: self.game_exit()
                                        reactor.iterate()
                                        if self.data_conn.data == 'r':
                                		self.color1 = 'r'
						self.screen.blit(self.p1picking, [200, 180])
                                                cont_var = 1
                                        elif self.data_conn.data == 'y':
                                		self.color1 = 'y'
						self.screen.blit(self.p1picking, [447, 457])
                                                cont_var = 1
                                        elif self.data_conn.data == 'g':
                                		self.color1 = 'g'
						self.screen.blit(self.p1picking, [450, 180])
                                                cont_var = 1
                                        elif self.data_conn.data == 'b':
                                                self.color1 = 'b'
                                                self.screen.blit(self.p1picking, [200,457])
                                                cont_var = 1
                                        else: continue

                                        if cont_var == 1:
                                                pygame.display.flip()
                                                break
                                if cont_var == 1: break

                # Player 2 picking.  If player 1, wait for player 2 to pick, If player 2, pick as normal
        	self.p2picking = pygame.image.load("p2small.png")
		while 1:
                        if self.player == 2:
				for event in pygame.event.get():
					if event.type == pygame.QUIT: self.game_exit()
					if event.type == pygame.MOUSEBUTTONUP:
						pos = pygame.mouse.get_pos()
						if (pos[0] > 447 and pos[0] < 447+180 and pos[1] > 457 and pos[1] < 457+180):
							self.color2 = 'y'
                                                        self.data_conn.transport.write('y')
                                                        reactor.iterate()
							self.screen.blit(self.p2picking, [447, 457])
							pygame.display.flip()
							return
						if (pos[0] > 200 and pos[0] < 200+180 and pos[1] > 180 and pos[1] < 180+180):
							self.color2 = 'r'
                                                        self.data_conn.transport.write(self.color2)
                                                        reactor.iterate()
							self.screen.blit(self.p2picking, [200, 180])
							pygame.display.flip()
							return
						if (pos[0] > 450 and pos[0] < 450+180 and pos[1] > 180 and pos[1] < 180+180):
							self.color2 = 'g'
                                                        self.data_conn.transport.write(self.color2)
                                                        reactor.iterate()
							self.screen.blit(self.p2picking, [450, 180])
							pygame.display.flip()
							return
						if (pos[0] > 200 and pos[0] < 200+180 and pos[1] > 457 and pos[1] < 457+180):
							self.color2 = 'b'
                                                        self.data_conn.transport.write(self.color2)
                                                        reactor.iterate()
							self.screen.blit(self.p2picking, [200, 457])
							pygame.display.flip()
							return
                        elif self.player == 1:
                                while 1:
					for event in pygame.event.get():
						if event.type == pygame.QUIT: self.game_exit()
                                        reactor.iterate()
                                        if self.data_conn.data == 'r':
                                		self.color2 = 'r'
						self.screen.blit(self.p2picking, [200, 180])
                                                pygame.display.flip()
                                                return
                                        elif self.data_conn.data == 'y':
                                		self.color2 = 'y'
						self.screen.blit(self.p2picking, [447, 457])
                                                pygame.display.flip()
                                                return
                                        elif self.data_conn.data == 'g':
                                		self.color2 = 'g'
						self.screen.blit(self.p2picking, [450, 180])
                                                pygame.display.flip()
                                                return
                                        elif self.data_conn.data == 'b':
                                                self.color2 = 'b'
                                                self.screen.blit(self.p2picking, [200,457])
                                                pygame.display.flip()
                                                return
                                        else: continue
                                        
	def collision(self, r, p):
		counter = 0
		loopcounter = 0
		rising = True
		while loopcounter <= 21 and counter >= 0:
			explosionfile = "./explosion/explosion" + str(counter) + ".png"
			self.collideimage = pygame.image.load(explosionfile)
			self.collideimagerect = self.collideimage.get_rect()
			self.collideimagerect.x = r.rect.x - 25
			self.collideimagerect.y = r.rect.y - 25
			if (counter == 10):
				rising = False
			if (rising):
				counter  = counter + 1
			else:
				counter = counter - 1
			self.screen.fill(self.black)
			for e in self.edge:
				self.screen.blit(e.image, e.rect)
			for b in self.blocks:
				self.screen.blit(b.image, b.rect)
			self.screen.blit(self.player1.image, self.player1.rect)
			self.screen.blit(self.player2.image, self.player2.rect)
			self.screen.blit(self.collideimage, self.collideimagerect)
			pygame.display.flip()

		self.screen.fill(self.black)
		for e in self.edge:
			self.screen.blit(e.image, e.rect)
		for b in self.blocks:
			self.screen.blit(b.image, b.rect)
		self.screen.blit(self.player1.image, self.player1.rect)
		self.screen.blit(self.player2.image, self.player2.rect)

		if p == 1:
			print ("Player 2 wins!")
                        self.data_conn.transport.write("w")
                        reactor.iterate()
			self.winimage = pygame.image.load("p2win.png")
		else:
			print ("Player 1 wins!")
                        self.data_conn.transport.write("w")
                        reactor.iterate()
			self.winimage = pygame.image.load("p1win.png")

		self.screen.blit(self.winimage, [50, 0])
		pygame.display.flip()



		restart = False
		while not restart:
			for event in pygame.event.get():
				if event.type == pygame.QUIT: self.game_exit()
				if event.type == KEYDOWN:
					if (event.key == K_q):
						self.game_exit()
					if (event.key == K_r):
						return
					else:
						pass
				else:
					pass

	def startanimation(self):
		counter = 0
		p1 = pygame.image.load("p1.png")
		p2 = pygame.image.load("p2.png")

		while counter < 20:
			counter += 1
			self.screen.fill(self.black)
			for e in self.edge:
				self.screen.blit(e.image, e.rect)
			self.screen.blit(self.player1.image, self.player1.rect)
			self.screen.blit(self.player2.image, self.player2.rect)
			self.screen.blit(p1, [100,300])
			self.screen.blit(p2, [500,300])
			pygame.display.flip()
	
	## Helper functions so that both main functiosn can be the same

        def player_me(self):
                if self.player == 1:
                        return self.player1
                else:
                        return self.player2
        def player_other(self):
                if self.player == 1:
                        return self.player2
                else:
                        return self.player1
        def color_me(self):
                if self.player == 1:
                        return self.color1
                else:
                        return self.color2
        def color_other(self):
                if self.player == 1:
                        return self.color2
                else:
                        return self.color1

	def main(self):
		self.menu()
		self.black = 0, 0, 0
		pygame.key.set_repeat(300, 50)

                

		while 1:
			self.playerSelect()
                        if self.player == 1:
                        	self.data_conn.transport.write("o")
                        elif self.player == 2:
                                self.data_conn.transport.write("n")

                        # Reset data
                        reactor.iterate()
                        pygame.time.wait(500)
                        reactor.iterate()
                        
			self.exploderect = None
			self.collideplayer = None
			self.player1 = Player(self.color1)
                        if self.player == 1:
				self.player1.rect.x = 200
                        else:
                                self.player1.rect.x = 200 - 8
			self.player1.rect.y = 400
			self.player2 = Player(self.color2)
			self.player2.rect.x = 600
			self.player2.rect.y = 400

                	# Set players

			self.clock = pygame.time.Clock()
			self.screen.fill(self.black)
			self.blocks = []
			self.edge = []

			for n in range(800):
				self.edge.append(Block(0, n, 'w'))
				self.edge.append(Block(n, 0, 'w'))
				self.edge.append(Block(n, 800-8, 'w'))
				self.edge.append(Block(800-8, n, 'w'))

			self.startanimation()

			self.collided = False
			while not self.collided:
				self.clock.tick(30)
                                # check for data from other game
                                reactor.iterate()
                                if self.data_conn.data == 'o':
                                        pass
                                        # This indicates that the opponent has not pressed any buttons.
                                elif self.data_conn.data in ('l','r','d','u'):
                                        self.player_other().dir = self.data_conn.data
                                        self.player_other().tick()
                                        self.screen.blit(self.player_other().image, self.player_other().rect)
                                        block = Block(self.player_other().rect.x, self.player_other().rect.y, self.color_other())
                        		self.blocks.append(block)
                                elif self.data_conn.data == 'n':
                                        # Indicates data has not been processed yet.
                                        continue
                                elif self.data_conn.data == 'w':
                                        self.check_collisions()
                                        continue
                                # Indicate we must receive new data
                                self.data_conn.data = 'n'
                                data_written = 0
				for event in pygame.event.get():
					if event.type == pygame.QUIT: self.game_exit()
					if event.type == KEYDOWN:
#						if (event.key == K_a):
#							self.player1.dir = 'l'
#							self.player1.tick()
#							self.screen.blit(self.player1.image, self.player1.rect)
#							block = Block(self.player1.rect.x, self.player1.rect.y, self.color1)
#							self.blocks.append(block)
#						if (event.key == K_d):
#							self.player1.dir = 'r'
#							self.player1.tick()
#							self.screen.blit(self.player1.image, self.player1.rect)
#							block = Block(self.player1.rect.x, self.player1.rect.y, self.color1)
#							self.blocks.append(block)
#						if (event.key == K_w):
#							self.player1.dir = 'u'
#							self.player1.tick()
#							self.screen.blit(self.player1.image, self.player1.rect)
#							block = Block(self.player1.rect.x, self.player1.rect.y, self.color1)
#							self.blocks.append(block)
#						if (event.key == K_s):
#							self.player1.dir = 'd'
#							self.player1.tick()
#							self.screen.blit(self.player1.image, self.player1.rect)
#							block = Block(self.player1.rect.x, self.player1.rect.y, self.color1)
#							self.blocks.append(block)

						if (event.key == K_LEFT):
                                			if not data_written:
								self.player_me().dir = 'l'
								self.player_me().tick()
								self.screen.blit(self.player_me().image, self.player_me().rect)
								block = Block(self.player_me().rect.x, self.player_me().rect.y, self.color_me())
								self.blocks.append(block)
                                                        	self.data_conn.transport.write("l")
                                                                data_written = 1
                                                                reactor.iterate()
						if (event.key == K_RIGHT):
                                			if not data_written:
								self.player_me().dir = 'r'
								self.player_me().tick()
								self.screen.blit(self.player_me().image, self.player_me().rect)
								block = Block(self.player_me().rect.x, self.player_me().rect.y, self.color_me())
								self.blocks.append(block)
                                                        	self.data_conn.transport.write("r")
                                                                data_written = 1
                                                                reactor.iterate()
						if (event.key == K_UP):
                                			if not data_written:
								self.player_me().dir = 'u'
								self.player_me().tick()
								self.screen.blit(self.player_me().image, self.player_me().rect)
								block = Block(self.player_me().rect.x, self.player_me().rect.y, self.color_me())
								self.blocks.append(block)
                                                        	self.data_conn.transport.write("u")
                                                                data_written = 1
                                                                reactor.iterate()
						if (event.key == K_DOWN):
                                			if not data_written:
								self.player_me().dir = 'd'
								self.player_me().tick()
								self.screen.blit(self.player_me().image, self.player_me().rect)
								block = Block(self.player_me().rect.x, self.player_me().rect.y, self.color_me())
								self.blocks.append(block)
                                                        	self.data_conn.transport.write("d")
                                                                data_written = 1
                                                                reactor.iterate()

                                if not data_written:
                                        self.data_conn.transport.write("o")
                                        reactor.iterate()
				self.player_me().tick()
				self.player_other().tick()
				block1 = Block(self.player_me().rect.x, self.player_me().rect.y, self.color_me())
				block2 = Block(self.player_other().rect.x, self.player_other().rect.y, self.color_other())

				self.screen.fill(self.black)
                                self.check_collisions()

                                self.blocks.append(block1)
				self.blocks.append(block2)

				self.screen.blit(self.player1.image, self.player1.rect)
				self.screen.blit(self.player2.image, self.player2.rect)

				pygame.display.flip()


        def check_collisions(self):
                for e in self.edge:
			self.screen.blit(e.image, e.rect)
                	if self.player1.rect.colliderect(e):
        			if (not self.collided):
					self.collision(e, 1)
                			self.collided = True
			elif self.player2.rect.colliderect(e):
                		if (not self.collided):
        				self.collision(e, 2)
					self.collided = True

        	for b in self.blocks:
			self.screen.blit(b.image, b.rect)
                	if self.player1.rect.colliderect(b):
        			if (not self.collided):
					self.collision(b, 1)
                			self.collided = True
			elif self.player2.rect.colliderect(b):
                		if (not self.collided):
        				self.collision(b, 2)
					self.collided = True
        def game_exit(self):
                reactor.stop()
                sys.exit()



if __name__ == '__main__':
	gs = GameSpace()
        gs.premain()
