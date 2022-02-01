#!/bin/bash/python3


import argparse
from osgeo import ogr
import os
import shutil
import geopandas as gpd
import numpy as np
import subprocess
import xarray as xr
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
        '--output_dir',
        type=str,
        required=False,
        help='''Directory where laz files will be placed upon running pipeline.
                If omitted files will be written to PWD'''
    )

    parser.add_argument(
        '--buffer',
        type=float,
        required=True,
        help='Width of buffer in files native projected units'
    )

    # parse the args
    args = parser.parse_args()

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