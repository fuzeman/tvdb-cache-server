import urllib2
import cherrypy
import os
from src.common import CACHE_DIR, BANNERS_CACHE_DIR, create_dir
import tvdb_api
from tvdb_cache import exists_in_cache, CachedResponse

__author__ = 'Dean Gardiner'

def _cacheResponse(url):
    if exists_in_cache(CACHE_DIR, url, 21600):
        response = CachedResponse(
            CACHE_DIR,
            url,
            set_cache_header = True
        )
        for rk, rv in response.headers.dict.items():
            if not rk in ['connection', 'transfer-encoding']:
                cherrypy.response.headers[rk] = rv
        return response.read()
    else:
        raise cherrypy.HTTPError(500, 'Internal Server Error')

def _download(url, path):
    print url, path

    req = urllib2.Request(url)
    f = urllib2.urlopen(req)

    _write(path, f.read())
    _write(path + ".headers", str(f.info()))

def _write(path, data):
    f = open(path, 'wb')
    f.write(data)
    f.close()

def _read(path):
    f = open(path, 'rb')
    d = f.read()
    f.close()
    return d

def _setHeadersFromData(data):
    for hl in data.split('\n'):
        if ':' in hl:
            i = hl.index(':')
            hk = hl[:i].strip()
            hv = hl[i+1:].strip()

            if not hk in ['connection', 'transfer-encoding']:
                cherrypy.response.headers[hk] = hv

def api_getSeries(seriesname, language):
    t = tvdb_api.Tvdb(cache = CACHE_DIR, language = language)
    show = t[seriesname]

    return _cacheResponse(u"%s/api/GetSeries.php?seriesname=%s&language=%s" % (t.config['base_url'], seriesname, language))

def api_seriesInfo(key, sid, lang):
    t = tvdb_api.Tvdb(cache = CACHE_DIR, language = lang)
    show = t[int(sid)]

    return _cacheResponse(t.config['url_seriesInfo'] % (show['id'], show['language']))

def api_seriesBanners(key, sid):
    t = tvdb_api.Tvdb(cache = CACHE_DIR, banners = True)
    show = t[int(sid)]

    return _cacheResponse(t.config['url_seriesBanner'] % (show['id']))

def api_seriesActors(key, sid):
    t = tvdb_api.Tvdb(cache = CACHE_DIR, actors = True)
    show = t[int(sid)]

    return _cacheResponse(t.config['url_actorsInfo'] % (show['id']))

def api_epInfo(key, sid, lang):
    t = tvdb_api.Tvdb(cache = CACHE_DIR, language = lang)
    show = t[int(sid)]

    return _cacheResponse(t.config['url_epInfo'] % (show['id'], show['language']))

def api_epInfo_zip(key, sid, lang):
    t = tvdb_api.Tvdb(cache = CACHE_DIR, language = lang, useZip = True)
    show = t[int(sid)]

    return _cacheResponse(t.config['url_epInfo_zip'] % (show['id'], show['language']))

def api_banners(type, id):
    dir = os.path.join(BANNERS_CACHE_DIR, type)
    create_dir(dir)
    file = os.path.join(dir, id + '.jpg')

    if not os.path.exists(file) or not os.path.exists(file + '.headers'):
        _download("http://www.thetvdb.com/banners/" + type + "/" + id + ".jpg", file)

    _setHeadersFromData(_read(file + '.headers'))

    return _read(file)

def api_banners_fanart(type, id):
    dir = os.path.join(BANNERS_CACHE_DIR, 'fanart', type)
    create_dir(dir)
    file = os.path.join(dir, id + '.jpg')

    if not os.path.exists(file) or not os.path.exists(file + '.headers'):
        _download("http://www.thetvdb.com/banners/fanart/" + type + "/" + id + ".jpg", file)

    _setHeadersFromData(_read(file + '.headers'))

    return _read(file)