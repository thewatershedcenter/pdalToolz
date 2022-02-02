#!/bin/bash/python

import argparse
import os
import shutil
import subprocess
import json
import multiprocessing

ncores = multiprocessing.cpu_count()



def parse_arguments():
    '''parses the arguments, returns args'''

    # init parser
    parser = argparse.ArgumentParser()

    # add args
    parser.add_argument(
        '--file',
        type=str,
        required=False,
        help='File to be processed,.',
    )

    parser.add_argument(
        '--overlay',
        type=str,
        required=True,
        help='''vecotr overlay. Must be in same crs as --file''',
    )

    parser.add_argument(
        '--output_directory',
        type=str,
        required=False,
        help='''Directory in which output will be placed.
                If not specified will default to intput directory'''
    )

    # parse the args
    args = parser.parse_args()

    if not args.output_directory:
        args.output_directory = os.path.dirname(f'./{args.file}')
        args.input = args.file

    return args


def make_pipe(input, outdir, overlay):
    '''makes the pipeline(s)'''

    # make sure outdir exists
    os.makedirs(outdir, exist_ok=True)

    # make a place for the json to live (demolish old home if exists)
    jsonhouse = os.path.join(outdir, 'jsonhouse')

    if os.path.isdir(jsonhouse):
        shutil.rmtree(jsonhouse)

    os.makedirs(jsonhouse)

    # make output filename
    basename = os.path.basename(input).partition('.')[0]
    outname = os.path.join(outdir, f'{basename}_conductor14.laz')

    # make the pipeline
    pipe = [
                input,
                    {
                        'type': 'filters.range',
                        'limits': 'Classification[7:7], NumberOfReturns[1:4], Intensity[19250:29900]'
                    },
                    {
                        'type': 'filters.overlay',
                        'datasource': overlay,
                        'dimension': 'Classification',
                        'column': 'value'
                    },
                    {
                        'type': 'filters.range',
                        'limits': 'Classification[14:14]'
                    }
                    ,
                outname
            ]

    # dump the json
    dump_path = os.path.join(jsonhouse, f'{basename}.json')

    with open(dump_path, 'w') as wf:
        json.dump(pipe, wf, indent=6)

    print(f'jsons written to {jsonhouse}')

    return(jsonhouse)


def run_pipes(jsonhouse):
    '''runs pipelines that live in jsonhouse'''

    if len(os.listdir(jsonhouse)) == 1:
        # get the sinlge file
        j = os.path.join(jsonhouse, os.listdir(jsonhouse)[0])

        # make the command
        cmd = f'pdal pipeline -i {j}'

    else:
        # make the comand with gnu ||
        cmd = f'find {jsonhouse} -type f  | parallel -j{ncores-1} pdal pipeline -i {{}}'

    # run the pipeline(s)
    _ = subprocess.run(cmd, shell=True)

if __name__ == '__main__':

    # bag the args
    args = parse_arguments()

    # make the pipes
    jsonhouse = make_pipe(args.input, args.output_directory, args.overlay)

    # run the pipes
    run_pipes(jsonhouse)

    # remove jsonhouse
    shutil.rmtree(jsonhouse)

    # give some indocation that the whole thing ran
    print('Avslutad!')