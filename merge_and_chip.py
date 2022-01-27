#!/bin/python3


import subprocess
import os
import argparse
import json


def parse_arguments():
    '''parses the arguments, returns args'''

    # init parser
    parser = argparse.ArgumentParser()

    # add args
    parser.add_argument(
        '--directory',
        type=str,
        required=True,
        help='Directory of files to merge.',
    )

    parser.add_argument(
        '--chipdir',
        type=str,
        required=False,
        help='Directory in which to place chips. Defualt = ./chipdir'
    )

    parser.add_argument(
        '--capacity',
        type=int,
        required=False,
        help='Desired number of points per chip, default = 10^6'
    )

    # parse the args
    args = parser.parse_args()

    if not args.chipdir:
        args.chipdir='./chipdir'

    if not args.capacity:
        args.capacity = 1_000_000

    return args


def ag_files_to_ramsize():
    '''generates filelist of files which are as
    close to frac * RAM as possible without going over.'''


def make_pipe(directory, chipdir, capacity):
    '''makes the pipeline'''

    # make sure chipdir exists
    os.makedirs(chipdir, exist_ok=True)

    # start the pipeline as a list on inout files
    pipe = [os.path.join(directory, f) for f in  os.listdir(directory) if 'laz' in f]

    # append the chipper stage to pipeline
    pipe.append(
        {
        "type":"filters.chipper",
        "capacity":capacity
        }
        )

    # append the output file pattern to pipeline
    pipe.append(
        os.path.join(chipdir, f'{directory}_chip#.laz')
    )

    # dump the json
    dump_path = os.path.join(chipdir, f'{directory}.json')

    with open(dump_path, 'w') as f:
        json.dump(pipe, f, indent=6)

    return dump_path


if __name__ == '__main__':

    args = parse_arguments()
    pipe = make_pipe(args.directory, args.chipdir, args.capacity)

    # make pdal command
    cmd = f'pdal pipeline -i {pipe}'

     # run it
    _ = subprocess.run(cmd, shell=True)

    # remove json from chipdir
    os.remove(pipe)