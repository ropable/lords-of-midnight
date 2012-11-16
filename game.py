#!/usr/bin/python
from __future__ import division, print_function, unicode_literals
import os
import pygame
import lom_data
from pygame.locals import *
from pgu import engine, text
from utils import draw_grids
__author__ = 'Ashley Felton'
__version__ = '0.0'
__license__ = 'Public Domain'

pygame.font.init()
os.environ["SDL_VIDEO_CENTERED"] = "1" ## Centre the graphics window.
screen = pygame.display.set_mode(lom_data.SCREENSIZE, 0, 32)
#screen = pygame.display.set_mode(lom_data.SCREENSIZE, SWSURFACE)

class StartScreen(engine.State):
    def paint(self, screen):
        screen.fill(lom_data.BLUE)
        #message = 'Now explore the epic world of THE LORDS OF MIDNIGHT by Mike Singleton'
        #text.writewrap(screen, font, pygame.Rect(10,10,100,100), lom_data.black, message)
        text.write(screen, font, (10,10), lom_data.GREEN, 'Now explore the epic world of', 0)
        text.write(screen, font, (10,24), lom_data.YELLOW, 'THE LORDS OF MIDNIGHT', 0)
        text.write(screen, font, (10,38), lom_data.PURPLE, '       by', 0)
        text.write(screen, font, (10,52), lom_data.AQUA, ' Mike Singleton', 0)
        pygame.display.update()
    
    def event(self, event):
        if event.type == QUIT:
            return engine.Quit()
        elif event.type == KEYDOWN:
            return GameScreen(self.game)
        
class GameScreen(engine.State):
    def paint(self, screen):
        screen.fill(lom_data.BLUE)
        land = pygame.surface.Surface((lom_data.SCREENSIZE[0], lom_data.SCREENSIZE[1]*0.39))
        land.fill(lom_data.WHITE)
        screen.blit(land, (0, lom_data.SCREENSIZE[1]*0.61))
        # Display the name of the current actor.
        text.write(screen, font, (6,6), lom_data.YELLOW, gamedata.actor.name, 0)
        # Describe what they are looking at.
        text.write(screen, font, (6,20), lom_data.AQUA, gamedata.actor.location_desc(gamedata.world), 0)
        # Draw their heraldry.
        shield = pygame.image.load(gamedata.actor.heraldry).convert_alpha()
        screen.blit(shield, (920,6))
        # Draw the actor's perspective.
        draw_grids(cardinal=gamedata.actor.heading.cardinal, grids=True, screen=screen)
        gamedata.actor.render_perspective(gamedata.world, screen)
        pygame.display.update()
        
    def event(self, event):
        if event.type is KEYDOWN:
            if event.key == K_ESCAPE:
                return engine.Quit(self.game)
            elif event.key == K_c:
                # Switch actors to Luxor
                gamedata.actor = gamedata.luxor
            elif event.key == K_v:
                # Switch actors to Morkin
                gamedata.actor = gamedata.morkin
            elif event.key == K_b:
                # Switch actors to Corleth
                gamedata.actor = gamedata.corleth
            elif event.key == K_n:
                # Switch actors to Morkin
                gamedata.actor = gamedata.rorthron
            elif event.key == K_1:
                # Change actor heading to north
                gamedata.actor.heading = lom_data.NORTH
            elif event.key == K_2:
                # Change actor heading to northeast
                gamedata.actor.heading = lom_data.NORTHEAST
            elif event.key == K_3:
                # Change actor heading to east
                gamedata.actor.heading = lom_data.EAST
            elif event.key == K_4:
                # Change actor heading to southeast
                gamedata.actor.heading = lom_data.SOUTHEAST
            elif event.key == K_5:
                # Change actor heading to south
                gamedata.actor.heading = lom_data.SOUTH
            elif event.key == K_6:
                # Change actor heading to southwest
                gamedata.actor.heading = lom_data.SOUTHWEST
            elif event.key == K_7:
                # Change actor heading to west
                gamedata.actor.heading = lom_data.WEST
            elif event.key == K_8:
                # Change actor heading to northwest
                gamedata.actor.heading = lom_data.NORTHWEST
            elif event.key == K_MINUS:
                # Rotate actor heading CCW
                gamedata.actor.rotate_ccw()
            elif event.key == K_EQUALS:
                # Rotate actor heading CW
                gamedata.actor.rotate_cw()
            elif event.key == K_q:
                # Move character forwards (if possible)
                gamedata.actor.move(gamedata)
            elif event.key == K_r:
                # Enter think screen
                pass
            self.repaint()
    
# Run the main game loop.
gamedata = lom_data.DefaultGameData(cheatmode=True)
font = pygame.font.Font(lom_data.FONT_BENG, 16)

pygame.init()
game = engine.Game()
game.run(GameScreen(game), screen)