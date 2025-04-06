# Average NDVI Raster

This project processes NDVI raster files, clips them to a boundary (e.g., Brno), calculates average NDVI values, and visualizes the results.

## Features

- Load and visualize NDVI rasters
- Clip rasters using a shapefile boundary
- Compute average NDVI (full and cropped)
- Save outputs as GeoTIFF files

## Requirements

- Python 3.x
- rasterio
- geopandas
- numpy
- matplotlib