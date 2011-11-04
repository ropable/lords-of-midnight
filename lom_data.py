#!/usr/bin/python
from __future__ import division, print_function, unicode_literals

import os
import json
from sys import path

from models import Heading, Terrain, Object, Monster, Race, Actor, GameData

PROJECT_PATH = path[0]
ASSET_PATH = PROJECT_PATH + os.sep + 'assets'
FONT_PATH = ASSET_PATH + os.sep + 'font'
FONT_BENG = FONT_PATH + os.sep + 'benguiat_book_bt.ttf'
IMG_PATH = ASSET_PATH + os.sep + 'img'
SCREENSIZE = (1024, 768)

# Define races
FREE = Race('free')
FOUL = Race('foul')
FEY = Race('fey')
HALF_FEY = Race('half_fey') # He's special: half-human, half-fey.
TARG = Race('targ')
WISE = Race('wise')
SKULKRIN = Race('skulkrin')
DRAGON = Race('')

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

# Define headings.
# A note about offsets: due to how the world data is stored (rows of columns),
# these offsets are NOT X,Y!
# Rather the opposite: (a,-b) means to move one row down (-Y) and one column left (-X). 
NORTH = Heading(name='north', cardinal=True, bearing=0, offset=(-1,0), 
    view_offsets=[
        # A list of lists; precalculated screen draw coords (x,y), location offsets and image scale.
        # This is the order in which terrain pieces are drawn to the screen (furtherest first). 
        #(draw coords, offset, scale]
        # First drawing curve.
        [(402, 469), (-6, -1), 0.1], # Left arc
        [(324, 471), (-6, -2), 0.1],
        [(246, 474), (-5, -3), 0.1],
        [(170, 472), (-5, -4), 0.1],
        [(89, 470), (-4, -5), 0.1],
        [(28, 472), (-3, -5), 0.1],
        [(621, 469), (-6, 1), 0.1], # Right arc
        [(699, 471), (-6, 2), 0.1],
        [(777, 474), (-5, 3), 0.1],
        [(853, 472), (-5, 4), 0.1],
        [(934, 470), (-4, 5), 0.1],
        [(995, 472), (-3, 5), 0.1],
        [(512, 470), (-6, 0), 0.1], # Centre
        #
        #[(512, 470), (-5, 0), 0.12],
        
        #[(188, 476), (-4, -3), 0.08],
        #[(128, 473), (-4, -4), 0.08],
        #[(74, 474), (-3, -4), 0.08],
        
        #[(835, 476), (-4, 3), 0.08],
        #[(896, 473), (-4, 4), 0.08],
        #[(949, 474), (-3, 4), 0.08],
        #
        #[(128, 479), (-3, -3),0.2],
        #[(44, 483), (-2, -3), 0.2],
        
        #[(896, 479), (-3, 3),0.2],
        #[(979, 483), (-2, 3),0.2],
        #
        
    ])
NORTHEAST = Heading(name='northeast', cardinal=False, bearing=45, offset=(-1,1),
    view_offsets=[
        [(512, 473), (-4, 4), 0.2],
        [(512, 479), (-3, 3), 0.3],
        [(512, 493), (-2, 2), 0.5],
        [(512, 541), (-1, 1), 0.9]
    ])
EAST = Heading(name='east', cardinal=True, bearing=90, offset=(0,1),
    view_offsets=[
        [(512, 469), (0, 6), 0.1],
        [(512, 472), (0, 5), 0.2],
        [(512, 477), (0, 4), 0.3],
        [(512, 486), (0, 3), 0.4],
        [(512, 507), (0, 2), 0.6],
        [(512, 568), (0, 1), 1.0]
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
        [(512, 469), (6, 0), 0.1],
        [(512, 472), (5, 0), 0.2],
        [(512, 477), (4, 0), 0.3],
        [(512, 486), (3, 0), 0.4],
        [(512, 507), (2, 0), 0.6],
        [(512, 568), (1, 0), 1.0]
    ])
SOUTHWEST = Heading(name='southwest', cardinal=False, bearing=225, offset=(1,-1),
    view_offsets=[
        [(512, 473), (4, -4), 0.2],
        [(512, 479), (3, -3), 0.3],
        [(512, 493), (2, -2), 0.5],
        [(512, 541), (1, -1), 0.9]
    ]) 
WEST = Heading(name='west', cardinal=True, bearing=270, offset=(0,-1),
    view_offsets=[
        [(512, 469), (0, -6), 0.1],
        [(512, 472), (0, -5), 0.2],
        [(512, 477), (0, -4), 0.3],
        [(512, 486), (0, -3), 0.4],
        [(512, 507), (0, -2), 0.6],
        [(512, 568), (0, -1), 1.0]
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
    '''
    # Load the world from the external file into a dictionary.
    #world = json.loads(open('data/world.json','r').readline())
    world = json.loads(open('data/test_world.json','r').readline())
    # For each grid cell, replace the terrain_type with the correct terrain class.
    for row in world:
        for grid in row:
            grid['terrain_type'] = eval(grid['terrain_type'].upper())
    
    # Define initial player-controlled actors.
    #luxor = Actor(location = (41,13),
    luxor = Actor(location = (10,10),
        name = 'Luxor',
        title = 'the Moonprince',
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