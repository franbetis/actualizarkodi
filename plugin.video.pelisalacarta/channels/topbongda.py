# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para livetv
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os
import sys
import re
from core import scrapertools
from core import logger
from core import config
from core import jsontools
from core.item import Item
from servers import servertools
import locale
import xbmc
from core.scrapertools import decodeHtmlentities as dhe
__channel__ = "topbongda"
__category__ = "d"
__type__ = "generic"
__title__ = "Topbongda"
__language__ = "ES"

host ="https:"
song = os.path.join(config.get_runtime_path(), "music", 'Easy.mp3')

DEBUG = config.get_setting("debug")

def isGeneric():
    
    return True

#Proxy para acceder a datos
def get_page(url):

    data = scrapertools.cachePage("http://ssl-proxy.my-addr.org/myaddrproxy.php/"+url)
    
    
    return data


def mainlist(item):
    logger.info("pelisalacarta.topbongda mainlist")
    itemlist = []
    
   
    if item.extra != "next_page":
       item.url = "http://topbongda.com"#/wendy/ajax/home_matches/?page=1"
       if not xbmc.Player().isPlaying():
          xbmc.executebuiltin('xbmc.PlayMedia('+song+')')
    data = dhe(get_page(item.url))
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;|&amp;","",data)
    #data = jsontools.load_json(data)

    patrongames= '<nav class="display-list">(.*?)<div class="match-block mdl-shadow--2dp ng-cloak" ng-repeat="match_block in match_data" ng-if="match_data.length > 0">'
    matchesgames= re.compile(patrongames,re.DOTALL).findall(data)
    for bloque_games in matchesgames:
        patrondaygames = '<i class="material-icons md-18">date_range</i>(.*?)<small>(.*?)</div></li></ul></div>'
        matchesdaygames =re.compile(patrondaygames,re.DOTALL).findall(bloque_games)
        for fecha, bloque_partidos in matchesdaygames:
            fecha = fecha.strip()
            #LIVE
            patronlive ='<span class="time">(.*?)</span>.*?<span class="minute">(.*?)<i class="playing">.*?<strong>(.*?)</strong>.*?<img src="/myaddrproxy.php/(.*?)".*?class="score">(.*?)</a>.*?<img src="/myaddrproxy.php/(.*?)" alt=""></a><strong>(.*?)</strong>.*?<a href="/myaddrproxy.php/(.*?)"'
            matcheslive=re.compile(patronlive,re.DOTALL).findall(bloque_partidos)
            for hora,minuto,team1,thumbnail,score,fanart,team2,url in matcheslive:
                thumbnail= re.sub(r"https","https:/",thumbnail)
                thumbnail= re.sub(r"_.*?\.",".",thumbnail)
                fanart= re.sub(r"https","https:/",fanart)
                fanart= re.sub(r"_.*?\.",".",fanart)
                minuto=minuto.strip()
                if "HT" in minuto:
                    minuto = "Descanso"
                title =  "[COLOR chartreuse][B]"+team1+"[/B][/COLOR]"+"[COLOR yellowgreen]__[/COLOR]"+"[COLOR yellow][B]"+score+"[/B][/COLOR]"+"[COLOR yellowgreen]__[/COLOR]"+"[COLOR chartreuse][B]"+team2+"[/B][/COLOR]"
                title = "[COLOR olivedrab]([/COLOR]"+"[COLOR yellowgreen][B]"+minuto+"[B][/COLOR]"+"[COLOR olivedrab])[/COLOR]"+" "+title+" "+"[COLOR crimson][B]LIVE!![/B][/COLOR]"
                url = re.sub(r"https/","http://",url)+"sopcast"
                url = re.sub(r"/ti-le","",url)
                if "default" in thumbnail :
                    thumbnail = "http://s6.postimg.org/bwlfc3fdd/topbongdafan.jpg"
                if "default" in fanart :
                    fanart = "http://s6.postimg.org/bwlfc3fdd/topbongdafan.jpg"
                itemlist.append( Item(channel=__channel__, title=title,action="enlaces",url = url,thumbnail=thumbnail,fanart="http://s6.postimg.org/bwlfc3fdd/topbongdafan.jpg", fulltitle= "[COLOR chartreuse][B]"+team1+" Vs "+team2+"[/B][/COLOR]",extra="LIVE",folder=True) )
            #NO LIVE
            patronnolive ='<div class="info"><span class="time">(\d+:\d+)</span><a href.*?class="league">(.*?)</a>.*?<strong>(.*?)</strong>.*?<img.*?"/myaddrproxy.php/(.*?)" alt="">.*?<img.*?"/myaddrproxy.php/(.*?)" alt=""></a><strong>(.*?)</strong>.*?<a href="/myaddrproxy.php/(.*?)" '
            matchesnolive=re.compile(patronnolive,re.DOTALL).findall(bloque_partidos)
            for hora,league,team1,thumbnail,fanart,team2,url in matchesnolive:
                
                thumbnail= re.sub(r"https","https:/",thumbnail)
                thumbnail= re.sub(r"_.*?\.",".",thumbnail)
                fanart= re.sub(r"https","https:/",fanart)
                fanart= re.sub(r"_.*?\.",".",fanart)
                
                from time import gmtime, strftime
                import time
                get_date=strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                
                ok_date =re.compile('(\d+)-(\d+)-(\d+) (\d+:\d+:\d+)',re.DOTALL).findall(get_date)
                for year, mes, dia, current_hour in ok_date:
                   date =dia+"/"+mes+"/"+year
                   current_date = date
                
                if fecha == "Hôm Nay":
                   check_hour = scrapertools.get_match(current_hour,'(\d+):\d+')
                   if check_hour >= "19":
                      dates =re.compile('(\d+)(/\d+/\d+)',re.DOTALL).findall(date)
                      for d, m_y in dates:
                          days = int(d) +1
                          date = str(days) + m_y
                          extra ="nuevodia"
                   else:
                      date =date
                      
                elif fecha == "Ngày Mai":
                     check_hour = scrapertools.get_match(current_hour,'(\d+):\d+')
                     dates = re.compile('(\d+)(/\d+/\d+)',re.DOTALL).findall(date)
                     for d, m_y in dates:
                         # check_hour ="00"
                         if check_hour >= "19":
                            
                            days = int(d) +2
                            date = str(days) + m_y
                         else:
                            days = int(d) +1
                            date = str(days) + m_y
                     
                else:
                    check_hour = scrapertools.get_match(current_hour,'(\d+):\d+')
                    dates = re.compile('(\d+)(/\d+/\d+)',re.DOTALL).findall(fecha)
                    for d, m_y in dates:
                        if check_hour >= "19":
                            days = int(d) -1
                            date = str(days) + m_y
                        else:
                            date = fecha
                time= re.compile('(\d+):(\d+)',re.DOTALL).findall(hora)
                #Corregimos las 5h de diferencia horaria con Vietnam
                for horas, minutos in time:
                    if  horas== "00":
                        horas = horas.replace("00","24")
                        #if minutos != "00":
                        dates = re.compile('(\d+)(/\d+/\d+)',re.DOTALL).findall(date)
                        for d, m_y in dates:
                            days = int(d) - 1
                            date = str(days) + m_y
                    
                
                    check =re.compile('(\d)\d',re.DOTALL).findall(horas)
                    if "0"in check:
                        horas = horas.replace("0","")
                        horas = 24 + int(horas)
                        dates = re.compile('(\d+)(/\d+/\d+)',re.DOTALL).findall(date)
                        for d, m_y in dates:
                            days = int(d) - 1
                            date = str(days) + m_y

                    wrong_time =int(horas)
                    value = 5
                    correct_time = wrong_time - value

                    if correct_time > 24:
                       correct_time = int(correct_time) - 24
                       
                       dates = re.compile('(\d+)(/\d+/\d+)',re.DOTALL).findall(date)
                       for d, m_y in dates:
                           days = int(d) + 1
                           date = str(days) + m_y
                    correct_time = '%02d' % int(correct_time)

                    ok_time = correct_time +":"+ minutos
                if "24:" in ok_time:
                    ok_time =ok_time.replace("24:","00:")
                    dates = re.compile('(\d+)(/\d+/\d+)',re.DOTALL).findall(date)
                    for d, m_y in dates:
                        days = int(d) + 1
                        date = str(days) + m_y

                check_date =scrapertools.get_match(date,'(\d+)/\d+/\d+')
                check_date = check_date.strip()

                if int(check_date) < 10:
                   if "0" in (check_date):
                       continue

                   date = "0" + date
                if "Ngoại Hạng Anh" in league:
                    league = "Premier League"
                if "Hạng Nhất Anh" in league:
                    league = "Premier League"

                extra =ok_time+"|"+date
                title = team1+" Vs "+team2
                title ="[COLOR chartreuse]"+ok_time+"[/COLOR]" +"[COLOR olivedrab]--[/COLOR]"+"[COLOR gold]"+date+"[/COLOR]"+" "+"[COLOR seagreen][B]"+title+"[/B][/COLOR]" + " "+"[COLOR olivedrab]([/COLOR]"+"[COLOR yellowgreen]"+league+"[/COLOR]"+"[COLOR olivedrab])[/COLOR]"
                if "default" in thumbnail :
                    thumbnail = "http://s6.postimg.org/bwlfc3fdd/topbongdafan.jpg"
                if "default" in fanart :
                    fanart = "http://s6.postimg.org/bwlfc3fdd/topbongdafan.jpg"
                itemlist.append( Item(channel=__channel__, title=title,action="enlaces",url = url ,thumbnail=thumbnail,fanart=fanart, fulltitle= "[COLOR seagreen][B]"+team1+" Vs "+team2+"[/B][/COLOR]",extra =extra,folder=True) )
    
    
    return itemlist




def enlaces(item):
    logger.info("pelisalacarta.topbongda scraper")
    
    itemlist = []
    
    # Descarga la página
    
    if "sopcast" in item.url:
        data = get_page(item.url)
        try:
           eid = scrapertools.get_match(data,'http.get.*?eid=(.*?)"')
        
        
           url ="http://topbongda.com/xem-bong-da-truc-tuyen/api/link/?eid="+ eid
           
           data = get_page(url)
           data = jsontools.load_json(data)
           sop = data['sop']
          
           if sop:
              tipo = "[COLOR aquamarine][B]Sopcast[/B][/COLOR]"
              thumbnail= "http://s6.postimg.org/v9z5ggmfl/sopcast.jpg"
            
              itemlist.append( Item(channel=__channel__,title=tipo.strip(), url="",action="mainlist",thumbnail=thumbnail, fanart= "http://s6.postimg.org/6756rs973/topbongda.jpg",folder=False) )
              for sop in data["sop"]:
                  no_sop = "false"
                  url = sop['url']
                  bibrate = sop['bitrate']
                  languaje =sop['language']
                  if languaje == '':
                      languaje ="Desconocido"
            
                  title = languaje.strip()
                  title = "[COLOR darkolivegreen][B]"+title+"[/B][/COLOR]"
                  if str(bibrate) != "0":
                     title = title +"  "+ "[COLOR palegreen]"+"("+str(bibrate)+" Kbps"+")"+"[/COLOR]"
                  itemlist.append( Item(channel=__channel__, title="        "+title,action="play",url =url,thumbnail= thumbnail,fanart="http://s6.postimg.org/6756rs973/topbongda.jpg",fulltitle = item.fulltitle, folder=True))
           else :
                 no_sop = "true"
           ace = data['ace']
           if ace:
               no_ace= "false"
               tipo = "[COLOR yellow][B]Acestrem[/B][/COLOR]"
               thumbnail= "http://s6.postimg.org/c2c0jv441/torrent_stream_logo_300x262.png"
               itemlist.append( Item(channel=__channel__,title=tipo.strip(), url="",action="mainlist",thumbnail=thumbnail, fanart= "http://s6.postimg.org/6756rs973/topbongda.jpg",folder=False) )
               
               for ace in data["ace"]:
            
                   url = ace['url']
                   bibrate = ace['bitrate']
                   languaje =ace['language']
                   if languaje == '':
                      languaje ="Desconocido"
                   title = languaje.strip()
                   title = "[COLOR darkolivegreen][B]"+title+"[/B][/COLOR]"
            
            
                   if str(bibrate) != "0":
                      title = title +"  "+ "[COLOR palegreen]"+"("+str(bibrate)+" Kbps"+")"+"[/COLOR]"
                
                   itemlist.append( Item(channel=__channel__, title="        "+title,action="play",url =url,thumbnail= thumbnail,fanart="http://s6.postimg.org/6756rs973/topbongda.jpg",fulltitle = item.fulltitle, folder=True) )
           else :
                no_ace = "true"

           if no_sop == "true" and no_ace =="true":
              title ="No hay ningun enlace Sopcast / Acestream".title()
              itemlist.append( Item(channel=__channel__,title="[COLOR limegreen][B]"+title+"[/B][/COLOR]", url="",action="mainlist",fanart="http://s6.postimg.org/unwjdqopd/topbongdafannolink.jpg",thumbnail="http://s6.postimg.org/m6x12tk0h/topbongdathumbnolink.png", folder=False) )
              
        except:
            xbmc.executebuiltin('Action(Back)')
            xbmc.sleep(100)
            xbmc.executebuiltin('Notification([COLOR palegreen][B]Partido[/B][/COLOR], [COLOR yellow][B]'+'sin enlaces'.upper()+'[/B][/COLOR],4000,"http://s6.postimg.org/ke8bfk7f5/topbongda.png")')
        
        
    else:
        
        check_hour = scrapertools.get_match(item.extra.split("|")[0],'(\d)\d:\d+')

        from time import gmtime, strftime
        import time
        get_date=strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        
        ok_date_hour =re.compile('(\d+)-(\d+)-(\d+) (\d+:\d+:\d+)',re.DOTALL).findall(get_date)
        for year,mes,day,hour in ok_date_hour:
            current_day =day+"/"+mes+"/"+year
            current_hour = hour
        
        today =scrapertools.get_match(current_day,'(\d+)/\d+/\d+')
        dia_match = scrapertools.get_match(item.extra.split("|")[1],'(\d+)/\d+/\d+')
        check_day =int(dia_match) - int(today)
        
        check_match_hour = scrapertools.get_match(item.extra.split("|")[0],'(\d+):\d+')
        
        check_today_hour = scrapertools.get_match(current_hour,'(\d+):\d+')
        
        if item.extra.split("|")[1] == current_day or item.extra.split("|")[1] != current_day and check_day <= 2   :
            
            time= re.compile('(\d+):(\d+):(\d+)',re.DOTALL).findall(get_date)
            for h,m,s in time:
                hora=h
                min = m
                            
            time_match = re.compile('(\d+):(\d+)',re.DOTALL).findall(item.extra.split("|")[0])
            
            for h,m in time_match:
                check_time_match = scrapertools.get_match(h,'(\d)\d')
                if "0" in str(check_hour) and str(check_match_hour) <= str(check_today_hour)   or  str(check_match_hour) < str(check_today_hour) :
                    #check_day == 1 and
                    h = 24 + int(h)
                    
                hora_match = h
                min_match = m
                remaining = int(hora_match) - int(hora)
                
                if min != "00":
                    correct_min = (60 - int(min))*60
                    remaining = (int(remaining) -1)*3600
                    remaining = remaining + correct_min+(int(min_match)*60)
                else :
                    remaining = (remaining*3600)+ int(min_match)
                        
                        
                num=int(remaining)
                #dia =(int(num/84600))
                hor=(int(num/3600))
                minu=int((num-(hor*3600))/60)
                #seg=num-((hor*3600)+(minu*60))
                
                remaining= (str(hor)+"h "+str(minu)+"m ")
                if check_day == 0 and check_match_hour == check_today_hour :
                    remaining =  str(minu)+"m "
                if check_day == 1 and check_match_hour >= check_today_hour or check_day == 2  and check_match_hour <= check_today_hour:
                    
                    if check_match_hour == check_today_hour :
                        
                       remaining = "23h" +" "+ str(minu)+"m "
                    else:
                        if "0h" in remaining:
                           remaining = re.sub(r"0h","",remaining)
                        remaining = "1d" +" "+ remaining
            
                elif check_day == 2:
                    
                    remaining = "2d" + " "+remaining
                else:
                    remaining = remaining
                
        else:
            
            
            if check_day >=3 and str(check_match_hour) >= str(check_today_hour):
               remaining = str(day)+" dias"
            
            else:
               time= re.compile('(\d+):(\d+):(\d+)',re.DOTALL).findall(get_date)
               for h,m,s in time:
                   hora=h
                   min = m
               time_match = re.compile('(\d+):(\d+)',re.DOTALL).findall(item.extra.split("|")[0])
               for h,m in time_match:
                   check_time_match = scrapertools.get_match(h,'(\d)\d')
                   
                   h = 24 + int(h)
                   hora_match = h
                   min_match = m
                   remaining = int(hora_match) - int(hora)
                   if min != "00":
                      correct_min = (60 - int(min))*60
                      remaining = (int(remaining) -1)*3600
                      remaining = remaining + correct_min+(int(min_match)*60)
                   else :
                      remaining = (remaining*3600)+ int(min_match)*60
               
                   num=int(remaining)
                   dia =(int(num/84600))
                   hor=(int(num/3600))
                   minu=int((num-(hor*3600))/60)
                   remaining= "2d"+(str(hor)+"h "+str(minu)+"m ")

        no_link="Aun no hay enlaces"
        no_link = no_link.title()
        itemlist.append( Item(channel=__channel__,title="               "+"[COLOR springgreen]"+no_link+"[/COLOR]", url="",action="mainlist",fanart="http://s6.postimg.org/mktb5axsh/topbongdafantime.jpg",thumbnail="http://s6.postimg.org/ippx2qemp/topbongdathumbtime.png", folder=False) )
        itemlist.append( Item(channel=__channel__,title="                                            "+"[COLOR lawngreen]Disponibles en[/COLOR]"+"  "+"[COLOR palegreen][B]"+str(remaining)+"[/B][/COLOR]", url="",action="mainlist",fanart="http://s6.postimg.org/mktb5axsh/topbongdafantime.jpg",thumbnail="http://s6.postimg.org/ippx2qemp/topbongdathumbtime.png", folder=False) )
    return itemlist



def play(item):
    logger.info("pelisalacarta.topbongda play")
    itemlist = []
    import xbmc
    xbmc.executebuiltin('xbmc.PlayMedia(Stop)')
    fulltitle = item.fulltitle
    
    # Se incluye el título en la url para pasarlo al conector
    url= item.url + "|" + fulltitle
    
    itemlist.append(Item(channel=__channel__, title=item.title, server="p2p", url=url, action="play", folder=False))
    
    return itemlist

def translate(to_translate, to_langage="auto", langage="auto"):
    ###Traducción atraves de Google
    '''Return the translation using google translate
        you must shortcut the langage you define (French = fr, English = en, Spanish = es, etc...)
        if you don't define anything it will detect it or use english by default
        Example:
        print(translate("salut tu vas bien?", "en"))
        hello you alright?'''
    agents = {'User-Agent':"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)"}
    before_trans = 'class="t0">'
    link = "http://translate.google.com/m?hl=%s&sl=%s&q=%s" % (to_langage, langage, to_translate.replace(" ", "+"))
    request = urllib2.Request(link, headers=agents)
    page = urllib2.urlopen(request).read()
    result = page[page.find(before_trans)+len(before_trans):]
    result = result.split("<")[0]
    return result

if __name__ == '__main__':
    to_translate = 'Hola como estas?'
    print("%s >> %s" % (to_translate, translate(to_translate)))
    print("%s >> %s" % (to_translate, translate(to_translate, 'fr')))
#should print Hola como estas >> Hello how are you
#and Hola como estas? >> Bonjour comment allez-vous?





