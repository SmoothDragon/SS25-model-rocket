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
        [0, 91.2],
        [50.8, 91.2],
        [69.85, 120.3],
        [0, 120.3],
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
