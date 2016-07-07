# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para 9score
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import re
from core import logger
from core import config
from core import scrapertools
from core.item import Item

__channel__ = "ninescore"
__type__ = "generic"
__title__ = "9score"
__language__ = "ES"

DEBUG = config.get_setting("debug")
host = "http://www.9score.com"


def isGeneric():
    return True


def mainlist(item):
    logger.info("pelisalacarta.channels.9score mainlist")
    itemlist = []

    itemlist.append(Item(channel=__channel__, title="Agenda/Directos" , action="agenda", url="http://www.9score.com/live-football-sopcast-link.html", thumbnail="http://s6.postimg.org/as7g0t9qp/STREAMSPORTAGENDA.png",fanart="http://s6.postimg.org/5utvfp7rl/streamsportonairfan.jpg", folder=True))
    itemlist.append(Item(channel=__channel__, title="Partidos Completos" , action="partidos", url="http://www.9score.com/fullmatch", thumbnail="http://s6.postimg.org/5w3t949ld/streamsportsfutbolthumb.png",fanart="http://s6.postimg.org/sm2y23ssx/streamsportsfutbolfan.jpg", folder=True))
    itemlist.append(Item(channel=__channel__, title="Resúmenes" , action="resumenes", url="http://www.9score.com/highlights", thumbnail="http://s6.postimg.org/5w3t949ld/streamsportsfutbolthumb.png",fanart="http://s6.postimg.org/sm2y23ssx/streamsportsfutbolfan.jpg", folder=True))

    return itemlist


def agenda(item):
    logger.info("pelisalacarta.channels.9score agenda")
    itemlist = []
    data = scrapertools.cachePage(item.url)
    data = re.sub(r"\n|\r|\t", '', data)

    bloque = scrapertools.find_multiple_matches(data, '<div class="leaguelogo column">(.*?)</li>')
    for match in bloque:
        patron = 'alt="([^"]+)".*?starttime time">(\d+):(\d+)<.*?endtime time">(.*?)<' \
                 '.*?alt="([^"]+)" src="([^"]+)".*?alt="([^"]+)" src="([^"]+)"' \
                 '.*?live_btn column"><a href="([^"]+)".*?style="color:#([^;]+)'
        matches = scrapertools.find_multiple_matches(match, patron)
        for liga, hora, minutos, fecha, team1, team1image, team2, team2image, scrapedurl, live in matches:
            scrapedthumbnail = host+team1image.replace('small/','big/').replace('.jpg','.png')
            if "no_image" in scrapedthumbnail:
                scrapedthumbnail = host+team2image.replace('small/','big/').replace('.jpg','.png')
                if "no_image" in scrapedthumbnail: scrapedthumbnail = item.thumbnail

            scrapedurl = host+scrapedurl
            team1 = scrapertools.decodeHtmlentities(team1)
            team2 = scrapertools.decodeHtmlentities(team2)
            fulltitle = "[COLOR darkorange]"+team1+" vs "+team2+"[/COLOR]"
            if int(hora)+2 >= 24:
                if hora == "22": hora = "00"
                elif hora == "23": hora = "01"
            else:
                hora = str(int(hora)+2)
        
            if "3434" in live:
                fecha = "[COLOR green]["+fecha+"] "+hora+":"+minutos+" [/COLOR]"
            else:
                fecha = "[COLOR red]["+fecha+"] "+hora+":"+minutos+" [/COLOR]"
        
            scrapedtitle = fecha + fulltitle + " [COLOR blue]("+liga+")[/COLOR]"
            itemlist.append(Item(channel=__channel__, title=scrapedtitle, url=scrapedurl, action="p2p", thumbnail=scrapedthumbnail, fanart=item.fanart, fulltitle=fulltitle, folder=True))
    
    next_page = scrapertools.find_single_match(data, 'rel="next" href="([^"]+)"')
    if len(next_page) > 0:
        itemlist.append(Item(channel=__channel__, title=">> Siguiente", url=host+next_page, action="agenda", thumbnail=item.thumbnail, fanart=item.fanart, folder=True))

    return itemlist


def partidos(item):
    logger.info("pelisalacarta.channels.9score partidos")
    itemlist = []
    data = scrapertools.cachePage(item.url)
    data = re.sub(r"\n|\r|\t", '', data)

    patron = '<div class="cover">.*?href="([^"]+)".*?title="([^"]+)".*?' \
             'src="([^"]+)".*?longdate">(\d+)-(\d+)-(\d+)<'
    matches = scrapertools.find_multiple_matches(data, patron)
    for scrapedurl, scrapedtitle, scrapedthumbnail, mes, dia, year in matches:
        scrapedurl = host + scrapedurl
        scrapedthumbnail = host + scrapedthumbnail
        scrapedtitle = "[COLOR darkorange]"+scrapedtitle+"[/COLOR] [COLOR red]["+dia+"/"+mes+"/"+year+"][/COLOR]"
        itemlist.append(Item(channel=__channel__, title=scrapedtitle, url=scrapedurl, action="findvideos", thumbnail=scrapedthumbnail, fanart=item.fanart, folder=True))
    
    next_page = scrapertools.find_single_match(data, '<span class=\'current\'>[^<]+</span><a href="([^"]+)"')
    if len(next_page) > 0:
        itemlist.append(Item(channel=__channel__, title=">> Siguiente", url=host+next_page, action="partidos", thumbnail=item.thumbnail, fanart=item.fanart, folder=True))
    return itemlist

    
def resumenes(item):
    logger.info("pelisalacarta.channels.9score resumenes")
    itemlist = []
    data = scrapertools.cachePage(item.url)
    data = re.sub(r"\n|\r|\t", '', data)

    bloque = scrapertools.find_multiple_matches(data, '<div class="leaguelogo column">(.*?)</li>')
    for match in bloque:
        patron = 'alt="([^"]+)".*?shortdate">(.*?)<.*?alt="([^"]+)" src="([^"]+)"' \
                 '.*?alt="([^"]+)" src="([^"]+)".*?play_btn column"><a href="([^"]+)"'
        matches = scrapertools.find_multiple_matches(match, patron)
        for liga, fecha, team1, team1image, team2, team2image, scrapedurl in matches:
            scrapedthumbnail = host+team1image.replace('small/','big/').replace('.jpg','.png')
            if "no_image" in scrapedthumbnail:
                scrapedthumbnail = host+team2image.replace('small/','big/').replace('.jpg','.png')
                if "no_image" in scrapedthumbnail: scrapedthumbnail = item.thumbnail

            scrapedurl = host+scrapedurl
            fulltitle = "[COLOR darkorange]"+team1+" vs "+team2+"[/COLOR]"
            fecha = "[COLOR red]["+fecha+"][/COLOR] "
            scrapedtitle = fecha + fulltitle + " [COLOR blue]("+liga+")[/COLOR]"
            itemlist.append(Item(channel=__channel__, title=scrapedtitle, url=scrapedurl, action="findvideos", thumbnail=scrapedthumbnail, fanart=item.fanart, fulltitle=fulltitle, folder=True))
    
    next_page = scrapertools.find_single_match(data, '<span class=\'current\'>[^<]+</span><a href="([^"]+)"')
    if len(next_page) > 0:
        itemlist.append(Item(channel=__channel__, title=">> Siguiente", url=host+next_page, action="resumenes", thumbnail=item.thumbnail, fanart=item.fanart, folder=True))
    return itemlist


def p2p(item):
    logger.info("pelisalacarta.channels.9score p2p")
    itemlist = []
    data = scrapertools.cachePage(item.url)
    data = re.sub(r"\n|\r|\t", '', data)

    try:
        patron = "<td align='left'>.*?</td><td>(.*?)</td><td>(.*?)</td>.*?href='([^']+)'"
        matches = scrapertools.find_multiple_matches(data, patron)

        acestream = False
        sopcast = False
        for idioma, bitrate, scrapedurl in matches:
            if not scrapedurl.startswith('sop') and not scrapedurl.startswith('acestream'): continue
            if scrapedurl.startswith('sop') and not sopcast:
                itemlist.append(Item(channel=__channel__, title="[COLOR green]Enlaces SOPCAST:[/COLOR]", url="", action="", thumbnail=item.thumbnail, fanart=item.fanart, folder=False))
                sopcast = True
            if scrapedurl.startswith('acestream') and not acestream:
                itemlist.append(Item(channel=__channel__, title="[COLOR green]Enlaces ACESTREAM:[/COLOR]", url="", action="", thumbnail=item.thumbnail, fanart=item.fanart, folder=False))
                acestream = True
            scrapedtitle = "     "+item.fulltitle
            if idioma != "":
                idioma = idioma.replace('tiếng Nga','Ruso').replace('tiếng TBN','Español').replace('tiếng Anh','Inglés')
                scrapedtitle += " [COLOR sienna]["+idioma+"][/COLOR]"
            if bitrate != "":
                scrapedtitle += " [COLOR orangered]("+bitrate+")[/COLOR]"
            scrapedurl += "|"+item.fulltitle
            itemlist.append(Item(channel=__channel__, title=scrapedtitle, url=scrapedurl, action="play", server="p2p", thumbnail=item.thumbnail, fanart=item.fanart, folder=False))
    except:
        pass

    if len(itemlist) == 0:
        itemlist.append(Item(channel=__channel__, title="[COLOR green]No hay enlaces disponibles todavía para este partido[/COLOR]", url="", action="", thumbnail=item.thumbnail, fanart=item.fanart, folder=False))

    return itemlist
