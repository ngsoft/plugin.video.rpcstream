# -*- coding: utf-8 -*-
import sys
import six
from . import debug

parser = six.moves.urllib_parse

try:
    from re import fullmatch
except:
    import re

    def fullmatch(regex, string, flags=0):
        return re.match(r"(?:" + regex + r")\Z", string, flags=flags)


def redirect(full_path, args=None):
    global url
    url = url_for(full_path,  args)
    debug('redirecting to %s' % (url))
    urlparse()
    run()


def route(rule, **options):
    def decorator(function):
        if function in routedict:
            routedict[function].append((rule, options))
        else:
            routedict[function] = [(rule, options)]

        return function

    return decorator


def run():
    for function, routes in routedict.items():
        for rule, options in routes:
            match = fullmatch(rule, path)

            if match:
                kwargs = match.groupdict()

                for name, value in options.items():
                    if isinstance(value, str):
                        if name in query:
                            for string in query[name]:
                                match = fullmatch(value, string)

                                if match:
                                    kwargs.update(match.groupdict())
                                else:
                                    break
                        else:
                            match = None
                            break
                    elif isinstance(value, bool) and ((value and name not in query) or (not value and name in query)):
                        match = None
                        break

                if match:
                    function(**kwargs)
                    return


def url_for(full_path, args=None):
    result = base_url + full_path

    if isinstance(args, str):
        qs = args
        if args.startswith('?'):
            qs = args[1:]
        result += '?' + qs

    elif isinstance(args, dict):
        qs = get_query_string(args)
        result += '?' + qs

    return result


def get_query_params(queryString=None):
    result = {}
    if queryString == None and query_string:
        queryString = query_string
    if len(queryString) > 0:
        if queryString.startswith('?'):
            queryString = queryString[1:]
        result = dict(parser.parse_qsl(queryString))
    return result


def get_query_string(params=None):
    if params == None:
        return query_string
    if isinstance(params, dict):
        return parser.urlencode(params)


def urlparse():
    global base_url, full_path, path, query, query_string
    (scheme, netloc, path, params, query_string, fragment) = parser.urlparse(url)
    base_url = '%s://%s' % (scheme, netloc)
    full_path = '%s?%s' % (path, query_string) if query_string else path
    query = parser.parse_qs(query_string)


base_url = None
full_path = None
handle = int(sys.argv[1])
path = None
query = None
query_string = None
routedict = {}
url = sys.argv[0] + sys.argv[2]
urlparse()
