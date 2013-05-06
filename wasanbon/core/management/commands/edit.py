#!/usr/bin/env python
import wasanbon
from wasanbon.core.management import *
from wasanbon.core.tools import *
from wasanbon.core.template import *
from wasanbon.core.rtc import *
import os
import yaml
import subprocess

def print_usage():
    print 'use wasanbon-admin.py edit [RTC_NAME]'

class Command(object):
    def __init__(self):
        pass

    def execute_with_argv(self, argv):
        if len(argv) < 3:
            print_usage()
            return

        setting = load_settings()
        rtm_home = setting['common']['path']['RTM_HOME']
        if not os.path.isfile(os.path.join(rtm_home, 'setting.yaml')):
            print 'execute wasanbon-admin.py init command.'
            return

        y = yaml.load(open(os.path.join(rtm_home, 'setting.yaml'), 'r'))

        rtcps = parse_rtcs(argv)
        for rtcp in rtcps:
            if argv[2] == rtcp.getName():
                cmd = [y['emacs_path'], '-nw']
                pp = parse_package_profile(rtcp)
                files = pp.getSourceFiles()
                for file in files:
                    cmd.append(file)
                subprocess.call(cmd)

        
