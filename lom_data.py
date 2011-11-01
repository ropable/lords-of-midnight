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
NORTH = Heading(name='north',
    cardinal=True,
    bearing=0,
    offset=(-1,0), 
    view_offsets=[
        #(draw coords, offset, scale]
        [(512, 469), (-6, 0), 0.1], # Furthest
        [(512, 472), (-5, 0), 0.2],
        [(512, 477), (-4, 0), 0.3],
        [(512, 486), (-3, 0), 0.4],
        [(512, 507), (-2, 0), 0.6],
        [(512, 568), (-1, 0), 1.0]  # Closest
    ])
NORTHEAST = Heading(name='northeast',
    cardinal=False,
    bearing=45,
    offset=(-1,1),
    view_offsets=[
        [(512, 473), (-4, 4), 0.2],
        [(512, 479), (-3, 3), 0.3],
        [(512, 493), (-2, 2), 0.5],
        [(512, 541), (-1, 1), 0.9]
    ])
EAST = Heading('east', True, 90, (0,1),
    view_offsets=[
        #(draw coords, offset, scale]
        [(512, 469), (0, 6), 0.1], # Furthest
        [(512, 472), (0, 5), 0.2],
        [(512, 477), (0, 4), 0.3],
        [(512, 486), (0, 3), 0.4],
        [(512, 507), (0, 2), 0.6],
        [(512, 568), (0, 1), 1.0]  # Closest
    ])
SOUTHEAST = Heading('southeast', False, 135, (1,1),
    view_offsets=[
        [(512, 473), (4, 4), 0.2],
        [(512, 479), (3, 3), 0.3],
        [(512, 493), (2, 2), 0.5],
        [(512, 541), (1, 1), 0.9]
    ])
SOUTH = Heading('south', True, 180, (1,0),
    view_offsets=[
        #(draw coords, offset, scale]
        [(512, 469), (6, 0), 0.1], # Furthest
        [(512, 472), (5, 0), 0.2],
        [(512, 477), (4, 0), 0.3],
        [(512, 486), (3, 0), 0.4],
        [(512, 507), (2, 0), 0.6],
        [(512, 568), (1, 0), 1.0]  # Closest
    ])
SOUTHWEST = Heading('southwest', False, 225, (1,-1),
    view_offsets=[
        [(512, 473), (4, -4), 0.2],
        [(512, 479), (3, -3), 0.3],
        [(512, 493), (2, -2), 0.5],
        [(512, 541), (1, -1), 0.9]
    ]) 
WEST = Heading('west', True, 270, (0,-1),
    view_offsets=[
        #(draw coords, offset, scale]
        [(512, 469), (0, -6), 0.1], # Furthest
        [(512, 472), (0, -5), 0.2],
        [(512, 477), (0, -4), 0.3],
        [(512, 486), (0, -3), 0.4],
        [(512, 507), (0, -2), 0.6],
        [(512, 568), (0, -1), 1.0]  # Closest
    ])
NORTHWEST = Heading('northwest', False, 315, (-1,-1),
    view_offsets=[
        [(512, 473), (-4, -4), 0.2],
        [(512, 479), (-3, -3), 0.3],
        [(512, 493), (-2, -2), 0.5],
        [(512, 541), (-1, -1), 0.9]
    ])

# Define objects

# Define monsters
WOLVES = Monster(name = 'wolves',
    hostile = True,
    image = os.path.join(IMG_PATH, 'wolf.png'))
DRAGONS = Monster(name = 'dragons',
    hostile = True,
    image = os.path.join(IMG_PATH, 'dragon.png'))
ICE_TROLLS = Monster(name = 'ice_trolls',
    hostile = True,
    image = os.path.join(IMG_PATH, 'ice_troll.png'))
SKULKRIN = Monster(name = 'skulkrin',
    hostile = True,
    image = os.path.join(IMG_PATH, 'skulkrin.png'))
WILD_HORSES = Monster(name='wild horses',
    hostile=False,
    image = os.path.join(IMG_PATH, 'horse.png'))

class DefaultGameData(GameData):
    '''A class to define all the additional data for a "default" game.
    You could mod the game by altering or subclassing this.
    '''
    # Load the world from the external file into a dictionary.
    world = json.loads(open('data/world.json','r').readline())
    # For each grid cell, replace the terrain_type with the correct terrain class.
    for row in world:
        for grid in row:
            grid['terrain_type'] = eval(grid['terrain_type'].upper())
    
    # Define initial player-controlled actors.
    luxor = Actor(location = (41,13),
        name = 'Luxor',
        title = 'the Moonprince',
        #image
        #image_mounted
        mounted = True,
        heraldry = os.path.join(IMG_PATH, 'shield_luxor.png'),
        race = FREE)
    morkin = Actor(location = (41,13),
        name = 'Morkin',
        title = None,
        #image
        #image_mounted
        mounted = True,
        icefear = False,
        heraldry = os.path.join(IMG_PATH, 'shield_morkin.png'),
        race = HALF_FEY)
    corleth = Actor(location = (41,13),
        name = 'Corleth',
        title = 'the Fey',
        #image
        #image_mounted
        mounted = True,
        heraldry = os.path.join(IMG_PATH, 'shield_corleth.png'),
        race = FEY)
    rorthron = Actor(location = (41,13),
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