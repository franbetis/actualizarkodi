# -*- coding: utf-8 -*-
#------------------------------------------------------------
# PLD.VisionTV Linker de SeriesFLV.com
# Version 0.3 (26.05.2016)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Gracias a la librería plugintools de Jesús (www.mimediacenter.info)


import os
import sys
import urllib
import urllib2
import re
import time

import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin

import re,urllib,urllib2,sys
import plugintools
import requests
from resources.tools.resolvers import *
from resources.tools.media_analyzer import *

from __main__ import *

__playlists__= xbmc.translatePath(os.path.join('special://home/userdata/playlists', ''))
__temp__ = xbmc.translatePath(os.path.join('special://home/userdata/playlists/tmp', ''))

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")

thumbnail = 'http://m1.paperblog.com/i/249/2490697/seriesflv-mejor-alternativa-series-yonkis-L-2whffw.jpeg'
fanart = 'http://media.tvalacarta.info/pelisalacarta/squares/seriesflv.png'
referer = 'http://www.seriesflv.net/'
web = 'http://www.seriesflv.net/'

sc = "[COLOR white]";ec = "[/COLOR]"
sc2 = "[COLOR palegreen]";ec2 = "[/COLOR]"
sc3 = "[COLOR seagreen]";ec3 = "[/COLOR]"
sc4 = "[COLOR red]";ec4 = "[/COLOR]"
sc5 = "[COLOR yellowgreen]";ec5 = "[/COLOR]"
version = " [0.3]"


def lista_capis(params):
    plugintools.log('[%s %s] Linker SeriesFlv %s' % (addonName, addonVersion, repr(params)))

    plugintools.add_item(action="",url="",title="[COLOR lightblue][B]Linker SeriesFlv"+version+"[/B][COLOR lightblue]"+sc4+"[I] *** PLD.VisionTV  ***[/I]"+ec4,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
    
    url = params.get("url")
    data = jump_cloudflare(url)
    
    logo = plugintools.find_single_match(data,'<img title=".*?src="([^"]+)"')
    if logo =="": logo = thumbnail  
    title = plugintools.find_single_match(data,'<h1 class="off">([^<]+)</h1>').replace('\\','') 
    votos = plugintools.find_single_match(data,'<span id="reviewCount">(.*?)<')
    if votos =="": votos = 'N/D'
    punt = plugintools.find_single_match(data,'<meta itemprop="ratingValue" content="([^"]+)"')
    if punt =="": punt = 'N/D'
    year = plugintools.find_single_match(data,'<td>Año.*?<td>(.*?)</td>')
    if year =="": year = 'N/D'
    bloq_temp =plugintools.find_single_match(data,'<div class="temporadas m1">(.*?)<div id="lista" class="color1 ma1">')
    n_temp = plugintools.find_multiple_matches(bloq_temp,'<a class="color1 on ma1 font2".*?">Temporada(.*?)<')
    n_temp = n_temp[-1].strip()
    if n_temp =="": n_temp = 'N/D'
    bloq_genr = plugintools.find_single_match(data,'<td>Géneros(.*?)</tr>')
    n_genr = plugintools.find_multiple_matches(bloq_genr,'href=".*?">(.*?)<')
    genr = seriesflv_genr(n_genr)
    bloq_pais = plugintools.find_single_match(data,'<td>País </td>(.*?)/td>')
    pais = plugintools.find_multiple_matches(bloq_pais,'<img src=".*?">(.*?)<')
    try:
        pais = pais[-1].strip()
    except: pais = 'N/D'
    sinopsis = plugintools.find_single_match(data,'<p class="color7">(.*?)</p>').replace('\&quot;','"')
    if sinopsis =="": sinopsis = 'N/D'

    datamovie = {
    'season': sc3+'[B]Temporadas Disponibles: [/B]'+ec3+sc+str(n_temp)+', '+ec,
    'votes': sc3+'[B]Votos: [/B]'+ec3+sc+str(votos)+', '+ec,
    'rating': sc3+'[B]Puntuación: [/B]'+ec3+sc+str(punt)+', '+ec,
    'genre': sc3+'[B]Género: [/B]'+ec3+sc+str(genr)+', '+ec,
    'year': sc3+'[B]Año: [/B]'+ec3+sc+str(year)+', '+ec,
    'country': sc3+'[B]País: [/B]'+ec3+sc+str(pais)+'[CR]'+ec,
    'sinopsis': sc3+'[B]Sinopsis: [/B]'+ec3+sc+str(sinopsis)+ec}
    
    datamovie["plot"]=datamovie["season"]+datamovie["votes"]+datamovie["rating"]+datamovie["genre"]+datamovie["year"]+datamovie["country"]+datamovie["sinopsis"]

    plugintools.add_item(action="",url="",title=sc5+"[B]"+title+"[/B]"+ec5,info_labels=datamovie,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)

    patron_temp = '<a class="color1 on ma1 font2"(.*?)/a>'
    item_temp = re.compile(patron_temp,re.DOTALL).findall(data)
    for temp in item_temp:
        url = plugintools.find_single_match(temp,'href="([^"]+)"')
        name_temp = plugintools.find_single_match(temp,'.html">(.*?)<')
        plugintools.addPeli(action="seriesflv_linker_capit",url=url,title=sc2+name_temp+' >>'+ec2,info_labels=datamovie,thumbnail=logo,fanart=fanart,folder=True,isPlayable=False)

def seriesflv_linker_capit(params):
    plugintools.log('[%s %s] Linker SeriesFlv %s' % (addonName, addonVersion, repr(params)))

    plugintools.add_item(action="",url="",title="[COLOR lightblue][B]Linker SeriesFlv"+version+"[/B][COLOR lightblue]"+sc4+"[I] *** PLD.VisionTV  ***[/I]"+ec4,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)

    url = params.get("url")
    data = jump_cloudflare(url)

    bloq_capit = plugintools.find_single_match(data,'<div class="serie-cont left">(.*?)</table>')
    title_temp = plugintools.find_single_match(bloq_capit,'<h1 class="off">(.*?)</h1>').replace('\\','')        
    plugintools.add_item(action="",url="",title=sc2+'[B]'+title_temp+'[/B]'+ec2,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)    
    
    bloq_cover = plugintools.find_single_match(data,'<div class="portada">(.*?)</div>')
    corver = plugintools.find_single_match(bloq_cover,'src="([^"]+)')

    capit= plugintools.find_multiple_matches(bloq_capit,'<td class="sape">(.*?)</tr>')
    for item in capit:
        title_capit = plugintools.find_single_match(item,'class="color4".*?">(.*?)</a>').replace('\\','')
        url_capit = plugintools.find_single_match(item, '<a class="color4" href="([^"]+)"')
        lang = plugintools.find_multiple_matches(item,'http://www.seriesflv.net/images/lang/(.*?).png')
        plugintools.addPeli(action="seriesflv_linker_servers",url=url_capit,title=sc+str(title_capit)+ec,extra=str(title_capit),thumbnail=corver,fanart=fanart,folder=True,isPlayable=False)

def seriesflv_linker_servers(params):
    plugintools.log('[%s %s] Linker SeriesFlv %s' % (addonName, addonVersion, repr(params)))

    plugintools.add_item(action="",url="",title="[COLOR lightblue][B]Linker SeriesFlv"+version+"[/B][COLOR lightblue]"+sc4+"[I] *** PLD.VisionTV ***[/I]"+ec4,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)

    url = params.get("url")
    data = jump_cloudflare(url)
    title_capit = params.get("extra")
    
    bloq_cover = plugintools.find_single_match(data,'<div class="portada">(.*?)</div>')
    corver = plugintools.find_single_match(bloq_cover,'src="([^"]+)')

    bloq_server = plugintools.find_single_match(data,'<div id="enlaces">(.*?)</table>')
    server = plugintools.find_multiple_matches(bloq_server, '<img width="20"(.*?)</tr>')
    
    for item in server:       
        lang = plugintools.find_single_match(item,'src="http://www.seriesflv.net/images/lang/(.*?).png"')
        if lang =='es': lang = sc2+'[I][ESP][/I]'+ec2
        elif lang =='la': lang = sc2+'[I][LAT][/I]'+ec2
        elif lang =='en': lang = sc2+'[I][ENG][/I]'+ec2
        elif lang =='sub': lang= sc2+'[I][SUB][/I]'+ec2 
        else: lang = sc2+'[I][N/D][/I]'+ec2
          
        server_name = plugintools.find_single_match(item,'class="e_server"><img width="16" src="([^"]+)"')
        server_name = server_name.split("domain=")
        server_name = server_name[-1]
        url_redir = plugintools.find_single_match(item,'<td width="84"><a href="([^"]+)"')
        server = video_analyzer(server_name)
        titlefull = sc+str(title_capit)+ec+' '+str(lang)+'  '+sc5+'[I]['+str(server)+'][/I]'+ec5
        plugintools.addPeli(action="getlink_flv",url=url_redir,title=titlefull,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=True)


def getlink_flv(params):
    plugintools.log('[%s %s] Linker SeriesFlv %s' % (addonName, addonVersion, repr(params)))

    url_redir = params.get('url')
    data = jump_cloudflare(url_redir)
    url = plugintools.find_single_match(data,'<a id="continue" href="([^"]+)"')
    url = url.split('=');url_encode = url[-1]
    url_final = urllib.unquote(url_encode) 
    params["url"] = url_final
    resolvers_flv(params)    
    #return url_final

def resolvers_flv(params):
    plugintools.log('[%s %s] Linker SeriesFlv %s' % (addonName, addonVersion, repr(params)))

    url_final = params.get("url")

    if url_final.find("allmyvideos") >= 0: params["url"]=url_final; allmyvideos(params)
    elif url_final.find("streamcloud") >= 0: params["url"]=url_final; streamcloud(params)
    elif url_final.find("played.to") >= 0: params["url"]=url_final; playedto(params)
    elif url_final.find("vidspot") >= 0: params["url"]=url_final; vidspot(params)
    elif url_final.find("vk") >= 0: params["url"]=url_final; vk(params)
    elif url_final.find("nowvideo.sx") >= 0: params["url"]=url_final; nowvideo(params)
    elif url_final.find("tumi.tv") >= 0: params["url"]=url_final; tumi(params)
    elif url_final.find("veehd") >= 0: params["url"]=url_final; veehd(params)
    elif url_final.find("turbovideos.net") >= 0: params["url"]=url_final; turbovideos(params)       
    elif url_final.find("streamin.to") >= 0: params["url"]=url_final; streaminto(params)
    elif url_final.find("powvideo") >= 0: params["url"]=url_final; powvideo(params)
    elif url_final.find("mail.ru") >= 0: params["url"]=url_final; mailru(params)
    elif url_final.find("mediafire") >= 0: params["url"]=url_final; mediafire(params)
    elif url_final.find("novamov") >= 0: params["url"]=url_final; novamov(params)
    elif url_final.find("gamovideo") >= 0: params["url"]=url_final; gamovideo(params)
    elif url_final.find("moevideos") >= 0: params["url"]=url_final; moevideos(params)
    elif url_final.find("movshare") >= 0: params["url"]=url_final; movshare(params)
    elif url_final.find("movreel") >= 0: params["url"]=url_final; movreel(params)
    elif url_final.find("videobam") >= 0: params["url"]=url_final; videobam(params)    
    elif url_final.find("vimeo") >= 0: params["url"]=url_final; vimeo(params)
    elif url_final.find("veetle") >= 0: params["url"]=url_final; veetle(params)
    elif url_final.find("videoweed") >= 0: params["url"]=url_final; videoweed(params)
    elif url_final.find("streamable") >= 0: params["url"]=url_final; streamable(params)
    elif url_final.find("rocvideo") >= 0: params["url"]=url_final; rocvideo(params)
    elif url_final.find("realvid") >= 0: params["url"]=url_final; realvid(params)
    elif url_final.find("netu") >= 0: params["url"]=url_final; netu(params)
    elif url_final.find("waaw") >= 0: params["url"]=url_final; waaw(params)
    elif url_final.find("videomega") >= 0: params["url"]=url_final; videomega(params)
    elif url_final.find("video.tt") >= 0: params["url"]=url_final; videott(params)
    elif url_final.find("flashx.tv") >= 0: params["url"]=url_final; flashx(params)
    elif url_final.find("ok.ru") >= 0: params["url"]=url_final; okru(params)
    elif url_final.find("vidto.me") >= 0: params["url"]=url_final; vidtome(params)
    elif url_final.find("playwire") >= 0: params["url"]=url_final; playwire(params)
    elif url_final.find("uptostream.com") >= 0: params["url"]=url_final; uptostream(params)
    elif url_final.find("youwatch") >= 0: params["url"]=url_final; youwatch(params)
    elif url_final.find("vidgg.to") >= 0: params["url"]=url_final; vidggto(params)
    elif url_final.find("vimple.ru") >= 0: params["url"]=url_final; vimple(params)
    elif url_final.find("idowatch.net") >= 0: params["url"]=url_final; idowatch(params)
    elif url_final.find("cloudtime.to") >= 0: params["url"]=url_final; cloudtime(params)
    elif url_final.find("vidzi.tv") >= 0: params["url"]=url_final; vidzitv(params)
    elif url_final.find("vodlocker") >= 0: params["url"]=url_final; vodlocker(params)
    elif url_final.find("streame.net") >= 0: params["url"]=url_final; streamenet(params)
    elif url_final.find("watchonline") >= 0: params["url"]=url_final; watchonline(params)
    elif url_final.find("allvid") >= 0: params["url"]=url_final; allvid(params)
    elif url_final.find("streamplay") >= 0: params["url"]=url_final; streamplay(params)
    elif url_final.find("myvideoz") >= 0: params["url"]=url_final; myvideoz(params)
    elif url_final.find("streamplay.to") >= 0: params["url"]=url_final; streamplay(params)
    elif url_final.find("watchonline") >= 0: params["url"]=url_final; watchonline(params)
    elif url_final.find("rutube.ru") >= 0: params["url"]=url_final; rutube(params)
    elif url_final.find("dailymotion") >= 0: params["url"]=url_final; dailymotion(params)
    elif url_final.find("auroravid") >= 0: params["url"]=url_final; auroravid(params)
    elif url_final.find("wholecloud.net") >= 0: params["url"]=url_final; wholecloud(params)
    elif url_final.find("bitvid.sx") >= 0: params["url"]=url_final; bitvid(params)
    elif url_final.find("spruto.tv") >= 0: params["url"]=url_final; spruto(params)
    elif url_final.find("stormo.tv") >= 0: params["url"]=url_final; stormo(params)
    elif url_final.find("myvi.ru") >= 0: params["url"]=url_final; myviru(params)
    elif url_final.find("youtube.com") >= 0: params["url"]=url_final; youtube(params)
    elif url_final.find("filmon.com") >= 0: params["url"]=url_final; filmon(params)
    elif url_final.find("thevideo.me") >= 0: params["url"]=url_final; thevideome(params)
    elif url_final.find("videowood.tv") >= 0: params["url"]=url_final; videowood(params)
    elif url_final.find("neodrive.co") >= 0: params["url"]=url_final; neodrive(params)
    elif url_final.find("thevideobee.to") >= 0: params["url"]=url_final; thevideobee(params)
    elif url_final.find("fileshow.tv") >= 0: params["url"]=url_final; fileshow(params)
    elif url_final.find("vid.ag") >= 0: params["url"]=url_final; vid(params)
    elif url_final.find("vidxtreme.to") >= 0: params["url"]=url_final; vidxtreme(params)
    elif url_final.find("vidup") >= 0: params["url"]=url_final; vidup(params)
    elif url_final.find("watchvideo") >= 0: params["url"]=url_final; watchvideo(params)
    elif url_final.find("speedvid") >= 0: params["url"]=url_final; speedvid(params)
    elif url_final.find("chefti.info") >= 0: params["url"]=url_final; exashare(params)
    elif url_final.find("vodbeast") >= 0: params["url"]=url_final; vodbeast(params)
    elif url_final.find("nosvideo") >= 0: params["url"]=url_final; nosvideo(params)
    elif url_final.find("noslocker") >= 0: params["url"]=url_final; noslocker(params)
    elif url_final.find("up2stream") >= 0: params["url"]=url_final; up2stream(params)
    elif url_final.find("openload") >= 0: params["url"]=url_final; openload(params)
    elif url_final.find("smartvid") >= 0: params["url"]=url_final; smartvid(params)
    elif url_final.find("greevid") >= 0: params["url"]=url_final; greevid(params)
    elif url_final.find("letwatch") >= 0: params["url"]=url_final; letwatch(params)
    
################################################### Herramientas #################################################

def seriesflv_genr(n_genr):

    if len(n_genr) >=5: n_genr = n_genr[0]+', '+n_genr[1]+', '+n_genr[2]+', '+n_genr[3]+', '+n_genr[4]
    elif len(n_genr) ==4: n_genr = n_genr[0]+', '+n_genr[1]+', '+n_genr[2]+', '+n_genr[3]
    elif len(n_genr) ==3: n_genr = n_genr[0]+', '+n_genr[1]+', '+n_genr[2]
    elif len(n_genr) ==2: n_genr = n_genr[0]+', '+n_genr[1]
    elif len(n_genr) ==1: n_genr = n_genr[0]
    return n_genr   

def jump_cloudflare(url):
    
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0','Accept-Encoding':'gzip, deflate','Host':'www.seriesflv.net',
    'Referer': url}
    r = requests.get(url,headers=headers)
    if 'refresh' in r.headers:
        time.sleep(int(r.headers['refresh'][:1]))
        url = web + r.headers['refresh'][7:]
    r = requests.get(url,headers=headers)
    data = r.content
    return data

############################################# By PalcoTv Team ####################################################
