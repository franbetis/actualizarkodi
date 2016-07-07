#!/usr/bin/env python
# -*- coding: utf-8 -*-
import shutil
import xbmc, xbmcgui, xbmcplugin, xbmcaddon,os
from resources.lib.main import main


ADDON=xbmcaddon.Addon(id='plugin.Activador.PLD-Visiontv')
INTRO = xbmc.translatePath(os.path.join('special://home/addons/plugin.Activador.PLD-Visiontv/intro.mp4'))

def INTROS():            
    if ADDON.getSetting('intro') == "true":
        xbmcPlayer=xbmc.Player()
        xbmcPlayer.play(INTRO)
        xbmc.sleep(250)
        ADDON.setSetting('intro','true')
    #else:
       # pass
        if ADDON.getSetting('message') == "true":
            #xbmc.sleep(250)
            intro=xbmcgui.Dialog()
            msg = intro.ok("[COLOR orange]Activador.PLD-VISIONTV[/COLOR]", "[COLOR orange]****************[COLOR red]-------NUEVO ACTIVADOR------[COLOR orange]****************[/COLOR]",
                            "*********************[COLOR lime]PLD-VISIONTV[/COLOR]*********************",
                            "*************[COLOR orange]ESPERAMOS QUE LO DISFRUTEIS[/COLOR]*************"
                            )
            if msg == True:
                ADDON.setSetting('message','true')
            else:
                pass
        else:
            pass      
INTROS()

__settings__   = xbmcaddon.Addon()



BASE=[
('https://dl.dropbox.com/s/doa8gt9s0tdo2y7/Espana.xml', 'Respaldo TV España'),
#('http://playstationstorelibre.eshost.es/ps/Series.xml', 'Series España'),
]

#if (__settings__.getSetting("habilitarmodoadultos") == 'true') and (__settings__.getSetting("canalesrumanos") == 'true'): from resources.lib.main import main;main(BASE3)
if (__settings__.getSetting("habilitarmodoadultos") == 'true'): from resources.lib.main import main;main(BASE2)
#if (__settings__.getSetting("canalesrumanos") == 'true'): from resources.lib.main import main;main(BASE1)
else: from resources.lib.main import main;main(BASE)


