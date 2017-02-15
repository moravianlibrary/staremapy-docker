#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import HTMLParser, urllib, httplib
import csv
import sys, time
from itertools import groupby

def transformHeader(header):
    header[header.index('title')] = 'Název mapy'
    header[header.index('georeferencer_id')] = 'Odkaz na StareMapy.cz'
    del header[header.index('collection')]

def transformData(header, data):
    geoid_index = header.index('Odkaz na StareMapy.cz');
    geoid = data[geoid_index]
    data[geoid_index] = 'http://staremapy.georeferencer.cz/map/%s/' % (geoid)

class HTMLWriter:
    def __init__(self, out):
        self.out = out

    def writeheader(self, collections):
        self.out.write('''<!DOCTYPE html>
        <html lang="cs">
            <head>
                <meta charset="utf-8">
                <title>Staré mapy</title>
                <meta name="description" content="">
                <meta name="keywords" content="">
                <meta name="author" content="">
                <link rel="stylesheet" href="/css/main.css" media="all">
                <script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
                <!--[if lt IE 9]>
                <script src="http://html5shiv.googlecode.com/svn/trunk/html5.js"></script>
                <![endif]-->
                <!-- Google Analytics -->
                <script>
                (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
                (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
                m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
                })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

                ga('create', 'UA-241776-5', 'auto', 'tracker1');
                ga('create', 'UA-107343-14', 'auto', 'tracker2');
                ga('tracker1.send', 'pageview');
                ga('tracker2.send', 'pageview');
                </script>
                <!-- End Google Analytics -->
            </head>
            <body>
                <div id="page">
                <header>
                    <div id="header">
                        <a href="http://www.staremapy.cz/" title="Staré mapy" id="logo">Staré mapy</a>
                        <hr>
                        <nav>
                            <div id="navigation">
                                <strong>Menu</strong>
                                <ul id="main-menu">
                                    <li><a href="/" title="Hlavní stránka">Hlavní stránka</a></li>
                                    <li><a href="/sbirky-starych-map-v-cr/" title="Sbírky starých map v ČR">Sbírky v ČR</a></li>
                                    <li><a href="/projekt/" title="Projekt">Projekt</a></li>
                                    <li><a href="/vysledky/" title="Výsledky">Výsledky</a></li>
                                    <li><a href="/vysledky-souteze/" title="Soutěž">Soutěž</a></li>
                                    <li><a href="/napoveda/" title="Nápověda">Nápověda</a></li>
                                </ul> <!-- / #main-menu -->
                            </div> <!-- / #navigation -->
                        </nav>
                    </div> <!-- / #header -->
                </header>
                <hr>
                <div id="content" class="subpage nonprocessed">
                    <h1>Označené jako nelze umístit</h1>
                    <ul>%s</ul>
        ''' % (''.join(map(lambda x: '<li><a href=#%s>%s</a></li>' % (revMapCollection(x), x), collections))))

    def writeTableHeader(self, header, collection):
        self.out.write('''<table id="%s" class="zbyva-zpracovat">
                        <tr><th colspan="2">%s</th></tr>
                        <tr>%s</tr>
        ''' % (revMapCollection(collection), collection, ''.join(map(lambda x: '<th>%s</th>' % (x), header))))

    def writerow(self, row):
        self.out.write('<tr>')
        self.out.write('<td>%s</td>' % (row[0]))
        self.out.write('<td><a target="_blank" href="%s">Zobrazit</a></td>' % (row[1]))
        self.out.write('</tr>')

    def writeTableFooter(self):
        self.out.write('</table>')

    def writefooter(self):
        self.out.write('''
            <div id="generated-date">Vygenerováno ''' + time.strftime("%d.%m.%Y v %H:%M") + '''</div>
            </div> <!-- / #content -->
            <footer>
                <div id="footer">

                    <div class="companies">
                        <div class="first-pilot">
                            <a href="http://www.mzk.cz/"><img src="/img/loga/georeferencer-logo-mzk.png" alt="Moravská zemská knihovna"></a>
                            <a href="http://www.cuni.cz/"><img src="/img/loga/georeferencer-logo-cuni.png" alt="Univerzita Karlova v Praze"></a>
                            <a href="http://www.muni.cz/"><img src="/img/loga/georeferencer-logo-mu.png" alt="Masarykova univerzita"></a>
                            <a href="http://www.nkp.cz/"><img src="/img/loga/georeferencer-logo-mns.png" alt="Národní knihovna ČR"></a>
                            <a href="http://www.zcm.cz/"><img src="/img/loga/georeferencer-logo-zcm.png" alt="Západočeské muzeum v Plzni"></a>
                            <a href="http://www.ujep.cz/"><img src="/img/loga/georeferencer-logo-fzp.png" alt="Univerzita Jana Evangelisty Purkyně"></a>
                            <a href="http://www.vkol.cz/"><img src="/img/loga/georeferencer-logo-vkol.png" alt="Vědecká knihovna v Olomouci"></a>
                            <a href="http://www.cbvk.cz/"><img src="/img/loga/georeferencer-logo-cbvk.png" alt="Jihočeská vědecká knihovna"></a>
                            <a href="http://www.techlib.cz/"><img src="/img/loga/georeferencer-logo-ntk.png" alt="Národní technická knihovna"></a>
                        </div>
                        <div class="second-pilot">
                            <a href="http://www.vugtk.cz/"><img src="/img/loga/georeferencer-logo-vugtk.png" alt="Výzkumný ústav geodetický, topografický a kartografický"></a>
                            <a href="http://www.ntm.cz/"><img src="/img/loga/georeferencer-logo-ntm.png" alt="Národní technické muzeum"></a>
                            <a href="http://www.hiu.cas.cz/"><img src="/img/loga/georeferencer-logo-huav.png" alt="Historický ústav AVČR"></a>
                            <a href="http://www.muzeumbrnenska.cz/"><img src="/img/loga/georeferencer-logo-muzeumbrnenska.png" alt="Muzeum Brněnska"></a>
                            <a href="http://www.nkp.cz/"><img src="/img/loga/georeferencer-logo-nkpvugtk.png" alt="Národní knihovna ČR"></a>
                            <a href="http://www.muzeumjaromer.cz/"><img src="/img/loga/georeferencer-logo-muzeumjaromer.png" alt="Městské muzeum Jaroměř"></a>
                            <table>
                              <tr><td><a href="http://www.mlp.cz/"><img src="/img/loga/georeferencer-logo-mlp.png" alt="Městská knihovna v Praze"></a></td></tr>
                              <tr><td><a href="http://vychodoceskearchivy.cz/zamrsk/"><img src="/img/loga/georeferencer-logo-soazamrsk.png" alt="Státní oblastní archiv v Zámrsku"></a></td></tr>
                            </table>
                            <table>
                              <tr><td><a href="http://www.soaplzen.cz/"><img src="/img/loga/georeferencer-logo-soaplzen.png" alt="Státní oblastní archiv v Plzni"></a></td></tr>
                              <tr><td><a href="http://www.ceskearchivy.cz/"><img src="/img/loga/georeferencer-logo-soatrebon.png" alt="Státní oblastní archiv v Třeboni"></a></td></tr>
                            </table>
                        </div>
                    </div>

                    <!--<div class="facebook">
                        facebook plugin...
                    </div>-->

                    <div class="bottom">

                        <div class="col1">
                            <img src="/img/map.png" alt="">
                            <p>
                                <a href="/sbirky-starych-map-v-cr">Seznam digitalizovaných sbírek starých map českého území.</a>
                            </p>
                        </div>
                        <div class="col2">
                            <ul>
                                <li><a href="http://www.staremapy.cz/">Staré a historické mapy</a></li>
                                <li><a href="/sbirky-starych-map-v-cr/">Sbírky starých map v ČR</a></li>
                                <li><a href="/stare-mapy-v-zahranici/">Staré mapy v zahraničí</a></li>
                                <li><a href="/historicke-mapy-archiv/">Historické mapy, archiv</a></li>
                            </ul>
                        </div>
                        <div class="col3">
                            <a href="http://www.temap.cz/"><img src="/img/temap.png" alt=""></a>
                            <p>Technologie pro zpřístupnění mapových sbírek ČR (DF11P01OVV003)</p>
                        </div>
                    </div>
                    <div class="copyright">
                        <p class="column-left">
                        	Projekt <a href="http://www.staremapy.cz/" title="Staré a historické mapy Čech, Moravy a Slezska">Staré Mapy</a> založil <a href="http://www.klokantech.com/">Klokan Petr Přidal</a>
                        </p>
                        <p class="column-left">
				<a href="http://www.radimkacer.com/">Design Radim Kacer</a>
                        </p>
                        <p style="display:none">
                        	Reklama: <a href="http://www.scootland.cz/">Scootland - </a><a href="http://www.scootland.cz/skutry/">skútry, </a><a href="http://www.scootland.cz/scooter-tuning-jaknato/">scooter tuning, </a><a href="http://www.scootland.cz/eshop/">náhradní díly</a>
                        </p>

                        <p class="column-right">
                        	<a href="http://www.temap.cz/">Výzkumný projekt TEMAP.</a>
                        </p>
                        <p class="column-right">
                        	Copyright © 2013 <a href="http://www.mzk.cz/">Moravská zemská knihovna.</a>
                        </p>

                    </div>

                </div> <!-- / #footer -->
            </footer>


        </div> <!-- / #page -->
        <div class="invisible-div"><a href="http://navrcholu.cz/"><img src="http://c1.navrcholu.cz/hit?site=100272;t=lb14;ref=;jss=0" width="14" height="14" alt="NAVRCHOLU.cz" style="border:none;visibility:hidden"></a></div>
        </body>
        </html>
        ''')

def groupByFunc(data, i):
    groups = {}
    for k, g in groupby(filter(lambda x: len(x) != 0, data), key = lambda x : x[i]):
        if k in groups:
            groups[k] += list(g)
        else:
            groups[k] = list(g)
    return list(groups.iteritems())

colMapping = {}
colMapping['Jihočeská vědecká knihovna v Českých Budějovicích'] = ['cbvk']
colMapping['Univerzita Karlova v Praze'] = ['cuni']
colMapping['Historický ústav AVČR'] = ['huav']
colMapping['Městská knihovna v Praze'] = ['mlp']
colMapping['Masarykova univerzita'] = ['muni']
colMapping['Muzeum Brněnska'] = ['muzeumbrnenska']
colMapping['Městské muzeum Jaroměř'] = ['muzeumjaromer']
colMapping['Moravská zemská knihovna'] = ['mzk']
colMapping['Národní knihovna ČR'] = ['nkp']
colMapping['Výzkumný ústav geodetický, topografický a kartografický'] = ['nkpvugtk']
colMapping['Národní technická knihovna'] = ['ntk', 'ntk2']
colMapping['Národní technické muzeum'] = ['ntm']
colMapping['Rajhrad'] = ['rajhrad2']
colMapping['Státní oblastní archiv v Plzni'] = ['soaplzen']
colMapping['Státní oblastní archiv v Třeboni'] = ['soatrebon']
colMapping['Státní oblastní archiv v Zámrsku'] = ['soazamrsk']
colMapping['Univerzita Jana Evangelisty Purkyně'] = ['ujep']
colMapping['Vědecká knihovna v Olomouci'] = ['vkol']
colMapping['Západočeské muzeum v Plzni'] = ['zcm']

revColMapping = {}
for key, value in colMapping.iteritems():
    for v in value:
        revColMapping[v] = key

def mapCollections(data, i):
    for row in data:
        if len(row) != 0:
            row[i] = revColMapping[row[i]]
            yield row

def revMapCollection(col):
    return colMapping[col][0]

def setUndefinedTitle(indata):
    for row in indata:
        if not row[0]:
            if row[2] == 'Univerzita Jana Evangelisty Purkyně':
                row[0] = 'oldmaps.geolab.cz'
            else:
                row[0] = 'Neuvedeno'
        yield row

query = "SELECT 'title', 'georeferencer_id', 'collection' FROM 1gpUBes9cpOkH3h-fNyS_4dnuLelIY-bSuWdNfqw WHERE 'status' = 'not_a_map'"
params = urllib.urlencode({'query' : query})
conn = httplib.HTTPSConnection("fusiontables.google.com")
conn.request("GET", "/exporttable?" + params)
response = conn.getresponse()
if response.status == 200:
    htmlParser = HTMLParser.HTMLParser()
    input = []
    for row in response.read().split('\n'):
        input.append(htmlParser.unescape(row.decode('utf-8')).encode('utf-8'))

    csvreader = csv.reader(input)

    htmlfile = open(sys.argv[1], 'w')

    htmlwriter = HTMLWriter(htmlfile)

    header = csvreader.next()

    indata = mapCollections(csvreader, 2)

    indata = setUndefinedTitle(indata)

    indata = groupByFunc(indata, 2)

    indata = sorted(indata, key = lambda x: x[0])

    transformHeader(header)

    htmlwriter.writeheader([x[0] for x in indata])
    for collection, data in indata:
        firstRow = True

        for row in data:
            if firstRow:
                firstRow = False
                htmlwriter.writeTableHeader(header, collection)

            transformData(header, row)
            htmlwriter.writerow(row)
        htmlwriter.writeTableFooter()

    htmlwriter.writefooter()

    htmlfile.close()
else:
    sys.stderr.write("Response status: %d" % response.status)
    sys.exit(1)
