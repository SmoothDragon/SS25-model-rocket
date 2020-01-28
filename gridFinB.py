#!/usr/bin/env python3

'''

UpperSabot	
Component1	
z (mm)	r (mm)
0	107.0
10	107.0
10	112.0
20	112.0
20	107.0
30	105.0
41	103.1
76.2	101.1
76.2	120.3
0	120.3
0	107.0


Component2	
z (mm)	r (mm)
0	91.2
50.8	91.2
69.85	120.3
0	120.3
'''
from solid import *
from solid.utils import *

def grid(fin_width, fin_spacing, fin_height, fin_length):
    slat = cube([fin_width, fin_length, fin_height], center=True)
    slats = slat + rotate([0,0,90])(slat)
    for i in range(4):
        shift = (-2)**(i-1) * fin_spacing
        slats = union()(slats, translate([shift, shift, 0])(slats))
    return slats


def grid(fin_width, fin_spacing, fin_height, n:'iterations'):
    limit = fin_spacing * 2**(n+1)
    slat = cube([fin_width, limit, fin_height], center=True)
    slats = slat + rotate([0,0,90])(slat)
    for i in range(n):
        shift = (-2)**(i) * fin_spacing
        slats = union()(slats, translate([shift, shift, 0])(slats))
    return slats

def gridFinTwo(grid, strut_width, strut_height, strut_length, crossRail_length):
    gridY = (5-1.25-1.125)
    strut_Yshift = 25.4 * (2.5-(gridY/2+1.125))
    gridY *= 25.4
    block = cube([crossRail_length, gridY, strut_height], center=True)
    grid = rotate([0,0,45])(grid)
    block = intersection()(block, grid)
    strut = cube([strut_width, strut_length, strut_height], center=True)
    # block = union()(block, translate([-(crossRail_length-strut_width)/2, strut_Yshift, 0])(strut))
    # block = union()(block, translate([(crossRail_length-strut_width)/2, strut_Yshift, 0])(strut))
    strut = cube([crossRail_length, strut_width, strut_height], center=True)
    block = union()(block, translate([0, (gridY-strut_width)/2, 0])(strut))
    block = union()(block, translate([0, -(gridY-strut_width)/2, 0])(strut))
    points = [(0,0), (0,.3), (.3,.5), (5,.5), (5,.3), (3.75,.1), (1.125,.1), (1.125,0)]
    points = [(25.4*x, 25.4*y) for x,y in points]
    side = polygon(points=points)
    hole = circle(d=25.4*11/64)
    hole = translate([.4375*25.4,.25*25.4])(hole)
    side = side - hole
    side = linear_extrude(height=strut_width, center=True, convexity=10)(side)
    side = rotate([90, 0, 90])(side)
    side = translate([0, -gridY/2-25.4*1.125, -(.25+.05)*25.4])(side)
    block = union()(block, translate([(crossRail_length-strut_width)/2, 0, 0])(side))
    block = union()(block, translate([-(crossRail_length-strut_width)/2, 0, 0])(side))
    block = rotate([0,180,0])(block)
    # Add support angle
    support_x = .875 * 25.4
    support_y = .4375 * 25.4
    support = cube([support_x, strut_width, strut_height])
    support_shear = [
        [1,0,0,-crossRail_length/2],
        [support_y/support_x,1,0],
        [0,0,1,0],
        [0,0,0,1],
        ]
    support = multmatrix(m=support_shear)(support)
    support = translate([0,-gridY/2-support_y,-strut_height/2])(support)
    block += support
    block += rotate([0,180,0])(support)
    return block


if __name__ == '__main__':
    fin_spacing = 25.4 * .3125 * .85
    fin_thickness = 25.4 * .0625
    fin_height = 25.4 * .4
    strut_thickness = 25.4 * .093
    strut_height = 25.4 * .4
    strut_width = 25.4 * .093
    strut_length = 25.4 * 5
    side_strut_length = 25.4 * 2.9375

    extGrid = grid(fin_thickness/2, fin_spacing, fin_height, 5)
    fin2 = gridFinTwo(extGrid, strut_width, strut_height, strut_length, side_strut_length) 
    final = fin2

    # print(scad_render(final, file_header=f'$fn={args.fn};'))
    fn = 64
    print(scad_render(final, file_header=f'$fn={fn};'))
