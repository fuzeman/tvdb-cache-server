import logging
import cherrypy
from src.pages import Server, Api

__author__ = 'Dean Gardiner'

class RootPage(object):
    @cherrypy.expose
    def index(self):
        return "RootPage, index"

def start(port=3475):
    logging.basicConfig(level=logging.DEBUG)
    logging.debug("server started")

    cherrypy.config.update({
        'server.socket_host': '127.0.0.1',
        'server.socket_port': port,
    })

    d = cherrypy.dispatch.RoutesDispatcher()
    # /api
    d.connect('api_getSeries', '/api/GetSeries.php', controller=Api.api_getSeries)
    d.connect('api_seriesBanners', '/api/:key/series/:sid/banners.xml', controller=Api.api_seriesBanners)
    d.connect('api_seriesActors', '/api/:key/series/:sid/actors.xml', controller=Api.api_seriesActors)
    d.connect('api_seriesInfo', '/api/:key/series/:sid/:lang.xml', controller=Api.api_seriesInfo)
    d.connect('api_epInfo', '/api/:key/series/:sid/all/:lang.xml', controller=Api.api_epInfo)
    d.connect('api_epInfo_zip', '/api/:key/series/:sid/all/:lang.zip', controller=Api.api_epInfo_zip)
    # /banners
    d.connect('api_banners_fanart', '/banners/fanart/:type/:id.jpg', controller=Api.api_banners_fanart)
    d.connect('api_banners', '/banners/:type/:id.jpg', controller=Api.api_banners)
    # /server
    d.connect('server', '/server', controller=Server.server_index)
    d.connect('server_test', '/server/test', controller=Server.server_test)

    cherrypy.tree.mount(root=RootPage(), config={
        '/': {
            'request.dispatch': d
        }
    })
    cherrypy.engine.start()
    cherrypy.engine.block()

if __name__ == '__main__':
    start()