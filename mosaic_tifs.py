import rasterio
from rasterio.merge import merge
import os

def merge_tifs(**kw):
    all_files = [fil for fil in os.listdir(f'{kw["local_folder"}/{kw["this_yr"]}/{kw["this_var"]}') if '.tif' in fil and f'{yr}_1' in fil]
    all_data = [rasterio.open(f'{kw["local_folder"}/{kw["this_yr"]}/{kw["this_var"]}/{my_fil}', 'r') for my_fil in all_files]
    out_meta = all_data[0].meta.copy()
    mosaic, out_trans = merge(all_data)
    out_meta.update({"driver": "GTiff", "height": mosaic.shape[1],
                     "width": mosaic.shape[2], "transform": out_trans,
                     "compress": "lzw"})
    mosaic_file_name = f'{kw["local_folder"}/{kw["this_yr"]}/{kw["this_var"]}/{kw["this_yr"]}_{kw["region"]}_{kw["this_var"]}.tif'
    with rasterio.open(mosaic_file_name, 'w', **out_meta) as dest:
        dest.write(mosaic)
    return mosaic_file_name

