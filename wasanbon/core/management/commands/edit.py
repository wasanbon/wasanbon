#!/usr/bin/env python
import os, sys, yaml, subprocess

import wasanbon
from wasanbon.core import rtc

def print_usage():
    print 'use wasanbon-admin.py edit [RTC_NAME]'

class Command(object):
    def __init__(self):
        pass

    def execute_with_argv(self, argv):
        if len(argv) < 3:
            print_usage()
            return

        if not 'application' in wasanbon.setting.keys():
            print 'execute wasanbon-admin.py init command.'
            return

        rtcps = rtc.parse_rtcs()
        for rtcp in rtcps:
            if argv[2] == rtcp.getName():
                cmd = [wasanbon.setting['local']['emacs'], '-nw']
                pp = rtc.PackageProfile(rtcp)
                files = pp.getSourceFiles()
                for file in files:
                    cmd.append(file)
                subprocess.call(cmd)

        
