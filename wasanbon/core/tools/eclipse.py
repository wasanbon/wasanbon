#!/usr/bin/env python

import os, sys
import urllib
import platform
import subprocess
import zipfile
from wasanbon.core import *
from wasanbon.core.management import *


def launch_eclipse():
    setting = load_settings()
    eclipse_dir = os.path.join(setting['common']['path']['RTM_HOME'], 'eclipse')
    eclipse_cmd = os.path.join(eclipse_dir, "eclipse")
    if sys.platform == 'win32':
        eclipse_cmd = eclipse_cmd + '.exe'
    if not os.path.isfile(eclipse_cmd):
        sys.stdout.write("Eclipse can not be found in %s.\n" % eclipse_cmd)
        sys.stdout.write("Please install eclipse by 'wasanbon-admin.py tools install' command.\n")
        return

    if not os.path.isfile(os.path.join(os.getcwd(), "setting.yaml")):
        cmd = [eclipse_cmd]
    else:
        y = yaml.load(open('setting.yaml', 'r'))
        if 'application' in y.keys():
            if 'RTC_DIR' in y['application'].keys():
                sys.stdout.write("Starting eclipse in current project directory.\n")
                cmd = [eclipse_cmd, '-data', os.path.join(os.getcwd(), y['application']['RTC_DIR'])]
        else:
            cmd = [eclipse_cmd]

    if sys.platform == 'win32':
        subprocess.Popen(cmd, creationflags=512)
    else:
        subprocess.Popen(cmd)

    
