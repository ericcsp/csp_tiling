imagename=cspinc/tiling:latest
mkdir -p $HOME/csptiling_data
docker build . -t $imagename
docker run -d -it -v $(pwd):/content/csp_tiling -v $HOME/csptiling_data:/data --name tile_container $imagename
