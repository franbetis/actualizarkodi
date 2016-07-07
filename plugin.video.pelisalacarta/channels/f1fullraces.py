# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para F1FullRaces
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import re
from core import logger
from core import config
from core import scrapertools
from servers import servertools
from core.item import Item

__channel__ = "f1fullraces"
__type__ = "generic"
__title__ = "F1FullRaces"
__language__ = "ES"

DEBUG = config.get_setting("debug")


def isGeneric():
    return True


def mainlist(item):
    logger.info("pelisalacarta.channels.f1fullraces mainlist")
    itemlist = []

    itemlist.append(Item(channel=__channel__, title="Novedades", url="http://f1fullraces.com/", action="novedades", thumbnail="http://i.imgur.com/QiUQLui.jpg", fanart="http://i.imgur.com/qo3393W.jpg?1"))
    itemlist.append(Item(channel=__channel__, title="Temporadas F1", url="http://f1fullraces.com/", action="temporadas", thumbnail="http://i.imgur.com/QiUQLui.jpg", fanart="http://i.imgur.com/NjRRsg7.jpg?1"))

    return itemlist


def novedades(item):
    logger.info("pelisalacarta.channels.f1fullraces novedades")
    itemlist = []
    data = scrapertools.cachePage(item.url)

    patron = '<div class="content-list-thumb">.*?<a href="([^"]+)" title="([^"]+)"' \
             '.*?src="([^"]+)"'
    matches = scrapertools.find_multiple_matches(data, patron)
    for scrapedurl, scrapedtitle, scrapedthumbnail  in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle).replace("Round","Carrera")
        scrapedtitle = scrapedtitle.split("Prix")[0]+"Prix"
        title1 = scrapedtitle.rsplit("–",1)[0]
        title2 = scrapedtitle.rsplit("–",1)[1]
        scrapedtitle = "[COLOR darkorange]"+title1+"-[/COLOR]"+"[COLOR green]"+title2+"[/COLOR]"
        itemlist.append(Item(channel=__channel__, title=scrapedtitle, url=scrapedurl, action="findvideos", thumbnail=scrapedthumbnail, fanart=item.fanart, folder=True))
    
    next = scrapertools.find_single_match(data, '<a class="next page-numbers" href="([^"]+)"')
    if len(next) > 0:
        itemlist.append(Item(channel=__channel__, title=">> Siguiente", url=next, action="novedades", thumbnail=item.thumbnail, fanart=item.fanart, folder=True))
    
    return itemlist

def temporadas(item):
    logger.info("pelisalacarta.channels.f1fullraces temporadas")
    itemlist = []
    data = scrapertools.cachePage(item.url)

    patron = '<option.*?>.*?(\d+)</option>'
    matches = scrapertools.find_multiple_matches(data, patron)
    for year  in matches:
        scrapedurl = "http://f1fullraces.com/category/full-race/%s/" % year
        scrapedtitle = "[COLOR darkorange]Temporada: [/COLOR][COLOR green]"+year+"[/COLOR]"
        itemlist.append(Item(channel=__channel__, title=scrapedtitle, url=scrapedurl, action="novedades", thumbnail=item.thumbnail, fanart=item.fanart, folder=True))
    
    itemlist.reverse()
    return itemlist


def findvideos(item):
    logger.info("pelisalacarta.channels.f1fullraces findvideos")
    itemlist= []
    data = scrapertools.cachePage(item.url)
    data = re.sub(r"\n|\r|\t", '', data)
    
    bloque = scrapertools.find_single_match(data, '<div class="entry-content">(.*?)</div>')
    bloque = bloque.replace("<p>","").replace("</p>","").replace("<em>","").replace("<br />","") \
                    .replace("</em>","").replace("<strong>","").replace("</strong>","") \
                    .replace("<b>","").replace("</b>","").replace("<i>","").replace("</i>","") \
                    .replace("<del>","").replace("</del>","").replace("<center>","").replace("</center>","")

    urls = scrapertools.find_multiple_matches(data, '(?i)(>)<iframe.*?src="([^"]+)"')
    if len(urls) > 1:
        urls = scrapertools.find_multiple_matches(bloque, '(?i)(.*?)<iframe.*?src="([^"]+)".*?</iframe>')

    for title, url in urls:
        if "drive.google" in url or "yourvideohost" in url or "filepup" in url:
            if title != ">":
                scrapedtitle = "[COLOR orange]"+title+"    [/COLOR]Enlace encontrado en "+scrapertools.find_single_match(url,'//(?:www.|)(\w+)')
            else:
                scrapedtitle = "Enlace encontrado en "+scrapertools.find_single_match(url,'//(?:www.|)(\w+)')
            itemlist.append( Item(channel=__channel__ , action="play" , title=scrapedtitle, url=url, thumbnail=item.thumbnail, fanart=item.fanart, folder=False))
        else: 
            video_itemlist = servertools.find_video_items(data=url)
            for video_item in video_itemlist:
                if title != ">": 
                    if title.count(':') > 1: scrapedtitle = "[COLOR orange]"+title.rsplit(':',2)[1]+":   [/COLOR]"+video_item.title
                    else: scrapedtitle = "[COLOR orange]"+title+"    [/COLOR]"+video_item.title
                else: scrapedtitle = video_item.title
                itemlist.append( Item(channel=__channel__ , action="play" , server=video_item.server, title=scrapedtitle, url=video_item.url, thumbnail=item.thumbnail, fanart=item.fanart, folder=False))

    if len(itemlist) == 0:
        urls_f1gp = scrapertools.find_multiple_matches(data, '<p style="text-align: center;">(.*?)</p>.*?src="([^"]+)"')
        for title, url in urls_f1gp:
            scrapedtitle = "[COLOR orange]"+title+"    [/COLOR]Enlace encontrado en directo"
            itemlist.append( Item(channel=__channel__ , action="play" , server="directo", title=scrapedtitle, url=url, thumbnail=item.thumbnail, fanart=item.fanart, folder=False))
    return itemlist

def play(item):
    logger.info("pelisalacarta.channels.f1fullraces play")
    itemlist = []
    if "drive.google" in item.url:
        data = scrapertools.cachePage(item.url)
        url = scrapertools.find_single_match(data, '"fmt_stream_map".*?(https.*?),')
        video_url = url.decode('unicode-escape')
        itemlist.append( Item(channel=__channel__ , action="play" , server="directo", title=item.title, url=video_url, thumbnail=item.thumbnail, folder=False))
    elif "yourvideohost" in item.url:
        data = scrapertools.cachePage(item.url)
        video_url = scrapertools.find_single_match(data, 'file:.*?"([^"]+)"')
        itemlist.append( Item(channel=__channel__ , action="play" , server="directo", title=item.title, url=video_url, thumbnail=item.thumbnail, folder=False))
    elif "filepup" in item.url:
        data = scrapertools.cachePage(item.url)
        video_url = scrapertools.find_single_match(data, 'sources: \[.*?src:.*?"([^"]+)"')
        video_url += '|User-Agent=Magic Browser'
        itemlist.append( Item(channel=__channel__ , action="play" , server="directo", title=item.title, url=video_url, thumbnail=item.thumbnail, folder=False))
    else:
        itemlist.append( Item(channel=__channel__ , action="play" , server=item.server, title=item.title, url=item.url, thumbnail=item.thumbnail, folder=False))

    return itemlist
