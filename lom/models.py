#!/usr/bin/python
from __future__ import division, print_function, unicode_literals
import pygame
import constants
import utils


class Heading:
    # This is a class for actor/army headings (facing direction).
    def __init__(self, name, cardinal, bearing, offset, view_offsets):
        self.name = name
        self.cardinal = cardinal
        self.bearing = bearing
        self.offset = offset # Position offset of the square in front.
        self.view_offsets = view_offsets

class Terrain:
    def __init__(self, terrain_type, image=None, move_cost=None, energy_cost=None):
        self.terrain_type = terrain_type
        self.image = image
        self.move_cost = move_cost or 1 # Base move cost is one hour (when mounted).
        self.energy_cost = energy_cost or 8
        
    @property
    def name(self):
        return self.name.replace('_', ' ')

class Object:
    def __init__(self, *args, **kwargs):
        self.name = kwargs.get('name')

class Monster:
    def __init__(self, *args, **kwargs):
        self.name = kwargs.get('name')
        self.hostile = kwargs.get('hostile') or True
        self.image = kwargs.get('image')
        self.strength = kwargs.get('strength')
        self.bane = kwargs.get('bane') # Is there an "auto-kill" object for this monster?
        
class Race:
    def __init__(self, *args, **kwargs):
        self.name = kwargs.get('name')
        # TODO: Add more racial attributes.

class Actor:
    def __init__(self, *args, **kwargs):
        self.location = kwargs.get('location') # A two-tuple coordinate (NOT x,y coords) of current grid location.
        self.heading = kwargs.get('heading') or constants.NORTH
        self.time = kwargs.get('time') or 8 # 8 AM is dawn.
        self.name = kwargs.get('name')
        self.title = kwargs.get('title')
        self.image = kwargs.get('image')
        self.image_mounted = kwargs.get('image_mounted')
        self.strength = kwargs.get('strength')
        self.energy = kwargs.get('energy') or 127 # Energy ranges between 0 and 127.
        self.health = kwargs.get('health') or 127 # Health level for a Lord ranges between 0 (dead) and 127 (full health).
        self.weapon = kwargs.get('weapon') or None
        self.mounted = kwargs.get('mounted') or True
        self.heraldry = kwargs.get('heraldry') or None
        self.race = kwargs.get('race') or None
        self.icefear = kwargs.get('icefear') or 1 # Set to False if Actor is immune to the Ice Fear.

    def rotate_cw(self):
        # Alters the Actor's bearing and heading by 45 degrees clockwise.
        headings = {'0':constants.NORTH, '45':constants.NORTHEAST, '90':constants.EAST,
                    '135':constants.SOUTHEAST, '180':constants.SOUTH, '225':constants.SOUTHWEST,
                    '270':constants.WEST, '315':constants.NORTHWEST}
        bearing = self.heading.bearing
        if bearing + 45 == 360:
            bearing = 0
        else:
            bearing += 45
        self.heading = headings[str(bearing)]
        
    def rotate_ccw(self):
        # Alters the Actor's bearing and heading by 45 degrees counterclockwise.
        headings = {'0':constants.NORTH, '45':constants.NORTHEAST, '90':constants.EAST,
                    '135':constants.SOUTHEAST, '180':constants.SOUTH, '225':constants.SOUTHWEST,
                    '270':constants.WEST, '315':constants.NORTHWEST}
        bearing = self.heading.bearing
        if bearing - 45 < 0:
            bearing = 315
        else:
            bearing -= 45
        self.heading = headings[str(bearing)]
        
    def location_desc(self, world):
        '''
        Returns a string description of where the Actor is standing, plus what they are looking at.
        '''
        location_desc = 'He stands at {0}, looking {1} to {2}.'
        current_location = world[self.location[0]][self.location[1]]
        offset = self.heading.offset
        facing_grid = (self.location[0] + offset[0], self.location[1] + offset[1])
        facing_location = world[facing_grid[0]][facing_grid[1]]
        # Still facing plains? Look further ahead.
        # TODO: only look three squares ahead.
        while facing_location.get('terrain_type') == constants.PLAINS:
            facing_grid = (facing_grid[0] + offset[0], facing_grid[1] + offset[1])
            facing_location = world[facing_grid[0]][facing_grid[1]]
        return location_desc.format(current_location.get('name'), self.heading.name,
            facing_location.get('name'))

    def clock_energy_desc(self, gamedata):
        '''
        Returns a description of the Actor's current time and energy level.
        '''
        energy_desc = ''
        if self.time == gamedata.dawn:
            message = 'It is dawn and {0} is {1}'
        elif self.time >= gamedata.nightfall:
            message = 'It is night and {0} is {1}'
        else:
            message = '{0} hours of the day remain and {1} is {2}'
        # Energy levels range between 0 and 128.
        # Utterly invigorated 128
        # Very invigorated
		# Somewhat invigorated
        # Invigorated
        return 'message'
        
    def move(self, gamedata):
        #print('Started at {0}'.format(self.location))
        offset = self.heading.offset
        dest_terrain = gamedata.world[self.location[0] + offset[0]][self.location[1] + offset[1]].get('terrain_type')
        #print(dest_terrain.terrain_type)
        if dest_terrain == constants.FROZEN_WASTES:
            # Actor can't move into Frozen Wastes, even if cheating.
            return
        # Can't move at night, even if cheating.
        if self.time >= gamedata.nightfall:
            return
        # Enough time left in the day to move?
        # Travelling on foot doubles the terrain move cost.
        if not self.mounted:
            move_cost = dest_terrain.move_cost * 2
        else:
            move_cost = dest_terrain.move_cost
        # Moving in one of the intercardinal directions adds 40% to move cost.
        if not self.heading.cardinal:
            move_cost = move_cost * 1.4
        if gamedata.cheatmode:
            # If we're cheating, we can move as far as we want with no energy cost.
            self.location = (self.location[0] + offset[0], self.location[1] + offset[1])
        else:
            if self.time + move_cost <= gamedata.nightfall:
                # Enough energy left to move?
                if self.energy >= dest_terrain.energy_cost:
                    # Set new location
                    self.location = (self.location[0] + offset[0], self.location[1] + offset[1])
                    self.time += move_cost
                    # Subtract energy cost
                    self.energy -= dest_terrain.energy_cost
                else:
                    print('Not enough energy left.')
            else:
                print('Not enough hours left.')
        #print('Moved to {0}'.format(self.location))
        #print('Time: {0}'.format(self.time))

    def render_perspective(self, world, screen):
        world_rows = len(world)
        world_cols = len(world[0])
        offset = self.heading.offset
        for node in self.heading.view_offsets:
            # If we're off the edge of the map, terrain == FROZEN_WASTES
            if self.location[0] + node[1][0] < 0 or self.location[0] + node[1][0] >= world_rows:
                terrain = constants.FROZEN_WASTES
            elif self.location[1] + node[1][1] < 0 or self.location[1] + node[1][1] >= world_cols:
                terrain = constants.FROZEN_WASTES
            else:
                location = world[self.location[0] + node[1][0]][self.location[1] + node[1][1]]
                terrain = location.get('terrain_type')
            # TODO: if terrain == PLAINS and there's an army present, draw it.
            if terrain.image:
                terrain_img = pygame.image.load(terrain.image).convert_alpha()
                # Scale the image
                img_x = terrain_img.get_width() * node[2]
                img_y = terrain_img.get_height() * node[2]
                terrain_img = utils.aspect_scale(terrain_img, (img_x,img_y))
                x = node[0][0] - (terrain_img.get_width()/2)
                y = node[0][1] - terrain_img.get_height()
                screen.blit(terrain_img, (x,y))
        # Check the facing direction for monsters, wild horses, armies, or other lords.
        facing_coord = (self.location[0] + offset[0], self.location[1] + offset[1])
        facing_location = world[facing_coord[0]][facing_coord[1]]
        if facing_location.get('monster'):
            monster = eval('constants.' + facing_location.get('monster').upper())
            monster_img = pygame.image.load(monster.image).convert_alpha()
            blit_y = (constants.SCREENSIZE[1] - monster_img.get_height())
            screen.blit(monster_img, (500,blit_y))

class GameData:
    '''
    This class stores everything about a game in progress. 
    '''
    world = None # A list of lists, each containing a number of dictionaries (one for each node).
    actor = None # Currently-selected actors
    actors = [] # A list of all player-controllable actors.
    npcs = [] # A list of NPC actors.
    game_days = 0 # Days passed since the start of the game.
    cheatmode = False
    dawn = 8 # 8AM is dawn.
    nightfall = 16 # 4PM is nightfall. The sun sure sets early here!
