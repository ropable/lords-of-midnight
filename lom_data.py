#!/usr/bin/python
from __future__ import division, print_function, unicode_literals

import os
import json
from sys import path

from models import Heading, Terrain, Object, Race, Actor, GameData

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
MOUNTAINS = Terrain('mountains', os.path.join(IMG_PATH, 'terrain_mountains.png'), 5.5, 64)
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
# A note about offsets: due to how the map data is stored (rows of columns),
# these offsets are NOT X,Y!
# Rather the opposite: (a,-b) means to move one row down (-Y) and one column left (-X). 
NORTH = Heading('north', True, 0, (-1,0), 
    [
     [(-4,-5),(-5,-4),(-5,4),(-4,5)],
     [(-3,-5),(-4,-4),(-5,-3),(-6,-2),(-6,2),(-5,3),(-4,4),(-3,5)],
     [(-3,-4),(-4,-3),(-5,-2),(-6,-1),(-6,1),(-5,2),(-4,3),(-3,4)],
     [(-3,-3),(-4,-2),(-5,-1),(-6,0),(-5,1),(-4,2),(-3,3)],
     [(-2,-3),(-3,-2),(-4,-1),(-5,0),(-4,1),(-3,2),(-2,3)],
     [(-2,-2),(-3,-1),(-4,0),(-3,1),(-2,2)],
     [(-1,-2),(-2,-1),(-3,0),(-2,1),(-1,2)],
     [(-1,-1),(-2,0),(-1,1)],
     [(-1,0)]
    ])
NORTHEAST = Heading('northeast', False, 45, (-1,1),
    [
     [(-6,-1),(-6,0),(-6,1),(-6,2),(-2,6),(-1,6),(0,6),(1,6)],
     [(-5,-1),(-5,0),(-5,1),(-5,2),(-5,3),(-5,4),(-4,5),(-3,5),(-2,5),(-1,5),(0,5),(1,5)],
     [(-4,-1),(-4,0),(-4,1),(-4,2),(-4,3),(-4,4),(-3,4),(-2,4),(-1,4),(0,4),(1,4)],
     [(-3,-1),(-3,0),(-3,1),(-3,2),(-3,3),(-2,3),(-1,3),(0,3),(1,3)],
     [(-2,0),(-2,1),(-2,2),(-1,2),(0,2)],
     [(-1,0),(-1,1),(0,1)]
    ])
EAST = Heading('east', True, 90, (0,1),
    [
     [(-5,4),(-4,5),(4,5),(5,4)],
     [(-5,3),(-4,4),(-3,5),(-2,6),(2,6),(3,5),(4,4),(5,3)],
     [(-4,3),(-3,4),(-2,5),(-1,6),(1,6),(2,5),(3,4),(4,3)],
     [(-3,3),(-2,4),(-1,5),(0,6),(1,5),(2,4),(3,3)],
     [(-3,2),(-2,3),(-1,4),(0,5),(1,4),(2,3),(3,2)],
     [(-2,2),(-1,3),(0,4),(1,3),(2,2)],
     [(-2,1),(-1,2),(0,3),(1,2),(2,1)],
     [(-1,1),(0,1),(1,1)],
     [(0,1)]
    ])
SOUTHEAST = Heading('southeast', False, 135, (1,1),
    [
     [(-1,6),(0,6),(1,6),(2,6),(6,2),(6,1),(6,0),(6,-1)],
     [(-1,5),(0,5),(1,5),(2,5),(3,5),(4,5),(5,4),(5,3),(5,2),(5,1),(5,0),(5,-1)],
     [(-1,4),(0,4),(1,4),(2,4),(3,4),(4,4),(4,3),(4,2),(4,1),(4,0),(4,-1)],
     [(-1,3),(0,3),(1,3),(2,3),(3,3),(3,2),(3,1),(3,0),(3,-1)],
     [(0,2),(1,2),(2,2),(2,1),(2,0)],
     [(0,1),(1,1),(1,0)]
    ])
SOUTH = Heading('south', True, 180, (1,0),
    [
     [(4,5),(5,4),(5,-4),(4,-5)],
     [(3,5),(4,4),(5,3),(6,2),(6,-2),(5,-3),(4,-4),(3,-5)],
     [(3,4),(4,3),(5,2),(6,1),(6,-1),(5,-2),(4,-3),(3,-4)],
     [(3,3),(4,2),(5,1),(6,0),(5,-1),(4,-2),(3,-3)],
     [(2,3),(3,2),(4,1),(5,0),(4,-1),(3,-2),(2,-3)],
     [(2,2),(3,1),(4,0),(3,-1),(2,-2)],
     [(1,2),(2,1),(3,0),(2,-1),(1,-2)],
     [(1,1),(2,0),(1,-1)],
     [(1,0)]
    ])
SOUTHWEST = Heading('southwest', False, 225, (1,-1),
    [
     [(6,1),(6,0),(6,-1),(6,-2),(2,-6),(1,-6),(0,-6),(-1,-6)],
     [(5,1),(5,0),(5,-1),(5,-2),(5,-3),(5,-4),(4,-5),(3,-5),(2,-5),(1,-5),(0,-5),(-1,-5)],
     [(4,1),(4,0),(4,-1),(4,-2),(4,-3),(4,-4),(3,-4),(2,-4),(1,-4),(0,-4),(-1,-4)],
     [(3,1),(3,0),(3,-1),(3,-2),(3,-3),(2,-3),(1,-3),(0,-3),(-1,-3)],
     [(2,0),(2,-1),(2,-2),(1,-2),(0,-2)],
     [(1,0),(1,-1),(0,-1)]
    ]) 
WEST = Heading('west', True, 270, (0,-1),
    [
     [(5,-4),(4,-5),(-4,-5),(-5,-4)],
     [(5,-3),(4,-4),(3,-5),(2,-6),(-2,-6),(-3,-5),(-4,-4),(-5,-3)],
     [(4,-3),(3,-4),(2,-5),(1,-6),(-1,-6),(-2,-5),(-3,-4),(-4,-3)],
     [(3,-3),(2,-4),(1,-5),(0,-6),(-1,-5),(-2,-4),(-3,-3)],
     [(3,-2),(2,-3),(1,-4),(0,-5),(-1,-4),(-2,-3),(-3,-2)],
     [(2,-2),(1,-3),(0,-4),(-1,-3),(-2,-2)],
     [(2,-1),(1,-2),(0,-3),(-1,-2),(-2,-1)],
     [(1,-1),(0,-1),(-1,-1)],
     [(0,-1)]
    ])
NORTHWEST = Heading('northwest', False, 315, (-1,-1),
    [
     [(1,-6),(0,-6),(-1,-6),(-2,-6),(-6,-2),(-6,-1),(-6,0),(-6,1)],
     [(1,-5),(0,-5),(-1,-5),(-2,-5),(-3,-5),(-4,-5),(-5,-4),(-5,-3),(-5,-2),(-5,-1),(-5,0),(-5,1)],
     [(1,-4),(0,-4),(-1,-4),(-2,-4),(-3,-4),(-4,-4),(-4,-3),(-4,-2),(-4,-1),(-4,0),(-4,1)],
     [(1,-3),(0,-3),(-1,-3),(-2,-3),(-3,-3),(-3,-2),(-3,-1),(-3,0),(-3,1)],
     [(0,-2),(-1,-2),(-2,-2),(-2,-1),(-2,0)],
     [(0,-1),(-1,-1),(-1,0)]
    ])

class DefaultGameData(GameData):
    '''
    A class to define all the additional data for a "default" game.
    You could mod the game by altering or subclassing this.
    '''
    # Load the map from the external file into a dictionary.
    map = json.loads(open('data/map.json','r').readline())
    # For each grid cell, replace the terrain_type with the correct terrain class.
    for row in map:
        for grid in row:
            grid['terrain_type'] = eval(grid['terrain_type'].upper())
    
    # Define initial player-controlled actors.
    luxor = Actor(
        name = 'Luxor the Moonprince',
        location = (41,13),
        mounted = True,
        heraldry = os.path.join(IMG_PATH, 'shield_luxor.png'),
        race = FREE)
    morkin = Actor(
        name = 'Morkin',
        location = (41,13),
        mounted = True,
        icefear = False,
        heraldry = os.path.join(IMG_PATH, 'shield_morkin.png'),
        race = HALF_FEY)
    corleth = Actor(
        name='Corleth the Fey',
        location=(41,13),
        mounted=True,
        heraldry=os.path.join(IMG_PATH, 'shield_corleth.png'),
        race = FEY)
    rorthron = Actor(
        name='Rorthron',
        location=(41,13),
        mounted=True,
        heraldry=os.path.join(IMG_PATH, 'shield_rorthron.png'),
        race = WISE)
     
    def __init__(self, *args, **kwargs):
        self.cheatmode = kwargs.get('cheatmode') or False
        self.actors.append(self.luxor)
        self.actors.append(self.morkin)
        self.actors.append(self.corleth)
        self.actors.append(self.rorthron)
        # Initially selected actor.
        self.actor = self.luxor