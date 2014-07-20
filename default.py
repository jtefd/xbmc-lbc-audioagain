import sys
import os.path
import xbmcplugin
import xbmcaddon
import xbmcgui
import urlparse

__plugin_handle__ = int(sys.argv[1])
__plugin_name__ = sys.argv[0]
__plugin_settings__ = xbmcaddon.Addon(id='plugin.audio.lbc_audioagain')

sys.path.append(xbmc.translatePath(os.path.join( __plugin_settings__.getAddonInfo('path'), 'lib' )))

from LBCAudioAgain import LBCAudioAgain

username = xbmcplugin.getSetting(__plugin_handle__, 'username')
password = xbmcplugin.getSetting(__plugin_handle__, 'password')

lbc = LBCAudioAgain(username, password)

def INDEX():
    feeds = lbc.get_feeds();
    
    for feed in sorted(feeds, key=feeds.get):
        listItem = xbmcgui.ListItem(feeds[feed])
        
        feed_image = lbc.get_feed_image(feed, xbmc.translatePath(os.path.join( __plugin_settings__.getAddonInfo('path'), 'resources', 'img' )))

        listItem.setIconImage(feed_image)
        listItem.setIconImage(feed_image)
        
        xbmcplugin.addDirectoryItem(
            handle=__plugin_handle__,
            url=__plugin_name__ + "?action=list_episodes&feed=" + feed,
            listitem=listItem,
            isFolder=True
        )
    
def EPISODES(feed_id):
    try:
        eps = lbc.get_feed_episodes(feed_id);
        
        feed_image = lbc.get_feed_image(feed_id, xbmc.translatePath(os.path.join( __plugin_settings__.getAddonInfo('path'), 'resources', 'img' )))
    
        for ep in sorted(eps, reverse=True):
            listItem = xbmcgui.ListItem(eps[ep])
            listItem.setIconImage(feed_image)
            listItem.setIconImage(feed_image)
        
            xbmcplugin.addDirectoryItem(
                handle=__plugin_handle__,
                url=ep,
                listitem=listItem
            )
    except:
        dialog = xbmcgui.Dialog()
        dialog.ok("Failed retrieving episodes", "Please check username/password")


params = urlparse.parse_qs(sys.argv[2].replace('?',''))

print params

if 'action' in params:
	action = params['action'][0]

	if action == 'list_episodes' and 'feed' in params:
		EPISODES(params['feed'][0])
else:
	INDEX()
    
xbmcplugin.endOfDirectory(__plugin_handle__)
