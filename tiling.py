import gdal
import numpy as np
import subprocess
import matplotlib as mpl
from matplotlib import cm as cm

def export_tif(image, ref_tif, outname, bands=None, dtype=gdal.GDT_Float32, metadata=None, bandmeta=None, rasterdriver='GTiff', verbose=True):
    '''
    Input a numpy array image and a reference geotif 
    to convert image to geotiff of same geotransform
    and projection. Note, if alpha_mask is not None,
    creates a 4 channel geotiff (alpha as last channel)
    Parameters:
    -----------
    image - 3D <numpy array>
    ref_tif - Geotiff reference <str> filename or <gdal object> of same dimensions
    outname - <str> file name to output to (use .tif extension)
    dtype - <str> denoting data type for GeoTiff. Defaults to 8 bit image,
    but can use gdal.GDT_Float32
    '''
    if type(ref_tif) is not gdal.Dataset:
        ref_tif = gdal.Open(ref_tif)
    gt = ref_tif.GetGeoTransform()
    proj = ref_tif.GetProjection()
    xsize = np.shape(image)[1] 
    ysize = np.shape(image)[0] 
    if bands is None:
        bands = ref_tif.RasterCount 
    driver = gdal.GetDriverByName(rasterdriver)
    out = driver.Create(outname, xsize, ysize, bands, dtype)
    out.SetGeoTransform(gt)
    out.SetProjection(proj)
    if metadata is not None:
        out.SetMetadata(metadata)
    if bands == 1:
        band = out.GetRasterBand(1)
        band.WriteArray(image)
        if bandmeta is not None:
            band.SetMetadata(bandmeta) 
            band.SetDescription(bandmeta)
    else:
        for i in range(bands):
            band = out.GetRasterBand(i+1)
            band.WriteArray(image[:,:,i]) #if we want a red image for a 4 channel
            if bandmeta is not None:
                band.SetMetadata(bandmeta[i]) 
                band.SetDescription(bandmeta[i])
    out = None
    if verbose:
        return(print('created %s'%(outname)))

class Image:
    def __init__(self, fname, outname, tilesdir, fake_t=False, zoom=[0,13], cmap=cm.get_cmap('viridis', 7), bounds=[0,1,5,10,20,50,100]):
        self.file_name = fname 
        self.outname = outname
        self.tiles_dir = tilesdir
        self.fake_t = fake_t
        self.zoom = zoom
        self.cmap = cmap 
        self.bounds = bounds

    def manipulate_array(self):
        self.array = gdal.Open(self.file_name).ReadAsArray()
        self.shape = self.array.shape
        self.band_position = self.bands_firstlast()
        if self.fake_t:
            self.add_fake_transparency()
        if self.band_position == 0:
            self.moveaxis()
        if self.band_position == -1:
            self.array = self.array[:,:,np.newaxis]
            self.array = np.stack([self.array[:,:,0], self.array[:,:,0], self.array[:,:,0]], axis=-1)
        self.make_mappable()

    def main(self):
        self.manipulate_array()
        export_tif(self.map, self.file_name, self.outname, bands=4, dtype=gdal.GDT_Byte)
        self.make_tiles()

    def bands_firstlast(self):
        if self.shape[0] < 5:
            return 0
        elif self.shape[-1] < 5:
            return 2
        elif self.array.ndim == 2:
            return -1

    def add_fake_transparency(self):
        if self.band_position == 0:
            new_array = np.stack([self.array[0,:,:], self.array[1,:,:], self.array[2,:,:], self.array[0,:,:]])
        else:
            new_array = np.stack([self.array[:,:,0], self.array[:,:,1], self.array[:,:,2], self.array[:,:,0]])
        self.array = new_array
        del new_array

    def moveaxis(self):
        my_im = np.moveaxis(self.array, 0, -1)
        self.array = my_im
        del my_im

    def make_mappable(self):
        norm = mpl.colors.BoundaryNorm(self.bounds, self.cmap.N)
        m = cm.ScalarMappable(norm=norm, cmap=self.cmap)
        self.map = (255*m.to_rgba(self.array/self.array.max())).astype('uint8')

    def make_tiles(self):
        tile_cmd = f"python3 gdal2tiles-leaflet/gdal2tiles.py -z {self.zoom[0]}-{self.zoom[1]} {self.outname} {self.tiles_dir}"
        p = subprocess.Popen(tile_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        p.communicate()

def main(file_stem):
    fname = f'/data/placer/tif/{file_stem}.tif' 
    outname = f'{file_stem}_remapped.tif'
    tilesdir = f'{file_stem}_tiles'
    my_im = Image(fname, outname, tilesdir) 
    my_im.main()
    return my_im

if __name__ == "__main__":
    main('2005_biomass')

