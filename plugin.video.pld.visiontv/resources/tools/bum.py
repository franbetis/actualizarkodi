# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Buscador Unificado de Magnets para PLD.VisionTV (Kickass, Isohunt, BitSnoop, Monova)
# Version 0.1 
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Gracias a la librería plugintools de Jesús (www.mimediacenter.info)
#------------------------------------------------------------

from __main__ import *

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

import re,urllib,urllib2,sys
import plugintools,ioncube,requests

from __main__ import *

playlists = xbmc.translatePath(os.path.join('special://userdata/playlists', ''))
temp = xbmc.translatePath(os.path.join('special://userdata/playlists/tmp', ''))

thumbnail = 'http://static.myce.com/images_posts/2011/04/kickasstorrents-logo.jpg'
fanart = 'https://yuq.me/users/19/529/lcqO6hj0XK.png'

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")

def bum_multiparser(params):
    plugintools.log('[%s %s] Iniciando BUM+ ... %s' % (addonName, addonVersion, repr(params)))

    # Archivo de control de resultados
    bumfile = temp + 'bum.dat'
    if not os.path.isfile(bumfile):  # Si no existe el archivo de control, se crea y se anotan resultados de la búsqueda
        controlbum = open(bumfile, "wb")
        controlbum.close()    

    try:
        texto = params.get("title")
        texto = texto.replace("[Multiparser]", "").replace("[/COLOR]", "").replace("[I]", "").replace("[/I]", "").replace("[COLOR white]", "").replace("[COLOR lightyellow]", "").strip()
        lang = plugintools.get_setting("bum_lang")
        if lang == '0':
            lang = ""            
        elif lang == '1':
            lang = 'spanish'
        elif lang == '2':
            lang = 'english'
        elif lang == '3':
            lang = 'french'
        elif lang == '4':
            lang = 'german'
        elif lang == '5':
            lang = 'latino'

        if lang != "": texto = texto+' ' + lang
        else: texto=texto.strip()
        
        plugintools.set_setting("bum_search",texto)
        params["plot"]=texto
        texto = texto.lower().strip()
        texto = texto.replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u").replace("ñ", "n")
        if texto == "":
            errormsg = plugintools.message("PLD.VisionTV","Por favor, introduzca el canal a buscar")
            #return errormsg
        else:
            url = 'https://kat.cr/usearch/'+texto+'/'  # Kickass
            params["url"]=url            
            url = params.get("url")
            referer = 'http://www.kat.cr'
            kickass1_bum(params)            
            url = 'http://bitsnoop.com/search/all/'+texto+'/c/d/1/'  # BitSnoop
            params["url"]=url            
            url = params.get("url")
            referer = 'http://www.bitsnoop.com'
            bitsnoop1_bum(params)
            url = 'https://isohunt.to/torrents/?ihq='+texto.replace(" ", "+").strip()+'&Torrent_sort=-seeders'  # Isohunt
            params["url"]=url            
            url = params.get("url")
            referer = 'https://isohunt.to'
            isohunt1_bum(params)
            url = 'http://www.limetorrents.co/search/all/'+texto.replace(" ", "+").strip()+'/seeds/1/'
            params["url"]=url
            limetorrents0(params)            
            #url = 'https://www.monova.org/search?term='+texto.replace(" ", "+")+'&cat=&page=1&sort=1&verified=1'  # Monova
            #params["url"]=url            
            #monova1_bum(params)
            
    except:
         pass

        
    controlbum = open(bumfile, "r")
    num_items = len(controlbum.readlines())
    fanart = 'http://images5.fanpop.com/image/photos/29400000/Massive-B-Horror-Collage-Wallpaper-horror-movies-29491579-2560-1600.jpg'

    i = -1
    controlbum.seek(0)
    while i <= num_items:        
        data = controlbum.readline()
        if data.startswith("EOF") == True:
            break
        elif data.startswith("Title") == True:
            title=data.replace("Title: ", "")
            url=controlbum.readline();url=url.replace("URL: ","")
            thumbnail=controlbum.readline();thumbnail=thumbnail.replace("Thumbnail: ", "").strip()
            seeds=controlbum.readline();seeds=seeds.replace("Seeds: ", "").replace(",", "").replace(".", "").strip();seeds=int(seeds);plugintools.log("seeds= "+str(seeds))
            size=controlbum.readline();size=size.replace("Size: ", "").strip();print size
            seeds_min=plugintools.get_setting("bum_seeds");seeds_min=int(seeds_min);plugintools.log("seeds_min= "+str(seeds_min))
            if int(seeds) >= int(seeds_min):
                if thumbnail == "":
                    thumbnail = art + 'bum.png'                
                if title.endswith("[Kickass][/I][/COLOR]") >= 0:
                    plugintools.add_item(action="play", title=title, url=url, thumbnail=thumbnail, fanart=fanart, folder=False, isPlayable=True)
                    i=i+1
                    print i
                    continue
                elif title.endswith("[BitSnoop][/I][/COLOR]") >= 0:
                    plugintools.add_item(action="bitsnoop2_bum", title=title, url=url, thumbnail=thumbnail, fanart=fanart, folder=False, isPlayable=True)
                    i=i+1
                    print i
                    continue
                elif title.endswith("[IsoHunt][/I][/COLOR]") >= 0:
                    plugintools.add_item(action="isohunt2_bum", title=title, url=url, thumbnail=thumbnail, fanart=fanart, folder=False, isPlayable=True)
                    i=i+1
                    print i
                    continue
                elif title.endswith("[LimeTorrents][/I][/COLOR]") >= 0:
                    plugintools.add_item(action="limetorrents1", title=title, url=url, thumbnail=thumbnail, fanart=fanart, folder=False, isPlayable=True)
                    i=i+1
                    print i
                    continue            
        else:
            i=i+1
            continue

    controlbum.close()
    xbmcplugin.addSortMethod(int(sys.argv[1]), 2)
    
    # Eliminamos archivo de registro
    try:
        if os.path.exists(bumfile):
            os.remove(bumfile)
    except: pass
    
    


def kickass0_bum(params):
    plugintools.log('[%s %s] [BUM+] Kickass... %s' % (addonName, addonVersion, repr(params)))

    try:
        texto = params.get("plot");
        if texto == "":
            errormsg = plugintools.message("PLD.VisionTV","Por favor, introduzca el canal a buscar")
        else:           
            texto = texto.lower().strip()
            url = 'https://kickass.to/usearch/'+texto+'/'
            plugintools.log("URL Kickass= "+url)
            params["url"]=url            
            url = params.get("url")
            referer = 'http://www.kickass.to'            
    except:
         pass      

    # Archivo de control de resultados (evita la recarga del cuadro de diálogo de búsqueda tras cierto tiempo)
    bumfile = temp + 'bum.dat'
    if not os.path.isfile(bumfile):  # Si no existe el archivo de control, se crea y se registra la búsqueda
        controlbum = open(bumfile, "a")
        controlbum.close()
        ahora = datetime.now()
        #print 'ahora',ahora
        anno_actual = ahora.year
        mes_actual = ahora.month
        hora_actual = ahora.hour
        min_actual = ahora.minute
        seg_actual = ahora.second
        hoy = ahora.day
        # Si el día o mes está entre el 1 y 9, nos devuelve un sólo dígito, así que añadimos un 0 (cero) delante:
        if hoy <= 9:
            hoy = "0" + str(hoy)
        if mes_actual <= 9:
            mes_actual = "0" + str(ahora.month)
        timestamp = str(ahora.year) + str(mes_actual) + str(hoy) + str(hora_actual) + str(min_actual) + str(seg_actual)
        controlbum = open(temp + 'bum.dat', "a")
        controlbum.seek(0)
        controlbum.write(timestamp+":"+texto)
        controlbum.close()
    else:
        controlbum = open(temp + 'bum.dat', "r")
        controlbum.seek(0)
        data = controlbum.readline()
        controlbum.close()        
        plugintools.log("BUM+= "+data)           
        plugintools.log("Control de BUM+ activado. Analizamos timestamp...")
        data = data.split(":")
        timestamp = data[0]
        term_search = data[1]
        ahora = datetime.now()
        #print 'ahora',ahora
        anno_actual = ahora.year
        mes_actual = ahora.month
        hora_actual = ahora.hour
        min_actual = ahora.minute
        seg_actual = ahora.second
        hoy = ahora.day
        # Si el día o mes está entre el 1 y 9, nos devuelve un sólo dígito, así que añadimos un 0 (cero) delante:
        if hoy <= 9:
            hoy = "0" + str(hoy)
        if mes_actual <= 9:
            mes_actual = "0" + str(ahora.month)
        timenow = str(ahora.year) + str(mes_actual) + str(hoy) + str(hora_actual) + str(min_actual) + str(seg_actual)
        # Comparamos valores (hora actual y el timestamp del archivo de control)
        if term_search == texto:
            result = int(timenow) - int(timestamp)
            print 'result',result
            if result > 90:  # Control fijado en 90 segundos; esto significa que una misma búsqueda no podremos realizarla en menos de 90 segundos, y en ese tiempo debe reproducirse el torrent
                # Borramos registro actual y guardamos el nuevo (crear una función que haga esto y no repetir!)
                ahora = datetime.now()
                print 'ahora',ahora
                anno_actual = ahora.year
                mes_actual = ahora.month
                hora_actual = ahora.hour
                min_actual = ahora.minute
                seg_actual = ahora.second
                hoy = ahora.day
                # Si el día o mes está entre el 1 y 9, nos devuelve un sólo dígito, así que añadimos un 0 (cero) delante:
                if hoy <= 9:
                    hoy = "0" + str(hoy)
                if mes_actual <= 9:
                    mes_actual = "0" + str(ahora.month)
                timestamp = str(ahora.year) + str(mes_actual) + str(hoy) + str(hora_actual) + str(min_actual) + str(seg_actual)
                controlbum = open(temp + 'bum.dat', "a")
                controlbum.seek(0)
                controlbum.write(timestamp+":"+texto)
                controlbum.close()                
                kickass_results(params)
            else:
                plugintools.log("Recarga de página")
                kickass_results(params)
        else:
            # Borramos registro actual y guardamos el nuevo (crear una función que haga esto y no repetir!)
            ahora = datetime.now()
            print 'ahora',ahora
            anno_actual = ahora.year
            mes_actual = ahora.month
            hora_actual = ahora.hour
            min_actual = ahora.minute
            seg_actual = ahora.second
            hoy = ahora.day
            # Si el día o mes está entre el 1 y 9, nos devuelve un sólo dígito, así que añadimos un 0 (cero) delante:
            if hoy <= 9:
                hoy = "0" + str(hoy)
            if mes_actual <= 9:
                mes_actual = "0" + str(ahora.month)
            timestamp = str(ahora.year) + str(mes_actual) + str(hoy) + str(hora_actual) + str(min_actual) + str(seg_actual)
            controlbum = open(temp + 'bum.dat', "a")
            controlbum.seek(0)
            controlbum.write(timestamp+":"+texto)
            controlbum.close()                
            kickass1_bum(params)
                
                
                
def kickass1_bum(params):
    plugintools.log('[%s %s] [BUM+] Kickass results... %s' % (addonName, addonVersion, repr(params)))

    bumfile = temp + 'bum.dat'
    controlbum = open(bumfile, "a")    

    show = 'biglist'
    plugintools.modo_vista(show)

    #plugintools.add_item(action="", title= '[COLOR green][B]KickAss[/COLOR][COLOR gold][I] Torrents[/I][/COLOR]   [/B][COLOR lightyellow][I]By Juarrox[/I][/COLOR]', url = "", thumbnail = thumbnail , fanart = fanart, folder = False, isPlayable = False)
    #plugintools.add_item(action="", title= '[COLOR red][B]Título [/COLOR][COLOR white] (Tamaño) [/COLOR]   [/B][COLOR lightyellow][I](Semillas)[/I][/COLOR]', url = "", thumbnail = thumbnail , fanart = fanart, folder = False, isPlayable = False)    
    url = params.get("url")
    referer = 'https://kat.cr/'

    data = gethttp_referer_headers(url,referer)
    #plugintools.log("data= "+data)
    thumbnail = plugintools.find_single_match(data, '<img src="([^"]+)')
    thumbnail = 'http:'+thumbnail
    #plugintools.log("thumbnail= "+thumbnail)        

    match_num_results = plugintools.find_single_match(data, '<div><h2>(.*?)</a></h2>')
    num_results = plugintools.find_single_match(match_num_results, '<span>(.*?)</span>')
    num_results = num_results.replace("from", "de").replace("results", "Resultados:").strip()
    #plugintools.log("num_results= "+num_results)
    results = plugintools.find_single_match(data, '<table width="100%" cellspacing="0" cellpadding="0" class="doublecelltable" id="mainSearchTable">(.*?)</table>')
    #plugintools.log("results_table= "+results)
    matches = plugintools.find_multiple_matches(results, '<div class="torrentname">(.*?)<a data-download')
    for entry in matches:
        #plugintools.log("entry= "+entry)
        match_title = plugintools.find_single_match(entry, 'class="cellMainLink">(.*?)</a>')
        match_title = match_title.replace("</strong>", "").replace("<strong>", "").replace('<strong class="red">', "").strip()
        #plugintools.log("match_title= "+match_title)        
        magnet_match = 'magnet:'+plugintools.find_single_match(entry, 'magnet:([^"]+)')
        plugintools.log("magnet_match= "+magnet_match)
        magnet_match = urllib.quote_plus(magnet_match).strip()
        addon_magnet = plugintools.get_setting("addon_magnet")
        if addon_magnet == "0":  # Stream (por defecto)
            magnet_url = 'plugin://plugin.video.stream/play/'+magnet_match
            magnet_url = magnet_url.strip()
        elif addon_magnet == "1":  # Pulsar
            magnet_url = 'plugin://plugin.video.pulsar/play?uri=' + magnet_match
            magnet_url = magnet_url.strip()
        elif addon_magnet == "2":  # KMediaTorrent
            magnet_url = 'plugin://plugin.video.kmediatorrent/play/' + magnet_match
            magnet_url = magnet_url.strip()
        plugintools.log("magnet_url= "+magnet_url)        
        size = plugintools.find_single_match(entry, 'class=\"nobr center\">(.*?)</td>')
        size = size.replace("<span>","").replace("</span>","").strip()
        #plugintools.log("size= "+size)
        seeds = plugintools.find_single_match(entry, '<td class="green center">(.*?)</td>').replace(",", "").replace(".", "")
        leechs = plugintools.find_single_match(entry, '<td class="red lasttd center">(.*?)</td>')
        #plugintools.log("seeds= "+seeds)
        #plugintools.log("leechs= "+leechs)
        title_fixed='[COLOR gold][I]['+seeds+'/'+leechs+'][/I][/COLOR] [COLOR white] '+match_title+' [I]['+size + '] [/COLOR][COLOR orange][Kickass][/I][/COLOR]'
        #plugintools.add_item(action="play", title=title_fixed, url=magnet_url, thumbnail = thumbnail , fanart = fanart , show = show , extra = show , folder=False, isPlayable=True)
        controlbum.write('Title: '+title_fixed+'\nURL: '+magnet_url+'\nThumbnail: '+thumbnail+'\nSeeds: '+seeds+'\nSize: '+size+'\n\n')

    controlbum.close()

                            

def bitsnoop0_bum(params):
    plugintools.log('[%s %s] [BUM+] BitSnoop... %s' % (addonName, addonVersion, repr(params)))

    try:
        texto = "";
        texto='riddick'
        texto = plugintools.keyboard_input(texto)
        plugintools.set_setting("alluc_search",texto)
        params["plot"]=texto
        texto = texto.lower()
        if texto == "":
            errormsg = plugintools.message("PLD.VisionTV","Por favor, introduzca el canal a buscar")
            #return errormsg
        else:
            texto = texto.lower().strip()
            texto = texto.replace(" ", "+")
            
            # http://bitsnoop.com/search/all/the+strain+spanish/c/d/1/
            url = 'http://bitsnoop.com/search/all/'+texto+'/c/d/1/'
            params["url"]=url            
            url = params.get("url")
            referer = 'http://www.bitsnoop.com'
            bitsnoop1_bum(params)
    except:
         pass    




def bitsnoop1_bum(params):
    plugintools.log('[%s %s] [BUM+] BitSnoop results... %s' % (addonName, addonVersion, repr(params)))

    thumbnail = 'http://upload.wikimedia.org/wikipedia/commons/9/97/Bitsnoop.com_logo.png'
    fanart = 'http://wallpoper.com/images/00/41/86/68/piracy_00418668.jpg'

    # Abrimos archivo de registro
    bumfile = temp + 'bum.dat'
    controlbum = open(bumfile, "a")    

    show = 'biglist'
    plugintools.modo_vista(show)

    #plugintools.add_item(action="", title= '[COLOR green][B]Bit[/COLOR][COLOR gold][I]Snoop[/I][/COLOR]   [/B][COLOR lightyellow][I]By Juarrox[/I][/COLOR]', url = "", thumbnail = thumbnail , fanart = fanart, folder = False, isPlayable = False)    
    url = params.get("url")
    referer = 'https://bitsnoop.com/'

    data = gethttp_referer_headers(url,referer)  #Todo: Añadir modo de vista (show)
    results = plugintools.find_single_match(data, '<ol id="torrents" start="1">(.*?)</ol>')
    matches = plugintools.find_multiple_matches(results, '<span class="icon cat_(.*?)</div></td>')
    i = 0
    for entry in matches:
        plugintools.log("entry= "+entry)
        i = i + 1
        print i
        page_url = plugintools.find_single_match(entry, 'a href="([^"]+)')
        title_url = plugintools.find_single_match(entry, 'a href="(.*?)</a>')
        title_url = title_url.replace(page_url, "").replace("<span class=srchHL>", "").replace('">', "").replace("<b class=srchHL>", "[COLOR white]").replace("</b>", "[/COLOR]").strip()
        page_url = 'http://bitsnoop.com'+page_url
        plugintools.log("title_url= "+title_url)
        plugintools.log("page_url= "+page_url)
        seeders = plugintools.find_single_match(entry, 'title="Seeders">(.*?)</span>').replace(",", "").replace(".", "")
        plugintools.log("seeders= "+seeders)
        leechers = plugintools.find_single_match(entry, 'title="Leechers">(.*?)</span>')
        size = plugintools.find_single_match(entry, '<tr><td align="right" valign="middle" nowrap="nowrap">(.*?)<div class="nfiles">')
        plugintools.log("size= "+size)
        plugintools.log("leechers= "+leechers)        
        if seeders == "":  # Verificamos el caso en que no haya datos de seeders/leechers
            seeders = "0"
        if leechers == "":
            leechers = "0"            
        stats = '[COLOR gold][I]['+seeders+'/'+leechers+'][/I][/COLOR]'
        title_fixed=stats+'  [COLOR white]'+title_url+' [I]['+size+'] [/COLOR][COLOR red][BitSnoop][/I][/COLOR]'
        #plugintools.add_item(action="bitsnoop2_bum", title=title_fixed, url = page_url , thumbnail = thumbnail, fanart = fanart, folder = False, isPlayable = True)
        controlbum.write('Title: '+title_fixed+'\nURL: '+page_url+'\nThumbnail: '+thumbnail+'\nSeeds: '+seeders+'\nSize: '+size+'\n\n')

    controlbum.close()
        



def bitsnoop2_bum(params):
    plugintools.log('[%s %s] [BUM+] BitSnoop getlink... %s' % (addonName, addonVersion, repr(params)))

    
    url = params.get("url")
    referer = 'https://bitsnoop.com/'
    data = gethttp_referer_headers(url,referer)  #Todo: Añadir modo de vista (show)
    plugintools.log("data= "+data)
    magnet_match = plugintools.find_single_match(data, '<a href="magnet([^"]+)')
    magnet_match = 'magnet'+magnet_match
    plugintools.log("Magnet: "+magnet_match)
    magnet_match = urllib.quote_plus(magnet_match).strip()    
    addon_magnet = plugintools.get_setting("addon_magnet")    
    if addon_magnet == "0":  # Stream (por defecto)
        magnet_url = 'plugin://plugin.video.stream/play/'+magnet_match
        magnet_url = magnet_url.strip()
    elif addon_magnet == "1":  # Pulsar
        magnet_url = 'plugin://plugin.video.pulsar/play?uri=' + magnet_match
        magnet_url = magnet_url.strip()
    elif addon_magnet == "2":  # KMediaTorrent
        magnet_url = 'plugin://plugin.video.kmediatorrent/play/' + magnet_match
        magnet_url = magnet_url.strip()

    plugintools.log("magnet_url= "+magnet_url)
    launch_bum(magnet_url)



def isohunt0_bum(params):
    plugintools.log('[%s %s] [BUM+] Isohunt... %s' % (addonName, addonVersion, repr(params)))

    thumbnail = 'http://www.userlogos.org/files/logos/dfordesmond/isohunt%201.png'
    fanart = 'http://2.bp.blogspot.com/_NP40rzexJsc/TMGWrixybJI/AAAAAAAAHCU/ij1--_DQEZo/s1600/Keep_Seeding____by_Carudo.jpg'    
    show = 'list'
    plugintools.modo_vista(show)
    
    try:
        texto = "";
        texto='riddick'
        texto = plugintools.keyboard_input(texto)
        plugintools.set_setting("alluc_search",texto)
        params["plot"]=texto
        texto = texto.lower()
        if texto == "":
            errormsg = plugintools.message("PLD.VisionTV","Por favor, introduzca el canal a buscar")
            #return errormsg
        else:
            texto = texto.lower().strip()
            texto = texto.replace(" ", "+")
            
            # https://isohunt.to/torrents/?ihq=the+strain+spanish
            url = 'https://isohunt.to/torrents/?ihq='+texto+'&Torrent_sort=seeders.desc'
            params["url"]=url            
            url = params.get("url")
            referer = 'https://isohunt.to'
            isohunt1_bum(params)
    except:
         pass       


def isohunt1_bum(params):
    plugintools.log('[%s %s] [BUM+] Isohunt results... %s' % (addonName, addonVersion, repr(params)))

    thumbnail = 'http://www.userlogos.org/files/logos/dfordesmond/isohunt%201.png'
    fanart = 'http://2.bp.blogspot.com/_NP40rzexJsc/TMGWrixybJI/AAAAAAAAHCU/ij1--_DQEZo/s1600/Keep_Seeding____by_Carudo.jpg' 

    # Abrimos archivo de registro
    bumfile = temp + 'bum.dat'
    controlbum = open(bumfile, "a")    

    show = 'biglist'
    
    #plugintools.add_item(action="", title= '[COLOR blue][B]Iso[/COLOR][COLOR lightblue][I]Hunt[/I][/COLOR]   [/B][COLOR lightyellow][I]By Juarrox[/I][/COLOR]', url = "", thumbnail = thumbnail , fanart = fanart, folder = False, isPlayable = False)    
    url = params.get("url")
    referer = 'https://isohunt.to/'

    data = gethttp_referer_headers(url,referer)  #Todo: Añadir modo de vista (show)
    #plugintools.log("data= "+data)
    matches = plugintools.find_multiple_matches(data, '<tr data-key="(.*?)</td></tr>')    
    for entry in matches:
        plugintools.log("entry= "+entry)
        page_url = plugintools.find_single_match(entry, '<a href="([^"]+)')
        page_url = 'https://isohunt.to'+page_url
        title_url = plugintools.find_single_match(entry, '<span>(.*?)</span>')
        plugintools.log("title_url= "+title_url)
        plugintools.log("page_url= "+page_url)
        size = plugintools.find_single_match(entry, '<td class="size-row">(.*?)</td>')
        plugintools.log("size= "+size)
        seeds = plugintools.find_single_match(entry, '<td class=" sy">(.*?)</td>').replace(",", "").replace(".", "")
        if seeds == "":
            seeds = plugintools.find_single_match(entry, '<td class=" sn">(.*?)</td>')
        leechs = '?'
        plugintools.log("seeds= "+seeds)
        category = plugintools.find_single_match(entry, 'title="([^"]+)')
        plugintools.log("category= "+category)        
        title_fixed='[COLOR gold][I]['+seeds+'/'+leechs+'][/I][/COLOR] [COLOR white] '+title_url+' [I]['+size+'] [/COLOR][COLOR lightblue][IsoHunt][/I][/COLOR]'
        #plugintools.add_item(action="isohunt2_bum", title= title_fixed, url = page_url , thumbnail = thumbnail, fanart = fanart, folder = False, isPlayable = True)
        controlbum.write('Title: '+title_fixed+'\nURL: '+page_url+'\nThumbnail: '+thumbnail+'\nSeeds: '+seeds+'\nSize: '+size+'\n\n')

    controlbum.close()
            
            

def isohunt2_bum(params):
    plugintools.log('[%s %s] [BUM+] Isohunt getlink... %s' % (addonName, addonVersion, repr(params)))
    
    url = params.get("url")
    referer = 'https://isohunt.to/'
    data = gethttp_referer_headers(url,referer)  #Todo: Añadir modo de vista (show)
    plugintools.log("data= "+data)
    magnet_match = plugintools.find_single_match(data, '<a href="magnet([^"]+)')
    magnet_match = 'magnet'+magnet_match
    plugintools.log("Magnet: "+magnet_match)
    magnet_match = urllib.quote_plus(magnet_match).strip()    
    addon_magnet = plugintools.get_setting("addon_magnet")    
    if addon_magnet == "0":  # Stream (por defecto)
        magnet_url = 'plugin://plugin.video.stream/play/'+magnet_match
        magnet_url = magnet_url.strip()
    elif addon_magnet == "1":  # Pulsar
        magnet_url = 'plugin://plugin.video.pulsar/play?uri=' + magnet_match
        magnet_url = magnet_url.strip()
    elif addon_magnet == "2":  # KMediaTorrent
        magnet_url = 'plugin://plugin.video.kmediatorrent/play/' + magnet_match
        magnet_url = magnet_url.strip()

    plugintools.log("magnet_url= "+magnet_url)
    launch_bum(magnet_url)



def monova0_bum(params):
    plugintools.log('[%s %s] [BUM+] Monova... %s' % (addonName, addonVersion, repr(params)))

    thumbnail = 'http://upload.wikimedia.org/wikipedia/en/f/f4/Monova.jpg'
    fanart = 'http://www.gadgethelpline.com/wp-content/uploads/2013/10/Digital-Piracy.png'    
    show = 'list'
    plugintools.modo_vista(show)
    
    try:
        texto = "";
        texto='the strain spanish'
        texto = plugintools.keyboard_input(texto)
        plugintools.set_setting("alluc_search",texto)
        params["plot"]=texto
        texto = texto.lower()
        if texto == "":
            errormsg = plugintools.message("PLD.VisionTV","Por favor, introduzca el término a buscar")
            #return errormsg
        else:
            texto = texto.lower().strip()
            texto = texto.replace(" ", "+")
            
            # https://isohunt.to/torrents/?ihq=the+strain+spanish
            url = 'https://www.monova.org/search.php?sort=5&term='+texto+'&verified=1'
            params["url"]=url            
            url = params.get("url")
            referer = 'https://monova.org'
            monova1_bum(params)
    except:
         pass


def monova1_bum(params):
    plugintools.log('[%s %s] [BUM+] Monova results... %s' % (addonName, addonVersion, repr(params)))
    url = params.get("url")
    referer= 'https://www.monova.org/'
    plugintools.log("URL= "+url)

    thumbnail = 'http://upload.wikimedia.org/wikipedia/en/f/f4/Monova.jpg'
    fanart = 'http://www.gadgethelpline.com/wp-content/uploads/2013/10/Digital-Piracy.png'    
    data = gethttp_referer_headers(url,referer)  #Todo: Añadir modo de vista (show)
    plugintools.log("data= "+data)    
    #plugintools.add_item(action="", title= '[COLOR blue][B]M[/COLOR][COLOR lightblue][I]onova.org[/I][/COLOR]   [/B][COLOR lightyellow][I]By Juarrox[/I][/COLOR]', url = "", thumbnail = thumbnail , fanart = fanart, folder = False, isPlayable = False)        
    block_matches = plugintools.find_single_match(data, '<table id="resultsTable"(.*?)<div id="hh"></div>')
    plugintools.log("block_matches= "+block_matches)
    matches = plugintools.find_multiple_matches(block_matches, '<div class="torrentname(.*?)</div></td></tr>')
    for entry in matches:
        plugintools.log("entry= "+entry)
        if entry.find("Direct Download") >= 0:  # Descartamos resultados publicitarios 'Direct Download' que descargan un .exe
            plugintools.log("Direct Download = Yes")
        else:
            plugintools.log("Direct Download = No")
            page_url = plugintools.find_single_match(entry, 'a href="([^"]+)')
            title_url = plugintools.find_single_match(entry, 'title="([^"]+)')
            size_url = plugintools.find_single_match(entry, '<div class="td-div-right pt1">(.*?)</div>')
            seeds = plugintools.find_single_match(entry, '<td class="d">(.*?)<td align="right" id="encoded-').replace(",", "").replace(".", "")
            seeds = seeds.replace("</td>", "")
            seeds = seeds.split('<td class="d">')
            #seeds = seeds.replace('<td align="right" id="encoded-10"', "")
            #seeds = seeds.replace('<td id="encoded-10" align="right"', "")
            try:
                print 'seeds',seeds
                if len(seeds) >= 2:
                    semillas = '[COLOR gold][I]['+seeds[0]+'/'+seeds[1]+'][/I][/COLOR]'
                    plugintools.log("semillas= "+semillas)                
            except:
                pass
        
            plugintools.log("page_url= "+page_url)
            plugintools.log("title_url= "+title_url)
            plugintools.log("size_url= "+size_url)
            plugintools.add_item(action="monova2_bum", title = semillas+'  '+title_url+' [COLOR lightgreen][I][ '+size_url+'][/I][/COLOR] ', url = page_url , thumbnail = thumbnail , fanart = fanart , folder = True, isPlayable = True)  
            
            

def monova2_bum(params):
    plugintools.log('[%s %s] [BUM+] Monova getlink... %s' % (addonName, addonVersion, repr(params)))
    
    url = params.get("url")
    referer = 'https://monova.org/'
    data = gethttp_referer_headers(url,referer)  #Todo: Añadir modo de vista (show)
    plugintools.log("data= "+data)
    magnet_match = plugintools.find_single_match(data, '<a href="magnet([^"]+)')
    magnet_match = 'magnet'+magnet_match
    plugintools.log("Magnet: "+magnet_match)
    magnet_match = urllib.quote_plus(magnet_match).strip()    
    addon_magnet = plugintools.get_setting("addon_magnet")    
    if addon_magnet == "0":  # Stream (por defecto)
        magnet_url = 'plugin://plugin.video.stream/play/'+magnet_match
        magnet_url = magnet_url.strip()
    elif addon_magnet == "1":  # Pulsar
        magnet_url = 'plugin://plugin.video.pulsar/play?uri=' + magnet_match
        magnet_url = magnet_url.strip()
    elif addon_magnet == "2":  # KMediaTorrent
        magnet_url = 'plugin://plugin.video.kmediatorrent/play/' + magnet_match
        magnet_url = magnet_url.strip()

    plugintools.log("magnet_url= "+magnet_url)
    launch_bum(magnet_url)


def limetorrents0(params):
    plugintools.log('[%s %s] [BUM+] LimeTorrents loading... %s' % (addonName, addonVersion, repr(params)))
    burl = 'http://www.limetorrents.co'

    # Abrimos archivo de registro
    bumfile = temp + 'bum.dat'
    controlbum = open(bumfile, "a")    

    show = 'biglist'    
    url = params.get("url")
    r = requests.get(url)
    data = r.content
    results = plugintools.find_single_match(data, '<h2>Search Results(.*?)Next page')
    matches = plugintools.find_multiple_matches(results, '<div class="tt-name">(.*?)<td class="tdleft">')
    for entry in matches:
        if entry.find("Verified torrent") >= 0:
            plugintools.log("entry= "+entry)
            page_url = burl + plugintools.find_single_match(entry, '</a><a href="([^"]+)')
            match_title = plugintools.find_single_match(entry, '.html">([^<]+)')
            seeds = plugintools.find_single_match(entry, '<td class="tdseed">(.*?)</td>').replace(",", "").replace(".", "")
            leechs = plugintools.find_single_match(entry, '<td class="tdleech">(.*?)</td>').replace(",", "").replace(".", "")
            size = plugintools.find_single_match(entry, '</a></td><td class="tdnormal">(.*?)B</td>')+'B'
            thumbnail='https://torrentfreak.com/images/limetorrents.jpg'
            #plugintools.log("match_title= "+match_title)
            #plugintools.log("page_url= "+page_url)
            plugintools.log("size= "+size)
            title_fixed='[COLOR gold][I]['+seeds+'/'+leechs+'][/I][/COLOR] [COLOR white] '+match_title+' [I]['+size + '] [/COLOR][COLOR lime][LimeTorrents][/I][/COLOR]'
            #plugintools.add_item(action="limetorrents1", title=title_fixed, url=page_url, thumbnail=thumbnail, folder=False, isPlayable=True)
            controlbum.write('Title: '+title_fixed+'\nURL: '+page_url+'\nThumbnail: '+thumbnail+'\nSeeds: '+seeds+'\nSize: '+size+'\n\n')

    controlbum.write("\n\n\nEOF\n\n")
    controlbum.close()            
            
                                                
    

def gethttp_headers(url):
    plugintools.log("gethttp_referer_headers "+url)
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    data,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)
    return data

def gethttp_referer_headers(url,referer):
    plugintools.log("gethttp_referer_headers "+url)
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    request_headers.append(["Referer",referer])
    data,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)
    plugintools.log("data= "+data)
    return data
        


def parser_title(title):
    plugintools.log("[%s %s] parser_title %s" % (addonName, addonVersion, title))

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
    cyd = cyd.replace("[COLOR=FF00FF00]", "")  
                
    cyd = cyd.replace("[/COLOR]", "")
    cyd = cyd.replace("[B]", "")
    cyd = cyd.replace("[/B]", "")
    cyd = cyd.replace("[I]", "")
    cyd = cyd.replace("[/I]", "")
    cyd = cyd.replace("[Auto]", "")
    cyd = cyd.replace("[Parser]", "")    
    cyd = cyd.replace("[TinyURL]", "")
    cyd = cyd.replace("[Auto]", "")

    # Control para evitar filenames con corchetes
    cyd = cyd.replace(" [Lista M3U]", "")
    cyd = cyd.replace(" [Lista PLX]", "")
    cyd = cyd.replace(" [Multilink]", "")

    title = cyd
    title = title.strip()
    if title.endswith(" .plx") == True:
        title = title.replace(" .plx", ".plx")
        
    plugintools.log("title_parsed= "+title)
    return title


def launch_bum(url):
    plugintools.log('[%s %s] Bum+: Launching magnet link... %s' % (addonName, addonVersion, url))    

    plugintools.log("Magnet URL= "+url)
    plugintools.play_resolved_url(url)

