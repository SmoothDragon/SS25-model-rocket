#!/usr/bin/env python3

'''
LowerSabot	
Component1	
z (mm)	r (mm)
0	98.7
10	98.7
10	105.7
25	105.7
25	102.2
30	102.2
30	120.8
0	120.8
0	98.7


Component2	
z (mm)	r (mm)
0	102.8
50.8	102.8
63.6	120.8
0	120.8
'''

from solid import *
from solid.utils import *


def parseArguments():
    # Argument parsing
    import argparse
    parser = argparse.ArgumentParser(
        description='Generate SCAD for half Sierpinski cube.')
    parser.add_argument('--size', action='store', default='50', dest='size',
        type=int, help='Piece thickness (in millimeters)')
    parser.add_argument('-n', action='store', default='8', dest='fn',
        type=int, help='Curvature parameter. Number of sides on circle.')
    # Internet wisdom .15mm
    # Nate Paystrup .10mm
    parser.add_argument('-t', action='store', default='0.10', dest='tolerance',
        type=float, help='Tolerance gap (in millimeters)')
    return parser.parse_args()


def buildCrossSection(cutSize=1000):
    points = [ 
        [0, 98.7],
        [10, 98.7],
        [10, 105.7],
        [25, 105.7],
        [25, 102.2],
        [30, 102.2],
        [30, 120.8],
        [0, 120.8],
        [0, 98.7],
    ]
    cross_section = polygon(points=points)
    cross_section = rotate([0,0,90])(cross_section)
    cut_plane = translate([0,cutSize/2,0])(cube([cutSize]*3, center=True))
    final = rotate_extrude(segments=256)(cross_section)
    final = intersection()(final, cut_plane)
    return final





if __name__ == '__main__':
    args = parseArguments()

    final = buildCrossSection()

    print(scad_render(final, file_header=f'$fn={args.fn};'))
