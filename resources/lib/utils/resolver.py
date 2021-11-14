# -*- coding: utf-8 -*-

from . import settings, utils

# <setting id="rpcstream.urlresolver" type="bool" label="Use UrlResolver if available" default="true"/>
# <setting id="rpcstream.resolveurl" type="bool" label="Use ResolveUrl if available" default="true"/>
SETTING_URLRESOLVER = settings.get_setting_as_bool('rpcstream.urlresolver')
SETTING_RESOLVEURL = settings.get_setting_as_bool('rpcstream.resolveurl')

_resolvers = []

if SETTING_RESOLVEURL == True:
    try:
        import resolveurl
        _resolvers.append(resolveurl.resolve)
    except:
        SETTING_RESOLVEURL = False
        settings.set_setting('rpcstream.resolveurl', SETTING_RESOLVEURL)

if SETTING_URLRESOLVER == True:
    try:
        import urlresolver
        _resolvers.append(urlresolver.resolve)
    except:
        SETTING_URLRESOLVER = False
        settings.set_setting('rpcstream.urlresolver', SETTING_URLRESOLVER)

ENABLED = SETTING_URLRESOLVER == True or SETTING_RESOLVEURL == True


def resolve(source):
    if len(_resolvers) > 0:
        for _resolve in _resolvers:
            try:
                result = _resolve(source)
                if result:
                    utils.debug('url %s resolved: %s' % (source, resolved))
                    return result
            except:
                pass
    return source
