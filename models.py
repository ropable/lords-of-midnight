#!/usr/bin/python
from __future__ import division, print_function, unicode_literals

import os
import json
import pygame

import lom_data
from utils import aspect_scale

class Heading:
    # This is a class for actor/army headings (facing direction).
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
    pass

class Race:
    def __init__(self, *args, **kwargs):
        self.name = kwargs.get('name')
        # TODO: Add more racial attributes.

class Actor:
    def __init__(self, *args, **kwargs):
        self.name = kwargs.get('name')
        self.title = kwargs.get('title')
        self.location = kwargs.get('location') # A two-tuple coordinate (NOT x,y coords).
        self.energy = kwargs.get('energy') or 127 # Energy ranges between 0 and 127.
        self.health = kwargs.get('health') or 127 # Health level for a Lord ranges between 0 (dead) and 127 (full health).
        self.heading = kwargs.get('heading') or lom_data.NORTH
        self.bearing = kwargs.get('bearing') or 0
        self.clock = kwargs.get('clock') or 8 # 8 AM is dawn.
        self.weapon = kwargs.get('weapon') or None
        self.mounted = kwargs.get('mounted') or True
        self.heraldry = kwargs.get('heraldry') or None
        self.race = kwargs.get('race') or None
        self.icefear = kwargs.get('icefear') or 1 # Set to False if Actor is immune to the Ice Fear.

    def rotate_cw(self):
        # Alters the Actor's bearing and heading by 45 degrees clockwise.
        headings = {'0':lom_data.NORTH, '45':lom_data.NORTHEAST, '90':lom_data.EAST,
                    '135':lom_data.SOUTHEAST, '180':lom_data.SOUTH, '225':lom_data.SOUTHWEST,
                    '270':lom_data.WEST, '315':lom_data.NORTHWEST}
        if (self.bearing + 45) == 360:
            self.bearing = 0
        else:
            self.bearing = self.bearing + 45
        self.heading = headings[str(self.bearing)]
        
    def rotate_ccw(self):
        # Alters the Actor's bearing and heading by 45 degrees counterclockwise.
        headings = {'0':lom_data.NORTH, '45':lom_data.NORTHEAST, '90':lom_data.EAST,
                    '135':lom_data.SOUTHEAST, '180':lom_data.SOUTH, '225':lom_data.SOUTHWEST,
                    '270':lom_data.WEST, '315':lom_data.NORTHWEST}
        if (self.bearing - 45) < 0:
            self.bearing = 315
        else:
            self.bearing = self.bearing - 45
        self.heading = headings[str(self.bearing)]
        
    def location_desc(self, map):
        '''
        Returns a string description of where the Actor is standing, plus what they are looking at.
        '''
        location_desc = 'He stands at {0}, looking {1} to {2}.'
        current_location = map[self.location[0]][self.location[1]]
        offset = self.heading.offset
        facing_grid = (self.location[0] + offset[0], self.location[1] + offset[1])
        facing_location = map[facing_grid[0]][facing_grid[1]]
        # Still facing plains? Look further ahead.
        while facing_location.get('terrain_type') == 'plains':
            facing_grid = (facing_grid[0] + offset[0], facing_grid[1] + offset[1])
            facing_location = map[facing_grid[0]][facing_grid[1]]
        return location_desc.format(current_location.get('name'), self.heading.name,
            facing_location.get('name'))

    def clock_energy_desc(self, gamedata):
        '''
        Returns a description of the Actor's current time and energy level.
        '''
        energy_desc = ''
        if self.clock == gamedata.dawn:
            message = 'It is dawn and {0} is {1}'
        elif self.clock >= gamedata.nightfall:
            message = 'It is night and {0} is {1}'
        else:
            message = '{0} hours of the day remain and {1} is {2}'
        # Energy levels range between 0 and 128.
        # Utterly invigorated 128
        # Very invigorated
        # 
        return 'message'
        
    def move(self, gamedata):
        #import lom_data
        print('Started at {0}'.format(self.location))
        offset = self.heading.offset
        dest_terrain = gamedata.map[self.location[0] + offset[0]][self.location[1] + offset[1]].get('terrain_type')
        if dest_terrain.terrain_type == 'frozen_wastes':
            # Actor can't move into Frozen Wastes, even if cheating.
            return
        # Can't move at night, even if cheating.
        if self.clock >= gamedata.nightfall:
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
            if self.clock + move_cost <= gamedata.nightfall:
                # Enough energy left to move?
                if self.energy >= dest_terrain.energy_cost:
                    # Set new location
                    self.location = (self.location[0] + offset[0], self.location[1] + offset[1])
                    self.clock += move_cost
                    # Subtract energy cost
                    self.energy -= dest_terrain.energy_cost
                else:
                    print('Not enough energy left.')
            else:
                print('Not enough hours left.')
        #print('Moved to {0}'.format(self.location))
        #print('Time: {0}'.format(self.clock))

    def render_perspective(self, map, screen):
        # Take the Actor's position and heading, and build the list of terrain pieces to render.
        rows_count = len(self.heading.view_offsets)
        y = 50 # Top of the grid.
        #print('Facing: {0}'.format(self.heading.name))
        #print('Current coords: {0}'.format(self.location))
        current_location = map[self.location[0]][self.location[1]]
        #print(current_location)
        for row in self.heading.view_offsets:
            x = 0
            for offset in row:
                offset_grid = (self.location[0] + offset[0], self.location[1] + offset[1])
                # Off the edge of the map? Terrain == Frozen Wastes
                #print('Facing coords: {0}'.format(offset_grid))
                if offset_grid[0] < 0 or offset_grid[0] > 62 or offset_grid[1] < 0 or offset_grid[1] > 66:
                    terrain = wastes
                else:
                    offset_location = map[offset_grid[0]][offset_grid[1]]
                    #print(offset_location)
                    terrain = eval(offset_location.get('terrain_type'))
                    #print(terrain.terrain_type)
                if terrain.image:
                    terrain_img = pygame.image.load(terrain.image).convert_alpha() # Returns the image as a surface.
                    #terrain_img = pygame.transform.scale(terrain_img,(20,20))
                    terrain_img = aspect_scale(terrain_img, (100,60))
                    screen.blit(terrain_img, (x, y))
                else: # Plains
                    pass
                x += 100
            y += 60

class GameData:
    '''
    This class stores everything about a game in progress. 
    '''
    map = None # A list of lists, each containing a number of dictionaries (one for each map tile).
    actor = None # Currently-selected actors
    actors = [] # A list of all player-controllable actors.
    npcs = [] # A list of NPC actors.
    game_days = 0 # Days passed since the start of the game.
    cheatmode = False
    dawn = 8 # 8AM is dawn.
    nightfall = 16 # 4PM is nightfall. The sun sure sets early here!
