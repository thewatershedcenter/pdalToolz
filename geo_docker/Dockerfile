FROM pdal/pdal:2.1

RUN apt-get update && \
    apt-get install -y apt-utils && \
    apt-get install -y parallel python3 python3-pip cython

RUN python3 -m pip install --upgrade osgeo pyproj==3.3.0 geopandas xarray-spatial geocube rioxarray dask

ENTRYPOINT [ "bash" ]