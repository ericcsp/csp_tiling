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

with open('config.yaml', 'r') as fh:
    kw = yaml.safe_load(fh)

kw["shapes"] = clip.get_shapes(kw["geojson"])
Path(kw["local_folder").mkdir(parents=True, exist_ok=True)
list_hls.get_files(**kw)
all_tifs = [fil for fil in os.listdir(kw["local_folder"]) if '.tif' in fil]
kw["years"] = list(set([fil.split('_')[0] for fil in all_tifs])).sort()
for yr in kw["years"]:
    kw["this_yr"] = yr
    Path(f'{kw["local_folder"}/{yr}').mkdir(parents=True, exist_ok=True)
    for tif in all_tifs:
        if yr in tif:
            os.rename(f'{kw["local_folder"]/tif', f'{kw["local_folder"]/{yr}/tif')
    for bnd in kw["bands"].values:
        Path(f'{kw["local_folder"}/{yr}/{bnd}').mkdir(parents=True, exist_ok=True)
    year_tifs = [fil for fil in os.listdir(f'{kw["local_folder"}/{yr}') if '.tif' in fil]
    for yr_tif in year_tifs:
        my_yrimg = get_band.Full_Img(yr_tif, **kw)
        my_yrimg.main()
        del my_yrimg
    for var in kw["variables"]:
        kw["this_var"] = var
        kw["mosaic_fn"] = mosaic_tifs.merge_tifs(**kw)
        kw["remapped_fn"] = rgba.main(**kw)
        kw["clipped_fn"] = clip.clip(**kw)
        kw["tilesdir"] = tiling.make_tiles(**kw)
        upload_tiles.upload(**kw)
