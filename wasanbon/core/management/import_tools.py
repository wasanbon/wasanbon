#!/usr/bin/env python

import os
import kotobuki
import yaml

def import_setting():
    #module = __import__(kotobuki.app_name + '.' +  "setting")
    #setting = getattr(module, "setting")
    #return setting
    f = open(os.path.join(kotobuki.app_name, "setting.yaml"), 'r')
    class o:
        def __init__(self, fn):
            self.yaml = yaml.load(open(fn, 'r'))
            
    return o
#return yaml.load(f)
        
def import_packages():
    module = __import__(kotobuki.app_name + '.' +  "packages")
    packs = getattr(module, "packages")
    return packs
