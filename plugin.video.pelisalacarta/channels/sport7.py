# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para livetv
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os
import sys

import re, htmlentitydefs
from core import scrapertools
from core import logger
from core import config
import xbmcplugin
import xbmcaddon
import xbmc
import xbmcgui
from core.item import Item
from servers import servertools
from core.scrapertools import decodeHtmlentities as dhe
import random
import time

__channel__ = "sport7"
__category__ = "d"
__type__ = "generic"
__title__ = "Sport7"
__language__ = "ES"
song = os.path.join(config.get_runtime_path() , "music", 'pantera - this love.mp3')
host ="http://sport7.ru"
DEBUG = config.get_setting("debug")

def isGeneric():
    
    return True



def mainlist(item):
    logger.info("pelisalacarta.sport7 mainlist")
    itemlist = []
    import xbmc, time
    if not xbmc.Player().isPlaying():
       xbmc.executebuiltin('xbmc.PlayMedia('+song+')')
    

    
    """
        Lo que ocurre con
        url = http://translate.googleusercontent.com/translate_c?depth=1&nv=1&rurl=translate.google.com&sl=ru&tl=es&u=http://lfootball.ws/&usg=ALkJrhgzJfI1TDn3BxGgPbjgAHHS7J0i9g
        Redirecciones:
        1. http://translate.google.com/translate?depth=1&nv=1&rurl=translate.google.com&sl=ru&tl=es&u=http://lfootball.ws/
        2. http://translate.googleusercontent.com/translate_p?nv=1&rurl=translate.google.com&sl=ru&tl=es&u=http://lfootball.ws/&depth=2&usg=ALkJrhgAAAAAVupk4tLINTbmU7JrcQdl0G4V3LtnRM1n
        3. http://translate.googleusercontent.com/translate_c?depth=2&nv=1&rurl=translate.google.com&sl=ru&tl=es&u=http://lfootball.ws/&usg=ALkJrhhhRDwHSDRDN4t27cX5CYZLFFQtmA
        Lo que significa que necesitamos una key nueva cada vez en el argumento "usg" y para llegar a la url 3 debemos hacer la petición 1 y 2 con 'follow_redirects=False' o con la convinación de 'follow_redirects=False' y 'header_to_get="location"'
        """
    
    #### Opción 1: 'follow_redirects=False'
    ## Petición 1
    url = "http://translate.google.com/translate?depth=1&nv=1&rurl=translate.google.com&sl=ru&tl=es&u=http://sport7.ru"
    data = dhe( scrapertools.downloadpage(url,follow_redirects=False) )#.decode('cp1251').encode('utf8')
    ## Petición 2
    url = scrapertools.get_match(data, ' src="([^"]+)" name=c ')
    data = dhe( scrapertools.downloadpage(url,follow_redirects=False) )#.decode('cp1251').encode('utf8')
    ## Petición 3
    url = scrapertools.get_match(data, 'URL=([^"]+)"')
    data = dhe( scrapertools.cachePage(url) )#.decode('cp1251').encode('utf8')
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
    print "pocoyo"
    print data
    """
        #### Opción 2: 'follow_redirects=False' y 'header_to_get="location"'
        ## Petición 1
        url = "http://translate.google.com/translate?depth=1&nv=1&rurl=translate.google.com&sl=ru&tl=es&u=http://lfootball.ws/"
        data = dhe( scrapertools.downloadpage(url,follow_redirects=False) )#.decode('cp1251').encode('utf8')
        ## Petición 2
        url = scrapertools.get_match(data, ' src="([^"]+)" name=c ')
        url = scrapertools.get_header_from_response(url, header_to_get="location")
        ## Petición 3
        data = dhe( scrapertools.cachePage(url ) )#.decode('cp1251').encode('utf8')
        """
    
    
    
    patrondata = 'Mostrar todos los partidos(.*?)véase también'
    matchesdata = re.compile(patrondata,re.DOTALL).findall(data)
    for bloque_data in matchesdata:
        
        print "pacopepe"
        print bloque_data
        patronpartidos = 'text-align: left">[^<]+</span>([^<]+)(.*?)<div class="middle data">'
        matchespartidos = re.compile(patronpartidos,re.DOTALL).findall(bloque_data)
        
        for fecha, bloque_partidos in matchespartidos:
            print "tusmuertos"
            print bloque_partidos
            #itemlist.append( Item(channel=__channel__, title=fecha,action="mainlist",url="",thumbnail ="",fanart ="",folder=False) )
            patron = 'src=([^"]+)>.*?<span class=time>(\d+:\d+)</span>.*?http.*?http.*?(http://sport[^"]+)&usg.*?>(.*?)</a>'
            matches = re.compile(patron,re.DOTALL).findall(bloque_partidos)
            for thumbnail, hora, url, title in matches:
                fulltitle = "[COLOR darkorange][B]"+title+"[/B][/COLOR]"
                time= re.compile('(\d+):(\d+)',re.DOTALL).findall(hora)
                print "manolo"
                print hora
                for horas, minutos in time:
                    if  horas== "00":
                        horas = horas.replace("00","24")
                
                    check =re.compile('(\d)\d',re.DOTALL).findall(horas)
                    if "0"in check:
                        horas = horas.replace("0","")
                        horas = 24 + int(horas)
                    
                    wrong_time =int(horas)
                    value = 1
                    correct_time = wrong_time - value
                    if correct_time == 23:
                       dates = re.compile('(.*?)(\d+)(.*)',re.DOTALL).findall(fecha)
                       for d, days,m in dates:
                           dia = int(days) - 1
                           date = d+" "+str(dia) + m
                    
                    else :
                       date= fecha
                    if correct_time > 24:
                       correct_time = int(correct_time) - 24
                    
                    correct_time = '%02d' % int(correct_time)
                    ok_time = correct_time +":"+ minutos
                    print "guay"
                    print ok_time
                 
                if "24:" in ok_time:
                    ok_time =ok_time.replace("24:","00:")
                
                
                from time import gmtime, strftime
                import time
                get_date=strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        
                ok_date_hour =re.compile('(\d+)-(\d+)-(\d+) (\d+:\d+:\d+)',re.DOTALL).findall(get_date)
                for year,mes,day,hour in ok_date_hour:
                    current_day =day+"/"+mes+"/"+year
                    current_hour = hour
                    today =scrapertools.get_match(current_day,'(\d+)/\d+/\d+')
                    check_match_hour = scrapertools.get_match(ok_time,'(\d+):\d+')
                    check_match_minute = scrapertools.get_match(ok_time,'\d+:(\d+)')
                    check_today_hour = scrapertools.get_match(current_hour,'(\d+):\d+')
                    check_today_minute = scrapertools.get_match(current_hour,'\d+:(\d+)')
                    check_match_end_live = int (check_match_hour) + 2
                    check_match_end = int (check_today_hour) - 2
                    print "pepe"
                    print check_match_hour
                    print check_match_end
                    print check_match_end_live
                if day in date and int(check_match_hour) < int(check_today_hour) and int(check_today_hour)>= int(check_match_end_live) :
                   continue
                if day in date and int(check_match_hour) == int(check_today_hour) and int(check_match_minute) <= int(check_today_minute) or day in date and int(check_match_hour) < int(check_today_hour) and int(check_today_hour)< int(check_match_end_live) :
                    
                    title = "[COLOR darkorange][B]"+title+"[/B][/COLOR]"+ " " +"[COLOR crimson][B]DIRECTO!![/B][/COLOR]"
                    extra= "live"
                else :
                    
                   title = "[COLOR firebrick][B]"+ok_time+"[/B][/COLOR]" +"  "+"[COLOR deepskyblue]"+"("+date.strip()+")"+"[/COLOR]" + " " + "[COLOR olivedrab][B]"+title+"[/B][/COLOR]"
                   extra = "nolive"
                
                print "amoooo"
                print url
                itemlist.append( Item(channel=__channel__, title="     "+title,action="enlaces",url=url,thumbnail =thumbnail,fanart ="http://s6.postimg.org/uo85sphn5/sport7fanart.jpg",extra=extra,fulltitle = fulltitle,folder=True) )


        

    
    
    return itemlist

def enlaces(item):
    logger.info("pelisalacarta.sport7 enlaces")
    itemlist = []
    print "lopera"
    print item.fulltitle
    data = scrapertools.cachePage(item.url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
    print "caca"
    print data
    '''if "Скоро здесь будет" in data :
        title = "Aun no hay enlaces. Pruebe mas tarde".title()
        itemlist.append( Item(channel=__channel__, title="[COLOR lightseagreen][B]"+title+"[/B][/COLOR]",action="mainlist",url="",thumbnail="http://s6.postimg.org/3n87z3jbl/livesportnolinkyetthumb.png",fanart ="http://s6.postimg.org/l1sg7dggh/livesportnolinskyet.jpg",folder=False) )'''

    patron= '<img class="img-bt" alt="(.*?) \d+".*?src="([^"]+).*?target="_blank" href="([^"]+).*?<div class="rc">(.*?)</div>'
    matches =re.compile(patron,re.DOTALL).findall(data)
    if len(matches) == 0:
        if item.extra == "live":
           itemlist.append( Item(channel=__channel__, title="[COLOR firebrick][B]No hay enlaces Acestream/Sopcast[/B][/COLOR]",action="mainlist",url="",thumbnail="http://s33.postimg.org/c4guv3q1r/sport7nolinksthumb.png",fanart="http://s33.postimg.org/sc0gx0k9r/sport7nolinksfan.jpg",folder=False) )
        else :
              title = "Aun no hay enlaces. Pruebe mas tarde".title()
              itemlist.append( Item(channel=__channel__, title="[COLOR mediumspringgreen][B]"+title+"[/B][/COLOR]",action="mainlist",url="",thumbnail="http://s33.postimg.org/5jfmbp1nj/sport7nolinkyetthumb.png",fanart ="http://s6.postimg.org/6srzxmt1t/sport7fanartnoenlacesyet.jpg",folder=False) )
    for tipo, thumbnail, link, bibrate in matches:
        print "joder"
        print bibrate
        if tipo == "Sopcast":
           tipo = "[COLOR aquamarine][B]"+tipo+"[/B][/COLOR]"
           thumbnail= "http://s6.postimg.org/v9z5ggmfl/sopcast.jpg"
        else:
            tipo = "[COLOR yellow][B]"+tipo+"[/B][/COLOR]"
            thumbnail= "http://s6.postimg.org/c2c0jv441/torrent_stream_logo_300x262.png"
        if bibrate == "0 kbps" or "-" in bibrate:
           bibrate = "[COLOR forestgreen]No Bitrate[/COLOR]"
        title = tipo + "  "+ "[COLOR chartreuse]"+bibrate+"[/COLOR]"
        if "down.png" in thumbnail:
           continue
        itemlist.append( Item(channel=__channel__, title=title,action="play",url=link,thumbnail=thumbnail,fanart="http://s6.postimg.org/3s6k3cscx/sport7fangame.jpg",fulltitle = item.fulltitle,folder=False) )



    return itemlist

def play(item):
    logger.info("pelisalacarta.sport7 play")
    itemlist = []
    data = scrapertools.cachePage(item.url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
    item.url =scrapertools.get_match(data,'<a href="([^"]+)"')
    import xbmc
    xbmc.executebuiltin('xbmc.PlayMedia(Stop)')
    fulltitle = item.fulltitle
    
    # Se incluye el título en la url para pasarlo al conector
    url= item.url + "|" + fulltitle
    
    itemlist.append(Item(channel=__channel__, title=item.title, server="p2p", url=url, action="play", folder=False))
    
    return itemlist










