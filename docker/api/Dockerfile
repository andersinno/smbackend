FROM python:3.4.8-slim-jessie

ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive

RUN mkdir /code
WORKDIR /code

# Install the appropriate Ubuntu packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libpython3.4-dev \
    virtualenvwrapper \
    libyaml-dev \
    libxml2-dev \
    libxslt1-dev \
    libpq-dev \
    git \
    libgeos-dev \
    binutils \
    libproj-dev \
    gdal-bin \
    netcat

# Upgrade pip
RUN pip install -U pip

# Install python dependencies
ADD . /code/

RUN pip install --no-cache-dir -r requirements.txt

# Add entrypoint script
ADD docker-entrypoint.sh /entrypoint/
RUN chmod +x /entrypoint/docker-entrypoint.sh
