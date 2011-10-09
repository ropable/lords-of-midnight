#!/usr/bin/python

import os
import json
from sys import path

PROJECT_PATH = path[0]
ASSET_PATH = PROJECT_PATH + os.sep + 'assets'
FONT_PATH = ASSET_PATH + os.sep + 'font'
FONT_BENG = FONT_PATH + os.sep + 'benguiat_book_bt.ttf'
IMG_PATH = ASSET_PATH + os.sep + 'img'
# Load the map from external file
MAP_JSON = json.loads(open('data/map.json','r').readline())

class Heading:
    '''
    This is a class for actor headings (facing direction).
    '''
    def __init__(self, name, bearing, offset):
        self.name = name
        self.bearing = bearing
        self.offset = offset
    
    def rotate_cw(self):
        if (self.bearing + 45) == 360:
            return '0'
        else:
            return str(self.bearing + 45)

    def rotate_ccw(self):
        if (self.bearing - 45) < 0:
            return '315'
        else:
            return str(self.bearing - 45)

# Define headings
NORTH = Heading('north', 0, (-1,0))
NORTHEAST = Heading('northeast', 45, (-1,1))
EAST = Heading('east', 90, (0,1))
SOUTHEAST = Heading('southeast', 135, (1,1))
SOUTH = Heading('south', 180, (1,0))
SOUTHWEST = Heading('southwest', 225, (1,-1)) 
WEST = Heading('west', 270, (0,-1))
NORTHWEST = Heading('northwest', 315, (-1,-1))
# Dictionary lookup for Heading classes
HEADINGS = {'0':NORTH,
    '45':NORTHEAST,
    '90':EAST,
    '135':SOUTHEAST,
    '180':SOUTH,
    '225':SOUTHWEST,
    '270':WEST,
    '315':NORTHWEST}

class Terrain:
    def __init__(self, terrain_type, move_cost=None, energy_cost=None, image=None):
        self.terrain_type = terrain_type
        self.move_cost = move_cost or 2
        self.energy_cost = energy_cost or 8
        self.image = image
        
    @property
    def name(self):
        return self.name.replace('_', ' ')

# Define terrain types
PLAINS = Terrain('plains')
MOUNTAINS = Terrain('mountains', 6, 64)
CITADEL = Terrain('citadel')
FOREST = Terrain('forest', 4, 12)
TOWER = Terrain('tower')
HENGE = Terrain('henge')
VILLAGE = Terrain('village')
DOWNS = Terrain('downs', 4, 16)
KEEP = Terrain('keep')
SNOWHALL = Terrain('snowhall')
LAKE = Terrain('lake')
WASTES = Terrain('frozen_wastes', 999)
RUIN = Terrain('ruin')
LITH = Terrain('lith')
CAVERN = Terrain('cavern')
TERRAIN = {'plains':PLAINS,
    'mountains':MOUNTAINS,
    'citadel':CITADEL,
    'forest':FOREST,
    'tower':TOWER,
    'henge':HENGE,
    'village':VILLAGE,
    'downs':DOWNS,
    'keep':KEEP,
    'snowhall':SNOWHALL,
    'lake':LAKE,
    'frozen_wastes':WASTES,
    'ruin':RUIN,
    'lith':LITH,
    'cavern':CAVERN}

class Object:
    pass

class Actor:
    def __init__(self, *args, **kwargs):
        self.name = kwargs.get('name') or 'Lord'
        self.location = kwargs.get('location') or (0,0) # A two-tuple coordinate (NOT x,y coords).
        self.energy = kwargs.get('energy') or 127 # Energy ranges between 0 and 127.
        self.health = kwargs.get('health') or 127 # Health level for a Lord ranges between 0 (dead) and 127 (full health).
        self.heading = kwargs.get('heading') or NORTH
        self.clock = kwargs.get('clock') or 6 # 6 AM is dawn, 6PM is twilight
        self.weapon = kwargs.get('weapon') or None
        self.mounted = kwargs.get('mounted') or False
        self.heraldry = kwargs.get('heraldry') or None
        self.race = kwargs.get('race') or None
    
    def location_desc(self):
        location_desc = 'He stands at {0}, looking {1} to {2}.'
        curent_location = MAP_JSON[self.location[0]][self.location[1]]
        offset = self.heading.offset
        facing_grid = (self.location[0] + offset[0], self.location[1] + offset[1])
        facing_location = MAP_JSON[facing_grid[0]][facing_grid[1]]
        # Still facing plains? Look further ahead.
        while facing_location.get('terrain_type') == 'plains':
            facing_grid = (facing_grid[0] + offset[0], facing_grid[1] + offset[1])
            facing_location = MAP_JSON[facing_grid[0]][facing_grid[1]]
        return location_desc.format(curent_location.get('name'), self.heading.name, facing_location.get('name'))
    
    def move(self):
        print('Started at {0}'.format(self.location))
        offset = self.heading.offset
        dest_type = MAP_JSON[self.location[0] + offset[0]][self.location[1] + offset[1]].get('terrain_type')
        dest_terrain = TERRAIN.get(dest_type)
        # Enough time left in the day to move?
        if self.mounted: # Being mounted halves the terrain move cost.
            move_cost = dest_terrain.move_cost / 2
        else:
            move_cost = dest_terrain.move_cost
        if self.clock + move_cost <= 18:
            # Enough energy left to move?
            if self.energy >= dest_terrain.energy_cost:
                # Set new location
                self.location = (self.location[0] + offset[0], self.location[1] + offset[1])
                self.clock += move_cost
                # Subtract energy cost
                self.energy -= dest_terrain.energy_cost
                print('Moved to {0}'.format(self.location))
            else:
                print('Not enough energy left.')
        else:
            print('Not enough hours left.')

class GameData:
    '''
    This class stores everything about a game in progress. 
    '''
    actors = [] # A list of all player-controllable actors.
    days_passed = 0 # Days passed since the start of the game.
    
    def __init__(self, *args, **kwargs):
        # Define actors
        self.luxor = Actor(name='Luxor the Moonprince', location=(41,13), mounted=True)
        self.actors.append(self.luxor)
        self.morkin = Actor(name='Morkin', location=(41,13), mounted=True)
        self.actors.append(self.morkin)
        self.corleth = Actor(name='Corleth the Fey', location=(41,13), mounted=True)
        self.actors.append(self.corleth)
        self.rorthron = Actor(name='Rorthron', location=(41,13), mounted=True)
        self.actors.append(self.rorthron)
        self.actor = kwargs.get('actor') or self.luxor