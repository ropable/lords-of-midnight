#!/usr/bin/python
from __future__ import division, print_function, unicode_literals
import os
import json
from sys import path
#from models import *
from models import Heading, Terrain, Object, Monster, Race, Actor, GameData
from utils import getIntersectPoint


# Game constants
PROJECT_PATH = path[0]
ASSET_PATH = PROJECT_PATH + os.sep + 'assets'
FONT_PATH = ASSET_PATH + os.sep + 'font'
FONT_BENG = FONT_PATH + os.sep + 'benguiat_book_bt.ttf'
IMG_PATH = ASSET_PATH + os.sep + 'img'
SCREENSIZE = (1024, 768)
# Colour tuples
WHITE = (255, 255, 255)
SILVER = (191, 191, 191)
GREY = (128, 128, 128)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
MAROON = (128, 0, 0)
YELLOW = (255, 255, 0)
OLIVE = (128, 128, 0)
LIME = (0, 255, 0)
GREEN = (0, 128, 0)
AQUA = (0, 255, 255)
TEAL = (0, 128, 128)
BLUE = (0, 0, 255)
NAVY = (0, 0, 128)
FUCHSIA = (255, 0, 255)
PURPLE = (128, 0, 128)
# Define races
FREE = Race('free')
FOUL = Race('foul')
FEY = Race('fey')
HALF_FEY = Race('half_fey') # He's special: half-human, half-fey.
TARG = Race('targ')
WISE = Race('wise')
SKULKRIN = Race('skulkrin')
DRAGON = Race('dragon')
# Define terrain types
PLAINS = Terrain('plains')
MOUNTAINS = Terrain('mountains', os.path.join(IMG_PATH, 'terrain_mountains.png'), 3, 64)
CITADEL = Terrain('citadel', os.path.join(IMG_PATH, 'terrain_citadel.png'))
FOREST = Terrain('forest', os.path.join(IMG_PATH, 'terrain_forest.png'), 2.5, 12)
TOWER = Terrain('tower', os.path.join(IMG_PATH, 'terrain_tower.png'))
HENGE = Terrain('henge', os.path.join(IMG_PATH, 'terrain_henge.png'))
VILLAGE = Terrain('village', os.path.join(IMG_PATH, 'terrain_village.png'))
DOWNS = Terrain('downs', os.path.join(IMG_PATH, 'terrain_downs.png'), 1.5, 16)
KEEP = Terrain('keep', os.path.join(IMG_PATH, 'terrain_keep.png'))
SNOWHALL = Terrain('snowhall', os.path.join(IMG_PATH, 'terrain_snowhall.png'))
LAKE = Terrain('lake', os.path.join(IMG_PATH, 'terrain_lake.png'))
FROZEN_WASTES = Terrain('frozen_wastes', os.path.join(IMG_PATH, 'terrain_wastes.png'), 999)
RUIN = Terrain('ruin', os.path.join(IMG_PATH, 'terrain_ruin.png'))
LITH = Terrain('lith', os.path.join(IMG_PATH, 'terrain_lith.png'))
CAVERN = Terrain('cavern', os.path.join(IMG_PATH, 'terrain_cavern.png'))

CARDINAL_DRAW_COORDS = [
	getIntersectPoint(p1=(512,462), p2=(512,568), p3=(128,460), p4=(5632,568)),
	getIntersectPoint(p1=(512,462), p2=(512,568), p3=(128,460), p4=(4096,568)),
	getIntersectPoint(p1=(512,462), p2=(512,568), p3=(128,460), p4=(2816,568)),
	getIntersectPoint(p1=(512,462), p2=(512,568), p3=(128,460), p4=(1792,568)),
	getIntersectPoint(p1=(512,462), p2=(512,568), p3=(128,460), p4=(1024,568)),
	getIntersectPoint(p1=(512,462), p2=(512,568), p3=(128,460), p4=(512,568)),
]
# Define headings.
# A note about offsets: due to how the world data is stored (rows of columns),
# these offsets are NOT X,Y!
# Rather the opposite: (a,-b) means to move one row down (-Y) and one column left (-X).
[(), ()]
NORTH = Heading(name='north', cardinal=True, bearing=0, offset=(-1,0), 
    view_offsets=[
        # A list of lists; precalculated screen draw coords (x,y), location offsets and image scale.
        # This is the order in which terrain pieces are drawn to the screen (furtherest first).
        #(draw coords, offset, scale]
        [(512, 467), (-6, 0), 0.1],
		# Left
		[(475, 469), (-6, -1), 0.1],
        [(402, 471), (-6, -2), 0.1],
        [(246, 474), (-5, -3), 0.1],
        [(170, 472), (-5, -4), 0.1],
        [(89, 470), (-4, -5), 0.1],
        [(28, 472), (-3, -5), 0.11],
		# Right
		[(548, 469), (-6, 1), 0.1],
        [(621, 471), (-6, 2), 0.1],
		[(777, 474), (-5, 3), 0.1],
        [(853, 472), (-5, 4), 0.1],
        [(934, 470), (-4, 5), 0.1],
        [(995, 472), (-3, 5), 0.11],
		# Centre
        [(512, 470), (-5, 0), 0.12],
		# Left
		[(457, 473), (-5, -1), 0.11],
        [(356, 474), (-5, -2), 0.11],
        [(188, 476), (-4, -3), 0.13],
        [(128, 473), (-4, -4), 0.12],
        [(74, 474), (-3, -4), 0.14],
        # Right
		[(566, 473), (-5, 1), 0.11],
        [(667, 474), (-5, 2), 0.11],
        [(835, 476), (-4, 3), 0.13],
        [(896, 473), (-4, 4), 0.12],
        [(949, 474), (-3, 4), 0.14],
        # Centre
		[(512, 475), (-4, 0), 0.16],
        # Left
		[(427, 479), (-4, -1), 0.13],
        [(294, 480), (-4, -2), 0.14],
        [(128, 479), (-3, -3), 0.17],
        [(44, 483), (-2, -3), 0.22],
        # Right
		[(596, 479), (-4, 1), 0.13],
        [(729, 480), (-4, 2), 0.14],
        [(896, 479), (-3, 3), 0.17],
        [(979, 483), (-2, 3), 0.22],
		# Centre
		[(512, 484), (-3, 0), 0.18],
        # Left
		[(376, 489), (-3, -1), 0.18],
        [(220, 486), (-3, -2), 0.18],
        [(128, 493), (-2, -2), 0.24],
        [(-42, 507), (-1, -2), 0.3],
        # Right
		[(647, 489), (-3, 1), 0.18],
        [(803, 486), (-3, 2), 0.18],
        [(896, 493), (-2, 2), 0.24],
        [(1066, 507), (-1, 2), 0.3],
		# Centre
		[(512, 506), (-2, 0), 0.4],
        # Left
		[(294, 506), (-2, -1), 0.32],
        [(128, 541), (-1, -1), 0.72],
        # Right
		[(729, 506), (-2, 1), 0.32],
        [(896, 541), (-1, 1), 0.72],
		# Centre line
        [(512, 568), (-1, 0), 1]
	])
NORTHEAST = Heading(name='northeast', cardinal=False, bearing=45, offset=(-1,1),
    view_offsets=[
        [(480, 470), (-5, 4), 0.1], # L1
		[(108, 469), (-6, -1), 0.1], # L7
        [(544, 470), (-4, 5), 0.1], # R1
		[(916, 469), (1, 6), 0.1], # R7
        [(128, 469), (-6, 0), 0.125], # L6
        [(896, 469), (0, 6), 0.125], # R6
        [(179, 470), (-6, 1), 0.125], # L5
        [(845, 470), (-1, 6), 0.125], # L6
        [(266, 471), (-6, 2), 0.125], # L4
        [(758, 471), (-2, 6), 0.125], # L4
        [(92, 470), (-5, -1), 0.15], # L6
        [(932, 470), (1, 5), 0.15], # L6
        [(128, 472), (-5, 0), 0.15], # L5
        [(896, 472), (0, 5), 0.15], # R5
        [(196, 474), (-5, 1), 0.15], # L4
        [(828, 474), (-1, 5), 0.15], # R4
        [(306, 475), (-5, 2), 0.15], # L3
        [(718, 475), (-2, 5), 0.15], # R3
        [(415, 473), (-5, 3), 0.125], # L2
        [(609, 473), (-3, 5), 0.125], # R2
        [(512, 473), (-4, 4), 0.2], # Middle
		[(79, 473), (-4, -1), 0.225], # L5
        [(945, 473), (1, 4), 0.225], # R5
        [(128, 477), (-4, 0), 0.25], # L4
        [(896, 477), (0, 4), 0.25], # R4
        [(224, 480), (-4, 1,), 0.275], # L3
        [(800, 480), (-1, 4,), 0.275], # R3
        [(362, 479), (-4, 2), 0.25], # L2
        [(662, 479), (-2, 4), 0.25], # R2
        [(462, 475), (-4, 3), 0.275], # L1
        [(562, 475), (-3, 4), 0.275], # R1
        [(512, 479), (-3, 3), 0.3], # middle
		[(57, 479), (-3, -1), 0.325], # L4
        [(967, 479), (1, 3), 0.325], # R4
        [(128, 486), (-3, 0), 0.35], # L3
        [(896, 486), (0, 3), 0.35], # R3
        [(272, 490), (-3, 1), 0.375], # L2
        [(752, 490), (-1, 3), 0.375], # R2
        [(427, 485), (-3, 2), 0.375], # L1
        [(597, 485), (-2, 3), 0.375], # R1
        [(512, 493), (-2, 2), 0.45], # middle
		[(128, 507), (-2, 0), 0.5], # L2
        [(896, 507), (0, 2), 0.5], # R2
        [(349, 506), (-2, 1), 0.6], # L1
        [(675, 506), (-1, 2), 0.6], # R1
        [(512, 541), (-1, 1), 0.8], # middle
        [(128, 568), (-1, 0), 0.9], # L1
        [(896, 568), (0, 1), 0.9], # R1
    ])
EAST = Heading(name='east', cardinal=True, bearing=90, offset=(0,1),
    view_offsets=[
        [(512, 467), (0, 6), 0.1],
		# Left
		[(475, 469), (-1, 6), 0.1],
        [(402, 471), (-2, 6), 0.1],
        [(246, 474), (-3, 5), 0.1],
        [(170, 472), (-4, 5), 0.1],
        [(89, 470), (-5, 4), 0.1],
        [(28, 472), (-5, 3), 0.11],
		# Right
		[(548, 469), (1, 6), 0.1],
        [(621, 471), (2, 6), 0.1],
		[(777, 474), (3, 5), 0.1],
        [(853, 472), (4, 5), 0.1],
        [(934, 470), (5, 4), 0.1],
        [(995, 472), (5, 3), 0.11],
		# Centre
        [(512, 470), (0, 5), 0.12],
		# Left
		[(457, 473), (-1, 5), 0.11],
        [(356, 474), (-2, 5), 0.11],
        [(188, 476), (-3, 4), 0.13],
        [(128, 473), (-4, 4), 0.12],
        [(74, 474), (-4, 3), 0.14],
        # Right
		[(566, 473), (1, 5), 0.11],
        [(667, 474), (2, 5), 0.11],
        [(835, 476), (3, 4), 0.13],
        [(896, 473), (4, 4), 0.12],
        [(949, 474), (4, 3), 0.14],
        # Centre
		[(512, 475), (0, 4), 0.16],
		# Left
		[(427, 479), (-1, 4), 0.13],
        [(294, 480), (-2, 4), 0.14],
        [(128, 479), (-3, 3), 0.17],
        [(44, 483), (-3, 2), 0.22],
        # Right
		[(596, 479), (1, 4), 0.13],
        [(729, 480), (2, 4), 0.14],
        [(896, 479), (3, 3), 0.17],
        [(979, 483), (3, 2), 0.22],
		# Centre
		[(512, 484), (0, 3), 0.18],
        # Left
		[(376, 489), (-1, 3), 0.18],
        [(220, 486), (-2, 3), 0.18],
        [(128, 493), (-2, 2), 0.24],
        [(-42, 507), (-2, 1), 0.3],
        # Right
		[(647, 489), (1, 3), 0.18],
        [(803, 486), (2, 3), 0.18],
        [(896, 493), (2, 2), 0.24],
        [(1066, 507), (2, 1), 0.3],
		# Centre
		[(512, 506), (0, 2), 0.4],
        # Left
		[(294, 506), (-1, 2), 0.32],
        [(128, 541), (-1, 1), 0.72],
        # Right
		[(729, 506), (1, 2), 0.32],
        [(896, 541), (1, 1), 0.72],
		# Centre line
        [(512, 568), (0, 1), 1]
    ])
SOUTHEAST = Heading(name='southeast', cardinal=False, bearing=135, offset=(1,1),
    view_offsets=[
        [(512, 473), (4, 4), 0.2],
        [(512, 479), (3, 3), 0.3],
        [(512, 493), (2, 2), 0.5],
        [(512, 541), (1, 1), 0.9]
    ])
SOUTH = Heading(name='south', cardinal=True, bearing=180, offset=(1,0),
    view_offsets=[
        [(512, 467), (6, 0), 0.1],
		# Left
		[(475, 469), (6, 1), 0.1],
        [(402, 471), (6, 2), 0.1],
        [(246, 474), (5, 3), 0.1],
        [(170, 472), (5, 4), 0.1],
        [(89, 470), (4, 5), 0.1],
        [(28, 472), (3, 5), 0.11],
		# Right
		[(548, 469), (6, -1), 0.1],
        [(621, 471), (6, -2), 0.1],
		[(777, 474), (5, -3), 0.1],
        [(853, 472), (5, -4), 0.1],
        [(934, 470), (4, -5), 0.1],
        [(995, 472), (3, -5), 0.11],
		# Centre
        [(512, 470), (5, 0), 0.12],
		# Left
		[(457, 473), (5, 1), 0.11],
        [(356, 474), (5, 2), 0.11],
        [(188, 476), (4, 3), 0.13],
        [(128, 473), (4, 4), 0.12],
        [(74, 474), (3, 4), 0.14],
        # Right
		[(566, 473), (5, -1), 0.11],
        [(667, 474), (5, -2), 0.11],
        [(835, 476), (4, -3), 0.13],
        [(896, 473), (4, -4), 0.12],
        [(949, 474), (3, -4), 0.14],
        # Centre
		[(512, 475), (4, 0), 0.16],
        # Left
		[(427, 479), (4, 1), 0.13],
        [(294, 480), (4, 2), 0.14],
        [(128, 479), (3, 3), 0.17],
        [(44, 483), (2, 3), 0.22],
        # Right
		[(596, 479), (4, -1), 0.13],
        [(729, 480), (4, -2), 0.14],
        [(896, 479), (3, -3), 0.17],
        [(979, 483), (2, -3), 0.22],
		# Centre
		[(512, 484), (3, 0), 0.18],
        # Left
		[(376, 489), (3, 1), 0.18],
        [(220, 486), (3, 2), 0.18],
        [(128, 493), (2, 2), 0.24],
        [(-42, 507), (1, 2), 0.3],
        # Right
		[(647, 489), (3, -1), 0.18],
        [(803, 486), (3, -2), 0.18],
        [(896, 493), (2, -2), 0.24],
        [(1066, 507), (1, -2), 0.3],
		# Centre
		[(512, 506), (2, 0), 0.4],
        # Left
		[(294, 506), (2, 1), 0.32],
        [(128, 541), (1, 1), 0.72],
        # Right
		[(729, 506), (2, -1), 0.32],
        [(896, 541), (1, -1), 0.72],
		# Centre line
        [(512, 568), (1, 0), 1]
    ])
SOUTHWEST = Heading(name='southwest', cardinal=False, bearing=225, offset=(1,-1),
    view_offsets=[
        [(480, 470), (5, -4), 0.1], # L1
		[(108, 469), (6, 1), 0.1], # L7
        [(544, 470), (4, -5), 0.1], # R1
		[(916, 469), (-1, -6), 0.1], # R7
        [(128, 469), (6, 0), 0.125], # L6
        [(896, 469), (0, -6), 0.125], # R6
        [(179, 470), (6, -1), 0.125], # L5
        [(845, 470), (1, -6), 0.125], # L6
        [(266, 471), (6, -2), 0.125], # L4
        [(758, 471), (2, -6), 0.125], # L4
        [(92, 470), (5, 1), 0.15], # L6
        [(932, 470), (-1, -5), 0.15], # L6
        [(128, 472), (5, 0), 0.15], # L5
        [(896, 472), (0, -5), 0.15], # R5
        [(196, 474), (5, -1), 0.15], # L4
        [(828, 474), (1, -5), 0.15], # R4
        [(306, 475), (5, -2), 0.15], # L3
        [(718, 475), (2, -5), 0.15], # R3
        [(415, 473), (5, -3), 0.125], # L2
        [(609, 473), (3, -5), 0.125], # R2
        [(512, 473), (4, -4), 0.2], # Middle
		[(79, 473), (4, 1), 0.225], # L5
        [(945, 473), (-1, -4), 0.225], # R5
        [(128, 477), (4, 0), 0.25], # L4
        [(896, 477), (0, -4), 0.25], # R4
        [(224, 480), (4, -1), 0.275], # L3
        [(800, 480), (1, -4), 0.275], # R3
        [(362, 479), (4, -2), 0.25], # L2
        [(662, 479), (2, -4), 0.25], # R2
        [(462, 475), (4, -3), 0.275], # L1
        [(562, 475), (3, -4), 0.275], # R1
        [(512, 479), (3, -3), 0.3], # middle
		[(57, 479), (3, 1), 0.325], # L4
        [(967, 479), (-1, -3), 0.325], # R4
        [(128, 486), (3, 0), 0.35], # L3
        [(896, 486), (0, -3), 0.35], # R3
        [(272, 490), (3, -1), 0.375], # L2
        [(752, 490), (1, -3), 0.375], # R2
        [(427, 485), (3, -2), 0.375], # L1
        [(597, 485), (2, -3), 0.375], # R1
        [(512, 493), (2, -2), 0.45], # middle
		[(128, 507), (2, 0), 0.5], # L2
        [(896, 507), (0, -2), 0.5], # R2
        [(349, 506), (2, -1), 0.6], # L1
        [(675, 506), (1, -2), 0.6], # R1
        [(512, 541), (1, -1), 0.8], # middle
        [(128, 568), (1, 0), 0.9], # L1
        [(896, 568), (0, -1), 0.9], # R1
    ])
WEST = Heading(name='west', cardinal=True, bearing=270, offset=(0,-1),
    view_offsets=[
        [(512, 467), (0, -6), 0.1],
        # Left
        [(475, 469), (1, -6), 0.1],
        [(402, 471), (2, -6), 0.1],
        [(246, 474), (3, -5), 0.1],
        [(170, 472), (4, -5), 0.1],
        [(89, 470), (5, -4), 0.1],
        [(28, 472), (5, -3), 0.11],
        # Right
        [(548, 469), (-1, -6), 0.1],
        [(621, 471), (-2, -6), 0.1],
        [(777, 474), (-3, -5), 0.1],
        [(853, 472), (-4, -5), 0.1],
        [(934, 470), (-5, -4), 0.1],
        [(995, 472), (-5, -3), 0.11],
        # Centre
        [(512, 470), (0, -5), 0.12],
        # Left
        [(457, 473), (1, -5), 0.11],
        [(356, 474), (2, -5), 0.11],
        [(188, 476), (3, -4), 0.13],
        [(128, 473), (4, -4), 0.12],
        [(74, 474), (4, -3), 0.14],
        # Right
        [(566, 473), (-1, -5), 0.11],
        [(667, 474), (-2, -5), 0.11],
        [(835, 476), (-3, -4), 0.13],
        [(896, 473), (-4, -4), 0.12],
        [(949, 474), (-4, -3), 0.14],
        # Centre
        [(512, 475), (0, -4), 0.16],
        # Left
        [(427, 479), (1, -4), 0.13],
        [(294, 480), (2, -4), 0.14],
        [(128, 479), (3, -3), 0.17],
        [(44, 483), (3, -2), 0.22],
        # Right
        [(596, 479), (-1, -4), 0.13],
        [(729, 480), (-2, -4), 0.14],
        [(896, 479), (-3, -3), 0.17],
        [(979, 483), (-3, -2), 0.22],
        # Centre
        [(512, 484), (0, -3), 0.18],
        # Left
        [(376, 489), (1, -3), 0.18],
        [(220, 486), (2, -3), 0.18],
        [(128, 493), (2, -2), 0.24],
        [(-42, 507), (2, -1), 0.3],
        # Right
        [(647, 489), (-1, -3), 0.18],
        [(803, 486), (-2, -3), 0.18],
        [(896, 493), (-2, -2), 0.24],
        [(1066, 507), (-2, -1), 0.3],
        # Centre
        [(512, 506), (0, -2), 0.4],
        # Left
        [(294, 506), (1, -2), 0.32],
        [(128, 541), (1, -1), 0.72],
        # Right
        [(729, 506), (-1, -2), 0.32],
        [(896, 541), (-1, -1), 0.72],
        # Centre line
        [(512, 568), (0, -1), 1]
    ])
NORTHWEST = Heading(name='northwest', cardinal=False, bearing=315, offset=(-1,-1),
    view_offsets=[
        [(512, 473), (-4, -4), 0.2],
        [(512, 479), (-3, -3), 0.3],
        [(512, 493), (-2, -2), 0.5],
        [(512, 541), (-1, -1), 0.9]
    ])

# Define objects
MOONRING = Object(name='moonring')
DRAGONSLAYER = Object(name='dragonslayer')
WOLFSLAYER = Object(name='wolfslayer')

# Define monsters
WOLVES = Monster(name='wolves', hostile=True, image=os.path.join(IMG_PATH, 'wolf.png'))
DRAGONS = Monster(name='dragons', hostile=True, image=os.path.join(IMG_PATH, 'dragon.png'))
ICE_TROLLS = Monster(name='ice_trolls', hostile=True, image=os.path.join(IMG_PATH, 'ice_troll.png'))
SKULKRIN = Monster(name='skulkrin', hostile=True, image=os.path.join(IMG_PATH, 'skulkrin.png'))
WILD_HORSES = Monster(name='wild horses', hostile=False, image=os.path.join(IMG_PATH, 'horse.png'))

class DefaultGameData(GameData):
    '''A class to define all the additional data for a "default" game.
    You could mod the game by altering or subclassing this.
	TODO: move this game config out into an external file (e.g. JSON).
	Character stats reference: http://www.icemark.com/tower/charstats.htm
	Doomdark's regiments: http://www.icemark.com/tower/regiments.htm
    '''
    # Load the world from the external file into a dictionary.
    world = json.loads(open('data/world.json','r').readline())
    #world = json.loads(open('data/test_world.json','r').readline())
    # For each grid cell, replace the terrain_type with the correct terrain class.
    for row in world:
        for grid in row:
            grid['terrain_type'] = eval(grid['terrain_type'].upper())
    
    # Define initial player-controlled actors.
    luxor = Actor(location = (41,13),
    #luxor = Actor(location = (10,10),
        name = 'Luxor',
        title = 'the Moonprince',
        heading = NORTHEAST,
        #image
        #image_mounted
        mounted = True,
        heraldry = os.path.join(IMG_PATH, 'shield_luxor.png'),
        race = FREE)
    #morkin = Actor(location = (41,13),
    morkin = Actor(location = (10,10),
        name = 'Morkin',
        title = None,
        #image
        #image_mounted
        mounted = True,
        icefear = False,
        heraldry = os.path.join(IMG_PATH, 'shield_morkin.png'),
        race = HALF_FEY)
    #corleth = Actor(location = (41,13),
    corleth = Actor(location = (10,10),
        name = 'Corleth',
        title = 'the Fey',
        #image
        #image_mounted
        mounted = True,
        heraldry = os.path.join(IMG_PATH, 'shield_corleth.png'),
        race = FEY)
    #rorthron = Actor(location = (41,13),
    rorthron = Actor(location = (10,10),
        name = 'Rorthron',
        title = 'the Wise',
        #image
        #image_mounted
        mounted = True,
        heraldry = os.path.join(IMG_PATH, 'shield_rorthron.png'),
        race = WISE)
    def __init__(self, *args, **kwargs):
        self.cheatmode = kwargs.get('cheatmode') or False
        self.actors.append(self.luxor)
        self.actors.append(self.morkin)
        self.actors.append(self.corleth)
        self.actors.append(self.rorthron)
        # Initially selected actor.
        self.actor = self.luxor