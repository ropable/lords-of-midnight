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
        return (int(x),int(y))
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
        
        vp1 = (512, 461) # 5 pixels above the horizon
        vp2 = (128, 463)
        vp3 = (896, 463)
        if gamedata.actor.heading in [lom.NORTH, lom.EAST, lom.SOUTH, lom.WEST]:
            sp1 = [-4608,-3072,-1792,-768,0,512,1024,1792,2816,4096] # Midpoint: 512
            sp2 = [-768,-256,128,512,1024,1792,2816,4096,5632] # Midpoint: 128
            sp3 = [-3072,-1792,-768,0,512,896,1280,1792] #Midpoint: 896
        else:
            sp1 = [-3456,-2176,-1152,-384,128,512,896,1408,2176,3200,4480] # Midpoint: 512
            sp2 = [-1152,-384,128,640,1408,2432,3712,5248,7040] # Midpoint: 128
            sp3 = [-4224,-2688,-1408,-384,384,896,1408,2176] #Midpoint: 896
        NORTH_DRAWPOINTS = [
            [
                getIntersectPoint(p1=vp1, p2=(-768,568), p3=vp2, p4=(2816,568)),
                getIntersectPoint(p1=vp1, p2=(0,568), p3=vp2, p4=(4096,568)),
                getIntersectPoint(p1=vp1, p2=(512, 568), p3=vp2, p4=(5632,568)),
                getIntersectPoint(p1=vp1, p2=(1024,568), p3=vp3, p4=(-3072,568)),
                getIntersectPoint(p1=vp1, p2=(1792,568), p3=vp3, p4=(-1792,568)),
            ],
            [
                getIntersectPoint(p1=vp1, p2=(-3072,568), p3=vp2, p4=(512,568)),
                getIntersectPoint(p1=vp1, p2=(-1792,568), p3=vp2, p4=(1024,568)),
                getIntersectPoint(p1=vp1, p2=(-768,568), p3=vp2, p4=(1792,568)),
                getIntersectPoint(p1=vp1, p2=(0,568), p3=vp2, p4=(2816,568)),
                getIntersectPoint(p1=vp1, p2=(512,568), p3=vp2, p4=(4096,568)),
                getIntersectPoint(p1=vp1, p2=(1024,568), p3=vp3, p4=(-1792,568)),
                getIntersectPoint(p1=vp1, p2=(1792,568), p3=vp3, p4=(-768,568)),
                getIntersectPoint(p1=vp1, p2=(2816,568), p3=vp3, p4=(0,568)),
                getIntersectPoint(p1=vp1, p2=(4096,568), p3=vp3, p4=(512,568)),
            ],
            [
                getIntersectPoint(p1=vp1, p2=(-4608,568), p3=vp2, p4=(-256,568)),
                getIntersectPoint(p1=vp1, p2=(-3072,568), p3=vp2, p4=(128,568)),
                getIntersectPoint(p1=vp1, p2=(-1792,568), p3=vp2, p4=(512,568)),
                getIntersectPoint(p1=vp1, p2=(-768,568), p3=vp2, p4=(1024,568)),
                getIntersectPoint(p1=vp1, p2=(0,568), p3=vp2, p4=(1792,568)),
                getIntersectPoint(p1=vp1, p2=(512,568), p3=vp2, p4=(2816,568)),
                getIntersectPoint(p1=vp1, p2=(1024,568), p3=vp3, p4=(-768,568)),
                getIntersectPoint(p1=vp1, p2=(1792,568), p3=vp3, p4=(0,568)),
                getIntersectPoint(p1=vp1, p2=(2816,568), p3=vp3, p4=(512,568)),
                getIntersectPoint(p1=vp1, p2=(4096,568), p3=vp3, p4=(896,568)),
                getIntersectPoint(p1=vp1, p2=(5632,568), p3=vp3, p4=(1280,568)),
            ],
            [
                getIntersectPoint(p1=vp1, p2=(-4608,568), p3=vp2, p4=(-768,568)),
                getIntersectPoint(p1=vp1, p2=(-3072,568), p3=vp2, p4=(-256,568)),
                getIntersectPoint(p1=vp1, p2=(-1792,568), p3=vp2, p4=(128,568)),
                getIntersectPoint(p1=vp1, p2=(-768,568), p3=vp2, p4=(512,568)),
                getIntersectPoint(p1=vp1, p2=(0,568), p3=vp2, p4=(1024,568)),
                getIntersectPoint(p1=vp1, p2=(512,568), p3=vp2, p4=(1792,568)),
                getIntersectPoint(p1=vp1, p2=(1024,568), p3=vp3, p4=(0,568)),
                getIntersectPoint(p1=vp1, p2=(1792,568), p3=vp3, p4=(512,568)),
                getIntersectPoint(p1=vp1, p2=(2816,568), p3=vp3, p4=(896,568)),
                getIntersectPoint(p1=vp1, p2=(4096,568), p3=vp3, p4=(1280,568)),
                getIntersectPoint(p1=vp1, p2=(5632,568), p3=vp3, p4=(1792,568)),
            ],
            [
                getIntersectPoint(p1=vp1, p2=(-3072,568), p3=vp2, p4=(-768,568)),
                getIntersectPoint(p1=vp1, p2=(-1792,568), p3=vp2, p4=(-256,568)),
                getIntersectPoint(p1=vp1, p2=(-768,568), p3=vp2, p4=(128,568)),
                getIntersectPoint(p1=vp1, p2=(0,568), p3=vp2, p4=(512,568)),
                getIntersectPoint(p1=vp1, p2=(512,568), p3=vp2, p4=(1024,568)),
                getIntersectPoint(p1=vp1, p2=(1024,568), p3=vp3, p4=(512,568)),
                getIntersectPoint(p1=vp1, p2=(1792,568), p3=vp3, p4=(896,568)),
                getIntersectPoint(p1=vp1, p2=(2816,568), p3=vp3, p4=(1280,568)),
                getIntersectPoint(p1=vp1, p2=(4096,568), p3=vp3, p4=(1792,568)),
            ],
            [
                getIntersectPoint(p1=vp1, p2=(-1792,568), p3=vp2, p4=(-768,568)),
                getIntersectPoint(p1=vp1, p2=(-768,568), p3=vp2, p4=(-256,568)),
                getIntersectPoint(p1=vp1, p2=(0,568), p3=vp2, p4=(128,568)),
                getIntersectPoint(p1=vp1, p2=(512,568), p3=vp2, p4=(512,568)),
                getIntersectPoint(p1=vp1, p2=(1024,568), p3=vp3, p4=(896,568)),
                getIntersectPoint(p1=vp1, p2=(1792,568), p3=vp3, p4=(1280,568)),
                getIntersectPoint(p1=vp1, p2=(2816,568), p3=vp3, p4=(1792,568)),
            ]
        ]
        #print(NORTH_DRAWPOINTS)
        for i in NORTH_DRAWPOINTS[0]:
            screen.set_at(i, colours.black)
        for i in NORTH_DRAWPOINTS[1]:
            screen.set_at(i, colours.black)
        for i in NORTH_DRAWPOINTS[2]:
            screen.set_at(i, colours.black)
        for i in NORTH_DRAWPOINTS[3]:
            screen.set_at(i, colours.black)
        for i in NORTH_DRAWPOINTS[4]:
            screen.set_at(i, colours.black)
        for i in NORTH_DRAWPOINTS[5]:
            screen.set_at(i, colours.black)
        downs_path = os.path.join(lom.IMG_PATH, 'terrain_downs.png')
        downs_img = pygame.image.load(downs_path).convert_alpha()
        downs_img_size = (downs_img.get_size())
        downs_img_sml = pygame.transform.scale(downs_img, (int(downs_img_size[0]*0.7), int(downs_img_size[1]*0.7)))
        screen.blit(downs_img_sml, (NORTH_DRAWPOINTS[5][2][0]-(downs_img_sml.get_width()/2), NORTH_DRAWPOINTS[5][2][1]-(downs_img_sml.get_height())))
        screen.blit(downs_img, (NORTH_DRAWPOINTS[5][3][0]-(downs_img.get_width()/2), NORTH_DRAWPOINTS[5][3][1]-(downs_img.get_height())))
        screen.blit(downs_img_sml, (NORTH_DRAWPOINTS[5][4][0]-(downs_img_sml.get_width()/2), NORTH_DRAWPOINTS[5][4][1]-(downs_img_sml.get_height())))
        pygame.draw.line(screen, colours.black, (0, 568), (1024,568), 1)
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