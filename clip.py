import fiona
import rasterio
import rasterio.mask

def get_shapes(geojson_file):
    with fiona.open(geojson_file, "r") as shapefile:
        return [feature["geometry"] for feature in shapefile]

def clip(**kw):
    clipped_fn = 'f{kw["remapped_fn"][:-4]}2.tif'
    with rasterio.open(kw["remapped_fn"], 'r') as src:
        out_image, out_transform = rasterio.mask.mask(src, kw["shapes"], crop=True)
        out_meta = src.meta
        out_meta.update({"compress": "lzw"})

    with rasterio.open(clipped_fn, "w", **out_meta) as dest:
        dest.write(out_image)
    del out_image
    del out_meta
    return clipped_fn
