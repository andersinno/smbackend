Service Map Backend
===================

This is the backend service for the Service Map UI.

Installation
------------

First, install the necessary Debian packages.

    libpython3.4-dev virtualenvwrapper libyaml-dev libxml2-dev libxslt1-dev

You might need to start a new shell for the virtualenvwrapper commands to activate.

1. Make a Python virtual environment.

```
mkvirtualenv -p /usr/bin/python3.4 smbackend
```

2. Install pip requirements.

    ```pip install -r requirements.txt```
 
3. Setup the PostGIS database.

Please note we require PostgreSQL version 9.4 or higher

Local setup:

```
sudo su postgres

createuser -R -S -D -P smbackend

createdb -O smbackend -T template0 -l fi_FI.UTF-8 -E utf8 smbackend

echo "CREATE EXTENSION postgis;" | psql smbackend

echo "CREATE EXTENSION hstore;" | psql smbackend
```

Docker setup (modify as needed, starts the database on local port 8765):
```
docker run --name smbackend-psql -e POSTGRES_USER=smbackend -e POSTGRES_PASSWORD=smbackend -p 8765:5432 -d mdillon/postgis
# you'll need the hstore extension enabled:
echo "CREATE EXTENSION hstore;" | docker exec -i smbackend-psql psql -U smbackend
```

4. Modify `local_settings.py` to contain the local database info.

```
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'HOST': '127.0.0.1',
        'NAME': 'smbackend',
        'USER': 'smbackend',
        'PASSWORD': 'smbackend',
    }
}
```

5. Create database tables.

```
./manage.py syncdb
./manage.py migrate
```

If these commands fail with: `django.core.exceptions.ImproperlyConfigured: GEOS is required and has not been detected.`,
then install the GEOS library. On a Mac this can be achieved with HomeBrew:
```
brew install geos
```

6. Import geo data.

```
./manage.py geo_import finland --municipalities
./manage.py geo_import helsinki --divisions
```

Search
------

You can configure multilingual Elasticsearch-based search by including
something like the following in your `local_settings.py`:

```python
import json
def read_config(name):
    return json.load(open(
        os.path.join(
            BASE_DIR,
            'smbackend',
            'elasticsearch/{}.json'.format(name))))

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'multilingual_haystack.backends.MultilingualSearchEngine',
    },
    'default-fi': {
        'ENGINE': 'multilingual_haystack.backends.LanguageSearchEngine',
        'BASE_ENGINE': 'multilingual_haystack.custom_elasticsearch_search_backend.CustomEsSearchEngine',
        'URL': 'http://localhost:9200/',
        'INDEX_NAME': 'servicemap-fi',
        'MAPPINGS': read_config('mappings_finnish')['modelresult']['properties'],
        'SETTINGS': read_config('settings_finnish')
    },
    'default-sv': {
        'ENGINE': 'multilingual_haystack.backends.LanguageSearchEngine',
        'BASE_ENGINE': 'multilingual_haystack.custom_elasticsearch_search_backend.CustomEsSearchEngine',
        'URL': 'http://localhost:9200/',
        'INDEX_NAME': 'servicemap-sv',
    },
    'default-en': {
        'ENGINE': 'multilingual_haystack.backends.LanguageSearchEngine',
        'BASE_ENGINE': 'multilingual_haystack.custom_elasticsearch_search_backend.CustomEsSearchEngine',
        'URL': 'http://localhost:9200/',
        'INDEX_NAME': 'servicemap-en',
    },
}
```

## Voikko

Voikko is a spelling and grammar checker, hyphenator and collection
of related linguistic data for Finnish language.

When indexing entries using the `rebuild_index` command the `voikko` library and Elasticsearch plugin
is required in order for the indexing to work.

To get Voikko working, the following steps needs to be taken:
1. Install the Voikko OS library, on Debian/Ubuntu you do this by running `apt install libvoikko1`
2. Install the Elasticsearch Voikko plugin, this can be done by running the following command
    * Voikko required the Morpho dict to be installed, depending on the version of libvoikko you will either
     need http://www.puimula.org/htp/testing/voikko-snapshot/dict-morpho.zip for libvoikko < 4 or
     http://www.puimula.org/htp/testing/voikko-snapshot-v5/dict-morpho.zip for libvoikko >= 4
     install it using the following command:
    ```
    wget <LINK_TO_MORPHO> --quiet -O /tmp/dict-morpho.zip \
    && mkdir -p /usr/lib/voikko \
    && unzip -q /tmp/dict-morpho.zip -d /usr/lib/voikko \
    && rm /tmp/dict-morpho.zip
    ```
    * Install the Voikko Elasticsearch plugin with `/usr/share/elasticsearch/bin/plugin --install fi.evident.elasticsearch/elasticsearch-analysis-voikko/0.3.0`
    * Symlink the libvoikko to 
This is a requirement for Elasticsearch and not for the application itself, so no changes needs
to be made to the application settings.


Troubleshooting
---------------

The error:
```
OSError: dlopen(/usr/local/lib/libgdal.dylib, 6): Symbol not found: _GEOSArea
```
Can be fixed by adding this to local_settings.py:
```python
GDAL_LIBRARY_PATH = "/usr/local/lib/libgdal.dylib"
import ctypes
ctypes.CDLL(GDAL_LIBRARY_PATH)
```
