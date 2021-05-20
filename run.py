import os
from pathlib import Path
import yaml
import list_hls
import get_band
import mosaic_tifs
import rgba
import clip
import tiling
import upload_tiles

with open('csp_tiling/config.yaml', 'r') as fh:
    kw = yaml.safe_load(fh)

Path(kw["local_folder"]).mkdir(parents=True, exist_ok=True)
list_hls.get_files(**kw)
all_tifs = [fil for fil in os.listdir(kw["local_folder"]) if '.tif' in fil]
kw["years"] = list(set([fil.split('_')[0] for fil in all_tifs]))
for yr in kw["years"]:
    kw["this_yr"] = yr
    yr_folder = f'{kw["local_folder"]}/{yr}'
    Path(yr_folder).mkdir(parents=True, exist_ok=True)
    for tif in all_tifs:
        if yr in tif:
            os.rename(f'{kw["local_folder"]}/{tif}', f'{kw["local_folder"]}/{yr}/{tif}')
    for bnd in kw["bands"].values():
        Path(f'{yr_folder}/{bnd}').mkdir(parents=True, exist_ok=True)
    year_tifs = [fil for fil in os.listdir(yr_folder) if '.tif' in fil]
    for yr_tif in year_tifs:
        my_yrimg = get_band.Full_Img(f'{yr_folder}/{yr_tif}', **kw)
        my_yrimg.main()
        del my_yrimg
    for var in kw["variables"]:
        kw["this_var"] = var
        kw["mosaic_fn"] = mosaic_tifs.merge_tifs(**kw)
        kw["remapped_fn"] = rgba.main(**kw)
        if 'shapes' not in kw.keys():
            kw["shapes"] = clip.get_shapes(kw["geojson"])
        kw["clipped_fn"] = clip.clip(**kw)
        kw["tilesdir"] = f'{kw["local_folder"]}/tiles_{kw["region"]}/{kw["this_yr"]}_{kw["region"]}_{kw["this_var"]}_tiles'
        Path(f'{kw["tilesdir"]}').mkdir(parents=True, exist_ok=True)
        tiling.make_tiles(**kw)
        upload_tiles.upload(**kw)
