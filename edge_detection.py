import rasterio
import numpy as np
from skimage import filters, exposure, morphology, measure, segmentation, feature, transform
from scipy import ndimage
from rasterio.plot import show, show_hist
from rasterio import features
import fiona

with rasterio.open("dsm.tif") as raster:
    img = raster.read(1)
    crs = raster.crs

# Apply median filter
kernel_size = 3
med_filtered = filters.median(img, footprint=morphology.square(kernel_size))

# Apply contrast stretching
p2, p98 = np.percentile(med_filtered, (2, 98))
contrast_stretched = exposure.rescale_intensity(med_filtered, in_range=(p2, p98))

# Threshold the DSM raster
threshold = filters.threshold_otsu(contrast_stretched)
binary = contrast_stretched > threshold

# Apply the watershed segmentation algorithm
# watershed = segmentation.watershed(contrast_stretched, mask=binary)
# shapes_ws = features.shapes(watershed.astype('uint16'), transform=raster.transform)
shapes_ws = features.shapes(binary.astype('uint16'), transform=raster.transform)

# Define the schema for the shapefile
schema = {'geometry': 'Polygon', 'properties': {'id': 'int'}}

# Open a new shapefile for writing
with fiona.open('output/vectors/dsm.shp', 'w', 'ESRI Shapefile', schema) as dst:
    # Write the geometries to the shapefile
    for i, shape in enumerate(shapes_ws):
        geom, value = shape
        feature = {'geometry': geom, 'properties': {'id': i}}
        dst.write(feature)

