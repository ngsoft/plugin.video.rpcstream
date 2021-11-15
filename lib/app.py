# -*- coding: utf-8 -*-
from kodi_six import xbmc
from .utils import resolver
from .models import History
from .items import *
from .icons import *
from .constants import *
from .utils import *
import base64
import re
import six

urllib_parse = six.moves.urllib_parse


# params = {
#    'request': {}, # b64encoded json string
#    'title': '', # b64encoded or plain text string
#    'url': '', # string starting with http
#    'subtitles': '', # string starting with http
#    'headers': {}, # b64encoded json string
#    'mode': 0,
#    deprecated:
#    'useragent': '', #plain text string
#    'referer': '', #plain text string
# }

# Main Menu
@router.route('/', url=False, request=False)
def _():
    dir = Directory()
    dir.addItem(Item('History', router.url_for(
        '/history'), ICON_VIDEOPLAYLISTS, True))
    dir.addItem(Item('Settings', router.url_for('/settings'), ICON_PROGRAM))
    dir.render()


# route with url
@router.route('/', url=True)
def _():
    router.redirect('/play', router.query_string)


# route with request
@router.route('/', request=True)
def _():
    router.redirect('/play', router.query_string)


@router.route('/history/clear')
def _():
    if confirm('Would you like to clear the history.') == True:
        hist = History()
        hist.clear()
        alert('History Cleared !')

    router.redirect('/')


@router.route('/history/delete', id=True)
def _():

    params = router.get_query_params()
    id = int(params['id'])
    hist = History()
    hist.delete(id)
    hist.close()
    alert('History entry removed.')
    xbmc.executebuiltin('Container.Refresh')


@router.route('/history')
def _():
    hist = History()
    cnt = 0
    dir = Directory('videos')

    for (id, title, path) in hist.getIterator():
        cnt += 1
        item = Item(title, router.url_for(
            '/play', {'id': id}), ICON_VIDEO, False, False)
        item.getListItem().addContextMenuItems([
            ('Remove entry', 'RunPlugin(%s)' %
             (router.url_for('/history/delete', {'id': id})))
        ])
        dir.addItem(item)

    hist.close()

    if cnt == 0:
        alert('History is empty.')
        router.redirect('/')
    else:
        dir.addItem(Item('Clear History.', router.url_for(
            '/history/clear'), ICON_PROGRAM, True))
        dir.render()


@router.route('/settings')
def _():
    show_settings()


@router.route('/play', id=False)
def _():
    currentURL = router.url
    hist = History()
    url = None
    subtitles = None
    mode = None
    title = None
    headers = {'User-Agent':  USER_AGENT}
    params = router.get_query_params()
    # request is the best way to pass the params
    if 'request' in params:
        newParams = b64load(params['request'])
        for key in newParams:
            params[key] = newParams[key]

    # title can be b64encoded inside json
    if 'title' in params:
        try:
            title = base64.b64decode(params['title'])
        except:
            title = params['title']

        #title = ensure_str(u(title))
        params['title'] = title

    if 'headers' in params:
        newheaders = b64load(params['headers'])
        if newheaders != None:
            headers = newheaders

    # legacy support
    if 'useragent' in params:
        debug('Using deprecated param: useragent')
        headers['User-Agent'] = params['useragent']

    # legacy support
    if 'referer' in params:
        debug('Using deprecated param: referer')
        ref = params['referer']
        headers['Referer'] = ref
        # Also add origin for cors
        if 'Origin' not in headers:
            parsed = urllib_parse.urlparse(ref)
            headers['Origin'] = '%s://%s' % (parsed.scheme, parsed.netloc)

    params['headers'] = headers

    if 'subtitles' in params and params['subtitles'].startswith('http'):
        subtitles = params['subtitles']
    if 'url' not in params or params['url'].startswith('http') == False:
        msg = 'Invalid URL Provided !'
        logger.error(msg)
        notify(msg)
        return
    url = params['url']

    if 'mode' in params:
        mode = int(params['mode'])

    # Auto set mode (if not explicitely set in the request)
    if mode == None:
        mode = PLAY_MODE_DEFAULT
        if re.search(r'\.m3u8', url) != None:
            mode = PLAY_MODE_HLS
        elif re.search(r'\.(json|dash|mpd)', url) != None:
            mode = PLAY_MODE_DASH
    params['mode'] = mode

    # log params
    debug(params)

    mode = int(mode)
    if mode not in [PLAY_MODE_DEFAULT, PLAY_MODE_HLS, PLAY_MODE_DASH]:
        msg = 'Invalid mode ' + str(mode)
        logger.error(msg)
        notify(msg)

    result = False
    if resolver.ENABLED == True:
        resolved = resolver.resolve(url)
        if resolved:

            kodiItem = VideoItem(title=title, path=resolved,
                                 subtitles=subtitles, headers=None)
            result = kodiItem.play()
            if result == True and hist.has(currentURL) == False:
                hist.add(title, currentURL)
            hist.close()
            return

    # Create Item
    kodiItem = VideoItem(title=title, path=url,
                         subtitles=subtitles, headers=headers)
    if mode == PLAY_MODE_DASH:
        result = kodiItem.playDash()
    elif mode == PLAY_MODE_HLS:
        result = kodiItem.playHLS()
    else:
        result = kodiItem.play()
    if result == True and hist.has(currentURL) == False:
        hist.add(title, currentURL)
    hist.close()


@router.route('/play', id=True)
def _():
    hist = History()
    params = router.get_query_params()
    id = int(params['id'])
    result = hist.find(id)
    if result == None:
        debug('Cannot find history entry with id %s' % (id))
        notify('Cannot find video!')
        return

    (id, title, path) = result
    hist.close()

    notify('Loading %s' % (title), icon=ICON_VIDEO)

    router.redirect_to_path(path)


def run():
    router.run()
