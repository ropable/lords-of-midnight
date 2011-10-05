#!/usr/bin/python
"""
State Machine Demo

An example of one way to switch between the various states of a game,
such as a main gameplay screen and a status screen. There's just enough
detail to show how the idea works in practice with a fake title screen,
status screen, and a pop-up screen. You can see the number of items on
the stack flicker from 0 to 1, or 1 to 2, as you run the program.

How it works:
The system switches between states by keeping a list called "game_state".
The Game class' main loop, Go(), looks at this list, pulls off the last item,
and tries to call a function named by it. This system helps prevent messy
infinite loops of function A calling B and B calling A, by having each screen
set the class' "done" flag to end its control of the program. When you want to
switch to another screen, just put the desired next screen(s) onto the stack.
"""

__author__ = 'Ashley Felton'
__version__ = '0.0'
__license__ = 'Public Domain'

import os
import json
os.environ["SDL_VIDEO_CENTERED"] = "1" ## Centre the graphics window.
import pygame
from pygame.locals import * ## Event handling constants.
from sys import path

PROJECT_PATH = path[0]
ASSET_PATH = PROJECT_PATH + os.sep + 'assets'
FONT_PATH = ASSET_PATH + os.sep + 'font'
FONT_BENG = FONT_PATH + os.sep + 'benguiat_book_bt.ttf'
IMG_PATH = ASSET_PATH + os.sep + 'img'
SCREEN_SIZE = (1024, 768)
STARTING_SCREEN = "title_screen"
# Define some RGB colours as tuples
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
LT_BLUE = (0, 255, 255)

HEADING_OFFSET = {
    'north':(-1,0),
    'northeast':(-1,1),
    'east':(0,1),
    'southeast':(1,1),
    'south':(1,0),
    'southwest':(1,-1),
    'west':(0,-1)}
MAP_JSON = json.loads(open('data/map.json','r').readline())

class Actor:
    def __init__(self, *args, **kwargs):
        self.name = kwargs.get('name') or 'Lord'
        self.location = kwargs.get('location') or (0,0) # A two-tuple coordinate (NOT x, y)
        self.energy = kwargs.get('energy') or 127 # Energy ranges between 0 and 127
        self.alive = kwargs.get('alive') or True
        self.heading = kwargs.get('heading') or 'north'
        self.clock = kwargs.get('clock') or 5 # 5AM is dawn
        self.weapon = kwargs.get('weapon') or None
    
    def location_desc(self):
        location_desc = 'He stands at {0}, looking {1} to {2}.'
        map_grid = MAP_JSON[self.location[0]][self.location[1]]
        offset = HEADING_OFFSET.get(self.heading)
        facing = MAP_JSON[self.location[0]-offset[0]][self.location[1]-offset[1]].get('name')
        return location_desc.format(map_grid.get('name'), self.heading, facing)
        
class GameData:
    def __init__(self, *args, **kwargs):
        self.actor = kwargs.get('actor')

class Game:
    def __init__(self, **options):
        self.screen = options.get("screen", pygame.display.set_mode(SCREEN_SIZE, 0, 32))
        self.game_state = [STARTING_SCREEN] # A stack of game screens.
        self.done = False # Done with current screen loop?
        self.messages = [] # Checked during event loops.
        self.font = pygame.font.Font(FONT_BENG, 16)
        self.clock = pygame.time.Clock() ## For FPS management.
        # Define actors
        self.luxor = Actor(name='Luxor the Moonprince', location=(41,13))
        self.morkin = Actor(name='Morkin', location=(41,13))
        self.corleth = Actor(name='Corleth the Fey', location=(41,13))
        self.rorthron = Actor(name='Rorthron', location=(41,13))
        # Define starting game data
        self.game_data = GameData(actor=self.luxor)
        
    def run(self):
        '''
        This is the main game loop.

        Go between various screens until the game is over.
        There's a stack of game states in self.game_state, which can have
        additional items appended and popped. If the stack is empty, or
        if this loop reaches a state not corresponding to the name of a
        function this class has, the game will end.

        The exact way this determines the function names assumes that they're
        functions of this class, named exactly as the strings appended to
        the list. E.g. "title_screen" leads this function to look
        for a function called title_screen. 
        If at any point no appropriate function is found, or if nothing is 
        left on the stack, the game ends.
        '''
        while True:
            if not self.game_state:
                break # Game over!
            
            next_state = self.game_state.pop()
            print "Returned to main loop. Now switching to: " + next_state
            function_name = next_state#.replace(" ","") ## Naming convention
            if hasattr(self, function_name):
                function = getattr(self, function_name)
                function()
            else:
                break # Game over!
        print "Game over. Thanks for playing!"

    def notify(self, message):
        """Get a message from the interface or game entities.
        These messages are handled during one of the screen loops.
        Use a dictionary format with a "headline" key, eg:
        {"headline":"Got Object","object":"Coconut"} """
        self.messages.append(message)
    
    def title_screen(self):
        '''
        The game title screen.
        '''
        self.done = False
        while not self.done:
            # Handle messages from elsewhere, such as the interface.
            for message in self.messages:
                headline = message.get("headline", "")
                print "Got a message: " + headline
            self.messages = []
            # Handle events.
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.done = True
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.done = True
                        self.game_state.append('game_screen')
                    # Some sample reaction to events.
                    elif event.key == K_s:
                        # This screen will end and go to another screen.
                        self.done = True
                        self.game_state.append("status_screen")

            ## Draw a sample set of stuff on the screen.
            self.screen.fill(BLUE)
            text_render = self.font.render('Now explore the epic world of', True, GREEN)
            self.screen.blit(text_render, (10,10))
            text_render = self.font.render('THE LORDS OF MIDNIGHT', True, YELLOW)
            self.screen.blit(text_render, (10,24))
            text_render = self.font.render('       by', True, PURPLE)
            self.screen.blit(text_render, (10,36))
            text_render = self.font.render(' Mike Singleton', True, LT_BLUE)
            self.screen.blit(text_render, (10,48))
            pygame.display.update()
            self.clock.tick(20)

    def game_screen(self):
        '''
        Main gameplay screen.
        '''
        self.done = False
        # Handle events.
        while not self.done:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.done = True
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.done = True
                        self.game_state.append("exit_screen")
                    elif event.key == K_c:
                        # Switch actors to Luxor
                        self.game_data.actor = self.luxor
                    elif event.key == K_v:
                        # Switch actors to Morkin
                        self.game_data.actor = self.morkin
                    elif event.key == K_b:
                        # Switch actors to Corleth
                        self.game_data.actor = self.corleth
                    elif event.key == K_n:
                        # Switch actors to Morkin
                        self.game_data.actor = self.rorthron

            self.screen.fill(BLUE)
            land = pygame.surface.Surface((1024,300))
            land.fill(WHITE)
            self.screen.blit(land, (0,468))
            # Display the name of the current actor
            actor_name = self.font.render(self.game_data.actor.name, True, YELLOW)
            self.screen.blit(actor_name, (6,6))
            location_desc = self.font.render(self.game_data.actor.location_desc(), True, LT_BLUE)
            self.screen.blit(location_desc, (6,20))
            pygame.display.update()
            
    def status_screen(self):
        """A sample screen."""

        self.done = False
        while not self.done:

            ## Handle messages from elsewhere, such as the interface.
            for message in self.messages:
                headline = message.get("headline","")
                print "Got a message: "+headline

            self.messages = []

            ## Handle events.
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.done = True
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.done = True

                    ## Some sample reaction to events.
                    elif event.key == K_t:
                        ## This screen will end and go to another screen.
                        self.done = True
                        self.game_state.append("title_screen")
                    elif event.key == K_p:
                        ## Return to _this_ screen after the pop-up.
                        self.done = True
                        self.game_state.append("status_screen")
                        self.game_state.append("popup_screen")

            ## Draw a sample set of stuff on the screen.
            self.screen.fill((0,0,180,255))
            text = "This is the Status Screen. Esc= quit, T= Title Screen, P= Pop-Up Screen."
            text_rendered = self.font.render(text,1,(255,255,255))
            self.screen.blit(text_rendered,(100,100))
            status = self.font.render("# of game states on stack: "+str(len(self.game_state)),1,(255,255,255))
            self.screen.blit(status,(100,300))

            pygame.display.update()
            self.clock.tick(20)

    def popup_screen(self):
        """A sample screen, resembling a pop-up dialog or something."""

        self.done = False
        while not self.done:

            ## Handle messages from elsewhere, such as the interface.
            for message in self.messages:
                headline = message.get("headline","")
                print "Got a message: "+headline

            self.messages = []

            ## Handle events.
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        ## This screen ends w/o putting another on stack.
                        self.done = True

            ## Draw a sample set of stuff on the screen.
            self.screen.fill((200,200,255),(50,50,700,500))
            text = "This is a Pop-Up Screen. Esc= leave this screen."
            text_rendered = self.font.render(text,1,(0,0,0))
            self.screen.blit(text_rendered,(100,100))
            status = self.font.render("# of game states on stack: "+str(len(self.game_state)),1,(0,0,0))
            self.screen.blit(status,(100,300))

            pygame.display.update()
            self.clock.tick(20)

# Run the main game loop.
pygame.init()
game = Game()
game.run()