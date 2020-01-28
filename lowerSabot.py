#!/usr/bin/env python3

'''
Upper sabot	
z (mm)	r (mm)
317.5	92.1
95.3	104.7
73.0	108.8
50.8	108.8
44.5	106.5
9.5	104.7
0.0	104.7
0.0	123.8
317.5	123.8
362.0	123.8
342.9	92.1
317.5	92.1


Lower sabot	
z (mm)	r (mm)
6.4	107.3
20.6	107.3
20.6	105.3
22.2	105.3
22.2	117.5
161.9	117.5
174.6	110.3
190.5	110.3
209.6	104.5
266.7	104.5
268.3	103.7
292.1	103.7
304.8	123.8
0.0	123.8
0.0	99.3
6.4	99.3
6.4	107.3

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
        [6.4, 107.3],
        [20.6, 107.3],
        [20.6, 105.3],
        [22.2, 105.3],
        [22.2, 117.5],
        [161.9, 117.5],
        [174.6, 110.3],
        [190.5, 110.3],
        [209.6, 104.5],
        [266.7, 104.5],
        [268.3, 103.7],
        [292.1, 103.7],
        [304.8, 123.8],
        [0.0, 123.8],
        [0.0, 99.3],
        [6.4, 99.3],
        [6.4, 107.3],
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

    print(scad_render(final, file_header='$fn=%s;'%args.fn))
