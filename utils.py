#!/usr/bin/python
from __future__ import division, print_function, unicode_literals

import pygame
import json

def edit_map_json(row, col, key, value):
    '''
    Convenience method to edit the JSON map data file.
    '''
    if not isinstance(row, int) or not isinstance(col, int):
        raise AssertionError('Row/column must be integer values.')
    # Load the map from the external file
    map = open('data/map.json','r')
    map_json = json.loads(map.readline())
    map.close()
    map_json[row][col][str(key)] = str(value)
    map = open('data/map.json','w')
    map.write(json.dumps(map_json))
    map.close()

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
