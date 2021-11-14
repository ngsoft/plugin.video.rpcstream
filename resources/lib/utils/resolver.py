# -*- coding: utf-8 -*-

from . import constants

try:
    import urlresolver
except:
    urlresolver = None
try:
    import resolveurl
except:
    resolveurl = None

RESOLVERS = {
    'script.module.resolveurl': resolveurl,
    'script.module.urlresolver': urlresolver
}


def resolve(source):

    return source
