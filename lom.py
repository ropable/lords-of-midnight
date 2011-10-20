#!/usr/bin/python
from __future__ import division

import os
import json
import pygame
from easypg import colours
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
     [(-5,-4),(-4,-5),(4,-5),(5,-4)],
     [(-5,-3),(-4,-4),(-3,-5),(-2,-6),(2,-6),(3,-5),(4,-4),(5,-3)],
     [(-4,-3),(-3,-4),(-2,-5),(-1,-6),(1,-6),(2,-5),(3,-4),(4,-3)],
     [(-3,-3),(-2,-4),(-1,-5),(0,-6),(1,-5),(2,-4),(3,-3)],
     [(-3,-2),(-2,-3),(-1,-4),(0,-5),(1,-4),(2,-3),(3,-2)],
     [(-2,-2),(-1,-3),(0,-4),(1,-3),(2,-2)],
     [(-2,-1),(-1,-2),(0,-3),(1,-2),(2,-1)],
     [(-1,-1),(0,-2),(1,-1)],
     [(0,-1)]
    ])
NORTHEAST = Heading('northeast', False, 45, (-1,1),
    [
     [(-1,-6),(0,-6),(1,-6),(2,-6),(6,-2),(6,-1),(6,0),(6,1)],
     [(-1,-5),(0,-5),(1,-5),(2,-5),(3,-5),(4,-5),(5,-4),(5,-3),(5,-2),(5,-1),(5,0),(5,1)],
     [(-1,-4),(0,-4),(1,-4),(2,-4),(3,-4),(4,-4),(4,-3),(4,-2),(4,-1),(4,0),(4,1)],
     [(-1,-3),(0,-3),(1,-3),(2,-3),(3,-3),(3,-2),(3,-1),(3,0),(3,1)],
     [(0,-2),(1,-2),(2,-2),(2,-1),(2,0)],
     [(0,-1),(1,-1),(1,0)]
    ])
EAST = Heading('east', True, 90, (0,1),
    [
     [(4,-5),(5,-4),(5,4),(4,5)],
     [(3,-5),(4,-4),(5,-3),(6,-2),(6,2),(5,3),(4,3),(3,5)],
     [(3,-4),(4,-3),(5,-2),(6,-1),(6,1),(5,2),(4,3),(3,4)],
     [(3,-3),(4,-2),(5,-1),(6,0),(5,-1),(4,2),(3,3)],
     [(2,-3),(3,-2),(4,-1),(5,0),(4,1),(3,2),(2,3)],
     [(2,-2),(3,-1),(4,0),(3,1),(2,2)],
     [(1,-2),(2,-1),(3,0),(2,1),(1,2)],
     [(1,-1),(2,0),(1,1)],
     [(1,0)]
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
     [(-5,4),(-4,5),(4,5),(5,4)],
     [(-5,3),(-4,4),(-3,5),(-2,6),(2,6),(3,5),(4,4),(5,3)],
     [(-4,3),(-3,4),(-2,5),(-1,6),(1,6),(2,5),(3,4),(4,3)],
     [(-3,3),(-2,4),(-1,5),(0,6),(1,5),(2,4),(3,3)],
     [(-3,2),(-2,3),(-1,4),(0,5),(1,4),(2,3),(3,2)],
     [(-2,2),(-1,3),(0,4),(1,3),(2,2)],
     [(-2,1),(-1,2),(0,3),(1,2),(2,1)],
     [(-1,1),(0,2),(1,1)],
     [(0,1)]
    ])
SOUTHWEST = Heading('southwest', False, 225, (1,-1),
    [
     [(-6,-1),(-6,0),(-6,1),(-6,2),(-2,6),(-1,6),(0,6),(1,6)],
     [(-5,-1),(-5,0),(-5,1),(-5,2),(-5,3),(-5,4),(-4,5),(-3,5),(-2,5),(-1,5),(0,5),(1,5)],
     [(-4,-1),(-4,0),(-4,1),(-4,2),(-4,3),(-4,4),(-3,4),(-2,4),(-1,4),(0,4),(1,4)],
     [(-3,-1),(-3,0),(-3,1),(-3,2),(-3,3),(-2,3),(-1,3),(0,-3),(1,3)],
     [(-2,0),(-2,1),(-2,2),(-1,2),(0,2)],
     [(-1,0),(-1,1),(0,1)]
    ]) 
WEST = Heading('west', True, 270, (0,-1),
    [
     [(-4,-5),(-5,-4),(-5,4),(-4,5)],
     [(-3,-5),(-4,-4),(-5,-3),(-6,-2),(-6,2),(-5,3),(-4,3),(-3,5)],
     [(-3,-4),(-4,-3),(-5,-2),(-6,-1),(-6,1),(-5,2),(-4,3),(-3,4)],
     [(-3,-3),(-4,-2),(-5,-1),(-6,0),(-5,-1),(-4,2),(-3,3)],
     [(-2,-3),(-3,-2),(-4,-1),(-5,0),(-4,1),(-3,2),(-2,3)],
     [(-2,-2),(-3,-1),(-4,0),(-3,1),(-2,2)],
     [(-1,-2),(-2,-1),(-3,0),(-2,1),(-1,2)],
     [(-1,-1),(-2,0),(-1,1)],
     [(-1,0)]
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
MOUNTAINS = Terrain('mountains', 6, 64, os.path.join(IMG_PATH, 'terrain_mountains.png'))
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
        self.icefear = kwargs.get('icefear') or 0 
    
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
    
    def move(self, cheating=False):
        print('Started at {0}'.format(self.location))
        offset = self.heading.offset
        dest_type = MAP_JSON[self.location[0] + offset[0]][self.location[1] + offset[1]].get('terrain_type')
        dest_terrain = TERRAIN.get(dest_type)
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

    def render_panorama(self):
        # Take the Actor's position and heading, and build the list of terrain pieces to render.
        for row in self.heading.view_offsets:
            for offset in row:
                 offset_grid = (self.location[0] + offset[0], self.location[1] + offset[1])
                 # Off the edge of the map? Terrain == Frozen Wastes
                 if offset_grid[0] < 0 or offset_grid[0] > 62 or offset_grid[1] < 0 or offset_grid[1] > 66:
                     terrain = WASTES
                 else:
                     offset_location = MAP_JSON[offset_grid[0]][offset_grid[1]]
                     terrain = TERRAIN[offset_location.get('terrain_type')]
                 print(terrain.terrain_type)
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

def drawpoints(cardinal=True, grids=False, screen=None):
    vp1 = (512, 466) # Couple of pixels above the horizon
    vp2 = (128, 462) # Slightly lower.
    vp3 = (896, 462)
    # Don't use these anymore, but keep for reference.
    if cardinal:
        sp1 = [-4608,-3072,-1792,-768,0,512,1024,1792,2816,4096] # Midpoint: 512
        sp2 = [-768,-256,128,512,1024,1792,2816,4096,5632] # Midpoint: 128
        sp3 = [-3072,-1792,-768,0,512,896,1280,1792] #Midpoint: 896
    else:
        sp1 = [-4992,-3456,-2176,-1152,-384,128,512,896,1408,2176,3200,4480,6016] # Midpoint: 512
        sp2 = [-1152,-384,128,640,1408,2432,3712,5248,7040] # Midpoint: 128
        sp3 = [-4224,-2688,-1408,-384,384,896,1408,2176] #Midpoint: 896
    if grids:
        pass
        #for i in sp1:
        #    pygame.draw.line(screen, colours.aqua, (i, 568), vp1, 1)            
        #for i in sp2:
        #    pygame.draw.line(screen, colours.red, (i, 568), vp2, 1)
        #for i in sp3:
        #    pygame.draw.line(screen, colours.green, (i, 568), vp3, 1)
        #pygame.draw.line(screen, colours.green, (-4992, 568), vp1, 1)
        #pygame.draw.line(screen, colours.green, vp2, (896,568), 1)
    intercardinal_points = [
        [
            getIntersectPoint(p1=vp1, p2=(-4992,568), p3=vp2, p4=(-384,568)),
            getIntersectPoint(p1=vp1, p2=(-4992,568), p3=vp2, p4=(128,568)),
            getIntersectPoint(p1=vp1, p2=(-4992,568), p3=vp2, p4=(640,568)),
            getIntersectPoint(p1=vp1, p2=(-4992,568), p3=vp2, p4=(1408,568)),
            getIntersectPoint(p1=vp1, p2=(6016,568), p3=vp3, p4=(-384,568)),
            getIntersectPoint(p1=vp1, p2=(6016,568), p3=vp3, p4=(384,568)),
            getIntersectPoint(p1=vp1, p2=(6016,568), p3=vp3, p4=(896,568)),
            getIntersectPoint(p1=vp1, p2=(6016,568), p3=vp3, p4=(1408,568)),
            
        ],
        [
            getIntersectPoint(p1=vp1, p2=(-3456,568), p3=vp2, p4=(-384,568)),
            getIntersectPoint(p1=vp1, p2=(-3456,568), p3=vp2, p4=(128,568)),
            getIntersectPoint(p1=vp1, p2=(-3456,568), p3=vp2, p4=(640,568)),
            getIntersectPoint(p1=vp1, p2=(-3456,568), p3=vp2, p4=(1408,568)),
            getIntersectPoint(p1=vp1, p2=(-3456,568), p3=vp2, p4=(2432,568)),
            getIntersectPoint(p1=vp1, p2=(-3456,568), p3=vp2, p4=(3712,568)),
            getIntersectPoint(p1=vp1, p2=(4480,568), p3=vp3, p4=(-2688,568)),
            getIntersectPoint(p1=vp1, p2=(4480,568), p3=vp3, p4=(-1408,568)),
            getIntersectPoint(p1=vp1, p2=(4480,568), p3=vp3, p4=(-384,568)),
            getIntersectPoint(p1=vp1, p2=(4480,568), p3=vp3, p4=(384,568)),
            getIntersectPoint(p1=vp1, p2=(4480,568), p3=vp3, p4=(896,568)),
            getIntersectPoint(p1=vp1, p2=(4480,568), p3=vp3, p4=(1408,568))
        ],
        [
            #getIntersectPoint(p1=vp1, p2=(-768,568), p3=vp2, p4=(896,568)),
            #getIntersectPoint(p1=vp1, p2=(0,568), p3=vp2, p4=(1408,568)),
            #getIntersectPoint(p1=vp1, p2=(512,568), p3=vp2, p4=(2432,568)),
            #getIntersectPoint(p1=vp1, p2=(1024,568), p3=vp3, p4=(-384,568)),
            #getIntersectPoint(p1=vp1, p2=(1792,568), p3=vp3, p4=(384,568)),
            #getIntersectPoint(p1=vp1, p2=(2816,568), p3=vp3, p4=(896,568))
        ],
        [
            #getIntersectPoint(p1=vp1, p2=(-4608,568), p3=vp2, p4=(-1152,568)),
            #getIntersectPoint(p1=vp1, p2=(-3072,568), p3=vp2, p4=(-384,568)),
            #getIntersectPoint(p1=vp1, p2=(-1792,568), p3=vp2, p4=(128,568)),
            #getIntersectPoint(p1=vp1, p2=(-768,568), p3=vp2, p4=(512,568)),
            #getIntersectPoint(p1=vp1, p2=(0,568), p3=vp2, p4=(896,568)),
            getIntersectPoint(p1=vp1, p2=(512,568), p3=vp2, p4=(1408,568)),
            #getIntersectPoint(p1=vp1, p2=(1024,568), p3=vp3, p4=(0,568)),
            #getIntersectPoint(p1=vp1, p2=(1792,568), p3=vp3, p4=(512,568)),
            #getIntersectPoint(p1=vp1, p2=(2816,568), p3=vp3, p4=(896,568)),
            #getIntersectPoint(p1=vp1, p2=(4096,568), p3=vp3, p4=(1280,568)),
            #getIntersectPoint(p1=vp1, p2=(5632,568), p3=vp3, p4=(1792,568)),
        ],
        [
            #getIntersectPoint(p1=vp1, p2=(-3072,568), p3=vp2, p4=(-1152,568)),
            #getIntersectPoint(p1=vp1, p2=(-1792,568), p3=vp2, p4=(-384,568)),
            #getIntersectPoint(p1=vp1, p2=(-768,568), p3=vp2, p4=(128,568)),
            #getIntersectPoint(p1=vp1, p2=(0,568), p3=vp2, p4=(512,568)),
            getIntersectPoint(p1=vp1, p2=(512,568), p3=vp2, p4=(640,568)),
            #getIntersectPoint(p1=vp1, p2=(1024,568), p3=vp3, p4=(512,568)),
            #getIntersectPoint(p1=vp1, p2=(1792,568), p3=vp3, p4=(896,568)),
            #getIntersectPoint(p1=vp1, p2=(2816,568), p3=vp3, p4=(1280,568)),
            #getIntersectPoint(p1=vp1, p2=(4096,568), p3=vp3, p4=(1792,568)),
        ],
        [
            #getIntersectPoint(p1=vp1, p2=(128,568), p3=vp2, p4=(128,568)),
            #getIntersectPoint(p1=vp1, p2=(896,568), p3=vp3, p4=(896,568)),
        ]
    ]
    
    cardinal_points = [
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
    if cardinal:
        return cardinal_points
    else:
        return intercardinal_points