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
        self.export_tif()
        self.dataset.close()

    def make_mappable(self):
        norm = mpl.colors.BoundaryNorm(self.bounds, self.cmap.N)
        m = cm.ScalarMappable(norm=norm, cmap=self.cmap)
        self.map = m.to_rgba((self.array/self.array.max()), bytes=True, norm=False)
        mask = self.array > 0.001
        self.map[...,-1] = 255*mask

    def export_tif(self):
        out_meta = self.dataset.meta.copy()
        out_meta.update({"count": 4, "dtype": "uint8", "compress": "lzw"})
        with rasterio.open(self.outname, 'w', **out_meta) as dest:
            for i in range(4):
                dest.write(self.map[:,:,i], i+1)

def make_tiles(outname, tilesdir, zoom=[0,13]):
    tile_cmd = f"python3 gdal2tiles-leaflet/gdal2tiles.py -z {zoom[0]}-{zoom[1]} {outname} {tilesdir}"
    p = subprocess.Popen(tile_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    p.communicate()

def main(file_stem, with_tiles=False):
    year, region, variable = file_stem.split('_')
    fname = f'/data/hls_output_2021-05-13/{year}/{variable}/{file_stem}.tif' 
    outname = f'/data/hls_output_2021-05-13/{year}/{variable}/{file_stem}_remapped.tif' 
    tilesdir = f'/data/tiles_{region}/{year}/{variable}/{file_stem}_tiles'
    my_rgb = RGBTiff(fname, outname) 
    my_rgb.main()
    if with_tiles:
        make_tiles(outname, tilesdir) 
    return my_rgb

if __name__ == "__main__":
    for yr in ['2016', '2018']:
        for var in ['biomass', 'basalarea', 'canopycover']:
            #my_main = 
            main(f'{yr}_California_{var}', with_tiles=False)
            #del my_main


