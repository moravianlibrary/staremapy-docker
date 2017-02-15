from php:7.1-apache

MAINTAINER Daniel Secik <daniel.secik@mzk.cz>

RUN apt-get update && \
    apt-get install -y git python cron && \
    rm -rf /var/lib/apt/lists/*

COPY scripts /scripts
RUN chmod u+x /scripts/generovat.sh
RUN chmod u+x /scripts/init.sh

COPY ./crontab /etc/cron.d/generate
RUN chmod 0644 /etc/cron.d/generate && chown root:root /etc/cron.d/generate

CMD [ "/scripts/init.sh" ]
