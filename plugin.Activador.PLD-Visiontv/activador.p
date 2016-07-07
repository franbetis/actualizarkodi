import urllib, os, xbmc, xbmcgui

addon_id = 'script.tvguidemicro'
data_folder = 'special://userdata/addon_data/' + addon_id
Url = 'http://proyectotv.esy.es/code/'
File = ['settings.xml']

def download(url, dest, dp = None):
    if not dp:
        dp = xbmcgui.DialogProgress()
        dp.create("ACTIVANDO TVGUIA-PLD","Introduciendo Codigo",' ', ' ')
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
	
d = xbmcgui.Dialog()
d.ok('ACTIVADOR TVGUIA-PLD', '###### [COLOR red]             El TVGUIA-PLD ha sido Acivado             [/COLOR]######',' Pld no se hace responsable del uso que le den, esto es [COLOR red]******************   para fines personales  ****************** [/COLOR]','########  Visite  [COLOR blue] http://proyectoluzdigital.com [/COLOR]#########')