# -*- coding: utf-8 -*-
#------------------------------------------------------------
# AgendaTV para PLD.VisionTV
# Version 0.1 (18.10.2014)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Gracias a la librería plugintools de Jesús (www.mimediacenter.info)


import os
import sys
import urllib
import urllib2
import re

import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin

import plugintools, xbmcplugin, scrapertools

from __main__ import *
from resources.tools.txt_reader import *

playlists = xbmc.translatePath(os.path.join('special://userdata/playlists', ''))
temp = xbmc.translatePath(os.path.join('special://userdata/playlists/tmp', ''))

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")

thumbnail = 'http://playtv.pw/wp-content/uploads/2015/05/logo1.png'
fanart = 'http://46wvda23y0nl13db2j3bl1yxxln.wpengine.netdna-cdn.com/wp-content/uploads/2013/06/tsn-dudes.jpg'

def futbolentv0(params):    
    filename = 'futboltv.txt'
    futboltv = open(temp + filename, "wb")
    
    futbolenlatv(params, futboltv)
    futboltv.write('\n\n')
    futbolenlatv_manana(params)
    futbolenlatv(params, futboltv)
    futboltv.close()
    params = plugintools.get_params()
    params["url"]=temp+'futboltv.txt'
    txt_reader(params)    


def futbolenlatv(params, futboltv):
    plugintools.log('[%s %s].futbolenlatv %s' % (addonName, addonVersion, repr(params)))

    hora_partidos = []
    lista_equipos=[]
    campeonato=[]
    canales=[]

    url = params.get("url")
    print url
    fecha = get_fecha()
    dia_manana = params.get("plot")
    data = plugintools.read(url)

    if dia_manana == "":  # Control para si es agenda de hoy o mañana
        title = '[COLOR lightblue][B]FutbolenlaTV.com[/B][/COLOR] - [COLOR lightblue][I]Agenda para el día '+ fecha + '[/I][/COLOR]'
        #plugintools.add_item(action="", title = title, folder = False , isPlayable = False )
        futboltv.write(title+'\n\n')

    else:
        dia_manana = dia_manana.split("-")
        dia_manana = dia_manana[2] + "/" + dia_manana[1] + "/" + dia_manana[0]
        title = '[COLOR lightblue][B]FutbolenlaTV.com[/B][/COLOR] - [COLOR lightblue][I]Agenda para el día '+ dia_manana + '[/I][/COLOR]'
        futboltv.write(title+'\n\n')   
        #plugintools.add_item(action="", title = title, folder = False , isPlayable = False )


    bloque = plugintools.find_multiple_matches(data,'<span class="cuerpo-partido">(.*?)</div>')
    for entry in bloque:
        category = plugintools.find_single_match(entry, '<i class=(.*?)</i>')
        category = category.replace("ftvi-", "")
        category = category.replace('comp">', '')
        category = category.replace('"', '')
        category = category.replace("-", " ")
        category = category.replace("Futbol", "Fútbol")
        category = category.strip()
        category = category.capitalize()
        plugintools.log("cat= "+category)
        champ = plugintools.find_single_match(entry, '<span class="com-detalle">(.*?)</span>')
        #champ = encode_string(champ)
        champ = decode_string(champ)
        event = plugintools.find_single_match(entry, '<span class="bloque">(.*?)</span>')
        #event = encode_string(event)
        event = decode_string(event)
        momentum = plugintools.find_single_match(entry, '<time itemprop="startDate" datetime=([^<]+)</time>')
        # plugintools.log("momentum= "+momentum)
        momentum = momentum.split(">")
        momentum = momentum[1]

        gametime = plugintools.find_multiple_matches(entry, '<span class="n">(.*?)</span>')
        for tiny in gametime:
            day = tiny
            month = tiny

        sport = plugintools.find_single_match(entry, '<meta itemprop="eventType" content=(.*?)/>')
        sport = sport.replace('"', '')
        sport = sport.strip()
        if sport == "Partido de fútbol":
            sport = "Fútbol"

        # plugintools.log("sport= "+sport)

        gameday = plugintools.find_single_match(entry, '<span class="dia">(.*?)</span>')

        rivals = plugintools.find_multiple_matches(entry, '<span>([^<]+)</span>([^<]+)<span>([^<]+)</span>')
        rivales = ""

        for diny in rivals:
            print diny
            items = len(diny)
            items = items - 1
            i = -1
            diny[i].strip()
            while i <= items:
                if diny[i] == "":
                    del diny[0]
                    i = i + 1
                else:
                    print diny[i]
                    rival = diny[i]
                    #rival = encode_string(rival)
                    rival = decode_string(rival)
                    plugintools.log("rival= "+rival)
                    if rival == "-":
                        i = i + 1
                        continue
                    else:
                        if rivales != "":
                            rivales = rivales + " vs " + rival
                            plugintools.log("rivales= "+rivales)
                            break
                        else:
                            rivales = rival
                            plugintools.log("rival= "+rival)
                            i = i + 1


        tv = plugintools.find_single_match(entry, '<span class="hidden-phone hidden-tablet canales"([^<]+)</span>')
        tv = tv.replace(">", "")
        #tv = encode_string(tv)
        tv = decode_string(tv)
        if tv == "":
            continue
        else:
            tv = tv.replace("(Canal+, Astra", "")
            tv = tv.split(",")
            tv_a = tv[0]
            tv_a = tv_a.rstrip()
            tv_a = tv_a.lstrip()
            tv_a = tv_a.replace(")", "")
            plugintools.log("tv_a= "+tv_a)
            print len(tv)
            if len(tv) == 2:
                tv_b = tv[1]
                tv_b = tv_b.lstrip()
                tv_b = tv_b.rstrip()
                tv_b = tv_b.replace(")", "")
                tv_b = tv_b.replace("(Bar+ dial 333-334", "")
                tv_b = tv_b.replace("(Canal+", "")
                tv = tv_a + " / " + tv_b
                plot = tv
                plugintools.log("plot= "+plot)

            elif len(tv) == 3:
                tv_b = tv[1]
                tv_b = tv_b.lstrip()
                tv_b = tv_b.rstrip()
                tv_b = tv_b.replace(")", "")
                tv_b = tv_b.replace("(Bar+ dial 333-334", "")
                tv_b = tv_b.replace("(Canal+", "")
                tv_c = tv[2]
                tv_c = tv_c.lstrip()
                tv_c = tv_c.rstrip()
                tv_c = tv_c.replace(")", "")
                tv_c = tv_c.replace("(Bar+ dial 333-334", "")
                tv_c = tv_c.replace("(Canal+", "")
                tv = tv_a + " / " + tv_b + " / " + tv_c
                plot = tv
                plugintools.log("plot= "+plot)

            elif len(tv) == 4:
                tv_b = tv[1]
                tv_b = tv_b.lstrip()
                tv_b = tv_b.rstrip()
                tv_b = tv_b.replace(")", "")
                tv_b = tv_b.replace("(Bar+ dial 333-334", "")
                tv_b = tv_b.replace("(Canal+", "")
                tv_c = tv[2]
                tv_c = tv_c.lstrip()
                tv_c = tv_c.rstrip()
                tv_c = tv_c.replace(")", "")
                tv_c = tv_c.replace("(Bar+ dial 333-334", "")
                tv_c = tv_c.replace("(Canal+", "")
                tv_d = tv[3]
                tv_d = tv_d.lstrip()
                tv_d = tv_d.rstrip()
                tv_d = tv_d.replace(")", "")
                tv_d = tv_d.replace("(Bar+ dial 333-334", "")
                tv_d = tv_d.replace("(Canal+", "")
                tv = tv_a + " / " + tv_b + " / " + tv_c + " / " + tv_d
                plot = tv
                plugintools.log("plot= "+plot)

            elif len(tv) == 5:
                tv_b = tv[1]
                tv_b = tv_b.lstrip()
                tv_b = tv_b.rstrip()
                tv_b = tv_b.replace(")", "")
                tv_b = tv_b.replace("(Bar+ dial 333-334", "")
                tv_b = tv_b.replace("(Canal+", "")
                tv_c = tv[2]
                tv_c = tv_c.lstrip()
                tv_c = tv_c.rstrip()
                tv_c = tv_c.replace(")", "")
                tv_c = tv_c.replace("(Bar+ dial 333-334", "")
                tv_c = tv_c.replace("(Canal+", "")
                tv_d = tv[3]
                tv_d = tv_d.lstrip()
                tv_d = tv_d.rstrip()
                tv_d = tv_d.replace(")", "")
                tv_d = tv_d.replace("(Bar+ dial 333-334", "")
                tv_d = tv_d.replace("(Canal+", "")
                tv_e = tv[4]
                tv_e = tv_e.lstrip()
                tv_e = tv_e.rstrip()
                tv_e = tv_e.replace(")", "")
                tv_e = tv_e.replace("(Bar+ dial 333-334", "")
                tv_e = tv_e.replace("(Canal+", "")
                tv = tv_a + " / " + tv_b + " / " + tv_c + " / " + tv_d + " / " + tv_e
                # tv = tv.replace(")", "")
                plot = tv
                plugintools.log("plot= "+plot)

            elif len(tv) == 6:
                tv_b = tv[1]
                tv_b = tv_b.lstrip()
                tv_b = tv_b.rstrip()
                tv_b = tv_b.replace(")", "")
                tv_b = tv_b.replace("(Bar+ dial 333-334", "")
                tv_b = tv_b.replace("(Canal+", "")
                tv_c = tv[2]
                tv_c = tv_c.lstrip()
                tv_c = tv_c.rstrip()
                tv_c = tv_c.replace(")", "")
                tv_c = tv_c.replace("(Bar+ dial 333-334", "")
                tv_c = tv_c.replace("(Canal+", "")
                tv_d = tv[3]
                tv_d = tv_d.lstrip()
                tv_d = tv_d.rstrip()
                tv_d = tv_d.replace(")", "")
                tv_d = tv_d.replace("(Bar+ dial 333-334", "")
                tv_d = tv_d.replace("(Canal+", "")
                tv_e = tv[4]
                tv_e = tv_e.lstrip()
                tv_e = tv_e.rstrip()
                tv_e = tv_e.replace(")", "")
                tv_e = tv_e.replace("(Bar+ dial 333-334", "")
                tv_e = tv_e.replace("(Canal+", "")
                tv_f = tv[5]
                tv_f = tv_f.lstrip()
                tv_f = tv_f.rstrip()
                tv_f = tv_f.replace(")", "")
                tv_f = tv_f.replace("(Bar+ dial 333-334", "")
                tv_f = tv_f.replace("(Canal+", "")
                tv = tv_a + " / " + tv_b + " / " + tv_c + " / " + tv_d + " / " + tv_e + " / " + tv_f
                # tv = tv.replace(")", "")
                plot = tv
                plugintools.log("plot= "+plot)

            elif len(tv) == 7:
                tv_b = tv[1]
                tv_b = tv_b.lstrip()
                tv_b = tv_b.rstrip()
                tv_b = tv_b.replace(")", "")
                tv_b = tv_b.replace("(Bar+ dial 333-334", "")
                tv_b = tv_b.replace("(Canal+", "")
                tv_c = tv[2]
                tv_c = tv_c.lstrip()
                tv_c = tv_c.rstrip()
                tv_c = tv_c.replace(")", "")
                tv_c = tv_c.replace("(Bar+ dial 333-334", "")
                tv_c = tv_c.replace("(Canal+", "")
                tv_d = tv[3]
                tv_d = tv_d.lstrip()
                tv_d = tv_d.rstrip()
                tv_d = tv_d.replace(")", "")
                tv_d = tv_d.replace("(Bar+ dial 333-334", "")
                tv_d = tv_d.replace("(Canal+", "")
                tv_e = tv[4]
                tv_e = tv_e.lstrip()
                tv_e = tv_e.rstrip()
                tv_e = tv_e.replace(")", "")
                tv_e = tv_e.replace("(Bar+ dial 333-334", "")
                tv_e = tv_e.replace("(Canal+", "")
                tv_f = tv[5]
                tv_f = tv_f.lstrip()
                tv_f = tv_f.rstrip()
                tv_f = tv_f.replace(")", "")
                tv_f = tv_f.replace("(Bar+ dial 333-334", "")
                tv_f = tv_f.replace("(Canal+", "")
                tv_g = tv[6]
                tv_g = tv_g.lstrip()
                tv_g = tv_g.rstrip()
                tv_g = tv_g.replace(")", "")
                tv_g = tv_g.replace("(Bar+ dial 333-334", "")
                tv_g = tv_g.replace("(Canal+", "")
                tv = tv_a + " / " + tv_b + " / " + tv_c + " / " + tv_d + " / " + tv_e + " / " + tv_f + " / " + tv_g
                plot = tv
                plugintools.log("plot= "+plot)
            else:
                tv = tv_a
                plot = tv_a
                plugintools.log("plot= "+plot)


            title = momentum + "h " + '[COLOR lightyellow][B]' + category + '[/B][/COLOR] ' + '[COLOR green]' + champ + '[/COLOR]' + " " + '[COLOR lightyellow][I]' + rivales + '[/I][/COLOR] [I][COLOR red]' + plot + '[/I][/COLOR]'
            #plugintools.add_item(action="contextMenu", plot = plot , title = title , thumbnail  = 'http://i2.bssl.es/telelocura/2009/05/futbol-tv.jpg' , fanart = art + 'agenda2.jpg' , folder = True, isPlayable = False)
            futboltv.write(title+'\n')

    
    

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
    


def get_fecha():

    from datetime import datetime

    ahora = datetime.now()
    anno_actual = ahora.year
    mes_actual = ahora.month
    dia_actual = ahora.day
    fecha = str(dia_actual) + "/" + str(mes_actual) + "/" + str(anno_actual)
    plugintools.log("fecha de hoy= "+fecha)
    return fecha    
    
            
            
def decode_string(string):
    string = string.replace("&nbsp;&nbsp;", "")
    string = string.replace("indexf.php?comp=", "")
    string = string.replace('>', "")
    string = string.replace('"', "")
    string = string.replace("\n", "")
    string = string.strip()
    string = string.replace('\xfa', 'ú')
    string = string.replace('\xe9', 'é')
    string = string.replace('\xf3', 'ó')
    string = string.replace('\xfa', 'ú')
    string = string.replace('\xaa', 'ª')
    string = string.replace('\xe1', 'á')
    string = string.replace('&#241;', 'ñ')
    string = string.replace('&#237;', 'í')
    string = string.replace('&#250;', 'ú')
    string = string.replace('\xf1', 'ñ').strip()
    

    return string
