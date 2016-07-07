# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para footballstreaming.com
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os
import sys
import re
from core import scrapertools
from core import logger
from core import config
from core import jsontools
from core.item import Item
from servers import servertools
import xbmc

__channel__ = "footballstreaming"
__category__ = "d"
__type__ = "generic"
__title__ = "Footballstreaming"
__language__ = "ES"

host ="http://www.footballstreamings.com"
song = os.path.join(config.get_runtime_path(), "music", 'Superstition.mp3')

DEBUG = config.get_setting("debug")

def isGeneric():
    
    return True


def mainlist(item):
    logger.info("pelisalacarta.footballstreaming mainlist")
    itemlist = []
    
    xbmc.executebuiltin('xbmc.PlayMedia('+song+')')
   
    itemlist.append( Item(channel=__channel__, title="[COLOR deeppink][B]Sports Channels[/B][/COLOR]"      , action="canales", url="http://www.footballstreamings.com/channels.html", fanart="http://s6.postimg.org/m5ed1akcx/footballstreamingfan1.jpg", thumbnail="http://s6.postimg.org/n8yhd9501/footballstreamingstvthumb.png", folder= True ))
    item.url ="http://www.footballstreamings.com/live-streams.html"
    data = scrapertools.cachePage(item.url)
    
    patronenlaces = '<table width=".*?" border=".*?" style="margin-left: 30px;">.*?src="([^"]+)".*?<h2>(.*?)</h2>(.*?)</tbody>'
    mathchesenlaces=re.compile(patronenlaces,re.DOTALL).findall(data)
    for thumbnail,competition , bloque_enlaces in mathchesenlaces:
        bloque_enlaces= re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",bloque_enlaces)
        
        itemlist.append( Item(channel=__channel__, title="                                            "+"[COLOR cadetblue][B]"+competition+"[/B][/COLOR]"      , action="mainlist", url="", fanart="http://s6.postimg.org/m5ed1akcx/footballstreamingfan1.jpg", thumbnail=urlparse.urljoin(host,thumbnail), folder= False))
    
        patron = '<td width="27%"><strong>.*?(\d\d.\d\dCET).*?</strong></td>.*?<strong>([^"]+)</strong></td>.*?<strong>([^"]+)</strong></td>.*?a href="([^"]+)"'
        matches=re.compile(patron,re.DOTALL).findall(bloque_enlaces)
        for hora, title,league,link in matches:
            hora = hora.replace("CET","")
            hora = hora.replace(hora,"[COLOR chartreuse]"+hora+"[/COLOR]")
            title = fulltitle = title.replace(title,"[COLOR orangered]"+title+"[/COLOR]")
            league = league.replace(league,"[COLOR salmon]"+"("+""+league+")"+"[/COLOR]")
            title = hora +"  "+title+"  "+league

            itemlist.append( Item(channel=__channel__, title=title   , action="enlaces", url=urlparse.urljoin(host,link), fanart="http://s6.postimg.org/m5ed1akcx/footballstreamingfan1.jpg", thumbnail=urlparse.urljoin(host,thumbnail), extra=fulltitle, folder= True))
  


    return itemlist

def enlaces(item):
    logger.info("pelisalacarta.footballstreaming enlaces")
    
    itemlist = []
    
    data = scrapertools.cachePage(item.url)
    data = re.sub(r"<!-- Flash -->|<!-- Table Body -->|<!-- VLC -->|<!-- livetable -->|<!-- <meta|<!-- <script|No VLC Links available for this match","",data)
    
    patronlinks = '<!-- (.*?) -->.*?<img src="([^"]+)".*?(.*?)<!-- .*? -->'
    matcheslinks = re.compile(patronlinks,re.DOTALL).findall(data)
    
    
    for tipo,image, bloque_links in matcheslinks:
        if "Analytics" in tipo:
           continue
        check ="go"
        
        if tipo =="Sopcast" and not "sop://" in bloque_links:
           fanart ="http://s6.postimg.org/5cnp2v7o1/footballstreamingnolinks.jpg"
           thumbnail ="http://s6.postimg.org/u8h4qcuc1/nosopcast.png"
        elif tipo =="Sopcast" and  "sop://" in bloque_links:
             fanart ="http://s6.postimg.org/y3kisxdhr/footballstreamingmatch.jpg"
             thumbnail =urlparse.urljoin(host,image)
        elif tipo =="Acestream" and not "acestream://" in bloque_links:
            fanart ="http://s6.postimg.org/5cnp2v7o1/footballstreamingnolinks.jpg"
            thumbnail = "http://s6.postimg.org/t7gw18dch/noacestream.png"
        else:
            fanart ="http://s6.postimg.org/y3kisxdhr/footballstreamingmatch.jpg"
            thumbnail =urlparse.urljoin(host,image)
        if tipo == "Sopcast":
           tipo = tipo.replace(tipo,"[COLOR skyblue][B]"+tipo+"[/B][/COLOR]")
        else:
           tipo = tipo.replace(tipo,"[COLOR palegreen][B]"+tipo+"[/B][/COLOR]")
        itemlist.append( Item(channel=__channel__, title="                                            "+tipo      , action="mainlist", url="", fanart=fanart, thumbnail=thumbnail, folder= False))
        if '<td width="100%" align="left" valign="middle" colspan="3" ><strong>No' in bloque_links:
            check = "ok"
            if tipo == "Sopcast":
               thumbnail ="http://s6.postimg.org/u8h4qcuc1/nosopcast.png"
            if tipo == "Acestream":
               thumbnail = "http://s6.postimg.org/t7gw18dch/noacestream.png"
            title ="Sin enlaces. Pruebe pasados unos minutos".title()
            itemlist.append( Item(channel=__channel__, title="[COLOR crimson]"+title+"[/COLOR]"     , action="mainlist", url="", fanart="http://s6.postimg.org/5cnp2v7o1/footballstreamingnolinks.jpg", thumbnail=thumbnail, folder= False))
        
        patron = '<strong>(.*?)</strong>.*?<strong>(.*?)</strong>.*?<a href="([^"]+)".*?</a>'
        matches= re.compile(patron,re.DOTALL).findall(bloque_links)

        if  len(matches)==0 and check != "ok":
            title = "Sin enlaces Acestream/Sopcast".title()
            itemlist.append( Item(channel=__channel__, title="[COLOR crimson]"+title+"[/COLOR]"      , action="mainlist", url="", fanart="http://s6.postimg.org/5cnp2v7o1/footballstreamingnolinks.jpg", thumbnail="http://s6.postimg.org/vq2l1wz2p/noacestreamsopcast.png", folder= False))
        for canal,idioma, link in matches:
            canal = canal.replace(canal,"[COLOR goldenrod][B]"+canal+"[/B][/COLOR]")
            idioma = idioma.replace(idioma,"[COLOR plum][B]"+"("+idioma+")"+"[/B][/COLOR]")
            title = canal + " "+idioma
            
            if "More Acestream Sport" in title:
                continue
            itemlist.append( Item(channel=__channel__, title=title      , action="play", url=link, fanart="http://s6.postimg.org/y3kisxdhr/footballstreamingmatch.jpg", thumbnail=urlparse.urljoin(host,image), extra=item.extra, folder= True))

    return itemlist

def canales(item):
    logger.info("pelisalacarta.topbongda scraper")
    
    itemlist = []
    data = scrapertools.cachePage(item.url)
    
    patron_enlace_canal ='<td width="20%" align="left".*?<strong>(.*?)</strong>(.*?)<tr valign="middle">'
    matchescanales= re.compile(patron_enlace_canal,re.DOTALL).findall(data)
    
    for channel, bloque_links in matchescanales:
        if not "acestream" in bloque_links and not "sopcast" in bloque_links:
            continue
        itemlist.append( Item(channel=__channel__, title="[COLOR antiquewhite][B]"+channel+"[/B][/COLOR]"      , action="mailsit", url="", fanart="http://s6.postimg.org/iocayblap/footballstreamingstvtfan.jpg", thumbnail="http://s6.postimg.org/qv4apwbdd/footballstreamingstvthumb2.png", folder= True))
        patron ='<strong>WATCH \d+.*?<a href="(.*?)(:[^"]+)"'
        matches = re.compile(patron,re.DOTALL).findall(bloque_links)
        
        for tipo , link in matches:
            if tipo == "http":
               continue
            title = channel + "("+tipo+")"
            url = str(tipo +  link)
            
            if tipo == "sop":
               tipo = tipo.replace(tipo,"[COLOR skyblue][B]Sopcast[/B][/COLOR]")
            else:
               tipo = tipo.replace(tipo,"[COLOR palegreen][B]Acestream[/B][/COLOR]")
            itemlist.append( Item(channel=__channel__, title="                     "+tipo      , action="play", url=url, fanart="http://s6.postimg.org/iocayblap/footballstreamingstvtfan.jpg", thumbnail="http://s6.postimg.org/qv4apwbdd/footballstreamingstvthumb2.png", extra=channel, folder= True))
    return itemlist

def play(item):
    logger.info("pelisalacarta.footballstreaming play")
    itemlist = []
    import xbmc
    xbmc.executebuiltin('xbmc.PlayMedia(Stop)')
    fulltitle = "[COLOR palegreen][B]"+item.extra+"[/B][/COLOR]"
    # Se incluye el título en la url para pasarlo al conector
    url= item.url + "|" + fulltitle
    
    itemlist.append(Item(channel=__channel__, title=item.title, server="p2p", url=url, action="play", folder=False))
    
    return itemlist

def translate(to_translate, to_langage="auto", langage="auto"):
    ###Traducción atraves de Google
    '''Return the translation using google translate
        you must shortcut the langage you define (French = fr, English = en, Spanish = es, etc...)
        if you don't define anything it will detect it or use english by default
        Example:
        print(translate("salut tu vas bien?", "en"))
        hello you alright?'''
    agents = {'User-Agent':"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)"}
    before_trans = 'class="t0">'
    link = "http://translate.google.com/m?hl=%s&sl=%s&q=%s" % (to_langage, langage, to_translate.replace(" ", "+"))
    request = urllib2.Request(link, headers=agents)
    page = urllib2.urlopen(request).read()
    result = page[page.find(before_trans)+len(before_trans):]
    result = result.split("<")[0]
    return result

if __name__ == '__main__':
    to_translate = 'Hola como estas?'
    print("%s >> %s" % (to_translate, translate(to_translate)))
    print("%s >> %s" % (to_translate, translate(to_translate, 'fr')))
#should print Hola como estas >> Hello how are you
#and Hola como estas? >> Bonjour comment allez-vous?





