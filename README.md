# pdalToolz
Scripts wrapping pdal pipelines to simplify tasks. See [PDAl](https://pdal.io/index.html) for more information.

Unless otherwise indicated, all files in the PDAL distribution are

Copyright (c) 2019, Hobu, Inc. (howard@hobu.co)


# Docker
The `pdal_docker` directory has a docker capable of running `conductor_trim.py`, `fisrt7_to_15only.py`, `merge_and_chip.py`.

Running `./pdal_docker_start.sh`, when in the directory containing `pdal_docker_start.sh` and  `pdal_docker` will build (if need be) and start the docker as an interactive bash session.

The `pdal_docker` directory has a docker capable of running 'feeder_buff.py'.

Running `./geo_docker_start.sh`, when in the directory containing `geo_docker_start.sh` and  `geo_docker` will build (if need be) and start the docker as an interactive bash session.


TODO:
+ Put images on quay and change start scripts to pull image, instead of building from Dockerfile.




# merge_and_chip.py
__NOTE: Does not work correctly__

Merges files in a directory, then chips them according to the specified capacity.  This is used in cases where it is desireable to transform a directory full of tiles which have different point densities and thus file sizes into chips each of which contain apporimately the same number of points.  See [PDAL's filters.chipper](https://pdal.io/stages/filters.chipper.html) for more information on the underlying function.  Be aware of how much memory is available and the total filesize within the directory.  This is not a streaming operation, and therefore must have suffficient memory to hold the files.

```
usage: merge_and_chip.py [-h] --directory DIRECTORY [--chipdir CHIPDIR]
                         [--capacity CAPACITY]

optional arguments:
  -h, --help            show this help message and exit
  --directory DIRECTORY
                        Directory of files to merge.
  --chipdir CHIPDIR     Directory in which to place chips. Defualt = ./chipdir
  --capacity CAPACITY   Desired number of points per chip, default = 10^6
```

# fisrt7_to_15only.py
Selects points by the following criteria:
```
'limits': 'Classification[7:7], ReturnNumber[1:1], Intensity[19250:29900]'
```
Then reclassifies them as 14 and writes a new point cloud with `_conductor15` inserted into the original filename.

```
usage: first7_to_15only.py [-h] [--file FILE] [--directory DIRECTORY]
                           [--output_directory OUTPUT_DIRECTORY]

optional arguments:
  -h, --help            show this help message and exit
  --file FILE           File to be processed, required if no directory is
                        specified.
  --directory DIRECTORY
                        Directory of files to be processed, required if no
                        directory is specified.
  --output_directory OUTPUT_DIRECTORY
                        Directory in which output will be placed. If not
                        specified will default to intput directory

```
# conductor_trim.py
Does everything `fisrt7_to_15only.py` does as well as clipping by an overlay vector.

```
usage: conductor_trim.py [-h] [--file FILE] --overlay OVERLAY
                         [--output_directory OUTPUT_DIRECTORY]

optional arguments:
  -h, --help            show this help message and exit
  --file FILE           File to be processed,.
  --overlay OVERLAY     vecotr overlay. Must be in same crs as --file
  --output_directory OUTPUT_DIRECTORY
                        Directory in which output will be placed. If not
                        specified will default to intput directory

```

# feeder_buff.py
Selects feeder, reprojects, and buffers feeder from span vector.

```
usage: feeder_buff.py [-h] --spans SPANS --feeder FEEDER [--epsg EPSG]
                      [--output_directory OUTPUT_DIRECTORY] [--buffer BUFFER]

optional arguments:
  -h, --help            show this help message and exit
  --spans SPANS         Vector file of spans.
  --feeder FEEDER       Name of feeder.
  --epsg EPSG           Int part of EPSG code. Strangely enough, defaults to
                        6339
  --output_directory OUTPUT_DIRECTORY
                        Directory in which output will be placed. If not
                        specified will default to directory of --spans
  --buffer BUFFER       Buffer distance in proj units, defaults to 15

```

# Typical workflow
Start the geo docker with the ,
```
./geo_docker_start.sh
```
then cs to data
```
cd /data
```
then run
```
python3 conductor_trim.py --spans=spans.gpkg --feeder='W02' --buffer=20
```
A directory calle `spans_buffer` containing a shapefile `spans_6339.shp` should have apeared.
Exit the geo_docker.
```
exit
```
Start the pdal docker and change directories
```
./pdal_docker_start.sh
cd /data
```
Then run
```
conductor_trim.py --file=los_puntos.laz --overlay=spans_buffer/spans_6339.shp --output_directory=.
```
A file called `los_puntos_conductor14.laz' should now be in /data. Exit pdal_docker.


 TODO: finish this...