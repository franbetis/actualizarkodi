# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Regex de Pordede para PLD.VisionTV
# Version 0.1 (Adaptación del parser de pelisalacarta)
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
import scrapertools
import requests

import traceback

from resources.tools.resolvers import *

playlists = xbmc.translatePath(os.path.join('special://userdata/playlists', ''))
temp = xbmc.translatePath(os.path.join('special://userdata/playlists/tmp', ''))

thumbnail = 'https://fbcdn-profile-a.akamaihd.net/hprofile-ak-xpa1/v/t1.0-1/p160x160/1391713_1426997127520069_470169989_n.png?oh=e88efae907434c6b447ad00d5607c953&oe=563DA15D&__gda__=1446384267_065b4440be84df1da5d5017cb7d5745f'
fanart = 'http://1.bp.blogspot.com/-KyT4YY-bcUY/VLf3_liTSWI/AAAAAAAABSI/mHgCLqONXfc/s1600/apertura-pordede.jpg'

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")

DEFAULT_HEADERS = []
DEFAULT_HEADERS.append( ["User-Agent","Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; es-ES; rv:1.9.2.12) Gecko/20101026 Firefox/3.6.12"] )
DEFAULT_HEADERS.append( ["Referer","http://www.pordede.com"] )


def pordede0(params):
    plugintools.log('[%s %s] ---> Launching Pordede regex... <--- ' % (addonName, addonVersion))

    if plugintools.get_setting("pordede_user") == "":
        plugintools.add_item(action="", title="Habilita tu cuenta de pordede en la configuración", folder=False, isPlayable=False)

    else:
        login_pordede()
        
    
def login_pordede():
    plugintools.log('[%s %s] ---> Iniciando login en Pordede.com... <--- ' % (addonName, addonVersion))

    params = plugintools.get_params()    
    url = "http://www.pordede.com/site/login"
    post = "LoginForm[username]="+plugintools.get_setting("pordede_user")+"&LoginForm[password]="+plugintools.get_setting("pordede_pwd")
    headers = DEFAULT_HEADERS[:]
    regex = params.get("extra")
    try:
        if os.path.exists(temp+'pordede.com') is True:
            print "Eliminando carpeta caché..."
            os.remove(temp+'pordede.com')
    except: pass

    data = scrapertools.cache_page(url,headers=headers,post=post);print data    
    if data != "":
        login_info = plugintools.find_single_match(data, '<div class="friendMini shadow"(.*?)</div>')
        user_title = plugintools.find_single_match(login_info, 'title="([^"]+)')
        user_thumb = plugintools.find_single_match(login_info, 'src="([^"]+)')
        if regex == "":
            plugintools.log("regex= "+regex)
            plugintools.add_item(action="menuseries", title='Usuario: [COLOR lightyellow][I]'+user_title+'[/I][/COLOR]', url="", thumbnail=user_thumb, fanart=fanart, folder=True, isPlayable=False)
            plugintools.add_item(action="menuseries", title="Series", url="", thumbnail=thumbnail, fanart=fanart, folder=True, isPlayable=False)
            plugintools.add_item(action="menupeliculas", title="Películas", url="", thumbnail=thumbnail, fanart=fanart, folder=True, isPlayable=False)
            plugintools.add_item(action="listas_sigues", title="Listas que sigues", url="http://www.pordede.com/lists/following", thumbnail=thumbnail, fanart=fanart, folder=True, isPlayable=False)
            plugintools.add_item(action="tus_listas", title="Tus listas", url="http://www.pordede.com/lists/yours", thumbnail=thumbnail, fanart=fanart, folder=True, isPlayable=False)
            plugintools.add_item(action="listas_sigues", title="Top listas", url="http://www.pordede.com/lists", thumbnail=thumbnail, fanart=fanart, folder=True, isPlayable=False)


def menuseries(params):
    plugintools.add_item(action="peliculas", title="Novedades", url="http://www.pordede.com/series/loadmedia/offset/0/showlist/hot", thumbnail=thumbnail, fanart=fanart, folder=True, isPlayable=False)
    plugintools.add_item(action="generos", title="Por géneros", url="http://www.pordede.com/series", thumbnail=thumbnail, fanart=fanart, folder=True, isPlayable=False)
    plugintools.add_item(action="peliculas", title="Siguiendo", url="http://www.pordede.com/series/following", thumbnail=thumbnail, fanart=fanart, folder=True, isPlayable=False)
    plugintools.add_item(action="siguientes", title="Siguientes Capítulos", url="http://www.pordede.com/index2.php", thumbnail=thumbnail, fanart=fanart, folder=True, isPlayable=False)
    plugintools.add_item(action="peliculas", title="Favoritas", url="http://www.pordede.com/series/favorite", thumbnail=thumbnail, fanart=fanart, folder=True, isPlayable=False)
    plugintools.add_item(action="peliculas", title="Pendientes", url="http://www.pordede.com/series/pending", thumbnail=thumbnail, fanart=fanart, folder=True, isPlayable=False)
    plugintools.add_item(action="peliculas", title="Terminadas", url="http://www.pordede.com/series/seen", thumbnail=thumbnail, fanart=fanart, folder=True, isPlayable=False)
    plugintools.add_item(action="peliculas", title="Recomendadas", url="http://www.pordede.com/series/recommended", thumbnail=thumbnail, fanart=fanart, folder=True, isPlayable=False)
    plugintools.add_item(action="search_pdd", title="Buscar...", url="http://www.pordede.com/series", thumbnail=thumbnail, fanart=fanart, folder=True, isPlayable=False)


def menupeliculas(params):
    plugintools.add_item(action="peliculas", title="Novedades", url="http://www.pordede.com/pelis/loadmedia/offset/0/showlist/hot", thumbnail=thumbnail, fanart=fanart, folder=True, isPlayable=False)
    plugintools.add_item(action="generos", title="Por géneros", url="http://www.pordede.com/pelis", thumbnail=thumbnail, fanart=fanart, folder=True, isPlayable=False)
    plugintools.add_item(action="peliculas", title="Favoritas", url="http://www.pordede.com/pelis/favorites", thumbnail=thumbnail, fanart=fanart, folder=True, isPlayable=False)
    plugintools.add_item(action="peliculas", title="Pendientes", url="http://www.pordede.com/pelis/pending", thumbnail=thumbnail, fanart=fanart, folder=True, isPlayable=False)
    plugintools.add_item(action="peliculas", title="Vistas", url="http://www.pordede.com/pelis/seen", thumbnail=thumbnail, fanart=fanart, folder=True, isPlayable=False)
    plugintools.add_item(action="peliculas", title="Recomendadas", url="http://www.pordede.com/pelis/recommended", thumbnail=thumbnail, fanart=fanart, folder=True, isPlayable=False)
    plugintools.add_item(action="search_pdd", title="Buscar...", url="http://www.pordede.com/pelis", thumbnail=thumbnail, fanart=fanart, folder=True, isPlayable=False)

def generos(params):
    plugintools.log('[%s %s] ---> Pordede: Por géneros... <--- ' % (addonName, addonVersion))

    # Descarga la pagina
    url = params.get("url")
    headers = DEFAULT_HEADERS[:]
    data = scrapertools.cache_page(url, headers=headers)
    #plugintools.log("data= "+data)

    # Extrae las entradas (carpetas)
    data = plugintools.find_single_match(data,'<div class="section genre">(.*?)</div>')
    #plugintools.log("data= "+data)
    patron  = '<a class="mediaFilterLink" data-value="([^"]+)" href="([^"]+)">([^<]+)<span class="num">\((\d+)\)</span></a>'
    matches = plugintools.find_multiple_matches(data, patron)
    for textid,scrapedurl,scrapedtitle,cuantos in matches:
        title = scrapedtitle.strip()+" ("+cuantos+")"
        
        if "/pelis" in url:
            url = "http://www.pordede.com/pelis/loadmedia/offset/0/genre/"+textid.replace(" ","%20")+"/showlist/all"
        else:
            url = "http://www.pordede.com/series/loadmedia/offset/0/genre/"+textid.replace(" ","%20")+"/showlist/all"
        plugintools.add_item(action="peliculas", title=title, url=url, thumbnail=thumbnail, fanart=fanart, folder=True, isPlayable=False)

    try: shutil.rmtree(temp + 'pordede.com', ignore_errors=False, onerror=None)
    except: pass

def peliculas(params):
    plugintools.log("[%s %s] Pordede: Listando películas... %s " % (addonName, addonVersion, repr(params)))

    url = params.get("url")

    # Descarga la pagina
    headers = DEFAULT_HEADERS[:]
    headers.append(["X-Requested-With","XMLHttpRequest"])
    data = scrapertools.cache_page(url,headers=headers)
    #plugintools.log("data= "+data)
    
    # Extrae las entradas (carpetas)
    items = plugintools.find_multiple_matches(data, 'defaultLink(.*?)data-action')
    for entry in items:
        entry=entry.replace('\\', '').replace("u00e1", "á").replace("u00ed", "í").replace("u00e9", "é").replace("u00f3", "ó").replace("u00a1", "¡").replace("00f1", "ñ")
        #plugintools.log("entry= "+entry)
        title_item = plugintools.find_single_match(entry, 'title=(.*?)>')
        url_item = plugintools.find_single_match(entry, 'href=(.*?)>')
        thumb_item = plugintools.find_single_match(entry, 'http(.*?)png')
        year_item = plugintools.find_single_match(entry, 'year(.*?)<')
        rank_item = plugintools.find_single_match(entry, '</i>(.*?)</span>')
        title_item=title_item.replace("\\", "").replace('"', "")
        url_item=url_item.replace("\\", "").replace('"', "");url_item='http://www.pordede.com'+url_item;url_item=url_item.replace("/peli/","/links/view/slug/")+"/what/peli"
        thumb_item='http'+thumb_item+'png'
        year_item=year_item.replace("\\", "").replace('"', "").replace(">", "")
        rank_item=rank_item.replace("\\", "").replace('"', "")
        #plugintools.log("title_item= "+title_item)
        #plugintools.log("url_item= "+url_item)
        #plugintools.log("thumb_item= "+thumb_item)
        #plugintools.log("year_item= "+year_item)
        #plugintools.log("rank_item= "+rank_item)

        title_fixed= '[COLOR white]'+title_item+' [/COLOR][COLOR lightyellow][I]('+year_item+') [/COLOR][COLOR lightgreen] ['+rank_item+'][/I][/COLOR]'

        plugintools.add_item(action="pdd_findvideos", title=title_fixed, url=url_item, thumbnail=thumb_item, fanart=fanart, folder=True, isPlayable=False)

def pdd_findvideos(params):
    plugintools.log("[%s %s] Pordede: Buscando enlaces... %s " % (addonName, addonVersion, repr(params)))

    if params.get("extra") == "regex":
        try: shutil.rmtree(temp + 'pordede.com', ignore_errors=False, onerror=None)
        except: pass
        params["regex"]='regex'
        login_pordede()
        url_peli = params.get("page")

        # Descarga la pagina
        headers = DEFAULT_HEADERS[:]
        headers.append(["X-Requested-With","XMLHttpRequest"])
        data = scrapertools.cache_page(url_peli,headers=headers)
        #plugintools.log("data= "+data)

        fanart = plugintools.find_single_match(data, 'src=(.*?)>').replace("\\", "").replace('"', "").replace(".png/", ".png").strip()
        thumbnail = fanart.replace("big", "").strip()
        plugintools.log("fanart= "+fanart)
        plugintools.log("thumbnail= "+thumbnail)
        
    url = params.get("url")
    if thumbnail == "":  # Control por si no se ejecuta regex o no captura thumbnail correctamente
        thumbnail = params.get("thumbnail")

    # Descarga la pagina
    headers = DEFAULT_HEADERS[:]
    data = scrapertools.cache_page(url,headers=headers)
    #plugintools.log("data="+data)

    sesion = plugintools.find_single_match(data,'SESS = "([^"]+)";')
    #plugintools.log("sesion="+sesion)

    patron  = '<a target="_blank" class="a aporteLink(.*?)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    itemlist = []

    i = 1
    plugintools.add_item(action="", title='[COLOR lightyellow][B]'+params.get("title")+'[/B][/COLOR]', url="", thumbnail = thumbnail, fanart=fanart, folder=False, isPlayable=False)
    for match in matches:
        #plugintools.log("match= "+match)        
        jdown = scrapertools.find_single_match(match,'<div class="jdownloader">[^<]+</div>')
        if jdown != '': # Descartar enlaces veronline/descargar
            continue

        idiomas = re.compile('<div class="flag([^"]+)">([^<]+)</div>',re.DOTALL).findall(match)
        idioma_0 = (idiomas[0][0].replace("&nbsp;","").strip() + " " + idiomas[0][1].replace("&nbsp;","").strip()).strip()
        if len(idiomas) > 1:
            idioma_1 = (idiomas[1][0].replace("&nbsp;","").strip() + " " + idiomas[1][1].replace("&nbsp;","").strip()).strip()
            idioma = idioma_0 + ", " + idioma_1
        else:
            idioma_1 = ''
            idioma = idioma_0

        idioma=idioma.replace("spanish", "ESP").replace("english", "ENG").replace("spanish SUB", "SUB-ESP").replace("english SUB", "SUB-ENG")

        calidad_video = plugintools.find_single_match(match,'<div class="linkInfo quality"><i class="icon-facetime-video"></i>([^<]+)</div>').strip()
        #plugintools.log("calidad_video="+calidad_video)
        calidad_audio = plugintools.find_single_match(match,'<div class="linkInfo qualityaudio"><i class="icon-headphones"></i>([^<]+)</div>').strip()
        #plugintools.log("calidad_audio="+calidad_audio)
        thumb_servidor = plugintools.find_single_match(match,'<div class="hostimage"[^<]+<img\s*src="([^"]+)">').strip()
        #plugintools.log("thumb_servidor="+thumb_servidor)
        nombre_servidor = plugintools.find_single_match(thumb_servidor,"popup_([^\.]+)\.png").strip()
        #plugintools.log("nombre_servidor="+nombre_servidor)
              
        title = "[COLOR white]Op. "+str(i)+'. [/COLOR][COLOR lightgreen][I]['+nombre_servidor+"] [/I][/COLOR][COLOR gold] ("+idioma+") [/COLOR][COLOR lightyellow][I][Video: "+calidad_video.strip()+", Audio: "+calidad_audio.strip()+"][/COLOR][/I] "
        i = i + 1

        cuenta = []
        valoracion = 0
        for idx, val in enumerate(['1', '2', 'report']):
            nn = plugintools.find_single_match(match,'<span\s+data-num="([^"]+)"\s+class="defaultPopup"\s+href="/likes/popup/value/'+val+'/')
            if nn != '0' and nn != '':
                cuenta.append(nn + ' ' + ['[COLOR green]OK[/COLOR]', '[COLOR red]KO[/COLOR]', 'rep'][idx])
                valoracion += int(nn) if val == '1' else -int(nn)

        if len(cuenta) > 0:
            title += ' [COLOR white](' + ', '.join(cuenta) + ')[/COLOR]'

        item_url = plugintools.find_single_match(match,'href="([^"]+)"')
        item_url = 'http://www.pordede.com'+item_url
        #thumbnail = thumb_servidor
        #plugintools.log("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        plugintools.add_item(action="pordede_play", title=title, url=item_url, thumbnail=thumbnail, fanart=fanart, extra=sesion+"|"+item_url, folder=False, isPlayable=True)

def pordede_play(params):
    plugintools.log("[%s %s] Pordede: Buscando enlaces... %s " % (addonName, addonVersion, repr(params)))

    # Marcar como visto
    #checkseen(item.extra.split("|")[1])

    # Hace la llamada
    headers = DEFAULT_HEADERS[:]
    headers.append( ["Referer" , params.get("extra").split("|")[1] ])

    data = scrapertools.cache_page(params.get("url"),post="_s="+params.get("extra").split("|")[0],headers=headers)
    url = plugintools.find_single_match(data,'<p class="links">\s+<a href="([^"]+)" target="_blank"')
    url = 'http://www.pordede.com'+url
    
    headers = DEFAULT_HEADERS[:]
    headers.append( ["Referer" , url ])

    media_url = scrapertools.downloadpage(url,headers=headers,header_to_get="location",follow_redirects=False)
    #plugintools.log("media_url="+media_url)

    if media_url.find("allmyvideos") >= 0:
        params=plugintools.get_params()
        params["url"]=media_url
        allmyvideos(params)
    elif media_url.find("vidspot") >= 0:
        params=plugintools.get_params()
        params["url"]=media_url
        vidspot(params)
    elif media_url.find("played.to") >= 0:
        params=plugintools.get_params()
        params["url"]=media_url
        playedto(params)
    elif media_url.find("streamcloud") >= 0:
        params=plugintools.get_params()
        params["url"]=media_url
        streamcloud(params)
    elif media_url.find("nowvideo") >= 0:
        params=plugintools.get_params()
        params["url"]=media_url
        nowvideo(params)
    elif media_url.find("streamin.to") >= 0:
        params=plugintools.get_params()
        params["url"]=media_url
        streaminto(params)
    elif media_url.find("vk") >= 0:
        params=plugintools.get_params()
        params["url"]=media_url
        vk(params)
    elif media_url.find("tumi") >= 0:
        params=plugintools.get_params()
        params["url"]=media_url
        tumi(params)
    elif media_url.find("veehd") >= 0:
        params=plugintools.get_params()
        params["url"]=media_url
        veehd(params)
    elif media_url.find("powvideo") >= 0:
        params=plugintools.get_params()
        params["url"]=media_url
        powvideo(params)        
    elif media_url.find("novamov") >= 0:
        params=plugintools.get_params()
        params["url"]=media_url
        novamov(params)
    elif media_url.find("gamovideo") >= 0:
        params=plugintools.get_params()
        params["url"]=media_url
        gamovideo(params)
    elif media_url.find("moevideos") >= 0:
        params=plugintools.get_params()
        params["url"]=media_url
        moevideos(params)
    elif media_url.find("movshare") >= 0:
        params=plugintools.get_params()
        params["url"]=media_url
        movshare(params)
    elif media_url.find("movreel") >= 0:
        params=plugintools.get_params()
        params["url"]=media_url
        movreel(params)
    elif media_url.find("videobam") >= 0:
        params=plugintools.get_params()
        params["url"]=media_url
        videobam(params)
    elif media_url.find("videoweed") >= 0:
        params=plugintools.get_params()
        params["url"]=media_url
        videoweed(params)
    elif media_url.find("streamable") >= 0:
        params=plugintools.get_params()
        params["url"]=media_url
        streamable(params)
    elif media_url.find("rocvideo") >= 0:
        params=plugintools.get_params()
        params["url"]=media_url
        rocvideo(params)
    elif media_url.find("realvid") >= 0:
        params=plugintools.get_params()
        params["url"]=media_url
        realvid(params)
    elif media_url.find("netu") >= 0:
        params=plugintools.get_params()
        params["url"]=media_url
        netu(params)
    elif media_url.find("videomega") >= 0:
        params=plugintools.get_params()
        params["url"]=media_url
        videomega(params)
    elif media_url.find("video.tt") >= 0:
        params=plugintools.get_params()
        params["url"]=media_url
        videott(params)
    elif media_url.find("flashx.tv") >= 0:
        params=plugintools.get_params()
        params["url"]=media_url
        flashx(params)          

        
