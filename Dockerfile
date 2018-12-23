FROM python:3.7-alpine


WORKDIR /usr/src/app
COPY requirements.txt .
RUN apk add --no-cache build-base;\
    echo "http://dl-cdn.alpinelinux.org/alpine/edge/testing/" > /etc/apk/repositories ;\
    echo "http://dl-cdn.alpinelinux.org/alpine/edge/main/" >> /etc/apk/repositories ;\
    apk add --no-cache geos-dev geos libxml2 libspatialite;\
    pip install -r requirements.txt;\
    pip install gunicorn;\
    apk del geos-dev build-base;\
    apk add --no-cache libc-dev binutils; 
ENV SPATIALITE_LIBRARY_PATH=/usr/lib/mod_spatialite.so.7


COPY . .

RUN python db_setup.py
CMD gunicorn -b 0.0.0.0 -w 4 foodapi:app

