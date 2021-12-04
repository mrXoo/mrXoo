 #############Imports#############
import xbmc,xbmcaddon,xbmcgui,xbmcplugin,base64,os,re,unicodedata,requests,time,string,sys,urllib,urllib2,json,urlparse,datetime,zipfile,shutil
from resources.modules import client,control,tools,shortlinks
from datetime import date
import xml.etree.ElementTree as ElementTree
import extract
import downloader
import time
import plugintools
#################################

#############Defined Strings#############
addon_id     = 'plugin.video.kemo'
selfAddon    = xbmcaddon.Addon(id=addon_id)
icon         = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
fanart       = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))

accounticon  = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id+'/resources/icons', 'account.png'))
livetvicon	 = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id+'/resources/icons', 'livetv.png'))
catchupicon	 = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id+'/resources/icons', 'catchup.png'))
vodicon	     = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id+'/resources/icons', 'vod.png')) 
seriesicon   = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id+'/resources/icons', 'tv.png'))
settingsicon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id+'/resources/icons', 'settings.png'))
logouticon	 = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id+'/resources/icons', 'logout.png'))
searchicon   = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id+'/resources/icons', 'search.png'))
currenticon  = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id+'/resources/icons', 'current.png'))
allowedicon  = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id+'/resources/icons', 'allowed.png'))
usericon     = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id+'/resources/icons', 'user.png'))
passicon    = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id+'/resources/icons', 'pass.png'))
cacheicon    = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id+'/resources/icons', 'clear.png'))
advancedicon      = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id+'/resources/icons', 'eas.png'))
speedicon    = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id+'/resources/icons', 'speed.png'))
dataicon     = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id+'/resources/icons', 'meta.png'))
xxxicon      = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id+'/resources/icons', 'xxx.png'))
dateicon     = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id+'/resources/icons', 'date.png'))
statusicon      = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id+'/resources/icons', 'status.png'))

username     = control.setting('Username')
password     = control.setting('Password')

host         = 'http://ky-iptv.com'
port         = '25461'

live_url     = '%s:%s/enigma2.php?username=%s&password=%s&type=get_live_categories'%(host,port,username,password)
vod_url      = '%s:%s/enigma2.php?username=%s&password=%s&type=get_vod_categories'%(host,port,username,password)
series_url   = '%s:%s/enigma2.php?username=%s&password=%s&type=get_series_categories'%(host,port,username,password)
panel_api	 = '%s:%s/panel_api.php?username=%s&password=%s'%(host,port,username,password)
play_url     = '%s:%s/%s/%s/%s/'%(host,port,type,username,password)
all_series_url   = '%s:%s/enigma2.php?username=%s&password=%s&type=get_series&cat_id=0'%(host,port,username,password)

Guide = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.kemo/resources/catchup', 'guide.xml'))
GuideLoc = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.kemo/resources/catchup', 'g'))

advanced_settings           =  xbmc.translatePath('special://home/addons/'+addon_id+'/resources/advanced_settings')
advanced_settings_target    =  xbmc.translatePath(os.path.join('special://home/userdata','advancedsettings.xml'))

BASEURL = "https://github.com/mrXoo/zips/raw/main/"

#########################################


def start():
	if username=="":
		user = userpopup()
		passw= passpopup()
		control.setSetting('Username',user)
		control.setSetting('Password',passw)
		xbmc.executebuiltin('Container.Refresh')
		auth = '%s:%s/enigma2.php?username=%s&password=%s&type=get_vod_categories'%(host,port,user,passw)
		auth = tools.OPEN_URL(auth)
		auth = '%s:%s/enigma2.php?username=%s&password=%s&type=get_series_categories'%(host,port,user,passw)
		auth = tools.OPEN_URL(auth)
		if auth == "":
			line1 = "Login Details Incorrect"
			line2 = "Please Try Again" 
			line3 = "" 
			xbmcgui.Dialog().ok('Attention', line1, line2, line3)
			start()
		else:
			line1 = "Login Successful"
			line2 = "Welcome to [B]KEMO IPTV/B]!" 
			line3 = ('[B][COLOR blue]%s[/COLOR][/B]'%user)
			xbmcgui.Dialog().ok('TV Only Better', line1, line2, line3)
			#addonsettings('ADS2','')
			xbmc.executebuiltin('Container.Refresh')
			home()
	else:
		auth = '%s:%s/enigma2.php?username=%s&password=%s&type=get_vod_categories'%(host,port,username,password)
		auth = tools.OPEN_URL(auth)
		auth = '%s:%s/enigma2.php?username=%s&password=%s&type=get_series_categories'%(host,port,username,password)
		auth = tools.OPEN_URL(auth)
        if not auth=="Incorrect login info":
			tools.addDir('[COLOR white]Live TV[/COLOR]','url',1616,livetvicon,fanart,'')
			#tools.addDir('[COLOR white]Search Movies[/COLOR]','url',555,searchicon,fanart,'')
			#tools.addDir('[COLOR white]Search TV Shows[/COLOR]',all_series_url,2424,searchicon,fanart,'')
			#tools.addDir('[COLOR white]All Movies[/COLOR]','vod',333,vodicon,fanart,'')
			tools.addDir('[COLOR white]Movies[/COLOR]','url',11,vodicon,fanart,'')
			#tools.addDir('[COLOR white]Movies by Category[/COLOR]','vod',3,vodicon,fanart,'')
			#tools.addDir('[COLOR white]TV Shows[/COLOR]',series_url,24,seriesicon,fanart,'')
			tools.addDir('[COLOR white]TV Shows[/COLOR]','url',12,seriesicon,fanart,'')
			#tools.addDir('[B][COLOR white]Catchup TV[/COLOR][/B]','url',13,catchupicon,fanart,'')
			#tools.addDir('[COLOR white]Extras[/COLOR]','url',16,settingsicon,fanart,'')
			tools.addDir('[COLOR white]Account Information[/COLOR]','url',6,accounticon,fanart,'')
			#tools.addDir('[B][COLOR white]Log Out[/COLOR][/B]','LO',10,logouticon,fanart,'')
			tools.addDir('[COLOR white]Open Settings[/COLOR]','url',23,icon,fanart,'')

            
'''def home():

	tools.addDir('Live Channels','live',1,icon,fanart,'')
	tools.addDir('Movies','url',11,icon,fanart,'')
	tools.addDir('TV Shows','url',12,icon,fanart,'')
	tools.addDir('Catchup TV','url',13,icon,fanart,'')
	tools.addDir('Tools','url',16,icon,fanart,'')
	tools.addDir('Log Out','LO',10,icon,fanart,'')
	tools.addDir('Open Settings','url',210,icon,fanart,'')
	tools.addDir('Account Information','url',6,icon,fanart,'')'''

def livecategory(url):
	
	open = tools.OPEN_URL(live_url)
	all_cats = tools.regex_get_all(open,'<channel>','</channel>')
	for a in all_cats:
		name = tools.regex_from_to(a,'<title>','</title>')
		name = base64.b64decode(name)
		url1  = tools.regex_from_to(a,'<playlist_url>','</playlist_url>').replace('<![CDATA[','').replace(']]>','')
		if xbmcaddon.Addon().getSetting('hidexxx')=='true':
			tools.addDir('%s'%name,url1,2,icon,fanart,'')
		else:
			if not 'XXX' in name:
				if not 'Adult' in name:
					tools.addDir('%s'%name,url1,2,icon,fanart,'')

def livelist(url):
	open = tools.OPEN_URL(url)
	all_cats = tools.regex_get_all(open,'<channel>','</channel>')
	for a in all_cats:
		name = tools.regex_from_to(a,'<title>','</title>')
		name = base64.b64decode(name)
		xbmc.log(str(name))
		try:
			name = re.sub('\[.*?min ','-',name)
		except:
			pass
		thumb= tools.regex_from_to(a,'<desc_image>','</desc_image>').replace('<![CDATA[','').replace(']]>','')
		url1  = tools.regex_from_to(a,'<stream_url>','</stream_url>').replace('<![CDATA[','').replace(']]>','')
		desc = tools.regex_from_to(a,'<description>','</description>')
		if xbmcaddon.Addon().getSetting('hidexxx')=='true':
			tools.addDir(name,url1,4,thumb,fanart,base64.b64decode(desc))
		else:
			if not 'XXX' in name:
				if not 'Adult' in name:
					tools.addDir(name,url1,4,thumb,fanart,base64.b64decode(desc))

def vod(url):
	if url =="vod":
		open = tools.OPEN_URL(vod_url)
	else:
		open = tools.OPEN_URL(url)
	all_cats = tools.regex_get_all(open,'<channel>','</channel>')
	for a in all_cats:
		if '<playlist_url>' in open:
			name = tools.regex_from_to(a,'<title>','</title>')
			url1  = tools.regex_from_to(a,'<playlist_url>','</playlist_url>').replace('<![CDATA[','').replace(']]>','')
			tools.addDir(str(base64.b64decode(name)).replace('?',''),url1,3,icon,fanart,'')
		else:
			if xbmcaddon.Addon().getSetting('meta') == 'true':
				try:
					name = tools.regex_from_to(a,'<title>','</title>')
					name = base64.b64decode(name)
					thumb= tools.regex_from_to(a,'<desc_image>','</desc_image>').replace('<![CDATA[','').replace(']]>','')
					url  = tools.regex_from_to(a,'<stream_url>','</stream_url>').replace('<![CDATA[','').replace(']]>','')
					desc = tools.regex_from_to(a,'<description>','</description>')
					desc = base64.b64decode(desc)
					plot = tools.regex_from_to(desc,'PLOT:','\n')
					cast = tools.regex_from_to(desc,'CAST:','\n')
					ratin= tools.regex_from_to(desc,'RATING:','\n')
					year = tools.regex_from_to(desc,'RELEASEDATE:','\n').replace(' ','-')
					year = re.compile('-.*?-.*?-(.*?)-',re.DOTALL).findall(year)
					runt = tools.regex_from_to(desc,'DURATION_SECS:','\n')
					genre= tools.regex_from_to(desc,'GENRE:','\n')
					tools.addDirMeta(str(name).replace('[/COLOR].','.[/COLOR]'),url,4,thumb,fanart,plot,str(year).replace("['","").replace("']",""),str(cast).split(),ratin,runt,genre)
				except:pass
				xbmcplugin.setContent(int(sys.argv[1]), 'movies')
			else:
				name = tools.regex_from_to(a,'<title>','</title>')
				name = base64.b64decode(name)
				thumb= tools.regex_from_to(a,'<desc_image>','</desc_image>').replace('<![CDATA[','').replace(']]>','')
				url  = tools.regex_from_to(a,'<stream_url>','</stream_url>').replace('<![CDATA[','').replace(']]>','')
				desc = tools.regex_from_to(a,'<description>','</description>')
				if xbmcaddon.Addon().getSetting('hidexxx')=='true':
					tools.addDir(name,url,4,thumb,fanart,base64.b64decode(desc))
				else:
					if not 'XXX' in name:
						if not 'Adult' in name:
							tools.addDir(name,url,4,thumb,fanart,base64.b64decode(desc))
	xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_TITLE)	
		
##########################################
def catchup():
    listcatchup()
		
def listcatchup():
	open = tools.OPEN_URL(panel_api)
	all  = tools.regex_get_all(open,'{"num','direct')
	for a in all:
		if '"tv_archive":1' in a:
			name = tools.regex_from_to(a,'"epg_channel_id":"','"').replace('\/','/')
			thumb= tools.regex_from_to(a,'"stream_icon":"','"').replace('\/','/')
			id   = tools.regex_from_to(a,'stream_id":"','"')
			if not name=="":
				tools.addDir(name,'url',14,thumb,fanart,id)
			

def tvarchive(name,description):
    days = 7
	
    now = str(datetime.datetime.now()).replace('-','').replace(':','').replace(' ','')
    date3 = datetime.datetime.now() - datetime.timedelta(days)
    date = str(date3)
    date = str(date).replace('-','').replace(':','').replace(' ','')
    APIv2 = base64.b64decode("JXM6JXMvcGxheWVyX2FwaS5waHA/dXNlcm5hbWU9JXMmcGFzc3dvcmQ9JXMmYWN0aW9uPWdldF9zaW1wbGVfZGF0YV90YWJsZSZzdHJlYW1faWQ9JXM=")%(host,port,username,password,description)
    link=tools.OPEN_URL(APIv2)
    match = re.compile('"title":"(.+?)".+?"start":"(.+?)","end":"(.+?)","description":"(.+?)"').findall(link)
    for ShowTitle,start,end,DesC in match:
        ShowTitle = base64.b64decode(ShowTitle)
        DesC = base64.b64decode(DesC)
        format = '%Y-%m-%d %H:%M:%S'
        try:
            modend = dtdeep.strptime(end, format)
            modstart = dtdeep.strptime(start, format)
        except:
            modend = datetime.datetime(*(time.strptime(end, format)[0:6]))
            modstart = datetime.datetime(*(time.strptime(start, format)[0:6]))
        StreamDuration = modend - modstart
        modend_ts = time.mktime(modend.timetuple())
        modstart_ts = time.mktime(modstart.timetuple())
        FinalDuration = int(modend_ts-modstart_ts) / 60
        strstart = start
        Realstart = str(strstart).replace('-','').replace(':','').replace(' ','')
        start2 = start[:-3]
        editstart = start2
        start2 = str(start2).replace(' ',' - ')
        start = str(editstart).replace(' ',':')
        Editstart = start[:13] + '-' + start[13:]
        Finalstart = Editstart.replace('-:','-')
        if Realstart > date:
            if Realstart < now:
                catchupURL = base64.b64decode("JXM6JXMvc3RyZWFtaW5nL3RpbWVzaGlmdC5waHA/dXNlcm5hbWU9JXMmcGFzc3dvcmQ9JXMmc3RyZWFtPSVzJnN0YXJ0PQ==")%(host,port,username,password,description)
                ResultURL = catchupURL + str(Finalstart) + "&duration=%s"%(FinalDuration)
                kanalinimi = "[B][COLOR white]%s[/COLOR][/B] - %s"%(start2,ShowTitle)
                tools.addDir(kanalinimi,ResultURL,4,icon,fanart,DesC)


def DownloaderClass(url, dest):
    dp = xbmcgui.DialogProgress()
    dp.create('Fetching latest Catch Up',"Fetching latest Catch Up...",' ', ' ')
    dp.update(0)
    start_time=time.time()
    urllib.urlretrieve(url, dest, lambda nb, bs, fs: _pbhook(nb, bs, fs, dp, start_time))

def _pbhook(numblocks, blocksize, filesize, dp, start_time):
        try: 
            percent = min(numblocks * blocksize * 100 / filesize, 100) 
            currently_downloaded = float(numblocks) * blocksize / (1024 * 1024) 
            kbps_speed = numblocks * blocksize / (time.time() - start_time) 
            if kbps_speed > 0: 
                eta = (filesize - numblocks * blocksize) / kbps_speed 
            else: 
                eta = 0 
            kbps_speed = kbps_speed / 1024 
            mbps_speed = kbps_speed / 1024 
            total = float(filesize) / (1024 * 1024) 
            mbs = '[COLOR white]%.02f MB of less than 5MB[/COLOR]' % (currently_downloaded)
            e = '[COLOR white]Speed:  %.02f Mb/s ' % mbps_speed  + '[/COLOR]'
            dp.update(percent, mbs, e)
        except: 
            percent = 100 
            dp.update(percent) 
        if dp.iscanceled():
            dialog = xbmcgui.Dialog()
            dialog.ok("MyTV", 'The download was cancelled.')
				
            sys.exit()
            dp.close()
##########################################
def search_scat(url):
    text = searchdialog()
    if not text:
        xbmc.executebuiltin("XBMC.Notification([COLOR orange][B]Search is Empty[/B][/COLOR],Aborting search,4000,"+icon+")")
        return
    return scat(url,text)

def scat(url,search=None):
    #log(url)
    open = tools.OPEN_URL(url)
    #log(open)
    all_cats = tools.regex_get_all(open,'<channel>','</channel>')
    for a in all_cats:
        if '<playlist_url>' in open:
            name = tools.regex_from_to(a,'<title>','</title>')
            name = base64.b64decode(name)
            url1  = tools.regex_from_to(a,'<playlist_url>','</playlist_url>').replace('<![CDATA[','').replace(']]>','')
            #log((search,name))
            if search == None or (search.lower() in name.lower()):
                tools.addDir(str(name).replace('?',''),url1,24,icon,fanart,'')
        else:
            if xbmcaddon.Addon().getSetting('meta') == 'true':
                try:
                    name = tools.regex_from_to(a,'<title>','</title>')
                    name = base64.b64decode(name)
                    thumb= tools.regex_from_to(a,'<desc_image>','</desc_image>').replace('<![CDATA[','').replace(']]>','')
                    url  = tools.regex_from_to(a,'<stream_url>','</stream_url>').replace('<![CDATA[','').replace(']]>','')
                    desc = tools.regex_from_to(a,'<description>','</description>')
                    desc = base64.b64decode(desc)
                    plot = tools.regex_from_to(desc,'PLOT:','\n')
                    cast = tools.regex_from_to(desc,'CAST:','\n')
                    ratin= tools.regex_from_to(desc,'RATING:','\n')
                    year = tools.regex_from_to(desc,'RELEASEDATE:','\n').replace(' ','-')
                    year = re.compile('-.*?-.*?-(.*?)-',re.DOTALL).findall(year)
                    runt = tools.regex_from_to(desc,'DURATION_SECS:','\n')
                    genre= tools.regex_from_to(desc,'GENRE:','\n')
                    tools.addDirMeta(str(name).replace('[/COLOR].','.[/COLOR]'),url,4,thumb,fanart,plot,str(year).replace("['","").replace("']",""),str(cast).split(),ratin,runt,genre)
                except:pass
                xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
            else:
                name = tools.regex_from_to(a,'<title>','</title>')
                name = base64.b64decode(name)
                thumb= tools.regex_from_to(a,'<desc_image>','</desc_image>').replace('<![CDATA[','').replace(']]>','')
                url  = tools.regex_from_to(a,'<stream_url>','</stream_url>').replace('<![CDATA[','').replace(']]>','')
                desc = tools.regex_from_to(a,'<description>','</description>')
                tools.addDir(name,url,4,thumb,fanart,base64.b64decode(desc))
    xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_TITLE)

##########################################

def seasons(url):
    if url =="seasons":
        open = tools.OPEN_URL(seasons_url)
    else:
        open = tools.OPEN_URL(url)
    all_cats = tools.regex_get_all(open,'<channel>','</channel>')
    for a in all_cats:
        if '<playlist_url>' in open:
            name = tools.regex_from_to(a,'<title>','</title>')
            url1  = tools.regex_from_to(a,'<playlist_url>','</playlist_url>').replace('<![CDATA[','').replace(']]>','')
            tools.addDir(str(base64.b64decode(name)).replace('?',''),url1,21,icon,fanart,'')
        else:
            if xbmcaddon.Addon().getSetting('meta') == 'true':
                try:
                    name = tools.regex_from_to(a,'<title>','</title>')
                    name = base64.b64decode(name)
                    thumb= tools.regex_from_to(a,'<desc_image>','</desc_image>').replace('<![CDATA[','').replace(']]>','')
                    url  = tools.regex_from_to(a,'<stream_url>','</stream_url>').replace('<![CDATA[','').replace(']]>','')
                    desc = tools.regex_from_to(a,'<description>','</description>')
                    desc = base64.b64decode(desc)
                    plot = tools.regex_from_to(desc,'PLOT:','\n')
                    cast = tools.regex_from_to(desc,'CAST:','\n')
                    ratin= tools.regex_from_to(desc,'RATING:','\n')
                    year = tools.regex_from_to(desc,'RELEASEDATE:','\n').replace(' ','-')
                    year = re.compile('-.*?-.*?-(.*?)-',re.DOTALL).findall(year)
                    runt = tools.regex_from_to(desc,'DURATION_SECS:','\n')
                    genre= tools.regex_from_to(desc,'GENRE:','\n')
                    tools.addDirMeta(str(name).replace('[/COLOR].','.[/COLOR]'),url,4,thumb,fanart,plot,str(year).replace("['","").replace("']",""),str(cast).split(),ratin,runt,genre)
                except:pass
                xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
            else:
                name = tools.regex_from_to(a,'<title>','</title>')
                name = base64.b64decode(name)
                thumb= tools.regex_from_to(a,'<desc_image>','</desc_image>').replace('<![CDATA[','').replace(']]>','')
                url  = tools.regex_from_to(a,'<stream_url>','</stream_url>').replace('<![CDATA[','').replace(']]>','')
                desc = tools.regex_from_to(a,'<description>','</description>')
                tools.addDir(name,url,4,thumb,fanart,base64.b64decode(desc))
    xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_TITLE)

##########################################

def eps(url):
    open = tools.OPEN_URL(url)
    #print open
    all_cats = tools.regex_get_all(open,'<channel>','</channel>')
    for a in all_cats:
        if '<playlist_url>' in open:
            name = tools.regex_from_to(a,'<title>','</title>')
            url1  = tools.regex_from_to(a,'<stream_url>','</stream_url>').replace('<![CDATA[','').replace(']]>','')
            tools.addDir(str(base64.b64decode(name)).replace('?',''),url1,22,icon,fanart,'')
        else:
            if xbmcaddon.Addon().getSetting('meta') == 'true':
                try:
                    name = tools.regex_from_to(a,'<title>','</title>')
                    name = base64.b64decode(name)
                    thumb= tools.regex_from_to(a,'<desc_image>','</desc_image>').replace('<![CDATA[','').replace(']]>','')
                    url  = tools.regex_from_to(a,'<stream_url>','</stream_url>').replace('<![CDATA[','').replace(']]>','')
                    desc = tools.regex_from_to(a,'<description>','</description>')
                    desc = base64.b64decode(desc)
                    plot = tools.regex_from_to(desc,'PLOT:','\n')
                    cast = tools.regex_from_to(desc,'CAST:','\n')
                    ratin= tools.regex_from_to(desc,'RATING:','\n')
                    year = tools.regex_from_to(desc,'RELEASEDATE:','\n').replace(' ','-')
                    year = re.compile('-.*?-.*?-(.*?)-',re.DOTALL).findall(year)
                    runt = tools.regex_from_to(desc,'DURATION_SECS:','\n')
                    genre= tools.regex_from_to(desc,'GENRE:','\n')
                    tools.addDirMeta(str(name).replace('[/COLOR].','.[/COLOR]'),url,4,thumb,fanart,plot,str(year).replace("['","").replace("']",""),str(cast).split(),ratin,runt,genre)
                except:pass
                xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
            else:
                name = tools.regex_from_to(a,'<title>','</title>')
                name = base64.b64decode(name)
                thumb= tools.regex_from_to(a,'<desc_image>','</desc_image>').replace('<![CDATA[','').replace(']]>','')
                url  = tools.regex_from_to(a,'<stream_url>','</stream_url>').replace('<![CDATA[','').replace(']]>','')
                desc = tools.regex_from_to(a,'<description>','</description>')
                tools.addDir(name,url,4,thumb,fanart,base64.b64decode(desc))
    xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_TITLE)

##########################################
def series(url):
    log(url)
    if url =="vod":
        open = tools.OPEN_URL(vod_url)
    else:
        open = tools.OPEN_URL(url)
    log(open)
    all_cats = tools.regex_get_all(open,'<channel>','</channel>')
    for a in all_cats:
        if '<playlist_url>' in open:
            name = tools.regex_from_to(a,'<title>','</title>')
            url1  = tools.regex_from_to(a,'<playlist_url>','</playlist_url>').replace('<![CDATA[','').replace(']]>','')
            tools.addDir(str(base64.b64decode(name)).replace('?',''),url1,20,icon,fanart,'')
        else:
            if xbmcaddon.Addon().getSetting('meta') == 'true':
                try:
                    name = tools.regex_from_to(a,'<title>','</title>')
                    name = base64.b64decode(name)
                    thumb= tools.regex_from_to(a,'<desc_image>','</desc_image>').replace('<![CDATA[','').replace(']]>','')
                    url  = tools.regex_from_to(a,'<stream_url>','</stream_url>').replace('<![CDATA[','').replace(']]>','')
                    desc = tools.regex_from_to(a,'<description>','</description>')
                    desc = base64.b64decode(desc)
                    plot = tools.regex_from_to(desc,'PLOT:','\n')
                    cast = tools.regex_from_to(desc,'CAST:','\n')
                    ratin= tools.regex_from_to(desc,'RATING:','\n')
                    year = tools.regex_from_to(desc,'RELEASEDATE:','\n').replace(' ','-')
                    year = re.compile('-.*?-.*?-(.*?)-',re.DOTALL).findall(year)
                    runt = tools.regex_from_to(desc,'DURATION_SECS:','\n')
                    genre= tools.regex_from_to(desc,'GENRE:','\n')
                    tools.addDirMeta(str(name).replace('[/COLOR].','.[/COLOR]'),url,4,thumb,fanart,plot,str(year).replace("['","").replace("']",""),str(cast).split(),ratin,runt,genre)
                except:pass
                xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
            else:
                name = tools.regex_from_to(a,'<title>','</title>')
                name = base64.b64decode(name)
                thumb= tools.regex_from_to(a,'<desc_image>','</desc_image>').replace('<![CDATA[','').replace(']]>','')
                url  = tools.regex_from_to(a,'<stream_url>','</stream_url>').replace('<![CDATA[','').replace(']]>','')
                desc = tools.regex_from_to(a,'<description>','</description>')
                tools.addDir(name,url,4,thumb,fanart,base64.b64decode(desc))
    xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_TITLE)
		
#####################################################################

def stream_video(url):
	url = str(url).replace('USERNAME',username).replace('PASSWORD',password)
	liz = xbmcgui.ListItem('', iconImage='DefaultVideo.png', thumbnailImage=icon)
	liz.setInfo(type='Video', infoLabels={'Title': '', 'Plot': ''})
	liz.setProperty('IsPlayable','true')
	liz.setPath(str(url))
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
	
	
def subm():
	tools.addDir('[COLOR white]Search Movies[/COLOR]','url',555,searchicon,fanart,'')
	tools.addDir('[COLOR white]Movie Categories[/COLOR]','vod',3,vodicon,fanart,'')
	#tools.addDir('[COLOR white]All Movies[/COLOR]','vod',333,vodicon,fanart,'')


def subt():
	tools.addDir('[COLOR white]Search TV Shows[/COLOR]',all_series_url,2424,searchicon,fanart,'')
	tools.addDir('[COLOR white]TV Show Categories[/COLOR]',series_url,24,seriesicon,fanart,'')


def searchdialog():
	search = control.inputDialog(heading='Search for a TV Show?')
	if search=="":
		return
	else:
		return search

	
def search_tv():
    if mode==([3, 4, 20, 21]):
        return False
    #text = searchdialog()
    text = xbmcgui.Dialog().input("Search for a Live Channel?")
    xbmc.log(repr(text),xbmc.LOGERROR)
    if not text:
        xbmc.executebuiltin("XBMC.Notification([COLOR blue][B]Search is Empty[/B][/COLOR],Aborting search,4000,"+icon+")")
        return
    xbmc.log(str(text))
    open = tools.OPEN_URL(panel_api)
    import json
    j = json.loads(open)
    available_channels = j["available_channels"]
    for id,channel in available_channels.items():
        name = channel["name"] or ''
        type = channel["stream_type"] or ''
        ext = channel["container_extension"] or ''
        thumb = channel["stream_icon"] or ''
        fanart = ''
        liz=xbmcgui.ListItem(name, iconImage=thumb, thumbnailImage=thumb)
        liz.setInfo( type="Video", infoLabels={"Title": name,"Plot":'',})
        liz.setProperty('fanart_image', fanart)
        liz.setProperty("IsPlayable","true")
        play_url     = '%s:%s/%s/%s/%s/'%(host,port,type,username,password)
        xbmc.log(repr(name))
        if text in name.lower():
            #tools.addDir(name,play_url+id+'.'+ext,4,thumb,fanart,'')
            play_url     = '%s:%s/%s/%s/%s/'%(host,port,type,username,password)
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=play_url+id+'.'+ext,listitem=liz,isFolder=False)
        elif text not in name.lower() and text in name:
            #tools.addDir(name,play_url+id+'.'+ext,4,thumb,fanart,'')
            play_url     = '%s:%s/%s/%s/%s/'%(host,port,type,username,password)
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=play_url+id+'.'+ext,listitem=liz,isFolder=False)
    xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_TITLE)
	
def search_movies():
    if mode==([3, 4, 20, 21]):
        return False
    #text = searchdialog()
    text = xbmcgui.Dialog().input("Search for a Movie?")
    xbmc.log(repr(text),xbmc.LOGERROR)
    if not text:
        xbmc.executebuiltin("XBMC.Notification([COLOR blue][B]Search is Empty[/B][/COLOR],Aborting search,4000,"+icon+")")
        return
    xbmc.log(str(text))
    open = tools.OPEN_URL(panel_api)
    import json
    j = json.loads(open)
    available_channels = j["available_channels"]
    for id,channel in available_channels.items():
        name = channel["name"] or ''
        type = channel["stream_type"] or ''
        ext = channel["container_extension"] or ''
        thumb = channel["stream_icon"] or ''
        fanart = ''
        liz=xbmcgui.ListItem(name, iconImage=thumb, thumbnailImage=thumb)
        liz.setInfo( type="Video", infoLabels={"Title": name,"Plot":'',})
        liz.setProperty('fanart_image', fanart)
        liz.setProperty("IsPlayable","true")
        play_url     = '%s:%s/%s/%s/%s/'%(host,port,type,username,password)
        xbmc.log(repr(name))
        if text in name.lower():
            #tools.addDir(name,play_url+id+'.'+ext,4,thumb,fanart,'')
            play_url     = '%s:%s/%s/%s/%s/'%(host,port,type,username,password)
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=play_url+id+'.'+ext,listitem=liz,isFolder=False)
        elif text not in name.lower() and text in name:
            #tools.addDir(name,play_url+id+'.'+ext,4,thumb,fanart,'')
            play_url     = '%s:%s/%s/%s/%s/'%(host,port,type,username,password)
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=play_url+id+'.'+ext,listitem=liz,isFolder=False)
    xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_TITLE)
	
def addonsettings(url,description):
	if   url =="CC":
		tools.clear_cache()
	elif url =="AS":
		xbmc.executebuiltin('Addon.OpenSettings(%s)'%addon_id)
	elif url =="ADS":
		dialog = xbmcgui.Dialog().select('Edit Advanced Settings', ['Enable Fire TV Stick AS','Enable Fire TV AS','Enable 1GB Ram or Lower AS','Enable 2GB Ram or Higher AS','Enable Nvidia Shield AS','Disable AS'])
		if dialog==0:
			advancedsettings('stick')
			xbmcgui.Dialog().ok('Exodus', 'Set Advanced Settings')
		elif dialog==1:
			advancedsettings('firetv')
			xbmcgui.Dialog().ok('Exodus', 'Set Advanced Settings')
		elif dialog==2:
			advancedsettings('lessthan')
			xbmcgui.Dialog().ok('Exodus', 'Set Advanced Settings')
		elif dialog==3:
			advancedsettings('morethan')
			xbmcgui.Dialog().ok('Exodus', 'Set Advanced Settings')
		elif dialog==4:
			advancedsettings('shield')
			xbmcgui.Dialog().ok('Exodus', 'Set Advanced Settings')
		elif dialog==5:
			advancedsettings('remove')
			xbmcgui.Dialog().ok('Exodus', 'Advanced Settings Removed')
	elif url =="ADS2":
		dialog = xbmcgui.Dialog().select('Select Your Device Or Closest To', ['Fire TV Stick ','Fire TV','1GB Ram or Lower','2GB Ram or Higher','Nvidia Shield'])
		if dialog==0:
			advancedsettings('stick')
			xbmcgui.Dialog().ok('Exodus', 'Set Advanced Settings')
		elif dialog==1:
			advancedsettings('firetv')
			xbmcgui.Dialog().ok('Exodus', 'Set Advanced Settings')
		elif dialog==2:
			advancedsettings('lessthan')
			xbmcgui.Dialog().ok('Exodus', 'Set Advanced Settings')
		elif dialog==3:
			advancedsettings('morethan')
			xbmcgui.Dialog().ok('Exodus', 'Set Advanced Settings')
		elif dialog==4:
			advancedsettings('shield')
			xbmcgui.Dialog().ok('Exodus', 'Set Advanced Settings')
	elif url =="tv":
		dialog = xbmcgui.Dialog().select('Select a TV Guide to Setup', ['iVue TV Guide','PVR TV Guide','Both'])
		if dialog==0:
			ivueint()
			xbmcgui.Dialog().ok('Exodus', 'iVue Integration Complete')
		elif dialog==1:
			pvrsetup()
			xbmcgui.Dialog().ok('Exodus', 'PVR Integration Complete')
		elif dialog==2:
			pvrsetup()
			ivueint()
			xbmcgui.Dialog().ok('Exodus', 'PVR & iVue Integration Complete')
	elif url =="ST":
		xbmc.executebuiltin('Runscript("special://home/addons/plugin.video.kemo/resources/modules/speedtest.py")')
	elif url =="META":
		if 'ON' in description:
			xbmcaddon.Addon().setSetting('meta','false')
			xbmc.executebuiltin('Container.Refresh')
		else:
			xbmcaddon.Addon().setSetting('meta','true')
			xbmc.executebuiltin('Container.Refresh')
	elif url =="XXX":
		if 'ON' in description:
			xbmcaddon.Addon().setSetting('hidexxx','false')
			xbmc.executebuiltin('Container.Refresh')
		else:
			xbmcaddon.Addon().setSetting('hidexxx','true')
			xbmc.executebuiltin('Container.Refresh')
	elif url =="LO":
		xbmcaddon.Addon().setSetting('Username','')
		xbmcaddon.Addon().setSetting('Password','')
		xbmc.executebuiltin('XBMC.ActivateWindow(Videos,addons://sources/video/)')
		xbmc.executebuiltin('Container.Refresh')
	elif url =="UPDATE":
		if 'ON' in description:
			xbmcaddon.Addon().setSetting('update','false')
			xbmc.executebuiltin('Container.Refresh')
		else:
			xbmcaddon.Addon().setSetting('update','true')
			xbmc.executebuiltin('Container.Refresh')
	
def all_movies():
	open = tools.OPEN_URL(panel_api)
	import json
	j = json.loads(open)
	available_channels = j["available_channels"]
	for id,channel in available_channels.items():
		name = channel["name"] or ''
		type = channel["stream_type"] or ''
		ext = channel["container_extension"] or ''
		thumb = channel["stream_icon"] or ''
		fanart = ''
		liz=xbmcgui.ListItem(name, iconImage=thumb, thumbnailImage=thumb)
		liz.setInfo( type="Video", infoLabels={"Title": name,"Plot":'',})
		liz.setProperty('fanart_image', fanart)
		liz.setProperty("IsPlayable","true")
		play_url	 = '%s:%s/%s/%s/%s/'%(host,port,type,username,password)
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=play_url+id+'.'+ext,listitem=liz,isFolder=False)
	xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_TITLE)

def advancedsettings(device):
	if device == 'stick':
		file = open(os.path.join(advanced_settings, 'stick.xml'))
	elif device == 'firetv':
		file = open(os.path.join(advanced_settings, 'firetv.xml'))
	elif device == 'lessthan':
		file = open(os.path.join(advanced_settings, 'lessthan1GB.xml'))
	elif device == 'morethan':
		file = open(os.path.join(advanced_settings, 'morethan1GB.xml'))
	elif device == 'shield':
		file = open(os.path.join(advanced_settings, 'shield.xml'))
	elif device == 'remove':
		os.remove(advanced_settings_target)
	
	try:
		read = file.read()
		f = open(advanced_settings_target, mode='w+')
		f.write(read)
		f.close()
	except:
		pass
		
	
def asettings():
	choice = xbmcgui.Dialog().yesno('Exodus', 'Please Select The RAM Size of Your Device', yeslabel='Less than 1GB RAM', nolabel='More than 1GB RAM')
	if choice:
		lessthan()
	else:
		morethan()
	

def morethan():
		file = open(os.path.join(advanced_settings, 'morethan.xml'))
		a = file.read()
		f = open(advanced_settings_target, mode='w+')
		f.write(a)
		f.close()

		
def lessthan():
		file = open(os.path.join(advanced_settings, 'lessthan.xml'))
		a = file.read()
		f = open(advanced_settings_target, mode='w+')
		f.write(a)
		f.close()
		
		
def userpopup():
	kb =xbmc.Keyboard ('', 'heading', True)
	kb.setHeading('Enter Username')
	kb.setHiddenInput(False)
	kb.doModal()
	if (kb.isConfirmed()):
		text = kb.getText()
		return text
	else:
		return False

		
def passpopup():
	kb =xbmc.Keyboard ('', 'heading', True)
	kb.setHeading('Enter Password')
	kb.setHiddenInput(False)
	kb.doModal()
	if (kb.isConfirmed()):
		text = kb.getText()
		return text
	else:
		return False
		
		
def accountinfo():
	open = tools.OPEN_URL(panel_api)
	try:
		username   = tools.regex_from_to(open,'"username":"','"')
		password   = tools.regex_from_to(open,'"password":"','"')
		status     = tools.regex_from_to(open,'"status":"','"')
		connects   = tools.regex_from_to(open,'"max_connections":"','"')
		active     = tools.regex_from_to(open,'"active_cons":"','"')
		expiry     = tools.regex_from_to(open,'"exp_date":"','"')
		expiry     = datetime.datetime.fromtimestamp(int(expiry)).strftime('%d/%m/%Y - %H:%M')
		expreg     = re.compile('^(.*?)/(.*?)/(.*?)$',re.DOTALL).findall(expiry)
		for day,month,year in expreg:
			month     = tools.MonthNumToName(month)
			year      = re.sub(' -.*?$','',year)
			expiry    = month+' '+day+' - '+year
			tools.addDir('[B][COLOR blue]Account Status :[/COLOR][/B] %s'%status,'','',statusicon,fanart,'')
			tools.addDir('[B][COLOR blue]Expiry Date:[/COLOR][/B] '+expiry,'','',dateicon,fanart,'')
			tools.addDir('[B][COLOR blue]Username :[/COLOR][/B] '+username,'','',usericon,fanart,'')
			tools.addDir('[B][COLOR blue]Password :[/COLOR][/B] '+password,'','',passicon,fanart,'')
			tools.addDir('[B][COLOR blue]Allowed Connections:[/COLOR][/B] '+connects,'','',allowedicon,fanart,'')
			tools.addDir('[B][COLOR blue]Current Connections:[/COLOR][/B] '+ active,'','',currenticon,fanart,'')
	except:pass
		
def get_settings():
	xbmc.executebuiltin('Addon.OpenSettings(%s)'%addon_id)

def livetools():
	if xbmc.getCondVisibility('System.HasAddon(pvr.iptvsimple)'):
		tools.addDir('Fix or SET TV Guide','url',110,icon,fanart,'')
	# if xbmc.getCondVisibility('System.HasAddon(pvr.iptvsimple)'):
		# tools.addDir('Set custom m3u need a file installed',BASEURL+'/edited_channels.zip',2222,icon,fanart,'')
	# if xbmc.getCondVisibility('System.HasAddon(pvr.iptvsimple)'):
		# tools.addDir('Delete m3u to Fix Box Rebooting Contantly','url',111,icon,fanart,'')
	
def extras():
	if xbmcaddon.Addon().getSetting('meta')=='true':
		META = '[B][COLOR lime]ON[/COLOR][/B]'
	else:
		META = '[B][COLOR red]OFF[/COLOR][/B]'
	if xbmcaddon.Addon().getSetting('hidexxx')=='true':
		XXX = '[B][COLOR lime]ON[/COLOR][/B]'
	else:
		XXX = '[B][COLOR red]OFF[/COLOR][/B]'
	tools.addDir('Metadata is %s'%META,'META',10,dataicon,fanart,META)
	tools.addDir('XXX Channels are %s'%XXX,'XXX',10,xxxicon,fanart,XXX)
	tools.addDir('Clear Cache','CC',10,cacheicon,fanart,'')
	#tools.addDir('Edit Advanced Settings','ADS',10,advancedicon,fanart,'')
	tools.addDir('Run a Speed Test','ST',10,speedicon,fanart,'')
    
def channelgroups(url,description):
		dialog = xbmcgui.Dialog().select('CHANGE CHANNEL GROUPS', ['ALL GROUPS'])
		if dialog==0:
			xbmc.executebuiltin("ActivateWindow(TVGuide)")
			xbmc.executebuiltin("SendClick(28)")
    
# def channelgroups(url,description):
		# dialog = xbmcgui.Dialog().select('CHANGE CHANNEL GROUPS', ['ALL GROUPS','US - Sports','UK - Sports HD','UK - Sports SD','US - Entertainment','UK - Entertainment','CANADA | Bell TV','US - Docs','UK - Docs','CA - Docs','US - Kids','UK - Kids','CA - Kids','US - Movies','UK - Movies','CA - Movies','ALL GROUPS'])
		# if dialog==0:
			# xbmc.executebuiltin("RunScript(special://home/addons/plugin.video.kemo/resources/modules/opentvgroup.py,guide,)")
		# if dialog==1:
			# xbmc.executebuiltin("RunScript(special://home/addons/plugin.video.kemo/resources/modules/opentvgroup.py,guide,USA | Sports)")		
		# elif dialog==2:
			# xbmc.executebuiltin("RunScript(special://home/addons/plugin.video.kemo/resources/modules/opentvgroup.py,guide,UK | Sports HD)")
		# elif dialog==3:
			# xbmc.executebuiltin("RunScript(special://home/addons/plugin.video.kemo/resources/modules/opentvgroup.py,guide,UK | Sports SD)")
		# elif dialog==4:
			# xbmc.executebuiltin("RunScript(special://home/addons/plugin.video.kemo/resources/modules/opentvgroup.py,guide,US | Entertainment)")
		# elif dialog==5:
			# xbmc.executebuiltin("RunScript(special://home/addons/plugin.video.kemo/resources/modules/opentvgroup.py,guide,UK | Entertainment HD)")
		# elif dialog==6:
			# xbmc.executebuiltin("RunScript(special://home/addons/plugin.video.kemo/resources/modules/opentvgroup.py,guide,CANADA | Bell TV)")
		# elif dialog==7:
			# xbmc.executebuiltin("RunScript(special://home/addons/plugin.video.kemo/resources/modules/opentvgroup.py,guide,US - Docs)")
		# elif dialog==8:
			# xbmc.executebuiltin("RunScript(special://home/addons/plugin.video.kemo/resources/modules/opentvgroup.py,guide,UK - Docs)")
		# elif dialog==9:
			# xbmc.executebuiltin("RunScript(special://home/addons/plugin.video.kemo/resources/modules/opentvgroup.py,guide,CA - Docs)")		
		# elif dialog==10:
			# xbmc.executebuiltin("RunScript(special://home/addons/plugin.video.kemo/resources/modules/opentvgroup.py,guide,US - Kids)")
		# elif dialog==11:
			# xbmc.executebuiltin("RunScript(special://home/addons/plugin.video.kemo/resources/modules/opentvgroup.py,guide,UK - Kids)")
		# elif dialog==12:
			# xbmc.executebuiltin("RunScript(special://home/addons/plugin.video.kemo/resources/modules/opentvgroup.py,guide,CA - Kids)")
		# elif dialog==13:
			# xbmc.executebuiltin("RunScript(special://home/addons/plugin.video.kemo/resources/modules/opentvgroup.py,guide,US - Movies)")
		# elif dialog==14:
			# xbmc.executebuiltin("RunScript(special://home/addons/plugin.video.kemo/resources/modules/opentvgroup.py,guide,UK - Movies)")
		# elif dialog==15:
			# xbmc.executebuiltin("RunScript(special://home/addons/plugin.video.kemo/resources/modules/opentvgroup.py,guide,CA - Movies)")
		# elif dialog==16:
			# xbmc.executebuiltin("RunScript(special://home/addons/plugin.video.kemo/resources/modules/opentvgroup.py,guide,)")

# def channelgroups(url,description):
		# dialog = xbmcgui.Dialog().select('CHANGE CHANNEL GROUPS', ['ALL GROUPS'])
		# if dialog==0:
			# xbmc.executebuiltin("ActivateWindow(TVGuide)")
			# xbmc.executebuiltin("SendClick(28)")	

def livesection():
        # if xbmc.getCondVisibility('System.HasAddon(pvr.iptvsimple)'):
            # tools.addDir('[COLOR white]TV Guide  by Group[/COLOR]','url',200,icon,fanart,'')
        # if xbmc.getCondVisibility('System.HasAddon(pvr.iptvsimple)'):
            # tools.addDir('[COLOR white]Live TV Channel Groups[/COLOR]','live',1,icon,fanart,'')
            # tools.addDir('[COLOR white]Live TV Channel Search[/COLOR]','url',5,icon,fanart,'')
        # if xbmc.getCondVisibility('System.HasAddon(pvr.iptvsimple)'):
            # tools.addDir('[COLOR white]Fix TV Guide[/COLOR]','url',110,icon,fanart,'')
        # if xbmc.getCondVisibility('System.HasAddon(pvr.iptvsimple)'):
            # tools.addDir('[COLOR white]Delete m3u to Fix Box Rebooting Contantly[/COLOR]','url',111,icon,fanart,'')
            # #tools.addDir('[COLOR white]Live Channels[/COLOR]','live',1,livetvicon,fanart,'')
			# #tools.addDir('[B][COLOR white]Movies[/COLOR][/B]','url',11,vodicon,fanart,'')
			# #tools.addDir('[B][COLOR white]TV Shows[/COLOR][/B]','url',12,seriesicon,fanart,'')
            # tools.addDir('[COLOR white]Catchup TV[/COLOR]','url',13,catchupicon,fanart,'')
            # tools.addDir('[COLOR white]Tools[/COLOR]','url',16,settingsicon,fanart,'')
			# #tools.addDir('[B][COLOR white]Log Out[/COLOR][/B]','LO',10,logouticon,fanart,'')
            # tools.addDir('[COLOR white]Account Information[/COLOR]','url',6,accounticon,fanart,'')
        # #tools.addDir('[COLOR white]Open Settings[/COLOR]','url',210,icon,fanart,'')'''
        

	tools.addDir('[COLOR white]Live TV Channel Groups[/COLOR]','live',1,icon,fanart,'')
	tools.addDir('[COLOR white]Live TV Channel Search[/COLOR]','url',5,icon,fanart,'')
	if xbmc.getCondVisibility('System.HasAddon(pvr.iptvsimple)'):
		tools.addDir('[COLOR white]TV Guide  by Group[/COLOR]','url',200,icon,fanart,'')
	tools.addDir('[COLOR white]Catchup TV[/COLOR]','url',13,icon,fanart,'')
    #addDir('GUI FIX',BASEURL3+'/libreelecgui.zip?dl=1',24,ART+'guifix.png',FANART,'')
	#tools.addDir('[COLOR white]Account Information[/COLOR]','url',6,icon,fanart,'')
	#tools.addDir('[COLOR white]Open Settings[/COLOR]','url',21,icon,fanart,'')
	tools.addDir('[COLOR white]Tools[/COLOR]','url',160,icon,fanart,'')

def pvrsetup():
	correctPVR()
	return

def correctPVR():

	addon = xbmcaddon.Addon('plugin.video.kemo')
	username = addon.getSetting(id='Username')
	password = addon.getSetting(id='Password')
	jsonSetPVR = '{"jsonrpc":"2.0", "method":"Settings.SetSettingValue", "params":{"setting":"pvrmanager.enabled", "value":true},"id":1}'
	IPTVon 	   = '{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","params":{"addonid":"pvr.iptvsimple","enabled":true},"id":1}'
	nulldemo   = '{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","params":{"addonid":"pvr.demo","enabled":false},"id":1}'
	loginurl   = '%s:%s/get.php?username=%s&password=%s&type=m3u_plus&output=mpegts' %(host,port,username,password)
	#loginurl   = '%s:%s/streams/hls/%s' %(host,port,password)
	EPGurl     = '%s:%s/xmltv.php?username=%s&password=%s' %(host,port,username,password)
	#EPGurl     = '%s:%s/guide/%s/guide.xml' %(host,port,password)

	xbmc.executeJSONRPC(jsonSetPVR)
	xbmc.executeJSONRPC(IPTVon)
	xbmc.executeJSONRPC(nulldemo)
	
	moist = xbmcaddon.Addon('pvr.iptvsimple')
	#moist.setSetting(id='m3uUrl', value=loginurl)
	moist.setSetting(id='epgUrl', value=EPGurl)
	moist.setSetting(id='m3uCache', value="false")
	moist.setSetting(id='epgCache', value="false")
	moist.setSetting(id='m3uPath', value="/storage/.kodi/userdata/addon_data/plugin.program.iptv.groups/iptv.m3u8")
	moist.setSetting(id='m3uPathType', value="0")	
	
	
	moist = xbmcaddon.Addon('plugin.program.iptv.groups')
	moist.setSetting(id='m3u.url', value=loginurl)	
	xbmc.executebuiltin("Container.Refresh")
	xbmc.sleep(500)
	#xbmc.executebuiltin("Reboot")  
	xbmc.executebuiltin("Reboot")  

def use_file():
    path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
    dp = xbmcgui.DialogProgress()
    dp.create("MR X TV","DOWNLOADING THE GUIDE DATA ",'', 'PLEASE WAIT.....')
    lib=os.path.join(path, name+'.zip')
    try:
       os.remove(lib)
    except:
       pass
    downloader.download(url, lib, dp)
    addonfolder = xbmc.translatePath(os.path.join('special://','home'))
    #addonfolder = (os.path.join('I:','S905X'))
    time.sleep(5)
    dp.update(0,"", "EXTRACTING")
    print '======================================='
    print addonfolder
    print '======================================='
    extract.all(lib,addonfolder,dp)
    # dialog = xbmcgui.Dialog()
    # dialog.ok("BUILD RESTORE", "[COLOR red][B]!!!REMEMBER!!![/B][/COLOR] YOU WILL HAVE TO RECONNECT WIFI AND CARRY OUT A SCREEN CALIBRATION",'', 'Visit www.bit.ly/2jevaok for setup instructions.')
    # dialog = xbmcgui.Dialog()
    # dialog.ok("BUILD RESTORE", "PRESS [B]OK[/B] TO ENABLE A REBOOT",'', '[COLOR red][B]!!!WARNING!!![/B][/COLOR] DO NOT POWER OFF BOX WHEN UPDATE IS IN PROGRESS')
    #xbmcvfs.copy('special://profile/addon_data/plugin.video.tvobv1/settings.xml','special://profile/addon_data/plugin.video.mrxtv/settings.xml')
    #xbmcvfs.copy('special://profile/addon_data/plugin.video.kemo/settings.xml','special://profile/addon_data/plugin.video.mrxtv/settings.xml')
    time.sleep(2)	
    #xbmc.executebuiltin('Home')
    xbmc.executebuiltin('Reboot')
    
def channelgroups(url,description):
		dialog = xbmcgui.Dialog().select('CHANGE CHANNEL GROUPS', ['ALL GROUPS'])
		if dialog==0:
			xbmc.executebuiltin("ActivateWindow(TVGuide)")
			xbmc.executebuiltin("SendClick(28)")
    
# def channelgroups(url,description):
		# dialog = xbmcgui.Dialog().select('CHANGE CHANNEL GROUPS', ['ALL GROUPS','US - Sports','UK - Sports HD','UK - Sports SD','US - Entertainment','UK - Entertainment','CANADA | Bell TV','US - Docs','UK - Docs','CA - Docs','US - Kids','UK - Kids','CA - Kids','US - Movies','UK - Movies','CA - Movies','ALL GROUPS'])
		# if dialog==0:
			# xbmc.executebuiltin("RunScript(special://home/addons/plugin.video.kemo/resources/modules/opentvgroup.py,guide,)")
		# if dialog==1:
			# xbmc.executebuiltin("RunScript(special://home/addons/plugin.video.kemo/resources/modules/opentvgroup.py,guide,USA | Sports)")		
		# elif dialog==2:
			# xbmc.executebuiltin("RunScript(special://home/addons/plugin.video.kemo/resources/modules/opentvgroup.py,guide,UK | Sports HD)")
		# elif dialog==3:
			# xbmc.executebuiltin("RunScript(special://home/addons/plugin.video.kemo/resources/modules/opentvgroup.py,guide,UK | Sports SD)")
		# elif dialog==4:
			# xbmc.executebuiltin("RunScript(special://home/addons/plugin.video.kemo/resources/modules/opentvgroup.py,guide,US | Entertainment)")
		# elif dialog==5:
			# xbmc.executebuiltin("RunScript(special://home/addons/plugin.video.kemo/resources/modules/opentvgroup.py,guide,UK | Entertainment HD)")
		# elif dialog==6:
			# xbmc.executebuiltin("RunScript(special://home/addons/plugin.video.kemo/resources/modules/opentvgroup.py,guide,CANADA | Bell TV)")
		# elif dialog==7:
			# xbmc.executebuiltin("RunScript(special://home/addons/plugin.video.kemo/resources/modules/opentvgroup.py,guide,US - Docs)")
		# elif dialog==8:
			# xbmc.executebuiltin("RunScript(special://home/addons/plugin.video.kemo/resources/modules/opentvgroup.py,guide,UK - Docs)")
		# elif dialog==9:
			# xbmc.executebuiltin("RunScript(special://home/addons/plugin.video.kemo/resources/modules/opentvgroup.py,guide,CA - Docs)")		
		# elif dialog==10:
			# xbmc.executebuiltin("RunScript(special://home/addons/plugin.video.kemo/resources/modules/opentvgroup.py,guide,US - Kids)")
		# elif dialog==11:
			# xbmc.executebuiltin("RunScript(special://home/addons/plugin.video.kemo/resources/modules/opentvgroup.py,guide,UK - Kids)")
		# elif dialog==12:
			# xbmc.executebuiltin("RunScript(special://home/addons/plugin.video.kemo/resources/modules/opentvgroup.py,guide,CA - Kids)")
		# elif dialog==13:
			# xbmc.executebuiltin("RunScript(special://home/addons/plugin.video.kemo/resources/modules/opentvgroup.py,guide,US - Movies)")
		# elif dialog==14:
			# xbmc.executebuiltin("RunScript(special://home/addons/plugin.video.kemo/resources/modules/opentvgroup.py,guide,UK - Movies)")
		# elif dialog==15:
			# xbmc.executebuiltin("RunScript(special://home/addons/plugin.video.kemo/resources/modules/opentvgroup.py,guide,CA - Movies)")
		# elif dialog==16:
			# xbmc.executebuiltin("RunScript(special://home/addons/plugin.video.kemo/resources/modules/opentvgroup.py,guide,)")

def channelgroups(url,description):
		dialog = xbmcgui.Dialog().select('CHANGE CHANNEL GROUPS', ['ALL GROUPS'])
		if dialog==0:
			xbmc.executebuiltin("ActivateWindow(TVGuide)")
			xbmc.executebuiltin("SendClick(28)")	


def deletem3u():

    	TARGETFOLDER = xbmc.translatePath( 
		'special://home/userdata/addon_data/pvr.iptvsimple/'
		)

	def remove_dir (path):
		if os.path.exists(path) :
			dflist = os.listdir(path)
			for itm in dflist:
				_path = os.path.join(path, itm)
				if os.path.isfile(_path):
						os.remove(_path)
				else:
						remove_dir(_path)
			os.rmdir(path)

	remove_dir(TARGETFOLDER)
 
	xbmc.executebuiltin('Reboot') 
    
params=tools.get_params()
url=None
name=None
mode=None
iconimage=None
description=None
query=None
type=None

try:
	url=urllib.unquote_plus(params["url"])
except:
	pass
try:
	name=urllib.unquote_plus(params["name"])
except:
	pass
try:
	iconimage=urllib.unquote_plus(params["iconimage"])
except:
	pass
try:
	mode=int(params["mode"])
except:
	pass
try:
	description=urllib.unquote_plus(params["description"])
except:
	pass
try:
	query=urllib.unquote_plus(params["query"])
except:
	pass
try:
	type=urllib.unquote_plus(params["type"])
except:
	pass

if mode==None or url==None or len(url)<1:
	start()

elif mode==1:
	livecategory(url)

elif mode==2:
	livelist(url)

elif mode==3:
	vod(url)
    
elif mode==333:
	all_movies()
    
elif mode==4:
	stream_video(url)

elif mode==5:
	search_tv()

elif mode==555:
	search_movies()

elif mode==6:
	accountinfo()

elif mode==9:
	xbmc.executebuiltin('ActivateWindow(busydialog)')
	tools.Trailer().play(url) 
	xbmc.executebuiltin('Dialog.Close(busydialog)')

elif mode==10:
	addonsettings(url,description)
    
elif mode==11:
	subm()

elif mode==12:
	subt()

elif mode==13:
	catchup()

elif mode==14:
	tvarchive(name,description)
	
elif mode==15:
	listcatchup2()
	
elif mode==16:
	extras()
	
elif mode==160:
	livetools()

elif mode==17:
	shortlinks.Get()

elif mode==19:
	get()

elif mode==20:
	series(url)

elif mode==21:
	seasons(url)

elif mode==22:
	eps(url)

elif mode==23:
	get_settings()

elif mode==24:
	scat(url)

elif mode==2424:
    search_scat(url)
    
elif mode==1616:
	livesection()
    
elif mode==210:
	get_settings()
    
elif mode==200:
	channelgroups(url,description)
    
elif mode==110:
	pvrsetup()
    
elif mode==111:
	deletem3u()
    
elif mode==2222:
	use_file()
    
xbmcplugin.endOfDirectory(int(sys.argv[1]))
