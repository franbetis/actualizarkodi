# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Dailymotion en PLD.VisionTV
# Version 0.1
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Gracias a la librería plugintools de Jesús (www.mimediacenter.info)


import os
import sys
import urllib
import urllib2
import re
import shutil
import zipfile
import time

import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin

import plugintools
import json
import math


addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")

playlists = xbmc.translatePath(os.path.join('special://userdata/playlists', ''))
temp = xbmc.translatePath(os.path.join('special://userdata/playlists/tmp', ''))


def dailym_getplaylist(url):	
    plugintools.log('[%s %s] Dailymotion: %s' % (addonName, addonVersion, repr(params)))
    
    # Fetch video list from Dailymotion playlist user
    data = plugintools.read(url)
    #plugintools.log("data= "+data)

    # Extract items from feed
    pattern = ""
    matches = plugintools.find_multiple_matches(data,'{"(.*?)}')
        
    pattern = '{"(.*?)},{'
    for entry in matches:
        plugintools.log("entry="+entry)
        title = plugintools.find_single_match(entry,'name":"(.*?)"')
        title = title.replace("\u00e9" , "é")
        title = title.replace("\u00e8" , "è")
        title = title.replace("\u00ea" , "ê")
        title = title.replace("\u00e0" , "à")
        plugintools.log("title= "+title)
        id_playlist = plugintools.find_single_match(entry,'id":"(.*?)",')
        if id_playlist:
            plugintools.log("id_playlist= "+id_playlist)
            return id_playlist

        

def dailym_getvideo(url):
    plugintools.log("PLD.VisionTV.dailymotion_videos "+url)

    # Fetch video list from Dailymotion feed
    data = plugintools.read(url)
    #plugintools.log("data= "+data)
    
    # Extract items from feed
    pattern = ""
    matches = plugintools.find_multiple_matches(data,'{"(.*?)}')

    pattern = '{"(.*?)},{'
    for entry in matches:
        plugintools.log("entry= "+entry)
        
        # Not the better way to parse XML, but clean and easy
        title = plugintools.find_single_match(entry,'title":"(.*?)"')
        title = title.replace("\u00e9" , "é")
        title = title.replace("\u00e8" , "è")
        title = title.replace("\u00ea" , "ê")
        title = title.replace("\u00e0" , "à")
        video_id = plugintools.find_single_match(entry,'id":"(.*?)",')
        if video_id:
            plugintools.log("video_id= "+video_id)
            return video_id

def dailym_pl(params):
    plugintools.log("dailym_pl "+repr(params))

    pl = params.get("url")
    data = plugintools.read(pl)
    plugintools.log("playlist= "+data)

    dailym_vid = plugintools.find_multiple_matches(data, '{(.*?)}')
    
    for entry in dailym_vid:
        plugintools.log("entry= "+entry)
        title = plugintools.find_single_match(entry, '"title":"(.*?)",')
        title = title.replace('"', "")
        title = title.replace('\*', "")        
        video_id = plugintools.find_single_match(entry, '"id":"(.*?)",')
        thumbnail = "https://api.dailymotion.com/thumbnail/video/"+video_id+""
        if thumbnail == "":
            thumbnail = 'http://image-parcours.copainsdavant.com/image/750/1925508253/4094834.jpg'        
        url = "plugin://plugin.video.dailymotion_com/?url="+video_id+"&mode=playVideo"
        print 'url',url
        plugintools.add_item(action="play", title=title, url=url, folder = False, fanart='http://image-parcours.copainsdavant.com/image/750/1925508253/4094834.jpg',thumbnail=thumbnail,isPlayable = True)
            
