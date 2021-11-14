# -*- coding: utf-8 -*-
import base64
import re
import sys
from utils import router
from utils.constants import *
from six.moves import urllib_parse

from utils.utils import log, b64load, notify
from utils import logger, item


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


@router.route('/')
def _():
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
        params['title'] = title

    if 'headers' in params:
        newheaders = b64load(params['headers'])
        if newheaders != None:
            headers = newheaders

    # legacy support
    if 'useragent' in params:
        headers['User-Agent'] = params['useragent']

    # legacy support
    if 'referer' in params:
        ref = params['referer']
        headers['Referer'] = ref
        # Also add origin for cors
        if 'Origin' not in headers:
            parsed = urllib_parse.urlparse(ref)
            headers['Origin'] = '%s://%s' % (parsed.scheme + parsed.netloc)

    params['headers'] = headers

    # log params
    for key in params:
        log('%s => %s', key, params[key])

    if 'subtitles' in params and params['subtitles'].startswith('http'):
        subtitles = params['subtitles']
    if 'url' not in params or params['url'].startwith('http') == False:
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

    mode = int(mode)
    if mode not in [PLAY_MODE_DEFAULT, PLAY_MODE_HLS, PLAY_MODE_DASH]:
        msg = 'Invalid mode ' + str(mode)
        logger.error(msg)
        notify(msg)

    # Create Item
    kodiItem = item.Item(title=title, url=url,
                         subtitles=subtitles, headers=headers)


router.run()
