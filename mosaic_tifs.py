import rasterio
from rasterio.merge import merge
import os

if __name__ == "__main__":
    all_files = [fil for fil in os.listdir('.') if '.tif' in fil]
    all_data = [rasterio.open(my_fil, 'r') for my_fil in all_files]
    mosaic, out_trans = merge(all_data)
    out_meta = all_data[0].meta.copy()
    out_meta.update({"driver": "GTiff", "height": mosaic.shape[1],
                     "width": mosaic.shape[2], "transform": out_trans,
                     "compress": "lzw"})
    with rasterio.open('california.tif', 'w', **out_meta) as dest:
        dest.write(mosaic)
