#!/bin/python

'''
python normalize.py \
--infile=/media/data/SouthForkMountain/tiled_pc_32610/SFM_0_-1_32610.las \
--outfile='buster.las' \
--Glim=1.1
'''

import numpy as np
import pdal
import argparse


def parse_arguments():
    '''parses the arguments, returns args'''

    # init parser
    parser = argparse.ArgumentParser()

    # add args
    parser.add_argument(
        '--infile',
        type=str,
        required=True,
        help='Input file',
    )

    parser.add_argument(
        '--outfile',
        type=str,
        required=True,
        help='Output file',
    )

    # add args
    parser.add_argument(
        '--Rlim',
        type=float,
        required=False,
        help='limit of redness above which points will be dropped',
    )

    # add args
    parser.add_argument(
        '--Glim',
        type=float,
        required=False,
        help='limit of greeness above which points will be dropped',
    )

    # add args
    parser.add_argument(
        '--Blim',
        type=float,
        required=False,
        help='limit of blueness above which points will be dropped',
    )

    parser.add_argument(
        '--modify',
        help='Normalize the the R, G, B dimensions and return a lasfile',
        action='store_true'
    )

    # parse the args
    args = parser.parse_args()

    return(args)


def norm_rgb(arr):
    '''returns normed RGB on 256 scale'''
    total = arr['Red'] + arr['Green'] + arr['Blue']
    normR = arr['Red'] / total
    normG = arr['Green'] / total
    normB = arr['Blue'] / total

    return(normR, normG, normB)


def norm_rgb_256(arr):
    '''returns normed RGB on 256 scale'''
    total = arr['Red'] + arr['Green'] + arr['Blue']
    normR = 255 * arr['Red'] // total
    normG = 255 * arr['Green'] // total
    normB = 255 * arr['Blue'] // total

    return(normR, normG, normB)


if __name__ == '__main__':

    # bag the args
    args = parse_arguments()

    # read the points
    pipeline = pdal.Reader.las(filename=args.infile).pipeline()
    n = pipeline.execute()
    print(f'{n} points read.')
    arr = pipeline.arrays[0]

# modify the arr and return if that is the aim
if args.modify:
    arr['Red'], arr['Green'], arr['Blue'] = norm_rgb_256(arr)
    msg = f'{args.infile} modified and written to {args.outfile}'

# filter the arr if that is the aim
else:
    normR, normG, normB = norm_rgb(arr)

    if args.Rlim:
        arr = arr[normR <= args.Rlim]

    if args.Glim:
        arr = arr[normG <= args.Glim]

    if args.Blim:
        arr = arr[normB <= args.Blim]

    msg = f'points dropped from {args.infile} based on criteria and results written to {args.outfile}'

pipeline = pdal.Writer.las(filename=args.outfile).pipeline(arr)
pipeline.execute()
print(msg)

