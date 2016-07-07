# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para Footballia
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import os
from core import logger
from core import config
from core import scrapertools
from core.item import Item

__channel__ = "footballia"
__type__ = "generic"
__title__ = "Footballia"
__language__ = "ES"

DEBUG = config.get_setting("debug")
host_footballia = "http://footballia.net"
footballia_log = os.path.join(config.get_data_path(), "footballia_login.txt")

def isGeneric():
    return True

def login():
    logger.info("pelisalacarta.channels.footballia login")

    if not os.path.exists(footballia_log): return False, "Introduce tu usuario y contraseña de footballia.net"
    else:
        try:
            file = open(footballia_log, "r")
            user = file.readline().strip()
            password = file.readline()
            file.close()
            data = scrapertools.cachePage("http://footballia.net/es")
            if user in data: return True, ""

            token = scrapertools.find_single_match(data, 'content="([^"]+)" name="csrf-token"')
            post = "utf8=✓&authenticity_token=%s&user[email]=%s&user[password]=%s&user[remember_me]=1&commit=Entra" % (token, user, password)
            data = scrapertools.cachePage("http://footballia.net/users/sign_in?locale=es", post=post)
            if "Invalid email or password" in data:
                logger.info("pelisalacarta.channels.footballia Error en el login")
                return False, "Error en el usuario y/o contraseña. Comprueba tus credenciales"
            else:
                logger.info("pelisalacarta.channels.footballia Login correcto")
                return True, ""
        except:
            return False, "Error durante el login. Comprueba tus credenciales"

def mainlist(item):
    logger.info("pelisalacarta.channels.footballia mainlist")
    itemlist = []

    log_result, message = login()
    if not log_result:
        itemlist.append(Item(channel=__channel__, title=bbcode_kodi2html("[COLOR darkorange]"+message+"[/COLOR]"), url="", action="auth", thumbnail=item.thumbnail, fanart=item.fanart, folder=False))

    itemlist.append(Item(channel=__channel__, title="Novedades", url="http://footballia.net/es", action="novedades", thumbnail=item.thumbnail, fanart=item.fanart))
    itemlist.append(Item(channel=__channel__, title="Más Votados", url="http://footballia.net/es", action="novedades", thumbnail=item.thumbnail, fanart=item.fanart))
    itemlist.append(Item(channel=__channel__, title="Competiciones", url="http://footballia.net/es", action="competiciones", thumbnail=item.thumbnail, fanart=item.fanart))
    itemlist.append(Item(channel=__channel__, title="Colecciones Especiales", url="http://footballia.net/es", action="colecciones", thumbnail=item.thumbnail, fanart=item.fanart))
    itemlist.append(Item(channel=__channel__, title="Búsqueda por equipo", action="search", extra="equipo", thumbnail=item.thumbnail, fanart=item.fanart))
    itemlist.append(Item(channel=__channel__, title="Búsqueda por jugador/entrenador", action="search", extra="jugador", thumbnail=item.thumbnail, fanart=item.fanart))

    return itemlist

def search(item,texto):
    logger.info("pelisalacarta.channels.footballia search")
    itemlist = []

    if item.extra == "jugador":
        item.url = "http://footballia.net/es/busqueda-por-jugador?utf8=%E2%9C%93&player_name="+texto+"&player_id=&url_base=%2Fes%2Fjugadores%2F"
        return busqueda(item)
    elif item.extra == "equipo":
        item.url = "http://footballia.net/es/busqueda-por-equipo?utf8=%E2%9C%93&team_name="+texto+"&team_id=&url_base=%2Fes%2Fequipos%2F"
        return busqueda(item)


def novedades(item):
    logger.info("pelisalacarta.channels.footballia novedades")
    itemlist = []
    data = scrapertools.cachePage(item.url)
    data = data.replace("\n","").replace("\t","")

    if item.title == "Novedades":
        bloque = scrapertools.find_single_match(data, '<div class="last_matches section-title">(.*?)<h2>')
        first_match = scrapertools.find_single_match(data, '<h2>Últimos partidos añadidos</h2>.*?<a href="(.*?)">(.*?)</a>.*?image: "([^"]+)"')
        if first_match != "":
            scrapedtitle = scrapertools.decodeHtmlentities(first_match[1]).replace("<br />", " (")+")"
            scrapedtitle = "[COLOR gold] "+scrapedtitle.rsplit("(",1)[0]+"[/COLOR][COLOR brown]("+scrapedtitle.rsplit("(",1)[1]+"[/COLOR]"
            itemlist.append(Item(channel=__channel__, title=scrapedtitle, action="findvideos", url=host_footballia+first_match[0], thumbnail=host_footballia+first_match[2], folder=True))
    else:
        bloque = scrapertools.find_single_match(data, '<h2>Partidos más votados(.*?)<h2>')

    patron = '<a href="([^"]+)".*?title="([^"]+)".*?src="([^"]+)".*?'
    patron += '<div class="(?:competition text-center">|m-t-xs competition">)(.*?)</div>'
    matches = scrapertools.find_multiple_matches(bloque, patron)
    for scrapedurl, scrapedtitle, scrapedthumbnail, competition in matches:
        scrapedtitle = " [COLOR gold]"+scrapertools.decodeHtmlentities(scrapedtitle)+"[/COLOR]"
        scrapedtitle += " [COLOR brown]("+scrapertools.decodeHtmlentities(competition)+")[/COLOR]"
        scrapedthumbnail = scrapedthumbnail.replace("mini_","")
        itemlist.append(Item(channel=__channel__, title=bbcode_kodi2html(scrapedtitle), action="findvideos", url=host_footballia+scrapedurl, thumbnail=host_footballia+scrapedthumbnail, folder=True))

    return itemlist

def colecciones(item):
    logger.info("pelisalacarta.channels.footballia colecciones")
    itemlist = []
    data = scrapertools.cachePage(item.url)
    data = data.replace("\n","").replace("\t","")

    bloque = scrapertools.find_single_match(data, '<h2>Nuestras colecciones especiales</h2>(.*?)<script')
    patron = '<a href="([^"]+)".*?title="([^"]+)".*?(?:src="([^"]+)"|</a>)'
    matches = scrapertools.find_multiple_matches(bloque, patron)
    for scrapedurl, scrapedtitle, scrapedthumbnail in matches:
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        if scrapedthumbnail == "": scrapedthumbnail = item.thumbnail
        else: scrapedthumbnail = host_footballia + scrapedthumbnail
        itemlist.append(Item(channel=__channel__, title=scrapedtitle, action="menu_partidos", url=host_footballia+scrapedurl, thumbnail=scrapedthumbnail, folder=True))

    return itemlist

def menu_partidos(item):
    logger.info("pelisalacarta.channels.footballia menu_partidos")
    itemlist = []
    data = scrapertools.cachePage(item.url)
    data = data.replace("\n","").replace("\t","")

    jugador = scrapertools.find_single_match(data, 'href="#matches_as_player">(.*?)</a>')
    if jugador != "": itemlist.append(Item(channel=__channel__, title=jugador, action="partidos", url=item.url, thumbnail=item.thumbnail, folder=True))
    entrenador = scrapertools.find_single_match(data, 'href="#matches_as_coach">(.*?)</a>')
    if entrenador != "": itemlist.append(Item(channel=__channel__, title=entrenador, action="partidos", url=item.url, thumbnail=item.thumbnail, folder=True))

    if len(itemlist) < 2:
        itemlist += partidos(item)

    return itemlist

def partidos(item):
    logger.info("pelisalacarta.channels.footballia partidos")
    itemlist = []
    data = scrapertools.cachePage(item.url)
    data = data.replace("\n","").replace("\t","")

    if "Jugador" in item.title:
        bloque = scrapertools.find_single_match(data, 'id="matches_as_player">(.*?)</table>')
    elif "Entrenador" in item.title:
        bloque = scrapertools.find_single_match(data, 'id="matches_as_coach">(.*?)</table>')
    else:
        bloque = scrapertools.find_single_match(data, '<div class="search-results">(.*?)<footer')

    patron = '<td class="match">.*?href="([^"]+)".*?<span itemprop="name">(.*?)</span>' \
             '.*?<span itemprop="name">(.*?)</span>.*?' \
             '<td class="competition hidden-xs">(.*?)</td>' \
             '<td class="season">(.*?)</td>' \
             '<td class="language hidden-xs">(.*?)</td>'
    matches = scrapertools.find_multiple_matches(bloque, patron)
    for scrapedurl, team1, team2, competition, season, lang in matches:
        team1 = scrapertools.decodeHtmlentities(team1)
        team2 = scrapertools.decodeHtmlentities(team2)
        competition = " [COLOR brown]("+scrapertools.decodeHtmlentities(competition)+"/"+season+")[/COLOR] "
        scrapedtitle = "[COLOR orange]"+team1+"-"+team2+competition+"[COLOR green]["+lang+"][/COLOR]"
        scrapedthumbnail = host_footballia+scrapedurl+"/preview_image"
        itemlist.append(Item(channel=__channel__, title=bbcode_kodi2html(scrapedtitle), action="findvideos", url=host_footballia+scrapedurl, thumbnail=scrapedthumbnail, folder=True))

    next_page = scrapertools.find_single_match(data, '<a rel="next" href="([^"]+)"')
    if next_page != "":
        itemlist.append(Item(channel=__channel__, title=">> Siguiente", action="partidos", url=host_footballia+next_page, thumbnail=item.thumbnail, folder=True))

    return itemlist

def competiciones(item):
    logger.info("pelisalacarta.channels.footballia competiciones")
    itemlist = []
    data = scrapertools.cachePage(item.url)
    data = data.replace("\n","").replace("\t","")

    bloque = scrapertools.find_single_match(data, '(<div class="mega-menu dropdown-menu browse_competitions">.*?</nav>)')
    # Primer menú
    if item.title == "Competiciones":
        patron = '<h5>(.*?)</h5>'
        matches = scrapertools.find_multiple_matches(bloque, patron)
        for scrapedtitle in matches:
            itemlist.append(Item(channel=__channel__, title=scrapedtitle, action="competiciones", url=item.url, thumbnail=item.thumbnail, extra="indice", folder=True))
    # Segundo menú
    elif item.extra == "indice":
        bloque2 = scrapertools.find_single_match(bloque, '(<h5>'+item.title+'</h5>.*?)(?:<h5>|</nav>)')
        if item.title == "Internacionales":
            patron = '<h5>(.*?)</h5>(.*?)<h5>'
        elif item.title == "Otras":
            patron = '<h5>(.*?)</h5>(.*?)</ul>'
        else:
            patron = '>([^<]+)<ul class="links">(.*?)</ul'
        matches = scrapertools.find_multiple_matches(bloque2, patron)
        if len(matches) > 0:
            for scrapedtitle, match in matches:
                scrapedtitle = "[COLOR gold]***"+scrapedtitle+"***[/COLOR]"
                itemlist.append(Item(channel=__channel__, title=bbcode_kodi2html(scrapedtitle), action="", url="", thumbnail=item.thumbnail, folder=True))
                entradas = scrapertools.find_multiple_matches(match, '<a href="([^"]+)">(.*?)</a>')
                for url, title in entradas:
                    title = scrapertools.htmlclean(title)
                    itemlist.append(Item(channel=__channel__, title=title, action="partidos", url=host_footballia+url, thumbnail=item.thumbnail, folder=True))
        else:
            patron = '<a>(.*?)</a>'
            matches = scrapertools.find_multiple_matches(bloque2, patron)
            for scrapedtitle in matches:
                itemlist.append(Item(channel=__channel__, title=scrapedtitle, action="competiciones", url=item.url, thumbnail=item.thumbnail, extra="indice2", folder=True))
    # Tercer menú
    elif item.extra == "indice2":
        bloque2 = scrapertools.find_single_match(data, '<a>'+item.title+'</a>(.*?)<li data-keep-open="true">')
        patron = '<a href="([^"]+)">(.*?)</a>'
        matches = scrapertools.find_multiple_matches(bloque2, patron)
        for scrapedurl, scrapedtitle in matches:
            scrapedtitle = scrapertools.htmlclean(scrapedtitle)
            itemlist.append(Item(channel=__channel__, title=scrapedtitle, action="partidos", url=host_footballia+scrapedurl, thumbnail=item.thumbnail, folder=True))

    return itemlist

def findvideos(item):
    logger.info("pelisalacarta.channels.footballia findvideos")
    itemlist = []
    data = scrapertools.cachePage(item.url)

    if "Este partido no está disponible temporalmente por motivos legales" in data:
        itemlist.append(Item(channel=__channel__, title="[COLOR red]Este partido no está disponible temporalmente[/COLOR]", action="", thumbnail=item.thumbnail, folder=False))
        return itemlist

    urls = scrapertools.find_multiple_matches(data, 'file(?:"\s*|\'\s*|\s*):(?:\s*"|\s*\')([^"\']+)')
    if len(urls) == 1:
        title = "[COLOR olive]Partido Completo  [/COLOR]"+item.title
        itemlist.append(Item(channel=__channel__, title=title, action="play", server="directo", url=urls[0], thumbnail=item.thumbnail, folder=False))
    else:
        for i, scrapedurl in enumerate(urls):
            title = "[COLOR olive]Parte "+str(i+1)+"  [/COLOR]"+item.title
            itemlist.append(Item(channel=__channel__, title=title, action="play", server="directo", url=scrapedurl, thumbnail=item.thumbnail, folder=False))
    return itemlist

def busqueda(item):
    logger.info("pelisalacarta.channels.footballia busqueda")
    itemlist = []
    data = scrapertools.cachePage(item.url)
    data = data.replace("\n","").replace("\t","")

    bloque = scrapertools.find_single_match(data, '<div class="search-results">(.*?)<footer')
    matches = scrapertools.find_multiple_matches(bloque, '<a href="([^"]+)" title="([^"]+)">.*?(?:<td class="full_name">(.*?)</td>|</tr>)')
    for scrapedurl, scrapedtitle, name in matches:
        if name != "": scrapedtitle += "   [COLOR gold]["+name+"][/COLOR]"
        itemlist.append(Item(channel=__channel__, title=bbcode_kodi2html(scrapedtitle), action="menu_partidos", url=host_footballia+scrapedurl, thumbnail=item.thumbnail, folder=True))

    return itemlist

def bbcode_kodi2html(text):
    if config.get_platform().startswith("plex") or config.get_platform().startswith("mediaserver"):
        import re
        text = re.sub(r'\[COLOR\s([^\]]+)\]',
                      r'<span style="color: \1">',
                      text)
        text = text.replace('[/COLOR]','</span>')
        text = text.replace('[CR]','<br>')
        text = re.sub(r'\[([^\]]+)\]',
                      r'<\1>',
                      text)
        text = text.replace('"color: white"','"color: auto"')

    return text

def auth(item):
    import xbmc
    message = ""
    if os.path.exists(footballia_log):
        fichero = open(footballia_log, "r")
        user = fichero.readline().strip()
        password = fichero.readline()
        fichero.close()
        message = user+","+password

    text = dialog_input(default=message, heading="Introduce tu usuario y contraseña separados por una coma")
    if text != "":
        try:
            if not "," in text:
                dialog_notification("Error", "Usuario y contraseña no válidos")
                return
            user = text.split(",")[0]+"\n"
            password = text.split(",")[1]
            fichero = open(footballia_log,"w")
            fichero.write(user+password)
            fichero.close()
            dialog_notification("Éxito", "Usuario y contraseña guardados")
            xbmc.executebuiltin("Container.Refresh")
        except:
            dialog_notification("ERROR al crear el archivo:", footballia_log, time=18000)
            pass

def dialog_input(default="", heading="", hidden=False):
    import xbmc
    keyboard = xbmc.Keyboard(default, heading, hidden)
    keyboard.doModal()
    if (keyboard.isConfirmed()):
        return keyboard.getText()
    else:
        return ""

def dialog_notification(heading, message, icon=0, time=5000, sound=True):
    import xbmcgui
    dialog = xbmcgui.Dialog()
    l_icono=(xbmcgui.NOTIFICATION_INFO , xbmcgui.NOTIFICATION_WARNING, xbmcgui.NOTIFICATION_ERROR)
    dialog.notification (heading, message, l_icono[icon], time, sound)
