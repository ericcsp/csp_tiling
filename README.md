tiling software... super basic instructions:

build the docker image and start container with build.sh

attach to the docker container and set the azure account key as an environmental variable with `export`, e.g.:
export AZURE\_ACCOUNT\_KEY=\<az-account-key\> which you can get from the Azure portal.

make sure you are in the /content directory (which is the parent directory of csp\_tiling within the container) and run the program with python3 csp\_tiling/run.py

cross fingers
