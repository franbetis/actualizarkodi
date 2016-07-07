# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Scraper de películas para PLD.VisionTV
# Version 0.1
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Gracias a la librería plugintools de Jesús (www.mimediacenter.info)
#------------------------------------------------------------


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
import plugintools,ioncube
import requests

from __main__ import *


addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")


temp = xbmc.translatePath(os.path.join('special://home/userdata/playlists/tmp', ''))


def tmdbsearch(title):
    plugintools.log("[%s %s] Searching URL TMDB.org for... %s" % (addonName, addonId, title))

    try:
        title=title.replace(" ", "+")
        tmdb_search = 'https://ajax.googleapis.com/ajax/services/search/web?v=1.0&q='+title +'+themoviedb'
        data = gethttp_referer_headers(tmdb_search,referer='')
        url_tmdb = 'https://www.themoviedb.org/'+plugintools.find_single_match(data, 'https://www.themoviedb.org/([^"]+)')
        return url_tmdb
    except: pass


def getposter(title):
    plugintools.log("GetPoster "+title)
	
    datamovie = {}
    datamovie = themoviedb(title, datamovie)
    print 'datamovie',datamovie
    return datamovie


def save_title(title, datamovie, filename):
    plugintools.log("PLD.VisionTV Saving data... "+repr(datamovie))

    # Comprobamos si no existe el archivo para crearlo
    if not os.path.isfile(temp + filename):
        plugintools.log("Creando archivo... temp/"+filename)
        imdb_file = open(temp + filename, "a")
        imdb_file.seek(0)
        imdb_file.write('#EXTM3U,movies\n\n')  # Fijamos modo de vista para la lista de películas
        imdb_file.close()
        print "Archivo creado correctamente!"
    else:
        pass    

    # Abrimos archivo para guardar datos de película
    plugintools.log("Abriendo archivo... temp/"+filename)
    imdb_file = open(temp + filename, "a")
    title = title.strip()
    if title.find("%nfo=") >= 0:        
        url_nfo = plugintools.find_single_match(title, '%nfo=(.*?)%')
        fixed='%nfo='+url_nfo
        title=title.replace(fixed, "").replace("%", "").strip()

    # Transformamos listas en strings para guardar en M3U
    cast_final = datamovie["Cast"]
    j=len(cast_final)
    i = 0
    total_cast=""
    while i < j:
        if total_cast == "": total_cast=cast_final[i]
        else: total_cast=total_cast+", "+cast_final[i]            
        i = i + 1

    writers_final = datamovie["Writer"]
    j=len(writers_final)
    i = 0
    total_writers=""
    while i < j:
        if total_writers == "": total_writers=writers_final[i]
        else: total_writers = total_writers+', '+writers_final[i]
        i = i + 1

    genre_final = datamovie["Genre"]
    j=len(genre_final)
    i = 0
    total_genre=""
    while i < j:
        if total_genre == "": total_genre=genre_final[i]
        else: total_genre=total_genre+", "+genre_final[i]            
        i = i + 1        
        
    imdb_file.write('#EXTINF:-1,'+title+',tvg-logo="'+datamovie["Poster"]+'",tvg-wall="'+datamovie["Fanart"]+'",imdb="'+datamovie["Rating"]+'",genre="'+total_genre+'",votes="'+datamovie["Votes"]+'",time="'+str(datamovie["Duration"])+'",year="'+datamovie["Year"]+'",dir="'+datamovie["Director"]+'",wri="'+total_writers+'",plot="'+datamovie["Plot"]+'",cast="'+total_cast+'"\n')
    imdb_file.close()


def save_url(url, filename):
    plugintools.log("PLD.VisionTV Saving URL...")
    
    # Abrimos archivo para guardar datos de película
    plugintools.log("Abriendo archivo... temp/"+filename)
    imdb_file = open(temp + filename, "a")
    imdb_file.write(url+'\n\n')
    imdb_file.close()


def save_multilink(url, filename):
    plugintools.log("PLD.VisionTV Saving URL...")

    # Abrimos archivo para guardar datos de pelicula
    plugintools.log("Abriendo archivo... temp/"+filename)
    imdb_file = open(temp + filename, "a")
    imdb_file.write(url+'\n')
    imdb_file.close()

def save_multiparser(url, filename):
    plugintools.log("PLD.VisionTV Saving URL...")

    # Abrimos archivo para guardar datos de pelÃ­cula
    plugintools.log("Abriendo archivo... temp/"+filename)
    imdb_file = open(temp + filename, "a")
    imdb_file.write(url+'\n')
    imdb_file.close()


def themoviedb(title, datamovie):
    plugintools.log("The Movie Database: "+title)

    if title.find("%nfo=") >= 0:
        plugintools.log("title= "+title)
        url_nfo = plugintools.find_single_match(title, '%nfo=(.*?)%')
        fixed='%nfo='+url_nfo
        title_fixed=title.replace(fixed, "").replace("%", "").strip()
        plugintools.log("title_fixed= "+title_fixed)
        plugintools.log("fixed= "+fixed)
        plugintools.log("url_nfo= "+url_nfo)
        datamovie = nfo_reader(title_fixed, url_nfo)
        return datamovie
        
    else:
        title_fixed=title.replace(" ", "+").strip()
        url = 'https://www.themoviedb.org/search?language=es&charset=utf-8&query='+title_fixed
        plugintools.log("URL búsqueda= "+url)
        referer = 'https://www.themoviedb.org/'
        headers = {"Referer": 'https://www.themoviedb.org/', 'user-agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14'}
        data = gethttp_referer_headers(url,referer)
        url_film = 'https://www.themoviedb.org/movie/'+plugintools.find_single_match(data, '<a id="movie_([^"]+)')+'?language=es';url_film=url_film.strip()
        plugintools.log("URL Film: "+url_film)    
        r=requests.get(url_film);body=r.content
        #plugintools.log("body= "+body)
        logo_pattern = plugintools.find_single_match(body, '<img itemprop="image" id="upload_poster"(.*?)>')
        logo = plugintools.find_single_match(logo_pattern, 'src="([^"]+)')
        datamovie["Poster"] = logo.strip()
        year = plugintools.find_single_match(body, '<h3 id="year">(.*?)</h3>').replace("(", "").replace(")", "").strip()
        #plugintools.log("year= "+year)
        datamovie["Year"]=year
        duration_match = plugintools.find_single_match(body, '<p><strong>Runtime:</strong>(.*?)</p>')
        #plugintools.log("duration_match= "+duration_match)
        duration = plugintools.find_single_match(duration_match, '/>(.*?)</span>')        
        #plugintools.log("duration= "+duration)
        datamovie["Duration"]=duration
        sinopsis = plugintools.find_single_match(body, 'itemprop="description">(.*?)</p>')
        sinopsis = sinopsis.replace('"', "")
        datamovie["Plot"]=sinopsis
        #plugintools.log("sinopsis= "+sinopsis)
        crew_match = plugintools.find_single_match(body, '<h3>Crew</h3>(.*?)</table>')
        match_director = plugintools.find_single_match(crew_match, '<td class="job">Director:</td>(.*?)</td>')
        director = plugintools.find_multiple_matches(match_director, 'itemprop="name">(.*?)</span>')
        directores = ""
        for match in director:
            if directores == "":
                directores = match
            else:
                directores = directores+", "+match
        datamovie["Director"] = directores
        #plugintools.log("director(es)= "+directores)
        match_writers = plugintools.find_single_match(crew_match, '<td class="job">Writers:</td>(.*?)</td>')
        writers = plugintools.find_multiple_matches(match_director, 'itemprop="name">(.*?)</span>')
        guionistas = ""
        for entry in writers:
            if guionistas == "":
                guionistas = entry
            else:
                guionistas = guionistas+", "+entry
        datamovie["Writer"] = guionistas
        #plugintools.log("guionista(s)= "+guionistas)
        backdrop = plugintools.find_single_match(body, '<meta name="twitter:image" content="([^"]+)')
        datamovie["Fanart"]=backdrop
        #plugintools.log("backdrop= "+backdrop)
        match_genres = plugintools.find_single_match(body, '<span id="genres">(.*?)</ul>')
        genres_match = plugintools.find_multiple_matches(match_genres, '<span itemprop="genre">(.*?)</span>')
        generos = ""
        for genero in genres_match:
            if generos == "":
                generos = genero
            else:
                generos = generos+", "+genero
        datamovie["Genre"] = generos
        rating = plugintools.find_single_match(body, '<span itemprop="ratingValue" id="rating_hint">(.*?)</span>')
        datamovie["Rating"]=rating
        votes = plugintools.find_single_match(body, '<span itemprop="ratingCount">(.*?)</span>')
        datamovie["Votes"]=votes

        cast_bloque = plugintools.find_single_match(body, '<h3>Cast</h3>(.*?)</table>')
        cast_item = plugintools.find_multiple_matches(cast_bloque, '<div class="castItem">(.*?)</div>')
        cast_final = ""
        for item in cast_item:
            cast_item = plugintools.find_single_match(item, 'itemprop="name">([^<]+)</span>')
            if cast_final == "": cast_final=cast_item
            else: cast_final=cast_final+', '+cast_item
            
        datamovie["Cast"]=cast_final
        return datamovie


def nfo_reader(title, url):
    data=gethttp_referer_headers(url,referer="")
    datamovie={}
    title=plugintools.find_single_match(data, '<title>([^<]+)')
    datamovie["Title"] = title
    imdb_rating=plugintools.find_single_match(data, '<rating>([^<]+)')
    datamovie["Rating"] = imdb_rating
    top = plugintools.find_single_match(data, '<top250>([^<]+)')
    datamovie["Top250"]=top
    year=plugintools.find_single_match(data, '<year>([^<]+)')
    datamovie["Year"] = year
    votes=plugintools.find_single_match(data, '<votes>([^<]+)')
    datamovie["Votes"] = votes
    sinopsis=plugintools.find_single_match(data, '<plot>([^<]+)')
    datamovie["Plot"] = sinopsis
    tagline=plugintools.find_single_match(data, '<tagline>([^<]+)')
    datamovie["Tagline"] = tagline
    duration=plugintools.find_single_match(data, '<runtime>([^<]+)')
    datamovie["Duration"] = duration
    fanart_matches=plugintools.find_single_match(data, '<fanart>(.*?)</fanart>')
    fanart=plugintools.find_single_match(fanart_matches, '<thumb[^>]+([^<]+)').replace(">", "").strip()
    datamovie["Fanart"] = fanart
    thumbnail=plugintools.find_single_match(data, '<thumb[^>]+([^<]+)').replace(">", "").strip()
    datamovie["Poster"] = thumbnail
    genres=plugintools.find_multiple_matches(data, '<genre>([^<]+)')
    genre_final = []
    for genre in genres:
        genre_final.append(genre)
    datamovie["Genre"] = genre_final
    dir=plugintools.find_single_match(data, '<director>([^<]+)')
    datamovie["Director"] = dir
    trailer=plugintools.find_single_match(data, '<trailer>([^<]+)')
    datamovie["Trailer"] = trailer
    duration=plugintools.find_single_match(data, '<runtime>([^<]+)')
    datamovie["Duration"] = duration
    cast_item=plugintools.find_multiple_matches(data, '<actor>(.*?)</actor>')
    cast_final = []
    for item in cast_item:
        #plugintools.log("item= "+item)
        actor=plugintools.find_single_match(item, '<name>(.*?)</name>')
        cast_final.append(actor)
    datamovie["Cast"]=cast_final
    studio=plugintools.find_single_match(data, '<studio><thumb preview="([^<]+)')
    datamovie["Studio"]=studio
    writers=plugintools.find_multiple_matches(data, '<credits>(.*?)</credits>')
    writers_final=[]
    for item in writers:
        writers_final.append(item)
    datamovie["Writer"]=writers_final
    return datamovie


def gethttp_referer_headers(url,referer):
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    request_headers.append(["Referer", referer])
    body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)
    
    return body
