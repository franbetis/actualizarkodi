# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Analizador de URLs tipo plugin:// para PLD.VisionTV
# Version 0.1 (05.05.2014)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
#------------------------------------------------------------


import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin
import plugintools
import urllib2
import HTMLParser
import urllib,urlparse

from BeautifulSoup import BeautifulSoup as bs
import json

from __main__ import *

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")

def plugin_analyzer(data, title, plot, datamovie, thumbnail, fanart, show):
    plugintools.log("[%s %s] Analizando plugin... %s " % (addonName, addonVersion, data))
    
    if data.startswith("plugin://plugin.video.SportsDevil/") == True:
        url = data.strip()                         
        plugintools.runAddon( action = "runPlugin" , title = '[COLOR white]' + title + '[COLOR orange] [SportsDevil][/COLOR]', plot = plot , url = data.strip() , info_labels = datamovie, thumbnail = thumbnail , show = show, fanart = fanart, folder = False, isPlayable = False)

    elif data.startswith("plugin://plugin.video.f4mTester") == True:
        plugintools.add_item( action = "runPlugin" , title = '[COLOR white]' + title + '[COLOR orange] [F4M][/COLOR]', plot = plot , url = data.strip() , info_labels = datamovie, thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                    
    elif data.startswith("plugin://plugin.video.youtube") == True:
        if data.startswith("plugin://plugin.video.youtube/channel/") == True:
            plugintools.add_item( action = "runPlugin" , title = '[COLOR white] ' + title + '[COLOR white] [You[COLOR red]Tube[/COLOR][COLOR white] Channel][/COLOR]', url = data.strip() , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart , show = show, folder = True , isPlayable = False )
        elif data.startswith("plugin://plugin.video.youtube/play/?playlist_id") == True:
            plugintools.add_item( action = "runPlugin" , title = '[COLOR white] ' + title + '[COLOR white] [You[COLOR red]Tube[/COLOR][COLOR white] Playlist][/COLOR]', url = data.strip() , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart , show = show, folder = True , isPlayable = False )
        else:
            plugintools.add_item( action = "runPlugin" , title = '[COLOR white] ' + title + '[COLOR white] [You[COLOR red]Tube[/COLOR][COLOR white] Video][/COLOR]', url = data.strip() , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart , show = show, folder = False , isPlayable = True )
       
    elif data.find("plugin.video.p2p-streams") == True:                        
        if data.find("mode=1") >= 0 :  # Acestream
            plugintools.add_item( action = "runPlugin" , title = '[COLOR white]' + title + '[COLOR lightblue] [Acestream][/COLOR]' , plot = plot , url = data.strip() , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart , show = show, folder = False , isPlayable = True )
                        
        elif data.find("mode=2") >= 0 :  # Sopcast
            plugintools.add_item( action = "runPlugin" , title = '[COLOR white]' + title + '[COLOR darkorange] [Sopcast][/COLOR]' , plot = plot , url = data.strip() , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart , show = show, folder = False , isPlayable = True )

        elif data.find("mode=401") >= 0 :  # P2P-Streams Parser
            plugintools.add_item( action = "runPlugin" , title = '[COLOR white]' + title + '[COLOR darkorange] [p2p-streams][/COLOR]' , plot = plot , url = data.strip() , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart , show = show, folder = True , isPlayable = False )            

    elif data.startswith("plugin://plugin.video.p2psport") == True:
        plugintools.add_item( action = "runPlugin" , title = '[COLOR white]' + title + '[COLOR gold] [P2P Sport][/COLOR]', url = data.strip() , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart , show = show, folder = True , isPlayable = False )

    elif data.startswith("plugin://plugin.video.live.streamspro") == True:
        plugintools.add_item( action = "runPlugin" , title = '[COLOR white]' + title + '[COLOR gold] [LiveStreams][/COLOR]', url = data.strip() , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart , show = show, folder = False , isPlayable = False )

    elif data.startswith("plugin://plugin.video.stalker") == True:
        plugintools.add_item( action = "runPlugin" , title = '[COLOR white]' + title + '[COLOR gold] [Stalker][/COLOR]', url = data.strip() , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart , show = show, folder = False , isPlayable = False )        
        
    else:
        plugintools.add_item( action = "runPlugin" , title = '[COLOR white]' + title + '[COLOR darkorange] [Addon][/COLOR]' , plot = datamovie["Plot"] , url = data.strip() , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart , show = show, folder = True , isPlayable = False )
      



