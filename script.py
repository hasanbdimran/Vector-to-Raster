import rasterio
from rasterio.plot import show
from rasterio import features
from rasterio import transform
from rasterio.enums import MergeAlg, Resampling

import os

import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt

bin_gfp = r"/Volumes/disk2s1/Thesis/Cleaned Version/Floodplains"
gfp_name = "Merged_Floodplains.shp"

# Read in vector
vector = gpd.read_file(os.path.join(bin_gfp, gfp_name))

# Get list of geometries and corresponding id for all features in vector file
geom_value = [(geom,value) for geom, value in zip(vector.geometry, vector.index)]

## Creating
bbox = vector.total_bounds
xmin, ymin, xmax, ymax = bbox
res = 30 # desired resolution
w = (xmax - xmin) // res 
h = (ymax - ymin) // res

out_meta = {
    "driver": "GTiff",
    "dtype": "uint8",
    "height": h,
    "width": w,
    "count": 1,
    "crs": vector.crs,
    "transform": transform.from_bounds(xmin, ymin, xmax, ymax, int(w), int(h)),
    "compress": 'lzw'
}

# Rasterize vector using the shape and transform of the raster
rasterized = features.rasterize(geom_value,
                                out_shape = [int(h), int(w)],
                                transform = out_meta['transform'],
                                all_touched = False,
                                fill = -5,   # background value
                                merge_alg = MergeAlg.replace,
                                dtype = 'int16')
