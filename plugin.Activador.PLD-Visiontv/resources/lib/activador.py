import urllib, os, xbmc, xbmcgui
import base64
addon_id = 'plugin.Activador.PLD-Visiontv'
data_folder = 'special://home/addons/plugin.video.pld.visiontv/'
Url = base64.b64decode('aHR0cDovL2Nsb3VkLjYxMzkyNTMtMC5hbG9qYW1pZW50by13ZWIuZXMvZG93bmxvYWQvYWN0aXZhZG9yZXMvYWN0aXZpc2lvbi8yMjA1Lw==')
File = ['default.py']

def download(url, dest, dp = None):
    if not dp:
        dp = xbmcgui.DialogProgress()
        dp.create("ACTIVANDO PLD-Visiontv","Introduciendo Codigo",' ', ' ')
    dp.update(0)
    urllib.urlretrieve(url,dest,lambda nb, bs, fs, url=url: _pbhook(nb,bs,fs,url,dp))
 
def _pbhook(numblocks, blocksize, filesize, url, dp):
    try:
        percent = min((numblocks*blocksize*100)/filesize, 100)
        dp.update(percent)
    except:
        percent = 100
        dp.update(percent)
    if dp.iscanceled(): 
        raise Exception("Cancelar")
        dp.close()

for file in File:
	url = Url + file
	fix = xbmc.translatePath(os.path.join( data_folder, file))
	download(url, fix)
	
	import urllib, os, xbmc, xbmcgui
import base64
	
addon_id = 'plugin.video.pld.visiontv'
data_folder = 'special://userdata/addon_data/' + addon_id
Url = base64.b64decode('aHR0cDovL2Nsb3VkLjYxMzkyNTMtMC5hbG9qYW1pZW50by13ZWIuZXMvZG93bmxvYWQvYWN0aXZhZG9yZXMvYWN0aXZpc2lvbi9zZXR0aW5ncy54bWw=')
File = ['settings.xml']

def download(url, dest, dp = None):
    if not dp:
        dp = xbmcgui.DialogProgress()
        dp.create("ACTIVANDO PLD-Visiontv-PLD","Introduciendo Codigo",' ', ' ')
    dp.update(0)
    urllib.urlretrieve(url,dest,lambda nb, bs, fs, url=url: _pbhook(nb,bs,fs,url,dp))
 
def _pbhook(numblocks, blocksize, filesize, url, dp):
    try:
        percent = min((numblocks*blocksize*100)/filesize, 100)
        dp.update(percent)
    except:
        percent = 100
        dp.update(percent)
    if dp.iscanceled(): 
        raise Exception("Cancelar")
        dp.close()

for file in File:
	url = Url + file
	fix = xbmc.translatePath(os.path.join( data_folder, file))
	download(url, fix)

import xbmcaddon, util	
addon = xbmcaddon.Addon('plugin.Activador.PLD-Visiontv')	
	
util.playMedia(addon.getAddonInfo('name'), addon.getAddonInfo('icon'), 
               'special://home/addons/plugin.Activador.PLD-Visiontv/resources/intro.mp4')