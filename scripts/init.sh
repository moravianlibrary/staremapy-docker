#!/bin/bash

git clone https://github.com/moravianlibrary/www.staremapy.cz.git /var/www/html
chown -R www-data:www-data /var/www/html
/scripts/generovat.sh
cron
apache2-foreground
