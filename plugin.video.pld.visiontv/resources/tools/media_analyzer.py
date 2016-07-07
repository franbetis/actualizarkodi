# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Librería de herramientas de análisis de URLs para PLD.VisionTV
# Version 0.1
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
            plugintools.add_item( action = "runPlugin" , title = '[COLOR white]' + title + '[COLOR white] [You[COLOR red]Tube[/COLOR][COLOR white] Channel][/COLOR]', url = data.strip() , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart , show = show, folder = True , isPlayable = False )
        elif data.startswith("plugin://plugin.video.youtube/play/?playlist_id") == True:
            plugintools.add_item( action = "runPlugin" , title = '[COLOR white]' + title + '[COLOR white] [You[COLOR red]Tube[/COLOR][COLOR white] Playlist][/COLOR]', url = data.strip() , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart , show = show, folder = True , isPlayable = False )
        else:
            plugintools.runAddon( action = "play" , title = '[COLOR white]' + title + '[COLOR white] [You[COLOR red]Tube[/COLOR][COLOR white] Video][/COLOR]', url = data.strip() , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart , show = show, folder = False , isPlayable = True )
       
    elif data.find("plugin.video.p2p-streams") == True:                        
        if data.find("mode=1") >= 0 :  # Acestream
            plugintools.add_item( action = "runPlugin" , title = '[COLOR white]' + title + '[COLOR lightblue] [Acestream][/COLOR]' , plot = plot , url = data.strip() , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart , show = show, folder = False , isPlayable = True )
                        
        elif data.find("mode=2") >= 0 :  # Sopcast
            plugintools.add_item( action = "runPlugin" , title = '[COLOR white]' + title + '[COLOR darkorange] [Sopcast][/COLOR]' , plot = plot , url = data.strip() , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart , show = show, folder = False , isPlayable = True )

        elif data.find("mode=401") >= 0 :  # P2P-Streams Parser
            plugintools.add_item( action = "runPlugin" , title = '[COLOR white]' + title + '[COLOR darkorange] [p2p-streams][/COLOR]' , plot = plot , url = data.strip() , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart , show = show, folder = True , isPlayable = False )            

    elif data.startswith("plugin://plugin.video.p2psport") == True:
        plugintools.runAddon( action = "runPlugin" , title = '[COLOR white]' + title + '[COLOR gold] [P2P Sport][/COLOR]', url = data.strip() , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart , show = show, folder = False , isPlayable = False )

    elif data.startswith("plugin://plugin.video.live.streamspro") == True:
        if data.strip().endswith("xml") == True:
            plugintools.add_item( action = "runPlugin" , title = '[COLOR white]' + title + '[COLOR gold] [LiveStreams][/COLOR]', url = data.strip() , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart , show = show, folder = True , isPlayable = False )
        else:
            plugintools.runAddon( action = "runPlugin" , title = '[COLOR white]' + title + '[COLOR gold] [LiveStreams][/COLOR]', url = data.strip() , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart , show = show, folder = False , isPlayable = False )

    elif data.startswith("plugin://plugin.video.stalker") == True:
        plugintools.add_item( action = "runPlugin" , title = '[COLOR white]' + title + '[COLOR gold] [Stalker][/COLOR]', url = data.strip() , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart , show = show, folder = False , isPlayable = False )

    elif data.startswith("plugin://plugin.video.dailymotion_com") == True:  # Dailymotion (2.1.5)
        plugintools.runAddon( action = "play" , title = '[COLOR white]' + title + '[COLOR lightblue] [Dailymotion Video][/COLOR]', url = data , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart , show = show, folder = False , isPlayable = False )          
        
    else:
        plugintools.add_item( action = "runPlugin" , title = '[COLOR white]' + title + '[COLOR darkorange] [Addon][/COLOR]' , plot = datamovie["Plot"] , url = data.strip() , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart , show = show, folder = False , isPlayable = True )
      

def p2p_builder_url(url, title_fixed, p2p):

    if p2p == "ace":
        p2p_launcher = plugintools.get_setting("p2p_launcher")
        plugintools.log("p2p_launcher= "+p2p_launcher)        
        if p2p_launcher == "0":
            url = 'plugin://program.plexus/?url='+url+'&mode=1&name='+title_fixed
        else:
            url = 'plugin://plugin.video.p2p-streams/?url='+url+'&mode=1&name='+title_fixed

    elif p2p == "sop":
        p2p_launcher = plugintools.get_setting("p2p_launcher")
        plugintools.log("p2p_launcher= "+p2p_launcher)
        if p2p_launcher == "0":
            url = 'plugin://program.plexus/?url='+url+'&mode=2&name='+title_fixed
        else:
            url = 'plugin://plugin.video.p2p-streams/?url='+url+'&mode=2&name='+title_fixed

    elif p2p == "torrent":
        url = urllib.quote_plus(url)
        addon_torrent = plugintools.get_setting("addon_torrent")
        if addon_torrent == "Stream":  # Stream (por defecto)
            url = 'plugin://plugin.video.stream/play/'+url
        elif addon_torrent == "Pulsar":  # Pulsar
            url = 'plugin://plugin.video.pulsar/play?uri=' + url        

    elif p2p == "magnet":
        addon_magnet = plugintools.get_setting("addon_magnet")
        if addon_magnet == "0":  # Stream (por defecto)
            url = 'plugin://plugin.video.stream/play/'+url
        elif addon_magnet == "1":  # Pulsar
            url = 'plugin://plugin.video.pulsar/play?uri=' + url
        elif addon_magnet == "2":  # Kmediatorrent
            url = 'plugin://plugin.video.kmediatorrent/play/'+url

    plugintools.log("[%s %s] Creando llamada para URL P2P... %s " % (addonName, addonVersion, url))
    return url


def video_analyzer(url):
    plugintools.log("[%s %s] Análisis de URL de vídeo... " % (addonName, addonVersion))

    if url.find("allmyvideos") >=0:
        server = "allmyvideos"
    elif url.find("vidspot") >= 0:
        server = "vidspot"
    elif url.find("played.to") >= 0:
        server = "playedto"
    elif url.find("streamin.to") >= 0:
        server = "streaminto"
    elif url.find("streamcloud") >= 0:
        server = "streamcloud"
    elif url.find("nowvideo") >= 0:
        server = "nowvideo"
    elif url.find("veehd") >= 0:
        server = "veehd"
    elif url.find("vk") >= 0:
        server = "vk"
    elif url.find("tumi") >= 0:
        server = "tumi"
    elif url.find("novamov") >= 0:
        server = "novamov"
    elif url.find("moevideos") >= 0:
        server = "moevideos"
    elif url.find("gamovideo") >= 0:
        server = "gamovideo"
    elif url.find("movshare") >= 0:
        server = "movshare"
    elif url.find("powvideo") >= 0:
        server = "powvideo"
    elif url.find("mail.ru") >= 0:
        server = "mailru"
    elif url.find("netu") >= 0:
        server = "netu"
    elif url.find("movshare") >= 0:
        server = "movshare"
    elif url.find("movreel") >= 0:
        server = "movreel"
    elif url.find("videobam") >= 0:
        server = "videobam"
    elif url.find("videoweed") >= 0:
        server = "videoweed"
    elif url.find("streamable") >= 0:
        server = "streamable"
    elif url.find("rocvideo") >= 0:
        server = "rocvideo"
    elif url.find("realvid") >= 0:
        server = "realvid"
    elif url.find("videomega") >= 0:
        server = "videomega"
    elif url.find("video.tt") >= 0:
        server = "videott"
    elif url.find("flashx.tv") >= 0:
        server = "flashx"
    elif url.find("waaw.tv") >= 0:
        server = "waaw"
    else: server = 'unknown'

    return server
    


    



