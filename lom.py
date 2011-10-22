#!/usr/bin/python
from __future__ import division

import os
import json
import pygame
from easypg import colours
from sys import path
from utils import aspect_scale

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
    def __init__(self, name, cardinal, bearing, offset, view_offsets):
        self.name = name
        self.cardinal = cardinal
        self.bearing = bearing
        self.offset = offset # Position offset of the square in front.
        self.view_offsets = view_offsets
    
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
NORTH = Heading('north', True, 0, (-1,0),
    [
     #[(-5,-4),(-4,-5),(4,-5),(5,-4)],
     #[(-5,-3),(-4,-4),(-3,-5),(-2,-6),(2,-6),(3,-5),(4,-4),(5,-3)],
     #[(-4,-3),(-3,-4),(-2,-5),(-1,-6),(1,-6),(2,-5),(3,-4),(4,-3)],
     #[(-3,-3),(-2,-4),(-1,-5),(0,-6),(1,-5),(2,-4),(3,-3)],
     #[(-3,-2),(-2,-3),(-1,-4),(0,-5),(1,-4),(2,-3),(3,-2)],
     #[(-2,-2),(-1,-3),(0,-4),(1,-3),(2,-2)],
     #[(-2,-1),(-1,-2),(0,-3),(1,-2),(2,-1)],
     #[(-1,-1),(0,-2),(1,-1)],
     [(-1,-1),(-1,0),(-1,1)]
    ])
NORTHEAST = Heading('northeast', False, 45, (-1,1),
    [
     #[(-1,-6),(0,-6),(1,-6),(2,-6),(6,-2),(6,-1),(6,0),(6,1)],
     #[(-1,-5),(0,-5),(1,-5),(2,-5),(3,-5),(4,-5),(5,-4),(5,-3),(5,-2),(5,-1),(5,0),(5,1)],
     #[(-1,-4),(0,-4),(1,-4),(2,-4),(3,-4),(4,-4),(4,-3),(4,-2),(4,-1),(4,0),(4,1)],
     #[(-1,-3),(0,-3),(1,-3),(2,-3),(3,-3),(3,-2),(3,-1),(3,0),(3,1)],
     #[(0,-2),(1,-2),(2,-2),(2,-1),(2,0)],
     [(-1,0),(-1,1),(0,1)]
    ])
EAST = Heading('east', True, 90, (0,1),
    [
     #[(4,-5),(5,-4),(5,4),(4,5)],
     #[(3,-5),(4,-4),(5,-3),(6,-2),(6,2),(5,3),(4,3),(3,5)],
     #[(3,-4),(4,-3),(5,-2),(6,-1),(6,1),(5,2),(4,3),(3,4)],
     #[(3,-3),(4,-2),(5,-1),(6,0),(5,-1),(4,2),(3,3)],
     #[(2,-3),(3,-2),(4,-1),(5,0),(4,1),(3,2),(2,3)],
     #[(2,-2),(3,-1),(4,0),(3,1),(2,2)],
     #[(1,-2),(2,-1),(3,0),(2,1),(1,2)],
     #[(1,-1),(2,0),(1,1)],
     [(-1,1),(0,1),(1,1)]
    ])
SOUTHEAST = Heading('southeast', False, 135, (1,1),
    [
     #[(-1,6),(0,6),(1,6),(2,6),(6,2),(6,1),(6,0),(6,-1)],
     #[(-1,5),(0,5),(1,5),(2,5),(3,5),(4,5),(5,4),(5,3),(5,2),(5,1),(5,0),(5,-1)],
     #[(-1,4),(0,4),(1,4),(2,4),(3,4),(4,4),(4,3),(4,2),(4,1),(4,0),(4,-1)],
     #[(-1,3),(0,3),(1,3),(2,3),(3,3),(3,2),(3,1),(3,0),(3,-1)],
     #[(0,2),(1,2),(2,2),(2,1),(2,0)],
     [(0,1),(1,1),(1,0)]
    ])
SOUTH = Heading('south', True, 180, (1,0),
    [
     #[(-5,4),(-4,5),(4,5),(5,4)],
     #[(-5,3),(-4,4),(-3,5),(-2,6),(2,6),(3,5),(4,4),(5,3)],
     #[(-4,3),(-3,4),(-2,5),(-1,6),(1,6),(2,5),(3,4),(4,3)],
     #[(-3,3),(-2,4),(-1,5),(0,6),(1,5),(2,4),(3,3)],
     #[(-3,2),(-2,3),(-1,4),(0,5),(1,4),(2,3),(3,2)],
     #[(-2,2),(-1,3),(0,4),(1,3),(2,2)],
     #[(-2,1),(-1,2),(0,3),(1,2),(2,1)],
     #[(-1,1),(0,2),(1,1)],
     [(1,1),(1,0),(1,-1)]
    ])
SOUTHWEST = Heading('southwest', False, 225, (1,-1),
    [
     #[(-6,-1),(-6,0),(-6,1),(-6,2),(-2,6),(-1,6),(0,6),(1,6)],
     #[(-5,-1),(-5,0),(-5,1),(-5,2),(-5,3),(-5,4),(-4,5),(-3,5),(-2,5),(-1,5),(0,5),(1,5)],
     #[(-4,-1),(-4,0),(-4,1),(-4,2),(-4,3),(-4,4),(-3,4),(-2,4),(-1,4),(0,4),(1,4)],
     #[(-3,-1),(-3,0),(-3,1),(-3,2),(-3,3),(-2,3),(-1,3),(0,-3),(1,3)],
     #[(-2,0),(-2,1),(-2,2),(-1,2),(0,2)],
     [(1,0),(1,-1),(0,-1)]
    ]) 
WEST = Heading('west', True, 270, (0,-1),
    [
     #[(-4,-5),(-5,-4),(-5,4),(-4,5)],
     #[(-3,-5),(-4,-4),(-5,-3),(-6,-2),(-6,2),(-5,3),(-4,3),(-3,5)],
     #[(-3,-4),(-4,-3),(-5,-2),(-6,-1),(-6,1),(-5,2),(-4,3),(-3,4)],
     #[(-3,-3),(-4,-2),(-5,-1),(-6,0),(-5,-1),(-4,2),(-3,3)],
     #[(-2,-3),(-3,-2),(-4,-1),(-5,0),(-4,1),(-3,2),(-2,3)],
     #[(-2,-2),(-3,-1),(-4,0),(-3,1),(-2,2)],
     #[(-1,-2),(-2,-1),(-3,0),(-2,1),(-1,2)],
     #[(-1,-1),(-2,0),(-1,1)],
     [(1,-1),(0,-1),(-1,-1)]
    ])
NORTHWEST = Heading('northwest', False, 315, (-1,-1),
    [
     #[(1,-6),(0,-6),(-1,-6),(-2,-6),(-6,-2),(-6,-1),(-6,0),(-6,1)],
     #[(1,-5),(0,-5),(-1,-5),(-2,-5),(-3,-5),(-4,-5),(-5,-4),(-5,-3),(-5,-2),(-5,-1),(-5,0),(-5,1)],
     #[(1,-4),(0,-4),(-1,-4),(-2,-4),(-3,-4),(-4,-4),(-4,-3),(-4,-2),(-4,-1),(-4,0),(-4,1)],
     #[(1,-3),(0,-3),(-1,-3),(-2,-3),(-3,-3),(-3,-2),(-3,-1),(-3,0),(-3,1)],
     #[(0,-2),(-1,-2),(-2,-2),(-2,-1),(-2,0)],
     [(0,-1),(-1,-1),(-1,0)]
    ])
# Dictionary lookup for the Heading classes.
HEADINGS = {'0':NORTH,
    '45':NORTHEAST,
    '90':EAST,
    '135':SOUTHEAST,
    '180':SOUTH,
    '225':SOUTHWEST,
    '270':WEST,
    '315':NORTHWEST}

class Terrain:
    def __init__(self, terrain_type, image=None, move_cost=None, energy_cost=None):
        self.terrain_type = terrain_type
        self.image = image
        self.move_cost = move_cost or 2
        self.energy_cost = energy_cost or 8
        
    @property
    def name(self):
        return self.name.replace('_', ' ')

# Define terrain types
PLAINS = Terrain('plains', os.path.join(IMG_PATH, 'terrain_plains.png'))
MOUNTAINS = Terrain('mountains', os.path.join(IMG_PATH, 'terrain_mountains.png'), 6, 64)
CITADEL = Terrain('citadel', os.path.join(IMG_PATH, 'terrain_citadel.png'))
FOREST = Terrain('forest', os.path.join(IMG_PATH, 'terrain_forest.png'), 4, 12)
TOWER = Terrain('tower', os.path.join(IMG_PATH, 'terrain_tower.png'))
HENGE = Terrain('henge', os.path.join(IMG_PATH, 'terrain_henge.png'))
VILLAGE = Terrain('village', os.path.join(IMG_PATH, 'terrain_village.png'))
DOWNS = Terrain('downs', os.path.join(IMG_PATH, 'terrain_downs.png'), 4, 16)
KEEP = Terrain('keep', os.path.join(IMG_PATH, 'terrain_keep.png'))
SNOWHALL = Terrain('snowhall', os.path.join(IMG_PATH, 'terrain_snowhall.png'))
LAKE = Terrain('lake', os.path.join(IMG_PATH, 'terrain_lake.png'))
WASTES = Terrain('frozen_wastes', os.path.join(IMG_PATH, 'terrain_wastes.png'), 999)
RUIN = Terrain('ruin', os.path.join(IMG_PATH, 'terrain_ruin.png'))
LITH = Terrain('lith', os.path.join(IMG_PATH, 'terrain_lith.png'))
CAVERN = Terrain('cavern', os.path.join(IMG_PATH, 'terrain_cavern.png'))
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
        self.icefear = kwargs.get('icefear') or 0 
    
    def location_desc(self):
        location_desc = 'He stands at {0}, looking {1} to {2}.'
        current_location = MAP_JSON[self.location[0]][self.location[1]]
        offset = self.heading.offset
        facing_grid = (self.location[0] + offset[0], self.location[1] + offset[1])
        facing_location = MAP_JSON[facing_grid[0]][facing_grid[1]]
        # Still facing plains? Look further ahead.
        while facing_location.get('terrain_type') == 'plains':
            facing_grid = (facing_grid[0] + offset[0], facing_grid[1] + offset[1])
            facing_location = MAP_JSON[facing_grid[0]][facing_grid[1]]
        return location_desc.format(current_location.get('name'), self.heading.name, facing_location.get('name'))
    
    def move(self, cheating=False):
        print('Started at {0}'.format(self.location))
        offset = self.heading.offset
        dest_type = MAP_JSON[self.location[0] + offset[0]][self.location[1] + offset[1]].get('terrain_type')
        dest_terrain = TERRAIN.get(dest_type)
        if dest_terrain == WASTES:
            # Actor can't move into Frozen Wastes, even if cheating.
            return
        # Enough time left in the day to move?
        if self.mounted: # Being mounted halves the terrain move cost.
            move_cost = dest_terrain.move_cost / 2
        else:
            move_cost = dest_terrain.move_cost
        if cheating:
            # If we're cheating, we can move as far as we want with no energy cost.
            self.location = (self.location[0] + offset[0], self.location[1] + offset[1])
            print('Moved to {0}'.format(self.location))
        else:
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

    def render_perspective(self, screen):
        # Take the Actor's position and heading, and build the list of terrain pieces to render.
        rows_count = len(self.heading.view_offsets)
        y = 50 # Top of the grid.
        #print('Facing: {0}'.format(self.heading.name))
        #print('Current coords: {0}'.format(self.location))
        current_location = MAP_JSON[self.location[0]][self.location[1]]
        #print(current_location)
        for row in self.heading.view_offsets:
            x = 0
            for offset in row:
                offset_grid = (self.location[0] + offset[0], self.location[1] + offset[1])
                # Off the edge of the map? Terrain == Frozen Wastes
                #print('Facing coords: {0}'.format(offset_grid))
                if offset_grid[0] < 0 or offset_grid[0] > 62 or offset_grid[1] < 0 or offset_grid[1] > 66:
                    terrain = WASTES
                else:
                    offset_location = MAP_JSON[offset_grid[0]][offset_grid[1]]
                    #print(offset_location)
                    terrain = TERRAIN[offset_location.get('terrain_type')]
                    #print(terrain.terrain_type)
                terrain_img = pygame.image.load(terrain.image).convert_alpha() # Returns the image as a surface.
                #terrain_img = pygame.transform.scale(terrain_img,(20,20))
                terrain_img = aspect_scale(terrain_img, (100,60))
                screen.blit(terrain_img, (x, y))
                x += 100
            y += 60
        
        #downs_path = os.path.join(lom.IMG_PATH, 'terrain_downs.png')
        #downs_img = pygame.image.load(downs_path).convert_alpha()
        #downs_img_size = (downs_img.get_size())
        #downs_img_sml = pygame.transform.scale(downs_img, (int(downs_img_size[0]*0.7), int(downs_img_size[1]*0.7)))
    
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
