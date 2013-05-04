#!/usr/bin/env python

import os
import urllib
import platform
import subprocess
import zipfile
import kotobuki.core.management.import_tools as importer
settings = importer.import_setting()
packages = importer.import_packages()

def launch_eclipse():
    rtc_dir = os.path.join(os.getcwd(), settings.application['RTC_DIR'])
    eclipse_dir = os.path.join(settings.rtm['TOOLS_ROOT'], 'eclipse')

    cmd = (os.path.join(eclipse_dir, "eclipse"), "-data", rtc_dir)
    if platform.system() == 'Windows':
        subprocess.Popen(cmd, creatioflags=512)
    else:
        subprocess.Popen(cmd)
"""
    conffile = os.path.join(eclipse_dir, 'configuration', 'config.ini')
    os.rename(conffile, conffile+'.bak')
    fin = open(conffile + '.bak', 'r')
    fout = open(conffile + '.bak', 'w')
    while True:
        line = fin.readline()
        if not line:
            break;
        if line.strip().startswith('#'):
            fout.write(line)
            continue

        if line.strip().startswith('osgi.instance.area.default'):
            fout.write('#' + line)
            fout.write('osgi.instance.area.default=' + rtc_dir)
            continue

        fout.write(line)
    fin.close()
    os.remove(conffile + '.bak')
    fout.close()
   """     

    
