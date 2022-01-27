# pdalToolz
Scripts wrapping pdal pipelines to simplify tasks. See [PDAl](https://pdal.io/index.html) for more information.

Unless otherwise indicated, all files in the PDAL distribution are

Copyright (c) 2019, Hobu, Inc. (howard@hobu.co)


# Docker
There the `pdal_docker` directory has a docker capable of running any of the scripts.

Running `./pdal_docker_start.sh`, when in the directory containing `pdal_docker_start.sh` and  `pdal_docker` will build (if need be) and start the docker as an interactive bash session.

# merge_and_chip.py
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

