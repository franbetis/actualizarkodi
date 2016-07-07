# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Linker de SeriesBlanco para PLD.VisionTV
# Version 0.3 (05/04/2016)
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

__playlists__= xbmc.translatePath(os.path.join('special://home/userdata/playlists', ''))
__temp__ = xbmc.translatePath(os.path.join('special://home/userdata/playlists/tmp', ''))

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")

referer = "http://seriesblanco.com/"   
thumbnail = "http://seriesblanco.com/imags_estilos/logofb.jpg"
fanart = "http://i1288.photobucket.com/albums/b487/elkinderguapo1982/awkward-awkward-big_zps91c11a59.jpg" 

sc = "[COLOR white]";ec = "[/COLOR]"
sc2 = "[COLOR palegreen]";ec2 = "[/COLOR]"
sc3 = "[COLOR seagreen]";ec3 = "[/COLOR]"
sc4 = "[COLOR red]";ec4 = "[/COLOR]"
sc5 = "[COLOR yellowgreen]";ec5 = "[/COLOR]"
version = " [0.3]"

def seriesblanco0(params):
    plugintools.log('[%s %s] Linker SeriesBlanco %s' % (addonName, addonVersion, repr(params)))

    plugintools.add_item(action="",url="",title="[COLOR lightblue][B]Linker SeriesBlanco"+version+"[/B][COLOR lightblue]"+sc4+"[I] ***  PLD.VisionTV ***[/I]"+ec4,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)

    url = params.get("url")    
    referer = url
    data = gethttp_referer_headers(url,referer)
    #plugintools.log("data= "+data)

    fondo = plugintools.find_single_match(data, "<meta property='og:image' content='(.*?)'")
    if fondo == "": fondo = fanart
    logo = plugintools.find_single_match(data,"<img id='port_serie' src='([^']+)'")
    if logo == "": logo = thumbnail

    info = plugintools.find_single_match(data, "<img id='port_serie'(.*?)</tbody></table>")
    #print info
    votos = plugintools.find_single_match(info,"color='yellow'>(.*?)<").strip()
    if votos =="": votos = "N/D"

    title_ser = plugintools.find_single_match(info, "<h4>(.*?)</h4>").decode('unicode_escape').encode('utf8').strip()
    if title_ser == "": title_ser = "N/D"

    genr = plugintools.find_single_match(info, "<font color='skyblue'>G.*?nero:</font></b>(.*?)<br>").decode('unicode_escape').encode('utf8').strip()
    if genr == "": genr = "N/D"

    prod_ser = plugintools.find_single_match(info, "color='skyblue'>Productora[^<]+</font></b>(.*?)<br>").decode('unicode_escape').encode('utf8').strip()
    if prod_ser == "": prod_ser = "N/D"
    
    pais_ser = plugintools.find_single_match(info, "color='skyblue'>Pa[^<]+</font></b>(.*?)<br>").decode('unicode_escape').encode('utf8').strip()
    if pais_ser == "": pais_ser = "N/D"
    
    time_ser = plugintools.find_single_match(info,"color='skyblue'>Duraci[^<]+</font></b>(.*?)<br>").decode('unicode_escape').encode('utf8').strip()
    if time_ser == "": time_ser = "N/D"
    
    temp = plugintools.find_multiple_matches(data, "<h2 style='cursor: hand; cursor: pointer;'>(.*?)</tbody></table>")
    n_temp = len(temp)

    sinopsis = plugintools.find_single_match(info,"<p>(.*?)</p>").decode('unicode_escape').encode('utf8')
    sinopsis = sinopsis.replace('<br/>','').replace('<br />','').replace('<br>','').strip()
    if sinopsis == "": sinopsis = "N/D"
    
    datamovie = {
    'season': sc3+'[B]Temporadas Disponibles: [/B]'+ec3+sc+str(n_temp)+', '+ec,
    'votes': sc3+'[B]Votos: [/B]'+ec3+sc+str(votos)+', '+ec,
    'genre': sc3+'[B]Género: [/B]'+ec3+sc+str(genr)+', '+ec,
    'studio': sc3+'[B]Productora: [/B]'+ec3+sc+str(prod_ser)+', '+ec,
    'duration': sc3+'[B]Duración: [/B]'+ec3+sc+str(time_ser)+'[CR]'+ec,
    'sinopsis': sc3+'[B]Sinopsis: [/B]'+ec3+sc+str(sinopsis)+ec}
    
    datamovie["plot"]=datamovie["season"]+datamovie["votes"]+datamovie["genre"]+datamovie["studio"]+datamovie["duration"]+datamovie["sinopsis"]

    plugintools.add_item(action="",title=sc5+"[B]"+title_ser+"[/B]"+ec5,url="",info_labels=datamovie,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
    
    for item in temp:
        title_temp = plugintools.find_single_match(item, "<u>(.*?)</u></h2>").decode('unicode_escape').encode('utf8')
        cap_temp = plugintools.find_multiple_matches(item,"<tr><td>(.*?)</td>")
        plugintools.add_item(action="",title=sc2+'-- '+title_temp+' --'+ec2,url="",thumbnail=logo,info_labels=datamovie,plot=sinopsis,fanart=fondo,folder=False,isPlayable=False)
        for cap in cap_temp:
            url_cap = plugintools.find_single_match(cap, "<a href='([^']+)")
            url_cap = 'http://www.seriesblanco.com'+url_cap
            title_cap = plugintools.find_single_match(cap, "'>(.*?)</a>")
            plugintools.addPeli(action="seriesblanco1",title=sc+title_cap+ec,url=url_cap,thumbnail=logo,info_labels=datamovie,plot=sinopsis,fanart=fondo,folder=True,isPlayable=False)
    
def seriesblanco1(params):
    plugintools.log('[%s %s] Linker SeriesBlanco %s' % (addonName, addonVersion, repr(params)))

    sinopsis = params.get("plot")
    datamovie = {}
    datamovie["Plot"]=sinopsis

    thumbnail = params.get("thumbnail")
    fanart = params.get("fanart")  
    
    headers = {'Host':"seriesblanco.com","User-Agent": 'User-Agent=Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; es-ES; rv:1.9.2.12) Gecko/20101026 Firefox/3.6.12', 
    "Referer": referer}
    url = params.get("url").replace('www.seriesblanco.com','seriesblanco.com')
    
    r = requests.get(url,headers=headers)
    data = r.content
    plugintools.add_item(action="",url="",title="[COLOR lightblue][B]Linker SeriesBlanco"+version+"[/B][COLOR lightblue]"+sc4+"[I] ***PLD.VisionTV***[/I]"+ec4,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
    
    #No hay peticion Ajax
    match_listacapis = plugintools.find_single_match(data,"<h2>Visionados Online</h2>(.*?)<h2>Descarga</h2>")

    #Si hay peticion Ajax
    if match_listacapis =="":
        # Buscando la url y datos del envio post a la peticion ajax
        ajax = plugintools.find_single_match(data,"function LoadGrid(.*?)success:")
        ajaxrequest = plugintools.find_single_match(ajax,"url : '(.*?)'.*?data : \"(.*?)\"")
        # Petición ajax
        url_ajax = scrapertools.cache_page(referer + ajaxrequest[0], ajaxrequest[1])
        custom_post=ajaxrequest[1]
        body,response_headers = plugintools.read_body_and_headers(referer+ajaxrequest[0], post=custom_post)
        #plugintools.log("data= "+data)
        match_listacapis = plugintools.find_single_match(body,'<h2>Visionados Online</h2>(.*?)</table>')

    match_capi = plugintools.find_multiple_matches(match_listacapis,'<td><div class="grid_content sno">(.*?)<br>')
    
    for entry in match_capi:
        img = plugintools.find_single_match(entry,"src='/servidores([^']+)")
        url_img = 'http://www.seriesblanco.com/servidores'+img
        url_capi = plugintools.find_single_match(entry,'<a href="([^"]+)"')
        #url_capi = 'http://www.seriesblanco.com'+url_capi
        #Puede ser seriesblanco.tv o seriesblanco.com
        
        lang_audio = plugintools.find_single_match(entry,'<img src="http://seriesblanco.tv/banderas/([^"]+)"')
        if lang_audio =="": 
            lang_audio = plugintools.find_single_match(entry,'<img src="http://seriesblanco.com/banderas/([^"]+)"')
        
        if lang_audio.find("es.png") >= 0: lang_audio = "ESP"
        elif lang_audio.find("la.png") >= 0: lang_audio = "LAT"
        elif lang_audio.find("vos.png") >= 0: lang_audio = "V.O.S."
        elif lang_audio.find("vo.png") >= 0: lang_audio = "V.O."            
        
        url_server = plugintools.find_single_match(entry,"<img src='/servidores/([^']+)")
        url_server = url_server.replace(".png", "").replace(".jpg", "")
        quality = plugintools.find_single_match(entry,"<img src='/servidores/.*?alt=''>.*?</center></td><td class='tam12'>(.*?)</td>")
        #if quality == "": quality = "undefined"
        server = video_analyzer(url_server)
        titlefull = params.get("title")+sc2+'[I] ['+lang_audio+'] [/I]'+ec2+sc5+'[I] ['+server+'][/I]  '+ec5+sc+'[I]'+quality+'[/I]'+ec
        if server != "":
            plugintools.addPeli(action="getlink_seriesblanco",title=titlefull,url=url_capi,info_labels=datamovie,thumbnail=url_img,fanart=fanart,folder=False,isPlayable=True)
'''
def seriesblanco_liker2(params):
    plugintools.log('[%s %s] Linker SeriesBlanco %s' % (addonName, addonVersion, repr(params)))

    url = params.get("url")
    print url
    
    referer = url
    data = gethttp_referer_headers(url,referer)
  
    # onclick='window.open("http://allmyvideos.net/lh18cer7ut8r")
    url_final = plugintools.find_single_match(data, "onclick='window.open(.*?);'/>")
    url_final = url_final.replace('("', "").replace('")', "")
    
    params = plugintools.get_params()
    params["url"]=url_final
    getlink_seriesblanco(params)
'''
def getlink_seriesblanco(params):
    plugintools.log("[%s %s] Parser Series Blanco %s" % (addonName, addonVersion, repr(params)))
    
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
    elif url_final.find("bojem3a.info") >= 0: params["url"]=url_final; exashare(params)
    elif url_final.find("vodbeast") >= 0: params["url"]=url_final; vodbeast(params)
    elif url_final.find("nosvideo") >= 0: params["url"]=url_final; nosvideo(params)
    elif url_final.find("noslocker") >= 0: params["url"]=url_final; noslocker(params)
    elif url_final.find("up2stream") >= 0: params["url"]=url_final; up2stream(params)
'''
def gethttp_referer_headers(url,referer):
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    request_headers.append(["Referer", referer])    
    body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)
    return body
'''
############################################# PLD.VisionTV ####################################################
