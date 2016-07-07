# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para Full Matches & Shows
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "fullmatches"
__type__ = "generic"
__title__ = "Full Matches & Shows"
__language__ = "ES"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("pelisalacarta.channels.fullmatches mainlist")
    itemlist = []
    itemlist.append(Item(channel=__channel__, title="Novedades" , action="novedades", url="http://www.fullmatchesandshows.com/", thumbnail=item.thumbnail, fanart=item.fanart))
    itemlist.append(Item(channel=__channel__, title="Competiciones" , action="categorias", url="http://www.fullmatchesandshows.com/", thumbnail=item.thumbnail, fanart=item.fanart))
    itemlist.append(Item(channel=__channel__, title="Buscar..."      , action="search", thumbnail=item.thumbnail, fanart=item.fanart))

    return itemlist

def search(item,texto):
    logger.info("pelisalacarta.channels.fullmatches search")
    itemlist = []
    item.url = "http://www.fullmatchesandshows.com/?s=" + texto
    return busqueda(item)

def novedades(item):
    logger.info("pelisalacarta.channels.fullmatches novedades")
    itemlist = []
    if item.url.startswith("action"):
        data = scrapertools.cachePage("http://www.fullmatchesandshows.com/wp-admin/admin-ajax.php?td_theme_name=Newspaper&v=6.5.1", post=item.url)
        data = scrapertools.decodeHtmlentities(data)
        data = data.replace("\\","")
        current_page = scrapertools.find_single_match(item.url, 'td_current_page=(\d+)&')
        max_page = item.extra
        next_page = ""
    else:
        data = scrapertools.cachePage(item.url)
        data = scrapertools.decodeHtmlentities(data)
        current_page = "1"
        max_page = 0
        next_page = scrapertools.find_single_match(data, '<a href="([^"]+)"><i class="td-icon-menu-right">')
        if next_page == "":
            block = scrapertools.find_single_match(data, 'id="next-page-([^"]+)"')
            if block != "":
                max_page = scrapertools.find_single_match(data, block+'.max_num_pages = "([^"]+)"')
                atts = "&td_atts="+scrapertools.find_single_match(data, block+".atts = '([^']+)'")
                id = "&td_block_id="+scrapertools.find_single_match(data, block+'.id = "([^"]+)"')
                type = "&block_type="+scrapertools.find_single_match(data, block+'.block_type = "([^"]+)"')
                column = "&td_column_number="+scrapertools.find_single_match(data, block+'.td_column_number = "([^"]+)"')
                item.url = "action=td_ajax_block"+ atts + id + column + "&td_current_page="+ current_page + type

    matches = scrapertools.find_multiple_matches(data, '<div class="td-block-span4">.*?<div class="td-module-thumb"><a href="([^"]+)".*?title="([^"]+)".*?src="(.*?)(?:"|\?resize)')
    for scrapedurl, scrapedtitle, scrapedthumbnail in matches:
        scrapedtitle = scrapedtitle.replace("Highlights","Resumen").replace("Full Match", "Partido Completo")
        itemlist.append(Item(channel=__channel__, title=scrapedtitle, url=scrapedurl, action="findvideos", thumbnail=scrapedthumbnail, folder=True))


    if int(current_page) < int(max_page) and next_page == "":
        page = int(current_page) + 1
        next_page = item.url.replace('td_current_page='+current_page, 'td_current_page='+str(page))

    if next_page != "": itemlist.append(Item(channel=__channel__, title=">> Siguiente", url=next_page, action="novedades", extra=max_page, thumbnail=item.thumbnail, folder=True))

    return itemlist

def entradas(item):
    logger.info("pelisalacarta.channels.fullmatches entradas")
    itemlist = []
    data = scrapertools.cachePage(item.url)
    data = scrapertools.decodeHtmlentities(data)

    if item.extra == "1":
        matches = scrapertools.find_multiple_matches(data, '(?:<div class="td_module_mx|<div class="td-block-span4">).*?<div class="td-module-thumb"><a href="([^"]+)".*?title="([^"]+)".*?src="(.*?)(?:"|\?resize)')
    else:
        matches = scrapertools.find_multiple_matches(data, '<div class="td-block-span4">.*?<div class="td-module-thumb"><a href="([^"]+)".*?title="([^"]+)".*?src="(.*?)(?:"|\?resize)')
    for scrapedurl, scrapedtitle, scrapedthumbnail in matches:
        scrapedtitle = scrapedtitle.replace("Highlights","Resumen").replace("Full Match", "Partido Completo")
        itemlist.append(Item(channel=__channel__, title=scrapedtitle, url=scrapedurl, action="findvideos", thumbnail=scrapedthumbnail, folder=True))

    next_page = scrapertools.find_single_match(data, '<a href="([^"]+)"><i class="td-icon-menu-right">')
    if next_page != "":
        itemlist.append(Item(channel=__channel__, title=">> Siguiente", url=next_page, action="novedades", thumbnail=item.thumbnail, folder=True))

    return itemlist

def categorias(item):
    logger.info("pelisalacarta.channels.fullmatches categorias")
    itemlist = []
    data = scrapertools.cachePage(item.url)
    data = scrapertools.decodeHtmlentities(data)

    bloque = scrapertools.find_single_match(data, '(<ul class="sub-menu">.*?</ul>)')

    matches = scrapertools.find_multiple_matches(bloque, '<a href="([^"]+)">(.*?)</a>')
    for scrapedurl, scrapedtitle in matches:
        if scrapedtitle == "La Liga": scrapedurl = "http://www.fullmatchesandshows.com/category/la-liga/"
        if scrapedtitle == "Champions League": continue
        if "category/" in scrapedurl: action = "entradas"
        else: action = "novedades"
        itemlist.append(Item(channel=__channel__, title=scrapedtitle, url=scrapedurl, action=action, thumbnail=item.thumbnail, extra= "1", folder=True))

    post = 'action=td_ajax_block&td_atts={"custom_title":"Latest Highlights and Full Matches","limit":"18","td_ajax_filter_type"' \
           ':"td_category_ids_filter","td_filter_default_txt":"All","ajax_pagination":"next_prev","td_ajax_filter_ids"' \
           ':"499,2,79,28,49,94,65,23,55,432","category_ids":"94, 65, 218, 233","class":"td_block_id_1991998159 td_uid_1_57080d828ccaf_rand"}' \
           '&td_block_id=td_uid_1_57080d828ccaf&td_column_number=3&td_current_page=1&block_type=td_block_3&td_filter_value=%s'

    itemlist.insert(4, Item(channel=__channel__, title="Champions League", url=post % "49", action="novedades", extra="10", thumbnail=item.thumbnail, folder=True))
    itemlist.insert(5, Item(channel=__channel__, title="Europa League", url=post % "55", action="novedades", extra="10", thumbnail=item.thumbnail, folder=True))
    itemlist.append(Item(channel=__channel__, title="Shows", url=post % "65", action="novedades", extra="10", thumbnail=item.thumbnail, folder=True))
    itemlist.append(Item(channel=__channel__, title="Competiciones de Inglaterra", url=post % "499", action="novedades", extra="10", thumbnail=item.thumbnail, folder=True))
    itemlist.append(Item(channel=__channel__, title="Competiciones de España", url=post % "2", action="novedades", extra="10", thumbnail=item.thumbnail, folder=True))
    itemlist.append(Item(channel=__channel__, title="Competiciones de Italia", url=post % "28", action="novedades", extra="10", thumbnail=item.thumbnail, folder=True))
    itemlist.append(Item(channel=__channel__, title="Competiciones de Alemania", url=post % "79", action="novedades", extra="10", thumbnail=item.thumbnail, folder=True))
    itemlist.append(Item(channel=__channel__, title="Competiciones de Francia", url=post % "23", action="novedades", extra="10", thumbnail=item.thumbnail, folder=True))

    return itemlist

def findvideos(item):
    logger.info("pelisalacarta.channels.fullmatches findvideos")
    itemlist = []
    if item.extra == "":
        data = scrapertools.cachePage(item.url)
        data = scrapertools.decodeHtmlentities(data)
        acp = "&acp_pid="+scrapertools.find_single_match(data,'<input id="acp_post".*?value="([^"]+)"/>')
        acp_shortcode = "&acp_shortcode="+scrapertools.find_single_match(data,'<input id="acp_shortcode".*?value="([^"]+)"/>')
        matches = scrapertools.find_multiple_matches(data, 'id="item.*?"><a href="([^"]+)"><div.*?>(.*?)</div>')
        if len (matches) > 1:
            for scrapedurl, scrapedtitle in matches:
                scrapedtitle = scrapedtitle \
                            .replace("HL ", "Resumen ").replace("Extended","Extendido") \
                            .replace("1st half ", "1ª parte ").replace("2nd half ","2ª parte ") \
                            .replace("Pre-Match", "Pre-partido").replace("Post-Match","Post-Partido")
                post = "acp_currpage=" + scrapedurl.replace("#","") + acp + acp_shortcode + "&action=pp_with_ajax"
                itemlist.append(Item(channel=__channel__, title=scrapedtitle, url=item.url, action="findvideos", thumbnail=item.thumbnail, extra=post, folder=True))
        else:
            itemlist = servertools.find_video_items(data=data)
            for item in itemlist:
                item.channel = __channel__
    else:
        post = item.extra
        data = scrapertools.cachePage("http://www.fullmatchesandshows.com/wp-admin/admin-ajax.php", post=post)
        itemlist = servertools.find_video_items(data=data)
        for item in itemlist:
            item.channel = __channel__

    return itemlist

def busqueda(item):
    logger.info("pelisalacarta.channels.fullmatches busqueda")
    itemlist = []
    data = scrapertools.cachePage(item.url)
    data = scrapertools.decodeHtmlentities(data)

    matches = scrapertools.find_multiple_matches(data, '<div class="td-block-span6">.*?<div class="td-module-thumb"><a href="([^"]+)".*?title="([^"]+)".*?src="(.*?)(?:"|\?resize)')
    for scrapedurl, scrapedtitle, scrapedthumbnail in matches:
        itemlist.append(Item(channel=__channel__, title=scrapedtitle, url=scrapedurl, action="findvideos", thumbnail=scrapedthumbnail, folder=True))


    next_page = scrapertools.find_single_match(data, '<link rel="next" href="([^"]+)"')
    if len (next_page) > 0:
        itemlist.append(Item(channel=__channel__, title=">> Siguiente", url=next_page, action="busqueda", thumbnail=item.thumbnail, folder=True))

    return itemlist