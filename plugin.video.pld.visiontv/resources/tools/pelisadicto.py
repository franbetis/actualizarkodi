# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Seriesadicto.com parser para PLD.VisionTV
# Version 0.1 (20/12/2014)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Librerías Plugintools por Jesús (www.mimediacenter.info)


import os
import sys
import urllib
import urllib2
import re
import shutil
import zipfile

import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin

import plugintools


addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")



# Lectura de cada carátula, título y enlace a la página de descargas de la peli
def pelicatcher(params):
    plugintools.log("[%s %s] Pelisadicto regex %s" % (addonName, addonVersion, repr(params)))
    
    url = params.get("url")
    data = plugintools.read(url)
    plugintools.log("data= "+data)
    items = plugintools.find_multiple_matches(data, '<li class="col-xs-6 col-sm-2(.*?)</li>')
    for entry in items:
        plugintools.log("entry= "+entry)
        thumbnail = plugintools.find_single_match(entry, 'src="([^"]+)')
        thumbnail = 'http://www.pelisadicto.com'+thumbnail
        plugintools.log("thumbnail= "+thumbnail)
        title = plugintools.find_single_match(entry, 'title="([^"]+)')
        title = title.replace("Ver", "").replace("Online", "").strip()
        plugintools.log("title= "+title)        
        movie_url = 'http://www.pelisadicto.com' + plugintools.find_single_match(entry, 'href="([^"]+)')
        plugintools.log("movie_url= "+movie_url)
        plugintools.add_item(action="", title=title, url=movie_url, thumbnail = thumbnail, fanart = fanart, folder = True, isPlayable = False)
        
        


def GetSerieChapters(params):
    plugintools.log("[%s %s].GetSerieChapters " % (addonName, addonVersion))

    season = params.get("season")
    data = plugintools.read(params.get("url"))
    
    season = plugintools.find_multiple_matches(data, season + '(.*?)</table>')
    season = season[0]
    
    for entry in season:
        url_cap = plugintools.find_multiple_matches(season, '<a href=\"/capitulo(.*?)\" class=\"color4\"')
        title = plugintools.find_multiple_matches(season, 'class=\"color4\">(.*?)</a>')

    num_items = len(url_cap)    
    i = 1
    
    while i <= num_items:
        url_cap_fixed = 'http://seriesadicto.com/capitulo/' + url_cap[i-1]
        title_fixed = title[i-1]
        fanart = params.get("extra")
        GetSerieLinks(fanart , url_cap_fixed, i, title_fixed)
        i = i + 1
        
        
    
def GetSerieLinks(fanart , url_cap_fixed, i, title_fixed):
    plugintools.log("[%s %s].GetSerieLinks " % (addonName, addonVersion))
    
    data = plugintools.read(url_cap_fixed)
    amv = plugintools.find_multiple_matches(data, 'allmyvideos.net/(.*?)"')
    strcld = plugintools.find_multiple_matches(data, 'streamcloud.eu/(.*?)"')
    vdspt = plugintools.find_multiple_matches(data, 'vidspot.net/(.*?)"')
    plydt = plugintools.find_multiple_matches(data, 'played.to/(.*?)"')
    thumbnail = plugintools.find_single_match(data, 'src=\"/img/series/(.*?)"')
    thumbnail_fixed = 'http://seriesadicto.com/img/series/' + thumbnail
    
    for entry in amv:
        amv_url = 'http://allmyvideos.net/' + entry        
        plugintools.add_item(action="play" , title = title_fixed + '[COLOR lightyellow] [Allmyvideos][/COLOR]', url = amv_url , thumbnail = thumbnail_fixed , fanart = fanart , folder = False , isPlayable = True)

    for entry in strcld:
        strcld_url = 'http://streamcloud.eu/' + entry
        plugintools.add_item(action="play" , title = title_fixed + '[COLOR lightskyblue] [Streamcloud][/COLOR]', url = strcld_url , thumbnail = thumbnail_fixed , fanart = fanart , folder = False , isPlayable = True)

    for entry in vdspt:
        vdspt_url = 'http://vidspot.net/' + entry
        plugintools.add_item(action="play" , title = title_fixed + '[COLOR palegreen] [Vidspot][/COLOR]', url = vdspt_url , thumbnail = thumbnail_fixed , fanart = fanart , folder = False , isPlayable = True)

    for entry in plydt:
        plydt_url = 'http://played.to/' + entry
        plugintools.add_item(action="play" , title = title_fixed + '[COLOR lavender] [Played.to][/COLOR]', url = plydt_url , thumbnail = thumbnail_fixed , fanart = fanart , folder = False , isPlayable = True)

    for entry in plydt:
        plydt_url = 'vk.com' + entry
        plugintools.add_item(action="play" , title = title_fixed + '[COLOR royalblue] [Vk][/COLOR]', url = plydt_url , thumbnail = thumbnail_fixed , fanart = fanart , folder = False , isPlayable = True)

    for entry in plydt:
        plydt_url = 'nowvideo.sx' + entry
        plugintools.add_item(action="play" , title = title_fixed + '[COLOR red] [Nowvideo][/COLOR]', url = plydt_url , thumbnail = thumbnail_fixed , fanart = fanart , folder = False , isPlayable = True)           

    for entry in plydt:
        plydt_url = 'http://tumi.tv/' + entry
        plugintools.add_item(action="play" , title = title_fixed + '[COLOR forestgreen] [Tumi][/COLOR]', url = plydt_url , thumbnail = thumbnail_fixed , fanart = fanart , folder = False , isPlayable = True)

        
        

def SelectTemp(params, temp):
    plugintools.log("[%s %s].SelectTemp " % (addonName, addonVersion))

    seasons = len(temp)
    
    dialog = xbmcgui.Dialog()
    
    if seasons == 1:
        selector = dialog.select('PLD.VisionTV', [temp[0]])
                                             
    if seasons == 2:
        selector = dialog.select('PLD.VisionTV', [temp[0], temp[1]])
                                             
    if seasons == 3:
        selector = dialog.select('PLD.VisionTV', [temp[0],temp[1], temp[2]])
                                             
    if seasons == 4:
        selector = dialog.select('PLD.VisionTV', [temp[0], temp[1],temp[2], temp[3]])
                                             
    if seasons == 5:
        selector = dialog.select('PLD.VisionTV', [temp[0], temp[1],temp[2], temp[3], temp[4]])
        
    if seasons == 6:
        selector = dialog.select('PLD.VisionTV', [temp[0], temp[1],temp[2], temp[3], temp[4], temp[5]])
        
    if seasons == 7:
        selector = dialog.select('PLD.VisionTV', [temp[0], temp[1],temp[2], temp[3], temp[4], temp[5], temp[6]])
        
    if seasons == 8:
        selector = dialog.select('PLD.VisionTV', [temp[0], temp[1],temp[2], temp[3], temp[4], temp[5], temp[6], temp[7]])
        
    if seasons == 9:
        selector = dialog.select('PLD.VisionTV', [temp[0], temp[1],temp[2], temp[3], temp[4], temp[5], temp[6], temp[7], temp[8]])
        
    if seasons == 10:
        selector = dialog.select('PLD.VisionTV', [temp[0], temp[1],temp[2], temp[3], temp[4], temp[5], temp[6], temp[7], temp[8], temp[9]])                               

    i = 0
    while i<= seasons :
        if selector == i:
            params["season"] = temp[i]
            GetSerieChapters(params)

        i = i + 1


def pelisadicto0(params):  # Regex de pelis
    plugintools.log("Pelisadicto regex "+repr(params))

    show='tvshows';plugintools.modo_vista(show)
    data = plugintools.read(params.get("url"))
    datamovie = {}

    tablesinopsis = plugintools.find_single_match(data, '<h2>Sinopsis(.*?)<p>Genero');plugintools.log("table sinopsis="+tablesinopsis)
    sinopsis = plugintools.find_single_match(tablesinopsis, '<p>(.*?)</p>');datamovie["Plot"]=sinopsis
    
    tabledata = plugintools.find_single_match(data, '<table class="table table-hover">(.*?)</table>')
    url_entry = plugintools.find_multiple_matches(tabledata, '<tr>(.*?)</tr>')
    thumbnail = plugintools.find_single_match(data, 'og:image" content=\"([^"]+)')
    #plugintools.log("thumb= "+thumbnail)
    #fanart = "http://socialgeek.co/wp-content/uploads/2013/06/series-TV-Collage-television-10056729-2560-1600.jpg"
    title=params.get("title").replace("[Multiparser]", "").strip()
    
    for entry in url_entry:
        plugintools.log("entry= "+entry)
        url_peli = plugintools.find_single_match(entry, '<a href="([^"]+)')
        plugintools.log("url_peli= "+url_peli)
        lang_audio = plugintools.find_single_match(entry, '<img src="/img/([^"]+)')
        if lang_audio.find("1.png") >= 0:
            lang_audio = "ESP"
        elif lang_audio.find("2.png") >= 0:
            lang_audio = "LAT"
        elif lang_audio.find("3.png") >= 0:
            lang_audio = "V.O.S."
        elif lang_audio.find("4.png") >= 0:
            lang_audio = "V.O."         
        if url_peli.find("allmyvideos") >=0:
            url_server = "allmyvideos"
            plugintools.add_item(action="allmyvideos", title=title+'[COLOR lightgreen][I] ['+lang_audio+'] [/I][/COLOR]'+'[COLOR lightyellow][I] ['+url_server+'][/I][/COLOR]', url = url_peli, info_labels = datamovie , page = show , thumbnail = thumbnail, fanart = thumbnail , folder = False, isPlayable = True)
        elif url_peli.find("vidspot") >= 0:
            url_server = "vidspot"
            plugintools.add_item(action="vidspot", title=title+'[COLOR lightgreen][I] ['+lang_audio+'] [/I][/COLOR]'+'[COLOR lightyellow][I] ['+url_server+'][/I][/COLOR]', url = url_peli, info_labels = datamovie , page = show , thumbnail = thumbnail, fanart = thumbnail , folder = False, isPlayable = True)
        elif url_peli.find("played.to") >= 0:
            url_server = "played.to"
            plugintools.add_item(action="playedto", title=title+'[COLOR lightgreen][I] ['+lang_audio+'] [/I][/COLOR]'+'[COLOR lightyellow][I] ['+url_server+'][/I][/COLOR]', url = url_peli, info_labels = datamovie , page = show , thumbnail = thumbnail, fanart = thumbnail , folder = False, isPlayable = True)
        elif url_peli.find("streamin.to") >= 0:
            url_server = "streamin.to"
            plugintools.add_item(action="streaminto", title=title+'[COLOR lightgreen][I] ['+lang_audio+'] [/I][/COLOR]'+'[COLOR lightyellow][I] ['+url_server+'][/I][/COLOR]', url = url_peli, info_labels = datamovie , page = show , thumbnail = thumbnail, fanart = thumbnail , folder = False, isPlayable = True)
        elif url_peli.find("streamcloud") >= 0:
            url_server = "streamcloud"
            plugintools.add_item(action="streamcloud", title=title+'[COLOR lightgreen][I] ['+lang_audio+'] [/I][/COLOR]'+'[COLOR lightyellow][I] ['+url_server+'][/I][/COLOR]', url = url_peli, info_labels = datamovie , page = show , thumbnail = thumbnail, fanart = thumbnail , folder = False, isPlayable = True)
        elif url_peli.find("nowvideo") >= 0:
            url_server = "nowvideo"
            plugintools.add_item(action="nowvideo", title=title+'[COLOR lightgreen][I] ['+lang_audio+'] [/I][/COLOR]'+'[COLOR lightyellow][I] ['+url_server+'][/I][/COLOR]', url = url_peli, info_labels = datamovie , page = show , thumbnail = thumbnail, fanart = thumbnail , folder = False, isPlayable = True)
        elif url_peli.find("veehd") >= 0:
            url_server = "veehd"
            plugintools.add_item(action="veehd", title=title+'[COLOR lightgreen][I] ['+lang_audio+'] [/I][/COLOR]'+'[COLOR lightyellow][I] ['+url_server+'][/I][/COLOR]', url = url_peli, info_labels = datamovie , page = show , thumbnail = thumbnail, fanart = thumbnail , folder = False, isPlayable = True)
        elif url_peli.find("vk") >= 0:
            url_server = "vk"
            plugintools.add_item(action="vk", title=title+'[COLOR lightgreen][I] ['+lang_audio+'] [/I][/COLOR]'+'[COLOR lightyellow][I] ['+url_server+'][/I][/COLOR]', url = url_peli, info_labels = datamovie , page = show , thumbnail = thumbnail, fanart = thumbnail , folder = False, isPlayable = True)
        elif url_peli.find("tumi") >= 0:
            url_server = "tumi"
            plugintools.add_item(action="tumi", title=title+'[COLOR lightgreen][I] ['+lang_audio+'] [/I][/COLOR]'+'[COLOR lightyellow][I] ['+url_server+'][/I][/COLOR]', url = url_peli, info_labels = datamovie , page = show , thumbnail = thumbnail, fanart = thumbnail , folder = False, isPlayable = True)
        elif url_peli.find("novamov") >= 0:
            url_server = "novamov"
            plugintools.add_item(action="novamov", title=title+'[COLOR lightgreen][I] ['+lang_audio+'] [/I][/COLOR]'+'[COLOR lightyellow][I] ['+url_server+'][/I][/COLOR]', url = url_peli, info_labels = datamovie , page = show , thumbnail = thumbnail, fanart = thumbnail , folder = False, isPlayable = True)
        elif url_peli.find("moevideos") >= 0:
            url_server = "moevideos"
            plugintools.add_item(action="moevideos", title=title+'[COLOR lightgreen][I] ['+lang_audio+'] [/I][/COLOR]'+'[COLOR lightyellow][I] ['+url_server+'][/I][/COLOR]', url = url_peli, info_labels = datamovie , page = show , thumbnail = thumbnail, fanart = thumbnail , folder = False, isPlayable = True)
        elif url_peli.find("gamovideo") >= 0:
            url_server = "gamovideo"
            plugintools.add_item(action="gamovideo", title=title+'[COLOR lightgreen][I] ['+lang_audio+'] [/I][/COLOR]'+'[COLOR lightyellow][I] ['+url_server+'][/I][/COLOR]', url = url_peli, info_labels = datamovie , page = show , thumbnail = thumbnail, fanart = thumbnail , folder = False, isPlayable = True)
        elif url_peli.find("movshare") >= 0:
            url_server = "movshare"
            plugintools.add_item(action="movshare", title=title+'[COLOR lightgreen][I] ['+lang_audio+'] [/I][/COLOR]'+'[COLOR lightyellow][I] ['+url_server+'][/I][/COLOR]', url = url_peli, info_labels = datamovie , page = show , thumbnail = thumbnail, fanart = thumbnail , folder = False, isPlayable = True)
        elif url_peli.find("movreel") >= 0:
            url_server = "movreel"
            plugintools.add_item(action="movreel", title=title+'[COLOR lightgreen][I] ['+lang_audio+'] [/I][/COLOR]'+'[COLOR lightyellow][I] ['+url_server+'][/I][/COLOR]', url = url_peli, info_labels = datamovie , page = show , thumbnail = thumbnail, fanart = thumbnail , folder = False, isPlayable = True)            
        elif url_peli.find("powvideo") >= 0:
            url_server = "powvideo"
            plugintools.add_item(action="powvideo", title=title+'[COLOR lightgreen][I] ['+lang_audio+'] [/I][/COLOR]'+'[COLOR lightyellow][I] ['+url_server+'][/I][/COLOR]', url = url_peli, info_labels = datamovie , page = show , thumbnail = thumbnail, fanart = thumbnail , folder = False, isPlayable = True)
        elif url_peli.find("mail.ru") >= 0:
            url_server = "mailru"
            plugintools.add_item(action="mailru", title=title+'[COLOR lightgreen][I] ['+lang_audio+'] [/I][/COLOR]'+'[COLOR lightyellow][I] ['+url_server+'][/I][/COLOR]', url = url_peli, info_labels = datamovie , page = show , thumbnail = thumbnail, fanart = thumbnail , folder = False, isPlayable = True)
        elif url_peli.find("netu") >= 0:
            url_server = "netu"
            plugintools.add_item(action="netu", title=title+'[COLOR lightgreen][I] ['+lang_audio+'] [/I][/COLOR]'+'[COLOR lightyellow][I] ['+url_server+'][/I][/COLOR]', url = url_peli, info_labels = datamovie , page = show , thumbnail = thumbnail, fanart = thumbnail , folder = False, isPlayable = True)
        elif url_peli.find("videobam") >= 0:
            url_server = "videobam"
            plugintools.add_item(action="videobam", title=title+'[COLOR lightgreen][I] ['+lang_audio+'] [/I][/COLOR]'+'[COLOR lightyellow][I] ['+url_server+'][/I][/COLOR]', url = url_peli, info_labels = datamovie , page = show , thumbnail = thumbnail, fanart = thumbnail , folder = False, isPlayable = True)
        elif url_peli.find("videoweed") >= 0:
            url_server = "videoweed"
            plugintools.add_item(action="videoweed", title=title+'[COLOR lightgreen][I] ['+lang_audio+'] [/I][/COLOR]'+'[COLOR lightyellow][I] ['+url_server+'][/I][/COLOR]', url = url_peli, info_labels = datamovie , page = show , thumbnail = thumbnail, fanart = thumbnail , folder = False, isPlayable = True)
        elif url_peli.find("streamable") >= 0:
            url_server = "streamable"
            plugintools.add_item(action="streamable", title=title+'[COLOR lightgreen][I] ['+lang_audio+'] [/I][/COLOR]'+'[COLOR lightyellow][I] ['+url_server+'][/I][/COLOR]', url = url_peli, info_labels = datamovie , page = show , thumbnail = thumbnail, fanart = thumbnail , folder = False, isPlayable = True)
        elif url_peli.find("rocvideo") >= 0:
            url_server = "rocvideo"
            plugintools.add_item(action="rocvideo", title=title+'[COLOR lightgreen][I] ['+lang_audio+'] [/I][/COLOR]'+'[COLOR lightyellow][I] ['+url_server+'][/I][/COLOR]', url = url_peli, info_labels = datamovie , page = show , thumbnail = thumbnail, fanart = thumbnail , folder = False, isPlayable = True)
        elif url_peli.find("realvid") >= 0:
            url_server = "realvid"
            plugintools.add_item(action="realvid", title=title+'[COLOR lightgreen][I] ['+lang_audio+'] [/I][/COLOR]'+'[COLOR lightyellow][I] ['+url_server+'][/I][/COLOR]', url = url_peli, info_labels = datamovie , page = show , thumbnail = thumbnail, fanart = thumbnail , folder = False, isPlayable = True)
        elif url_peli.find("netu") >= 0:
            url_server = "netu"
            plugintools.add_item(action="netu", title=title+'[COLOR lightgreen][I] ['+lang_audio+'] [/I][/COLOR]'+'[COLOR lightyellow][I] ['+url_server+'][/I][/COLOR]', url = url_peli, info_labels = datamovie , page = show , thumbnail = thumbnail, fanart = thumbnail , folder = False, isPlayable = True)
        elif url_peli.find("videomega") >= 0:
            url_server = "videomega"
            plugintools.add_item(action="videomega", title=title+'[COLOR lightgreen][I] ['+lang_audio+'] [/I][/COLOR]'+'[COLOR lightyellow][I] ['+url_server+'][/I][/COLOR]', url = url_peli, info_labels = datamovie , page = show , thumbnail = thumbnail, fanart = thumbnail , folder = False, isPlayable = True)            
        elif url_peli.find("video.tt") >= 0:
            url_server = "videott"
            plugintools.add_item(action="videott", title=title+'[COLOR lightgreen][I] ['+lang_audio+'] [/I][/COLOR]'+'[COLOR lightyellow][I] ['+url_server+'][/I][/COLOR]', url = url_peli, info_labels = datamovie , page = show , thumbnail = thumbnail, fanart = thumbnail , folder = False, isPlayable = True)
        elif url_peli.find("flashx.tv") >= 0:
            url_server = "flashx"
            plugintools.add_item(action="videott", title=title+'[COLOR lightgreen][I] ['+lang_audio+'] [/I][/COLOR]'+'[COLOR lightyellow][I] ['+url_server+'][/I][/COLOR]', url = url_peli, info_labels = datamovie , page = show , thumbnail = thumbnail, fanart = thumbnail , folder = False, isPlayable = True)
        elif url_peli.find("turbovideos") >= 0:
            url_server = "turbovideos"
            plugintools.add_item(action="turbovideos", title=title+'[COLOR lightgreen][I] ['+lang_audio+'] [/I][/COLOR]'+'[COLOR lightyellow][I] ['+url_server+'][/I][/COLOR]', url = url_peli, info_labels = datamovie , page = show , thumbnail = thumbnail, fanart = thumbnail , folder = False, isPlayable = True)                        
        elif url_peli.find("vidto.me") >= 0:
            url_server = "vidto.me"
            plugintools.add_item(action="vidtome", title=title+'[COLOR lightgreen][I] ['+lang_audio+'] [/I][/COLOR]'+'[COLOR lightyellow][I] ['+url_server+'][/I][/COLOR]', url = url_peli, info_labels = datamovie , page = show , thumbnail = thumbnail, fanart = thumbnail , folder = False, isPlayable = True)                        
            
        
        plugintools.modo_vista(show)


