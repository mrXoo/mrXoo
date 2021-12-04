# -*- coding: utf-8 -*-
###########################################################################################################################
###########################################################################################################################
### https://github.com/trogggy/trogggy.scripts/blob/master/opentvgroup.py                                               ###
### save this as eg userdata/opentvgroup.py                                                                             ###
### opens specified tv channel or guide groups.                                                                         ###
### start from a shortcut with 1 or 2 arguments                                                                         ###
### argument 1 (optional) - open channels or guide window (default is channels)                                         ###
### argument 2 - name of requested group - if name not found the script will default to 'choose group' screen           ###
### eg to open 'Sport' group guide from skin shortcut or remote:                                                        ###
### RunScript(special://masterprofile/opentvgroup.py,guide,Sport)                                                       ###
### or from favourite:                                                                                                  ###
### <favourite name="Sport Guide">RunScript(special://masterprofile/opentvgroup.py,guide,Sport)</favourite>             ###
### All channels (channel window):                                                                                      ###
### <favourite name="All channels">RunScript(special://masterprofile/opentvgroup.py,channels,All channels)</favourite>  ###
### Most recent channels:                                                                                               ###
### <favourite name="Most recent channels">RunScript(special://masterprofile/opentvgroup.py,channels,last)</favourite>  ###  
###                                                                                                                     ###
###########################################################################################################################
###########################################################################################################################

import xbmc
import sys
import json
			
def getchannelgroups():
    global CHANNELGROUPS, channelgroups, numb
    CHANNELGROUPS = []
    ret = json.loads(xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id": 1, "method": "PVR.GetChannelGroups", "params":{"channeltype":"tv"} }'))
    channelgroups = ret['result']['channelgroups']
    for channelgroup in channelgroups:
#        xbmc.log(channelgroup)
        chanstring = str(channelgroup)
        start = "u'label': u'"
        end = "'}"		
        group = (chanstring.split(start))[1].split(end)[0]
        CHANNELGROUPS.append(group)
    numb = len(CHANNELGROUPS)
    xbmc.log('There are %d channel groups' % numb)
    c = 0
    while c < numb:
        xbmc.log(CHANNELGROUPS[c])
        c = c + 1
	
def setf():
    global a, f
    if a in ["Channels", "channels", "Channel", "channel"]:
        f = 1
        f = int(f)
    elif a in ['Guide', 'guide']:
        f = 2
        f = int(f)
    else:
        f = 1               # ie defaults to channels, this can be changed
        f = int(f)

def setg():
    global b, g, CHANNELGROUPS, channelgroups, numb
    c = 0
    g = 0               # choose - if group doesn't exist it will fall back to this
    while c < numb:
        GRP = CHANNELGROUPS[c]
        if b == CHANNELGROUPS[c]:
            g = c + 1
        c = c + 1
    xbmc.log('Requested group is %s' % b)
        
def opengroups():
    global f, g
# open channel or guide windows
    if f == 1:
	    xbmc.executebuiltin('ActivateWindow(TVChannels)')
    elif f == 2: 
	    xbmc.executebuiltin('ActivateWindow(TVGuide)')
    if b == 'last':
        finish()
    c = 2                                                       # use to count to right group
    xbmc.executebuiltin('SendClick(28)')
    xbmc.executebuiltin( "XBMC.Action(FirstPage)" )
    # loop move down to correct group (if necessary)
    if g > 1:
	    while (c <= g):	
		    c = c + 1
		    xbmc.executebuiltin( "XBMC.Action(Down)" )			
    # open group if not using 'choose' option.		
    if g >= 1:		
	    xbmc.executebuiltin( "XBMC.Action(Select)" )
	    xbmc.executebuiltin( "XBMC.Action(Right)" )
	    xbmc.executebuiltin( "ClearProperty(SideBladeOpen)" )
        
def finish():
    xbmc.log('%s is stopping' % script)
    exit()

################################################################################################################### 
# get going
script = sys.argv[0]
xbmc.log('Running %s' % script)       
# make sure pvr is running - exit script if not
if not xbmc.getCondVisibility('System.HasPVRAddon'):
    xbmc.executebuiltin('Notification(PVR addon, is not enabled)')
    xbmc.log('no pvr addon enabled')
    finish()
# define stuff
if len(sys.argv) > 1:
    a = sys.argv[1]		# channels or guide
    b = sys.argv[2]		# which group - name or 'choose' (if this doesn't match a group it defaults to 'choose')
else:
    a = 'channels'               # default is channels, can be changed to 'guide' by editing this line
    b = sys.argv[1]		# which group
setf()              # f is used to determine channels or groups
getchannelgroups()
if not b == 'last':
    setg()                  # g represents the number of the specified group
opengroups()	
finish()