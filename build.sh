imagename=cspinc/tiling:latest
datadir=$1
if [[ "$(docker images -q $imagename 2> /dev/null)" == "" ]]; then
  docker build . -t $imagename
fi
docker run -d -it -v $(pwd):/content/csp_tiling -v ${datadir}:/data --name tile_container $imagename
