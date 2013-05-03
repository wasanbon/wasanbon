#!/usr/bin/env python

import wasanbon
from wasanbon.core.management import *

class Command(object):
    def __init__(self):
        pass

    def execute_with_argv(self, argv):
        setting = load_settings()
        repo = setting['common']['repository']['wasanbon']
        rtm_temp = setting['common']['path']['RTM_TEMP']
        print rtm_temp
