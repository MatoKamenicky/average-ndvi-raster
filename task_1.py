import rasterio as rio
import numpy as np
import matplotlib.pyplot as plt
import glob
from rasterio.plot import show
from rasterio.mask import mask
import geopandas as gpd
import os


def process_raster(files, boundary):
    cropped_data = []
    data = []
    filenames = []

    # Open and read raster files + handle nodata values
    for f in files:
        src = rio.open(f)
        nodata_val = src.nodata
        boundary = boundary.to_crs(src.crs)
        filenames.append(os.path.basename(f))    

        data.append(np.ma.masked_where(src.read(1) == nodata_val, src.read(1)))
        cropped_brno = mask(src, boundary.geometry, crop=True, nodata=0)
        cropped_data.append(np.ma.masked_where(cropped_brno[0] == nodata_val, cropped_brno[0]))

    return cropped_data, data, filenames, src


def calculate_average(cropped_data, data):
    crop_average = np.reshape(np.ma.mean(cropped_data, axis=0), (2052, 2179))
    average = np.ma.mean(data, axis=0)

    return crop_average, average
    

def plot_input_data(data, filenames, cmap='Greens'):
    for i in range(len(data)):
        show(data[i], cmap=cmap, title=filenames[i], vmin=0, vmax=1)
        plt.show()
    return


def plot_cropped_data(data, filenames, cmap='Greens'):
    for i in range(len(data)):
        show(data[i][0], cmap=cmap, title=filenames[i], vmin=0, vmax=1)
        plt.show()
    return



def plot_average_ndvi(average, cropped_average):
    fig, (ax1, ax2) = plt.subplots(figsize=(15, 8), ncols=2)
    avg = ax1.imshow(average, cmap='Greens', vmin=0, vmax=1)
    ax1.set_title('Average NDVI')
    fig.colorbar(avg, ax=ax1, anchor=(0, 0.5), shrink=0.6)

    avg_mas = ax2.imshow(cropped_average, cmap='Greens', vmin=0, vmax=1)
    ax2.set_title('Cropped average NDVI')
    fig.colorbar(avg_mas, ax=ax2, anchor=(0, 0.5), shrink=0.6)
    plt.show()
    return

def save_geotiff(src, average):
    with rio.open(
        'average_ndvi_cropped.tiff',
        'w',
        driver=src.driver,
        height=src.height,
        width=src.width,
        count=src.count,
        dtype=average.dtype,
        crs=src.crs,
        transform=src.transform,
    ) as dst:
        dst.write(average, 1)
    return


if __name__ == '__main__':
    folder = 'NDVI'
    files = glob.glob(folder + '*.tiff')
    boundary = gpd.read_file('Brno_boundaries.shp')

    # Process raster files
    cropped_data, data, filenames, src = process_raster(files, boundary)

    # Calculate average NDVI
    cropped_average, average = calculate_average(cropped_data, data)

    # Show average NDVI
    plot_average_ndvi(average, cropped_average)

    # Show input raster files
    plot_input_data(data, filenames)

    # Show cropped raster files
    plot_cropped_data(cropped_data, filenames)

    # Save average NDVI to geotiff
    save_geotiff(src, average)
    save_geotiff(src, cropped_average)
