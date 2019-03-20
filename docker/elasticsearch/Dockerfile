FROM elasticsearch:1.7.6

# Install libvoikko
RUN DEBIAN_FRONTEND=noninteractive

RUN mkdir /tmp/voikko
ADD . /tmp/voikko

RUN apt-get update && apt-get install -yq libvoikko1

RUN sed -i 's%^#*ES_JAVA_OPTS=%ES_JAVA_OPTS=-Djna.library.path=/usr/lib/x86_64-linux-gnu%' /etc/default/elasticsearch

# Install Voikko's morpho-dictionary
# Note that if the version of libvoikko >=4 then use http://www.puimula.org/htp/testing/voikko-snapshot-v5/dict-morpho.zip
RUN wget http://www.puimula.org/htp/testing/voikko-snapshot/dict-morpho.zip --quiet -O /tmp/dict-morpho.zip \
    && mkdir -p /usr/lib/voikko \
    && unzip -q /tmp/dict-morpho.zip -d /usr/lib/voikko \
    && rm /tmp/dict-morpho.zip


RUN plugin --install fi.evident.elasticsearch/elasticsearch-analysis-voikko/0.3.0
RUN ln -s /usr/lib/x86_64-linux-gnu/libvoikko.so.1 /usr/share/elasticsearch/libvoikko.so.1
