# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------------------------------------------------------
# pld.visiontv / Kodi Add-on by Juarrox (juarrox@gmail.com)
# Version 0.3.3 (30.10.2015)
#-----------------------------------------------------------------------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
#-----------------------------------------------------------------------------------------------------------------------------
# Gracias a las librerías plugintools, scrapertools de Jesús (www.mimediacenter.info)
# pld.visiontv utiliza los scripts: t0mm0.common, beautifulsoup, requests, youtube.dl, common.plugin.cache, m3u8 y dateutil.
# Se recomienda instalar Plexus o p2p-streams, Pulsar, Youtube, Dailymotion para mejorar la experiencia de uso de este addon.
#-----------------------------------------------------------------------------------------------------------------------------
# Este addon no sería posible sin la ayuda y ánimo de mis amigos: 
# Reig, DMO, Quequino, DaniC, Aquilesserr, V1k1ng0, Teseo, MadQuark, Alegre, Sebas, Harold, y Paco. ¡Gracias!
#-----------------------------------------------------------------------------------------------------------------------------

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

import plugintools, ioncube, scrapertools, unwise, locale
import time, random

__home__ = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.pld.visiontv/', ''))
__temp__ = xbmc.translatePath(os.path.join('special://home/userdata/playlists/tmp', ''))
__playlists__ = xbmc.translatePath(os.path.join('special://home/userdata/playlists', ''))
__art__ = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.pld.visiontv/art', ''))
__cbx_pages__ = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.pld.visiontv/art/cbx', ''))
__icons__ = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.pld.visiontv/art/icons', ''))
__libdir__ = xbmc.translatePath(os.path.join('special://xbmc/system/players/dvdplayer/', ''))
__tools__ = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.pld.visiontv/resources/tools', ''))
__addons__ = xbmc.translatePath(os.path.join('special://home/addons/', ''))
__resources__ = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.pld.visiontv/resources', ''))

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")

lOO=xbmcaddon.Addon().getAddonInfo('id');l0O='aHR0cDovL2NpcHJvbWFyaW8udy5wdy9weWMvaW5kZXgucGhw';
profile=xbmcaddon.Addon().getAddonInfo('profile').decode('utf-8')
cookiefile=profile+'cookies.dat'
for i in ('resources','pages','tools','playlists','cookies','art','tmp','profile'): sys.path.append(os.path.join(__xbmcaddonid__,i))



selfAddon = xbmcaddon.Addon()

icon = __art__ + 'icon.png'
fanart = 'fanart.jpg'

LIST = "list"
THUMBNAIL = "thumbnail"
MOVIES = "movies"
TV_SHOWS = "tvshows"
SEASONS = "seasons"
EPISODES = "episodes"
OTHER = "other"

# Regex de canales
from resources.regex.vaughnlive import *
from resources.regex.ninestream import *
from resources.regex.vercosas import *
from resources.regex.castalba import *
from resources.regex.castdos import *
from resources.regex.directwatch import *
from resources.regex.freetvcast import *
from resources.regex.freebroadcast import *
from resources.regex.sawlive import *
from resources.regex.broadcastlive import *
from resources.regex.businessapp import *
from resources.regex.rdmcast import *
from resources.regex.dinozap import *
from resources.regex.streamingfreetv import *
from resources.regex.byetv import *
from resources.regex.ezcast import *
from resources.regex.ucaster import *
from resources.regex.iguide import *
from resources.regex.miplayernet import *

# Regex de series
from resources.tools.seriesblanco import *
from resources.tools.seriesflv import *
from resources.tools.seriesadicto import *
from resources.tools.seriesyonkis import *
from resources.tools.seriesmu import *

# Regex de pelis
from resources.tools.oranline import *
from resources.tools.pordede import *
from resources.tools.pelisadicto import *

# Regex de vídeos
from resources.tools.dailymotion import *
from resources.tools.yt_playlist import *

# Herramientas y utilidades
from resources.tools.resolvers import *
from resources.tools.multilink import *
from resources.tools.epg_miguiatv import *
from resources.tools.epg_arenasport import *
from resources.tools.epg_formulatv import *
from resources.tools.epg_elmundo import * 
from resources.tools.epg_verahora import *
from resources.tools.epg_entutele import *
from resources.tools.getposter import *
from resources.tools.kickass import *
from resources.tools.goear import *
from resources.tools.moviedb import *
from resources.tools.mundoplus import *
from resources.tools.bers_sy import *
from resources.tools.server_rtmp import *
from resources.tools.txt_reader import *
from resources.tools.loadtxt_ftv import *
from resources.tools.epg_txt import *
from resources.tools.agendatv import *
from resources.tools.context import *
from resources.tools.media_analyzer import *
from resources.tools.fpa import *
from resources.tools.livesoccertv import *

ADDON=xbmcaddon.Addon(id='plugin.video.pld.visiontv')
INTRO = xbmc.translatePath(os.path.join('special://home/plugin.video.pld.visiontv/intro.mp4'))

def INTROS():            
    if ADDON.getSetting('intro') == "true":
        xbmcPlayer=xbmc.Player()
        xbmcPlayer.play(INTRO)
        xbmc.sleep(15)
        ADDON.setSetting('intro','false')
    #else:
       # pass
        if ADDON.getSetting('message') == "true":
            xbmc.sleep(150)
            intro=xbmcgui.Dialog()
            msg = intro.ok("[COLOR blue]http://Proyectoluzdigital.info[/COLOR]", "[COLOR orange]****************[COLOR red]-------NUEVO ADOONS------[COLOR orange]****************[/COLOR]",
                            "**********************[COLOR lime]PLD-VISIONTV[/COLOR]**********************",
                            "*************[COLOR orange]ESPERAMOS QUE LO DISFRUTEIS[/COLOR]*************"
                            )
            if msg == True:
                ADDON.setSetting('message','false')
            else:
                pass
        else:
            pass      
INTROS()


# Entry point
def run():
    plugintools.log('[%s %s] ---> pld.visiontv.run <--- ' % (addonName, addonVersion))
    
    plugintools.log("")
    plugintools.modo_vista("list")

    # Obteniendo parámetros...
    params = plugintools.get_params()
    
    if params.get("action") is None:
        main_list(params)
    else:
       action = params.get("action")
       url = params.get("url")
       exec action+"(params)"   
    
    if not os.path.exists(__playlists__) :
        os.makedirs(__playlists__)

    if not os.path.exists(__temp__) :
        os.makedirs(__temp__)

    plugintools.close_item_list()



# Main menu

def main_list(params):
    plugintools.log('[%s %s].main_list %s' % (addonName, addonVersion, repr(params)))

    # Control del skin de pld.visiontv
    mastermenu = xml_skin()
    plugintools.log("XML menu: "+mastermenu)
    try:
        data = plugintools.read(mastermenu)
    except:
        mastermenu = 'http://pastebin.com/raw.php?i=ydUjKXnN'
        data = plugintools.read(mastermenu)
        xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('pld.visiontv', "XML no reconocido...", 3 , __art__+'icon.png'))

    matches = plugintools.find_multiple_matches(data,'<menu_info>(.*?)</menu_info>')
    for entry in matches:
        title = plugintools.find_single_match(entry,'<title>(.*?)</title>')
        date = plugintools.find_single_match(entry,'<date>(.*?)</date>')
        thumbnail = plugintools.find_single_match(entry,'<thumbnail>(.*?)</thumbnail>')
        fanart = plugintools.find_single_match(entry,'<fanart>(.*?)</fanart>')
        plugintools.add_item( action="" , title = title + date , fanart = fanart , thumbnail=thumbnail , folder = False , isPlayable = False )

    data = plugintools.read(mastermenu)
    matches = plugintools.find_multiple_matches(data,'<channel>(.*?)</channel>')
    for entry in matches:
        title = plugintools.find_single_match(entry,'<name>(.*?)</name>')
        thumbnail = plugintools.find_single_match(entry,'<thumbnail>(.*?)</thumbnail>')
        fanart = plugintools.find_single_match(entry,'<fanart>(.*?)</fanart>')
        action = plugintools.find_single_match(entry,'<action>(.*?)</action>')
        last_update = plugintools.find_single_match(entry,'<last_update>(.*?)</last_update>')
        url = plugintools.find_single_match(entry,'<url>(.*?)</url>')
        date = plugintools.find_single_match(entry,'<last_update>(.*?)</last_update>')

        # Control paternal
        pekes_no = plugintools.get_setting("pekes_no")
        if pekes_no == "true" :
            print "Control paternal en marcha"
            if title.find("Adultos") >= 0 :
                plugintools.log("Activando control paternal...")
            else:
                fixed = title
                plugintools.log("fixed= "+fixed)
                if fixed == "Actualizaciones":
                    plugintools.add_item( action = action , plot = fixed , title = '[COLOR lightblue]' + fixed + '[/COLOR]' , fanart = fanart , thumbnail = thumbnail , url = url , folder = True , isPlayable = False )
                elif fixed == 'Agenda TV':
                    plugintools.add_item( action = action , plot = fixed , title = '[COLOR lightblue]' + fixed + '[/COLOR]' , fanart = fanart , thumbnail = thumbnail , url = url , folder = True , isPlayable = False )
                elif fixed == 'Configuración':
                    plugintools.add_item( action = action , plot = fixed , title = '[COLOR lightblue]' + fixed + '[/COLOR]' , fanart = fanart , thumbnail = thumbnail , url = url , folder = False , isPlayable = False )                    
                else:
                    plugintools.add_item( action = action , plot = fixed , title = '[COLOR white]' + fixed + '[/COLOR]' , fanart = fanart , thumbnail = thumbnail , url = url , folder = True , isPlayable = False )
        else:
            fixed = title
            if fixed == "Actualizaciones":
                plugintools.add_item( action = action , plot = fixed , title = '[COLOR lightblue]' + fixed + '[/COLOR]' , fanart = fanart , thumbnail = thumbnail , url = url , folder = True , isPlayable = False )
            elif fixed == "Agenda TV":
                plugintools.add_item( action = action , plot = fixed , title = '[COLOR lightblue]' + fixed + '[/COLOR]' , fanart = fanart , thumbnail = thumbnail , url = url , folder = True , isPlayable = False )
            else:
                plugintools.add_item( action = action , plot = fixed , title = '[COLOR white]' + fixed + '[/COLOR]' , fanart = fanart , thumbnail = thumbnail , url = url , folder = True , isPlayable = False )



def play(params):
    plugintools.log('[%s %s].play %s' % (addonName, addonVersion, repr(params)))
    show = params.get("show")  # Control de modo de vista predefinido
    if show == "":
        show = params.get("extra")
        if show == "":
            show = "list"

    plugintools.modo_vista(show)
    url = params.get("url")
    plugintools.play_resolved_url(url)
    plugintools.modo_vista(show)


def runPlugin(params):
    plugintools.log('[%s %s] runPlugin %s' % (addonName, addonVersion, repr(params)))
    
    url = params.get("url")
    if url.startswith("plugin://plugin.video.live.streamspro/") == True:        
        builtin = 'Container.Update(%s)' %url
        xbmc.executebuiltin(builtin)      
    elif url.startswith("plugin://plugin") == False:
        item = xbmcgui.ListItem(path=url)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
    elif url.startswith("plugin://plugin.video.youtube") == True:
        xbmc.executebuiltin('XBMC.RunPlugin('+url+')')      
    else:
        print 'Not setting setResolvedUrl'
        builtin = 'RunPlugin(%s)' %url
        xbmc.executebuiltin(builtin)   


def live_items_withlink(params):
    plugintools.log('[%s %s].live_items_withlink %s' % (addonName, addonVersion, repr(params)))
    data = plugintools.read(params.get("url"))

    # ToDo: Agregar función lectura de cabecera (fanart, thumbnail, título, últ. actualización)
    header_xml(params)

    fanart = plugintools.find_single_match(data, '<fanart>(.*?)</fanart>')  # Localizamos fanart de la lista
    if fanart == "":
        fanart = __art__ + 'fanart.jpg'

    author = plugintools.find_single_match(data, '<poster>(.*?)</poster>')  # Localizamos autor de la lista (encabezado)

    matches = plugintools.find_multiple_matches(data,'<item>(.*?)</item>')
    for entry in matches:
        title = plugintools.find_single_match(entry,'<title>(.*?)</title>')
        title = title.replace("<![CDATA[", "")
        title = title.replace("]]>", "")
        thumbnail = plugintools.find_single_match(entry,'<thumbnail>(.*?)</thumbnail>')
        url = plugintools.find_single_match(entry,'<link>(.*?)</link>')
        url = url.replace("<![CDATA[", "")
        url = url.replace("]]>", "")
        plugintools.add_item(action = "play" , title = title , url = url , fanart = fanart , thumbnail = thumbnail , folder = False , isPlayable = True )



def xml_lists(params):
    plugintools.log('[%s %s].xml_lists %s' % (addonName, addonVersion, repr(params)))
    data = plugintools.read( params.get("url") )
    name_channel = params.get("title")
    name_channel = parser_title(name_channel)
    plugintools.log("name_channel= "+name_channel)
    data = plugintools.find_single_match(data, '<name>'+name_channel+'(.*?)</channel>')
    print data
    plugintools.add_item(action="" , title='[B][COLOR yellow]'+name_channel+'[/B][/COLOR]' , thumbnail= 'icon.png' , fanart = 'fanart.jpg' , folder = False , isPlayable = False )

    # Control paternal
    pekes_no = plugintools.get_setting("pekes_no")

    subchannel = re.compile('<subchannel>([^<]+)<name>([^<]+)</name>([^<]+)<thumbnail>([^<]+)</thumbnail>([^<]+)<fanart>([^<]+)</fanart>([^<]+)<action>([^<]+)</action>([^<]+)<url>([^<]+)</url>([^<]+)</subchannel>').findall(data)
    for biny, ciny, diny, winy, pixy, dixy, boxy, susy, lexy, muny, kiny in subchannel:
        if pekes_no == "true" :
            print "Control paternal en marcha"
            if ciny.find("XXX") >= 0 :
                plugintools.log("Activando control paternal...")
            else:
                plugintools.add_item( action = susy , title = ciny , url= muny , thumbnail = winy , fanart = dixy , extra = dixy , page = dixy , folder = True , isPlayable = False )
                params["fanart"]=dixy                

        else:
            plugintools.add_item( action = susy , title = ciny , url= muny , thumbnail = winy , fanart = dixy , extra = dixy , page = dixy , folder = True , isPlayable = False )
            params["fanart"]=dixy
            

def getstreams_now(params):
    plugintools.log('[%s %s].getstreams_now %s' % (addonName, addonVersion, repr(params)))

    data = plugintools.read( params.get("url") )
    poster = plugintools.find_single_match(data, '<poster>(.*?)</poster>')
    plugintools.add_item(action="" , title='[COLOR blue][B]'+poster+'[/B][/COLOR]', url="", folder =False, isPlayable=False)
    matches = plugintools.find_multiple_matches(data,'<title>(.*?)</link>')

    for entry in matches:
        title = plugintools.find_single_match(entry,'(.*?)</title>')
        url = plugintools.find_single_match(entry,'<link> ([^<]+)')
        plugintools.add_item( action="play" , title=title , url=url , folder = False , isPlayable = True )



# Soporte de listas de canales por categorías (Livestreams, XBMC México, Motor SportsTV, etc.).

def livestreams_channels(params):
    plugintools.log('[%s %s].livestreams_channels %s' % (addonName, addonVersion, repr(params)))
    data = plugintools.read( params.get("url") )

    # Extract directory list
    thumbnail = params.get("thumbnail")

    if thumbnail == "":
        thumbnail = 'icon.jpg'
        plugintools.log(thumbnail)
    else:
        plugintools.log(thumbnail)

    if thumbnail == __art__ + 'icon.png':
        matches = plugintools.find_multiple_matches(data,'<channel>(.*?)</items>')
        for entry in matches:
            title = plugintools.find_single_match(entry,'<name>(.*?)</name>')
            thumbnail = plugintools.find_single_match(entry,'<thumbnail>(.*?)</thumbnail>')
            fanart = plugintools.find_single_match(entry,'<fanart>(.*?)</fanart>')
            plugintools.add_item( action="livestreams_subchannels" , title=title , url=params.get("url") , thumbnail=thumbnail , fanart=fanart , folder = True , isPlayable = False )

    else:
        matches = plugintools.find_multiple_matches(data,'<channel>(.*?)</items>')
        for entry in matches:
            title = plugintools.find_single_match(entry,'<name>(.*?)</name>')
            thumbnail = plugintools.find_single_match(entry,'<thumbnail>(.*?)</thumbnail>')
            fanart = plugintools.find_single_match(entry,'<fanart>(.*?)</fanart>')
            plugintools.add_item( action="livestreams_items" , title=title , url=params.get("url") , fanart=fanart , thumbnail=thumbnail , folder = True , isPlayable = False )


def livestreams_subchannels(params):
    plugintools.log('[%s %s].livestreams_subchannels %s' % (addonName, addonVersion, repr(params)))

    data = plugintools.read( params.get("url") )
    # title_channel = params.get("title")
    title_channel = params.get("title")
    name_subchannel = '<name>'+title_channel+'</name>'
    data = plugintools.find_single_match(data, name_subchannel+'(.*?)</channel>')
    info = plugintools.find_single_match(data, '<info>(.*?)</info>')
    title = params.get("title")
    plugintools.add_item( action="" , title='[B]'+title+'[/B] [COLOR yellow]'+info+'[/COLOR]' , folder = False , isPlayable = False )

    subchannel = plugintools.find_multiple_matches(data , '<name>(.*?)</name>')
    for entry in subchannel:
        plugintools.add_item( action="livestreams_subitems" , title=entry , url=params.get("url") , thumbnail=__art__+'motorsports-xbmc.jpg' , folder = True , isPlayable = False )


# Pendiente de cargar thumbnail personalizado y fanart...
def livestreams_subitems(params):
    plugintools.log('[%s %s].livestreams_subitems %s' % (addonName, addonVersion, repr(params)))

    title_subchannel = params.get("title")
    data = plugintools.read( params.get("url") )
    source = plugintools.find_single_match(data , title_subchannel+'(.*?)<subchannel>')

    titles = re.compile('<title>([^<]+)</title>([^<]+)<link>([^<]+)</link>').findall(source)
    url = params.get("url")
    title = params.get("title")
    thumbnail = params.get("thumbnail")

    for entry, quirry, winy in titles:
        winy = winy.replace("amp;","")
        plugintools.add_item( action="play" , title = entry , url = winy , thumbnail = thumbnail , folder = False , isPlayable = True )


def livestreams_items(params):
    plugintools.log('[%s %s].livestreams_items %s' % (addonName, addonVersion, repr(params)))

    title_subchannel = params.get("title")
    plugintools.log("title= "+title_subchannel)
    title_subchannel_fixed = title_subchannel.replace("Ã±", "ñ")
    title_subchannel_fixed = title_subchannel_fixed.replace("\\xc3\\xb1", "ñ")
    title_subchannel_fixed = plugintools.find_single_match(title_subchannel_fixed, '([^[]+)')
    title_subchannel_fixed = title_subchannel_fixed.encode('utf-8', 'ignore')
    plugintools.log("subcanal= "+title_subchannel_fixed)
    if title_subchannel_fixed.find("+") >= 0:
        title_subchannel_fixed = title_subchannel_fixed.split("+")
        title_subchannel_fixed = title_subchannel_fixed[1]
        title_subchannel_fixxed = title_subchannel_fixed[0]
        if title_subchannel_fixed == "":
            title_subchannel_fixed = title_subchannel_fixxed

    data = plugintools.read( params.get("url") )
    source = plugintools.find_single_match(data , title_subchannel_fixed+'(.*?)</channel>')
    plugintools.log("source= "+source)
    fanart_channel = plugintools.find_single_match(source, '<fanart>(.*?)</fanart>')
    titles = re.compile('<title>([^<]+)</title>([^<]+)<link>([^<]+)</link>([^<]+)<thumbnail>([^<]+)</thumbnail>').findall(source)

    url = params.get("url")
    title = params.get("title")
    thumbnail = params.get("thumbnail")

    for entry, quirry, winy, xiry, miry in titles:
        plugintools.log("title= "+entry)
        plugintools.log("url= "+winy)
        winy = winy.replace("amp;","")
        plugintools.add_item( action="play" , title = entry , url = winy , thumbnail = miry , fanart = fanart_channel , folder = False , isPlayable = True )


def xml_items(params):
    plugintools.log('[%s %s].xml_items %s' % (addonName, addonVersion, repr(params)))
    data = plugintools.read( params.get("url") )
    thumbnail = params.get("thumbnail")

    #Todo: Implementar una variable que permita seleccionar qué tipo de parseo hacer
    if thumbnail == "title_link.png":
        matches = plugintools.find_multiple_matches(data,'<item>(.*?)</item>')
        for entry in matches:
            title = plugintools.find_single_match(entry,'<title>(.*?)</title>')
            thumbnail = plugintools.find_single_match(entry,'<thumbnail>(.*?)</thumbnail>')
            url = plugintools.find_single_match(entry,'<link>([^<]+)</link>')
            fanart = plugintools.find_single_match(entry,'<fanart>([^<]+)</fanart>')
            plugintools.add_item( action = "play" , title = title , url = url , thumbnail = thumbnail , fanart = fanart , plot = title , folder = False , isPlayable = True )

    if thumbnail == "name_rtmp.png":
        matches = plugintools.find_multiple_matches(data,'<channel>(.*?)</channel>')
        for entry in matches:
            title = plugintools.find_single_match(entry,'<name>(.*?)</name>')
            url = plugintools.find_single_match(entry,'<rtmp>([^<]+)</rtmp>')
            plugintools.add_item( action = "play" , title = title , url = url , fanart = __art__ + 'fanart.jpg' , plot = title , folder = False , isPlayable = True )


def simpletv_items(params):
    plugintools.log('[%s %s].simpletv_items %s' % (addonName, addonVersion, repr(params)))

    saving_url = 0  # Interruptor para scraper de pelis
    datamovie = {}  # Creamos lista de datos película
    filtros_on = plugintools.get_setting("fpa_on")  # Filtros activos?
    
    logo = ""; background = ""

    show = "list"
    params["show"]=show
    
    # Obtenemos fanart y thumbnail del diccionario
    thumbnail = params.get("thumbnail")
    if thumbnail == "" :
        thumbnail = __art__ + 'icon.png'

    # Parche para solucionar un bug por el cuál el diccionario params no retorna la variable fanart
    fanart = params.get("extra")
    if fanart == " " :
        fanart = params.get("fanart")
        if fanart == " " :
            fanart = __art__ + 'fanart.png'
        
    title = params.get("plot")
    texto= params.get("texto")
    busqueda = ""
    if title == 'search':
        title = title + '.txt'
        plugintools.log("title= "+title)
    else:
        title = title + '.m3u'

    if title == 'search.txt':
        busqueda = 'search.txt'
        filename = title
        file = open(__temp__ + 'search.txt', "r")
        file.seek(0)
        data = file.readline()
        if data == "":
            ok = plugintools.message("pld.visiontv", "Sin resultados")
            return ok
    else:
        title = params.get("title")
        title = parser_title(title)
        ext = params.get("ext")
        title_plot = params.get("plot")
        if title_plot == "":
            filename = title + "." + ext

        if ext is None:
            filename = title
        else:
            plugintools.log("ext= "+ext)
            filename = title + "." + ext
            
        file = open(__playlists__ + filename, "r")
        file.seek(0)
        v = file.readlines();print v
        file.seek(0)
        data = file.readline().strip()
        
        if data.find("#EXTM3U") >= 0:  # Control modo de vista
            if "no_follow" in data:
                follower = 1
            data = data.split(",")
            print '#EXTM3U items',data
            for item in data:
                if item.startswith("view") == True:
                    show = item.replace("view:", "")
                    plugintools.modo_vista(show)
                if "background" in item:
                    background = item.replace("background=", "").replace('"',"").strip()
                    plugintools.log("background= "+background)
                    if background != "": fanart = background
                if "logo" in item:
                    logo = item.replace("logo=", "").replace('"',"").strip()
                    plugintools.log("logo= "+logo)
                    if logo != "": thumbnail = logo
            
    if data == "":
        print "No es posible leer el archivo!"
        data = file.readline()
        plugintools.log("data= "+data)
    else:
        file.seek(0)
        num_items = len(file.readlines())
        print num_items
        plugintools.log("filename= "+filename)
        plugintools.add_item(action="" , title = '[COLOR lightyellow][B][I]playlists / '+ filename + '[/B][/I][/COLOR]' , url = __playlists__ + title , fanart = fanart , thumbnail = thumbnail , folder = False , isPlayable = False)
            
    cat = ""  # Control para evitar error en búsquedas (cat is null)   
    plot = " "   # Control canal sin EPG (plot is null)
    file.seek(0)
    data = file.readline()
    i = -1
    while i <= num_items:
        if data.startswith("#EXTINF:-1") == True:
            title = data.replace("#EXTINF:-1", "")
            title = title.replace(",", "")
            title = title.replace("-AZBOX *", "")
            title = title.replace("-AZBOX-*", "")
            title = title.replace("tvg-shift=0", "").replace("tvg-shift=-5", "").strip()            
            if title.startswith("$") == True:  # Control para lanzar scraper IMDB
                title = title.replace("$","")
                images = m3u_items(title)
                #plugintools.modo_vista(show)  # Para no perder el modo de vista predefinido tras llamar a la función m3u_items
                title_fixed = images[3]
                datamovie = {}
                datamovie = getposter(title_fixed)
                save_title(title_fixed, datamovie, filename)
                getdatafilm = 1  # Control para cargar datos de película
                saving_url = 1  # Control para guardar URL
                if datamovie == {}:
                    title = '[COLOR lightyellow][B]'+title+' - [/B][I][COLOR orange][IMDB: [B]'+datamovie["Rating"]+'[/B]][/I][/COLOR] '
                    thumbnail = datamovie["Poster"];fanart = datamovie["Fanart"]

            # Control de la línea del título en caso de búsqueda 
            if busqueda == 'search.txt':
                title_search = title.split('"')
                print 'title',title
                titulo = title_search[0]
                titulo = titulo.strip()
                origen = title_search[1]
                origen = origen.strip()
                data = file.readline()
                i = i + 1      
            else:
                images = m3u_items(title)
                print 'images',images
                #plugintools.modo_vista(show)  # Para no perder el modo de vista predefinido tras llamar a la función m3u_items
                thumbnail = images[0]
                fanart = images[1]
                cat = images[2]
                title = images[3]
                # Recopilamos datos de película en diccionario
                datamovie["Rating"] = images[6]  # Ranking IMDB
                datamovie["Duration"] = images[7]  # Duración
                datamovie["Year"] = images[8]  # Año
                datamovie["Director"] = images[9]  # Director
                datamovie["Writer"]=images[10]  # Escritor(es)
                datamovie["Genre"]=images[11]  # Géneros
                datamovie["Votes"]=images[12]  # Votos
                datamovie["Plot"]=images[13]  # Plot (sinopsis)
                total_cast=images[14]  # Cast
                total_cast=total_cast.split(", ")
                datamovie["Cast"]=total_cast
                origen = title.split(",")                
                title = title.strip()
                plugintools.log("title= "+title)
                data = file.readline()
                i = i + 1

                # Control para thumbnail y fanart global (logo y background)
                if logo != "":  # Existe logo global
                    if thumbnail == __art__ + 'icon.png':
                        thumbnail = logo
                    else:
                        thumbnail = images[0]
                        
                if background != "":  # Existe background global
                    if fanart == __art__ + 'fanart.jpg':
                        fanart = background
                    else:
                        fanart = images[1]                

            if title.startswith("#") == True:  # Control para comentarios
                title = title.replace("#", "")
                plugintools.log("desc= "+data)                
                if data.startswith("desc") == True:
                    plot = data.replace("desc=", "").replace('"',"")
                    plugintools.add_item(action="", title = title , url = "", plot = datamovie["Plot"] , thumbnail = thumbnail , info_labels = datamovie, fanart = fanart , folder = False , isPlayable = False)
                else:                    
                    plugintools.add_item(action="", title = title , url = "", plot = datamovie["Plot"] , thumbnail = thumbnail , info_labels = datamovie, fanart = fanart , folder = False , isPlayable = False)
                data = file.readline()
                i = i + 1
                continue                

            if title.startswith("@") == True:  # Control para lanzar EPG
                if plugintools.get_setting("epg_no") == "true":
                    title = title.replace("@","")                    
                    plugintools.log('[%s %s] EPG desactivado ' % (addonName, addonVersion))
                    if show == "":
                        plugintools.get_setting("video_id")                                        
                else:
                    title = title.replace("@","")
                    if show == "":
                        plugintools.get_setting("video_id")
                    #plugintools.modo_vista(show)
                    epg_channel = []
                    epg_source = plugintools.get_setting("epg_source")
                    plugintools.log("Fuente EPG = "+epg_source)
                      
                    if epg_source == "0":  # MiguíaTV
                        epg_channel = epg_now(title)
                        print 'EPG:',epg_channel                            
                        try:
                            title = title + " [COLOR orange][I][B] " + epg_channel[0] + "[/B] " + epg_channel[1] + "[/I][/COLOR] "
                            plot = "[COLOR white][I]" + epg_channel[2].strip() + " " + epg_channel[3].strip() + "[CR]"+ epg_channel[4].strip() + " " + epg_channel[5].strip()+"[CR]"+ epg_channel[6].strip() + " " + epg_channel[7].strip()+"[CR]"+ epg_channel[8].strip() + " " + epg_channel[9].strip()+"[/I][/COLOR] "
                            datamovie["Plot"]=plot
                        except:
                            plot = ""
                            pass
                    else:  # FórmulaTV General | FTV Movistar+ | FTV Telecable | FTV Ono | FTV Jazztel
                        epg_channel = epg_ftv(title)
                        print 'EPG:',epg_channel
                        if epg_channel != False:
                            try:
                                ejemplo = epg_channel[0]
                                print epg_channel[0]
                                title = title + " [COLOR orange][I][B] " + epg_channel[0] + "[/B] " + epg_channel[1] + "[/I][/COLOR] "
                                plot = "[COLOR white]" + epg_channel[2].strip() + " " + epg_channel[4].strip() + " [/COLOR][COLOR lightyellow][I]("+epg_channel[3].strip() + ")[/I][/COLOR][CR]" + epg_channel[5].strip()+" "+ epg_channel[6].strip()
                                datamovie["Plot"]=plot
                            except:
                                plot = ""
                                pass                        
                    
            # Control para determinadas listas de decos sat
            if title.startswith(' $ExtFilter="') == True:
                if busqueda == 'search.txt':
                    title = title.replace('$ExtFilter="', "")
                    title_search = title.split('"')
                    titulo = title_search[1]
                    origen = title_search[2]
                    origen = origen.strip()
                    data = file.readline()
                    i = i + 1                    
                else:
                    title = title.replace('$ExtFilter="', "")
                    category = title.split('"')
                    tipo = category[0]
                    tipo = tipo.strip()
                    title = category[1]
                    title = title.strip()
                    print title
                    data = file.readline()
                    i = i + 1
                    
            if data != "":
                url = data.strip()
                
                if url == "#multilink":
                    # Control para info de canal o sinopsis de película
                    #data = file.readline()
                    plugintools.log("linea= "+data)
                    if data.startswith("desc") == True:                        
                        plot = data.replace("desc=", "").replace('"',"")
                        plugintools.log("sinopsis= "+data)
                    if cat == "":
                        plugintools.add_item( action = "multilink" , plot = plot , extra = filename , title = '[COLOR white]' + title + ' [COLOR lightyellow][Multilink][/COLOR]', url = url ,  thumbnail = thumbnail, info_labels = datamovie , show = show , page = show , fanart = fanart , folder = False , isPlayable = True )
                        if saving_url == 1:
                            plugintools.log("URL= "+url)
                            save_multilink(url, filename)
                            while url != "":
                                url = file.readline().strip()
                                plugintools.log("URL= "+url)
                                save_multilink(url, filename)
                                i = i + 1
                            saving_url = 0                            
                        plot = ""
                    else:  
                        plugintools.add_item( action = "multilink" , plot = plot , extra = filename , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + ' [COLOR purple][Multilink][/COLOR]' , url = url , info_labels = datamovie , thumbnail = thumbnail, show = show, page = show , fanart = fanart , folder = False , isPlayable = True )

                elif url == "#multiparser":                    
                    if data.startswith("desc") == True:                        
                        plot = data.replace("desc=", "").replace('"',"")
                        
                    if filtros_on == "true" and params.get("extra") == "1":
                        params["title"]=title
                        params["thumbnail"]=thumbnail
                        params["fanart"]=fanart
                        title = filtros0(params, datamovie);plugintools.modo_vista(show)
                        if title:
                            url = params.get("url")
                            genre = datamovie["Genre"];genre=genre.strip();genre=genre.replace("Ciencia ficción", "Ciencia-Ficción");genre=genre.replace(" ", ", ");print genre
                            datamovie["Plot"]='[B]'+datamovie["Year"]+'[/B][COLOR lightgreen][I] '+datamovie["Duration"]+'  [/I][/COLOR][COLOR white][B][COLOR lightyellow]'+datamovie["Rating"]+'[/B][/COLOR] [I]('+genre+')[/I] [B][COLOR lightyellow]Cast:[/B][/COLOR] '+images[14]+' [B][COLOR lightyellow]Dir:[/B][/COLOR] '+datamovie["Director"]+'[CR]'+datamovie["Plot"]
                            print datamovie
                            plugintools.addPeli( action = "multiparser" , plot = plot , extra = filename , title = '[COLOR white]' + title+'[/COLOR]', url = url ,  thumbnail = thumbnail, info_labels = datamovie , show = show , page = show , fanart = fanart , folder = True , isPlayable = False )

                    else:
                        # Control para info de canal o sinopsis de película
                        #data = file.readline()
                        plugintools.log("linea= "+data)
                        if data.startswith("desc") == True:                        
                            plot = data.replace("desc=", "").replace('"',"")
                            plugintools.log("sinopsis= "+data)
                        if cat == "":
                            plugintools.add_item( action = "multiparser" , plot = datamovie["Plot"] , extra = filename , title = '[COLOR white]' + title + ' [COLOR lightyellow][Multiparser][/COLOR]', url = url ,  thumbnail = thumbnail, info_labels = datamovie , show = show , page = show , fanart = fanart , folder = True , isPlayable = False )
                            if saving_url == 1:
                                save_multiparser(url, filename)
                                while url != "":
                                    url = file.readline().strip()
                                    save_multiparser(url, filename)
                                    i = i + 1
                                saving_url = 0                            
                            plot = ""
                        else:  
                            plugintools.add_item( action = "multiparser" , plot = datamovie["Plot"] , extra = filename , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + ' [COLOR purple][Multiparser][/COLOR]' , url = url , info_labels = datamovie , thumbnail = thumbnail, show = show, page = show, fanart = fanart , folder = True , isPlayable = False )

                elif url.startswith("img") == True:
                    url = data.strip()
                    plugintools.add_item( action = "show_image" , plot = datamovie["Plot"] , extra = filename , title = '[COLOR white] ' + title + ' [COLOR lightyellow][IMG][/COLOR]' , url = url , info_labels = datamovie , thumbnail = thumbnail, show = show, page = show, fanart = fanart , folder = False , isPlayable = False )
                    data = file.readline()
                    i = i + 1
                    continue                                       
                            
                elif url.startswith("serie") == True:
                    url = data.strip()
                    if cat == "":
                        if busqueda == 'search.txt':                            
                            url = url.replace("serie:", "")
                            params["fanart"] = fanart
                            if url.find("seriesadicto") >= 0:
                                plugintools.add_item( action = "seriecatcher" , title = '[COLOR white]' + title + ' [COLOR lightgreen][B][Series[/B]adicto][/COLOR][COLOR white][I] (' + origen + ')[/I][/COLOR]', url = url , thumbnail = thumbnail , show = show, fanart = fanart , folder = True , isPlayable = False )
                                data = file.readline()
                                i = i + 1
                                continue
                            elif url.find("seriesflv") >= 0:
                                plugintools.add_item( action = "lista_capis" , title = '[COLOR white]' + title + ' [COLOR lightgreen][B][Series[/B]FLV][/COLOR][COLOR white][I] (' + origen + ')[/I][/COLOR]', url = url , thumbnail = thumbnail , show = show, fanart = fanart , folder = True , isPlayable = False )
                                data = file.readline()
                                i = i + 1
                                continue
                            elif url.find("seriesyonkis") >= 0:
                                plugintools.add_item( action = "serie_capis" , title = '[COLOR white]' + title + ' [COLOR lightgreen][B][Series[/B]Yonkis][/COLOR][COLOR white][I] (' + origen + ')[/I][/COLOR]', url = url , thumbnail = thumbnail , show = show, fanart = fanart , folder = True , isPlayable = False )
                                data = file.readline()
                                i = i + 1
                                continue
                            elif url.find("seriesblanco") >= 0:
                                plugintools.add_item( action = "seriesblanco0" , title = '[COLOR white]' + title + ' [COLOR lightgreen][B][Series[/B]Blanco][/COLOR][COLOR white][I] (' + origen + ')[/I][/COLOR]', url = url , thumbnail = thumbnail , show = show, fanart = fanart , folder = True , isPlayable = False )
                                data = file.readline()
                                i = i + 1
                                continue
                            elif url.find("series.mu") >= 0:
                                plugintools.add_item( action = "seriesmu0" , title = '[COLOR white]' + title + ' [COLOR lightgreen][B][Series[/B].Mu][/COLOR][COLOR white][I] (' + origen + ')[/I][/COLOR]', url = url , thumbnail = thumbnail , show = show, fanart = fanart , folder = True , isPlayable = False )
                                data = file.readline()
                                i = i + 1
                                continue                              
                            data = file.readline()
                            i = i + 1
                            continue
                        else:
                            url = url.replace("serie:", "")
                            params["fanart"] = fanart
                            if url.find("seriesadicto") >= 0:
                                plugintools.add_item( action = "seriecatcher" , title = '[COLOR white]' + title + ' [COLOR lightgreen][B][Series[/B]adicto][/COLOR]', url = url , thumbnail = thumbnail , show = show, fanart = fanart , folder = True , isPlayable = False )
                                data = file.readline()
                                i = i + 1
                                continue
                            elif url.find("seriesflv") >= 0:
                                plugintools.add_item( action = "lista_capis" , title = '[COLOR white]' + title + ' [COLOR lightgreen][B][Series[/B]FLV][/COLOR]', url = url , thumbnail = thumbnail , show = show, fanart = fanart , folder = True , isPlayable = False )
                                data = file.readline()
                                i = i + 1
                                continue
                            elif url.find("seriesyonkis") >= 0:
                                plugintools.add_item( action = "serie_capis" , title = '[COLOR white]' + title + ' [COLOR lightgreen][B][Series[/B]Yonkis][/COLOR]', url = url , thumbnail = thumbnail , show = show, fanart = fanart , folder = True , isPlayable = False )
                                data = file.readline()
                                i = i + 1
                                continue
                            elif url.find("seriesblanco") >= 0:
                                plugintools.add_item( action = "seriesblanco0" , title = '[COLOR white]' + title + ' [COLOR lightgreen][B][Series[/B]Blanco][/COLOR]', url = url , thumbnail = thumbnail , show = show, fanart = fanart , folder = True , isPlayable = False )
                                data = file.readline()
                                i = i + 1
                                continue
                            elif url.find("series.mu") >= 0:
                                plugintools.add_item( action = "seriesmu0" , title = '[COLOR white]' + title + ' [COLOR lightgreen][B][Series[/B].Mu][/COLOR]', url = url , thumbnail = thumbnail , show = show, fanart = fanart , folder = True , isPlayable = False )
                                data = file.readline()
                                i = i + 1
                                continue
                elif url.startswith("peli") == True:
                    url = data.strip()
                    if cat == "":                                                 
                        url = url.replace("peli:", "")
                        params["fanart"] = fanart
                        if url.find("pelisadicto") >= 0:
                            plugintools.add_item( action = "seriecatcher" , title = '[COLOR white]' + title + ' [COLOR lightgreen][B][Pelis[/B]adicto][/COLOR][COLOR white][I] (' + origen + ')[/I][/COLOR]', url = url , thumbnail = thumbnail , show = show, fanart = fanart , folder = True , isPlayable = False )
                            data = file.readline()
                            i = i + 1
                            continue
                        elif url.find("oranline") >= 0:
                            plugintools.add_item( action = "oranline0" , title = '[COLOR white]' + title + ' [COLOR lightgreen][Oranline][/COLOR]', url = url , thumbnail = thumbnail , show = show, fanart = fanart , folder = True , isPlayable = False )
                            data = file.readline()
                            i = i + 1
                            continue
                        elif url.find("pordede.com") >= 0:
                            # Guardamos 'regex' como identificador de regex en la variable 'extra' y la URL de la película en 'page' para coger thumbnail y fanart
                            title_item = url.split("/peli/")[1];url_links=url.replace("/peli/","/links/view/slug/")+"/what/peli"
                            plugintools.add_item( action = "pdd_findvideos" , title = '[COLOR white]' + title + ' [COLOR lightgreen][Pordede][/COLOR]', url = url_links , page = url, thumbnail = thumbnail , extra = 'regex', show = show, fanart = fanart , folder = True , isPlayable = False )
                            data = file.readline()
                            i = i + 1
                            continue                        

                        data = file.readline()
                        i = i + 1
                        continue

                    else:
                        url = url.replace("peli:", "")
                        params["fanart"] = fanart
                        if url.find("pelisadicto") >= 0:
                            plugintools.add_item( action = "seriecatcher" , title = '[COLOR white]' + title + ' [COLOR lightgreen][B][Pelis[/B]adicto][/COLOR][COLOR white][I] (' + origen + ')[/I][/COLOR]', url = url , thumbnail = thumbnail , show = show, fanart = fanart , folder = True , isPlayable = False )
                            data = file.readline()
                            i = i + 1
                            continue
                        elif url.find("oranline") >= 0:
                            plugintools.add_item( action = "lista_capis" , title = '[COLOR white]' + title + ' [COLOR lightgreen][B][Series[/B]FLV][/COLOR][COLOR white][I] (' + origen + ')[/I][/COLOR]', url = url , thumbnail = thumbnail , show = show, fanart = fanart , folder = True , isPlayable = False )
                            data = file.readline()
                            i = i + 1
                            continue
                        elif url.find("pordede.com") >= 0:
                            # Guardamos 'regex' como identificador de regex en la variable 'extra' y la URL de la película en 'page' para coger thumbnail y fanart
                            title_item = url.split("/peli/")[1];url_links=url.replace("/peli/","/links/view/slug/")+"/what/peli"
                            plugintools.add_item( action = "pdd_findvideos" , title = '[COLOR white]' + title + ' [COLOR lightgreen][Pordede][/COLOR]', url = url_links , thumbnail = thumbnail , page = url, extra = 'regex', show = show, fanart = fanart , folder = True , isPlayable = False )
                            data = file.readline()
                            i = i + 1
                            continue                          

                        data = file.readline()
                        i = i + 1
                        continue

                elif url.startswith("cbz:") == True:
                    if url.find("copy.com") >= 0:
                        plugintools.log("CBR Copy.com")
                        #url = url.replace("cbz:", "").strip()
                    else:
                        url = url.replace("cbz:", "").strip()
                    title = title.split('"')
                    title = title[0]
                    title = title.strip()
                    plugintools.add_item( action = "cbx_reader" , title = '[COLOR white]' + title + '[COLOR gold] [CBZ][/COLOR]', url = url , plot = datamovie["Plot"], info_labels = datamovie , thumbnail = thumbnail , extra = show , show = show, fanart = fanart , folder = True , isPlayable = False )
                    data = file.readline()
                    i = i + 1
                    continue

                elif url.startswith("cbr:") == True:
                    if url.find("copy.com") >= 0:
                        plugintools.log("CBR Copy.com")
                        #url = url.replace("cbr:", "").strip()
                    else:
                        url = url.replace("cbr:", "").strip()
                    title = title.split('"')
                    title = title[0]
                    title = title.strip()
                    plugintools.add_item( action = "cbx_reader" , title = '[COLOR white]' + title + '[COLOR gold] [CBR][/COLOR]', url = url , plot = datamovie["Plot"], info_labels = datamovie , thumbnail = thumbnail , extra = show , show = show, fanart = fanart , folder = True , isPlayable = False )
                    data = file.readline()
                    i = i + 1
                    continue

                elif url.startswith("txt:") == True:
                    url = url.replace("txt:", "").strip()
                    txt_file = url.replace("txt:", "").strip()                        
                    title = title.split('"')
                    title = title[0]
                    title = title.strip()
                    plugintools.add_item( action = "txt_reader" , title = '[COLOR white]' + title + '[COLOR gold] [TXT][/COLOR]', url = url , plot = datamovie["Plot"], info_labels = datamovie , thumbnail = thumbnail , extra = show , show = show, fanart = fanart , folder = False , isPlayable = False )
                    data = file.readline()
                    i = i + 1
                    continue

                elif url.startswith("agendatv:") == True:
                    url = url.replace("agendatv:", "").strip()
                    if url == "futbolenlatv":
                        url = 'http://agenda.futbolenlatv.com/m?deporte=agenda'
                        action = 'futbolentv0'
                    elif url == "footballonuktv":
                        url = 'http://www.footballonuktv.com/'
                        action = 'agendatv'
                    elif url == "calciointv":
                        url = 'http://www.calciointv.com/'
                        action = 'agendatv'
                    elif url == "futbolenlatele":
                        url = 'http://www.futbolenlatele.com'
                        action = 'agendatv'
                    elif url == "queverahora":
                        url = 'http://www.formulatv.com/programacion/'
                        action = 'epg_verahora'                       
                    plugintools.add_item( action = action , title = '[COLOR white]' + title + '[COLOR gold] [Agenda[B]TV[/B]][/COLOR]', url = url , plot = datamovie["Plot"], info_labels = datamovie , thumbnail = thumbnail , extra = show , show = show, fanart = fanart , folder = False , isPlayable = False )
                    data = file.readline()
                    i = i + 1
                    continue                

                elif url.startswith("epg-txt") == True:
                    url=url.replace("epg-txt:", "")
                    title_fixed=title
                    try: url = epg_txt_dict(parser_title(title_fixed))
                    except: url="";pass
                    plugintools.add_item( action = "epg_txt0" , title = '[COLOR white]' + title + '[COLOR gold] [EPG-TXT][/COLOR]', url = url , plot = datamovie["Plot"], info_labels = datamovie , thumbnail = thumbnail , extra = show , show = show, fanart = fanart , folder = False , isPlayable = False )
                    data = file.readline()
                    i = i + 1
                    continue                

                elif url.startswith("short") == True:
                    if busqueda == 'search.txt':
                        url = url.replace("short:", "").strip()
                        plugintools.add_item( action = "longurl" , title = '[COLOR white]' + title + '[COLOR lightblue] [shortlink][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url , extra = show , show = show , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                        data = file.readline()
                        i = i + 1
                        continue
                    else:
                        url = url.replace("short:", "").strip()
                        plugintools.add_item( action = "longurl" , title = '[COLOR white]' + title + '[COLOR lightblue] [shortlink][/COLOR]', url = url , extra = show , show = show , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                        data = file.readline()
                        i = i + 1
                        continue

                elif url.startswith("devil") == True:
                    url=url.replace("devil:", "");
                    if url.find("referer") >= 0:
                        url = url.split(" referer=");pageurl=url[0].strip();ref=url[1].strip()
                    if cat != "":                                      
                        if ref != "":
                            url = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url='+pageurl+'%26referer='+ref                            
                        else:
                            url = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url='+pageurl
                        urllib.quote_plus(url)
                        plugintools.add_item( action = "runPlugin" , plot = plot , extra = filename , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + ' [COLOR orange][SportsDevil][/COLOR]' , url = url , info_labels = datamovie , thumbnail = thumbnail, show = show, page = show , fanart = fanart, folder = False, isPlayable=True)
                        data = file.readline()
                        i = i + 1
                        continue
                    else:                        
                        if ref != "":
                            url = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url='+pageurl+'%26referer='+ref                            
                        else:
                            url = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url='+pageurl
                        urllib.quote_plus(url)
                        plugintools.add_item( action = "runPlugin" , title = '[COLOR white]' + title + '[COLOR orange] [SportsDevil][/COLOR]', plot = plot , url = url , thumbnail = thumbnail , show = show, fanart = fanart, folder = False, isPlayable=True)
                        data = file.readline()
                        i = i + 1
                        continue

                elif url.startswith("filtro") == True:
                    url = url.replace("filtro:", "");url=url.split(",");filter=url[0];url=url[1]
                    if filter.startswith("filtro_gen") == True:
                        filter_fixed = filter.replace("filtro_gen:", "").strip()
                        filter_fixed = 'Filtro de género:[B]'+filter_fixed+'[/B]'
                    elif filter.startswith("filtro_title") == True:
                        filter_fixed = filter.replace("filtro_title:", "").strip()
                        filter_fixed = 'Filtro de título:[B]'+filter_fixed+'[/B]'
                    elif filter.startswith("filtro_year") == True:
                        filter_fixed = filter.replace("filtro_year:", "").strip()
                        filter_fixed = 'Filtro de Año:[B]'+filter_fixed+'[/B]'
                    elif filter.startswith("filtro_dir") == True:
                        filter_fixed = filter.replace("filtro_dir:", "").strip()
                        filter_fixed = 'Filtro de Director:[B]'+filter_fixed+'[/B]'
                    elif filter.startswith("filtro_cast") == True:
                        filter_fixed = filter.replace("filtro_cast:", "").strip()
                        filter_fixed = 'Filtro de Reparto:[B]'+filter_fixed+'[/B]'
                    elif filter.startswith("filtro_punt") == True:
                        filter_fixed = filter.replace("filtro_punt:", "").strip()
                        filter_fixed = 'Filtro de Puntuación:[B]'+filter_fixed+'[/B]'                        
                    else:
                        filter_fixed = 'Filtro desconocido'               
                    plugintools.add_item( action = "getfile_http" , title = '[COLOR white]' + title + '[COLOR gold][I] ['+filter_fixed+'][/I][/COLOR]', url = url , info_labels=datamovie, extra = "1" , page=filter, thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )
                    params["plot"]=datamovie
                    data = file.readline()
                    i = i + 1
                    continue                    
                    
                elif data.startswith("http") == True:
                    url = data.strip()
                    if cat != "":  # Controlamos el caso de subcategoría de canales
                        if busqueda == 'search.txt':
                            if url.startswith("serie") == True:
                                url = url.replace("serie:", "")
                                params["fanart"] = fanart
                                plugintools.add_item( action = "seriecatcher" , title = '[COLOR white]' + title + ' [COLOR purple][Serie online][/COLOR][COLOR lightsalmon](' + origen + ')[/I][/COLOR]' , url = url , thumbnail = thumbnail , show = show, fanart = fanart , folder = True , isPlayable = False )
                                data = file.readline()
                                i = i + 1
                                continue
                          
                            elif url.find("allmyvideos") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()
                                plugintools.add_item( action = "allmyvideos" , title = '[COLOR white]' + title + '[COLOR orange] [Allmyvideos][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url , thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("streamcloud") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "streamcloud" , title = '[COLOR white]' + title + '[COLOR orange] [Streamcloud][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )                          
                                data = file.readline()
                                i = i + 1
                                continue                        

                            elif url.find("vidspot") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "vidspot" , title = '[COLOR white]' + title + '[COLOR orange] [Vidspot][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("played.to") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "playedto" , title = '[COLOR white]' + title + '[COLOR orange] [Played.to][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("vk.com") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "vk" , title = '[COLOR white]' + title + '[COLOR orange] [Vk][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("nowvideo") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "nowvideo" , title = '[COLOR white]' + title + '[COLOR orange] [Nowvideo][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue
                            
                            elif url.find("tumi") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "tumi" , title = '[COLOR white]' + title + '[COLOR orange] [Tumi][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("veehd") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "veehd" , title = '[COLOR white]' + title + '[COLOR orange] [Veehd][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("streamin.to") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "streaminto" , title = '[COLOR white]' + title + '[COLOR orange] [Streamin.to][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("powvideo") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "powvideo" , title = '[COLOR white]' + title + '[COLOR orange] [powvideo][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("mail.ru") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "mailru" , title = '[COLOR white]' + title + '[COLOR orange] [Mail.ru][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("novamov") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "novamov" , title = '[COLOR white]' + title + '[COLOR orange] [Novamov][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("gamovideo") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "gamovideo" , title = '[COLOR white]' + title + '[COLOR orange] [Gamovideo][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("moevideos") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "moevideos" , title = '[COLOR white]' + title + '[COLOR orange] [Moevideos][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("movshare") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "movshare" , title = '[COLOR white]' + title + '[COLOR orange] [Movshare][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("movreel") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "movreel" , title = '[COLOR white]' + title + '[COLOR orange] [Movreel][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("videobam") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "videobam" , title = '[COLOR white]' + title + '[COLOR orange] [Videobam][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("videoweed") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "videoweed" , title = '[COLOR white]' + title + '[COLOR orange] [Videoweed][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("streamable") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "streamable" , title = '[COLOR white]' + title + '[COLOR orange] [Streamable][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("rocvideo") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "rocvideo" , title = '[COLOR white]' + title + '[COLOR orange] [Rocvideo][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue
                            
                            elif url.find("realvid") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "realvid" , title = '[COLOR white]' + title + '[COLOR orange] [Realvid][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue
                            
                            elif url.find("netu") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "netu" , title = '[COLOR white]' + title + '[COLOR orange] [Netu][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue
                            
                            elif url.find("videomega") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "videomega" , title = '[COLOR white]' + title + '[COLOR orange] [Videomega][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("video.tt") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "videott" , title = '[COLOR white]' + title + '[COLOR orange] [Video.tt][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("flashx") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "flashx" , title = '[COLOR white]' + title + '[COLOR orange] [Flashx][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("turbovideos") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "turbovideos" , title = '[COLOR white]' + title + '[COLOR orange] [Turbovideos][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("ok.ru") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "okru" , title = '[COLOR white]' + title + '[COLOR orange] [Ok.ru][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("vidto.me") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "vidtome" , title = '[COLOR white]' + title + '[COLOR orange] [Vidto.me][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue                                
                            
                            elif url.find("www.youtube.com") >= 0:  # Video youtube
                                plugintools.log("linea titulo= "+title_search)
                                title = title.split('"')[0].strip()
                                videoid = url.replace("https://www.youtube.com/watch?=", "")
                                url = 'plugin://plugin.video.youtube/play/?video_id='+videoid                       
                                plugintools.runAddon( action = "play" , title = '[COLOR white]' + title.strip() + ' [[COLOR red]You[COLOR white]tube Video][I] (' + origen + ')[/I][/COLOR]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = False )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("www.dailymotion.com/playlist") >= 0:  # Playlist
                                id_playlist = dailym_getplaylist(url)
                                if id_playlist != "":
                                    url = "https://api.dailymotion.com/playlist/"+id_playlist+"/videos"
                                    thumbnail = "https://api.dailymotion.com/thumbnail/video/"+id_playlist
                                    if thumbnail == "":
                                        thumbnail = 'http://press.dailymotion.com/wp-old/wp-content/uploads/logo-Dailymotion.png'
                                    plugintools.add_item( action="dailym_pl" , title=title + ' [COLOR lightyellow][B][Dailymotion[/B] playlist][/COLOR]' , fanart=fanart, show = show, thumbnail=thumbnail, url=url , folder=True, isPlayable=False)
                                else:
                                    data = file.readline()
                                    i = i + 1
                                    continue

                            elif url.find("dailymotion.com/video") >= 0:
                                video_id = dailym_getvideo(url)
                                if video_id != "":
                                    thumbnail = "https://api.dailymotion.com/thumbnail/video/"+video_id
                                    url = "plugin://plugin.video.dailymotion_com/?url="+video_id+"&mode=playVideo"
                                    # Appends a new item to the xbmc item list
                                    # API Dailymotion list of video parameters: http://www.dailymotion.com/doc/api/obj-video.html
                                    plugintools.add_item( action="play" , title=title + ' [COLOR lightyellow][B][Dailymotion[/B] video][/COLOR]' , url=url , thumbnail = thumbnail , show = show, fanart = fanart, isPlayable=True, folder=False )
                                    data = file.readline()
                                    i = i + 1
                                    continue
                                else:
                                    data = file.readline()
                                    i = i + 1
                                    continue        

                            elif url.endswith("m3u8") == True:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()
                                plugintools.add_item( action = "play" , title = '[COLOR white]' + title + '[COLOR purple] [m3u8][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url , info_labels = datamovie , thumbnail = thumbnail , extra = show , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.endswith(".torrent") == True:  # Archivos torrents
                                title_fixed = title.replace(" ", "+").strip()
                                url = p2p_builder_url(url, title_fixed, p2p="torrent")                               
                                plugintools.add_item( action = "play" , title = '[COLOR white]' + title + '[COLOR gold] [Torrent][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url , plot = datamovie["Plot"], info_labels = datamovie , thumbnail = thumbnail , extra = show , show = show, fanart = fanart , folder = True , isPlayable = False )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.startswith("short") == True:
                                url.replace("short:", "").strip()
                                title = title_search.split('"')
                                title = title[0]
                                title = title.strip()
                                plugintools.add_item( action = "longurl" , title = '[COLOR white]' + title + '[COLOR lightblue] [HTTP1][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url , extra = show , show = show , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                params["show"]=show
                                plugintools.log("show "+show)
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.endswith("acelive") == True:
                                title_fixed = parser_title(title);title_fixed=title_fixed.replace(" ", "+").strip()
                                url = p2p_builder_url(url, title_fixed, p2p="ace")
                                plugintools.add_item( action = "runPlugin" , title = '[COLOR white]' + title + '[COLOR lightblue] [Acestream][/COLOR]', url = url , extra = show , show = show , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                params["show"]=show
                                plugintools.log("show "+show)
                                data = file.readline()
                                i = i + 1
                                continue                            
                            
                            else:
                                title = title_search.split('"')
                                title = title[0]
                                title = title.strip()
                                plugintools.add_item( action = "play" , title = '[COLOR white]' + title + '[COLOR lightblue] [HTTP][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', info_labels = datamovie , plot = datamovie["Plot"], url = url , extra = show , show = show , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue
                        else:
                            if url.startswith("serie") == True:
                                url = url.replace("serie:", "")
                                params["fanart"] = fanart
                                plugintools.add_item( action = "seriecatcher" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + ' [COLOR purple][Serie online][/COLOR]', url = url , thumbnail = thumbnail , info_labels = datamovie , show = show, fanart = fanart , folder = True , isPlayable = False )
                                data = file.readline()
                                i = i + 1
                                continue
                            
                            elif url.find("allmyvideos") >= 0:
                                listitem = xbmcgui.ListItem( title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail )
                                plugintools.add_item( action = "allmyvideos" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR lightyellow] [Allmyvideos][/COLOR]' , url = url , thumbnail = thumbnail , info_labels = datamovie , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0
                                data = file.readline()
                                i = i + 1
                                continue
                            
                            elif url.find("streamcloud") >= 0:                             
                                plugintools.add_item( action = "streamcloud" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR lightskyblue] [Streamcloud][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("vidspot") == True:                             
                                plugintools.add_item( action = "vidspot" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR palegreen] [Vidspot][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0                                
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("played.to") >= 0:                            
                                plugintools.add_item( action = "playedto" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR lavender] [Played.to][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0                              
                                data = file.readline()
                                i = i + 1
                                continue
                            
                            elif url.find("vk") >= 0:                            
                                plugintools.add_item( action = "vk" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR royalblue] [Vk][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0                              
                                data = file.readline()
                                i = i + 1
                                continue                            

                            elif url.find("nowvideo") >= 0:                            
                                plugintools.add_item( action = "nowvideo" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR red] [Nowvideo][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0                               
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("tumi") >= 0:                            
                                plugintools.add_item( action = "tumi" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR forestgreen] [Tumi][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0                               
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("veehd") >= 0:                            
                                plugintools.add_item( action = "veehd" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR orange] [VeeHD][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0                               
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("streamin.to") >= 0:                            
                                plugintools.add_item( action = "streaminto" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR orange] [streamin.to][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0                           
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("mail.ru") >= 0:                            
                                plugintools.add_item( action = "mailru" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR orange] [Mail.ru][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0                              
                                data = file.readline()
                                i = i + 1
                                continue                            

                            elif url.find("powvideo") >= 0:                            
                                plugintools.add_item( action = "powvideo" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR orange] [Powvideo][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0                              
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("novamov") >= 0:                            
                                plugintools.add_item( action = "novamov" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR orange] [Novamov][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0                              
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("gamovideo") >= 0:                            
                                plugintools.add_item( action = "gamovideo" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR orange] [Gamovideo][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0                              
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("moevideos") >= 0:                            
                                plugintools.add_item( action = "moevideos" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR orange] [Moevideos][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0                              
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("movshare") >= 0:                            
                                plugintools.add_item( action = "movshare" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR orange] [Movshare][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0                              
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("movreel") >= 0:                            
                                plugintools.add_item( action = "movreel" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR orange] [Movreel][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0                              
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("videobam") >= 0:                            
                                plugintools.add_item( action = "videobam" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR orange] [Videobam][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0                              
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("videoweed") >= 0:                            
                                plugintools.add_item( action = "videoweed" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR orange] [Videoweed][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0                              
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("streamable") >= 0:                            
                                plugintools.add_item( action = "streamable" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR orange] [Streamable][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0                              
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("rocvideo") >= 0:                            
                                plugintools.add_item( action = "rocvideo" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR orange] [Rocvideo][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0                              
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("realvid") >= 0:                            
                                plugintools.add_item( action = "realvid" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR orange] [Realvid][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0                              
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("netu") >= 0:                            
                                plugintools.add_item( action = "netu" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR orange] [Netu][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0                              
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("videomega") >= 0:                            
                                plugintools.add_item( action = "videomega" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR orange] [Videomega][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0                              
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("video.tt") >= 0:                            
                                plugintools.add_item( action = "videott" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR orange] [Video.tt][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0                              
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("flashx.tv") >= 0:                            
                                plugintools.add_item( action = "flashx" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR orange] [Flashx][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0                              
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("turbovideos") >= 0:                            
                                plugintools.add_item( action = "turbovideos" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR orange] [Turbovideos][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0                              
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("ok.ru") >= 0:                            
                                plugintools.add_item( action = "okru" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR orange] [Ok.ru][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0                              
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("vidto.me") >= 0:                            
                                plugintools.add_item( action = "vidtome" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR orange] [Vidto.me][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0                              
                                data = file.readline()
                                i = i + 1
                                continue                            
   
                            elif url.find("www.youtube.com") >= 0:  # Video youtube
                                title = title.split('"')[0].strip()
                                videoid = url.replace("https://www.youtube.com/watch?=", "")
                                url = 'plugin://plugin.video.youtube/play/?video_id='+videoid                       
                                plugintools.runAddon( action = "play" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + ' [[COLOR red]You[COLOR white]tube Video][/COLOR]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = False )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0                                
                                data = file.readline()
                                i = i + 1
                                continue
                            
                            elif url.find("www.dailymotion.com/playlist") >= 0:  # Playlist
                                id_playlist = dailym_getplaylist(url)
                                if id_playlist != "":
                                    plugintools.log("id_playlist= "+id_playlist)
                                    if thumbnail == "":
                                        thumbnail = 'http://press.dailymotion.com/wp-old/wp-content/uploads/logo-Dailymotion.png'
                                    url = "https://api.dailymotion.com/playlist/"+id_playlist+"/videos"
                                    plugintools.add_item( action="dailym_pl" , title='[COLOR red][I]'+cat+' / [/I][/COLOR] '+title+' [COLOR lightyellow][B][Dailymotion[/B] playlist][/COLOR]', url=url , fanart = fanart , show = show, thumbnail=thumbnail , folder=True, isPlayable=False)
                                else:
                                    data = file.readline()
                                    i = i + 1
                                    continue

                            elif url.find("dailymotion.com/video") >= 0:
                                video_id = dailym_getvideo(url)
                                if video_id != "":
                                    thumbnail = "https://api.dailymotion.com/thumbnail/video/"+video_id+""
                                    url = "plugin://plugin.video.dailymotion_com/?url="+video_id+"&mode=playVideo"
                                    # Appends a new item to the xbmc item list
                                    # API Dailymotion list of video parameters: http://www.dailymotion.com/doc/api/obj-video.html
                                    plugintools.add_item( action="play" , title='[COLOR red][I]' + cat + ' / [/I][/COLOR] '+title+' [COLOR lightyellow][B][Dailymotion[/B] Video][/COLOR]', url=url , thumbnail = thumbnail , show = show, fanart= fanart , isPlayable=True, folder=False )
                                    data = file.readline()
                                    i = i + 1
                                    continue
                                else:
                                    data = file.readline()
                                    i = i + 1
                                    continue
                                    
                                data = file.readline()
                                i = i + 1
                                continue  

                            elif url.endswith("m3u8") == True:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "play" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR purple] [m3u8][/COLOR]', url = url , plot = plot , info_labels = datamovie , thumbnail = thumbnail , extra = show , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.startswith("cbz") == True:
                                if url.find("copy.com") >= 0:
                                    plugintools.log("CBZ Copy.com")
                                    #url = url.replace("cbz:", "").strip()
                                else:
                                    url = url.replace("cbz:", "").strip()
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "cbx_reader" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR gold] [CBZ][/COLOR]', url = url , plot = datamovie["Plot"] , info_labels = datamovie , thumbnail = thumbnail , extra = show , show = show, fanart = fanart , folder = True , isPlayable = False )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.startswith("cbr") == True:
                                if url.find("copy.com") >= 0:
                                    plugintools.log("CBR Copy.com")
                                    #url = url.replace("cbr:", "").strip()
                                else:
                                    url = url.replace("cbr:", "").strip()
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "cbx_reader" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR gold] [CBR][/COLOR]', url = url , plot = datamovie["Plot"], info_labels = datamovie , thumbnail = thumbnail , extra = show , show = show, fanart = fanart , folder = True , isPlayable = False )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.startswith("txt") == True:
                                url = url.replace("txt:", "").strip()
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "txt_reader" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR gold] [TXT][/COLOR]', url = url , plot = datamovie["Plot"], info_labels = datamovie , thumbnail = thumbnail , extra = show , show = show, fanart = fanart , folder = False , isPlayable = False )
                                data = file.readline()
                                i = i + 1
                                continue  

                            elif url.endswith("acelive") == True:
                                title_fixed = parser_title(title);title=title.replace(" ", "+").strip()
                                url = p2p_builder_url(url, title_fixed, p2p="ace")
                                plugintools.add_item( action = "runPlugin" , title = '[COLOR white]' + title + '[COLOR lightblue] [Acestream][/COLOR]', url = url , extra = show , show = show , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                params["show"]=show
                                plugintools.log("show "+show)
                                data = file.readline()
                                i = i + 1
                                continue                            

                            elif url.startswith("short") == True:
                                url.replace("short:", "").strip()
                                title = title_search.split('"')
                                title = title[0]
                                title = title.strip()
                                plugintools.add_item( action = "longurl" , title = '[COLOR white]' + title + '[COLOR lightblue] [HTTP][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url , extra = show , show = show , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                params["show"]=show
                                plugintools.log("show "+show)
                                data = file.readline()
                                i = i + 1
                                continue                              
                            
                            else:
                                plugintools.add_item( action = "play" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR blue] [HTTP][/COLOR]' , url = url , plot = plot , info_labels = datamovie , extra = show , show = show , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )                                
                                data = file.readline()
                                i = i + 1
                                continue
                            
                    # Sin categoría de canales   
                    else:
                        if busqueda == 'search.txt':
                            if url.startswith("serie") == True:
                                url = url.replace("serie:", "")
                                params["fanart"] = fanart
                                plugintools.log("fanart= "+fanart)
                                plugintools.add_item( action = "seriecatcher" , title = '[COLOR white]' + title + ' [COLOR purple][Serie online][/COLOR][COLOR lightsalmon](' + origen + ')[/I][/COLOR]' , url = url , thumbnail = thumbnail , show = show, fanart = fanart , folder = True , isPlayable = False )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.startswith("goear") == True:
                                params["fanart"] = fanart
                                if show == "list":
                                    show = plugintools.get_setting("music_id")
                                    plugintools.log("show en config")
                                data = file.readline()
                                if data.startswith("desc") == True:
                                    datamovie["Plot"] = data.replace("desc=", "").replace('"',"")                                    
                                plugintools.add_item( action = "goear" , plot = plot , title = '[COLOR white]' + title + ' [COLOR blue][goear][/COLOR][COLOR lightsalmon](' + origen + ')[/I][/COLOR]' , url = url , thumbnail = thumbnail , info_labels = datamovie , extra = show , show = show, fanart = fanart , folder = True , isPlayable = False )
                                data = file.readline()                                    
                                i = i + 1
                                continue
                                                        
                            elif url.find("allmyvideos") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()
                                listitem = xbmcgui.ListItem( title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail )
                                plugintools.add_item( action = "allmyvideos" , title = '[COLOR white]' + title + '[COLOR lightyellow] [Allmyvideos][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url , thumbnail = thumbnail , info_labels = datamovie , show = show, fanart = fanart , folder = False , isPlayable = True )                                                      
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("streamcloud") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                             
                                plugintools.add_item( action = "streamcloud" , title = '[COLOR white]' + titulo + '[COLOR lightskyblue] [Streamcloud][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0								
                                data = file.readline()
                                i = i + 1
                                continue                        
                            
                            elif url.find("vidspot") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                             
                                plugintools.add_item( action = "vidspot" , title = '[COLOR white]' + title + '[COLOR palegreen] [Vidspot][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0								
                                data = file.readline()
                                i = i + 1
                                continue
                            
                            elif url.find("played.to") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                             
                                plugintools.add_item( action = "playedto" , title = '[COLOR white]' + title + '[COLOR lavender] [Played.to][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0								
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("vk.com") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                             
                                plugintools.add_item( action = "vk" , title = '[COLOR white]' + title + '[COLOR royalblue] [Vk][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0								
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("nowvideo") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                             
                                plugintools.add_item( action = "nowvideo" , title = '[COLOR white]' + title + '[COLOR red] [Nowvideo][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0								
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("tumi.tv") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                             
                                plugintools.add_item( action = "tumi" , title = '[COLOR white]' + title + '[COLOR forestgreen] [Tumi][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0								
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("veehd") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                             
                                plugintools.add_item( action = "veehd" , title = '[COLOR white]' + title + '[COLOR orange] [VeeHD][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0								
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("streamin.to") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                             
                                plugintools.add_item( action = "streaminto" , title = '[COLOR white]' + title + '[COLOR orange] [streamin.to][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url , thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0								
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("powvideo") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                             
                                plugintools.add_item( action = "powvideo" , title = '[COLOR white]' + title + '[COLOR orange] [Powvideo][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0								
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("mail.ru") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                             
                                plugintools.add_item( action = "mailru" , title = '[COLOR white]' + title + '[COLOR orange] [Mail.ru][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0								
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("novamov") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                             
                                plugintools.add_item( action = "novamov" , title = '[COLOR white]' + title + '[COLOR orange] [Novamov][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0								
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("moevideos") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                             
                                plugintools.add_item( action = "moevideos" , title = '[COLOR white]' + title + '[COLOR orange] [Moevideos][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0								
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("videoweed") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                             
                                plugintools.add_item( action = "videoweed" , title = '[COLOR white]' + title + '[COLOR orange] [Videoweed][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0								
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("streamable") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                             
                                plugintools.add_item( action = "streamable" , title = '[COLOR white]' + title + '[COLOR orange] [Streamable][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0								
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("rocvideo") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                             
                                plugintools.add_item( action = "rocvideo" , title = '[COLOR white]' + title + '[COLOR orange] [Rocvideo][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0								
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("realvid") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                             
                                plugintools.add_item( action = "realvid" , title = '[COLOR white]' + title + '[COLOR orange] [Realvid][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0								
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("netu") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                             
                                plugintools.add_item( action = "netu" , title = '[COLOR white]' + title + '[COLOR orange] [Netu][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0								
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("videomega") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                             
                                plugintools.add_item( action = "videomega" , title = '[COLOR white]' + title + '[COLOR orange] [Videomega][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0								
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("video.tt") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                             
                                plugintools.add_item( action = "videott" , title = '[COLOR white]' + title + '[COLOR orange] [Video.tt][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0								
                                data = file.readline()
                                i = i + 1
                                continue                             

                            elif url.find("flashx.tv") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                             
                                plugintools.add_item( action = "flashx" , title = '[COLOR white]' + title + '[COLOR orange] [Flashx][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0								
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("turbovideos") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                             
                                plugintools.add_item( action = "turbovideos" , title = '[COLOR white]' + title + '[COLOR orange] [Turbovideos][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0								
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("vidto.me") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                             
                                plugintools.add_item( action = "vidtome" , title = '[COLOR white]' + title + '[COLOR orange] [Vidto.me][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0								
                                data = file.readline()
                                i = i + 1
                                continue                            

                            elif url.find("ok.ru") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                             
                                plugintools.add_item( action = "okru" , title = '[COLOR white]' + title + '[COLOR orange] [Ok.ru][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0								
                                data = file.readline()
                                i = i + 1
                                continue                                

                            elif url.find("www.youtube.com") >= 0:
                                title = title.split('"')[0].strip()
                                videoid = url.replace("https://www.youtube.com/watch?=", "")
                                url = 'plugin://plugin.video.youtube/play/?video_id='+videoid                       
                                plugintools.runAddon( action = "play" , title = '[COLOR white][' + title + ' [[COLOR red]You4[/COLOR][COLOR white]tube Video][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = False )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("www.dailymotion.com/playlist") >= 0:  # Playlist
                                id_playlist = dailym_getplaylist(url)
                                if id_playlist != "":
                                    if thumbnail == "":
                                        thumbnail = 'http://press.dailymotion.com/wp-old/wp-content/uploads/logo-Dailymotion.png'                               
                                    url = "https://api.dailymotion.com/playlist/"+id_playlist+"/videos"
                                    plugintools.add_item( action="dailym_pl" , title=title+' [COLOR lightyellow][B][Dailymotion[/B] playlist][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url=url , fanart = fanart , show = show, thumbnail=thumbnail , folder=True, isPlayable=False)
                                else:
                                    data = file.readline()
                                    i = i + 1
                                    continue

                            elif url.find("dailymotion.com/video") >= 0:
                                video_id = dailym_getvideo(url)
                                if video_id != "":
                                    thumbnail = "https://api.dailymotion.com/thumbnail/video/"+video_id+""
                                    url = "plugin://plugin.video.dailymotion_com/?url="+video_id+"&mode=playVideo"
                                    # Appends a new item to the xbmc item list
                                    # API Dailymotion list of video parameters: http://www.dailymotion.com/doc/api/obj-video.html
                                    plugintools.add_item( action="play" , title=title+' [COLOR lightyellow][B][Dailymotion[/B] video][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url=url , fanart = fanart , show = show, thumbnail = thumbnail , isPlayable=True, folder=False )
                                    data = file.readline()
                                    i = i + 1
                                    continue
                                else:
                                    data = file.readline()
                                    i = i + 1
                                    continue
                                    
                                data = file.readline()
                                i = i + 1
                                continue                             
                            
                            elif url.endswith("m3u8") == True:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "play" , title = '[COLOR white]' + title + ' [COLOR purple][m3u8][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url , info_labels = datamovie , thumbnail = thumbnail , extra = show , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.startswith("cbz:") == True:
                                if url.find("copy.com") >= 0:
                                    plugintools.log("CBZ Copy.com")
                                    #url = url.replace("cbz:", "").strip()
                                else:
                                    url = url.replace("cbz:", "").strip()
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "cbx_reader" , title = '[COLOR white]' + title + ' [COLOR gold][CBZ][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url , plot = datamovie["Plot"], info_labels = datamovie , thumbnail = thumbnail , extra = show , show = show, fanart = fanart , folder = True , isPlayable = False )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.startswith("cbr:") == True:
                                if url.find("copy.com") >= 0:
                                    plugintools.log("CBR Copy.com")
                                    #url = url.replace("cbr:", "").strip()
                                else:
                                    url = url.replace("cbr:", "").strip()
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "cbx_reader" , title = '[COLOR white]' + title + ' [COLOR gold][CBR][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url , plot = datamovie["Plot"], info_labels = datamovie , thumbnail = thumbnail , extra = show , show = show, fanart = fanart , folder = True , isPlayable = False )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.startswith("txt:") == True:
                                url = url.replace("txt:", "").strip()
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "txt_reader" , title = '[COLOR white]' + title + ' [COLOR gold][TXT][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url , plot = datamovie["Plot"], info_labels = datamovie , thumbnail = thumbnail , extra = show , show = show, fanart = fanart , folder = False , isPlayable = False )
                                data = file.readline()
                                i = i + 1
                                continue                             

                            elif url.find("mediafire") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "cbx_reader" , title = '[COLOR white]' + title + ' [COLOR gold][Mediafire][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url , info_labels = datamovie , thumbnail = thumbnail , extra = show , show = show, fanart = fanart , folder = True , isPlayable = False )
                                data = file.readline()
                                i = i + 1
                                continue        

                            elif url.startswith("short") == True:
                                url.replace("short:", "").strip()
                                title = title_search.split('"')
                                title = title[0]
                                title = title.strip()
                                plugintools.add_item( action = "longurl" , title = '[COLOR white]' + title + '[COLOR lightblue] [HTTP][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url , extra = show , show = show , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                params["show"]=show
                                plugintools.log("show "+show)
                                data = file.readline()
                                i = i + 1
                                continue                             
                            
                            else:                      
                                title = title_search[0]
                                title = title.strip()                             
                                plugintools.add_item( action = "play" , title = '[COLOR white]' + title + ' [COLOR blue][HTTP][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url , extra = show , show = show , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                params["show"]=show
                                plugintools.log("show "+show)
                                data = file.readline()
                                i = i + 1
                                continue

                        else:
                            if url.find("allmyvideos") >= 0:
                                listitem = xbmcgui.ListItem( title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail )
                                plugintools.add_item( action = "allmyvideos" , title = '[COLOR white]' + title + ' [COLOR lightyellow][Allmyvideos][/COLOR]', url = url , thumbnail = thumbnail , info_labels = datamovie , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("streamcloud") >= 0:                             
                                plugintools.add_item( action = "streamcloud" , title = '[COLOR white]' + title + ' [COLOR lightskyblue][Streamcloud][/COLOR]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0								
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("vidspot") >= 0:                            
                                plugintools.add_item( action = "vidspot" , title = '[COLOR white]' + title + ' [COLOR palegreen][Vidspot][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0								
                                data = file.readline()
                                i = i + 1
                                continue
                            
                            elif url.find("played.to") >= 0:                            
                                plugintools.add_item( action = "playedto" , title = '[COLOR white]' + title + ' [COLOR lavender][Played.to][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0								
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("vk.com") >= 0:                            
                                plugintools.add_item( action = "vk" , title = '[COLOR white]' + title + ' [COLOR royalblue][Vk][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0								
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("nowvideo") >= 0:                            
                                plugintools.add_item( action = "nowvideo" , title = '[COLOR white]' + title + '[COLOR red] [Nowvideo][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0								
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("tumi.tv") >= 0:                            
                                plugintools.add_item( action = "tumi" , title = '[COLOR white]' + title + '[COLOR forestgreen] [Tumi][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0								
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("VeeHD") >= 0:                            
                                plugintools.add_item( action = "veehd" , title = '[COLOR white]' + title + '[COLOR forestgreen] [VeeHD][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0								
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("streamin.to") >= 0:                            
                                plugintools.add_item( action = "streaminto" , title = '[COLOR white]' + title + '[COLOR forestgreen] [streamin.to][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0								
                                data = file.readline()
                                i = i + 1
                                continue
                            
                            elif url.find("powvideo") >= 0:                            
                                plugintools.add_item( action = "powvideo" , title = '[COLOR white]' + title + '[COLOR forestgreen] [Powvideo][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0								
                                data = file.readline()
                                i = i + 1
                                continue
                            
                            elif url.find("mail.ru") >= 0:                            
                                plugintools.add_item( action = "mailru" , title = '[COLOR white]' + title + '[COLOR forestgreen] [Mail.ru][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0								
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("novamov") >= 0:                            
                                plugintools.add_item( action = "novamov" , title = '[COLOR white]' + title + '[COLOR forestgreen] [Novamov][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0								
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("gamovideo") >= 0:                            
                                plugintools.add_item( action = "gamovideo" , title = '[COLOR white]' + title + '[COLOR forestgreen] [Gamovideo][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0								
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("moevideos") >= 0:                            
                                plugintools.add_item( action = "moevideos" , title = '[COLOR white]' + title + '[COLOR forestgreen] [Moevideos][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0								
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("movshare") >= 0:                            
                                plugintools.add_item( action = "movshare" , title = '[COLOR white]' + title + '[COLOR forestgreen] [Movshare][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0								
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("movreel") >= 0:                            
                                plugintools.add_item( action = "movreel" , title = '[COLOR white]' + title + '[COLOR forestgreen] [Movreel][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0								
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("videobam") >= 0:                            
                                plugintools.add_item( action = "videobam" , title = '[COLOR white]' + title + '[COLOR forestgreen] [Videobam][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0								
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("videoweed") >= 0:                            
                                plugintools.add_item( action = "videoweed" , title = '[COLOR white]' + title + '[COLOR forestgreen] [Videoweed][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0								
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("streamable") >= 0:                            
                                plugintools.add_item( action = "streamable" , title = '[COLOR white]' + title + '[COLOR forestgreen] [streamable][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0								
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("rocvideo") >= 0:                            
                                plugintools.add_item( action = "rocvideo" , title = '[COLOR white]' + title + '[COLOR forestgreen] [Rocvideo][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0								
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("realvid") >= 0:                            
                                plugintools.add_item( action = "realvid" , title = '[COLOR white]' + title + '[COLOR forestgreen] [Realvid][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0								
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("netu") >= 0:                            
                                plugintools.add_item( action = "netu" , title = '[COLOR white]' + title + '[COLOR forestgreen] [Netu][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0								
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("videomega") >= 0:                            
                                plugintools.add_item( action = "videomega" , title = '[COLOR white]' + title + '[COLOR forestgreen] [Videomega][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0								
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("video.tt") >= 0:                            
                                plugintools.add_item( action = "videott" , title = '[COLOR white]' + title + '[COLOR forestgreen] [Video.tt][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0								
                                data = file.readline()
                                i = i + 1
                                continue                            

                            elif url.find("flashx.tv") >= 0:                            
                                plugintools.add_item( action = "flashx" , title = '[COLOR white]' + title + '[COLOR forestgreen] [Flashx][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0								
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("turbovideos") >= 0:                            
                                plugintools.add_item( action = "turbovideos" , title = '[COLOR white]' + title + '[COLOR forestgreen] [Turbovideos][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0								
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("ok.ru") >= 0:                            
                                plugintools.add_item( action = "okru" , title = '[COLOR white]' + title + '[COLOR forestgreen] [Ok.ru][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0								
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("vidto.me") >= 0:                            
                                plugintools.add_item( action = "vidtome" , title = '[COLOR white]' + title + '[COLOR forestgreen] [Vidto.me][/COLOR]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                if saving_url == 1:
                                    save_url(url, filename)
                                    saving_url = 0								
                                data = file.readline()
                                i = i + 1
                                continue                            

                            elif url.find("www.youtube.com") >= 0:
                                title = title.split('"')[0].strip()
                                videoid = url.replace("https://www.youtube.com/watch?v=", "")
                                url = 'plugin://plugin.video.youtube/play/?video_id='+videoid                       
                                plugintools.runAddon( action = "play" , title = '[COLOR white]' + title + ' [[COLOR red]You[/COLOR][COLOR white]tube Video][/COLOR]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = False )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("www.dailymotion.com/playlist") >= 0:  # Playlist
                                id_playlist = dailym_getplaylist(url)
                                if id_playlist != "":
                                    plugintools.log("id_playlist= "+id_playlist)
                                    thumbnail=__art__+'/lnh_logo.png'
                                    url = "https://api.dailymotion.com/playlist/"+id_playlist+"/videos"
                                    #plugintools.log("url= "+url)
                                    plugintools.add_item( action="dailym_pl" , title=title + ' [COLOR lightyellow][B][Dailymotion[/B] playlist][/COLOR]' , url=url , fanart = fanart , show = show, thumbnail=thumbnail , folder=True)
                                else:
                                    data = file.readline()
                                    i = i + 1
                                    continue

                            elif url.find("dailymotion.com/video") >= 0:
                                video_id = dailym_getvideo(url)
                                if video_id != "":
                                    thumbnail = "https://api.dailymotion.com/thumbnail/video/"+video_id+""
                                    url = "plugin://plugin.video.dailymotion_com/?url="+video_id+"&mode=playVideo"
                                    #plugintools.log("url= "+url)
                                    # Appends a new item to the xbmc item list
                                    # API Dailymotion list of video parameters: http://www.dailymotion.com/doc/api/obj-video.html
                                    plugintools.add_item( action="play" , title=title + ' [COLOR lightyellow][B][Dailymotion[/B] video][/COLOR]' , url=url , thumbnail = thumbnail , show = show, fanart = fanart , isPlayable=True, folder=False )
                                    data = file.readline()
                                    i = i + 1
                                    continue
                                else:
                                    data = file.readline()
                                    i = i + 1
                                    continue
                                    
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.endswith("m3u8") == True:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "play" , title = '[COLOR white]' + title + ' [COLOR purple][m3u8][/COLOR]', plot = plot , url = url , info_labels = datamovie , thumbnail = thumbnail , extra = show , show = show, fanart = fanart , folder = False , isPlayable = True )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.startswith("cbz:") == True:
                                if url.find("copy.com") >= 0:
                                    plugintools.log("CBZ Copy.com")
                                    #url = url.replace("cbz:", "").strip()
                                else:
                                    url = url.replace("cbz:", "").strip()
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "cbx_reader" , title = '[COLOR white]' + title + ' [COLOR gold][CBZ][/COLOR]', url = url , plot = datamovie["Plot"], info_labels = datamovie , thumbnail = thumbnail , extra = show , show = show, fanart = fanart , folder = True , isPlayable = False )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.startswith("cbr:") == True:
                                if url.find("copy.com") >= 0:
                                    plugintools.log("CBR Copy.com")
                                    #url = url.replace("cbr:", "").strip()
                                else:
                                    url = url.replace("cbr:", "").strip()
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "cbx_reader" , title = '[COLOR white]' + title + ' [COLOR gold][CBR][/COLOR]', url = url , plot = datamovie["Plot"], info_labels = datamovie , thumbnail = thumbnail , extra = show , show = show, fanart = fanart , folder = True , isPlayable = False )
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.startswith("txt:") == True:
                                url = url.replace("txt:", "").strip()
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "txt_reader" , title = '[COLOR white]' + title + ' [COLOR gold][TXT][/COLOR]', url = url , plot = datamovie["Plot"], info_labels = datamovie , thumbnail = thumbnail , extra = show , show = show, fanart = fanart , folder = False , isPlayable = False )
                                data = file.readline()
                                i = i + 1
                                continue                              

                            elif url.find("mediafire") >= 0:
                                title = title.split('"')
                                title = title[0]
                                title = title.strip()                            
                                plugintools.add_item( action = "cbx_reader" , title = '[COLOR white]' + title + ' [COLOR gold][Mediafire][/COLOR]', plot = plot , url = url , info_labels = datamovie , thumbnail = thumbnail , extra = show , show = show, fanart = fanart , folder = True , isPlayable = False )
                                data = file.readline()
                                i = i + 1
                                continue  

                            elif url.startswith("short") == True:
                                url.replace("short:", "").strip()
                                title = title_search.split('"')
                                title = title[0]
                                title = title.strip()
                                plugintools.add_item( action = "longurl" , title = '[COLOR white]' + title + '[COLOR lightblue] [HTTP][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url , extra = show , show = show , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                params["show"]=show
                                plugintools.log("show "+show)
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.endswith("acelive") == True:
                                title_fixed = parser_title(title);title_fixed=title.replace(" ", "+").strip()
                                url = p2p_builder_url(url, title_fixed, p2p="ace")
                                plugintools.add_item( action = "runPlugin" , title = '[COLOR white]' + title + '[COLOR lightblue] [Acestream][/COLOR]', url = url , extra = show , show = show , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                params["show"]=show
                                plugintools.log("show "+show)
                                data = file.readline()
                                i = i + 1
                                continue

                            elif url.find("veetle.com") >= 0: 
                                plugintools.add_item( action = "veetle" , title = '[COLOR white]' + title + '[COLOR red] [Veetle][/COLOR]', url = url , extra = show , show = show , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                params["show"]=show
                                plugintools.log("show "+show)
                                data = file.readline()
                                i = i + 1
                                continue                              
                            
                            else:
                                plugintools.add_item( action = "play" , title = '[COLOR red][I]' + '[/I][/COLOR][COLOR white]' + title + ' [COLOR blue][HTTP][/COLOR]' , plot = plot , url = url , extra = show , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                                params["show"]=show
                                plugintools.log("show "+show)
                                data = file.readline()
                                i = i + 1
                                continue
              
                if data.startswith("rtmp") == True or data.startswith("rtsp") == True:
                    url = data
                    url = parse_url(url)
                    if cat != "":  # Controlamos el caso de subcategoría de canales
                        if busqueda == 'search.txt':
                            params["url"] = url
                            server_rtmp(params)
                            server = params.get("server")
                            url = params.get("url")   
                            plugintools.add_item( action = "launch_rtmp" , title = '[COLOR white]' + titulo + '[COLOR green] [' + server + '][/COLOR][I][COLOR lightgreen] (' + origen + ')[/COLOR][/I]', url = params.get("url") , thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                            params["server"] = server
                            data = file.readline()
                            i = i + 1
                            continue
                        else:
                            params["url"] = url
                            server_rtmp(params)
                            server = params.get("server")
                            url = params.get("url")                                                                                                     
                            plugintools.add_item( action = "launch_rtmp" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR green] [' + server + '][/COLOR]' , plot = plot , url = params.get("url") , info_labels = datamovie , thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                            data = file.readline()
                            i = i + 1
                            continue
                            
                    else:
                        if busqueda == 'search.txt':
                            params["url"] = url
                            server_rtmp(params)
                            server = params.get("server")
                            url = params.get("url")
                            plugintools.add_item( action = "launch_rtmp" , title = '[COLOR white]' + titulo + '[COLOR green] [' + server + '][/COLOR][I][COLOR lightgreen] (' + origen + ')[/COLOR][/I]' , url = params.get("url") , info_labels = datamovie , thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                            data = file.readline()
                            i = i + 1
                            continue
                        else:
                            params["url"] = url
                            server_rtmp(params)
                            server = params.get("server")
                            url = params.get("url")
                            plugintools.add_item( action = "launch_rtmp" , title = '[COLOR white]' + title + '[COLOR green] ['+ server + '][/COLOR]' , plot = plot , url = params.get("url") , info_labels = datamovie , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                            data = file.readline()
                            i = i + 1
                            continue

                if data.startswith("udp") == True or data.startswith("rtp") == True:
                    # print "udp"
                    url = data
                    url = parse_url(url)
                    if cat != "":  # Controlamos el caso de subcategoría de canales
                        if busqueda == 'search.txt':
                            plugintools.add_item( action = "play" , title = '[COLOR white]' + titulo + '[COLOR red] [UDP][/COLOR][I][COLOR lightgreen] (' + origen + ')[/COLOR][/I]', url = url , info_labels = datamovie , thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                            data = file.readline()
                            i = i + 1
                            continue
                        else:
                            plugintools.add_item( action = "play" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR red] [UDP][/COLOR]' , plot = plot , url = url , info_labels = datamovie , thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                            data = file.readline()
                            i = i + 1
                            continue
                            
                    else:
                        if busqueda == 'search.txt':
                            plugintools.add_item( action = "play" , title = '[COLOR white]' + titulo + '[COLOR red] [UDP][/COLOR][I][COLOR lightgreen] (' + origen + ')[/COLOR][/I]' , url = url , info_labels = datamovie , thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                            data = file.readline()
                            i = i + 1
                            continue
                        else:
                            plugintools.add_item( action = "play" , title = '[COLOR white]' + title + '[COLOR red] [UDP][/COLOR]' , plot = plot , url = url , info_labels = datamovie , thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                            data = file.readline()
                            i = i + 1
                            continue

                if data.startswith("mms") == True or data.startswith("rtp") == True:
                    url = parse_url(data)
                    plugintools.log("url retornada= "+url)
                    if cat != "":  # Controlamos el caso de subcategoría de canales
                        if busqueda == 'search.txt':
                            plugintools.add_item( action = "play" , title = '[COLOR white]' + titulo + '[COLOR red] [MMS][/COLOR][I][COLOR lightgreen] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                            data = file.readline()
                            i = i + 1
                            continue
                        else:
                            plugintools.add_item( action = "play" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR red] [MMS][/COLOR]' , plot = plot , url = url , thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                            data = file.readline()
                            i = i + 1
                            continue
                            
                    else:
                        if busqueda == 'search.txt':
                            plugintools.add_item( action = "play" , title = '[COLOR white]' + titulo + '[COLOR red] [MMS][/COLOR][I][COLOR lightgreen] (' + origen + ')[/COLOR][/I]' , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                            data = file.readline()
                            i = i + 1
                            continue
                        else:                            
                            plugintools.add_item( action = "play" , title = '[COLOR white]' + title + '[COLOR red] [MMS][/COLOR]' , plot = plot , url = url ,  thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                            data = file.readline()
                            i = i + 1
                            continue                      

                if data.startswith("plugin") == True:
                    if cat != "":
                        title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title
                    plugin_analyzer(data, title, plot, datamovie, thumbnail, fanart, show)
                    data = file.readline()
                    i = i + 1
                    continue    

                elif data.startswith("magnet") == True:
                    if cat != "":
                        if busqueda == 'search.txt':
                            url = urllib.quote_plus(data)
                            title = parser_title(title)
                            url = launch_magnet(url)
                            plugintools.add_item( action = "play" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR orangered] [Magnet][/COLOR][I][COLOR lightblue] (' + origen + ')[/COLOR][/I]', url = url , thumbnail = thumbnail , fanart = fanart , show = show, folder = False , isPlayable = True )
                            data = file.readline()
                            i = i + 1
                            continue
                        else:
                            data = data.strip()
                            url = urllib.quote_plus(data).strip()                      
                            title = parser_title(title)
                            url = launch_magnet(url)
                            plugintools.add_item( action = "play" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + ' [COLOR orangered][Magnet][/COLOR]', url = url , thumbnail = thumbnail , fanart = fanart , show = show, folder = False , isPlayable = True )
                            data = file.readline()
                            i = i + 1
                            continue
                    else:
                        if busqueda == 'search.txt':
                            url = urllib.quote_plus(data)
                            url = launch_magnet(url)
                            title = parser_title(title)
                            plugintools.add_item( action = "play" , title = '[COLOR white]' + title + '[COLOR orangered] [Magnet][/COLOR][I][COLOR lightblue] (' + origen + ')[/COLOR][/I]', url = url , thumbnail = thumbnail , fanart = fanart , show = show, folder = False , isPlayable = True )
                            data = file.readline()
                            i = i + 1
                            continue
                        else:
                            title = parser_title(title)
                            data = data.strip()
                            url = urllib.quote_plus(data)
                            url = launch_magnet(url)
                            plugintools.add_item( action = "play" , title = '[COLOR white]' + title + ' [COLOR orangered][Magnet][/COLOR]', url = url , thumbnail = thumbnail , fanart = fanart , show = show, folder = False , isPlayable = True )
                            data = file.readline()
                            i = i + 1
                            continue

                elif data.startswith("torrent") == True:  # Torrent file (URL)
                    url = data.replace("torrent:", "").strip()
                    if cat != "":
                        data = data.strip()
                        title = parser_title(title)
                        url = launch_torrent(url)
                        plugintools.add_item( action = "play" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + ' [COLOR orangered][Torrent][/COLOR]', url = url , thumbnail = thumbnail , fanart = fanart , show = show, folder = False , isPlayable = True )
                        data = file.readline()
                        i = i + 1
                        continue
                    else:
                        title = parser_title(title)
                        data = data.strip()                            
                        url = launch_torrent(url)
                        plugintools.add_item( action = "play" , title = '[COLOR white]' + title + ' [COLOR orangered][Torrent][/COLOR]', url = url , thumbnail = thumbnail , fanart = fanart , show = show, folder = False , isPlayable = True )
                        data = file.readline()
                        i = i + 1
                        continue                        
                        
                elif data.startswith("sop") == True:
                    title = title.split('"')
                    title = title[0]
                    title = title.replace("#EXTINF:-1,", "")
                    if cat != "":
                        if filtros_on == "true" and params.get("extra") == "1":
                            print 'Ejecutamos filtro... '
                            params["title"]=title
                            params["thumbnail"]=thumbnail
                            params["fanart"]=fanart
                            title = filtros0(params, datamovie);plugintools.modo_vista(show)
                            url = url.strip()
                            title_fixed=parser_title(title);title_fixed=title_fixed.replace(" ", "+").strip()
                            url = p2p_builder_url(data, title_fixed, p2p="sop")
                            if title != "":
                                plugintools.add_item( action = "play" , title = '[COLOR white]' + title + ' [COLOR darkorange][Sopcast][/COLOR]', plot = plot , url = url , extra="1", thumbnail = thumbnail , fanart = fanart , show = show, folder = False , isPlayable = True )
                                data = file.readline()
                                data = data.strip()
                                i = i + 1
                                continue
                        else:
                            title = parser_title(title)
                            title_fixed=parser_title(title);title_fixed=title_fixed.replace(" ", "+").strip()
                            url = p2p_builder_url(data, title_fixed, p2p="sop")
                            plugintools.add_item( action = "play" , title = '[COLOR white] ' + title + ' [COLOR darkorange][Sopcast][/COLOR]', plot = plot , url = url , thumbnail = thumbnail , fanart = fanart , show = show, folder = False , isPlayable = True )
                            data = file.readline()
                            i = i + 1
                            continue
                    else:
                        if filtros_on == "true" and params.get("extra") == "1":
                            print 'Ejecutamos filtro... '
                            params["title"]=title
                            params["thumbnail"]=thumbnail
                            params["fanart"]=fanart
                            title = filtros0(params, datamovie);plugintools.modo_vista(show)
                            url = url.strip()                            
                            title_fixed=parser_title(title);title_fixed=title_fixed.replace(" ", "+").strip()
                            url = p2p_builder_url(url, title_fixed, p2p="sop")
                            if title != "":
                                plugintools.add_item( action = "play" , title = '[COLOR white]' + title + ' [COLOR darkorange][Sopcast][/COLOR]', plot = plot , url = url , extra="1", thumbnail = thumbnail , fanart = fanart , show = show, folder = False , isPlayable = True )
                                data = file.readline()
                                data = data.strip()
                                i = i + 1
                                continue                                  
                        else:
                            title = parser_title(title)
                            url = url.strip()
                            title_fixed=title.replace(" ", "+").strip()
                            title_fixed=parser_title(title);title_fixed=title_fixed.replace(" ", "+").strip()
                            url = p2p_builder_url(url, title_fixed, p2p="sop")
                            plugintools.add_item(action="play" , title = '[COLOR white]' + title + ' [COLOR darkorange][Sopcast][/COLOR]' , plot = plot , url = url, thumbnail = thumbnail , fanart = fanart , show = show, folder = False , isPlayable = True)
                            data = file.readline()
                            data = data.strip()
                            i = i + 1
                            continue                       

                elif data.startswith("ace") == True:
                    if cat != "":
                        title = parser_title(title)
                        print 'data',data
                        url = data.replace("ace:", "").strip()
                        title_fixed=parser_title(title);title_fixed=title_fixed.replace(" ", "+").strip()
                        url = p2p_builder_url(url, title_fixed, p2p="ace")
                        plugintools.add_item(action="play" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + ' [COLOR lightblue][Acestream][/COLOR]' , plot = plot , url = url, thumbnail = thumbnail , fanart = fanart , show = show, folder = False , isPlayable = True)
                        data = file.readline()
                        data = data.strip()
                        i = i + 1
                        continue
                    else:
                        if filtros_on == "true" and params.get("extra") == "1":
                            print 'Ejecutamos filtro... '
                            params["title"]=title
                            params["thumbnail"]=thumbnail
                            params["fanart"]=fanart
                            title = filtros0(params, datamovie);plugintools.modo_vista(show)
                            url = data.replace("ace:", "").strip()
                            title_fixed=parser_title(title);title_fixed=title_fixed.replace(" ", "+").strip()
                            url = p2p_builder_url(url, title_fixed, p2p="ace")
                            if title != "":
                                plugintools.add_item(action="play" , title = '[COLOR white]' + title + ' [COLOR lightblue][Acestream][/COLOR]' , plot = plot , url = url, extra="1" , thumbnail = thumbnail , fanart = fanart , show = show, folder = False , isPlayable = True)
                                data = file.readline()
                                data = data.strip()
                                i = i + 1
                                continue                                  
                        else:
                            title = parser_title(title)
                            print 'data',data
                            url = data.replace("ace:", "")
                            url = url.strip()
                            title_fixed=parser_title(title);title_fixed=title_fixed.replace(" ", "+").strip()
                            url = p2p_builder_url(url, title_fixed, p2p="ace")
                            plugintools.add_item(action="play" , title = '[COLOR white]' + title + ' [COLOR lightblue][Acestream][/COLOR]' , plot = plot , url = url, thumbnail = thumbnail , fanart = fanart , show = show, folder = False , isPlayable = True)
                            data = file.readline()
                            data = data.strip()
                            i = i + 1
                            continue                        
                
                # Youtube playlist & channel    
                
                elif data.startswith("yt_playlist") == True:
                    title = title.split('"')
                    title = title[0]
                    title = title.replace("#EXTINF:-1,", "")
                    plugintools.log("title= "+title)
                    pid = data.replace("yt_playlist(", "")
                    pid = pid.replace(")", "").strip()
                    pid = pid+'/';pid=pid.strip();pid.replace(" ", "")                            
                    plugintools.log("pid= "+pid)                    
                    url = 'plugin://plugin.video.youtube/playlist/'+pid
                    url = url.strip().replace(" ", "")
                    plugintools.add_item( action = "runPlugin" , title = '[COLOR white]' + title + ' [COLOR red][You[COLOR white]Tube Playlist][/COLOR]', url = url ,  thumbnail = thumbnail , fanart = fanart , show = show, folder = True , isPlayable = False )
                    data = file.readline()
                    i = i + 1
                    continue                   

                elif data.startswith("yt_channel") == True:  # (UID = User ID), CID = Channel ID) .- Dejamos por defecto canales por UID
                    title = title.split('"')
                    title = title[0]
                    title = title.replace("#EXTINF:-1,", "")
                    uid = data.replace("yt_channel(", "")
                    uid = uid.replace(")", "").strip()
                    uid = uid+'/';uid=uid.strip();uid.replace(" ", "")
                    url = 'plugin://plugin.video.youtube/user/'+uid
                    url = url.strip().replace(" ", "")                             
                    plugintools.add_item( action = "runPlugin" , title = '[COLOR white]' + title + ' [COLOR red][You[COLOR white]Tube Channel][/COLOR]', url = url ,  thumbnail = thumbnail , fanart = fanart , show = show, folder = True , isPlayable = False )
                    data = file.readline()
                    i = i + 1
                    continue
                        
                elif data.startswith("m3u") == True:
                    if busqueda == 'search.txt':
                        url = data.replace("m3u:", "")
                        data = file.readline()
                        if data.startswith("desc=") == True:
                            plot = data.replace("desc=", "")                            
                        else:
                            plot = ""
                        plugintools.add_item( action = "getfile_http" , title = title + ' [I][COLOR lightblue](' + origen + ')[/I][/COLOR]', url = url ,  thumbnail = thumbnail , fanart = fanart , show = show, folder = True , isPlayable = False )
                        data = file.readline()
                        i = i + 1
                        continue
                    else:
                        url = data.replace("m3u:", "")
                        data = file.readline()
                        if data.startswith("desc=") == True:
                            data = data.replace("desc=", "")
                            data = data.replace('"', "")
                            datamovie = {}
                            datamovie["Plot"] = data
                            plugintools.log("SHOW= "+show)
                            if plugintools.get_setting("nolabel") == "true":
                                plugintools.add_item( action = "getfile_http" , title = title, info_labels = datamovie , url = url ,  thumbnail = thumbnail , fanart = fanart , show = show, folder = True , isPlayable = False )
                            else:
                                plugintools.add_item( action = "getfile_http" , title = title + ' [COLOR orange][Lista [B]M3U[/B]][/COLOR]', info_labels = datamovie , url = url , thumbnail = thumbnail , fanart = fanart , show = show, folder = True , isPlayable = False )
                            data = file.readline()
                            i = i + 1
                            continue
                        else:
                            plugintools.log("SHOW= "+show)
                            if plugintools.get_setting("nolabel") == "true":
                                plugintools.add_item( action = "getfile_http" , title = title, url = url ,  thumbnail = thumbnail , fanart = fanart , show = show, folder = True , isPlayable = False )
                            else:
                                plugintools.add_item( action = "getfile_http" , title = title + ' [COLOR orange][Lista [B]M3U[/B]][/COLOR]', url = url ,  thumbnail = thumbnail , fanart = fanart , show = show, folder = True , isPlayable = False )                                                
                            i = i + 1
                            continue

                elif data.startswith("plx") == True:
                    if busqueda == 'search.txt':
                        url = data.replace("plx:", "")
                        # Se añade parámetro plot porque en las listas PLX no tengo en una función separada la descarga (FIX IT!)
                        plugintools.add_item( action = "plx_items" , plot = "" , title = title + ' [I][/COLOR][COLOR lightblue](' + origen + ')[/I][/COLOR]', url = url ,  thumbnail = thumbnail , fanart = fanart , show = show, folder = True , isPlayable = False )
                        data = file.readline()
                        i = i + 1
                        continue
                    else:
                        url = data.replace("plx:", "")
                        # Se añade parámetro plot porque en las listas PLX no tengo en una función separada la descarga (FIX IT!)                        
                        plugintools.add_item( action = "plx_items" , plot = "" , title = title + ' [COLOR orange][Lista [B]PLX[/B]][/COLOR]', url = url ,  thumbnail = thumbnail , fanart = fanart , show = show, folder = True , isPlayable = False )
                        data = file.readline()
                        i = i + 1
                        continue

                elif data.startswith("goear") == True:
                    if busqueda == 'search.txt':
                        plugintools.add_item( action = "goear" , title = title + ' [I][/COLOR][COLOR lightblue](' + origen + ')[/I][/COLOR]', url = url ,  thumbnail = thumbnail , fanart = fanart , show = show, extra = show , folder = True , isPlayable = False )
                        data = file.readline()
                        i = i + 1
                        continue
                    else:
                        data = file.readline()
                        if show == "list":
                            show = plugintools.get_setting("music_id")
                            plugintools.log("show en config")                        
                        if data.startswith("desc") == True:
                            datamovie["Plot"] = data.replace("desc=", "").replace('"',"").strip()                            
                        plugintools.add_item( action = "goear" , plot = plot , title = title + ' [COLOR blue][goear][/COLOR]', url = url , info_labels = datamovie , thumbnail = thumbnail , fanart = fanart , show = show, extra = show , folder = True , isPlayable = False )
                        data = file.readline()
                        i = i + 1
                        continue                    
                    
                
            else:
                data = file.readline()
                i = i + 1
                continue

        else:
            data = file.readline()
            i = i + 1
            
    
    file.close()
    plugintools.modo_vista(show)
    if title == 'search.txt':
            os.remove(__temp__ + title)

    # Control para EPG de Fórmula TV (elimina archivo backup)
    try:
        if os.path.exists(tmp + 'backup_ftv.txt'):
            os.remove(tmp + 'backup_ftv.txt')
    except: pass

    if plugintools.get_setting("fpa_on"):
        show = plugintools.get_setting("pelis_view")
        plugintools.modo_vista(show)
    


def myplaylists_m3u(params):  # Mis listas M3U
    plugintools.log('[%s %s].myplaylist_m3u %s' % (addonName, addonVersion, repr(params)))
    thumbnail = params.get("thumbnail")
    plugintools.add_item(action="my_albums" , title = "[COLOR gold][B]Mis álbumes[/B][/COLOR][COLOR lightblue][I] (CBR/CBZ)[/I][/COLOR]" , thumbnail = __art__ + "search.png" , fanart = __art__ + 'fanart.jpg' , folder = True , isPlayable = False )
    plugintools.add_item(action="search_channel" , title = "[COLOR lightyellow]Buscador[/COLOR]" , thumbnail = __art__ + "search.png" , fanart = __art__ + 'fanart.jpg' , folder = True , isPlayable = False )
    plugintools.add_item(action="url_tester" , title = "[COLOR lightyellow]Probar URL![/COLOR]" , thumbnail = __art__ + "logo.png" , fanart ='http://4.bp.blogspot.com/-XHrjQMGVG_k/UNIj-CQSCfI/AAAAAAAAAhk/xdcoPKssrXs/s1600/LiveStreaming_Banner.jpg' , folder = True , isPlayable = False )

    # Agregamos listas online privadas del usuario
    add_playlist(params)

    ficheros = os.listdir(__playlists__)  # Lectura de archivos en carpeta /playlists. Cuidado con las barras inclinadas en Windows

    # Control paternal
    pekes_no = plugintools.get_setting("pekes_no")

    for entry in ficheros:
        plot = entry.split(".")
        plot = plot[0]
        plugintools.log("entry= "+entry)

        if pekes_no == "true" :
            print "Control paternal en marcha"
            if entry.find("XXX") >= 0 :
                plugintools.log("Activando control paternal...")

            else:
                if entry.endswith("plx") == True:  # Control para según qué extensión del archivo se elija thumbnail y función a ejecutar
                    entry = entry.replace(".plx", "")
                    plugintools.add_item(action="plx_items" , plot = plot , title = '[COLOR white]' + entry + '[/COLOR][COLOR green][B][I].plx[/I][/B][/COLOR]' , url = __playlists__ + entry , thumbnail = __art__ + 'plx3.png' , fanart = __art__ + 'fanart.jpg' , folder = True , isPlayable = False )

                elif entry.endswith("p2p") == True:
                    entry = entry.replace(".p2p", "")
                    plugintools.add_item(action="p2p_items" , plot = plot , title = '[COLOR white]' + entry + '[COLOR blue][B][I].p2p[/I][/B][/COLOR]', url = __playlists__ + entry , thumbnail = __art__ + 'p2p.png' , fanart = __art__ + 'fanart.jpg' , folder = True , isPlayable = False )

                elif entry.endswith("m3u") == True:
                    entry = entry.replace(".m3u", "")
                    plugintools.add_item(action="simpletv_items" , plot = plot , title = '[COLOR white]' + entry + '[COLOR red][B][I].m3u[/I][/B][/COLOR]', url = __playlists__ + entry , thumbnail = __art__ + 'm3u7.png' , fanart = __art__ + 'fanart.jpg' , folder = True , isPlayable = False )

                elif entry.endswith("jsn") == True:
                    entry = entry.replace(".jsn", "")
                    plugintools.add_item(action="json_items" , plot = plot , title = '[COLOR white]' + entry + '[COLOR yellow][B][I].jsn[/I][/B][/COLOR]', url = __playlists__ + entry , thumbnail = __art__ + 'm3u7.png' , fanart = __art__ + 'fanart.jpg' , folder = True , isPlayable = False )

        else:

                if entry.endswith("plx") == True:  # Control para según qué extensión del archivo se elija thumbnail y función a ejecutar
                    entry = entry.replace(".plx", "")
                    plugintools.add_item(action="plx_items" , plot = plot , title = '[COLOR white]' + entry + '[/COLOR][COLOR green][B][I].plx[/I][/B][/COLOR]' , url = __playlists__ + entry , thumbnail = __art__ + 'plx3.png' , fanart = __art__ + 'fanart.jpg' , folder = True , isPlayable = False )

                elif entry.endswith("p2p") == True:
                    entry = entry.replace(".p2p", "")
                    plugintools.add_item(action="p2p_items" , plot = plot , title = '[COLOR white]' + entry + '[COLOR blue][B][I].p2p[/I][/B][/COLOR]', url = __playlists__ + entry , thumbnail = __art__ + 'p2p.png' , fanart = __art__ + 'fanart.jpg' , folder = True , isPlayable = False )

                elif entry.endswith("m3u") == True:
                    entry = entry.replace(".m3u", "")
                    plugintools.add_item(action="simpletv_items" , plot = plot , title = '[COLOR white]' + entry + '[COLOR red][B][I].m3u[/I][/B][/COLOR]', url = __playlists__ + entry , thumbnail = __art__ + 'm3u7.png' , fanart = __art__ + 'fanart.jpg' , folder = True , isPlayable = False )

                elif entry.endswith("jsn") == True:
                    entry = entry.replace(".jsn", "")
                    plugintools.add_item(action="json_items" , plot = plot , title = '[COLOR white]' + entry + '[COLOR yellow][B][I].jsn[/I][/B][/COLOR]', url = __playlists__ + entry , thumbnail = __art__ + 'm3u7.png' , fanart = __art__ + 'fanart.jpg' , folder = True , isPlayable = False )


def my_albums(params):  # Mis listas M3U
    plugintools.log('[%s %s].my_albums %s' % (addonName, addonVersion, repr(params)))
    thumbnail = params.get("thumbnail")

    plugintools.add_item(action="" , title = "[COLOR gold][B]Mis álbumes[/B][/COLOR][COLOR lightblue][I] (CBR/CBZ)[/I][/COLOR]" , thumbnail = __art__ + "albums_icon.png" , fanart = __art__ + 'my_albums.jpg' , folder = False , isPlayable = False )
    ficheros = os.listdir(__temp__)  # Lectura de archivos en carpeta /__temp__. Cuidado con las barras inclinadas en Windows

    # Control paternal
    pekes_no = plugintools.get_setting("pekes_no")

    for entry in ficheros:
        plot = entry.split(".")
        plot = plot[0]
        plugintools.log("entry= "+entry)

        if pekes_no == "true" :
            print "Control paternal en marcha"
            if entry.find("XXX") >= 0 :
                plugintools.log("Activando control paternal...")

            else:
                if entry.endswith("cbr") == True:  # Control para según qué extensión del archivo se elija thumbnail y función a ejecutar
                    entry = entry.replace(".cbr", "")
                    plugintools.add_item(action="cbx_reader" , plot = plot , title = '[COLOR white]' + entry + '[/COLOR][COLOR green][B][I].cbr[/I][/B][/COLOR]' , extra = "my_albums", url = __playlists__ + entry , thumbnail = __art__+'cbr.png' , fanart = __art__ + 'my_albums.jpg' , folder = True , isPlayable = False )

                elif entry.endswith("cbz") == True:
                    entry = entry.replace(".cbz", "")
                    plugintools.add_item(action="cbx_reader" , plot = plot , title = '[COLOR white]' + entry + '[COLOR blue][B][I].cbz[/I][/B][/COLOR]', extra = "my_albums" , url = __playlists__ + entry , thumbnail = __art__+'cbz.png' , fanart = __art__ + 'my_albums.jpg' , folder = True , isPlayable = False )

        else:

                if entry.endswith("cbr") == True:  # Control para según qué extensión del archivo se elija thumbnail y función a ejecutar
                    entry = entry.replace(".cbr", "")
                    plugintools.add_item(action="cbx_reader" , plot = plot , title = '[COLOR white]' + entry + '[/COLOR][COLOR green][B][I].cbr[/I][/B][/COLOR]' , extra = "my_albums" , url = __playlists__ + entry , thumbnail = __art__+'cbr.png' , fanart = __art__ + 'my_albums.jpg' , folder = True , isPlayable = False )

                elif entry.endswith("cbz") == True:
                    entry = entry.replace(".cbz", "")
                    plugintools.add_item(action="cbx_reader" , plot = plot , title = '[COLOR white]' + entry + '[COLOR blue][B][I].cbz[/I][/B][/COLOR]', extra = "my_albums" , url = __playlists__ + entry , thumbnail = __art__+'cbz.png' , fanart = __art__ + 'my_albums.jpg' , folder = True , isPlayable = False )



def playlists_m3u(params):  # Biblioteca online
    plugintools.log('[%s %s].playlist_m3u %s' % (addonName, addonVersion, repr(params)))

    data = plugintools.read( params.get("url") )
    name_channel = params.get("plot")
    pattern = '<name>'+name_channel+'(.*?)</channel>'
    data = plugintools.find_single_match(data, pattern)
    online = '[COLOR yellowgreen][I][Auto][/I][/COLOR]'
    params["ext"] = 'm3u'
    plugintools.add_item( action="" , title='[B][COLOR yellow]'+name_channel+'[/B][/COLOR] - [B][I][COLOR lightyellow]juarrox@gmail.com [/COLOR][/B][/I]' , thumbnail= __art__ + 'icon.png' , folder = False , isPlayable = False )
    subchannel = re.compile('<subchannel>([^<]+)<name>([^<]+)</name>([^<]+)<thumbnail>([^<]+)</thumbnail>([^<]+)<url>([^<]+)</url>([^<]+)</subchannel>').findall(data)
    # Sustituir por una lista!!!
    for biny, ciny, diny, winy, pixy, dixy, boxy in subchannel:
        if ciny == "Vcx7 IPTV":
            plugintools.add_item( action="getfile_http" , plot = ciny , title = '[COLOR lightyellow]' + ciny + '[/COLOR] ' + online , url= dixy , thumbnail = __art__ + winy , fanart = __art__ + 'fanart.jpg' , folder = True , isPlayable = False )
            params["ext"] = "m3u"
            title = ciny
            params["title"]=title
        elif ciny == "Largo Barbate M3U":
            plugintools.add_item( action="getfile_http" , plot = ciny , title = '[COLOR lightyellow]' + ciny + '[/COLOR] ' + online , url= dixy , thumbnail = __art__ + winy , fanart = __art__ + 'fanart.jpg' , folder = True , isPlayable = False )
            title = ciny
            params["title"]=title
        elif ciny == "XBMC Mexico":
            plugintools.add_item( action="getfile_http" , plot = ciny , title = '[COLOR lightyellow]' + ciny + '[/COLOR] ' + online , url= dixy , thumbnail = __art__ + winy , fanart = __art__ + 'fanart.jpg' , folder = True , isPlayable = False )
            title = ciny
            params["title"]=title
        elif ciny == "allSat":
            plugintools.add_item( action="getfile_http" , plot = ciny , title = '[COLOR lightyellow]' + ciny + '[/COLOR] ' + online , url= dixy , thumbnail = __art__ + winy , fanart = __art__ + 'fanart.jpg' , folder = True , isPlayable = False )
            title = ciny
            params["title"]=title
        elif ciny == "AND Wonder":
            plugintools.add_item( action="getfile_http" , plot = ciny , title = '[COLOR lightyellow]' + ciny + '[/COLOR] ' + online , url= dixy , thumbnail = __art__ + winy , fanart = __art__ + 'fanart.jpg' , folder = True , isPlayable = False )
            title = ciny
            params["title"]=title
        elif ciny == "FenixTV":
            plugintools.add_item( action="getfile_http" , plot = ciny , title = '[COLOR lightyellow]' + ciny + '[/COLOR] ' + online , url= dixy , thumbnail = __art__ + winy , fanart = __art__ + 'fanart.jpg' , folder = True , isPlayable = False )
            title = ciny
            params["title"]=title
        else:
            plot = ciny.split("[")
            plot = plot[0]
            plugintools.add_item( action="getfile_http" , plot = plot , title = '[COLOR lightyellow]' + ciny + '[/COLOR] ' , url= dixy , thumbnail = __art__ + winy , fanart = __art__ + 'fanart.jpg' , folder = True , isPlayable = False )



    plugintools.log('[%s %s].playlist_m3u %s' % (addonName, addonVersion, repr(params)))    



def getfile_http(params):  # Descarga de lista M3U + llamada a simpletv_items para que liste los items
    plugintools.log('[%s %s].getfile_http ' % (addonName, addonVersion))
    
    url = params.get("url")
    params["ext"] = "m3u"
    getfile_url(params)
    simpletv_items(params)

        


def parse_url(url):
    # plugintools.log("url entrante= "+url)

    if url != "":
        url = url.strip()
        url = url.replace("rtmp://$OPT:rtmp-raw=", "")
        return url

    else:
        plugintools.log("error en url= ")  # Mostrar diálogo de error al parsear url (por no existir, por ejemplo)



def getfile_url(params):
    plugintools.log('[%s %s].getfile_url ' % (addonName, addonVersion))
    ext = params.get("ext")
    title = params.get("title")

    if ext == 'plx':
        filename = parser_title(title)
        params["plot"]=filename
        filename = title + ".plx"  # El título del archivo con extensión (m3u, p2p, plx)
    elif ext == 'm3u':
        filename = params.get("plot")
        # Vamos a quitar el formato al texto para que sea el nombre del archivo
        filename = parser_title(title)
        filename = filename + ".m3u"  # El título del archivo con extensión (m3u, p2p, plx)
    else:
        ext == 'p2p'
        filename = parser_title(title)
        filename = filename + ".p2p"  # El título del archivo con extensión (m3u, p2p, plx)

    if filename.endswith("plx") == True :
        filename = parser_title(filename)

    plugintools.log("filename= "+filename)
    url = params.get("url")
    plugintools.log("url= "+url)

    try:
        response = urllib2.urlopen(url)
        body = response.read()
    except:
        # Control si la lista está en el cuerpo del HTTP
        request_headers=[]
        request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
        body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)

    #open the file for writing
    fh = open(__playlists__ + filename, "wb")

    # read from request while writing to file
    fh.write(body)

    fh.close()

    file = open(__playlists__ + filename, "r")
    file.seek(0)
    data = file.readline()
    data = data.strip()

    lista_items = {'linea': data}
    file.seek(0)
    lista_items = {'plot': data}
    file.seek(0)



def header_xml(params):
    plugintools.log('[%s %s].header_xml %s' % (addonName, addonVersion, repr(params)))

    url = params.get("url")
    params.get("title")
    data = plugintools.read(url)
    # plugintools.log("data= "+data)
    author = plugintools.find_single_match(data, '<poster>(.*?)</poster>')
    author = author.strip()
    fanart = plugintools.find_single_match(data, '<fanart>(.*?)</fanart>')
    message = plugintools.find_single_match(data, '<message>(.*?)</message>')
    desc = plugintools.find_single_match(data, '<description>(.*?)</description>')
    thumbnail = plugintools.find_single_match(data, '<thumbnail>(.*?)</thumbnail>')

    if author != "":
        if message != "":
            plugintools.add_item(action="" , plot = author , title = '[COLOR green][B]' + author + '[/B][/COLOR][I] ' + message + '[/I]', url = "" , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = False )
            return fanart
        else:
            plugintools.add_item(action="" , plot = author , title = '[COLOR green][B]' + author + '[/B][/COLOR]', url = "" , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = False )
            return fanart
    else:
        if desc != "":
            plugintools.add_item(action="" , plot = author , title = '[COLOR green][B]' + desc + '[/B][/COLOR]', url = "" , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = False )
            return fanart
        else:
            return fanart


def search_channel(params):
    plugintools.log('[%s %s].search_channel %s' % (addonName, addonVersion, repr(params)))

    buscar = params.get("plot")
    if buscar == "":
        last_search = plugintools.get_setting("last_search")
        texto = plugintools.keyboard_input(last_search)
        plugintools.set_setting("last_search",texto)
        params["texto"]=texto
        texto = texto.lower()
        cat = ""
        if texto == "":
            errormsg = plugintools.message("pld.visiontv","Por favor, introduzca el canal a buscar")
            return errormsg

    else:
        texto = buscar
        texto = texto.lower()
        plugintools.log("texto a buscar= "+texto)
        cat = ""

    results = open(__temp__ + 'search.txt', "wb")
    results.seek(0)
    results.close()

    # Listamos archivos de la biblioteca local
    ficheros = os.listdir(__playlists__)  # Lectura de archivos en carpeta /playlists. Cuidado con las barras inclinadas en Windows

    for entry in ficheros:
        if entry.endswith("m3u") == True:
            print "Archivo tipo m3u"
            plot = entry.split(".")
            plot = plot[0]  # plot es la variable que recoge el nombre del archivo (sin extensión txt)
            # Abrimos el primer archivo
            filename = plot + '.m3u'
            plugintools.log("Archivo M3U: "+filename)
            arch = open(__playlists__ + filename, "r")
            num_items = len(arch.readlines())
            print num_items
            i = 0  # Controlamos que no se salga del bucle while antes de que lea el último registro de la lista
            arch.seek(0)
            data = arch.readline()
            data = data.strip()
            plugintools.log("data linea= "+data)
            texto = texto.strip()
            plugintools.log("data_antes= "+data)
            plugintools.log("texto a buscar= "+texto)

            data = arch.readline()
            data = data.strip()
            i = i + 1
            while i <= num_items :
                if data.startswith('#EXTINF:-1') == True:
                    data = data.replace('#EXTINF:-1,', "")  # Ignoramos la primera parte de la línea
                    data = data.replace(",", "")
                    title = data.strip()  # Ya tenemos el título

                    if data.find('$ExtFilter="') >= 0:
                        data = data.replace('$ExtFilter="', "")

                    if data.find(' $ExtFilter="') >= 0:
                        data = data.replace('$ExtFilter="', "")

                    title = title.replace("-AZBOX*", "")
                    title = title.replace("AZBOX *", "")

                    images = m3u_items(title)
                    plugintools.modo_vista(show)  # Para no perder el modo de vista predefinido tras llamar a la función m3u_items
                    #print 'images',images
                    thumbnail = images[0]
                    fanart = images[1]
                    cat = images[2]
                    title = images[3]
                    #plugintools.log("title= "+title)
                    minus = title.lower()
                    data = arch.readline()
                    data = data.strip()
                    i = i + 1

                    if minus.find(texto) >= 0:
                    # if re.match(texto, title, re.IGNORECASE):
                        # plugintools.log("Concidencia hallada. Obtenemos url del canal: " + texto)
                        if data.startswith("http") == True:
                            url = data.strip()
                            if cat != "":  # Controlamos el caso de subcategoría de canales
                                results = open(__temp__ + 'search.txt', "a")
                                results.write("#EXTINF:-1," + title + '"' + filename + '\n')
                                results.write(url + '\n\n')
                                results.close()
                                data = arch.readline()
                                i = i + 1
                                continue
                            else:
                                results = open(__temp__ + 'search.txt', "a")
                                results.write("#EXTINF:-1," + title + '"' + filename + '\n')
                                results.write(url + '\n\n')
                                results.close()
                                data = arch.readline()
                                i = i + 1
                                continue
                        if data.startswith("rtmp") == True:
                            url = data
                            url = parse_url(url)
                            if cat != "":   # Controlamos el caso de subcategoría de canales
                                results = open(__temp__ + 'search.txt', "a")
                                results.write("#EXTINF:-1," + title + '"' + filename + '\n')
                                results.write(url + '\n\n')
                                results.close()
                                data = arch.readline()
                                i = i + 1
                                continue
                            else:
                                results = open(__temp__ + 'search.txt', "a")
                                results.write("#EXTINF:-1," + title + '"' + filename + '\n')
                                results.write(url + '\n\n')
                                results.close()
                                data = arch.readline()
                                i = i + 1
                                continue
                        if data.startswith("yt") == True:
                            print "CORRECTO"
                            url = data
                            results = open(__temp__ + 'search.txt', "a")
                            results.write("#EXTINF:-1," + title + '"' + filename + '\n')
                            results.write(url + '\n\n')
                            results.close()
                            data = arch.readline()
                            i = i + 1
                            continue


                else:
                    data = arch.readline()
                    data = data.strip()
                    plugintools.log("data_buscando_title= "+data)
                    i = i + 1

            else:
                data = arch.readline()
                data = data.strip()
                plugintools.log("data_final_while= "+data)
                i = i + 1
                continue



    # Listamos archivos de la biblioteca local
    ficheros = os.listdir(__playlists__)  # Lectura de archivos en carpeta /playlist. Cuidado con las barras inclinadas en Windows

    for entry in ficheros:
        if entry.endswith('p2p') == True:
            plot = entry.split(".")
            plot = plot[0]  # plot es la variable que recoge el nombre del archivo (sin extensión txt)
            # Abrimos el primer archivo
            plugintools.log("texto a buscar= "+texto)
            filename = plot + '.p2p'
            arch = open(__playlists__ + filename, "r")
            num_items = len(arch.readlines())
            plugintools.log("archivo= "+filename)
            i = 0  # Controlamos que no se salga del bucle while antes de que lea el último registro de la lista
            arch.seek(0)
            while i <= num_items:
                data = arch.readline()
                data = data.strip()
                title = data
                texto = texto.strip()
                plugintools.log("linea a buscar title= "+data)
                i = i + 1

                if data.startswith("#") == True:
                    data = arch.readline()
                    data = data.strip()
                    i = i + 1
                    continue

                if data.startswith("default=") == True:
                    data = arch.readline()
                    data = data.strip()
                    i = i + 1
                    continue

                if data.startswith("__art__=") == True:
                    data = arch.readline()
                    data = data.strip()
                    i = i + 1
                    continue

                if data != "":
                    title = data.strip()  # Ya tenemos el título
                    plugintools.log("title= "+title)
                    minus = title.lower()
                    if minus.find(texto) >= 0:
                        plugintools.log("title= "+title)
                        data = arch.readline()
                        i = i + 1
                        #print i
                        plugintools.log("linea a comprobar url= "+data)
                        if data.startswith("sop") == True:
                            # plugin://plugin.video.p2p-streams/?url=sop://124.232.150.188:3912/11265&mode=2&name=Titulo+canal+Sopcast
                            title_fixed= urllib_quote_plus(title)
                            title_fixed=parser_title(title);title_fixed=title_fixed.replace(" ", "+").strip()
                            url=data.split(":3912/")[1];url=url.strip();url='sop://'+url
                            url = p2p_builder_url(url, title_fixed, p2p="sop")
                            results = open(__temp__ + 'search.txt', "a")
                            results.write("#EXTINF:-1," + title + '"' + filename + '\n')  # Hay que cambiar esto! No puede agregar #EXTINF:-1, si no es una lista m3u
                            results.write(url + '\n\n')
                            results.close()
                            data = arch.readline()
                            i = i + 1
                            continue

                        elif data.startswith("magnet") == True:
                            # magnet:?xt=urn:btih:6CE983D676F2643430B177E2430042E4E65427...
                            title_fixed = title.split('"')
                            title = title_fixed[0]
                            plugintools.log("title magnet= "+title)
                            url = data
                            plugintools.log("url magnet= "+url)
                            results = open(__temp__ + 'search.txt', "a")
                            results.write("#EXTINF:-1," + title + '"' + filename + '\n')
                            results.write(url + '\n\n')
                            results.close()
                            data = arch.readline()
                            i = i + 1
                            continue

                        elif data.find("://") == -1:
                            # plugin://plugin.video.p2p-streams/?url=a55f96dd386b7722380802b6afffc97ff98903ac&mode=1&name=Sky+Sports+title
                            title_fixed = title.split('"')
                            title = title_fixed[0]
                            title_fixed = title.replace(" " , "+")
                            url = p2p_builder_url(data, title_fixed, p2p="ace")
                            results = open(__temp__ + 'search.txt', "a")
                            results.write("#EXTINF:-1," + title + '"' + filename + '\n')  # Hay que cambiar esto! No puede agregar #EXTINF:-1, si no es una lista m3u
                            results.write(url + '\n\n')
                            results.close()
                            data = arch.readline()
                            i = i + 1
                            continue

                    else:
                        plugintools.log("no coinciden titulo y texto a buscar")


    for entry in ficheros:
        if entry.endswith('plx') == True:
            plot = entry.split(".")
            plot = plot[0]  # plot es la variable que recoge el nombre del archivo (sin extensión)
            # Abrimos el primer archivo
            plugintools.log("texto a buscar= "+texto)
            filename = plot + '.plx'
            plugintools.log("archivo PLX: "+filename)
            arch = open(__playlists__ + filename, "r")
            num_items = len(arch.readlines())
            print num_items
            i = 0
            arch.seek(0)
            while i <= num_items:
                data = arch.readline()
                data = data.strip()
                i = i + 1
                print i

                if data.startswith("#") == True:
                    continue

                if (data == 'type=video') or (data == 'type=audio') == True:
                    data = arch.readline()
                    i = i + 1
                    print i
                    data = data.replace("name=", "")
                    data = data.strip()
                    title = data
                    minus = title.lower()
                    if minus.find(texto) >= 0:
                        plugintools.log("Título coincidente= "+title)
                        data = arch.readline()
                        plugintools.log("Siguiente linea= "+data)
                        i = i + 1
                        print i
                        print "Analizamos..."
                        while data <> "" :
                            if data.startswith("thumb") == True:
                                data = arch.readline()
                                plugintools.log("data_plx= "+data)
                                i = i + 1
                                print i
                                continue

                            if data.startswith("date") == True:
                                data = arch.readline()
                                plugintools.log("data_plx= "+data)
                                i = i + 1
                                print i
                                continue

                            if data.startswith("background") == True:
                                data = arch.readline()
                                plugintools.log("data_plx= "+data)
                                i = i + 1
                                print i
                                continue

                            if data.startswith("URL") == True:
                                data = data.replace("URL=", "")
                                data = data.strip()
                                url = data
                                parse_url(url)
                                plugintools.log("URL= "+url)
                                results = open(__temp__ + 'search.txt', "a")
                                results.write("#EXTINF:-1," + title + '"' + filename + '\n')
                                results.write(url + '\n\n')
                                results.close()
                                data = arch.readline()
                                i = i + 1
                                break




    arch.close()
    results.close()
    params["plot"] = 'search'  # Pasamos a la lista de variables (params) el valor del archivo de resultados para que lo abra la función simpletv_items
    params['texto']= texto  # Agregamos al diccionario una nueva variable que contiene el texto a buscar
    simpletv_items(params)



def encode_string(url):


    d = {    '\xc1':'A',
            '\xc9':'E',
            '\xcd':'I',
            '\xd3':'O',
            '\xda':'U',
            '\xdc':'U',
            '\xd1':'N',
            '\xc7':'C',
            '\xed':'i',
            '\xf3':'o',
            '\xf1':'n',
            '\xe7':'c',
            '\xba':'',
            '\xb0':'',
            '\x3a':'',
            '\xe1':'a',
            '\xe2':'a',
            '\xe3':'a',
            '\xe4':'a',
            '\xe5':'a',
            '\xe8':'e',
            '\xe9':'e',
            '\xea':'e',
            '\xeb':'e',
            '\xec':'i',
            '\xed':'i',
            '\xee':'i',
            '\xef':'i',
            '\xf2':'o',
            '\xf3':'o',
            '\xf4':'o',
            '\xf5':'o',
            '\xf0':'o',
            '\xf9':'u',
            '\xfa':'u',
            '\xfb':'u',
            '\xfc':'u',
            '\xe5':'a'
    }

    nueva_cadena = url
    for c in d.keys():
        plugintools.log("caracter= "+c)
        nueva_cadena = nueva_cadena.replace(c,d[c])

    auxiliar = nueva_cadena.encode('utf-8')
    url = nueva_cadena
    return nueva_cadena



def plx_items(params):
    plugintools.log('[%s %s].plx_items %s' % (addonName, addonVersion, repr(params)))

    fanart = ""
    thumbnail = ""
    datamovie = {}
    show = "LIST"

    # Control para elegir el título (plot, si formateamos el título / title , si no existe plot)
    if params.get("plot") == "":
        title = params.get("title").strip() + '.plx'
        title = parser_title(title)
        title = title.strip()
        filename = title
        params["plot"]=filename
        params["ext"] = 'plx'
        getfile_url(params)
        title = params.get("title")
    else:
        title = params.get("plot")
        title = title.strip()
        title = parser_title(title)
        plugintools.log("Lectura del archivo PLX")

    title = title.replace(" .plx", ".plx")
    title = title.strip()
    file = open(__playlists__ + parser_title(title) + '.plx', "r")
    file.seek(0)
    num_items = len(file.readlines())
    print num_items
    file.seek(0)

    # Lectura del título y fanart de la lista
    background = __art__ + 'fanart.jpg'
    logo = __art__ + 'plx3.png'
    file.seek(0)
    data = file.readline()
    while data <> "":
        plugintools.log("data= "+data)
        if data.startswith("background=") == True:
            data = data.replace("background=", "")
            background = data.strip()
            plugintools.log("background= "+background)
            if background == "":
                background = params.get("extra")
                if background == "":
                    background = __art__ + 'fanart.jpg'

            data = file.readline()
            continue

        if data.startswith("title=") == True:
            name = data.replace("title=", "")
            name = name.strip()
            plugintools.log("name= "+name)
            if name == "Select sort order for this list":
                name = "Seleccione criterio para ordenar ésta lista... "
            data = file.readline()
            continue

        if data.startswith("logo=") == True:
            data = data.replace("logo=", "")
            logo = data.strip()
            plugintools.log("logo= "+logo)
            title = parser_title(title)
            if thumbnail == "":
                thumbnail = __art__ + 'plx3.png'

            plugintools.add_item(action="" , title = '[COLOR lightyellow][B][I]playlists / '+ title + '[/B][/I][/COLOR]', url = __playlists__ + title , thumbnail = logo , fanart = background , folder = False , isPlayable = False)
            plugintools.log("fanart= "+fanart)
            plugintools.add_item(action="" , title = '[I][B]' + name + '[/B][/I]' , url = "" , thumbnail = logo , fanart = background , folder = False , isPlayable = False)

            data = file.readline()
            break

        else:
            data = file.readline()


    try:
        data = file.readline()
        plugintools.log("data= "+data)
        if data.startswith("background=") == True:
            data = data.replace("background=", "")
            data = data.strip()
            fanart = data
            background = fanart
            plugintools.log("fanart= "+fanart)
        else:
            # data = file.readline()
            if data.startswith("background=") == True:
                print "Archivo plx!"
                data = data.replace("background=", "")
                fanart = data.strip()
                plugintools.log("fanart= "+fanart)
            else:
                if data.startswith("title=") == True:
                    name = data.replace("title=", "")
                    name = name.strip()
                    plugintools.log("name= "+name)
    except:
        plugintools.log("ERROR: Unable to load PLX file")


    data = file.readline()
    try:
        if data.startswith("title=") == True:
            data = data.replace("title=", "")
            name = data.strip()
            plugintools.log("title= "+title)
            plugintools.add_item(action="" , title = '[COLOR lightyellow][B][I]playlists / '+ title +'[/I][/B][/COLOR]' , url = __playlists__ + title , thumbnail = logo , fanart = fanart , folder = False , isPlayable = False)
            plugintools.add_item(action="" , title = '[I][B]' + name + '[/B][/I]' , url = "" , thumbnail = __art__ + "icon.png" , fanart = fanart , folder = False , isPlayable = False)
    except:
        plugintools.log("Unable to read PLX title")


    # Lectura de items

    i = 0
    file.seek(0)
    while i <= num_items:
        data = file.readline()
        data = data.strip()
        i = i + 1
        print i

        if data.startswith("#") == True:
            continue
        elif data.startswith("rating") == True:
            continue
        elif data.startswith("description") == True:
            continue

        if (data == 'type=comment') == True:
            data = file.readline()
            i = i + 1
            print i

            while data <> "" :
                if data.startswith("name") == True:
                    title = data.replace("name=", "")
                    data = file.readline()
                    data = data.strip()
                    i = i + 1
                    print i
                    continue

                elif data.startswith("thumb") == True:
                    data = data.replace("thumb=", "")
                    data = data.strip()
                    thumbnail = data
                    if thumbnail == "":
                        thumbnail = logo
                    data = file.readline()
                    data = data.strip()
                    i = i + 1
                    print i
                    continue

                elif data.startswith("background") == True:
                    data = data.replace("background=", "")
                    fanart = data.strip()
                    if fanart == "":
                        fanart = background
                    data = file.readline()
                    data = data.strip()
                    i = i + 1
                    print i
                    continue

            plugintools.add_item(action="", title = title , url = "", thumbnail = thumbnail , fanart = fanart , folder = False, isPlayable = False)

        if (data == 'type=video') or (data == 'type=audio') == True:
            data = file.readline()
            i = i + 1
            print i

            while data <> "" :
                if data.startswith("#") == True:
                    data = file.readline()
                    data = data.strip()
                    i = i + 1
                    print i
                    continue
                elif data.startswith("description") == True:
                    data = file.readline()
                    data = data.strip()
                    i = i + 1
                    print i
                    continue
                elif data.startswith("rating") == True:
                    data = file.readline()
                    data = data.strip()
                    i = i + 1
                    print i
                    continue
                elif data.startswith("name") == True:
                    data = data.replace("name=", "")
                    data = data.strip()
                    title = data
                    if title == "[COLOR=FF00FF00]by user-assigned order[/COLOR]" :
                        title = "Seleccione criterio para ordenar ésta lista... "

                    if title == "by user-assigned order" :
                        title = "Según se han agregado en la lista"

                    if title == "by date added, oldest first" :
                        title = "Por fecha de agregación, las más antiguas primero"

                    if title == "by date added, newest first" :
                        title = "Por fecha de agregación, las más nuevas primero"

                    data = file.readline()
                    data = data.strip()
                    i = i + 1
                    print i
                elif data.startswith("thumb") == True:
                    data = data.replace("thumb=", "")
                    data = data.strip()
                    thumbnail = data
                    if thumbnail == "":
                        thumbnail = logo
                    data = file.readline()
                    data = data.strip()
                    i = i + 1
                    print i
                    continue
                elif data.startswith("date") == True:
                    data = file.readline()
                    i = i + 1
                    print i
                    continue
                elif data.startswith("background") == True:
                    data = data.replace("background=", "")
                    fanart = data.strip()
                    if fanart == "":
                        fanart = background
                    data = file.readline()
                    data = data.strip()
                    i = i + 1
                    print i
                    continue

                elif data.startswith("URL") == True:
                    # Control para el caso de que no se haya definido fanart en cada entrada de la lista => Se usa el fanart general
                    if fanart == "":
                        fanart = background
                    data = data.replace("URL=", "")
                    data = data.strip()
                    url = data
                    parse_url(url)
                    if url.startswith("yt_channel") == True:
                        uid = url.replace("yt_channel", "")
                        uid = uid.replace(")", "").replace("(", "").strip()
                        uid = uid+'/';uid=uid.strip();uid.replace(" ", "")                            
                        url = 'plugin://plugin.video.youtube/user/'+uid
                        url = url.strip().replace(" ", "")
                        plugintools.log("url= "+url)                    
                        plugintools.add_item(action="runPlugin" , title = title + ' [[COLOR red]You[COLOR white]tube Channel][/COLOR]', extra = show, url = url , thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False)
                        break

                    elif url.startswith("yt_playlist") == True:
                        youtube_playlist = url.replace("yt_playlist(", "")
                        youtube_playlist = youtube_playlist.replace(")", "")
                        plugintools.log("youtube_playlist= "+youtube_playlist).strip()
                        pid = pid.replace(")", "").strip()
                        pid = pid+'/';pid=pid.strip();pid.replace(" ", "")
                        url = 'plugin://plugin.video.youtube/playlist/'+pid
                        plugintools.add_item( action = "runPlugin" , title = title + ' [COLOR red][You[COLOR white]tube Playlist][/COLOR] [I][COLOR lightblue][/I][/COLOR]', extra = show, url = url , thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )
                        plugintools.log("CONTROL Youtube")
                        data = file.readline()
                        i = i + 1
                        break

                    elif url.startswith("serie") == True:
                        url = url.replace("serie:", "")
                        plugintools.log("URL= "+url)
                        plugintools.log("FANART = "+fanart)
                        plugintools.add_item(action="seriecatcher" , title = title + ' [COLOR purple][Serie online][/COLOR]' , show = show, url = url , thumbnail = thumbnail , fanart = fanart , extra = fanart , folder = True , isPlayable = False)
                        break

                    elif url.startswith("goear") == True:
                        plugintools.add_item(action="goear" , title = title + ' [COLOR blue][goear][/COLOR]' , show = show, url = url , thumbnail = thumbnail , fanart = fanart , extra = fanart , folder = True , isPlayable = False)
                        break

                    elif url.startswith("http") == True:
                        if url.find("allmyvideos") >= 0:
                            plugintools.add_item(action="allmyvideos" , title = title + ' [COLOR lightyellow][Allmyvideos][/COLOR]' , extra = show, url = url , info_labels = datamovie , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True)
                            plugintools.log("URL= "+url)
                            break

                        elif url.find("streamcloud") >= 0:
                            plugintools.add_item(action="streamcloud" , title = title + ' [COLOR lightskyblue][Streamcloud][/COLOR]' , extra = show, url = url , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True)
                            plugintools.log("URL= "+url)
                            plugintools.log("FANART = "+fanart)
                            break

                        elif url.find("played.to") >= 0:
                            plugintools.add_item(action="playedto" , title = title + ' [COLOR lavender][Played.to][/COLOR]' , url = url , extra = show, thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True)
                            plugintools.log("URL= "+url)
                            plugintools.log("FANART = "+fanart)
                            break

                        elif url.find("vidspot") >= 0:
                            plugintools.add_item(action="vidspot" , title = title + ' [COLOR palegreen][Vidspot][/COLOR]' , url = url , extra = show, thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True)
                            plugintools.log("URL= "+url)
                            plugintools.log("FANART = "+fanart)
                            break

                        elif url.find("vk.com") >= 0:
                            plugintools.add_item(action="vk" , title = title + ' [COLOR royalblue][Vk][/COLOR]' , url = url , extra = show, thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True)
                            plugintools.log("URL= "+url)
                            plugintools.log("FANART = "+fanart)
                            break

                        elif url.find("nowvideo") >= 0:
                            plugintools.add_item(action="nowvideo" , title = title + ' [COLOR red][Nowvideo][/COLOR]' , url = url , extra = show, thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True)
                            plugintools.log("URL= "+url)
                            break

                        elif url.find("tumi.tv") >= 0:
                            plugintools.add_item(action="tumi" , title = title + ' [COLOR forestgreen][Tumi][/COLOR]' , url = url , extra = show, thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True)
                            plugintools.log("URL= "+url)
                            break

                        elif url.find("veehd.com") >= 0:
                            plugintools.add_item(action="veehd" , title = title + ' [COLOR orange][VeeHD][/COLOR]' , url = url , extra = show, thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True)
                            plugintools.log("URL= "+url)
                            break

                        elif url.find("streamin.to") >= 0:
                            plugintools.add_item(action="streaminto" , title = title + ' [COLOR orange][streamin.to][/COLOR]' , url = url , thumbnail = thumbnail , extra = show, fanart = fanart , folder = False , isPlayable = True)
                            plugintools.log("URL= "+url)
                            break

                        elif url.find("powvideo") >= 0:
                            plugintools.add_item(action="powvideo" , title = title + ' [COLOR orange][powvideo][/COLOR]' , url = url , thumbnail = thumbnail , extra = show, fanart = fanart , folder = False , isPlayable = True)
                            plugintools.log("URL= "+url)
                            break

                        elif url.find("mail.ru") >= 0:
                            plugintools.add_item(action="mailru" , title = title + ' [COLOR orange][Mail.ru][/COLOR]' , url = url , thumbnail = thumbnail , extra = show, fanart = fanart , folder = False , isPlayable = True)
                            plugintools.log("URL= "+url)
                            break

                        elif url.find("novamov") >= 0:
                            plugintools.add_item(action="novamov" , title = title + ' [COLOR orange][Novamov][/COLOR]' , url = url , thumbnail = thumbnail , extra = show, fanart = fanart , folder = False , isPlayable = True)
                            plugintools.log("URL= "+url)
                            break

                        elif url.find("gamovideo") >= 0:
                            plugintools.add_item(action="gamovideo" , title = title + ' [COLOR orange][Gamovideo][/COLOR]' , url = url , thumbnail = thumbnail , extra = show, fanart = fanart , folder = False , isPlayable = True)
                            plugintools.log("URL= "+url)
                            break

                        elif url.find("moevideos") >= 0:
                            plugintools.add_item(action="moevideos" , title = title + ' [COLOR orange][Moevideos][/COLOR]' , url = url , thumbnail = thumbnail , extra = show, fanart = fanart , folder = False , isPlayable = True)
                            plugintools.log("URL= "+url)
                            break

                        elif url.find("movshare") >= 0:
                            plugintools.add_item(action="movshare" , title = title + ' [COLOR orange][Movshare][/COLOR]' , url = url , thumbnail = thumbnail , extra = show, fanart = fanart , folder = False , isPlayable = True)
                            plugintools.log("URL= "+url)
                            break

                        elif url.find("movreel") >= 0:
                            plugintools.add_item(action="movreel" , title = title + ' [COLOR orange][Movreel][/COLOR]' , url = url , thumbnail = thumbnail , extra = show, fanart = fanart , folder = False , isPlayable = True)
                            plugintools.log("URL= "+url)
                            break

                        elif url.find("videobam") >= 0:
                            plugintools.add_item(action="videobam" , title = title + ' [COLOR orange][Videobam][/COLOR]' , url = url , thumbnail = thumbnail , extra = show, fanart = fanart , folder = False , isPlayable = True)
                            plugintools.log("URL= "+url)
                            break

                        elif url.find("videoweed") >= 0:
                            plugintools.add_item(action="videoweed" , title = title + ' [COLOR orange][Videoweed][/COLOR]' , url = url , thumbnail = thumbnail , extra = show, fanart = fanart , folder = False , isPlayable = True)
                            plugintools.log("URL= "+url)
                            break

                        elif url.find("streamable") >= 0:
                            plugintools.add_item(action="streamable" , title = title + ' [COLOR orange][Streamable][/COLOR]' , url = url , thumbnail = thumbnail , extra = show, fanart = fanart , folder = False , isPlayable = True)
                            plugintools.log("URL= "+url)
                            break

                        elif url.find("rocvideo") >= 0:
                            plugintools.add_item(action="rocvideo" , title = title + ' [COLOR orange][Rocvideo][/COLOR]' , url = url , thumbnail = thumbnail , extra = show, fanart = fanart , folder = False , isPlayable = True)
                            plugintools.log("URL= "+url)
                            break

                        elif url.find("realvid") >= 0:
                            plugintools.add_item(action="realvid" , title = title + ' [COLOR orange][Realvid][/COLOR]' , url = url , thumbnail = thumbnail , extra = show, fanart = fanart , folder = False , isPlayable = True)
                            plugintools.log("URL= "+url)
                            break

                        elif url.find("netu") >= 0:
                            plugintools.add_item(action="netu" , title = title + ' [COLOR orange][Netu][/COLOR]' , url = url , thumbnail = thumbnail , extra = show, fanart = fanart , folder = False , isPlayable = True)
                            plugintools.log("URL= "+url)
                            break

                        elif url.find("videomega") >= 0:
                            plugintools.add_item(action="videomega" , title = title + ' [COLOR orange][Videomega][/COLOR]' , url = url , thumbnail = thumbnail , extra = show, fanart = fanart , folder = False , isPlayable = True)
                            plugintools.log("URL= "+url)
                            break
                        
                        elif url.find("video.tt") >= 0:
                            plugintools.add_item(action="videott" , title = title + ' [COLOR orange][Video.tt][/COLOR]' , url = url , thumbnail = thumbnail , extra = show, fanart = fanart , folder = False , isPlayable = True)
                            plugintools.log("URL= "+url)
                            break                        

                        elif url.find("flashx.tv") >= 0:
                            plugintools.add_item(action="flashx" , title = title + ' [COLOR orange][Flashx][/COLOR]' , url = url , thumbnail = thumbnail , extra = show, fanart = fanart , folder = False , isPlayable = True)
                            plugintools.log("URL= "+url)
                            break

                        elif url.find("turbovideos") >= 0:
                            plugintools.add_item(action="turbovideos" , title = title + ' [COLOR orange][Turbovideos][/COLOR]' , url = url , thumbnail = thumbnail , extra = show, fanart = fanart , folder = False , isPlayable = True)
                            plugintools.log("URL= "+url)
                            break

                        elif url.find("vidto.me") >= 0:
                            plugintools.add_item(action="vidtome" , title = title + ' [COLOR orange][Vidto.me][/COLOR]' , url = url , thumbnail = thumbnail , extra = show, fanart = fanart , folder = False , isPlayable = True)
                            plugintools.log("URL= "+url)
                            break                        

                        elif url.find("ok.ru") >= 0:
                            plugintools.add_item(action="okru" , title = title + ' [COLOR orange][Ok.ru][/COLOR]' , url = url , thumbnail = thumbnail , extra = show, fanart = fanart , folder = False , isPlayable = True)
                            plugintools.log("URL= "+url)
                            break                          
                        
                        elif url.endswith("flv") == True:
                            plugintools.log("URL= "+url)
                            plugintools.log("FANART = "+fanart)
                            plugintools.add_item( action = "play" , title = title + ' [COLOR cyan][Flash][/COLOR]' , url = url ,  thumbnail = thumbnail , extra = show, fanart = fanart , folder = False , isPlayable = True )
                            break

                        elif url.endswith("m3u8") == True:
                            plugintools.log("URL= "+url)
                            plugintools.log("FANART = "+fanart)
                            plugintools.add_item( action = "play" , title = title + ' [COLOR purple][m3u8][/COLOR]' , url = url , info_labels = datamovie , thumbnail = thumbnail , extra = show, fanart = fanart , folder = False , isPlayable = True )
                            break

                        elif url.startswith("cbr:") == True:
                            if url.find("copy.com") >= 0:
                                plugintools.log("CBR Copy.com")
                                #url = url.replace("cbr:", "").strip()
                            else:
                                url = url.replace("cbr:", "").strip()
                            plugintools.add_item( action = "cbx_reader" , title = '[COLOR white]' + title + ' [COLOR gold][CBR][/COLOR]', plot = plot , url = url , thumbnail = thumbnail , show = show, fanart = fanart , folder = True , isPlayable = False )                    
                            break

                        elif url.startswith("txt:") == True:
                            url = url.replace("txt:", "").strip()
                            plugintools.add_item( action = "txt_reader" , title = '[COLOR white]' + title + ' [COLOR gold][TXT][/COLOR]', plot = plot , url = url , thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = False )                    
                            break                        

                        elif url.startswith("cbz:") == True:
                            if url.find("copy.com") >= 0:
                                plugintools.log("CBZ Copy.com")
                                #url = url.replace("cbr:", "").strip()
                            else:
                                url = url.replace("cbr:", "").strip()
                            plugintools.add_item( action = "cbx_reader" , title = '[COLOR white]' + title + ' [COLOR gold][CBZ][/COLOR]', plot = plot , url = url , thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                            break

                        elif url.find("mediafire") >= 0:                                
                            plugintools.add_item( action = "cbx_reader" , title = '[COLOR white]' + title + ' [COLOR gold][Mediafire][/COLOR]', plot = plot , url = url , thumbnail = thumbnail , show = show, fanart = fanart , folder = True , isPlayable = True )
                            break                     
                            
                        elif url.find("youtube.com") >= 0:
                            videoid = url.replace("https://www.youtube.com/watch?v=", "")
                            url = 'plugin://plugin.video.youtube/play/?video_id='+videoid                       
                            plugintools.runAddon( action = "play" , title = title.strip() + ' [[COLOR red]You[COLOR white]tube Video][/COLOR]', url = url , extra = show, thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = False )
                            break

                        elif url.startswith("short") == True:
                            url.replace("short:", "").strip()
                            title = title_search.split('"')
                            title = title[0]
                            title = title.strip()
                            plugintools.add_item( action = "longurl" , title = '[COLOR white]' + title + '[COLOR lightblue] [HTTP][/COLOR][I][COLOR lightsalmon] (' + origen + ')[/COLOR][/I]', url = url , extra = show , show = show , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                            params["show"]=show
                            plugintools.log("show "+show)
                            data = file.readline()
                            i = i + 1
                            continue

                        elif url.endswith("acelive") == True:
                            title_fixed = parser_title(title);title=title.replace(" ", "+").strip()
                            url = p2p_builder_url(url, title_fixed, p2p="ace")
                            plugintools.add_item( action = "runPlugin" , title = '[COLOR white]' + title + '[COLOR lightblue] [Acestream][/COLOR]', url = url , extra = show , show = show , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                            params["show"]=show
                            plugintools.log("show "+show)
                            data = file.readline()
                            i = i + 1
                            continue
                        
                        else:
                            plugintools.log("URL= "+url)
                            plugintools.add_item( action = "play" , title = title + ' [COLOR white][HTTP][/COLOR]' , url = url ,  extra = show , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                            plugintools.log("show "+show)
                            break

                    elif url.startswith("rtmp") == True:
                        params["url"] = url                        
                        server_rtmp(params)
                        server = params.get("server")                        
                        plugintools.add_item( action = "launch_rtmp" , title = title + '[COLOR green] [' + server + '][/COLOR]' , extra = show, url = params.get("url") ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                        break

                    elif url.startswith("rtsp") == True:
                        params["url"] = url
                        server_rtmp(params)
                        server = params.get("server")
                        plugintools.add_item( action = "launch_rtmp" , title = title + '[COLOR green] [' + server + '][/COLOR]' , extra = show, url = params.get("url") ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                        break

                    elif url.startswith("plugin") == True:
                        if url.find("plugin.video.f4mTester") >= 0:
                            if cat != "":
                                if busqueda == 'search.txt':
                                    plugintools.add_item( action = "play" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR orange] [F4M][/COLOR][I][COLOR lightblue] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = __art__ + "icon.png" , fanart = __art__ + 'fanart.jpg' , show = show, folder = False , isPlayable = True )
                                    data = file.readline()
                                    i = i + 1
                                    continue
                                else:                                    
                                    plugintools.add_item( action = "play" , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR orange] [F4M][/COLOR]', plot = plot , url = url , thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                    data = file.readline()
                                    i = i + 1
                                    continue
                            else:
                                if busqueda == 'search.txt':
                                    plugintools.add_item( action = "play" , title = '[COLOR white]' + title + '[COLOR orange] [F4M][/COLOR][I][COLOR lightblue] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = __art__ + "icon.png" , fanart = __art__ + 'fanart.jpg' , show = show, folder = False , isPlayable = True )
                                    data = file.readline()
                                    i = i + 1
                                    continue
                                else:                                    
                                    plugintools.add_item( action = "play" , title = '[COLOR white]' + title + '[COLOR orange] [F4M][/COLOR]', plot = plot , url = url , thumbnail = thumbnail , show = show, fanart = fanart , folder = False , isPlayable = True )
                                    data = file.readline()
                                    i = i + 1
                                    continue
                        
                        elif url.find("plugin.video.youtube") >= 0:
                            plugintools.log("url= "+url)
                            plugintools.add_item( action = "runPlugin" , title = title.strip() + ' [COLOR white][[COLOR red]You[COLOR white]tube Video][/COLOR][/COLOR]' , extra = show, url = url ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                            i = i + 1
                            continue
                        
                        elif url.find("plugin.video.p2p-streams") >= 0:
                            if url.find("mode=1") >= 0:
                                title = parser_title(title)
                                url = url.strip()
                                plugintools.add_item(action="play" , title = title + ' [COLOR lightblue][Acestream][/COLOR]' , extra = show, url = url, thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True)
                                i = i + 1
                                continue
                            elif url.find("mode=2") >= 0:
                                title = parser_title(title)
                                url = url.strip()
                                plugintools.add_item(action="play" , title = title_fixed + ' [COLOR lightblue][Sopcast][/COLOR]' , extra = show, url = url, thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True)
                                i = i + 1
                                continue

                    elif url.startswith("sop") == True:
                        # plugin://plugin.video.p2p-streams/?url=sop://124.232.150.188:3912/11265&mode=2&name=Titulo+canal+Sopcast
                        title = parser_title(title);title_fixed=title.replace(" ", "+").strip()
                        url = p2p_builder_url(url, title_fixed, p2p="sop")
                        plugintools.add_item(action="play" , title = title + ' [COLOR lightgreen][Sopcast][/COLOR]' , extra = show, url = url, thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True)
                        data = file.readline()
                        data = data.strip()
                        i = i + 1                        
                        continue

                    elif url.startswith("ace") == True:
                        title = parser_title(title);title_fixed=title.replace(" ", "+").strip()
                        url = url.replace("ace:", "")
                        url = p2p_builder_url(url, title_fixed, p2p="ace")
                        plugintools.add_item(action="play" , title = title + ' [COLOR lightblue][Acestream][/COLOR]' , extra = show, url = url, thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True)
                        data = file.readline()
                        data = data.strip()
                        i = i + 1
                        continue

                    elif url.startswith("magnet") >= 0:
                        url = urllib.quote_plus(data)
                        title = parser_title(title);title_fixed=title.replace(" ", "+").strip()
                        url = p2p_builder_url(url, title_fixed, p2p="magnet")
                        plugintools.add_item(action="play" , title = title + ' [COLOR orangered][Torrent][/COLOR]' , extra = show, url = url, thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True)
                        break
                    
                    else:
                        plugintools.add_item(action="play" , title = title , extra = show, url = url , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True)
                        plugintools.log("URL = "+url)
                        break

                elif data == "" :
                    break
                else:
                    data = file.readline()
                    data = data.strip()
                    i = i + 1
                    print i

        if (data == 'type=playlist') == True:
            # Control si no se definió fanart en cada entrada de la lista => Se usa fanart global de la lista
            if fanart == "":
                fanart = background
            data = file.readline()
            i = i + 1
            print i
            while data <> "" :
                if data.startswith("name") == True :
                    data = data.replace("name=", "")
                    title = data.strip()
                    if title == '>>>' :
                        title = title.replace(">>>", "[I][COLOR lightyellow]Siguiente[/I][/COLOR]")
                        data = file.readline()
                        data = data.strip()
                        i = i + 1

                    elif title == '<<<' :
                        title = title.replace("<<<", "[I][COLOR lightyellow]Anterior[/I][/COLOR]")
                        data = file.readline()
                        data = data.strip()
                        i = i + 1

                    elif title.find("Sorted by user-assigned order") >= 0:
                        title = "[I][COLOR lightyellow]Ordenar listas por...[/I][/COLOR]"
                        data = file.readline()
                        data = data.strip()
                        i = i + 1

                    elif title.find("Sorted A-Z") >= 0:
                        title = "[I][COLOR lightyellow][COLOR lightyellow]De la A a la Z[/I][/COLOR]"
                        data = file.readline()
                        data = data.strip()
                        i = i + 1

                    elif title.find("Sorted Z-A") >= 0:
                        title = "[I][COLOR lightyellow]De la Z a la A[/I][/COLOR]"
                        data = file.readline()
                        data = data.strip()
                        i = i + 1

                    elif title.find("Sorted by date added, newest first") >= 0:
                        title = "Ordenado por: Las + recientes primero..."
                        data = file.readline()
                        data = data.strip()
                        i = i + 1

                    elif title.find("Sorted by date added, oldest first") >= 0:
                        title = "Ordenado por: Las + antiguas primero..."
                        data = file.readline()
                        data = data.strip()
                        i = i + 1

                    elif title.find("by user-assigned order") >= 0:
                        title = "[COLOR lightyellow]Ordenar listas por...[/COLOR]"
                        data = file.readline()
                        data = data.strip()
                        i = i + 1

                    elif title.find("by date added, newest first") >= 0 :
                        title = "Las + recientes primero..."
                        data = file.readline()
                        data = data.strip()
                        i = i + 1
                    elif title.find("by date added, oldest first") >= 0 :
                        title = "Las + antiguas primero..."
                        data = file.readline()
                        data = data.strip()
                        i = i + 1

                elif data.startswith("thumb") == True:
                    data = data.replace("thumb=", "")
                    data = data.strip()
                    thumbnail = data
                    data = file.readline()
                    data = data.strip()
                    i = i + 1
                    print i
                    continue

                elif data.startswith("URL") == True:
                    data = data.replace("URL=", "")
                    data = data.strip()
                    url = data
                    parse_url(url)
                    if url.startswith("m3u") == True:
                        url = url.replace("m3u:", "")
                        plugintools.add_item(action="getfile_http" , title = title , extra = show, url = url , thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False)
                    elif url.startswith("plx") == True:
                        url = url.replace("plx:", "")
                        plugintools.add_item(action="plx_items" , title = title , extra = show, url = url , thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False)

                elif data == "" :
                    break

                else:
                    data = file.readline()
                    data = data.strip()
                    i = i + 1
                    print i
                    continue


    file.close()
	

    # Purga de listas erróneas creadas al abrir listas PLX (por los playlist de ordenación que crea Navixtreme)

    if os.path.isfile(__playlists__ + 'Siguiente.plx'):
        os.remove(__playlists__ + 'Siguiente.plx')
        print "Correcto!"
    else:
        pass

    if os.path.isfile(__playlists__ + 'Ordenar listas por....plx'):
        os.remove(__playlists__ + 'Ordenar listas por....plx')
        print "Ordenar listas por....plx eliminado!"
        print "Correcto!"
    else:
        print "No es posible!"
        pass

    if os.path.isfile(__playlists__ + 'A-Z.plx'):
        os.remove(__playlists__ + 'A-Z.plx')
        print "A-Z.plx eliminado!"
    else:
        print "No es posible!"
        pass

    if os.path.isfile(__playlists__ + 'De la A a la Z.plx'):
        os.remove(__playlists__ + 'De la A a la Z.plx')
        print "De la A a la Z.plx eliminado!"
    else:
        print "No es posible!"
        pass

    if os.path.isfile(__playlists__ + 'Z-A.plx'):
        os.remove(__playlists__ + 'Z-A.plx')
        print "Z-A.plx eliminado!"
    else:
        print "No es posible!"
        pass

    if os.path.isfile(__playlists__ + 'De la Z a la A.plx'):
        os.remove(__playlists__ + 'De la Z a la A.plx')
        print "De la Z a la A.plx eliminado!"
    else:
        print "No es posible!"
        pass

    if os.path.isfile(__playlists__ + 'Las + antiguas primero....plx'):
        os.remove(__playlists__ + 'Las + antiguas primero....plx')
        print "Las más antiguas primero....plx eliminado!"
    else:
        print "No es posible!"
        pass

    if os.path.isfile(__playlists__ + 'by date added, oldest first.plx'):
        os.remove(__playlists__ + 'by date added, oldest first.plx')
        print "by date added, oldest first.plx eliminado!"
    else:
        print "No es posible!"
        pass

    if os.path.isfile(__playlists__ + 'Las + recientes primero....plx'):
        os.remove(__playlists__ + 'Las + recientes primero....plx')
    else:
        print "No es posible!"
        pass

    if os.path.isfile(__playlists__ + 'by date added, newest first.plx'):
        os.remove(__playlists__ + 'by date added, newest first.plx')
        print "by date added, newest first.plx eliminado!"
    else:
        print "No es posible!"
        pass

    if os.path.isfile(__playlists__ + 'Sorted by user-assigned order.plx'):
        os.remove(__playlists__ + 'Sorted by user-assigned order.plx')
        print "Sorted by user-assigned order.plx eliminado!"
    else:
        print "No es posible!"
        pass

    if os.path.isfile(__playlists__ + 'Ordenado por.plx'):
        os.remove(__playlists__ + 'Ordenado por.plx')
        print "Correcto!"
    else:
        print "No es posible!"
        pass

    if os.path.isfile(__playlists__ + 'Ordenado por'):
        os.remove(__playlists__ + 'Ordenado por')
        print "Correcto!"
    else:
        print "No es posible!"
        pass


def encode_string(txt):
    plugintools.log('[%s %s].encode_string %s' % (addonName, addonVersion, txt))

    txt = txt.replace("&#231;", "ç")
    txt = txt.replace('&#233;', 'é')
    txt = txt.replace('&#225;', 'á')
    txt = txt.replace('&#233;', 'é')
    txt = txt.replace('&#225;', 'á')
    txt = txt.replace('&#241;', 'ñ')
    txt = txt.replace('&#250;', 'ú')
    txt = txt.replace('&#237;', 'í')
    txt = txt.replace('&#243;', 'ó')
    txt = txt.replace('&#39;', "'")
    txt = txt.replace("&nbsp;", "")
    txt = txt.replace("&nbsp;", "")
    txt = txt.replace('&#39;', "'")
    return txt



def splive_items(params):
    plugintools.log('[%s %s].splive_items %s' % (addonName, addonVersion, repr(params)))
    data = plugintools.read( params.get("url") )

    channel = plugintools.find_multiple_matches(data,'<channel>(.*?)</channel>')

    for entry in channel:
        # plugintools.log("channel= "+channel)
        title = plugintools.find_single_match(entry,'<name>(.*?)</name>')
        category = plugintools.find_single_match(entry,'<category>(.*?)</category>')
        thumbnail = plugintools.find_single_match(entry,'<link_logo>(.*?)</link_logo>')
        rtmp = plugintools.find_single_match(entry,'<rtmp>([^<]+)</rtmp>')
        isIliveTo = plugintools.find_single_match(entry,'<isIliveTo>([^<]+)</isIliveTo>')
        rtmp = rtmp.strip()
        pageurl = plugintools.find_single_match(entry,'<url_html>([^<]+)</url_html>')
        link_logo = plugintools.find_single_match(entry,'<link_logo>([^<]+)</link_logo>')

        if pageurl == "SinProgramacion":
            pageurl = ""

        playpath = plugintools.find_single_match(entry, '<playpath>([^<]+)</playpath>')
        playpath = playpath.replace("Referer: ", "")
        token = plugintools.find_single_match(entry, '<token>([^<]+)</token>')

        iliveto = 'rtmp://188.122.91.73/edge'

        if isIliveTo == "0":
            if token == "0":
                url = rtmp
                url = url.replace("&amp;", "&")
                parse_url(url)
                plugintools.add_item( action = "play" , title = title , url = url , thumbnail = thumbnail , fanart = fanart , plot = title , folder = False , isPlayable = True )
                plugintools.log("url= "+url)
            else:
                url = rtmp + " pageUrl=" + pageurl + " " + 'token=' + token + playpath + " live=1"
                parse_url(url)
                plugintools.add_item( action = "play" , title = title , url = url , thumbnail = thumbnail , fanart = fanart , plot = title , folder = False , isPlayable = True )
                plugintools.log("url= "+url)

        if isIliveTo == "1":
            if token == "1":
                url = iliveto + " pageUrl=" + pageurl + " " + 'token=' + token + playpath + " live=1"
                url = url.replace("&amp;", "&")
                parse_url(url)
                plugintools.add_item( action = "play" , title = title , url = url , thumbnail = thumbnail , fanart = fanart , plot = title , folder = False , isPlayable = True )
                plugintools.log("url= "+url)

            else:
                url = iliveto + ' swfUrl=' + rtmp +  " playpath=" + playpath + " pageUrl=" + pageurl
                url = url.replace("&amp;", "&")
                parse_url(url)
                plugintools.add_item( action = "play" , title = title , url = url , thumbnail = thumbnail , fanart = fanart , plot = title , folder = False , isPlayable = True )
                plugintools.log("url= "+url)


def p2p_items(params):
    plugintools.log('[%s %s].p2p_items %s' % (addonName, addonVersion, repr(params)))

    # Vamos a localizar el título
    title = params.get("plot")
    if title == "":
        title = params.get("title")

    data = plugintools.read("http://pastebin.com/raw.php?i=ydUjKXnN")
    subcanal = plugintools.find_single_match(data,'<name>' + title + '(.*?)</subchannel>')
    thumbnail = plugintools.find_single_match(subcanal, '<thumbnail>(.*?)</thumbnail>')
    fanart = plugintools.find_single_match(subcanal, '<fanart>(.*?)</fanart>')
    plugintools.log("thumbnail= "+thumbnail)


    # Controlamos el caso en que no haya thumbnail en el menú de pld.visiontv
    if thumbnail == "":
        thumbnail = __art__ + 'p2p.png'
    elif thumbnail == 'name_rtmp.png':
        thumbnail = __art__ + 'p2p.png'

    if fanart == "":
        fanart = __art__ + 'p2p.png'

    # Comprobamos si la lista ha sido descargada o no
    plot = params.get("plot")

    if plot == "":
        title = params.get("title")
        title = parser_title(title)
        filename = title + '.p2p'
        getfile_url(params)
    else:
        print "Lista ya descargada (plot no vacío)"
        filename = params.get("plot")
        params["ext"] = 'p2p'
        params["plot"]=filename
        filename = filename + '.p2p'
        plugintools.log("Lectura del archivo P2P")

    plugintools.add_item(action="" , title='[COLOR lightyellow][I][B]' + title + '[/B][/I][/COLOR]' , thumbnail=thumbnail , fanart=fanart , folder=False, isPlayable=False)

    # Abrimos el archivo P2P y calculamos número de líneas
    file = open(__playlists__ + filename, "r")
    file.seek(0)
    data = file.readline()
    num_items = len(file.readlines())
    print num_items
    file.seek(0)
    data = file.readline()
    if data.startswith("default") == True:
        data = data.replace("default=", "")
        data = data.split(",")
        thumbnail = data[0]
        fanart = data[1]
        plugintools.log("fanart= "+fanart)

    # Leemos entradas
    i = 0
    file.seek(0)
    data = file.readline()
    data = data.strip()
    while i <= num_items:
        if data == "":
            data = file.readline()
            data = data.strip()
            # plugintools.log("linea vacia= "+data)
            i = i + 1
            #print i
            continue

        elif data.startswith("default") == True:
            data = file.readline()
            data = data.strip()
            i = i + 1
            #print i
            continue

        elif data.startswith("#") == True:
            title = data.replace("#", "")
            plugintools.log("title comentario= "+title)
            plugintools.add_item(action="play" , title = title , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True)
            data = file.readline()
            data = data.strip()
            i = i + 1
            continue

        else:
            title = data
            title = title.strip()
            plugintools.log("title= "+title)
            data = file.readline()
            data = data.strip()
            i = i + 1
            #print i
            plugintools.log("linea URL= "+data)
            if data.startswith("sop") == True:
                print "empieza el sopcast..."
                # plugin://plugin.video.p2p-streams/?url=sop://124.232.150.188:3912/11265&mode=2&name=Titulo+canal+Sopcast
                title = parser_title(title);title_fixed=title.replace(" ", "+").strip()
                url = p2p_builder_url(url, title_fixed, p2p="sop")
                plugintools.add_item(action="play" , title = title + ' [COLOR lightgreen][Sopcast][/COLOR]' , url = url, thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True)
                data = file.readline()
                data = data.strip()
                i = i + 1
                #print i
                continue

            elif data.startswith("magnet") == True:
                url = urllib.quote_plus(data)
                title = parser_title(title);title_fixed=title.replace(" ", "+").strip()
                url = p2p_builder_url(url, title_fixed, p2p="magnet")
                plugintools.add_item(action="play" , title = title + ' [COLOR orangered][Torrent][/COLOR]' , url = url, thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True)
                data = file.readline()
                data = data.strip()
                i = i + 1
                continue

            else:
                # plugin://plugin.video.p2p-streams/?url=a55f96dd386b7722380802b6afffc97ff98903ac&mode=1&name=Sky+Sports+title
                title = parser_title(title);title_fixed=title.replace(" ", "+").strip()
                url = p2p_builder_url(data, title_fixed, p2p="ace")
                plugintools.add_item(action="play" , title = title + ' [COLOR lightblue][Acestream][/COLOR]' , url = url, thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True)
                data = file.readline()
                data = data.strip()
                i = i + 1
                #print i




def contextMenu(params):
    plugintools.log('[%s %s].contextMenu %s' % (addonName, addonVersion, repr(params)))

    dialog = xbmcgui.Dialog()
    plot = params.get("plot")
    canales = plot.split("/")
    len_canales = len(canales)
    print len_canales
    plugintools.log("canales= "+repr(canales))

    if len_canales == 1:
        tv_a = canales[0]
        tv_a = parse_channel(tv_a)
        search_channel(params)
        selector = ""
    else:
        if len_canales == 2:
            print "len_2"
            tv_a = canales[0]
            tv_a = parse_channel(tv_a)
            tv_b = canales[1]
            tv_b = parse_channel(tv_b)
            selector = dialog.select('pld.visiontv', [tv_a, tv_b])

        elif len_canales == 3:
            tv_a = canales[0]
            tv_a = parse_channel(tv_a)
            tv_b = canales[1]
            tv_b = parse_channel(tv_b)
            tv_c = canales[2]
            tv_c = parse_channel(tv_c)
            selector = dialog.select('pld.visiontv', [tv_a, tv_b, tv_c])

        elif len_canales == 4:
            tv_a = canales[0]
            tv_a = parse_channel(tv_a)
            tv_b = canales[1]
            tv_b = parse_channel(tv_b)
            tv_c = canales[2]
            tv_c = parse_channel(tv_c)
            tv_d = canales[3]
            tv_d = parse_channel(tv_d)
            selector = dialog.select('pld.visiontv', [tv_a, tv_b, tv_c, tv_d])

        elif len_canales == 5:
            tv_a = canales[0]
            tv_a = parse_channel(tv_a)
            tv_b = canales[1]
            tv_b = parse_channel(tv_b)
            tv_c = canales[2]
            tv_c = parse_channel(tv_c)
            tv_d = canales[3]
            tv_d = parse_channel(tv_d)
            tv_e = canales[4]
            tv_e = parse_channel(tv_e)
            selector = dialog.select('pld.visiontv', [tv_a, tv_b, tv_c, tv_d, tv_e])

        elif len_canales == 6:
            tv_a = canales[0]
            tv_a = parse_channel(tv_a)
            tv_b = canales[1]
            tv_b = parse_channel(tv_b)
            tv_c = canales[2]
            tv_c = parse_channel(tv_c)
            tv_d = canales[3]
            tv_d = parse_channel(tv_d)
            tv_e = canales[4]
            tv_e = parse_channel(tv_e)
            tv_f = canales[5]
            tv_f = parse_channel(tv_f)
            selector = dialog.select('pld.visiontv', [tv_a , tv_b, tv_c, tv_d, tv_e, tv_f])

        elif len_canales == 7:
            tv_a = canales[0]
            tv_a = parse_channel(tv_a)
            tv_b = canales[1]
            tv_b = parse_channel(tv_b)
            tv_c = canales[2]
            tv_c = parse_channel(tv_c)
            tv_d = canales[3]
            tv_d = parse_channel(tv_d)
            tv_e = canales[4]
            tv_e = parse_channel(tv_e)
            tv_f = canales[5]
            tv_f = parse_channel(tv_f)
            tv_g = canales[6]
            tv_g = parse_channel(tv_g)
            selector = dialog.select('pld.visiontv', [tv_a , tv_b, tv_c, tv_d, tv_e, tv_f, tv_g])

    if selector == 0:
        print selector
        if tv_a.startswith("Gol") == True:
            tv_a = "Gol"
        params["plot"] = tv_a
        plugintools.log("tv= "+tv_a)
        search_channel(params)
    elif selector == 1:
        print selector
        if tv_b.startswith("Gol") == True:
            tv_b = "Gol"
        params["plot"] = tv_b
        plugintools.log("tv= "+tv_b)
        search_channel(params)
    elif selector == 2:
        print selector
        if tv_c.startswith("Gol") == True:
            tv_c = "Gol"
        params["plot"] = tv_c
        plugintools.log("tv= "+tv_c)
        search_channel(params)
    elif selector == 3:
        print selector
        if tv_d.startswith("Gol") == True:
            tv_d = "Gol"
        params["plot"] = tv_d
        plugintools.log("tv= "+tv_d)
        search_channel(params)
    elif selector == 4:
        print selector
        if tv_e.startswith("Gol") == True:
            tv_e = "Gol"
        params["plot"] = tv_e
        plugintools.log("tv= "+tv_e)
        search_channel(params)
    elif selector == 5:
        print selector
        if tv_f.startswith("Gol") == True:
            tv_f = "Gol"
        params["plot"] = tv_f
        plugintools.log("tv= "+tv_f)
        search_channel(params)
    elif selector == 6:
        print selector
        if tv_g.startswith("Gol") == True:
            tv_g = "Gol"
        params["plot"] = tv_g
        plugintools.log("tv= "+tv_g)
        search_channel(params)
    else:
        pass



def magnet_items(params):
    plugintools.log('[%s %s].magnet_items %s' % (addonName, addonVersion, repr(params)))

    plot = params.get("plot")


    title = params.get("title")
    fanart = ""
    thumbnail = ""

    if plot != "":
        filename = params.get("plot")
        params["ext"] = 'p2p'
        params["plot"]=filename
        title = plot + '.p2p'
    else:
        getfile_url(params)
        title = params.get("title")
        title = title + '.p2p'

    # Abrimos el archivo P2P y calculamos número de líneas
    file = open(__playlists__ + title, "r")
    file.seek(0)
    data = file.readline()
    num_items = len(file.readlines())

    # Leemos entradas
    file.seek(0)
    i = 0
    while i <= num_items:
        data = file.readline()
        i = i + 1
        #print i
        if data != "":
            data = data.strip()
            title = data
            data = file.readline()
            i = i + 1
            #print i
            data = data.strip()
            if data.startswith("magnet:") == True:
                # plugin://plugin.video.p2p-streams/?url=sop://124.232.150.188:3912/11265&mode=2&name=Titulo+canal+Sopcast
                #title_fixed = title.replace(" " , "+")
                title_fixed=urllib_quote_plus(title)
                url_fixed = urllib.quote_plus(link)
                url = url.strip()
                url = p2p_builder_url(url, title_fixed, p2p="magnet")
                plugintools.add_item(action="play" , title = data + ' [COLOR orangered][Torrent][/COLOR]' , url = url, thumbnail = __art__ + 'p2p.png' , fanart = __art__ + 'fanart.jpg' , folder = False , isPlayable = True)
            else:
                data = file.readline()
                i = i + 1
                #print i
        else:
            data = file.readline()
            i = i + 1
            #print i


def parse_channel(txt):
    plugintools.log('[%s %s].parse_channelñana %s' % (addonName, addonVersion, txt))

    txt = txt.rstrip()
    txt = txt.lstrip()
    return txt


def futbolenlatv_manana(params):
    plugintools.log('[%s %s].futbolenlatv_mañana %s' % (addonName, addonVersion, repr(params)))

    # Fecha de mañana
    import datetime

    today = datetime.date.today()
    manana = today + datetime.timedelta(days=1)
    anno_manana = manana.year
    mes_manana = manana.month
    if mes_manana == 1:
        mes_manana = "enero"
    elif mes_manana == 2:
        mes_manana = "febrero"
    elif mes_manana == 3:
        mes_manana = "marzo"
    elif mes_manana == 4:
        mes_manana = "abril"
    elif mes_manana == 5:
        mes_manana = "mayo"
    elif mes_manana == 6:
        mes_manana = "junio"
    elif mes_manana == 7:
        mes_manana = "julio"
    elif mes_manana == 8:
        mes_manana = "agosto"
    elif mes_manana == 9:
        mes_manana = "septiembre"
    elif mes_manana == 10:
        mes_manana = "octubre"
    elif mes_manana == 11:
        mes_manana = "noviembre"
    elif mes_manana == 12:
        mes_manana = "diciembre"


    dia_manana = manana.day
    plot = str(anno_manana) + "-" + str(mes_manana) + "-" + str(dia_manana)
    print manana

    url = 'http://www.futbolenlatv.com/m/Fecha/' + plot + '/agenda/false/false'
    plugintools.log("URL mañana= "+url)
    params["url"] = url
    params["plot"] = plot
    futbolenlatv(params)





def parser_title(title):
    plugintools.log('[%s %s].parser_title %s' % (addonName, addonVersion, title))

    cyd = title

    cyd = cyd.replace("[COLOR lightyellow]", "")
    cyd = cyd.replace("[COLOR green]", "")
    cyd = cyd.replace("[COLOR red]", "")
    cyd = cyd.replace("[COLOR blue]", "")
    cyd = cyd.replace("[COLOR royalblue]", "")
    cyd = cyd.replace("[COLOR white]", "")
    cyd = cyd.replace("[COLOR pink]", "")
    cyd = cyd.replace("[COLOR cyan]", "")
    cyd = cyd.replace("[COLOR steelblue]", "")
    cyd = cyd.replace("[COLOR forestgreen]", "")
    cyd = cyd.replace("[COLOR olive]", "")
    cyd = cyd.replace("[COLOR khaki]", "")
    cyd = cyd.replace("[COLOR lightsalmon]", "")
    cyd = cyd.replace("[COLOR orange]", "")
    cyd = cyd.replace("[COLOR lightgreen]", "")
    cyd = cyd.replace("[COLOR lightblue]", "")
    cyd = cyd.replace("[COLOR lightpink]", "")
    cyd = cyd.replace("[COLOR skyblue]", "")
    cyd = cyd.replace("[COLOR darkorange]", "")
    cyd = cyd.replace("[COLOR greenyellow]", "")
    cyd = cyd.replace("[COLOR yellow]", "")
    cyd = cyd.replace("[COLOR yellowgreen]", "")
    cyd = cyd.replace("[COLOR orangered]", "")
    cyd = cyd.replace("[COLOR grey]", "")
    cyd = cyd.replace("[COLOR gold]", "")
    cyd = cyd.replace("[COLOR lime]", "")
    cyd = cyd.replace("[COLOR brown]", "")
    cyd = cyd.replace("[COLOR black]", "")
    cyd = cyd.replace("[COLOR=FF00FF00]", "")

    cyd = cyd.replace("&quot;", '"')

    cyd = cyd.replace("[/COLOR]", "")
    cyd = cyd.replace("[B]", "")
    cyd = cyd.replace("[/B]", "")
    cyd = cyd.replace("[I]", "")
    cyd = cyd.replace("[/I]", "")
    cyd = cyd.replace("[Auto]", "")
    cyd = cyd.replace("[Parser]", "")
    cyd = cyd.replace("[TinyURL]", "")
    cyd = cyd.replace("[Auto]", "")
    cyd = cyd.replace("[Filtros]", "")
    cyd = cyd.replace("[Filtro]", "")

    # Control para evitar filenames con corchetes
    cyd = cyd.replace(" [Lista M3U]", "")
    cyd = cyd.replace(" [Lista PLX]", "")
    cyd = cyd.replace(" [Multilink]", "")
    cyd = cyd.replace(" [Multiparser]", "")
    cyd = cyd.replace(" [COLOR orange][Lista [B]PLX[/B]][/COLOR]", "")
    cyd = cyd.replace(" [COLOR orange][Lista [B]M3U[/B]][/COLOR]", "")
    cyd = cyd.replace(" [COLOR lightyellow][B][Dailymotion[/B] playlist][/COLOR]", "")
    cyd = cyd.replace(" [COLOR lightyellow][B][Dailymotion[/B] video][/COLOR]", "")
    cyd = cyd.replace(' [COLOR gold][CBZ][/COLOR]', "")
    cyd = cyd.replace(' [COLOR gold][CBR][/COLOR]', "")
    cyd = cyd.replace(' [COLOR gold][Mediafire][/COLOR]', "")
    cyd = cyd.replace(' [CBZ]', "")
    cyd = cyd.replace(' [CBR]', "")
    cyd = cyd.replace(' [Mediafire]', "")
    cyd = cyd.replace(' [EPG-TXT]', "")
    
    # Control para evitar errores al crear archivos
    cyd = cyd.replace("[", "")
    cyd = cyd.replace("]", "")
    #cyd = cyd.replace(".", "")
    
    title = cyd
    title = title.strip()
    if title.endswith(" .plx") == True:
        title = title.replace(" .plx", ".plx")

    plugintools.log("title_parsed= "+title)
    return title


def json_items(params):
    plugintools.log('[%s %s].json_items %s' % (addonName, addonVersion, repr(params)))
    
    filename = params.get("plot")
    if filename != "":
        filename =  filename + '.jsn'
        fjson = open(__playlists__ + filename, "r")
        data = fjson.readlines()
    else:
        data = plugintools.read(params.get("url"))
        
    # Título y autor de la lista
    try:
        match = plugintools.find_single_match(data, '"name"(.*?)"url"')
        match = match.split(",")
        namelist = match[0].strip()
        author = match[1].strip()
        namelist = namelist.replace('"', "")
        namelist = namelist.replace(": ", "")
        author = author.replace('"author":', "")
        author = author.replace('"', "")
        fanart = params.get("extra")
        thumbnail = params.get("thumbnail")
        plugintools.log("title= "+namelist)
        plugintools.log("author= "+author)
        plugintools.add_item(action="", title = '[B][COLOR lightyellow]' + namelist + '[/B][/COLOR]' , url = "" , thumbnail = thumbnail , fanart = fanart, isPlayable = False , folder = False)
    except:
        pass

    # Items de la lista
    data = plugintools.find_single_match(data, '"stations"(.*?)]')
    matches = plugintools.find_multiple_matches(data, '"name"(.*?)}')
    for entry in matches:
        if entry.find("isHost") <= 0:
            title = plugintools.find_single_match(entry,'(.*?)\n')
            title = title.replace(": ", "")
            title = title.replace('"', "")
            title = title.replace(",", "")
            url = plugintools.find_single_match(entry,'"url":(.*?)\n')
            url = url.replace('"', "")
            url = url.strip()
            params["url"]=url
            server_rtmp(params)
            server = params.get("server")
            thumbnail = plugintools.find_single_match(entry,'"image":(.*?)\n')
            thumbnail = thumbnail.replace('"', "")
            thumbnail = thumbnail.replace(',', "")
            thumbnail = thumbnail.strip()
            plugintools.log("thumbnail= "+thumbnail)
            # Control por si en la lista no aparece el logo en cada entrada
            if thumbnail == "" :
                thumbnail = params.get("thumbnail")

            plugintools.add_item( action="play" , title = '[COLOR white] ' + title + '[COLOR green] ['+ server + '][/COLOR]' , url = params.get("url") , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )

        else:
            title = plugintools.find_single_match(entry,'(.*?)\n')
            title = title.replace(": ", "")
            title = title.replace('"', "")
            title = title.replace(",", "")
            url = plugintools.find_single_match(entry,'"url":(.*?)\n')
            url = url.replace('"', "")
            url = url.strip()

            if url.find("allmyvideos")>= 0:
                url = url.replace(",", "")
                plugintools.log("url= "+url)
                fanart = params.get("extra")
                thumbnail = plugintools.find_single_match(entry,'"image":(.*?)\n')
                thumbnail = thumbnail.replace('"', "")
                thumbnail = thumbnail.replace(',', "")
                thumbnail = thumbnail.strip()
                plugintools.log("thumbnail= "+thumbnail)
                if thumbnail == "":
                    thumbnail = params.get("thumbnail")

                plugintools.add_item( action="allmyvideos" , title = title + ' [COLOR lightyellow][Allmyvideos][/COLOR]' , url = url , fanart = fanart , thumbnail = thumbnail , folder = False , isPlayable = True )

            elif url.find("streamcloud") >= 0:
                url = url.replace(",", "")
                plugintools.log("url= "+url)
                fanart = params.get("extra")
                thumbnail = plugintools.find_single_match(entry,'"image":(.*?)\n')
                thumbnail = thumbnail.replace('"', "")
                thumbnail = thumbnail.replace(',', "")
                thumbnail = thumbnail.strip()
                plugintools.log("thumbnail= "+thumbnail)
                if thumbnail == "":
                    thumbnail = params.get("thumbnail")

                plugintools.add_item( action="streamcloud" , title = title + ' [COLOR lightskyblue][Streamcloud][/COLOR]' , url = url , fanart = fanart , thumbnail = thumbnail , folder = False , isPlayable = True )

            elif url.find("played.to") >= 0:
                url = url.replace(",", "")
                plugintools.log("url= "+url)
                fanart = params.get("extra")
                thumbnail = plugintools.find_single_match(entry,'"image":(.*?)\n')
                thumbnail = thumbnail.replace('"', "")
                thumbnail = thumbnail.replace(',', "")
                thumbnail = thumbnail.strip()
                plugintools.log("thumbnail= "+thumbnail)
                if thumbnail == "":
                    thumbnail = params.get("thumbnail")
                plugintools.add_item( action="playedto" , title = title + ' [COLOR lavender][Played.to][/COLOR]' , url = url , fanart = fanart , thumbnail = thumbnail , folder = False , isPlayable = True )

            elif url.find("vidspot") >= 0:
                url = url.replace(",", "")
                plugintools.log("url= "+url)
                fanart = params.get("extra")
                thumbnail = plugintools.find_single_match(entry,'"image":(.*?)\n')
                thumbnail = thumbnail.replace('"', "")
                thumbnail = thumbnail.replace(',', "")
                thumbnail = thumbnail.strip()
                plugintools.log("thumbnail= "+thumbnail)
                if thumbnail == "":
                    thumbnail = params.get("thumbnail")

                plugintools.add_item( action="vidspot" , title = title + ' [COLOR palegreen][Vidspot][/COLOR]' , url = url , fanart = fanart , thumbnail = thumbnail , folder = False , isPlayable = True )

            if url.find("vk.com")>= 0:
                url = url.replace(",", "")
                plugintools.log("url= "+url)
                fanart = params.get("extra")
                thumbnail = plugintools.find_single_match(entry,'"image":(.*?)\n')
                thumbnail = thumbnail.replace('"', "")
                thumbnail = thumbnail.replace(',', "")
                thumbnail = thumbnail.strip()
                plugintools.log("thumbnail= "+thumbnail)
                if thumbnail == "":
                    thumbnail = params.get("thumbnail")

                plugintools.add_item( action="vk" , title = title + ' [COLOR royalblue][Vk][/COLOR]' , url = url , fanart = fanart , thumbnail = thumbnail , folder = False , isPlayable = True )

            if url.find("nowvideo")>= 0:
                url = url.replace(",", "")
                plugintools.log("url= "+url)
                fanart = params.get("extra")
                thumbnail = plugintools.find_single_match(entry,'"image":(.*?)\n')
                thumbnail = thumbnail.replace('"', "")
                thumbnail = thumbnail.replace(',', "")
                thumbnail = thumbnail.strip()
                plugintools.log("thumbnail= "+thumbnail)
                if thumbnail == "":
                    thumbnail = params.get("thumbnail")

                plugintools.add_item( action="nowvideo" , title = title + ' [COLOR palegreen][Nowvideo][/COLOR]' , url = url , fanart = fanart , thumbnail = thumbnail , folder = False , isPlayable = True )

            if url.find("tumi")>= 0:
                url = url.replace(",", "")
                plugintools.log("url= "+url)
                fanart = params.get("extra")
                thumbnail = plugintools.find_single_match(entry,'"image":(.*?)\n')
                thumbnail = thumbnail.replace('"', "")
                thumbnail = thumbnail.replace(',', "")
                thumbnail = thumbnail.strip()
                plugintools.log("thumbnail= "+thumbnail)
                if thumbnail == "":
                    thumbnail = params.get("thumbnail")

                plugintools.add_item( action="tumi" , title = title + ' [COLOR forestgreen][Tumi][/COLOR]' , url = url , fanart = fanart , thumbnail = thumbnail , folder = False , isPlayable = True )

            if url.find("veehd.com")>= 0:
                url = url.replace(",", "")
                plugintools.log("url= "+url)
                fanart = params.get("extra")
                thumbnail = plugintools.find_single_match(entry,'"image":(.*?)\n')
                thumbnail = thumbnail.replace('"', "")
                thumbnail = thumbnail.replace(',', "")
                thumbnail = thumbnail.strip()
                plugintools.log("thumbnail= "+thumbnail)
                if thumbnail == "":
                    thumbnail = params.get("thumbnail")

                plugintools.add_item( action="veehd" , title = title + ' [COLOR orange][VeeHD][/COLOR]' , url = url , fanart = fanart , thumbnail = thumbnail , folder = False , isPlayable = True )

            if url.find("streamin.to")>= 0:
                url = url.replace(",", "")
                plugintools.log("url= "+url)
                fanart = params.get("extra")
                thumbnail = plugintools.find_single_match(entry,'"image":(.*?)\n')
                thumbnail = thumbnail.replace('"', "")
                thumbnail = thumbnail.replace(',', "")
                thumbnail = thumbnail.strip()
                plugintools.log("thumbnail= "+thumbnail)
                if thumbnail == "":
                    thumbnail = params.get("thumbnail")

                plugintools.add_item( action="streaminto" , title = title + ' [COLOR orange][streamin.to][/COLOR]' , url = url , fanart = fanart , thumbnail = thumbnail , folder = False , isPlayable = True )

            if url.find("powvideo")>= 0:
                url = url.replace(",", "")
                plugintools.log("url= "+url)
                fanart = params.get("extra")
                thumbnail = plugintools.find_single_match(entry,'"image":(.*?)\n')
                thumbnail = thumbnail.replace('"', "")
                thumbnail = thumbnail.replace(',', "")
                thumbnail = thumbnail.strip()
                plugintools.log("thumbnail= "+thumbnail)
                if thumbnail == "":
                    thumbnail = params.get("thumbnail")

                plugintools.add_item( action="powvideo" , title = title + ' [COLOR orange][powvideo][/COLOR]' , url = url , fanart = fanart , thumbnail = thumbnail , folder = False , isPlayable = True )

            if url.find("mail.ru")>= 0:
                url = url.replace(",", "")
                plugintools.log("url= "+url)
                fanart = params.get("extra")
                thumbnail = plugintools.find_single_match(entry,'"image":(.*?)\n')
                thumbnail = thumbnail.replace('"', "")
                thumbnail = thumbnail.replace(',', "")
                thumbnail = thumbnail.strip()
                plugintools.log("thumbnail= "+thumbnail)
                if thumbnail == "":
                    thumbnail = params.get("thumbnail")

                plugintools.add_item( action="mailru" , title = title + ' [COLOR orange][Mail.ru][/COLOR]' , url = url , fanart = fanart , thumbnail = thumbnail , folder = False , isPlayable = True )

            if url.find("novamov")>= 0:
                url = url.replace(",", "")
                plugintools.log("url= "+url)
                fanart = params.get("extra")
                thumbnail = plugintools.find_single_match(entry,'"image":(.*?)\n')
                thumbnail = thumbnail.replace('"', "")
                thumbnail = thumbnail.replace(',', "")
                thumbnail = thumbnail.strip()
                plugintools.log("thumbnail= "+thumbnail)
                if thumbnail == "":
                    thumbnail = params.get("thumbnail")

                plugintools.add_item( action="novamov" , title = title + ' [COLOR orange][Novamov][/COLOR]' , url = url , fanart = fanart , thumbnail = thumbnail , folder = False , isPlayable = True )

            if url.find("gamovideo")>= 0:
                url = url.replace(",", "")
                plugintools.log("url= "+url)
                fanart = params.get("extra")
                thumbnail = plugintools.find_single_match(entry,'"image":(.*?)\n')
                thumbnail = thumbnail.replace('"', "")
                thumbnail = thumbnail.replace(',', "")
                thumbnail = thumbnail.strip()
                plugintools.log("thumbnail= "+thumbnail)
                if thumbnail == "":
                    thumbnail = params.get("thumbnail")

                plugintools.add_item( action="gamovideo" , title = title + ' [COLOR orange][Gamovideo][/COLOR]' , url = url , fanart = fanart , thumbnail = thumbnail , folder = False , isPlayable = True )

            if url.find("moevideos")>= 0:
                url = url.replace(",", "")
                plugintools.log("url= "+url)
                fanart = params.get("extra")
                thumbnail = plugintools.find_single_match(entry,'"image":(.*?)\n')
                thumbnail = thumbnail.replace('"', "")
                thumbnail = thumbnail.replace(',', "")
                thumbnail = thumbnail.strip()
                plugintools.log("thumbnail= "+thumbnail)
                if thumbnail == "":
                    thumbnail = params.get("thumbnail")

                plugintools.add_item( action="moevideos" , title = title + ' [COLOR orange][Moevideos][/COLOR]' , url = url , fanart = fanart , thumbnail = thumbnail , folder = False , isPlayable = True )

            if url.find("movshare")>= 0:
                url = url.replace(",", "")
                plugintools.log("url= "+url)
                fanart = params.get("extra")
                thumbnail = plugintools.find_single_match(entry,'"image":(.*?)\n')
                thumbnail = thumbnail.replace('"', "")
                thumbnail = thumbnail.replace(',', "")
                thumbnail = thumbnail.strip()
                plugintools.log("thumbnail= "+thumbnail)
                if thumbnail == "":
                    thumbnail = params.get("thumbnail")

                plugintools.add_item( action="movshare" , title = title + ' [COLOR orange][Movshare][/COLOR]' , url = url , fanart = fanart , thumbnail = thumbnail , folder = False , isPlayable = True )

            if url.find("movreel")>= 0:
                url = url.replace(",", "")
                plugintools.log("url= "+url)
                fanart = params.get("extra")
                thumbnail = plugintools.find_single_match(entry,'"image":(.*?)\n')
                thumbnail = thumbnail.replace('"', "")
                thumbnail = thumbnail.replace(',', "")
                thumbnail = thumbnail.strip()
                plugintools.log("thumbnail= "+thumbnail)
                if thumbnail == "":
                    thumbnail = params.get("thumbnail")

                plugintools.add_item( action="movreel" , title = title + ' [COLOR orange][Movreel][/COLOR]' , url = url , fanart = fanart , thumbnail = thumbnail , folder = False , isPlayable = True )

            if url.find("videobam")>= 0:
                url = url.replace(",", "")
                plugintools.log("url= "+url)
                fanart = params.get("extra")
                thumbnail = plugintools.find_single_match(entry,'"image":(.*?)\n')
                thumbnail = thumbnail.replace('"', "")
                thumbnail = thumbnail.replace(',', "")
                thumbnail = thumbnail.strip()
                plugintools.log("thumbnail= "+thumbnail)
                if thumbnail == "":
                    thumbnail = params.get("thumbnail")

                plugintools.add_item( action="videobam" , title = title + ' [COLOR orange][Videobam][/COLOR]' , url = url , fanart = fanart , thumbnail = thumbnail , folder = False , isPlayable = True )

            if url.find("videoweed")>= 0:
                url = url.replace(",", "")
                plugintools.log("url= "+url)
                fanart = params.get("extra")
                thumbnail = plugintools.find_single_match(entry,'"image":(.*?)\n')
                thumbnail = thumbnail.replace('"', "")
                thumbnail = thumbnail.replace(',', "")
                thumbnail = thumbnail.strip()
                plugintools.log("thumbnail= "+thumbnail)
                if thumbnail == "":
                    thumbnail = params.get("thumbnail")

                plugintools.add_item( action="videoweed" , title = title + ' [COLOR orange][Videoweed][/COLOR]' , url = url , fanart = fanart , thumbnail = thumbnail , folder = False , isPlayable = True )

            if url.find("streamable")>= 0:
                url = url.replace(",", "")
                plugintools.log("url= "+url)
                fanart = params.get("extra")
                thumbnail = plugintools.find_single_match(entry,'"image":(.*?)\n')
                thumbnail = thumbnail.replace('"', "")
                thumbnail = thumbnail.replace(',', "")
                thumbnail = thumbnail.strip()
                plugintools.log("thumbnail= "+thumbnail)
                if thumbnail == "":
                    thumbnail = params.get("thumbnail")

                plugintools.add_item( action="streamable" , title = title + ' [COLOR orange][Streamable][/COLOR]' , url = url , fanart = fanart , thumbnail = thumbnail , folder = False , isPlayable = True )

            if url.find("rocvideo")>= 0:
                url = url.replace(",", "")
                plugintools.log("url= "+url)
                fanart = params.get("extra")
                thumbnail = plugintools.find_single_match(entry,'"image":(.*?)\n')
                thumbnail = thumbnail.replace('"', "")
                thumbnail = thumbnail.replace(',', "")
                thumbnail = thumbnail.strip()
                plugintools.log("thumbnail= "+thumbnail)
                if thumbnail == "":
                    thumbnail = params.get("thumbnail")

                plugintools.add_item( action="rocvideo" , title = title + ' [COLOR orange][Rocvideo][/COLOR]' , url = url , fanart = fanart , thumbnail = thumbnail , folder = False , isPlayable = True )

            if url.find("realvid")>= 0:
                url = url.replace(",", "")
                plugintools.log("url= "+url)
                fanart = params.get("extra")
                thumbnail = plugintools.find_single_match(entry,'"image":(.*?)\n')
                thumbnail = thumbnail.replace('"', "")
                thumbnail = thumbnail.replace(',', "")
                thumbnail = thumbnail.strip()
                plugintools.log("thumbnail= "+thumbnail)
                if thumbnail == "":
                    thumbnail = params.get("thumbnail")

                plugintools.add_item( action="realvid" , title = title + ' [COLOR orange][Realvid][/COLOR]' , url = url , fanart = fanart , thumbnail = thumbnail , folder = False , isPlayable = True )

            if url.find("netu")>= 0:
                url = url.replace(",", "")
                plugintools.log("url= "+url)
                fanart = params.get("extra")
                thumbnail = plugintools.find_single_match(entry,'"image":(.*?)\n')
                thumbnail = thumbnail.replace('"', "")
                thumbnail = thumbnail.replace(',', "")
                thumbnail = thumbnail.strip()
                plugintools.log("thumbnail= "+thumbnail)
                if thumbnail == "":
                    thumbnail = params.get("thumbnail")

                plugintools.add_item( action="netu" , title = title + ' [COLOR orange][Netu][/COLOR]' , url = url , fanart = fanart , thumbnail = thumbnail , folder = False , isPlayable = True )

            if url.find("videomega")>= 0:
                url = url.replace(",", "")
                plugintools.log("url= "+url)
                fanart = params.get("extra")
                thumbnail = plugintools.find_single_match(entry,'"image":(.*?)\n')
                thumbnail = thumbnail.replace('"', "")
                thumbnail = thumbnail.replace(',', "")
                thumbnail = thumbnail.strip()
                plugintools.log("thumbnail= "+thumbnail)
                if thumbnail == "":
                    thumbnail = params.get("thumbnail")

                plugintools.add_item( action="videomega" , title = title + ' [COLOR orange][Videomega][/COLOR]' , url = url , fanart = fanart , thumbnail = thumbnail , folder = False , isPlayable = True )

            if url.find("video.tt")>= 0:
                url = url.replace(",", "")
                plugintools.log("url= "+url)
                fanart = params.get("extra")
                thumbnail = plugintools.find_single_match(entry,'"image":(.*?)\n')
                thumbnail = thumbnail.replace('"', "")
                thumbnail = thumbnail.replace(',', "")
                thumbnail = thumbnail.strip()
                plugintools.log("thumbnail= "+thumbnail)
                if thumbnail == "":
                    thumbnail = params.get("thumbnail")

                plugintools.add_item( action="videott" , title = title + ' [COLOR orange][Video.tt][/COLOR]' , url = url , fanart = fanart , thumbnail = thumbnail , folder = False , isPlayable = True )

            if url.find("flashx.tv")>= 0:
                url = url.replace(",", "")
                plugintools.log("url= "+url)
                fanart = params.get("extra")
                thumbnail = plugintools.find_single_match(entry,'"image":(.*?)\n')
                thumbnail = thumbnail.replace('"', "")
                thumbnail = thumbnail.replace(',', "")
                thumbnail = thumbnail.strip()
                plugintools.log("thumbnail= "+thumbnail)
                if thumbnail == "":
                    thumbnail = params.get("thumbnail")

                plugintools.add_item( action="flashx" , title = title + ' [COLOR orange][Flashx][/COLOR]' , url = url , fanart = fanart , thumbnail = thumbnail , folder = False , isPlayable = True )

            if url.find("turbovideos")>= 0:
                url = url.replace(",", "")
                plugintools.log("url= "+url)
                fanart = params.get("extra")
                thumbnail = plugintools.find_single_match(entry,'"image":(.*?)\n')
                thumbnail = thumbnail.replace('"', "")
                thumbnail = thumbnail.replace(',', "")
                thumbnail = thumbnail.strip()
                plugintools.log("thumbnail= "+thumbnail)
                if thumbnail == "":
                    thumbnail = params.get("thumbnail")

                plugintools.add_item( action="turbovideos" , title = title + ' [COLOR orange][Turbovideos][/COLOR]' , url = url , fanart = fanart , thumbnail = thumbnail , folder = False , isPlayable = True )             

            if url.find("ok.ru")>= 0:
                url = url.replace(",", "")
                plugintools.log("url= "+url)
                fanart = params.get("extra")
                thumbnail = plugintools.find_single_match(entry,'"image":(.*?)\n')
                thumbnail = thumbnail.replace('"', "")
                thumbnail = thumbnail.replace(',', "")
                thumbnail = thumbnail.strip()
                plugintools.log("thumbnail= "+thumbnail)
                if thumbnail == "":
                    thumbnail = params.get("thumbnail")

                plugintools.add_item( action="flashx" , title = title + ' [COLOR orange][Ok.ru][/COLOR]' , url = url , fanart = fanart , thumbnail = thumbnail , folder = False , isPlayable = True )

            if url.find("vidto.me")>= 0:
                url = url.replace(",", "")
                plugintools.log("url= "+url)
                fanart = params.get("extra")
                thumbnail = plugintools.find_single_match(entry,'"image":(.*?)\n')
                thumbnail = thumbnail.replace('"', "")
                thumbnail = thumbnail.replace(',', "")
                thumbnail = thumbnail.strip()
                plugintools.log("thumbnail= "+thumbnail)
                if thumbnail == "":
                    thumbnail = params.get("thumbnail")

                plugintools.add_item( action="vidtome" , title = title + ' [COLOR orange][Vidto.me][/COLOR]' , url = url , fanart = fanart , thumbnail = thumbnail , folder = False , isPlayable = True )                  

            else:
                # Canales no reproducibles en XBMC (de momento)
                params["url"]=url
                server_rtmp(params)
                server = params.get("server")
                plugintools.add_item( action="play" , title = '[COLOR red] ' + title + ' ['+ server + '][/COLOR]' , url = params.get("url") , fanart = fanart , thumbnail = thumbnail , folder = False , isPlayable = True )

                if title == "":
                    plugintools.log("url= "+url)
                    fanart = params.get("extra")
                    thumbnail = plugintools.find_single_match(entry,'"image":(.*?)\n')
                    thumbnail = thumbnail.replace('"', "")
                    thumbnail = thumbnail.replace(',', "")
                    thumbnail = thumbnail.strip()
                    plugintools.log("thumbnail= "+thumbnail)
                    if thumbnail == "":
                        thumbnail = params.get("thumbnail")





def youtube_playlist(params):
    plugintools.log('[%s %s].youtube_playlist %s' % (addonName, addonVersion, repr(params)))

    data = plugintools.read( params.get("url") )

    pattern = ""
    matches = plugintools.find_multiple_matches(data,"<entry(.*?)</entry>")

    for entry in matches:
        plugintools.log("entry="+entry)

        title = plugintools.find_single_match(entry,"<titl[^>]+>([^<]+)</title>")
        plot = plugintools.find_single_match(entry,"<media\:descriptio[^>]+>([^<]+)</media\:description>")
        thumbnail = plugintools.find_single_match(entry,"<media\:thumbnail url='([^']+)'")
        url = plugintools.find_single_match(entry,"<content type\='application/atom\+xml\;type\=feed' src='([^']+)'/>")
        fanart = __art__ + 'youtube.png'

        plugintools.add_item( action="youtube_videos" , title=title , plot=plot , url=url , thumbnail=thumbnail , fanart=fanart , folder=True )
        plugintools.log("fanart= "+fanart)



# Muestra todos los vídeos del playlist de Youtube
def youtube_videos(params):
    plugintools.log('[%s %s].youtube_videos %s' % (addonName, addonVersion, repr(params)))

    # Fetch video list from YouTube feed
    data = plugintools.read( params.get("url") )
    plugintools.log("data= "+data)

    # Extract items from feed
    pattern = ""
    matches = plugintools.find_multiple_matches(data,"<entry(.*?)</entry>")

    for entry in matches:
        plugintools.log("entry="+entry)

        # Not the better way to parse XML, but clean and easy
        title = plugintools.find_single_match(entry,"<titl[^>]+>([^<]+)</title>")
        title = title.replace("I Love Handball | ","")
        plot = plugintools.find_single_match(entry,"<summa[^>]+>([^<]+)</summa")
        thumbnail = plugintools.find_single_match(entry,"<media\:thumbnail url='([^']+)'")
        fanart = __art__+'youtube.png'
        video_id = plugintools.find_single_match(entry,"http\://www.youtube.com/watch\?v\=([0-9A-Za-z_-]{11})")
        url = 'plugin://plugin.video.youtube/play/?video_id='+videoid                       

        # Appends a new item to the xbmc item list
        plugintools.runAddon( action="runPlugin" , title=title , plot=plot , url=url , thumbnail=thumbnail , fanart=fanart , isPlayable=True, folder=False )



def peliseries(params):
    plugintools.log('[%s %s].peliseries %s' % (addonName, addonVersion, repr(params)))

    # Abrimos archivo remoto
    url = params.get("url")
    filepelis = urllib2.urlopen(url)

    # Creamos archivo local para pegar las entradas
    plot = params.get("plot")
    plot = parser_title(plot)
    if plot == "":
        title = params.get("title")
        title = parser_title(title)
        filename = title + ".m3u"
        fh = open(__playlists__ + filename, "wb")
    else:
        filename = params.get("plot") + ".m3u"
        fh = open(__playlists__ + filename, "wb")

    plugintools.log("filename= "+filename)
    url = params.get("url")
    plugintools.log("url= "+url)


    #open the file for writing
    fw = open(__playlists__ + filename, "wb")

    #open the file for writing
    fh = open(__playlists__ + 'filepelis.m3u', "wb")
    fh.write(filepelis.read())

    fh.close()

    fw = open(__playlists__ + filename, "wb")
    fr = open(__playlists__ + 'filepelis.m3u', "r")
    fr.seek(0)
    num_items = len(fr.readlines())
    print num_items
    fw.seek(0)
    fr.seek(0)
    data = fr.readline()
    fanart = params.get("extra")
    thumbnail = params.get("thumbnail")
    fw.write('#EXTM3U:"background"='+fanart+',"thumbnail"='+thumbnail)
    fw.write("#EXTINF:-1,[COLOR lightyellow][I]playlists / " + filename + '[/I][/COLOR]' + '\n\n')
    i = 0

    while i <= num_items:

        if data == "":
            data = fr.readline()
            data = data.strip()
            plugintools.log("data= " +data)
            i = i + 1
            print i
            continue

        elif data.find("http") >= 0 :
            data = data.split("http")
            chapter = data[0]
            chapter = chapter.strip()
            url = "http" + data[1]
            url = url.strip()
            plugintools.log("url= "+url)
            fw.write("\n#EXTINF:-1," + chapter + '\n')
            fw.write(url + '\n\n')
            data = fr.readline()
            plugintools.log("data= " +data)
            i = i + 1
            print i
            continue

        else:
            data = fr.readline()
            data = data.strip()
            plugintools.log("data= "+data)
            i = i + 1
            print i
            continue

    fw.close()
    fr.close()
    params["ext"]='m3u'
    filename = filename.replace(".m3u", "")
    params["plot"]=filename
    params["title"]=filename

    # Capturamos de nuevo thumbnail y fanart

    os.remove(__playlists__ + 'filepelis.m3u')
    simpletv_items(params)


def tinyurl(params):
    plugintools.log('[%s %s].tinyurl %s' % (addonName, addonVersion, repr(params)))

    url = params.get("url")
    url_getlink = 'http://www.getlinkinfo.com/info?link=' +url

    plugintools.log("url_fixed= "+url_getlink)

    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    body,response_headers = plugintools.read_body_and_headers(url_getlink, headers=request_headers)
    plugintools.log("data= "+body)

    r = plugintools.find_multiple_matches(body, '<dt class="link-effective-url">Effective URL</dt>(.*?)</a></dd>')
    xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('pld.visiontv', "Redireccionando enlace...", 3 , __art__+'icon.png'))

    for entry in r:
        entry = entry.replace("<dd><a href=", "")
        entry = entry.replace('rel="nofollow">', "")
        entry = entry.split('"')
        entry = entry[1]
        entry = entry.strip()
        plugintools.log("vamos= "+entry)

        if entry.startswith("http"):
            plugintools.play_resolved_url(entry)



# Conexión con el servicio longURL.org para obtener URL original
def longurl(params):
    plugintools.log('[%s %s].longurl %s' % (addonName, addonVersion, repr(params)))

    # Control de modo de vista predefinido
    show = params.get("extra")
    if show != "":
        plugintools.modo_vista(show)

    url = params.get("url")
    url_getlink = 'http://api.longurl.org/v2/expand?url=' +url

    plugintools.log("url_fixed= "+url_getlink)

    try:
        request_headers=[]
        request_headers.append(["User-Agent","Application-Name/3.7"])
        body,response_headers = plugintools.read_body_and_headers(url_getlink, headers=request_headers)
        plugintools.log("data= "+body)

        # <long-url><![CDATA[http://85.25.43.51:8080/DE_skycomedy?u=euorocard:p=besplatna]]></long-url>
        # xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('pld.visiontv', "Redireccionando enlace...", 3 , __art__+'icon.png'))
        longurl = plugintools.find_single_match(body, '<long-url>(.*?)</long-url>')
        longurl = longurl.replace("<![CDATA[", "")
        longurl = longurl.replace("]]>", "")
        plugintools.log("longURL= "+longurl)
        if longurl.startswith("http"):
            plugintools.play_resolved_url(longurl)

    except:
        play(params)




# name and create our window 
class opentxt(xbmcgui.Window): 
    # and define it as self
    def __init__(self):
        # add picture control to our window (self) with a hardcoded path name to picture
        self.addControl(xbmcgui.ControlImage(0,0,720,480, __art__+ 'logo.png'))
        # store our window as a short variable for easy of use
        W = BlahMainWindow()
        # run our window we created with our background jpeg image
        W.doModal()
        # after the window is closed, Destroy it.
        del W



def encode_url(url):
    url_fixed= urlencode(url)
    print url_fixed



def m3u_items(title):
    #plugintools.log('[%s %s].m3u_items %s' % (addonName, addonVersion, title))	
    thumbnail = __art__ + 'icon.png'
    fanart = __art__ + 'fanart.jpg'
    only_title = title

    if title.find("tvg-logo") >= 0:
        thumbnail = re.compile('tvg-logo="(.*?)"').findall(title)
        num_items = len(thumbnail)
        print 'num_items',num_items
        if num_items == 0:
            thumbnail = 'm3u.png'
        else:
            thumbnail = thumbnail[0]
            #plugintools.log("thumbnail= "+thumbnail)

        only_title = only_title.replace('tvg-logo="', "")
        only_title = only_title.replace(thumbnail, "")

    if title.find("tvg-wall") >= 0:
        fanart = re.compile('tvg-wall="(.*?)"').findall(title)
        fanart = fanart[0]
        only_title = only_title.replace('tvg-wall="', "")
        only_title = only_title.replace(fanart, "")

    try:
        if title.find("imdb") >= 0:
            imdb = re.compile('imdb="(.*?)"').findall(title)
            imdb = imdb[0]
            only_title = only_title.replace('imdb="', "")
            only_title = only_title.replace(imdb, "")
        else:
            imdb = ""
    except:
        imdb = ""

    try:
        if title.find("dir") >= 0:
            dir = re.compile('dir="(.*?)"').findall(title)
            dir = dir[0]
            only_title = only_title.replace('dir="', "")
            only_title = only_title.replace(dir, "")
        else:
            dir = ""
    except:
        dir = ""

    try:
        if title.find("cast") >= 0:
            cast = re.compile('cast="(.*?)"').findall(title)
            cast = cast[0]            
            only_title = only_title.replace('cast="', "")
            only_title = only_title.replace(cast, "")
            
        else:
            cast = ""
    except:
        cast = ""        

    try:
        if title.find("wri") >= 0:
            writers = re.compile('wri="(.*?)"').findall(title)
            writers = writers[0]
            only_title = only_title.replace('wri="', "")
            only_title = only_title.replace(writers, "")
        else:
            writers = ""
    except:
        writers = ""

    try:
        if title.find("votes") >= 0:
            num_votes = re.compile('votes="(.*?)"').findall(title)
            num_votes = num_votes[0]
            only_title = only_title.replace('votes="', "")
            only_title = only_title.replace(num_votes, "")
        else:
            num_votes = ""
    except:
        num_votes = ""

    try:
        if title.find("plot") >= 0:
            plot = re.compile('plot="(.*?)"').findall(title)
            plot = plot[0]
            only_title = only_title.replace('plot="', "")
            only_title = only_title.replace(plot, "")
        else:
            plot = ""
    except:
        plot = ""

    try:
        if title.find("genre") >= 0:
            genre = re.compile('genre="(.*?)"').findall(title)
            genre = genre[0]
            only_title = only_title.replace('genre="', "")
            only_title = only_title.replace(genre, "")
            print 'genre',genre
        else:
            genre = ""
    except:
        genre = ""

    try:
        if title.find("time") >= 0:
            duration = re.compile('time="(.*?)"').findall(title)
            duration = duration[0]
            only_title = only_title.replace('time="', "")
            only_title = only_title.replace(duration, "")
            print 'duration',duration
        else:
            duration = ""
    except:
        duration = ""

    try:
        if title.find("year") >= 0:
            year = re.compile('year="(.*?)"').findall(title)
            year = year[0]
            only_title = only_title.replace('year="', "")
            only_title = only_title.replace(year, "")
            print 'year',year
        else:
            year = ""
    except:
        year = ""

    if title.find("group-title") >= 0:
        cat = re.compile('group-title="(.*?)"').findall(title)
        if len(cat) == 0:
            cat = ""
        else:
            cat = cat[0]
        plugintools.log("m3u_categoria= "+cat)
        only_title = only_title.replace('group-title=', "")
        only_title = only_title.replace(cat, "")
    else:
        cat = ""

    if title.find("tvg-id") >= 0:
        title = title.replace('”', '"')
        title = title.replace('“', '"')
        tvgid = re.compile('tvg-id="(.*?)"').findall(title)
        print 'tvgid',tvgid
        tvgid = tvgid[0]
        plugintools.log("m3u_categoria= "+tvgid)
        only_title = only_title.replace('tvg-id=', "")
        only_title = only_title.replace(tvgid, "")
    else:
        tvgid = ""

    if title.find("tvg-name") >= 0:
        tvgname = re.compile('tvg-name="(.*?)').findall(title)
        tvgname = tvgname[0]
        plugintools.log("m3u_categoria= "+tvgname)
        only_title = only_title.replace('tvg-name=', "")
        only_title = only_title.replace(tvgname, "")
    else:
        tvgname = ""

    only_title = only_title.replace('"', "").strip()
    return thumbnail, fanart, cat, only_title, tvgid, tvgname, imdb, duration, year, dir, writers, genre, num_votes, plot, cast


def xml_skin():
    plugintools.log('[%s %s].xml_skin ' % (addonName, addonVersion))

    mastermenu = plugintools.get_setting("mastermenu")
    xmlmaster = plugintools.get_setting("xmlmaster")
    SelectXMLmenu = plugintools.get_setting("SelectXMLmenu")

    # values="Default|Pastebin|Personalizado"
    if xmlmaster == 'true':
        if SelectXMLmenu == '0':  # Default skin
            mastermenu = 'https://dl.dropbox.com/s/hw7f9kp4unz169f/PLDVisionTV21pld.xml'
            plugintools.log("[pld.visiontv.xml_skin: "+SelectXMLmenu)
            
            # Control para ver la intro de pld.visiontv
            ver_intro = plugintools.get_setting("ver_intro")
            if ver_intro == "true":
                xbmc.Player(xbmc.PLAYER_CORE_AUTO).play(art + 'intro.mp4')
				
        elif SelectXMLmenu == '1':  # Pastebin
            id_pastebin = plugintools.get_setting("id_pastebin")
            if id_pastebin == "":
                plugintools.log("[pld.visiontv.xml_skin: No definido")
                mastermenu = 'https://dl.dropbox.com/s/hw7f9kp4unz169f/PLDVisionTV21pld.xml'
            else:
                mastermenu = 'http://pastebin.com/raw.php?i=' +id_pastebin
                plugintools.log("[pld.visiontv.xml_skin: "+mastermenu)

                # Control para ver la intro de pld.visiontv
                ver_intro = plugintools.get_setting("ver_intro")
                if ver_intro == "true":
                    xbmc.Player(xbmc.PLAYER_CORE_AUTO).play(art + 'intro.mp4')                
				
        elif SelectXMLmenu == '2':   # Personalizado
            id_pastebin = plugintools.get_setting("id_pastebin")
            if id_pastebin == "":
                mastermenu = plugintools.get_setting("mastermenu")
                if mastermenu == "":
                    plugintools.log("[pld.visiontv.xml_skin: No definido")
                    mastermenu = 'https://dl.dropbox.com/s/hw7f9kp4unz169f/PLDVisionTV21pld.xml'
                    
                    # Control para ver la intro de pld.visiontv
                    ver_intro = plugintools.get_setting("ver_intro")
                    if ver_intro == "true":
                        xbmc.Player(xbmc.PLAYER_CORE_AUTO).play(art + 'intro.mp4')
						
    else:
        # xmlmaster = False (no activado), menú por defecto
        mastermenu = 'https://dl.dropbox.com/s/hw7f9kp4unz169f/PLDVisionTV21pld.xml'

        # Control para ver la intro de pld.visiontv
        ver_intro = plugintools.get_setting("ver_intro")
        if ver_intro == "true":
            xbmc.Player(xbmc.PLAYER_CORE_AUTO).play(art + 'intro.mp4')
						
    return mastermenu


def add_playlist(params):
    plugintools.log('[%s %s].add_playlist %s' % (addonName, addonVersion, repr(params)))
    url_pl1 = plugintools.get_setting("url_pl1")
    url_pl2 = plugintools.get_setting("url_pl2")
    url_pl3 = plugintools.get_setting("url_pl3")

    # Sintaxis de la lista online. Acciones por defecto (M3U)
    action_pl1 = "getfile_http"
    action_pl2 = "getfile_http"
    action_pl3 = "getfile_http"

    tipo_pl1 = plugintools.get_setting('tipo_pl1')
    tipo_pl2 = plugintools.get_setting('tipo_pl2')
    tipo_pl3 = plugintools.get_setting('tipo_pl3')

    if tipo_pl1 == '0':
        action_pl1 = 'getfile_http'

    if tipo_pl1 == '1':
        action_pl1 = 'plx_items'

    if tipo_pl2 == '0':
        action_pl2 = 'getfile_http'

    if tipo_pl2 == '1':
        action_pl2 = 'plx_items'

    if tipo_pl3 == '0':
        action_pl3 = 'getfile_http'

    if tipo_pl3 == '1':
        action_pl3 = 'plx_items'

    title_pl1 = plugintools.get_setting("title_pl1")
    title_pl2 = plugintools.get_setting("title_pl2")
    title_pl3 = plugintools.get_setting("title_pl3")

    plugintools.add_item(action="", title='[COLOR lightyellow]Listas online:[/COLOR]', url="", folder=False, isPlayable=False)

    if url_pl1 != "":
        if title_pl1 == "":
            title_pl1 = "[COLOR lightyellow]Lista online 1[/COLOR]"
        plugintools.add_item(action=action_pl1, title='  '+title_pl1, url=url_pl1, folder=True, isPlayable=False)

    if url_pl2 != "":
        if title_pl2 == "":
            title_pl2 = "[COLOR lightyellow]Lista online 2[/COLOR]"
        plugintools.add_item(action=action_pl2, title='  '+title_pl2, url=url_pl2, folder=True, isPlayable=False)

    if url_pl3 != "":
        if title_pl3 == "":
            title_pl3 == "[COLOR lightyellow]Lista online 3[/COLOR]"
        plugintools.add_item(action=action_pl3, title='  '+title_pl3, url=url_pl3, folder=True, isPlayable=False)


####### Menú lateral ###############


##################################MENU LATERAL######################
class menulateral(xbmcgui.WindowXMLDialog):

    C_CHANNELS_LIST = 6000

    def __init__( self, *args, **kwargs ):
            xbmcgui.WindowXML.__init__(self)
            #self.finalurl = kwargs[ "finalurl" ]
            #self.siglacanal = kwargs[ "siglacanal" ]
            #self.name = kwargs[ "name" ]
            #self.directo = kwargs[ "directo" ]

    def onInit(self):
        self.updateChannelList()

    def onAction(self, action):
        if action.getId() in [ACTION_PARENT_DIR, ACTION_PREVIOUS_MENU, KEY_NAV_BACK, KEY_CONTEXT_MENU]:
            self.close()
            return

    def onClick(self, controlId):
        if controlId == 4001:
            self.close()
            request_servidores(url,name)

        elif controlId == 40010:
            self.close()
            iniciagravador(self.finalurl,self.siglacanal,self.name,self.directo)

        elif controlId == 203:
            #xbmc.executebuiltin("XBMC.PlayerControl(stop)")
            self.close()

        elif controlId == 6000:
            listControl = self.getControl(self.C_CHANNELS_LIST)
            item = listControl.getSelectedItem()
            nomecanal=item.getProperty('chname')
            self.close()
            request_servidores(url,nomecanal)


        #else:
        #    self.buttonClicked = controlId
        #    self.close()

    def onFocus(self, controlId):
        pass

    def updateChannelList(self):
        idx=-1
        listControl = self.getControl(self.C_CHANNELS_LIST)
        listControl.reset()
        canaison=openfile('canaison')
        canaison=canaison.replace('[','')
        lista=re.compile('B](.+?)/B]').findall(canaison)
        for nomecanal in lista:
            idx=int(idx+1)
            if idx==0: idxaux=' '
            else:
                idxaux='%4s.' % (idx)
                item = xbmcgui.ListItem(idxaux + ' %s' % (nomecanal), iconImage = '')
                item.setProperty('idx', str(idx))
                item.setProperty('chname', '[B]' + nomecanal + '[/B]')
                listControl.addItem(item)

    def updateListItem(self, idx, item):
        channel = self.channelList[idx]
        item.setLabel('%3d. %s' % (idx+1, channel.title))
        item.setProperty('idx', str(idx))

    def swapChannels(self, fromIdx, toIdx):
        if self.swapInProgress: return
        self.swapInProgress = True

        c = self.channelList[fromIdx]
        self.channelList[fromIdx] = self.channelList[toIdx]
        self.channelList[toIdx] = c

        # recalculate weight
        for idx, channel in enumerate(self.channelList):
            channel.weight = idx

        listControl = self.getControl(self.C_CHANNELS_LIST)
        self.updateListItem(fromIdx, listControl.getListItem(fromIdx))
        self.updateListItem(toIdx, listControl.getListItem(toIdx))

        listControl.selectItem(toIdx)
        xbmc.sleep(50)
        self.swapInProgress = False

    def addLink(name,url,iconimage):
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty('fanart_image', "%s/fanart.jpg"%selfAddon.getAddonInfo("path"))
        try:
            if re.search('HD',name) or re.search('1080P',name) or re.search('720P',name):liz.addStreamInfo( 'video', { 'Codec': 'h264', 'width': 1280, 'height': 720 } )
            else: liz.addStreamInfo( 'video', { 'Codec': 'h264', 'width': 600, 'height': 300 } )
        except: pass
        return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)

    def addCanal(name,url,mode,iconimage,total,descricao):
        cm=[]
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&thumb="+urllib.quote_plus(iconimage)
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "overlay":6 ,"plot":descricao} )
        liz.setProperty('fanart_image', "%s/fanart.jpg"%selfAddon.getAddonInfo("path"))
        try:
            if re.search('HD',name) or re.search('1080P',name) or re.search('720P',name):liz.addStreamInfo( 'video', { 'Codec': 'h264', 'width': 1280, 'height': 720 } )
            else: liz.addStreamInfo( 'video', { 'Codec': 'h264', 'width': 600, 'height': 300 } )
        except: pass
        #cm.append(('Adicionar stream preferencial', "XBMC.RunPlugin(%s?mode=%s&name=%s&url=%s)")%(sys.argv[0],)
        liz.addContextMenuItems(cm, replaceItems=False)
        return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False,totalItems=total)

    def addDir(name,url,mode,iconimage,total,descricao,pasta):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "overlay":6 ,"plot":descricao} )
        liz.setProperty('fanart_image', "%s/fanart.jpg"%selfAddon.getAddonInfo("path"))
        return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)

    def clean(text):
        command={'\r':'','\n':'','\t':'','&nbsp;':''}
        regex = re.compile("|".join(map(re.escape, command.keys())))
        return regex.sub(lambda mo: command[mo.group(0)], text)

    def parseDate(dateString):
        try: return datetime.datetime.fromtimestamp(time.mktime(time.strptime(dateString.encode('utf-8', 'replace'), "%Y-%m-%d %H:%M:%S")))
        except: return datetime.datetime.today() - datetime.timedelta(days = 1) #force update



''' Pruebas EPG flotante en modo reproducción
def testejanela(params):
    d = menulateral("menulateral.xml" , home, "Default")
    while xbmc.getCondVisibility('Window.IsActive(videoosd)') == False:
        xbmc.sleep(1000)
        if xbmc.getCondVisibility('Window.IsActive(videoosd)'):
            d.doModal()
        else:
            pass
'''


# Esta función añade coletilla de tipo de enlace a los multilink
def multiparse_title(title, url):

    if url.startswith("serie") == True:
        if url.find("seriesflv") >= 0:
            title = title + ' [COLOR lightyellow][I][Series[B]FLV[/B]][/I][/COLOR]'
        if url.find("seriesyonkis") >= 0:
            title = title + ' [COLOR lightyellow][I][Series[B]Yonkis[/B]][/I][/COLOR]'
        if url.find("seriesadicto") >= 0:
            title = title + ' [COLOR lightyellow][I][Series[B]Adicto[/B]][/I][/COLOR]'
        if url.find("seriesblanco") >= 0:
            title = title + ' [COLOR lightyellow][I][Series[B]Blanco[/B]][/I][/COLOR]'

    if url.startswith("peli") == True:
        if url.find("oranline") >= 0:
            title = title + ' [COLOR lightyellow][I][Oranline][/I][/COLOR]'
        if url.find("seriesyonkis") >= 0:
            title = title + ' [COLOR lightyellow][I][PelisAdicto][/I][/COLOR]'    
        if url.find("pordede") >= 0:
            title = title + ' [COLOR lightyellow][I][Pordede][/I][/COLOR]'  

    elif url.startswith("goear") == True:
        title = title + ' [COLOR lightyellow][I][goear][/I][/COLOR]'

    elif url.startswith("http") == True:
        if url.find("allmyvideos") >= 0:
            title = title + ' [COLOR lightyellow][I][Allmyvideos][/I][/COLOR]'

        elif url.find("streamcloud") >= 0:
            title = title + ' [COLOR lightyellow][I][Streamcloud][/I][/COLOR]'

        elif url.find("vidspot") >= 0:
            title = title + ' [COLOR lightyellow][I][Vidspot][/I][/COLOR]'

        elif url.find("played.to") >= 0:
            title = title + ' [COLOR lightyellow][I][Played.to][/I][/COLOR]'

        elif url.find("vk.com") >= 0:
            title = title + ' [COLOR lightyellow][I][Vk][/I][/COLOR]'

        elif url.find("nowvideo") >= 0:
            title = title + ' [COLOR lightyellow][I][Nowvideo.sx][/I][/COLOR]'

        elif url.find("tumi") >= 0:
            title = title + ' [COLOR lightyellow][I][Tumi][/I][/COLOR]'

        elif url.find("streamin.to") >= 0:
            title = title + ' [COLOR lightyellow][I][Streamin.to][/I][/COLOR]'

        elif url.find("veehd") >= 0:
            title = title + ' [COLOR lightyellow][I][Veehd][/I][/COLOR]'
            
        elif url.find("tumi.tv") >= 0:
            title = title + ' [COLOR lightyellow][I][Tumi][/I][/COLOR]'       

        elif url.find("novamov") >= 0:
            title = title + ' [COLOR lightyellow][I][Novamov][/I][/COLOR]'

        elif url.find("gamovideo") >= 0:
            title = title + ' [COLOR lightyellow][I][Gamovideo][/I][/COLOR]'            
        
        elif url.find("moevideos") >= 0:
            title = title + ' [COLOR lightyellow][I][Moevideos][/I][/COLOR]'

        elif url.find("movshare") >= 0:
            title = title + ' [COLOR lightyellow][I][Movshare][/I][/COLOR]'

        elif url.find("powvideo") >= 0:
            title = title + ' [COLOR lightyellow][I][Powvideo][/I][/COLOR]'

        elif url.find("mail.ru") >= 0:
            title = title + ' [COLOR lightyellow][I][Mail.ru][/I][/COLOR]'          

        elif url.find("videobam") >= 0:
            title = title + ' [COLOR lightyellow][I][Videobam][/I][/COLOR]'

        elif url.find("videoweed") >= 0:
            title = title + ' [COLOR lightyellow][I][Videoweed][/I][/COLOR]'

        elif url.find("streamable") >= 0:
            title = title + ' [COLOR lightyellow][I][Streamable][/I][/COLOR]'

        elif url.find("rocvideo") >= 0:
            title = title + ' [COLOR lightyellow][I][Rocvideo][/I][/COLOR]'

        elif url.find("realvid") >= 0:
            title = title + ' [COLOR lightyellow][I][Realvid][/I][/COLOR]'

        elif url.find("netu") >= 0:
            title = title + ' [COLOR lightyellow][I][Netu][/I][/COLOR]'

        elif url.find("videomega") >= 0:
            title = title + ' [COLOR lightyellow][I][Videomega][/I][/COLOR]'

        elif url.find("video.tt") >= 0:
            title = title + ' [COLOR lightyellow][I][Video.tt][/I][/COLOR]'

        elif url.find("flashx.tv") >= 0:
            title = title + ' [COLOR lightyellow][I][Flashx][/I][/COLOR]'

        elif url.find("ok.ru") >= 0:
            title = title + ' [COLOR lightyellow][I][Ok.ru][/I][/COLOR]'               

        elif url.find("www.youtube.com") >= 0:
            title = title + ' [COLOR lightyellow][I][Youtube][/I][/COLOR]'

        elif url.find(".m3u8") >= 0:
            title = title + ' [COLOR lightyellow][I][M3u8][/I][/COLOR]'

        elif url.find(".cbz") >= 0:
            title = title + ' [COLOR lightyellow][I][CBZ][/I][/COLOR]'

        elif url.find(".cbr") >= 0:
            title = title + ' [COLOR lightyellow][I][CBR][/I][/COLOR]'            

        elif url.find(".pdf") >= 0:
            title = title + ' [COLOR lightyellow][I][PDF][/I][/COLOR]'         

    elif url.startswith("udp") == True:
        title = title + ' [COLOR lightyellow][I][udp][/I][/COLOR]'

    elif url.startswith("rtp") == True:
        title = title + ' [COLOR lightyellow][I][rtp][/I][/COLOR]'

    elif url.startswith("mms") == True:
        title = title + ' [COLOR lightyellow][I][mms][/I][/COLOR]'

    elif url.startswith("plugin") == True:
        if url.find("youtube") >= 0 :
            title = title + ' [COLOR lightyellow][I][Youtube][/I][/COLOR]'

        elif url.find("mode=1") >= 0 :
            title = title + ' [COLOR lightyellow][I][Acestream][/I][/COLOR]'

        elif url.find("mode=2") >= 0 :
            title = title + ' [COLOR lightyellow][I][Sopcast][/I][/COLOR]'

    elif url.startswith("magnet") == True:
        title = title + ' [COLOR lightyellow][I][Torrent][/I][/COLOR]'

    elif url.startswith("torrent") == True:
        title = title + ' [COLOR lightyellow][I][Torrent][/I][/COLOR]'        

    elif url.startswith("sop") == True:
        title = title + ' [COLOR lightyellow][I][Sopcast][/I][/COLOR]'

    elif url.startswith("ace") == True:
        title = title + ' [COLOR lightyellow][I][Acestream][/I][/COLOR]'

    elif url.startswith("yt") == True:
        if url.startswith("yt_playlist") == True:
            title = title + ' [COLOR lightyellow][I][Youtube Playlist][/I][/COLOR]'

        elif url.startswith("yt_channel") == True:
            title = title + ' [COLOR lightyellow][I][Youtube Channel][/I][/COLOR]'

    elif url.startswith("rtmp") == True or url.startswith("rtsp") == True:

        if url.find("iguide.to") >= 0:
            title = title + ' [COLOR lightyellow][I][iguide][/I][/COLOR]'
        elif url.find("freetvcast.pw") >= 0:
            title = title + ' [COLOR lightyellow[I][freetvcast][/I][/COLOR]'
        elif url.find("pageUrl=http://streamingfreetv") >= 0:
            title = title + ' [COLOR lightyellow][I][streamingfreetv][/I][/COLOR]'
        elif url.find("9stream") >= 0:
            title = title + ' [COLOR lightyellow][I][9stream][/I][/COLOR]'
        elif url.find("freebroadcast") >= 0:
            title = title + ' [COLOR lightyellow][I][freebroadcast][/I][/COLOR]'
        elif url.find("cast247") >= 0:
            title = title + ' [COLOR lightyellow][I][cast247][/I][/COLOR]'
        elif url.find("castalba") >= 0:
            title = title + ' [COLOR lightyellow][I][castalba][/I][/COLOR]'
        elif url.find("direct2watch") >= 0:
            title = title + ' [COLOR lightyellow][I][direct2watch][/I][/COLOR]'
        elif url.find("vaughnlive") >= 0:
            title = title + ' [COLOR lightyellow][I][vaughnlive][/I][/COLOR]'
        elif url.find("sawlive") >= 0:
            title = title + ' [COLOR lightyellow][I][sawlive][/I][/COLOR]'
        elif url.find("shidurlive") >= 0:
            title = title + ' [COLOR lightyellow][I][shidurlive][/I][/COLOR]'
        elif url.find("vercosas") >= 0:
            title = title + ' [COLOR lightyellow][I][vercosas][/I][/COLOR]'
        elif url.find("pageUrl=http://rdmcast.com") >= 0:
            title = title + ' [COLOR lightyellow][I][rdmcast][/I][/COLOR]'
        elif url.find("businessapp1") >= 0:
            title = title + ' [COLOR lightyellow][I][businessapp1][/I][/COLOR]'
        elif url.find("miplayer.net") >= 0:
            title = title + ' [COLOR lightyellow][I][miplayer.net][/I][/COLOR]'            
        elif url.find("janjua") >= 0:
            title = title + ' [COLOR lightyellow][I][janjua][/I][/COLOR]'
        elif url.find("mips") >= 0:
            title = title + ' [COLOR lightyellow][I][mips][/I][/COLOR]'
        elif url.find("broadcastlive") >= 0:
            title = title + ' [COLOR lightyellow][I][broadcastlive][/I][/COLOR]'             
        else:
            title = title + ' [COLOR lightyellow][I][rtmp][/I][/COLOR]'

    elif url.startswith("img") == True:
        title = title + ' [COLOR lightyellow][I][IMG][/I][/COLOR]'

    elif url.startswith("bum") == True:
        title = title + ' [COLOR lightyellow][I][BUM+][/I][/COLOR]'                               
        
    else:
	title = title + ' [COLOR lightyellow][I][Unknown][/I][/COLOR]'

    return title


def launch_magnet(url):
    plugintools.log('[%s %s] launch_magnet... %s' % (addonName, addonVersion, url))    

    addon_magnet = plugintools.get_setting("addon_magnet")
    plugintools.log("addon_magnet= "+addon_magnet)
    #url = urllib.unquote_plus(url)
    if addon_magnet == "0":  # Stream (por defecto)
        url = 'plugin://plugin.video.stream/play/'+url
    elif addon_magnet == "1":  # Pulsar
        url = 'plugin://plugin.video.pulsar/play?uri=' + url
    elif addon_magnet == "2":  # Kmediatorrent
        url = 'plugin://plugin.video.kmediatorrent/play/'+url

    plugintools.log("Magnet URL= "+url)
    return url



def launch_torrent(url):
    plugintools.log('[%s %s] launch_torrent... %s' % (addonName, addonVersion, url))    

    addon_torrent = plugintools.get_setting("addon_torrent")
    print addon_torrent
    #url = urllib.quote_plus(url)
    if addon_torrent == "0":  # Stream (por defecto)
        url = 'plugin://plugin.video.stream/play/'+url
    elif addon_torrent == "1":  # Pulsar
        url = 'plugin://plugin.video.pulsar/play?uri=' + url
        
    return url


def launch_kickass(params):
    plugintools.log('[%s %s].launch_kickass %s' % (addonName, addonVersion, repr(params)))

    url = params.get("url")
    addon_magnet = plugintools.get_setting("addon_magnet")
    if addon_magnet == "0":  # Stream (por defecto)
        url = 'plugin://plugin.video.stream/play/'+url
    elif addon_magnet == "1":  # Pulsar
        url = 'plugin://plugin.video.pulsar/play?uri=' + url

    play(url)


def open_settings(self):  #Open addon settings    
    selfAddon.openSettings()
    params = plugintools.get_params()
    main_list(params)

    

def cbx_reader(params):
    plugintools.log('[%s %s].CBX_reader %s' % (addonName, addonVersion, repr(params)))
    mediafire = 0
    url = params.get("url")
    show= params.get("extra")
    datamovie = {}
    datamovie["Plot"] = params.get("plot")
    url_fixed = url.split("/");num_splits = int(len(url_fixed)) - 1
    filename = url_fixed[num_splits]    
    title = params.get("title")
    title = parser_title(title).strip()
    filename = filename.replace(".cbz","").replace(".cbr", "").replace("?", "").replace("+", "").replace(" ", "_").strip()
    if params.get("extra") == "my_albums":  # Control para abrir álbumes desde "My albums"
        plugintools.log("Extra!")
        dst_folder = __temp__ + title
        mediafire = 0
        if title.endswith("cbr") == True:
            filename = filename.replace(".cbr", "")
        elif title.endswith("cbz") == True:
            filename = filename.replace(".cbz", "")
        dst_folder = __playlists__ + title
        dst_folder = dst_folder.replace(" ", "_").strip()
        print 'dst_folder 6655',dst_folder
        if url.endswith("cbr") == True:
            filename = filename+'.cbr'              
        elif url.endswith("cbz") == True:
            filename = filename+'.cbz'
        print os.path.exists(dst_folder)
        if os.path.exists(dst_folder) == "False":        
            plugintools.log("Creando directorio... "+dst_folder)
            os.mkdir(dst_folder)
        if not os.path.exists(dst_folder):
            os.makedirs(dst_folder)
        src_cbx = __temp__ + title
        show = 'thumbnails'
        print 'src 6668',src_cbx
        print 'dst 6669',dst_folder
        modo_vista(show)
    else:  # Control para abrir álbumes desde una lista M3U
        dst_folder = __temp__ + filename
        dst_folder = dst_folder.replace(" ", "_").strip()
        dst_folder = dst_folder.replace("?", "").replace("%", "").replace("download=1", "").strip()
        print 'dst_folder 6675',dst_folder
        if url.endswith("cbr") == True:
            filename = filename+'.cbr'              
        elif url.endswith("cbz") == True:
            filename = filename+'.cbz'
        elif url.find("copy.com") >= 0:
            filename = filename.replace("?", "").replace("download=1", "").replace("%", "").strip()
            if url.find("cbz") >= 0:
                filename = filename+'.cbz'
            elif url.find("cbr") >= 0:
                filename = filename+'.cbr'
        if os.path.exists(dst_folder) == "False":        
            plugintools.log("Creando directorio... "+dst_folder)
            os.mkdir(dst_folder)
        if not os.path.exists(dst_folder):
            os.makedirs(dst_folder)
        src_cbx = __temp__ + filename
        print 'src 6441',src_cbx
        print 'dst 6442',dst_folder
        modo_vista(show)
        

    
    if url.find("mediafire") >= 0:  # ***************** MEDIAFIRE *****************
        plugintools.log("Iniciando descarga de Mediafire")
        src_cbx = __temp__ + filename+'.cbr'  # ExtensiÃ³n .rar para que no salte iteraciÃ³n posterior de url.endswith("url") == True en linea 6223

        # Solicitud de página web
        mediafire = 1
        url = params.get("url")
        data = plugintools.read(url)

        # Espera un segundo y vuelve a cargar
        percent = 0
        progreso = xbmcgui.DialogProgress()
        progreso.create("pld.visiontv", "Iniciando descarga de [I]Mediafire[/I] en [I][B]playlists/tmp[/B][/I]\n")
        msg = "Obteniendo URL de descarga...\n"
        percent = 25
        progreso.update(percent, "", msg, "")        

        time.sleep(1)  # Espera de 1 seg para obtener URL de Mediafire...
        plugintools.log("Iniciando lectura de "+url)
        data = plugintools.read(url)
        url_mediafire = plugintools.find_single_match(data, 'kNO \= "([^"]+)"')
        plugintools.log("URL Mediafire 1= "+url_mediafire)
        if url_mediafire == "":
            time.sleep(1)
            data = plugintools.read(url)
            matches = plugintools.find_multiple_matches(data, 'kNO \= "([^"]+)"')
            for entry in matches:
                plugintools.log("entry= "+entry)
                if entry != "":
                    url_mediafire = entry
                    plugintools.log("URL Mediafire 2= "+url_mediafire)                    
                    msg = "URL Mediafire: [I]"+url_mediafire+"[/I]\n Iniciando descarga..."
                    percent = 50
                    progreso.update(percent, "", msg, "")

        # Comprobamos si no existe el archivo ya descargado e iniciamos descarga...
        if os.path.isfile(src_cbx) is False:
            msg = "Leyendo datos de: [I]"+url_mediafire+"[/I]\n"
            percent = 50
            progreso.update(percent, "", msg, "")            
            response = urllib2.urlopen(url_mediafire)
            body = response.read()
            file_compressed = filename + '.cbr'
            fh = open(__temp__ + file_compressed, "wb")  #open the file for writing
            fh.write(body)  # read from request while writing to file

            # Thumbnail y fanart
            thumbnail = params.get("thumbnail")
            if thumbnail == "":
                thumbnail = dst_folder+'\\00.jpg'
                if thumbnail == "":
                    thumbnail = 'http://ww1.prweb.com/prfiles/2010/07/13/3676844/Slideshow512.png'        
            fanart = dst_folder+'\\00.jpg'
            plugintools.log("fanart1= "+fanart)
            if fanart == "":
                fanart = dst_folder+'\\00.jpg'
                plugintools.log("fanart2= "+fanart)
                if fanart == "":
                    fanart = __art__+'slideshow.png'
                    plugintools.log("fanart3= "+fanart)
        else:
            msg = "Archivo ya descargado. Abriendo páginas... "
            percent = 75
            progreso.update(percent, "", msg, "")
            mediafire = 1

    elif url.endswith("cbz") == True or url.endswith("cbr") == True or url.find("copy.com") >= 0:  # *** Descarga de archivos CBR y CBZ ***
        plugintools.log("Iniciando descarga de Dropbox/Copy.com")
        if os.path.isfile(src_cbx) is False:
            percent = 0
            progreso = xbmcgui.DialogProgress()
            if url.endswith("cbz") == True:
                progreso.create("pld.visiontv", "Descargando archivo CBZ en [I][B]playlists/tmp[/B][/I]")
            elif url.endswith("cbr") == True:
                progreso.create("pld.visiontv", "Descargando archivo CBR en [I][B]playlists/tmp[/B][/I]")
            elif url.find("copy.com") >= 0:
                if url.find("cbr") >= 0:
                    progreso.create("pld.visiontv", "Descargando archivo CBR de Copy.com en [I][B]playlists/tmp[/B][/I]")
                elif url.find("cbz") >= 0:
                    progreso.create("pld.visiontv", "Descargando archivo CBZ de Copy.com en [I][B]playlists/tmp[/B][/I]")
            # response = urllib2.urlopen(url)
            # body = response.read()
            if url.startswith("cbr:") == True:
                url = url.replace("cbr:", "")
                #filename = filename + '.cbr'
                plugintools.log("Iniciando descarga desde..."+url)
            elif url.startswith("cbz:") == True:
                url = url.replace("cbz:", "")
                #filename = filename + '.cbz'
                plugintools.log("Iniciando descarga desde..."+url)            
            h=urllib2.HTTPHandler(debuglevel=0)  # Iniciamos descarga...
            request = urllib2.Request(url)
            opener = urllib2.build_opener(h)
            urllib2.install_opener(opener)

            fh = open(__temp__ + filename, "wb")  #open the file for writing
            size_local = fh.tell()            
            try:
                connected = opener.open(request)
                meta = connected.info()
                filesize = meta.getheaders("Content-Length")[0]
                filesize_mb = str(int(filesize) / 1024000) + " MB"                
                try:
                    while int(size_local) < int(filesize):
                        blocksize = 100*1024
                        bloqueleido = connected.read(blocksize)                        
                        if progreso.iscanceled():
                            progreso.close()
                            fh.close()
                        msg = "[COLOR gold][B]"+filename+"[/B][/COLOR][COLOR lightgreen][I] ("+filesize_mb+")[/I][/COLOR]\n"+str(size_local)+" de "+str(filesize)+" bytes\n"
                        #print filesize
                        #print size_local
                        percent_fixed = float((float(size_local) * 100)/(float(filesize) * 100) * 100)
                        percent = int(percent_fixed)
                        progreso.update(percent, "" , msg, "")
                        fh.write(bloqueleido)  # read from request while writing to file
                        size_local = fh.tell()                        
                except:
                    percent = 100
                    progreso.update(percent)
                    
            except urllib2.HTTPError,e:
                progreso.close()
                fh.close()
                
            fh.close()
            progreso.close()
    
    page = 1
    if src_cbx.endswith("cbz") == True:  # Descompresión archivos CBZ
        #unzipper = ziptools()
        #unzipper.extract(src_cbx, dst_folder, params)
        print src_cbx
        print dst_folder
        xbmc.executebuiltin('XBMC.Extract('+src_cbx+','+dst_folder+')')
        xbmc.sleep(1000)
        thumbnail = params.get("thumbnail")
        if thumbnail == "":
            thumbnail = dst_folder+'\\00.jpg'
            if thumbnail == "":
                thumbnail = 'http://ww1.prweb.com/prfiles/2010/07/13/3676844/Slideshow512.png'        
        fanart = dst_folder+'\\00.jpg'
        plugintools.log("fanart1= "+fanart)
        if fanart == "":
            fanart = dst_folder+'\\00.jpg'
            plugintools.log("fanart2= "+fanart)
            if fanart == "":
                fanart = __art__+'slideshow.png'
                plugintools.log("fanart3= "+fanart)

    elif src_cbx.endswith("cbr") == True:  # DescompresiÃ³n archivos CBR
        xbmc.executebuiltin('XBMC.Extract('+src_cbx+','+dst_folder+')')
        xbmc.sleep(1000)
        thumbnail = params.get("thumbnail")
        if thumbnail == "":
            thumbnail = dst_folder+'\\00.jpg'
            if thumbnail == "":
                thumbnail = 'http://ww1.prweb.com/prfiles/2010/07/13/3676844/Slideshow512.png'        
        fanart = dst_folder+'\\00.jpg'
        plugintools.log("fanart1= "+fanart)
        if fanart == "":
            fanart = dst_folder+'\\00.jpg'
            plugintools.log("fanart2= "+fanart)
            if fanart == "":
                fanart = __art__+'slideshow.png'
                plugintools.log("fanart3= "+fanart)
        if mediafire == 1:
            percent = 100
            msg = "Proceso finalizado! ;)"
            progreso.update(percent, "", msg, "")
            fh.close()
            progreso.close()   

    # Abriendo páginas...
    plugintools.add_item(action="show_cbx", title="[COLOR orange][B]Ayuda: [/COLOR][COLOR white]Atajos de teclado[/B][/COLOR]", url=__art__+'help_cbx.png', info_labels = datamovie , thumbnail = __art__+'help_cbx.png', fanart = fanart, folder=False, isPlayable=False)    
    plugintools.add_item(action="slide_cbx", title="[COLOR orange][B]Slideshow: [/COLOR][COLOR white]"+title+"[/B][/COLOR]", url=dst_folder, page=str(page), extra=dst_folder , info_labels = datamovie , thumbnail = thumbnail, fanart = fanart, folder=False, isPlayable=False)    
    plugintools.log("dst_folder= "+dst_folder)
    for f in os.listdir(dst_folder):
        file_path = os.path.join(dst_folder, f)
        print f
        if os.path.isfile(file_path):
            thumbnail = cbx_pages+str(page)+'.png'
            plugintools.add_item(action="show_cbx", title="Página "+str(page), url=dst_folder+'\\'+f, page=str(page), extra=dst_folder , info_labels = datamovie , thumbnail = thumbnail , fanart = fanart , folder=False, isPlayable=False)
            page = page + 1     
                    
					
def slide_cbx(params):
    plugintools.log('[%s %s].slide_CBX %s' % (addonName, addonVersion, repr(params)))
    xbmc.executebuiltin("Container.SetViewMode(500)")
    url = params.get("url")
    dst_folder = params.get("extra")
    page = params.get("page")
    plugintools.log("url= "+url)
    page_to_start = dst_folder + '\\'+str(page)
    xbmc.executebuiltin( "SlideShow("+dst_folder+"," +page+")" )
    


def show_cbx(params):
    plugintools.log('[%s %s].show_CBX %s' % (addonName, addonVersion, repr(params)))
    xbmc.executebuiltin("Container.SetViewMode(500)")
    url = params.get("url")
    dst_folder = params.get("extra")
    page = params.get("page")
    plugintools.log("url= "+url)
    page_to_start = dst_folder + '\\'+str(page)    
    xbmc.executebuiltin( "ShowPicture("+url+")" )    
    

def show_image(params):
    plugintools.log('[%s %s].show_image %s' % (addonName, addonVersion, repr(params)))
    url=params.get("url")
    url = url.replace("img:", "")

    plugintools.log("Iniciando descarga desde..."+url)
    h=urllib2.HTTPHandler(debuglevel=0)  # Iniciamos descarga...
    request = urllib2.Request(url)
    opener = urllib2.build_opener(h)
    urllib2.install_opener(opener)
    filename = url.split("/")
    max_len = len(filename)
    max_len = int(max_len) - 1
    filename = filename[max_len]
    fh = open(__temp__ + filename, "wb")  #open the file for writing
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
    imagen = __temp__ + filename
    print imagen
    xbmc.executebuiltin( "ShowPicture("+imagen+")" )  


def devil_call(params):
    plugintools.log("[%s %s] devil_call " % (addonName, addonVersion))
    
    url = params.get("url")
    url = xbmc.executebuiltin('XBMC.RunPlugin('+url+')')
    print url
    plugintools.play_resolved_url(url)
    
run()


