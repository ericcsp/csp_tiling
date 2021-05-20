import subprocess

def make_tiles(**kw):
    tilesdir = f'{kw["local_folder"]}/tiles_{kw["region"]}/{kw["this_yr"]}_{kw["region"]}_{kw["this_var"]}_tiles'
    tile_cmd = f'python3 gdal2tiles-leaflet/gdal2tiles.py -z {kw["zoom"][0]}-{kw["zoom"][1]} {kw["clipped_fn"]} {tilesdir}'
    p = subprocess.Popen(tile_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    p.communicate()
