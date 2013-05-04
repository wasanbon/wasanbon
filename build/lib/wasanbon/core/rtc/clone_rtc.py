import os
import urllib
import platform
import subprocess
import zipfile
#from status_rtm import *
import kotobuki.core.management.import_tools as importer
settings = importer.import_setting()
packages = importer.import_packages()



def clone_rtc(kind, name, url):
    if kind == 'git':
        cmd = ('git', 'clone', url, os.path.join(settings.application['RTC_DIR'], name))
        subprocess.call(cmd)
    else:
        print 'Unknown Package Kind (%s) for %s' % (kind, name)

