# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para Miscelánea
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import os, re, xbmc, urllib

from core import scrapertools
from core import logger
from core import config
from core.item import Item

__channel__ = "miscelanea_p2p"
__category__ = "d"
__type__ = "generic"
__title__ = "Miscelánea"
__language__ = "ES"

song = os.path.join(config.get_runtime_path(), 'music', 'Survivor - eye of the tiger.mp3')
DEBUG = config.get_setting("debug")


def isGeneric():
    return True


def mainlist(item):
    logger.info("pelisalacarta.channels.miscelanea_p2p mainlist")
    itemlist = []
    
    xbmc.executebuiltin('xbmc.PlayMedia('+song+')')

    itemlist.append(Item(channel=__channel__, title="[COLOR teal]Enlaces sin canal asociado[/COLOR]", action="canales", url="", thumbnail="http://s6.postimg.org/etyqbs3o1/miscelania.png",fanart="http://i.imgur.com/Bt9PHVR.jpg?1", folder=True))
    itemlist.append(Item(channel=__channel__, title="", action="", thumbnail="http://s6.postimg.org/etyqbs3o1/miscelania.png", fanart="http://i.imgur.com/Bt9PHVR.jpg?1", folder=False))
    itemlist.append(Item(channel=__channel__, title="[COLOR darkgreen]Reproducir enlace Acestream[/COLOR]", action="p2p", thumbnail="http://i.imgur.com/0kq0Jx6.png",fanart="http://i.imgur.com/Bt9PHVR.jpg?1", folder=False))
    itemlist.append(Item(channel=__channel__, title="[COLOR seagreen]Reproducir enlace Sopcast[/COLOR]", action="p2p", thumbnail="http://i.imgur.com/0kq0Jx6.png",fanart="http://i.imgur.com/Bt9PHVR.jpg?1", folder=False))

    return itemlist


def p2p(item):
    if "Sopcast" in item.title:
        texto = dialog_input(default='sop://broker.sopcast.com:3912/', heading="Introduce la url de sopcast")
        titulo = "[Sopcast]"
    else:
        texto = dialog_input(default='acestream://', heading="Introduce la url de acestream")
        titulo = "[Acestream]"
    if texto != "":
        url = texto + "|" + titulo
        from platformcode import xbmctools
        item_play = item.clone()
        item_play.url = url
        item_play.server = "p2p"
        xbmctools.play_video(item_play)


def canales(item):
    logger.info("pelisalacarta.channels.miscelanea_p2p canales")
    itemlist = []

    itemlist.append(Item(channel=__channel__, title="[COLOR teal]PremierTv Canal 1[/COLOR]", action="play", url="http://premiertv.pw/1/ifi.html", thumbnail="http://i.imgur.com/o7sosoD.png",fanart="http://i.imgur.com/FtrAOlU.jpg", folder=False))
    itemlist.append(Item(channel=__channel__, title="[COLOR teal]Elgoles[/COLOR]", action="elgoles", url="http://elgoles2017.blogspot.com.es", thumbnail="http://s6.postimg.org/5w3t949ld/streamsportsfutbolthumb.png",fanart="http://s6.postimg.org/sm2y23ssx/streamsportsfutbolfan.jpg", folder=True))
    itemlist.append(Item(channel=__channel__, title="[COLOR teal]DHD1[/COLOR]", action="dhd1", url="http://deporteshd1.blogspot.com.es/", thumbnail="http://i.imgur.com/K7SiYi5.jpg?1",fanart="http://i.imgur.com/Ww2Dahm.jpg?1", folder=True))

    return itemlist


def elgoles(item):
    logger.info("pelisalacarta.channels.miscelanea_p2p elgoles")
    itemlist = []

    try:
        from servers import servertools
    except:
        from core import servertools
        
    data = scrapertools.downloadpage(item.url)
    bloque = scrapertools.find_single_match(data, '<h2>Páginas</h2>.*?<ul>(.*?)</ul>')
    matches = scrapertools.find_multiple_matches(bloque, "<a href='([^']+)'>(.*?)</a>")
    for scrapedurl, scrapedtitle in matches:
        scrapedtitle = "[COLOR crimson]"+scrapedtitle.capitalize()+"[/COLOR]"
        data = scrapertools.downloadpageWithoutCookies(scrapedurl)
        urls = servertools.findvideosbyserver(data, "p2p")
        if urls:
            scrapedtitle += "   [COLOR darkcyan]"+urls[0][0]+"[/COLOR]"
            itemlist.append(item.clone(url=scrapedurl, action="play", title=scrapedtitle, folder=False))
    
    return itemlist


def dhd1(item):
    logger.info("pelisalacarta.channels.miscelanea_p2p dhd1")
    itemlist = []
        
    data = scrapertools.downloadpage(item.url)
    bloque = scrapertools.find_single_match(data, "ACE 24/7</a>(.*?)<a href='#'>Flash")
    matches = scrapertools.find_multiple_matches(bloque, "<a href='(http://[^']+)'.*?>(.*?)</a>")
    for scrapedurl, scrapedtitle in matches:
        scrapedtitle = "[COLOR crimson]"+scrapedtitle+"[/COLOR]"
        itemlist.append(item.clone(url=scrapedurl, action="play", title=scrapedtitle, extra="dhd1", folder=False))
 
    bloque = scrapertools.find_single_match(data, "<a href='#'>Flash(.*?)<a href='#'>DHD1")
    matches = scrapertools.find_multiple_matches(bloque, "<a href='(http://[^']+)'.*?>(.*?)</a>")
    url_prefix = ['cp','cp','cp','cp','cp','','','','','']
    url_sufix = ['bull','cl','fut','cd','cd2','mf1','mgp','bnesp','espt','plus0']
    for i, match in enumerate(matches):
        scrapedtitle = "[COLOR crimson]"+match[1]+"[/COLOR]  [COLOR darkcyan][Flash][/COLOR]"
        scrapedurl = "http://dhd1.ml/%sdhd%s.php" % (url_prefix[i], url_sufix[i])
        itemlist.append(item.clone(url=scrapedurl, action="play_flash", title=scrapedtitle, folder=False))
    return itemlist


def play(item):
    logger.info("pelisalacarta.channels.miscelanea_p2p play")
    itemlist = []
    xbmc.executebuiltin('xbmc.PlayMedia(Stop)')

    try:
        from servers import servertools
    except:
        from core import servertools

    data = scrapertools.downloadpage(item.url)

    # Si el canal está en la web se busca manualmente el enlace ya que puede haber varios
    if item.extra == "dhd1":
        url = scrapertools.find_single_match(data, 'href="(acestream://[^"]+)"')
        if url == "":
            redirect = scrapertools.find_single_match(data, 'src="(http://buker[^"]+)"')
            data = scrapertools.downloadpage(redirect)
            urls = servertools.findvideosbyserver(data, "p2p")
            if urls:
                url = urls[0][1] +"|" + item.title
                itemlist.append(item.clone(url=url, server="p2p"))
        else:
            url += "|" + item.title
            itemlist.append(item.clone(url=url, server="p2p"))
    else:
        # Se automatiza la búsqueda del enlace acestream/sopcast a través del conector p2p
        urls = servertools.findvideosbyserver(data, "p2p")
        if urls:
            url = urls[0][1]+"|" + item.title
            itemlist.append(item.clone(url=url, server="p2p"))
        
    return itemlist


def play_flash(item):
    logger.info("pelisalacarta.channels.miscelanea_p2p play_flash")
    xbmc.executebuiltin('xbmc.PlayMedia(Stop)')
    data = scrapertools.downloadpage(item.url)

    url = scrapertools.find_single_match(data, 'src="(http://www.sunhd[^"]+)"')
    if url == "":
        url = scrapertools.find_single_match(data, 'src="(http://verdirecto[^"]+)"')

    url_dev = "catcher=%s&url=%s&referer=%s" % ("streams", url, item.url)
    xbmc.executebuiltin("XBMC.RunPlugin(plugin://plugin.video.SportsDevil/?item=%s&mode=1)" % urllib.quote_plus(url_dev))


def dialog_input(default="", heading="", hidden=False):
    keyboard = xbmc.Keyboard(default, heading, hidden)
    keyboard.doModal()
    if (keyboard.isConfirmed()):
        return keyboard.getText()
    else:
        return ""
