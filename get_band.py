import rasterio
import os

class Full_Img:
    def __init__(self, fname, **kw):
        self.fname = fname
        self.img = rasterio.open(self.fname)
        self.bands = kw["bands"]
        self.year = kw["this_yr"]
        self.children = {}

    def make_children(self):
        for k, v in self.bands.items():
            self.children[k] = Band_Img(k, v, self)

    def write_children(self):
        for child in self.children.values():
            child.newimg()

    def main(self):
        self.make_children()
        self.write_children()
        self.img.close()

class Band_Img:
    def __init__(self, index, band_name, parent):
        self.index = index
        self.band_name = band_name
        self.parent = parent
        self.meta = self.parent.img.meta.copy()
        self.data = self.parent.img.read(self.index)
        self.scale = self.parent.img.scales[self.index-1]
        self.outname = f'{kw["local_folder"}/{self.parent.year}/{self.band_name}/{self.parent.fname[:-4]}_{self.band_name}.tif'

    def newimg(self):
        self.meta.update({"count": 1, "dtype": self.data.dtype,
            "compress": "lzw"})
        with rasterio.open(self.outname, 'w', **self.meta) as band_write:
            band_write.write(self.scale*self.data, 1)
