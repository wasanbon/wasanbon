#!/usr/bin/env python
import sys, os
import yaml, types
from wasanbon.core.management import *

tagdict = {'$HOME': get_home_path()}

def load_settings():
    import wasanbon
    root_dir = os.path.join(wasanbon.__path__[0], 'settings')
    setting = load_subdir(root_dir)
    
    pathdict = setting['common']['path']
    old_len = len(tagdict)
    while True:
        for key in pathdict:
            pathdict[key] = replace_tag(pathdict[key])
        update_tagdict(pathdict)
        if len(tagdict) == old_len:
            break
        old_len = len(tagdict)

        #if type(setting) is types.DictType:
        #setting = parse_yaml(setting)
    return setting

def update_tagdict(hash):
    for key in hash.keys():
        if hash[key].find('$') < 0:
            tagdict['$'+key] = hash[key]

def replace_tag(str):
    global tagdict
    for tag in tagdict.keys():
        str = str.replace(tag, tagdict[tag])
    return str

def parse_yaml(hash):
    for key in hash.keys():
        val = hash[key]
        if type(val) is types.DictType:
            hash[key] = parse_yaml(val)
        elif type(val) is types.StringType:
            hash[key] = replace_tags(val)
    return hash

def load_yaml(file):
    return yaml.load(open(file, 'r'))
    
def load_subdir(root):
    ret = {}
    for dir in os.listdir(root):
        path = os.path.join(root, dir)
        if os.path.isdir(path):
            ret[dir] = load_subdir(path)
        elif os.path.isfile(path):
            if dir.endswith('yaml'):
                ret[dir[:len(dir)-5]] = load_yaml(path)
    return ret
