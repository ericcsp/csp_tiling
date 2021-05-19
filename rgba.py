import rasterio
import matplotlib as mpl
from matplotlib import cm as cm

class RGBTiff:
    def __init__(self, fname, outname, **kw):
        self.file_name = fname 
        self.outname = outname
        self.cmap = cm.get_cmap(kw['ramp'], kw['c_levels']) 
        self.bounds = kw['bounds']

    def manipulate_array(self):
        self.dataset = rasterio.open(self.file_name)
        self.array = self.dataset.read(1)
        self.array[self.array < 0] = 0
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
        del out_meta['nodata']
        with rasterio.open(self.outname, 'w', **out_meta) as dest:
            for i in range(4):
                dest.write(self.map[:,:,i], i+1)

def main(**kw):
    outname = f'{kw["mosaic_fn"][:-4]}_remapped.tif'
    my_rgb = RGBTiff(kw["mosaic_fn"], outname, **kw) 
    my_rgb.main()
    return outname
