FROM ubuntu:20.04

RUN apt-get update && apt-get install git python3 python3-matplotlib

RUN mkdir -p /content && cd /content && git clone https://github.com/commenthol/gdal2tiles-leaflet/

WORKDIR /content

CMD /bin/bash
