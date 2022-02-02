import geopandas as gpd
import os
import argparse
import warnings
warnings.filterwarnings("ignore")


def parse_arguments():
    '''parses the arguments, returns args'''

    # init parser
    parser = argparse.ArgumentParser()

    # add args
    parser.add_argument(
        '--spans',
        type=str,
        required=True,
        help='Vector file of spans.',
    )

    parser.add_argument(
        '--feeder',
        type=str,
        required=True,
        help='''Name of feeder.''',
    )

    parser.add_argument(
        '--epsg',
        type=int,
        required=False,
        help='''Int part of EPSG code.
                Strangely enough, defaults to 6339''',
    )

    parser.add_argument(
        '--output_directory',
        type=str,
        required=False,
        help='''Directory in which output will be placed.
                If not specified will default to directory
                of --spans'''
    )

    parser.add_argument(
        '--buffer',
        type=int,
        required=False,
        help='''Buffer distance in proj units, defaults to 15''',
    )

    # parse the args
    args = parser.parse_args()

    if not args.output_directory:
        args.output_directory = os.path.dirname(f'./{args.spans}')

    if not args.epsg:
        args.epsg = 6339

    if not args.buffer:
        args.epsg = 15

    return args


def read_filter(vector, feeder):
    '''
    Reads vector (gpkg of spans),
    filters resulting geodatframe by feeder,
    returns df.
    '''
    # open the vector file
    df = gpd.read_file(vector)

    # filter
    df = df.loc[df.gs_feeder_ == feeder]

    return(df)



if __name__ == '__main__':

    # bag the args
    args = parse_arguments()

    # read spans
    df = read_filter(args.spans, args.feeder)

    # check epsg, reproject if necessary
    if df.crs.to_epsg() != args.epsg:
        df = df.to_crs(args.epsg)

    # buffer
    df['geometry'] = df.buffer(args.buffer)
    df['value'] = 14

    # make outfile name
    base = os.path.basename(args.spans).split('.')[0]
    path_ = os.path.join(args.output_directory, f'{base}_buffer')
    os.makedirs(path_, exist_ok=True)
    fname = os.path.join(path_, f'{base}_{args.epsg}.shp')

    df.to_file(fname)

    print(fname)