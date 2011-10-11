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

def calculateGradient(p1, p2):
    # Calculate the gradient 'm' of a line between p1 and p2
    if (p1[0] != p2[0]):
        m = (p1[1] - p2[1]) / (p1[0] - p2[0])
        return m
    else:
       return None

def calculateYAxisIntersect(p, m):
    # Calculate the point 'b' where line crosses the Y axis
    return  p[1] - (m * p[0])
def getIntersectPoint(p1, p2, p3, p4):
    m1 = calculateGradient(p1, p2)
    m2 = calculateGradient(p3, p4)       
    # See if the the lines are parallel
    if (m1 != m2):
        # Not parallel
        # See if either line is vertical
        if (m1 is not None and m2 is not None):
            # Neither line vertical           
            b1 = calculateYAxisIntersect(p1, m1)
            b2 = calculateYAxisIntersect(p3, m2)   
            x = (b2 - b1) / (m1 - m2)       
            y = (m1 * x) + b1           
        else:
            # Line 1 is vertical so use line 2's values
            if (m1 is None):
                b2 = calculateYAxisIntersect(p3, m2)   
                x = p1[0]
                y = (m2 * x) + b2
            # Line 2 is vertical so use line 1's values               
            elif (m2 is None):
                b1 = calculateYAxisIntersect(p1, m1)
                x = p3[0]
                y = (m1 * x) + b1           
            else:
                assert false
        return (x,y)
    else:
        return None
    
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
        
        vp1 = (SCREENSIZE[0]*0.5, SCREENSIZE[1]*0.6) # 5 pixels above the horizon
        vp2 = (128, SCREENSIZE[1]*0.605)
        vp3 = (896, SCREENSIZE[1]*0.605)
        if gamedata.actor.heading in [lom.NORTH, lom.EAST, lom.SOUTH, lom.WEST]:
            sp1 = [-4608,-3072,-1792,-768,-0,512,1024,1792,2816,4096,5632]
            sp2 = [-512,-128,128,512,1024,1792,2816,4096]
            sp3 = [-3072,-1792,-768,-0,512,896,1152,1536]
            # Draw the 1st set of vanishing points 
            for i in sp1:
                pygame.draw.line(screen, colours.black, (i, SCREENSIZE[1]*0.74), vp1, 1)            
            # Draw the 2nd set
            for i in sp2:
                pygame.draw.line(screen, colours.red, (i, SCREENSIZE[1]*0.74), vp2, 1)
            # Draw the 3rd set
            for i in sp3:
                pygame.draw.line(screen, colours.green, (i, SCREENSIZE[1]*0.74), vp3, 1)
        else:
            sp1 = [-3456,-2176,-1152,-384,128,512,896,1408,2176,3200,4480]
            sp2 = [-512,-128,128,640,1408,2432,3712,5248]
            sp3 = [-4224,-2688,-1408,-384,384,896,1152,1536]            
            for i in sp1:
                pygame.draw.line(screen, colours.black, (i, SCREENSIZE[1]*0.74), vp1, 1)            
            for i in sp2:
                pygame.draw.line(screen, colours.red, (i, SCREENSIZE[1]*0.74), vp2, 1)
            for i in sp3:
                pygame.draw.line(screen, colours.green, (i, SCREENSIZE[1]*0.74), vp3, 1)

        
        #heights = [468,471,475,480,493,518,568]
        #for i in heights:
        #    pygame.draw.line(screen, colours.black, (0,i), (1024,i), 1)
        #intersect = getIntersectPoint(p1=vanishing_point, p2=(-64,568), p3=(0,518), p4=(1024,518))
        #print(intersect)
        #dot = pygame.image.load(os.path.join(lom.IMG_PATH,'dot.png')).convert_alpha()
        #screen.blit(dot, (intersect[0]-(dot.get_width()/2), intersect[1]-(dot.get_height()/2)))
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