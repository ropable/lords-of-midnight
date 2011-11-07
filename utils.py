#!/usr/bin/python
from __future__ import division, print_function, unicode_literals

import pygame
import json
from easypg import colours

def edit_world_json(row, col, key, value):
    '''
    Convenience method to edit the JSON world data file.
    '''
    if not isinstance(row, int) or not isinstance(col, int):
        raise AssertionError('Row/column must be integer values.')
    # Load the world from the external file
    world = open('data/world.json','r')
    map_json = json.loads(world.readline())
    world.close()
    map_json[row][col][str(key)] = str(value)
    world = open('data/world.json','w')
    world.write(json.dumps(map_json))
    world.close()

def aspect_scale(img,(bx,by)):
    '''
    Source: http://www.pygame.org/pcr/transform_scale/index.php
    Scales a pygame surface to fit into box bx/by.
    This method will retain the original image's aspect ratio.
    '''
    ix,iy = img.get_size()
    if ix > iy:
        # fit to width
        scale_factor = bx/float(ix)
        sy = scale_factor * iy
        if sy > by:
            scale_factor = by/float(iy)
            sx = scale_factor * ix
            sy = by
        else:
            sx = bx
    else:
        # fit to height
        scale_factor = by/float(iy)
        sx = scale_factor * ix
        if sx > bx:
            scale_factor = bx/float(ix)
            sx = bx
            sy = scale_factor * iy
        else:
            sy = by

    return pygame.transform.scale(img, (int(sx),int(sy)))

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
                assert False
        return (int(x),int(y))
    else:
        return None

def draw_grids(cardinal=True, grids=False, screen=None):
    vp1 = (512, 462) # Couple of pixels above the horizon
    vp2 = (128, 460)
    vp3 = (896, 460)
    # Don't use these anymore, but keep for reference.
    if cardinal:
        sp1 = [-4608,-3072,-1792,-768,0,512,1024,1792,2816,4096,5632] # Midpoint: 512
        sp2 = [-768,-256,128,512,1024,1792,2816,4096,5632] # Midpoint: 128
        sp3 = [-3072,-1792,-768,0,512,896,1280,1792] #Midpoint: 896
    else:
        sp1 = [-4992,-3456,-2176,-1152,-384,128,512,896,1408,2176,3200,4480,6016] # Midpoint: 512
        sp2 = [-256,128,640,1408,2432,3712] # Midpoint: 128
        sp3 = [-2688,-1408,-384,384,896,1408] #Midpoint: 896
    if grids:
        for i in sp1:
            pygame.draw.line(screen, colours.aqua, (i, 568), vp1, 1)            
        for i in sp2:
            pygame.draw.line(screen, colours.red, (i, 568), vp2, 1)
        for i in sp3:
            pygame.draw.line(screen, colours.green, (i, 568), vp3, 1)
        #pygame.draw.line(screen, colours.green, (-4992, 568), vp1, 1)
        #pygame.draw.line(screen, colours.green, vp2, (896,568), 1)
    if cardinal:
        intersects = [
            getIntersectPoint(p1=(512,462), p2=(-3072,568), p3=(128,460), p4=(4096,568)),
            #getIntersectPoint(p1=(512,462), p2=(1024,568), p3=(896,460), p4=(-3072,568)),
        ]
    else:
        intersects = [
            getIntersectPoint(p1=(512,462), p2=(512,568), p3=(128,462), p4=(3712,568)),
            getIntersectPoint(p1=(512,462), p2=(512,568), p3=(128,462), p4=(2432,568)),
            getIntersectPoint(p1=(512,462), p2=(512,568), p3=(128,462), p4=(1408,568)),
            getIntersectPoint(p1=(512,462), p2=(512,568), p3=(128,462), p4=(640,568))                        
            ]
    print(intersects)

if __name__ == '__main__':
    draw_grids(cardinal=True)