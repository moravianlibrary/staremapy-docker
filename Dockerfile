from php:7.1-apache

LABEL maintainer="daniel.secik@mzk.cz"

RUN apt-get update && \
    apt-get install -y git && \
    rm -rf /var/lib/apt/lists/*

COPY scripts /scripts

COPY apache.conf /etc/apache2/sites-available/000-default.conf
RUN /scripts/setup.sh

CMD [ "/scripts/init.sh" ]
