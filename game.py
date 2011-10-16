#!/usr/bin/python
from __future__ import division

__author__ = 'Ashley Felton'
__version__ = '0.0'
__license__ = 'Public Domain'

import pygame
from pygame.locals import *
#screen = pygame.display.set_mode((1024,768), SWSURFACE)
import os
os.environ["SDL_VIDEO_CENTERED"] = "1" ## Centre the graphics window.
SCREENSIZE = (1024, 768)
screen = pygame.display.set_mode(SCREENSIZE, 0, 32)

from pgu import engine, text
from easypg import colours

import lom
gamedata = lom.GameData()
pygame.font.init()
font = pygame.font.Font(lom.FONT_BENG, 16)
    
class StartScreen(engine.State):
    def paint(self, screen): 
        screen.fill(colours.blue)
        #message = 'Now explore the epic world of THE LORDS OF MIDNIGHT by Mike Singleton'
        #text.writewrap(screen, font, pygame.Rect(10,10,100,100), colours.black, message)
        text.write(screen, font, (10,10), colours.green, 'Now explore the epic world of', 0)
        text.write(screen, font, (10,24), colours.yellow, 'THE LORDS OF MIDNIGHT', 0)
        text.write(screen, font, (10,38), colours.purple, '       by', 0)
        text.write(screen, font, (10,52), colours.aqua, ' Mike Singleton', 0)
        pygame.display.update()
    
    def event(self, event):
        if event.type == QUIT:
            return engine.Quit()
        elif event.type == KEYDOWN:
            return GameScreen(self.game)
        
class GameScreen(engine.State):
    def paint(self, screen):
        screen.fill(colours.blue)
        land = pygame.surface.Surface((SCREENSIZE[0],SCREENSIZE[1]*0.39))
        land.fill(colours.white)
        screen.blit(land, (0,SCREENSIZE[1]*0.61))
        # Display the name of the current actor
        text.write(screen, font, (6,6), colours.yellow, gamedata.actor.name, 0)
        text.write(screen, font, (6,20), colours.aqua, gamedata.actor.location_desc(), 0)
        # If the Actor is facing one of the cardinal directions, render the panorama for that heading.
        if gamedata.actor.heading in [lom.NORTH, lom.EAST, lom.SOUTH, lom.WEST]:
            cardinal = True
        else:
            cardinal = False
        drawpoints = lom.drawpoints(cardinal=cardinal, grids=True, screen=screen)
        for i in drawpoints[0]:
            screen.set_at(i, colours.black)
        for i in drawpoints[1]:
            screen.set_at(i, colours.black)
        for i in drawpoints[2]:
            screen.set_at(i, colours.black)
        for i in drawpoints[3]:
            screen.set_at(i, colours.black)
        for i in drawpoints[4]:
            screen.set_at(i, colours.black)
        for i in drawpoints[5]:
            screen.set_at(i, colours.black)
        downs_path = os.path.join(lom.IMG_PATH, 'terrain_downs.png')
        downs_img = pygame.image.load(downs_path).convert_alpha()
        downs_img_size = (downs_img.get_size())
        downs_img_sml = pygame.transform.scale(downs_img, (int(downs_img_size[0]*0.7), int(downs_img_size[1]*0.7)))
        #screen.blit(downs_img_sml, (NORTH_DRAWPOINTS[5][2][0]-(downs_img_sml.get_width()/2), NORTH_DRAWPOINTS[5][2][1]-(downs_img_sml.get_height())))
        #screen.blit(downs_img, (NORTH_DRAWPOINTS[5][3][0]-(downs_img.get_width()/2), NORTH_DRAWPOINTS[5][3][1]-(downs_img.get_height())))
        #screen.blit(downs_img_sml, (NORTH_DRAWPOINTS[5][4][0]-(downs_img_sml.get_width()/2), NORTH_DRAWPOINTS[5][4][1]-(downs_img_sml.get_height())))
        #pygame.draw.line(screen, colours.black, (0, 568), (1024,568), 1)
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
                gamedata.actor.heading = NORTH
            elif event.key == K_2:
                # Change actor heading to northeast
                gamedata.actor.heading = NORTHEAST
            elif event.key == K_3:
                # Change actor heading to east
                gamedata.actor.heading = EAST
            elif event.key == K_4:
                # Change actor heading to southeast
                gamedata.actor.heading = SOUTHEAST
            elif event.key == K_5:
                # Change actor heading to south
                gamedata.actor.heading = SOUTH
            elif event.key == K_6:
                # Change actor heading to southwest
                self.b.actor.heading = SOUTHWEST
            elif event.key == K_7:
                # Change actor heading to west
                gamedata.actor.heading = WEST
            elif event.key == K_8:
                # Change actor heading to northwest
                gamedata.actor.heading = NORTHWEST
            elif event.key == K_MINUS:
                # Rotate heading CCW
                new_bearing = gamedata.actor.heading.rotate_ccw()
                gamedata.actor.heading = lom.HEADINGS.get(new_bearing)
            elif event.key == K_EQUALS:
                # Rotate heading CW
                new_bearing = gamedata.actor.heading.rotate_cw()
                gamedata.actor.heading = lom.HEADINGS.get(new_bearing)
            elif event.key == K_q:
                # Move character forwards (if possible)
                print(gamedata.actor.clock)
                gamedata.actor.move()
            elif event.key == K_r:
                # Enter think screen
                pass
            self.repaint()
    
# Run the main game loop.
pygame.init()
game = engine.Game()
game.run(GameScreen(game), screen)