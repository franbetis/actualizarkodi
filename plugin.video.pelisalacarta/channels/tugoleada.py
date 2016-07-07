# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para TUGOLEADA
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import re

from core import scrapertools
from core import logger
from core import config
from core.item import Item
from core.scrapertools import decodeHtmlentities as dhe

__channel__ = "tugoleada"
__category__ = "d"
__type__ = "generic"
__title__ = "TUGOLEADA"
__language__ = "ES"

host ="http://tugoleada.com/"
DEBUG = config.get_setting("debug")


def isGeneric():
    return True


def mainlist(item):
    logger.info("pelisalacarta.channels.tugoleada mainlist")
    itemlist = []

    itemlist.append(Item(channel=__channel__, title="Agenda/Directos", action="entradas", url="http://www.elitegol.com/", thumbnail="http://i.imgur.com/DegBUpj.png",fanart="http://i.imgur.com/bCn8lHB.jpg?1", folder=True))
    itemlist.append(Item(channel=__channel__, title="Canales Acestream", action="canales", url=host+"index.php", thumbnail="http://i.imgur.com/DegBUpj.png",fanart="http://i.imgur.com/bCn8lHB.jpg?1", folder=True))
    itemlist.append(Item(channel=__channel__, title="Canales Sopcast", action="canales", url=host+"index.php", thumbnail="http://i.imgur.com/DegBUpj.png",fanart="http://i.imgur.com/bCn8lHB.jpg?1", folder=True))
    itemlist.append(Item(channel=__channel__, title="Canales Web/Html5", action="canales", url=host+"index.php", thumbnail="http://i.imgur.com/DegBUpj.png",fanart="http://i.imgur.com/bCn8lHB.jpg?1", folder=True))

    return itemlist


def canales(item):
    logger.info("pelisalacarta.channels.tugoleada canales")
    itemlist = []

    data = scrapertools.cachePage(item.url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)

    bloque = scrapertools.find_single_match(data, item.title.upper()+'(.*?)</ul></li>')
    patron = '<a href="([^"]+)">(.*?)</a>'
    matches = scrapertools.find_multiple_matches(bloque, patron)

    for scrapedurl, scrapedtitle  in matches:
        scrapedurl = host + scrapedurl
        scrapedtitle = "[COLOR darkorange]"+scrapedtitle.strip()+"[/COLOR] [COLOR green]["+ \
                       item.title.replace('Canales ','')+"][/COLOR]"
        itemlist.append(Item(channel=__channel__, title=scrapedtitle, action="play", url=scrapedurl, thumbnail=item.thumbnail, fanart=item.fanart, folder=False))

    return itemlist


def entradas(item):
    logger.info("pelisalacarta.channels.tugoleada entradas")
    itemlist = []

    data = scrapertools.cachePage(item.url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
    patron = '<div class="litd fecha"><b>(.*?)</b>(.*?)</div>' \
             '.*?<div class="litd competicion">(.*?)</div>.*?href=[^>]+>(.*?)</a>' \
             '.*?javascript:abrir_evento\((\d+)\)(.*?)</li>'
    matches = scrapertools.find_multiple_matches(data, patron)

    canales = ['Acestream','Sopcast','Web']
    ucanales = ['a','s','']
    lista = []
    urls = []
    for fecha, hora, torneo, partido, id, check_live  in matches:
        urls.append("http://www.elitegol.com/ajax/abrir_evento.php?id=%s" % id)
        evento = "[COLOR darkorange][B]"+partido+"[/B][/COLOR]"
        torneo = "  [COLOR blue]"+torneo+"[/COLOR]"
        if "EN JUEGO" in check_live: scrapedtitle = "[COLOR red][B]"+fecha+hora+"[/B][/COLOR] " + evento + torneo
        else: scrapedtitle = "[COLOR green][B]"+fecha+hora+"[/B][/COLOR] " + evento + torneo
        lista.append(item.clone(channel=__channel__, title=scrapedtitle, action="do_nothing", url="", fulltitle=evento, folder=False))

    try:
        from multiprocessing.dummy import Pool as ThreadPool
        thread = ThreadPool()
        results = thread.map(scrapertools.downloadpageWithoutCookies, urls)
        thread.close()
        thread.join()
    except:
        results = []
        for url_ajax in urls:
            data_result = scrapertools.downloadpageWithoutCookies(url_ajax)
            results.append(data_result)
    
    prox_eventos = []
    for i, data in enumerate(results):
        busqueda = re.search(r'(?i)tugoleada', data, flags=re.DOTALL)
        if busqueda:
            itemlist.append(lista[i])
            canal = scrapertools.find_single_match(data, '(?i)>(?:\w+|\s*|)Tugoleada.*?(\d+).*?</a>')
            fulltitle = lista[i].fulltitle
            for i in range(0, len(canales)):
                scrapedurl = host + "canal" + canal + ucanales[i] + ".php"
                scrapedtitle = "      [COLOR green]CANAL "+canal+" [/COLOR][COLOR indianred][" \
                               +canales[i]+"][/COLOR]"
                itemlist.append(item.clone(channel=__channel__, title=scrapedtitle, action="play", url = scrapedurl, server="p2p", fulltitle=fulltitle, folder=False))
        else:
            prox_eventos.append(lista[i])

    itemlist.append(item.clone(action="do_nothing", title="", folder=False))            
    itemlist.append(item.clone(action="do_nothing", title="[COLOR magenta][B]Posibles próximos eventos (No confirmados)[/B][/COLOR]", folder=False))
    for evento in prox_eventos:
        itemlist.append(evento)

    return itemlist


def do_nothing(item):
    return


def play(item):
    itemlist = []
    data = scrapertools.cachePage(item.url)
    if "Web" in item.title:
        url = scrapertools.find_single_match(data, "(?:source|file):\s*['\"]([^'\"]+)['\"]") + "|Referer="+item.url
        itemlist.append(Item(channel=__channel__, title=item.title, server="directo", url=url, action="play", folder=False))
    else:
        url = scrapertools.find_single_match(data, 'Abrir canal en.*?href="([^"]+)"')
        url += "|"+item.fulltitle 
        itemlist.append(Item(channel=__channel__, title=item.title, server="p2p", url=url, action="play", folder=False))

    return itemlist
