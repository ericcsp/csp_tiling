import rasterio
import os

class Full_Img:
    def __init__(self, fname):
        self.fname = fname
        self.img = rasterio.open(self.fname)
        self.bands = {1: "classtype", 2: "basalarea", 3: "biomass", 4: "canopycover"}
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
        self.data = self.parent.img.read(self.index)
        self.outname = f'{self.band_name}/{self.parent.fname[:-4]}_{self.band_name}.tif'

    def newimg(self):
        with rasterio.open(
                 self.outname,
                 'w',
                 driver='GTiff',
                 height=self.parent.img.height,
                 width=self.parent.img.width,
                 count=1,
                 dtype=self.data.dtype,
                 crs=self.parent.img.crs,
                 transform=self.parent.img.transform) as band_write:
            band_write.write(self.data, 1)

if __name__ == "__main__":
    all_files = [fil for fil in os.listdir('.') if '.tif' in fil]
    for my_fil in all_files:
        my_img = Full_Img(my_fil)
        my_img.main()
