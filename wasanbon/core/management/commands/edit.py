#!/usr/bin/env python
import os, sys, yaml, subprocess, signal

import wasanbon
from wasanbon.core import rtc

def print_usage():
    print 'use wasanbon-admin.py edit [RTC_NAME]'

def signal_action(num, frame):
    pass

class Command(object):
    def __init__(self):
        pass

    def is_admin(self):
        return False

    def execute_with_argv(self, argv, clean, force, verbose):
        if len(argv) < 3:
            print_usage()
            return

        if not 'application' in wasanbon.setting.keys():
            print 'execute wasanbon-admin.py init command.'
            return

        rtcps = rtc.parse_rtcs()
        for rtcp in rtcps:
            if argv[2] == rtcp.basicInfo.name:
                editenv = os.environ.copy()
                if not 'HOME' in editenv.keys():
                    editenv['HOME'] = wasanbon.get_home_path()
                if sys.platform == 'darwin':
                    cmd = [wasanbon.setting['local']['emacs']]
                else:
                    cmd = [wasanbon.setting['local']['emacs'], '-nw']
                
                pp = rtc.PackageProfile(rtcp)
                files = pp.getSourceFiles()
                for file in files:
                    cmd.append(file)

                signal.signal(signal.SIGINT, signal_action)
                subprocess.call(cmd, env=editenv)

        
