#!/bin/bash

mkdir -p /var/www/html/vysledky/zbyva-zpracovat /var/www/html/vysledky/nelze-umistit /var/www/html/vysledky/zpracovane 

python /scripts/gen-nezpracovane.py /var/www/html/vysledky/zbyva-zpracovat/index.html /var/www/html/vysledky/zbyva-zpracovat/export.csv
python /scripts/gen-notmap.py /var/www/html/vysledky/nelze-umistit/index.html
python /scripts/gen-zpracovane.py /var/www/html/vysledky/zpracovane/index.html
