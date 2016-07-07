# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Parser de Kickass.so para PLD.VisionTV
# Version 0.1
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Gracias a la librería plugintools de Jesús (www.mimediacenter.info)
#------------------------------------------------------------

import os
import sys
import urllib
import urllib2
import re

import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin

import re,urllib,urllib2,sys
import plugintools

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")


thumbnail = 'http://m1.paperblog.com/i/249/2490697/seriesflv-mejor-alternativa-series-yonkis-L-2whffw.jpeg'
fanart = 'http://www.nikopik.com/wp-content/uploads/2011/10/S%C3%A9ries-TV.jpg'
referer = 'http://www.kickass.so/'


def kickass0(params):		
    plugintools.log('[%s %s] Kickass regex %s' % (addonName, addonVersion, repr(params)))
    
    url = params.get("url")
    data = gethttp_referer_headers(url,referer)
    resultados = plugintools.find_multiple_matches(data, "{ 'name':(.*?)}")
    for entry in resultados:
        entry = entry.replace("'","").replace("magnet:","").strip().split(",")
        titulo = entry[0]
        titulo=urllib.unquote(titulo)
        url = entry[1].strip()
        url=urllib.unquote(url)
        url = 'plugin://plugin.video.pulsar/play?uri='+url
        plugintools.log("url= "+url)
        plugintools.add_item(action="", title = titulo , url = url , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True)

       
            

def gethttp_referer_headers(url,referer):
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    request_headers.append(["Referer", referer])
    data,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)      
    return data

