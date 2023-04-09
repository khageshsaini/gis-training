FROM osgeo/gdal:alpine-normal-3.6.3

RUN apk add --update make cmake gcc g++ gfortran python3-dev py3-pip

WORKDIR /app
COPY requirements.txt ./

RUN python -m pip install -r requirements.txt
COPY . .
