# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Regex de Seriesadicto para PLD.VisionTV
# Version 0.1
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Librerías Plugintools por Jesús (www.mimediacenter.info)
#------------------------------------------------------------

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
from resources.tools.resolvers import *
from resources.tools.media_analyzer import *

fanart = "http://socialgeek.co/wp-content/uploads/2013/06/series-TV-Collage-television-10056729-2560-1600.jpg"

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")

def seriecatcher(params):
    #plugintools.log("[%s %s] Seriesadicto: seriecatcher() %s" % (addonName, addonVersion, repr(params)))

    show = params.get("series_id")  # Obtenemos modo de vista del usuario para series TV
    if show is None:
        show = params.get("page")
        if show is None:
            show = "tvshows"
    plugintools.log("show= "+show)            
    plugintools.modo_vista(show)    
    
    url = params.get("url")
    data = plugintools.read(url)
    temp = plugintools.find_multiple_matches(data, '<i class=\"glyphicon\"></i>(.*?)</a>')
    SelectTemp(params, show, temp)


def GetSerieChapters(params):
    #plugintools.log("[%s %s] Seriesadicto: getseriechapters() %s" % (addonName, addonVersion, repr(params)))

    season = params.get("season")
    datamovie = {}
    datamovie["Plot"] = params.get("plot")
    data = plugintools.read(params.get("url"))
    show = params.get("series_id")  # Obtenemos modo de vista del usuario para series TV
    if show is None:
        show = params.get("page")
        if show is None:
            show = "tvshows"
    plugintools.log("show= "+show)            
    plugintools.modo_vista(show)        
    
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
        fanart = "http://socialgeek.co/wp-content/uploads/2013/06/series-TV-Collage-television-10056729-2560-1600.jpg"
        plugintools.add_item(action="seriesadicto4", title= title_fixed, url = url_cap_fixed, thumbnail = params.get("thumbnail") , extra = str(i) , info_labels = datamovie , page = show , plot = datamovie["Plot"] , fanart = fanart, folder = True, isPlayable = False)        
        i = i + 1
        
        
    
def seriesadicto4(params):
    #plugintools.log("[%s %s] Seriesadicto: getserielinks() %s" % (addonName, addonVersion, repr(params)))

    show = params.get("series_id")  # Obtenemos modo de vista del usuario para series TV
    if show is None:
        show = params.get("page")
        if show is None:
            show = "tvshows"
    plugintools.log("show= "+show)            
    plugintools.modo_vista(show)
    
    url_cap_fixed = params.get("url")
    title_fixed = params.get("title")
    data = plugintools.read(url_cap_fixed)
    #plugintools.log("data= "+data)
    
    # Thumbnail, sinopsis y fanart
    thumbnail = plugintools.find_single_match(data, 'src=\"/img/series/(.*?)"')
    thumbnail_fixed = 'http://seriesadicto.com/img/series/' + thumbnail
    fanart = "http://socialgeek.co/wp-content/uploads/2013/06/series-TV-Collage-television-10056729-2560-1600.jpg"
    datamovie = {}
    datamovie["Plot"] = params.get("plot")

    matches = plugintools.find_multiple_matches(data, '<td class="enlacevideo"(.*?)/></td>')
    for entry in matches:
        #plugintools.log("entry= "+entry)
        audio_url = plugintools.find_single_match(entry, '<img src="([^"]+)')
        if audio_url == "/img/1.png":
            audio_url = "[COLOR lightyellow][I][ESP][/I][/COLOR]"
        elif audio_url == "/img/2.png":
            audio_url = "[COLOR lightyellow][I][LAT][/I][/COLOR]"
        elif audio_url == "/img/3.png":
            audio_url = "[COLOR lightyellow][I][VOS][/I][/COLOR]"
        elif audio_url == "/img/4.png":
            audio_url = "[COLOR lightyellow][I][ENG][/I][/COLOR]"
        page_url = plugintools.find_single_match(entry, '<a href="([^"]+)')
        server = video_analyzer(page_url)
        plugintools.add_item(action=server, title = title_fixed+' [COLOR lightgreen][I]['+server+'][/I][/COLOR] '+audio_url , url = page_url , thumbnail = thumbnail_fixed, info_labels = datamovie , fanart = fanart, folder = False, isPlayable = True)

    plugintools.modo_vista(show) 


def SelectTemp(params, show, temp):
    #plugintools.log("[%s %a] Seriesadicto: selectTemp() " % (addonName, addonVersion, repr(params)))

    show = params.get("series_id")  # Obtenemos modo de vista del usuario para series TV
    if show is None:
        show = params.get("page")
        if show is None:
            show = "tvshows"
    plugintools.log("show= "+show)            
    plugintools.modo_vista(show)

    titles_temp = []
    seasons = len(temp)
    i = 1
    while i <= seasons:
        titles_temp.append('[COLOR lightyellow]'+params.get("title").replace("[Multiparser]", "").strip()+': [/COLOR]Temporada '+str(i))
        i = i + 1

    print titles_temp    
    select_temp = plugintools.selector(titles_temp, 'PLD.VisionTV')
    i = 0
    while i<= seasons :
        if select_temp == i:
            params["season"] = temp[i]
            GetSerieChapters(params)

        i = i + 1

    plugintools.modo_vista(show)
