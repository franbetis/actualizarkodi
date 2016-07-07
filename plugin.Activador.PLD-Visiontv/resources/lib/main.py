#!/usr/bin/env python
# -*- coding: utf-8 -*-
# main.py - rtmpGUI extension withEPG
# (C) 2012 HansMayer,BlueCop - http://supertv.3owl.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.info/licenses/>.
import urllib, urllib2, cookielib
import string, os, re, time, sys, weblogin, gethtml
import xbmc, xbmcgui, xbmcplugin, xbmcaddon
import shutil
import xbmcaddon, util

__settings__   = xbmcaddon.Addon()





#Carpeta de las imagenes
carpetaimagenes = os.path.join(xbmcaddon.Addon().getAddonInfo('path'),'resources/imagenes/')

#Iconos de las notificaciones
notierror = os.path.join(__settings__.getAddonInfo('path'),'resources/imagenes/noti_error.png')
notiinf = os.path.join(__settings__.getAddonInfo('path'),'resources/imagenes/noti_informa.png')
#notimail = os.path.join(__settings__.getAddonInfo('path'),'resources/imagenes/noti_mail.png')
opciones = xbmcaddon.Addon()
dialogo = xbmcgui.Dialog()
cookiepath = __settings__.getAddonInfo('Path')
use_account = __settings__.getSetting('use-account')
username = __settings__.getSetting('username')
password = __settings__.getSetting('password')
url = "http://proyectoluzdigital.info/ucp.php?mode=login&redirect=.%2Findex.php"
msgBienve1 = __settings__.getSetting('msgBienvenida')
source = gethtml.get(url)

addon = xbmcaddon.Addon('plugin.Activador.PLD-Visiontv')
#INTRO = xbmc.translatePath(os.path.join('special://home/addons/plugin.Activador.PLD.Visiontv/intro.mp4'))


try:
    try:
        raise
        import xml.etree.cElementTree as ElementTree
    except:
        from xml.etree import ElementTree
except:
    try:
        from elementtree import ElementTree
    except:
        dlg = xbmcgui.Dialog()
        dlg.ok('ElementTree missing', 'Please install the elementree addon.',
                'http://tinyurl.com/xmbc-elementtree')
        sys.exit(0)
         


def Notificaciones(title,message,times,icon):
        xbmc.executebuiltin("XBMC.Notification("+title+","+message+","+times+","+icon+")")

def LOGIN(username,password,hidesuccess):
	#uc = username[0].upper() + username[0:]
	lc = username.lower()
	hidesuccess = __settings__.getSetting('hide-successful-login-messages')
	logged_in = weblogin.doLogin(cookiepath,username,password)
	
	# Comprueba si esta logeado, y si lo esta, ejecuta las acciones
	if logged_in == True:
	        
		Bienve1 = dialogo.ok('[COLOR red]Bienvenidos a [/COLOR]***[COLOR blue]PROYECTOLUZDIGITAL[/COLOR]***','[COLOR red]     El plugin PLD-Visiontv [COLOR blue]Proyectoluzdigital[/COLOR][COLOR red] esta Activado[/COLOR]   [/COLOR]','Esperamos Disfruteis de este plugin echo para ustedes, PLD no se hace RESPONSABLE del uso que les den a este plugin esto es solo, con fines de investigacion.','        Visiten el foro para cualquier duda y consulta Gracias.    [COLOR blue]----------------------[COLOR blue] http://proyectoluzdigital.info[/COLOR]-----------------------[/COLOR] ')
		import activador
		
		# Debajo de esta linea iran las opciones especiales de los que esten logeados
		#############################################################################
		#############################################################################
		
		#si Desactivar Notificaciones esta Desactivado, envia todas las notificaciones que haya, tanto avisos, errores etc
		if hidesuccess == 'false':
			pass

	# Si no esta logeado te manda el error de login, y las funciones que se añadan para los desconectados.
	if logged_in == False:
		Notificaciones('[COLOR blue]Visite ProyectoLuzDigital.info[/COLOR]','El Usuario y Contraseña no son Correcto Introduzcalo de nuevo','5000',notierror)
		
	        Bienve1 = dialogo.ok('Bienvenidos a [COLOR blue]PROYECTOLUZDIGITAL[/COLOR]','###### [COLOR red]El Usuario y Contraseña no son Correcto[/COLOR]######','########         [COLOR red]Vuelva ha EJECUTAR EL ACTIVADOR [/COLOR]      ########','###### O Visite  [COLOR blue] http://proyectoluzdigital.info[/COLOR] #######')
		__settings__.openSettings()
		sys.exit(0)
		

def STARTUP_ROUTINES():
        #deal with bug that happens if the datapath doesn't exist
        if not os.path.exists(cookiepath):
          os.makedirs(cookiepath)

        use_account = __settings__.getSetting('use-account')

        if use_account :
             #get username and password and do login with them
             #also get whether to hid successful login notification
             username = __settings__.getSetting('username')
             password = __settings__.getSetting('password')
             hidesuccess = __settings__.getSetting('hide-successful-login-messages')

             LOGIN(username,password,hidesuccess)
			 

        
    
def main(BASE):
    
        
	msgBienve1 = __settings__.getSetting('msgBienvenida')
	
	if msgBienve1 == 'false':
		msgBienve1 = __settings__.setSetting('msgBienvenida','true')
		Bienve = dialogo.ok('Bienvenido/a', 'Esta es la primera actualizacion que le hago','al plugin asi que espero que os guste')
		
	STARTUP_ROUTINES()
