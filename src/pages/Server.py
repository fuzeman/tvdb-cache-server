import logging
import cherrypy
from jinja2 import Environment, FileSystemLoader
from src.common import CACHE_DIR
import tvdb_api

env = Environment(loader=FileSystemLoader('templates'))

__author__ = 'Dean Gardiner'

def server_index():
    return env.get_template('server/index.html').render()

def server_test():
    logging.basicConfig(level=logging.DEBUG)

    t = tvdb_api.Tvdb(base_url="http://127.0.0.1:3475", cache=False)
    s = t['Bones']
    return str(s['seriesname'])