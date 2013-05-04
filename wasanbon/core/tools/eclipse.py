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
    
    if not os.path.isfile("setting.yaml"):
        cmd = [os.path.join(eclipse_dir, "eclipse")]
    else:
        y = yaml.load(open('setting.yaml', 'r'))
        cmd = [os.path.join(eclipse_dir, "eclipse"), '-data', os.path.join(os.getcwd(), y['application']['RTC_DIR'])]

    if sys.platform == 'win32':
        subprocess.Popen(cmd, creatioflags=512)
    else:
        subprocess.Popen(cmd)

    
