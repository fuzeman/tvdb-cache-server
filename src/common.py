import os

__author__ = 'Dean Gardiner'

BASE_DIR = os.path.realpath(os.curdir)
CACHE_DIR = os.path.join(BASE_DIR, 'data', 'cache')
BANNERS_CACHE_DIR = os.path.join(CACHE_DIR, 'banners')

def create_dir(path):
    if os.path.exists(path): return
    os.makedirs(path)

create_dir(CACHE_DIR)
create_dir(BANNERS_CACHE_DIR)