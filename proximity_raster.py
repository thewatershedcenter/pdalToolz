#!/bin/bash/python3


import argparse
from osgeo import ogr
import os
import shutil
import geopandas as gpd
import numpy as np
import subprocess
import xarray as xr
import rioxarray
from geocube.api.core import make_geocube
from xrspatial import proximity
from dask import delayed, compute


def parse_arguments():
    '''parses the arguments, returns args'''

    # init parser
    parser = argparse.ArgumentParser()

    # add args
    parser.add_argument(
        '--spans',
        type=str,
        required=True,
        help='Vectorfile of spans'
    )

    parser.add_argument(
        '--feeder',
        type=str,
        required=True,
        help='Name of feeder'
    )

    parser.add_argument(
        '--outfile',
        type=str,
        required=False,
        help='''Path to output file. Defaults to ./out.tiff'''
    )


    # parse the args
    args = parser.parse_args()

    if not args.outfile:
        args.outfile = './out.tiff'

    return(args)


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


def rasterize_to_xarray(df):
    '''
    Makes proximity raster based on spans.
    '''

    # get feeder name
    feeder = df.gs_feeder_.unique()[0]

    # find the crs
    crs = df.crs

    # buffer so there will not be gaps
    df['geometry'] = df.buffer(3) # this is for feet :(
    df['value'] = 1

    # make raster cube
    g = make_geocube(
                    vector_data=df,
                    measurements=['value'],
                    resolution=(-3, 3),
                    fill=0
                    )

    # create the distance raster
    g['distance'] = proximity(g.value)

    # add metadata
    g.attrs = {'feeder' : feeder, 'crs' : crs}

    return(g)


if __name__ == '__main__':

    args = parse_arguments()

    df = read_filter(args.spans, args.feeder)

    xr = rasterize_to_xarray(df)

    xr['distance'].rio.to_raster(args.outfile)
