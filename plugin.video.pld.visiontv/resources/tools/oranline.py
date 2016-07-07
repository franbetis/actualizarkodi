# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Regex de Oranline - PLD.VisionTV
# Version 0.1
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

import re,urllib,urllib2,sys,requests
import plugintools

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")

thumbnail = 'http://www.oranline.com/wp-content/uploads/2015/01/logoneworange-300x92.png'
fanart = 'http://wallpoper.com/images/00/33/95/82/film-roll_00339582.jpg'
referer = 'http://www.oranline.com/'


def oranline0(params):
    plugintools.log('[%s %s] Oranline regex %s' % (addonName, addonVersion, repr(params)))

    show = 'tvshows'
    # Leemos el código web
    url = params.get("url")
    headers = {'user-agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14'}
    r = requests.get(url, headers=headers)
    data = r.content

    bloque_thumb = plugintools.find_single_match(data, '<!--Begin Image-->(.*?)<!--End Image-->')
    thumb_peli = plugintools.find_single_match(bloque_thumb, '<img src="([^"]+)')
    if thumb_peli == "":
        thumb_peli = thumbnail
                    
    datamovie = {}
    datamovie["Plot"]=params.get("plot")  # Sinopsis

    bloque = plugintools.find_single_match(data, '<div id="veronline">(.*?)</form>')
    bloque_peli = plugintools.find_multiple_matches(bloque, '<p>(.*?)</img></a></span></p>')

    i = 1
    plugintools.add_item(action="", title='[COLOR orange][B]Oranline.com / [/B][/COLOR][COLOR white] Resultados de: [/COLOR][COLOR lightyellow][I]'+params.get("title")+'[/I][/COLOR]', thumbnail=thumb_peli, fanart=fanart, folder=False, isPlayable=False)
    plugintools.add_item(action="", title='[COLOR white][I](Núm.) [/I][/COLOR][COLOR white][I]Formato[/I][/COLOR][COLOR lightblue] Calidad (sobre 5)[/COLOR][COLOR lightgreen][I][Idioma][/I][/COLOR]', thumbnail=thumb_peli, fanart=fanart, folder=False, isPlayable=False)
    
    for entry in bloque_peli:
        #plugintools.log("entry= "+entry)
        lang_audio = plugintools.find_single_match(entry, 'src="([^"]+)')
        if lang_audio.endswith("1.png") == True:
            lang_audio = '[COLOR lightgreen][I][ESP][/I][/COLOR]'
        elif lang_audio.endswith("2.png") == True:
            lang_audio = '[COLOR lightgreen][I][LAT][/I][/COLOR]'
        elif lang_audio.endswith("3.png") == True:
            lang_audio = '[COLOR lightgreen][I][VOS][/I][/COLOR]'
        elif lang_audio.endswith("4.png") == True:
            lang_audio = '[COLOR lightgreen][I][ENG][/I][/COLOR]'
        formatq = plugintools.find_single_match(entry, 'calidad(.+?).png')
        #plugintools.log("formatq= "+formatq)
        
        id_link = plugintools.find_single_match(entry, 'reportarpelicula([^>]+)')
        id_link = id_link.replace('"', "").replace("'", "").replace(",", "").replace(")", "")
        url = oranline2(id_link, params.get("url"))
        #plugintools.log("url= "+url)
        
        title_peli = plugintools.find_single_match(entry, 'title="([^"]+)')        
        title_peli = title_peli.replace("Calidad de Video:", "").replace("Calidad de video", "").replace("Calidad de Audio", "").replace("\t\r\n", "").replace("reportar enlace", "N/D").strip()
        info_video = title_peli.split(":")[0].strip()
        title_peli = '[COLOR white][I]'+info_video+' [/I][/COLOR][COLOR lightblue]'+formatq+'/5[/COLOR]'
        if url.find("allmyvideos") >= 0:
            server_url = "[COLOR lightyellow][I][allmyvideos][/I][/COLOR]"
            plugintools.add_item(action="allmyvideos", title= '[COLOR white]'+str(i)+'. '+title_peli+'[/COLOR] '+lang_audio+' '+server_url , url = url, info_labels = datamovie , extra = show , page = show , fanart = fanart , thumbnail = thumb_peli , folder = False, isPlayable = True)
        elif url.find("vidspot") >= 0:
            server_url = "[COLOR lightyellow][I][vidspot][/I][/COLOR]"
            plugintools.add_item(action="vidspot", title= '[COLOR white]'+str(i)+'. '+title_peli+'[/COLOR] '+lang_audio+' '+server_url , url = url, info_labels = datamovie , extra = show , page = show , fanart = fanart , thumbnail = thumb_peli , folder = False, isPlayable = True)
        elif url.find("played.to") >= 0:
            server_url = "[COLOR lightyellow][I][played.to][/I][/COLOR]"
            plugintools.add_item(action="playedto", title= '[COLOR white]'+str(i)+'. '+title_peli+'[/COLOR] '+lang_audio+' '+server_url , url = url, info_labels = datamovie , extra = show , page = show , fanart = fanart , thumbnail = thumb_peli , folder = False, isPlayable = True)
        elif url.find("nowvideo") >= 0:
            server_url = "[COLOR lightyellow][I][nowvideo][/I][/COLOR]"
            plugintools.add_item(action="nowvideo", title= '[COLOR white]'+str(i)+'. '+title_peli+'[/COLOR] '+lang_audio+' '+server_url , url = url, info_labels = datamovie , extra = show , page = show , fanart = fanart , thumbnail = thumb_peli , folder = False, isPlayable = True)
        elif url.find("streamin.to") >= 0:
            server_url = "[COLOR lightyellow][I][streamin.to][/I][/COLOR]"
            plugintools.add_item(action="streaminto", title= '[COLOR white]'+str(i)+'. '+title_peli+'[/COLOR] '+lang_audio+' '+server_url , url = url, info_labels = datamovie , extra = show , page = show , fanart = fanart , thumbnail = thumb_peli , folder = False, isPlayable = True)
        elif url.find("vk") >= 0:
            server_url = "[COLOR lightyellow][I][vk][/I][/COLOR]"
            plugintools.add_item(action="vk", title= '[COLOR white]'+str(i)+'. '+title_peli+'[/COLOR] '+lang_audio+' '+server_url , url = url, info_labels = datamovie , extra = show , page = show , fanart = fanart , thumbnail = thumb_peli , folder = False, isPlayable = True)
        elif url.find("tumi") >= 0:
            server_url = "[COLOR lightyellow][I][tumi][/I][/COLOR]"
            plugintools.add_item(action="tumi", title= '[COLOR white]'+str(i)+'. '+title_peli+'[/COLOR] '+lang_audio+' '+server_url , url = url, info_labels = datamovie , extra = show , page = show , fanart = fanart , thumbnail = thumb_peli , folder = False, isPlayable = True)
        elif url.find("powvideo") >= 0:
            server_url = "[COLOR lightyellow][I][powvideo][/I][/COLOR]"
            plugintools.add_item(action="powvideo", title= '[COLOR white]'+str(i)+'. '+title_peli+'[/COLOR] '+lang_audio+' '+server_url , url = url, info_labels = datamovie , extra = show , page = show , fanart = fanart , thumbnail = thumb_peli , folder = False, isPlayable = True)            
        elif url.find("streamcloud") >= 0:
            server_url = "[COLOR lightyellow][I][streamcloud][/I][/COLOR]"
            plugintools.add_item(action="streamcloud", title= '[COLOR white]'+str(i)+'. '+title_peli+'[/COLOR] '+lang_audio+' '+server_url , url = url, info_labels = datamovie , extra = show , page = show , fanart = fanart , thumbnail = thumb_peli , folder = False, isPlayable = True)
        elif url.find("veehd") >= 0:
            server_url = "[COLOR lightyellow][I][veehd][/I][/COLOR]"
            plugintools.add_item(action="veehd", title= '[COLOR white]'+str(i)+'. '+title_peli+'[/COLOR] '+lang_audio+' '+server_url , url = url, info_labels = datamovie , extra = show , page = show , fanart = fanart , thumbnail = thumb_peli , folder = False, isPlayable = True)
        elif url.find("novamov") >= 0:
            server_url = "[COLOR lightyellow][I][novamov][/I][/COLOR]"
            plugintools.add_item(action="novamov", title= '[COLOR white]'+str(i)+'. '+title_peli+'[/COLOR] '+lang_audio+' '+server_url , url = url, info_labels = datamovie , extra = show , page = show , fanart = fanart , thumbnail = thumb_peli , folder = False, isPlayable = True)
        elif url.find("moevideos") >= 0:
            server_url = "[COLOR lightyellow][I][moevideos][/I][/COLOR]"
            plugintools.add_item(action="moevideos", title= '[COLOR white]'+str(i)+'. '+title_peli+'[/COLOR] '+lang_audio+' '+server_url , url = url, info_labels = datamovie , extra = show , page = show , fanart = fanart , thumbnail = thumb_peli , folder = False, isPlayable = True)
        elif url.find("movshare") >= 0:
            server_url = "[COLOR lightyellow][I][movshare][/I][/COLOR]"
            plugintools.add_item(action="movshare", title= '[COLOR white]'+str(i)+'. '+title_peli+'[/COLOR] '+lang_audio+' '+server_url , url = url, info_labels = datamovie , extra = show , page = show , fanart = fanart , thumbnail = thumb_peli , folder = False, isPlayable = True)
        elif url.find("movreel") >= 0:
            server_url = "[COLOR lightyellow][I][movreel][/I][/COLOR]"
            plugintools.add_item(action="movshare", title= '[COLOR white]'+str(i)+'. '+title_peli+'[/COLOR] '+lang_audio+' '+server_url , url = url, info_labels = datamovie , extra = show , page = show , fanart = fanart , thumbnail = thumb_peli , folder = False, isPlayable = True)
        elif url.find("gamovideo") >= 0:
            server_url = "[COLOR lightyellow][I][gamovideo][/I][/COLOR]"
            plugintools.add_item(action="gamovideo", title= '[COLOR white]'+str(i)+'. '+title_peli+'[/COLOR] '+lang_audio+' '+server_url , url = url, info_labels = datamovie , extra = show , page = show , fanart = fanart , thumbnail = thumb_peli , folder = False, isPlayable = True)
        elif url.find("videobam") >= 0:
            server_url = "[COLOR lightyellow][I][videobam][/I][/COLOR]"
            plugintools.add_item(action="videobam", title= '[COLOR white]'+str(i)+'. '+title_peli+'[/COLOR] '+lang_audio+' '+server_url , url = url, info_labels = datamovie , extra = show , page = show , fanart = fanart , thumbnail = thumb_peli , folder = False, isPlayable = True)
        elif url.find("videoweed") >= 0:
            server_url = "[COLOR lightyellow][I][videoweed][/I][/COLOR]"
            plugintools.add_item(action="videoweed", title= '[COLOR white]'+str(i)+'. '+title_peli+'[/COLOR] '+lang_audio+' '+server_url , url = url, info_labels = datamovie , extra = show , page = show , fanart = fanart , thumbnail = thumb_peli , folder = False, isPlayable = True)
        elif url.find("streamable") >= 0:
            server_url = "[COLOR lightyellow][I][streamable][/I][/COLOR]"
            plugintools.add_item(action="streamable", title= '[COLOR white]'+str(i)+'. '+title_peli+'[/COLOR] '+lang_audio+' '+server_url , url = url, info_labels = datamovie , extra = show , page = show , fanart = fanart , thumbnail = thumb_peli , folder = False, isPlayable = True)            
        elif url.find("rocvideo") >= 0:
            server_url = "[COLOR lightyellow][I][rocvideo][/I][/COLOR]"
            plugintools.add_item(action="rocvideo", title= '[COLOR white]'+str(i)+'. '+title_peli+'[/COLOR] '+lang_audio+' '+server_url , url = url, info_labels = datamovie , extra = show , page = show , fanart = fanart , thumbnail = thumb_peli , folder = False, isPlayable = True)
        elif url.find("realvid") >= 0:
            server_url = "[COLOR lightyellow][I][realvid][/I][/COLOR]"
            plugintools.add_item(action="realvid", title= '[COLOR white]'+str(i)+'. '+title_peli+'[/COLOR] '+lang_audio+' '+server_url , url = url, info_labels = datamovie , extra = show , page = show , fanart = fanart , thumbnail = thumb_peli , folder = False, isPlayable = True)
        elif url.find("netu") >= 0:
            server_url = "[COLOR lightyellow][I][netu][/I][/COLOR]"
            plugintools.add_item(action="netu", title= '[COLOR white]'+str(i)+'. '+title_peli+'[/COLOR] '+lang_audio+' '+server_url , url = url, info_labels = datamovie , extra = show , page = show , fanart = fanart , thumbnail = thumb_peli , folder = False, isPlayable = True)
        elif url.find("videomega") >= 0:
            server_url = "[COLOR lightyellow][I][videomega][/I][/COLOR]"
            plugintools.add_item(action="videomega", title= '[COLOR white]'+str(i)+'. '+title_peli+'[/COLOR] '+lang_audio+' '+server_url , url = url, info_labels = datamovie , extra = show , page = show , fanart = fanart , thumbnail = thumb_peli , folder = False, isPlayable = True)
        elif url.find("video.tt") >= 0:
            server_url = "[COLOR lightyellow][I][video.tt][/I][/COLOR]"
            plugintools.add_item(action="videott", title= '[COLOR white]'+str(i)+'. '+title_peli+'[/COLOR] '+lang_audio+' '+server_url , url = url, info_labels = datamovie , extra = show , page = show , fanart = fanart , thumbnail = thumb_peli , folder = False, isPlayable = True)                        
        elif url.find("flashx.tv") >= 0:
            server_url = "[COLOR lightyellow][I][flashx][/I][/COLOR]"
            plugintools.add_item(action="flashx", title= '[COLOR white]'+str(i)+'. '+title_peli+'[/COLOR] '+lang_audio+' '+server_url , url = url, info_labels = datamovie , extra = show , page = show , fanart = fanart , thumbnail = thumb_peli , folder = False, isPlayable = True)                        
            
        i = i + 1


def oranline1(params):
    plugintools.log('[%s %s] Oranline URL analyzer %s' % (addonName, addonVersion, repr(params)))    
    
    if url.find("allmyvideos") >= 0:
        server_url = "[COLOR lightgreen][I][allmyvideos][/I][/COLOR]"
        plugintools.add_item(action="allmyvideos", title= '[COLOR white]'+title_fixed+' [/COLOR][COLOR lightyellow][I]('+server_name+')[/I][/COLOR]  [COLOR lightgreen][I]'+lang+'[/I][/COLOR]' , url = url, info_labels = datamovie , extra = show , page = show , fanart = fanart , thumbnail = thumbnail , folder = False, isPlayable = True)
    elif url.find("vidspot") >= 0:
        server_url = "[COLOR lightgreen][I][vidspot][/I][/COLOR]"
        plugintools.add_item(action="vidspot", title= '[COLOR white]'+title_fixed+' [/COLOR][COLOR lightyellow][I]('+server_name+')[/I][/COLOR]  [COLOR lightgreen][I]'+lang+'[/I][/COLOR]' , url = url, info_labels = datamovie , extra = show , page = show , fanart = fanart , thumbnail = thumbnail , folder = False, isPlayable = True)
    elif url.find("played.to") >= 0:
        server_url = "[COLOR lightgreen][I][played.to][/I][/COLOR]"
        plugintools.add_item(action="playedto", title= '[COLOR white]'+title_fixed+' [/COLOR][COLOR lightyellow][I]('+server_name+')[/I][/COLOR]  [COLOR lightgreen][I]'+lang+'[/I][/COLOR]' , url = url, info_labels = datamovie , extra = show , page = show , fanart = fanart , thumbnail = thumbnail , folder = False, isPlayable = True)
    elif url.find("nowvideo") >= 0:
        server_url = "[COLOR lightgreen][I][nowvideo][/I][/COLOR]"
        plugintools.add_item(action="nowvideo", title= '[COLOR white]'+title_fixed+' [/COLOR][COLOR lightyellow][I]('+server_name+')[/I][/COLOR]  [COLOR lightgreen][I]'+lang+'[/I][/COLOR]' , url = url, info_labels = datamovie , extra = show , page = show , fanart = fanart , thumbnail = thumbnail , folder = False, isPlayable = True)
    elif url.find("streamin.to") >= 0:
        server_url = "[COLOR lightgreen][I][streamin.to][/I][/COLOR]"
        plugintools.add_item(action="streaminto", title= '[COLOR white]'+title_fixed+' [/COLOR][COLOR lightyellow][I]('+server_name+')[/I][/COLOR]  [COLOR lightgreen][I]'+lang+'[/I][/COLOR]' , url = url, info_labels = datamovie , extra = show , page = show , fanart = fanart , thumbnail = thumbnail , folder = False, isPlayable = True)
    elif url.find("vk") >= 0:
        server_url = "[COLOR lightgreen][I][vk][/I][/COLOR]"
        plugintools.add_item(action="vk", title= '[COLOR white]'+title_fixed+' [/COLOR][COLOR lightyellow][I]('+server_name+')[/I][/COLOR]  [COLOR lightgreen][I]'+lang+'[/I][/COLOR]' , url = url, info_labels = datamovie , extra = show , page = show , fanart = fanart , thumbnail = thumbnail , folder = False, isPlayable = True)
    elif url.find("tumi") >= 0:
        server_url = "[COLOR lightgreen][I][tumi][/I][/COLOR]"
        plugintools.add_item(action="tumi", title= '[COLOR white]'+title_fixed+' [/COLOR][COLOR lightyellow][I]('+server_name+')[/I][/COLOR]  [COLOR lightgreen][I]'+lang+'[/I][/COLOR]' , url = url, info_labels = datamovie , extra = show , page = show , fanart = fanart , thumbnail = thumbnail , folder = False, isPlayable = True)
    elif url.find("streamcloud") >= 0:
        server_url = "[COLOR lightgreen][I][streamcloud][/I][/COLOR]"
        plugintools.add_item(action="streamcloud", title= '[COLOR white]'+title_fixed+' [/COLOR][COLOR lightyellow][I]('+server_name+')[/I][/COLOR]  [COLOR lightgreen][I]'+lang+'[/I][/COLOR]' , url = url, info_labels = datamovie , extra = show , page = show , fanart = fanart , thumbnail = thumbnail , folder = False, isPlayable = True)
    elif url.find("veehd") >= 0:
        server_url = "[COLOR lightgreen][I][veehd][/I][/COLOR]"
        plugintools.add_item(action="veehd", title= '[COLOR white]'+title_fixed+' [/COLOR][COLOR lightyellow][I]('+server_name+')[/I][/COLOR]  [COLOR lightgreen][I]'+lang+'[/I][/COLOR]' , url = url, info_labels = datamovie , extra = show , page = show , fanart = fanart , thumbnail = thumbnail , folder = False, isPlayable = True)
    elif url.find("novamov") >= 0:
        server_url = "[COLOR lightgreen][I][novamov][/I][/COLOR]"
        plugintools.add_item(action="novamov", title= '[COLOR white]'+title_fixed+' [/COLOR][COLOR lightyellow][I]('+server_name+')[/I][/COLOR]  [COLOR lightgreen][I]'+lang+'[/I][/COLOR]' , url = url, info_labels = datamovie , extra = show , page = show , fanart = fanart , thumbnail = thumbnail , folder = False, isPlayable = True)
    elif url.find("moevideos") >= 0:
        server_url = "[COLOR lightgreen][I][moevideos][/I][/COLOR]"
        plugintools.add_item(action="moevideos", title= '[COLOR white]'+title_fixed+' [/COLOR][COLOR lightyellow][I]('+server_name+')[/I][/COLOR]  [COLOR lightgreen][I]'+lang+'[/I][/COLOR]' , url = url, info_labels = datamovie , extra = show , page = show , fanart = fanart , thumbnail = thumbnail , folder = False, isPlayable = True)
    elif url.find("movshare") >= 0:
        server_url = "[COLOR lightgreen][I][movshare][/I][/COLOR]"
        plugintools.add_item(action="movshare", title= '[COLOR white]'+title_fixed+' [/COLOR][COLOR lightyellow][I]('+server_name+')[/I][/COLOR]  [COLOR lightgreen][I]'+lang+'[/I][/COLOR]' , url = url, info_labels = datamovie , extra = show , page = show , fanart = fanart , thumbnail = thumbnail , folder = False, isPlayable = True)
    elif url.find("movreel") >= 0:
        server_url = "[COLOR lightgreen][I][movreel][/I][/COLOR]"
        plugintools.add_item(action="movshare", title= '[COLOR white]'+title_fixed+' [/COLOR][COLOR lightyellow][I]('+server_name+')[/I][/COLOR]  [COLOR lightgreen][I]'+lang+'[/I][/COLOR]' , url = url, info_labels = datamovie , extra = show , page = show , fanart = fanart , thumbnail = thumbnail , folder = False, isPlayable = True)
    elif url.find("gamovideo") >= 0:
        server_url = "[COLOR lightgreen][I][gamovideo][/I][/COLOR]"
        plugintools.add_item(action="gamovideo", title= '[COLOR white]'+title_fixed+' [/COLOR][COLOR lightyellow][I]('+server_name+')[/I][/COLOR]  [COLOR lightgreen][I]'+lang+'[/I][/COLOR]' , url = url, info_labels = datamovie , extra = show , page = show , fanart = fanart , thumbnail = thumbnail , folder = False, isPlayable = True)
    elif url.find("videobam") >= 0:
        server_url = "[COLOR lightgreen][I][videobam][/I][/COLOR]"
        plugintools.add_item(action="videobam", title= '[COLOR white]'+title_fixed+' [/COLOR][COLOR lightyellow][I]('+server_name+')[/I][/COLOR]  [COLOR lightgreen][I]'+lang+'[/I][/COLOR]' , url = url, info_labels = datamovie , extra = show , page = show , fanart = fanart , thumbnail = thumbnail , folder = False, isPlayable = True)
    elif url.find("videoweed") >= 0:
        server_url = "[COLOR lightgreen][I][videoweed][/I][/COLOR]"
        plugintools.add_item(action="videoweed", title= '[COLOR white]'+title_fixed+' [/COLOR][COLOR lightyellow][I]('+server_name+')[/I][/COLOR]  [COLOR lightgreen][I]'+lang+'[/I][/COLOR]' , url = url, info_labels = datamovie , extra = show , page = show , fanart = fanart , thumbnail = thumbnail , folder = False, isPlayable = True)
    elif url.find("streamable") >= 0:
        server_url = "[COLOR lightgreen][I][streamable][/I][/COLOR]"
        plugintools.add_item(action="streamable", title= '[COLOR white]'+title_fixed+' [/COLOR][COLOR lightyellow][I]('+server_name+')[/I][/COLOR]  [COLOR lightgreen][I]'+lang+'[/I][/COLOR]' , url = url, info_labels = datamovie , extra = show , page = show , fanart = fanart , thumbnail = thumbnail , folder = False, isPlayable = True)
    elif url.find("rocvideo") >= 0:
        server_url = "[COLOR lightgreen][I][rocvideo][/I][/COLOR]"
        plugintools.add_item(action="rocvideo", title= '[COLOR white]'+title_fixed+' [/COLOR][COLOR lightyellow][I]('+server_name+')[/I][/COLOR]  [COLOR lightgreen][I]'+lang+'[/I][/COLOR]' , url = url, info_labels = datamovie , extra = show , page = show , fanart = fanart , thumbnail = thumbnail , folder = False, isPlayable = True)
    elif url.find("realvid") >= 0:
        server_url = "[COLOR lightgreen][I][realvid][/I][/COLOR]"
        plugintools.add_item(action="realvid", title= '[COLOR white]'+title_fixed+' [/COLOR][COLOR lightyellow][I]('+server_name+')[/I][/COLOR]  [COLOR lightgreen][I]'+lang+'[/I][/COLOR]' , url = url, info_labels = datamovie , extra = show , page = show , fanart = fanart , thumbnail = thumbnail , folder = False, isPlayable = True)                     
    elif url.find("netu") >= 0:
        server_url = "[COLOR lightgreen][I][netu][/I][/COLOR]"
        plugintools.add_item(action="netu", title= '[COLOR white]'+title_fixed+' [/COLOR][COLOR lightyellow][I]('+server_name+')[/I][/COLOR]  [COLOR lightgreen][I]'+lang+'[/I][/COLOR]' , url = url, info_labels = datamovie , extra = show , page = show , fanart = fanart , thumbnail = thumbnail , folder = False, isPlayable = True)
    elif url.find("videomega") >= 0:
        server_url = "[COLOR lightgreen][I][videomega][/I][/COLOR]"
        plugintools.add_item(action="videomega", title= '[COLOR white]'+title_fixed+' [/COLOR][COLOR lightyellow][I]('+server_name+')[/I][/COLOR]  [COLOR lightgreen][I]'+lang+'[/I][/COLOR]' , url = url, info_labels = datamovie , extra = show , page = show , fanart = fanart , thumbnail = thumbnail , folder = False, isPlayable = True)
    elif url.find("video.tt") >= 0:
        server_url = "[COLOR lightgreen][I][video.tt][/I][/COLOR]"
        plugintools.add_item(action="videott", title= '[COLOR white]'+title_fixed+' [/COLOR][COLOR lightyellow][I]('+server_name+')[/I][/COLOR]  [COLOR lightgreen][I]'+lang+'[/I][/COLOR]' , url = url, info_labels = datamovie , extra = show , page = show , fanart = fanart , thumbnail = thumbnail , folder = False, isPlayable = True)
    elif url.find("flashx.tv") >= 0:
        server_url = "[COLOR lightgreen][I][flashx][/I][/COLOR]"
        plugintools.add_item(action="flashx", title= '[COLOR white]'+title_fixed+' [/COLOR][COLOR lightyellow][I]('+server_name+')[/I][/COLOR]  [COLOR lightgreen][I]'+lang+'[/I][/COLOR]' , url = url, info_labels = datamovie , extra = show , page = show , fanart = fanart , thumbnail = thumbnail , folder = False, isPlayable = True)                             


def categorias_flv(data,show):
    plugintools.log("[Arena+ 0.3.4] SeriesFLV Categorias ")

    plugintools.modo_vista(show)
    #plugintools.log("show= "+show)    

    params = plugintools.get_params()
    thumbnail = params.get("thumbnail")
    if thumbnail == "":  
        thumbnail = 'http://m1.paperblog.com/i/249/2490697/seriesflv-mejor-alternativa-series-yonkis-L-2whffw.jpeg'
    fanart = 'http://www.nikopik.com/wp-content/uploads/2011/10/S%C3%A9ries-TV.jpg'

    sinopsis = params.get("plot")
    datamovie = {}
    datamovie["Plot"]=sinopsis      
    
    sections = plugintools.find_single_match(data, '<div class="lang over font2 bold">(.*?)</div>')
    #plugintools.log("sections= "+sections)
    tipo_selected = plugintools.find_single_match(sections, 'class="select">(.*?)</a>')
    plugintools.add_item(action="listado_seriesflv", title='[COLOR orange]Listado completo[/COLOR]' , url = "http://www.seriesflv.net/series/", extra = data , info_labels = datamovie , page = show , thumbnail = thumbnail , fanart = fanart , folder = True, isPlayable = False)
    plugintools.add_item(action="lista_chapters", title='[COLOR orange]'+tipo_selected+'[/COLOR]' , url = "", extra = data , info_labels = datamovie , page = show , thumbnail = thumbnail , fanart = fanart , folder = True, isPlayable = False)
    tipos = plugintools.find_multiple_matches(sections, ';">(.*?)</a>')
    for entry in tipos:
        plugintools.add_item(action="lista_chapters", title='[COLOR orange]'+entry+'[/COLOR]' , url = "", thumbnail = thumbnail , extra = data , plot = datamovie["Plot"] , info_labels = datamovie , page = show , fanart = fanart , folder = True, isPlayable = False)
        

def lista_chapters(params):
    plugintools.log("[Arena+ 0.3.4] SeriesFLV Lista_chapters "+repr(params))

    url = params.get("url")
    referer = 'http://www.seriesflv.com/'
    show = plugintools.get_setting("series_id")
    if show == "":
        show = "tvshows"
        plugintools.modo_vista(show)
        #plugintools.log("show= "+show)
     
    data = gethttp_referer_headers(url, referer, show)
    #plugintools.log("data= "+data) 

    thumbnail = params.get("thumbnail")
    if thumbnail == "":  
        thumbnail = 'http://m1.paperblog.com/i/249/2490697/seriesflv-mejor-alternativa-series-yonkis-L-2whffw.jpeg'
    fanart = 'http://www.nikopik.com/wp-content/uploads/2011/10/S%C3%A9ries-TV.jpg'

    sinopsis = params.get("plot")
    datamovie = {}
    datamovie["Plot"]=sinopsis 

    chapters = plugintools.find_multiple_matches(data, '<a href="http://www.seriesflv.net/ver/(.*?)</a>')
    title = params.get("title")
    for entry in chapters:
        if title.find("Subtitulada") >= 0:            
            if entry.find('lang="sub"') >=0:
                #plugintools.log("entry= "+entry)
                entry_fixed = entry.split('"')
                url_chapter = 'http://www.seriesflv.net/ver/'+entry_fixed[0]
                #plugintools.log("url_chapter= "+url_chapter)
                title_chapter = plugintools.find_single_match(entry, '<div class="i-title">(.*?)</div>')
                #plugintools.log("title_chapter= "+title_chapter)
                num_chapter = plugintools.find_single_match(entry, '<div class="box-tc">(.*?)</div>')
                #plugintools.log("núm. capítulo= "+num_chapter)
                i_time = plugintools.find_single_match(entry, '<div class="i-time">(.*?)</div>')
                #plugintools.log("desde hace= "+i_time)
                plugintools.add_item(action="chapter_urls", title='[COLOR orange]'+num_chapter+'[/COLOR]'+'  [COLOR lightyellow][B]'+title_chapter+'[/B][/COLOR][COLOR lightgreen][I] ('+i_time+')[/I][/COLOR]' , info_labels = datamovie , plot = datamovie["Plot"] , extra = show , page = show , url = url_chapter , thumbnail = thumbnail , fanart = fanart , folder = True, isPlayable = False)

        if title.find("Español") >= 0:        
            if entry.find('lang="es"') >= 0:
                #plugintools.log("entry= "+entry)
                entry_fixed = entry.split('"')
                url_chapter = 'http://www.seriesflv.net/ver/'+entry_fixed[0]
                #plugintools.log("url_chapter= "+url_chapter)
                title_chapter = plugintools.find_single_match(entry, '<div class="i-title">(.*?)</div>')
                #plugintools.log("title_chapter= "+title_chapter)
                num_chapter = plugintools.find_single_match(entry, '<div class="box-tc">(.*?)</div>')
                #plugintools.log("núm. capítulo= "+num_chapter)
                i_time = plugintools.find_single_match(entry, '<div class="i-time">(.*?)</div>')
                #plugintools.log("desde hace= "+i_time)
                plugintools.add_item(action="chapter_urls", title='[COLOR orange]'+num_chapter+'[/COLOR]'+'  [COLOR lightyellow][B]'+title_chapter+'[/B][/COLOR][COLOR lightgreen][I] ('+i_time+')[/I][/COLOR]' , url = url_chapter , info_labels = datamovie , plot = datamovie["Plot"] , extra = show , page = show , thumbnail = thumbnail , fanart = fanart , folder = True, isPlayable = False)

        if title.find("Latino") >= 0:
            if entry.find('lang="la"') >= 0:
                #plugintools.log("entry= "+entry)
                entry_fixed = entry.split('"')
                url_chapter = 'http://www.seriesflv.net/ver/'+entry_fixed[0]
                #plugintools.log("url_chapter= "+url_chapter)
                title_chapter = plugintools.find_single_match(entry, '<div class="i-title">(.*?)</div>')
                #plugintools.log("title_chapter= "+title_chapter)
                num_chapter = plugintools.find_single_match(entry, '<div class="box-tc">(.*?)</div>')
                #plugintools.log("núm. capítulo= "+num_chapter)
                i_time = plugintools.find_single_match(entry, '<div class="i-time">(.*?)</div>')
                #plugintools.log("desde hace= "+i_time)
                plugintools.add_item(action="chapter_urls", title='[COLOR orange]'+num_chapter+'[/COLOR]'+'  [COLOR lightyellow][B]'+title_chapter+'[/B][/COLOR][COLOR lightgreen][I] ('+i_time+')[/I][/COLOR]' , url = url_chapter , info_labels = datamovie , plot = datamovie["Plot"] , extra = show , page = show , thumbnail = thumbnail , fanart = fanart , folder = True, isPlayable = False)

        if title.find("Original") >= 0:  
            if entry.find('lang="en"') >= 0:
                #plugintools.log("entry= "+entry)
                entry_fixed = entry.split('"')
                url_chapter = 'http://www.seriesflv.net/ver/'+entry_fixed[0]
                #plugintools.log("url_chapter= "+url_chapter)
                title_chapter = plugintools.find_single_match(entry, '<div class="i-title">(.*?)</div>')
                #plugintools.log("title_chapter= "+title_chapter)
                num_chapter = plugintools.find_single_match(entry, '<div class="box-tc">(.*?)</div>')
                #plugintools.log("núm. capítulo= "+num_chapter)
                i_time = plugintools.find_single_match(entry, '<div class="i-time">(.*?)</div>')
                #plugintools.log("desde hace= "+i_time)
                plugintools.add_item(action="chapter_urls", title='[COLOR orange]'+num_chapter+'[/COLOR]'+'  [COLOR lightyellow][B]'+title_chapter+'[/B][/COLOR][COLOR lightgreen][I] ('+i_time+')[/I][/COLOR]' , url = url_chapter , info_labels = datamovie , plot = datamovie["Plot"] , extra = show , page = show , thumbnail = thumbnail , fanart = fanart , folder = True, isPlayable = False)



def oranline2(id_link, url):
    plugintools.log("[%s %s] Oranline2 %s %s" % (addonName, addonVersion, id_link, url))

    geturl = 'http://www.oranline.com/wp-content/themes/reviewit/enlace.php?id='+id_link
    headers = {'user-agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14', 'Referer': url}
    r = requests.get(geturl, headers=headers)
    data = r.content
    print data
    url = 'http'+plugintools.find_single_match(data, '<a href="http([^"]+)')
    #plugintools.log("url= "+url)
    return url




def gethttp_referer_headers(url,referer,show):
    plugintools.modo_vista(show)
    #plugintools.log("show= "+show)  
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    request_headers.append(["Referer", referer])
    request_headers.append(["X-Requested-With", "XMLHttpRequest"])
    request_headers.append(["Cookie:","__utma=253162379.286456173.1418323503.1421078750.1422185754.16; __utmz=253162379.1421070671.14.3.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=http%3A%2F%2Fwww.seriesflv.net%2Fserie%2Fhora-de-aventuras.html; __cfduid=daeed6a2aacaffab2433869fd863162821419890996; __utmb=253162379.4.10.1422185754; __utmc=253162379; __utmt=1"])
    body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers);print response_headers
    return body


