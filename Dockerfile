FROM ubuntu:20.04

ENV TZ=America/New_York
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update -yq && apt-get install -yq git python3 python3-matplotlib python3-gdal python3-pip azure-cli

RUN pip install rasterio fiona pyyaml

RUN mkdir -p /content && cd /content && git clone https://github.com/commenthol/gdal2tiles-leaflet/

WORKDIR /content

CMD /bin/bash
