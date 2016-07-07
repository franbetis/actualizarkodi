# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Parser de LiveSoccerTV para PLD.VisionTV
# Version 0.1 (05.05.2014)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
#------------------------------------------------------------

import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin
import plugintools

from __main__ import *

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")

playlists = xbmc.translatePath(os.path.join('special://userdata/playlists', ''))
temp = xbmc.translatePath(os.path.join('special://userdata/playlists/tmp', ''))


def lstv0(params):
    plugintools.log("[%s %s] LiveSoccerTV " % (addonName, addonVersion))

    thumbnail = params.get("thumbnail")
    fanart = params.get("fanart")
    url = params.get("url")
    
    data = gethttp_referer_headers(url,url)
    today0 = plugintools.find_single_match(data, '<a class="open-calendar">(.*?)</a>')
    today1 = plugintools.find_single_match(data, '<a class="open-calendar navbar_cal_current-data">(.*?)</a>')
    today0 = diasem(today0)
    plugintools.add_item(action="", title='[COLOR lightyellow][B]LiveSoccerTV[/B] / [COLOR lightgreen][I]'+today0+' '+today1+'[/I][/COLOR]', url = "", thumbnail = thumbnail , fanart = fanart, folder = False, isPlayable = False)
   
    ligas = plugintools.find_multiple_matches(data, '<div class="clearfix b_trim">(.*?)<div class="b_league -low -blue-bg -accordion -white-border-bottom">')
    liga_logo = plugintools.find_multiple_matches(data, 'class="fll b_league_logo"><img src="([^"]+)')
    print 'liga_logo',liga_logo
    i=0
    for entry in ligas:
        cabecera = plugintools.find_single_match(entry, '<span class="fll b_league_name b_trim_inner">(.*?)</span>')
        try: ligalogo = liga_logo[i]
        except: ligalogo = thumbnail        
        #plugintools.log("cabecera= "+cabecera)
        cabecera=cabecera.replace("&#039;", "'")
        plugintools.add_item(action="", title='[COLOR orange][B]'+cabecera+'[/B][/COLOR]', fanart=fanart, thumbnail=ligalogo, url="", folder=False, isPlayable=False)
        matches = plugintools.find_multiple_matches(entry, '<div class="b_match_info-elem-wrapper">(.*?)class="b_match_all-link"></a></div>')
        i = i + 1
        for entry in matches:
            url = 'http'+plugintools.find_single_match(entry, 'href="http([^"]+)')
            teams = plugintools.find_multiple_matches(entry, '<span>(.*?)</span>')
            goals = plugintools.find_multiple_matches(entry, '<div class="b_match_count">(.*?)</div>')
            chs = plugintools.find_single_match(entry, '<div class="b_match_channel_links">(.*?)</div>').strip()
            chs = chs.split(",")
            bcasters = ""
            for item in chs:
                if bcasters == "": bcasters = item
                else: bcasters = bcasters + ", " + item
            if chs[0] == "":
                bcasters = 'Sin emisión en España'
            print bcasters
            bcasters = bcasters.replace("\t", "")
            if len(goals) == 2:
                match_title = '[COLOR white]'+teams[0] + '[COLOR lightyellow][B] '+goals[0]+'[/COLOR][/B][COLOR white] vs ' + teams[1]+' [/COLOR][COLOR lightyellow][B]'+goals[1]+'[/COLOR][/B]'
            else:
                match_title = '[COLOR white]'+teams[0] + ' vs ' + teams[1]+'[/COLOR]'
            match_title=match_title.replace("&#039;", "'")
            plugintools.add_item(action="lstv1", title=match_title, url=url, thumbnail=ligalogo, extra=bcasters, fanart=fanart, folder=False, isPlayable=False)


def lstv1(params):
    menu_selec = ['[COLOR cyan]'+params.get("extra")+'[/COLOR]', "Ver cobertura internacional", "Estadísticas en vivo"]

    dia_lstv = plugintools.selector(menu_selec, params.get("title"))
    if dia_lstv == 1: lstv2()
    if dia_lstv == 2: lstv3()


def lstv2():
    params = plugintools.get_params()

    url = params.get("url")
    data = gethttp_referer_headers(url,url)
    
    match_coverage = plugintools.find_single_match(data, 'International Coverage(.*?)<div id="match-lineups" class="match-info hidden">')
    country_match = plugintools.find_multiple_matches(match_coverage, '<div class="row">(.*?)<div class="b_channel col-xs-12 -low b_trim -international">')
    for entry in country_match:
        plugintools.log("entry= "+entry)
        country = plugintools.find_single_match(entry, '<div class="fll b_channel_name -broadcast -country b_trim_inner">(.*?)</div>').replace("&nbsp;", "").strip()
        if country != "":
            channels = ""
            channel = plugintools.find_multiple_matches(entry, '<div class="fll b_channel_name -broadcast b_trim_inner">(.*?)</div>')
            for item in channel:
                if channels == "":
                    channels = item
                else:
                    channels = channels + ', '+item                    

            lstv_file = open(temp + "lstv.tmp", "a")
            lstv_file.write('[COLOR gold][B]'+country+'[/B][/COLOR][COLOR white]: '+channels+'[/COLOR]\n')


    lstv_file.close()
    params["url"] = temp + 'lstv.tmp'
    txt_reader(params)


def lstv3():
    params=plugintools.get_params()
    title = params.get("title").replace("[COLOR white]", "[COLOR lightgreen]")
    team_a = title.split(" vs ")[0]
    team_b = title.split(" vs ")[1]
    url = 'http://m.livesoccertv.com/match/1709586/olympiakos-piraeus-vs-bayern-m-nchen/'
    data = gethttp_referer_headers(url,url)

    lstv_file = open(temp + "lstv_stats.tmp", "wb")
    lstv_file.write("\n[COLOR red]"+title+"[/COLOR]\n")    
    lstv_file.write("\n[COLOR gold]TITULARES[/COLOR]\n")
            
    stats = plugintools.find_single_match(data, '<span>Stats</span>(.*?)Substitutes</h3>')
    players_a = plugintools.find_multiple_matches(stats, '<div class="fll b_lineup_players b_trim_inner -right">(.*?)</div>')
    players_b = plugintools.find_multiple_matches(stats, '<div class="fll b_lineup_players b_trim_inner -left">(.*?)</div>')
    i = 0
    while i < len(players_a):
        players_a[i]=players_a[i].replace("</span>", "[/COLOR] ").replace('<span class="b_lineup_number">', '[COLOR lightyellow]').rstrip()
        players_b[i]=players_b[i].replace("</span>", "[/COLOR] ").replace('<span class="b_lineup_number">', '[COLOR lightyellow]').rstrip()
        spaces = 80 - len(players_b[i])
        plugintools.log("longitud_texto= "+str(len(players_a[i])))
        plugintools.log("espacios que faltan= "+str(spaces))
        tabulador = ""
        j = spaces
        k = 0 
        while k <= j:
            tabulador = tabulador + "..."
            k = k + 1
        line_player = players_b[i]+tabulador+players_a[i]+'\n'
        lstv_file.write(line_player)
        print line_player
        i = i + 1

    lstv_file.write("\n\n[COLOR gold]SUPLENTES[/COLOR]\n")
    stats = plugintools.find_single_match(data, 'Substitutes</h3>(.*?)<div id="match-stats"')
    players_a = plugintools.find_multiple_matches(stats, '<div class="fll b_lineup_players b_trim_inner -right">(.*?)</div>')
    players_b = plugintools.find_multiple_matches(stats, '<div class="fll b_lineup_players b_trim_inner -left">(.*?)</div>')
    i = 0
    while i < len(players_a):
        players_a[i]=players_a[i].replace("</span>", "[/COLOR] ").replace('<span class="b_lineup_number">', '[COLOR lightyellow]').rstrip()
        players_b[i]=players_b[i].replace("</span>", "[/COLOR] ").replace('<span class="b_lineup_number">', '[COLOR lightyellow]').rstrip()
        spaces = 80 - len(players_b[i])
        tabulador = ""
        j = spaces
        k = 0 
        while k <= j:
            tabulador = tabulador + "..."
            k = k + 1
        line_player = players_b[i]+tabulador+players_a[i]+'\n'
        lstv_file.write(line_player)
        print line_player
        i = i + 1
    
    lstv_file.close()
    params["url"] = temp + 'lstv_stats.tmp'
    txt_reader(params)    
    
            
def gethttp_referer_headers(url,referer):
    plugintools.modo_vista("tvshows");request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    request_headers.append(["Referer", referer])
    body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers);
    try: r='\'set-cookie\',\s\'([^;]+.)';jar=plugintools.find_single_match(str(response_headers),r);jar=getjad(jar);
    except: pass
    try: r='\'location\',\s\'([^\']+)';loc=plugintools.find_single_match(str(response_headers),r);
    except: pass
    if loc:
     request_headers.append(["Referer",url]);
     if jar: request_headers.append(["Cookie",jar]);#print jar
     body,response_headers=plugintools.read_body_and_headers(loc,headers=request_headers);
     try: r='\'set-cookie\',\s\'([^;]+.)';jar=plugintools.find_single_match(str(response_headers),r);jar=getjad(jar);
     except: pass
     plugintools.modo_vista("tvshows")
    return body


def diasem(dia):
    if dia == "Monday":
        dia = "Lun"
    elif dia == "Tuesday":
        dia = "Mar"
    elif dia == "Wednesday":
        dia = "Mié"
    elif dia == "Thursday":
        dia = "Jue"
    elif dia == "Friday":
        dia = "Vie"
    elif dia == "Saturday":
        dia = "Sáb"
    elif dia == "Sunday":
        dia = "Dom"

    return dia
