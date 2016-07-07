# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Context Menu - PLD.VisionTV
# Version 0.1 (18.08.2015)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Gracias a la librería plugintools de Jesús (www.mimediacenter.info)


import os
import sys
import urllib
import urllib2
import re

import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin

import plugintools, requests
from resources.tools.resolvers import *
from resources.tools.txt_reader import *

from __main__ import *


playlists = xbmc.translatePath(os.path.join('special://userdata/playlists', ''))
temp = xbmc.translatePath(os.path.join('special://userdata/playlists/tmp', ''))

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")



def trailer0(params):  # Thanks to Abelhas addon!
    plugintools.log("[%s %s] PLD.VisionTV ContextMenu (Trailer) %s" % (addonName, addonId, repr(params)))

    show = plugintools.get_setting("pelis_view")
    plugintools.modo_vista(show)       

    youtube_trailer_search = 'https://www.googleapis.com/youtube/v3/search?part=id,snippet&q=%s-Trailer&maxResults=1&key=AIzaSyCgpWUrGw2mySqmxxzlrsUoNhpGCBVJD7s'
    title = parser_title(params.get("title"));title_fixed = title.split("[")
    i = len(title_fixed)
    if i >= 2: title_fixed = title_fixed[0].strip()
    ytpage = abrir_url(youtube_trailer_search % (urllib.quote_plus(title_fixed)))
    youtubeid = re.compile('"videoId": "(.+?)"').findall(ytpage)
    url = 'plugin://plugin.video.youtube/play/?video_id=%s' % youtubeid[0]
    if url == None: return
    item = xbmcgui.ListItem(path=url)
    item.setProperty("IsPlayable", "true")
    xbmc.Player().play(url, item)    

     
    
def abrir_url(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', user_agent)
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link


def filmaff0(params):
    plugintools.log("[%s %s] PLD.VisionTV ContextMenu (Filmaff) %s" % (addonName, addonId, repr(params)))
    show = plugintools.get_setting("pelis_view")
    plugintools.modo_vista(show)    

    title = parser_title(params.get("title"));title_fixed = title.split("[")
    i = len(title_fixed)
    if i >= 2: title_fixed = title_fixed[0].strip()

    title_upper = title_fixed.upper()
    fpeli = temp + 'infopeli-'+title_fixed+'.m3u'
    filepeli = open(fpeli, "a")

    plugintools.log("Buscando película... "+title_fixed)
    url = 'http://www.filmaffinity.com/es/search.php?stext='+title_fixed+'&stype=all'
    referer='http://www.filmaffinity.com/'
    data = gethttp_referer_headers(url,referer)
    #plugintools.log("data buscador= "+data)
    
    bloque = plugintools.find_single_match(data, '<div class="mc-poster">(.*?)</div>')
    url_film = plugintools.find_single_match(bloque, 'href="/es/film(.*?).html')

    # Ficha técnica de la película
    url = 'http://www.filmaffinity.com/es/film'+url_film+'.html';print url
    body = gethttp_referer_headers(url, referer)

    # Puntuación y número de votos
    rating_aff = plugintools.find_single_match(body, '<div id="movie-rat-avg" itemprop="ratingValue">([^<]+)').strip()
    votes_aff = plugintools.find_single_match(body, '<span itemprop="ratingCount">([^<]+)')

    # Información técnica
    info = plugintools.find_single_match(body, '<dl class="movie-info">(.*?)</dl>')
    title_original = plugintools.find_single_match(info, '<dd>([^<]+)')
    title_original = plugintools.find_single_match(info, '<dd itemprop="datePublished">([^<]+)')
    year_film = plugintools.find_single_match(info, '<dd itemprop="datePublished">(.*?)</dd>')
    length = plugintools.find_single_match(info, '<dt>Duración</dt>(.*?)min.</dd>');length=length.replace("<dd>", "").strip()
    pais0 = plugintools.find_single_match(info, '<dd><span id="country-img">(.*?)</dd>')
    pais = plugintools.find_single_match(info, 'title="([^"]+)')
    directors = plugintools.find_single_match(info, '<dd class="directors"(.*?)</dd>')
    direc = plugintools.find_multiple_matches(directors, '<span itemprop="name">(.*?)</span>'); dir_final= ""    
    for entry in direc:
        if dir_final != "":
            dir_final = dir_final + ', '+entry
        else:
            dir_final = entry
    guion = plugintools.find_single_match(info, '<dt>Guión</dt>(.*?)</dd>');guion=guion.replace("<dd>", "").strip()
    music = plugintools.find_single_match(info, '<dt>Música</dt>(.*?)min.</dd>');music=music.replace("<dd>", "").strip()
    foto = plugintools.find_single_match(info, '<dt>Fotografía</dt>(.*?)min.</dd>');foto=foto.replace("<dd>", "").strip()
    cast = plugintools.find_single_match(info, '<dt>Reparto</dt>(.*?)</a></dd>')
    cast_item = plugintools.find_multiple_matches(cast, '">([^<]+)');cast_final = ""
    for entry in cast_item:
        if cast_final != "":
            cast_final = cast_final + ', '+entry
        else:
            cast_final = entry
    prod = plugintools.find_single_match(info, '<dt>Productora</dt>(.*?)</dd>');prod=prod.replace("<dd>", "").strip()
    genres = plugintools.find_single_match(info, '<dt>Género</dt>(.*?)</dd>')
    genre_items = plugintools.find_multiple_matches(genres, '">(.*?)</a>'); genre_final= ""    
    for entry in genre_items:
        if genre_final != "":
            genre_final = genre_final + ', '+entry
        else:
            genre_final = entry
    web0 = plugintools.find_single_match(info, '<dt>Web oficial</dt>(.*?)</dd>')
    web = plugintools.find_single_match(web0, 'href="([^"]+)')
    sinopsis = plugintools.find_single_match(info, '<dt>Sinopsis</dt>(.*?)</dd>');sinopsis=sinopsis.replace("<dd>", "").replace("&quot;", '"').replace("<br>", "[CR]").strip()

    # Guardamos info en archivo...
    filepeli.write('[COLOR lightyellow][B]'+title_upper+'[/B][/COLOR] ('+year_film+')\n\n')
    filepeli.write("[B]AÑO: [COLOR lightblue]"+year_film+' [/COLOR][B]PAÍS:[/B] [COLOR lightblue]'+pais+' [/COLOR][B]NOTA[/B]: [COLOR lightblue]('+rating_aff+'/'+votes_aff+') [/COLOR][B]DURACIÓN:[/B] [COLOR lightblue]'+length+' [/COLOR][B]DIRECCIÓN:[/B] [COLOR lightblue]'+dir_final+' [/COLOR][B]GUIÓN:[/B] [COLOR lightblue]'+guion+' [/COLOR][B]MÚSICA:[/B] [COLOR lightblue]'+music+' [/COLOR][B]FOTOGRAFÍA:[/B] [COLOR lightblue]'+foto+' [/COLOR][B]REPARTO:[/B] [COLOR lightblue]'+cast_final+' [/COLOR][B]PRODUCTORA:[/B] [COLOR lightblue]'+prod+' [/COLOR][B]GÉNERO:[/B] [COLOR lightblue]'+genre_final+' [/COLOR][B]WEB OFICIAL:[/B] [COLOR lightblue]'+web+'[/COLOR]\n\n[B]SINOPSIS:[/B] [I]'+sinopsis+'[/I]\n\n')   
    
    url_film = 'http://www.filmaffinity.com/es/reviews/1/'+url_film+'.html'
    body = gethttp_referer_headers(url_film, referer)
    
    # Bloque de críticas en Filmaffinity
    filepeli.write('[B]Críticas más destacadas[/B] [I](Sin spoilers)[/I]\n\n')
    bloque_critic = plugintools.find_multiple_matches(body, '<div class="fa-shadow movie-review-wrapper rw-item"(.*?)<div class="share-review-wrapper">')    
    for entry in bloque_critic:
        user_aff = plugintools.find_single_match(entry, '<div class="review-user-nick">([^<]+)')
        date_aff = plugintools.find_single_match(entry, '<div><div class="review-date">(.*?)</div>')
        text = plugintools.find_single_match(entry, '<div class="review-text1">(.*?)</div>')
        text = text.replace("<br />", "").replace("&quot;", '"').strip()
        filepeli.write('Crítica de [COLOR lightblue][I]'+user_aff+' [/COLOR][/I]del [COLOR lightgreen]'+date_aff+'[/COLOR]: \n'+text+'\n\n')

    filepeli.close()

    params=plugintools.get_params()
    params["url"]=fpeli
    wikipeli0(params)


def wikipeli0(params):
    plugintools.log('[%s %s] TXT_reader %s' % (addonName, addonVersion, repr(params)))
    show = plugintools.get_setting("pelis_view")
    plugintools.modo_vista(show)
    url=params.get("url")
    url = url.replace("txt:", "")

    if url.startswith("http") == True:  # Control para textos online
        plugintools.log("Iniciando descarga desde..."+url)
        h=urllib2.HTTPHandler(debuglevel=0)  # Iniciamos descarga...
        request = urllib2.Request(url)
        opener = urllib2.build_opener(h)
        urllib2.install_opener(opener)
        filename = url.split("/")
        max_len = len(filename)
        max_len = int(max_len) - 1
        filename = filename[max_len]
        fh = open(playlists + filename, "wb")  #open the file for writing
        connected = opener.open(request)
        meta = connected.info()
        filesize = meta.getheaders("Content-Length")[0]
        size_local = fh.tell()
        print 'filesize',filesize
        print 'size_local',size_local
        while int(size_local) < int(filesize):
            blocksize = 100*1024
            bloqueleido = connected.read(blocksize)
            fh.write(bloqueleido)  # read from request while writing to file
            size_local = fh.tell()
            print 'size_local',size_local
        filename = url.split("/")
        inde = len(filename);print inde
        filename = filename[inde-1]
        txt_file = filename
        txt_path = playlists + txt_file
        plugintools.log("Abriendo texto de "+txt_path)
        xbmc.sleep(100)
        TextBoxes("[B][COLOR lightyellow][I]playlists / [/B][/COLOR][/I] "+txt_file,txt_path)       
        
    else:
        txt_path = url
        plugintools.log("Abriendo texto de "+txt_path)
        xbmc.sleep(100)
        TextBoxes("[B][COLOR lightyellow][I]Wikipeli en [/COLOR][COLOR gold]Filmaffinity [/COLOR][/B][/I] ",txt_path)

    show = plugintools.get_setting("pelis_view")
    plugintools.modo_vista(show)
        
    
    


def gethttp_referer_headers(url,referer):
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    request_headers.append(["Referer", referer])
    body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)
    
    return body

