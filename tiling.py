import rasterio
import subprocess
import matplotlib as mpl
from matplotlib import cm as cm

class RGBTiff:
    def __init__(self, fname, outname, cmap=cm.get_cmap('viridis', 7), bounds=[0,1,5,10,20,50,100]):
        self.file_name = fname 
        self.outname = outname
        self.cmap = cmap 
        self.bounds = bounds

    def manipulate_array(self):
        self.dataset = rasterio.open(self.file_name)
        self.array = self.dataset.read(1)
        self.make_mappable()

    def main(self):
        self.manipulate_array()
        export_tif(self.map, self.file_name, self.outname)
        self.dataset.close()

    def make_mappable(self):
        norm = mpl.colors.BoundaryNorm(self.bounds, self.cmap.N)
        m = cm.ScalarMappable(norm=norm, cmap=self.cmap)
        self.map = m.to_rgba((self.array/self.array.max()), bytes=True, norm=False)

    def export_tif(self):
        out_meta = self.dataset.meta.copy()
        out_meta.update({"compress": "lzw"})
        with rasterio.open(self.outname, 'w', **out_meta) as dest:
            dest.write(self.map)

def make_tiles(outname, tilesdir, zoom=[0,13]):
    tile_cmd = f"python3 gdal2tiles-leaflet/gdal2tiles.py -z {zoom[0]}-{zoom[1]} {outname} {tiles_dir}"
    p = subprocess.Popen(tile_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    p.communicate()

def main(file_stem, with_tiles=False):
    fname = f'/data/placer/tif/{file_stem}.tif' 
    outname = f'/data/{file_stem}_remapped.tif'
    tilesdir = f'/data/{file_stem}_tiles'
    my_rgb = RGBTiff(fname, outname, tilesdir) 
    my_rgb.main()
    return my_rgb
    if with_tiles:
        make_tiles(outname, tilesdir) 

if __name__ == "__main__":
    for yr in ['2005', '2020']:
        for var in ['ba', 'biomass', 'canopycover']:
            if '2005' in yr and 'biomass' in var:
                continue
            else:
                out = main(f'{yr}_{var}')
                del out

