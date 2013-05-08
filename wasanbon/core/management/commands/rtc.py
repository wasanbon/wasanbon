#!/usr/bin/env python

import os, sys
import wasanbon
from wasanbon.core import rtc
from wasanbon import util
from wasanbon.core.rtc import git

import getpass
rtcprofile_filename = 'RTC.xml'

def print_usage(cmd=''):
    return

def print_rtc_profile(rtcp):
    str = rtcp.getName() + ' : \n'
    str = str + '    name       : ' + rtcp.getName() + '\n'
    str = str + '    language   : ' + rtcp.getLanguage() + '\n'
    str = str + '    category   : ' + rtcp.getCategory() + '\n'
    filename = rtcp.getRTCProfileFileName()
    if filename.startswith(os.getcwd()):
        filename = filename[len(os.getcwd()) + 1:]
    str = str + '    RTC.xml    : ' + filename + '\n'
    sys.stdout.write(str)

def print_package_profile(pp):
    filename = pp.getRTCFilePath()
    if filename.startswith(os.getcwd()):
        filename = filename[len(os.getcwd()) + 1:]
    str = '    executable : ' + filename + '\n'
    sys.stdout.write(str)

def git_init(rtcps, argv):
    if len(argv) < 4:
        print_usage()
    rtcname = argv[3]
    for rtcp in rtcps:
        if rtcname == rtcp.getName():
            sys.stdout.write('Initializing GIT repository in %s\n' % rtcname)
            git.git_init(rtcp)

class Command(object):
    def __init__(self):
        pass

    def execute_with_argv(self, argv):
        if len(argv) < 3:
            print_usage()
        rtcps = rtc.parse_rtcs()

        if argv[2] == 'list':
            for rtcp in rtcps:
                print_rtc_profile(rtcp)
                pp = rtc.PackageProfile(rtcp)
                print_package_profile(pp)

        if argv[2] == 'git_init':
            git_init(rtcps, argv)

        if argv[2] == 'git_clone':
            if len(argv) < 4:
                print_usage('git_clone')
            rtcname = argv[3]
            distpath = os.path.join(wasanbon.rtm_temp, os.path.basename(url)[:-4])
            cmd = [wasanbon.setting['local']['git'], 'clone', url, distpath]
            subprocess.call(cmd)
            crrdir = os.getcwd()
            os.chdir(distpath)
            cmd = ['python', 'setup.py', 'install', '--record', 'installed_files.txt']
            subprocess.call(cmd)
            os.chdir(crrdir)

            
        if argv[2] == 'git_commit':
            if len(argv) < 5:
                print_usage()
            rtcname = argv[3]
            comment = argv[4]
            for rtcp in rtcps:
                if rtcname == rtcp.getName():
                    sys.stdout.write('Commiting GIT repository in %s\n' % rtcname)
                    git.git_commit(rtcp, comment)

        if argv[2] == 'git_push':
            if len(argv) < 4:
                print_usage()
            rtcname = argv[3]
            for rtcp in rtcps:
                if rtcname == rtcp.getName():
                    sys.stdout.write('Pushing Upstream GIT repository in %s\n' % rtcname)
                    git.git_push(rtcp)

        if argv[2] == 'github_init':
            if len(argv) < 4:
                print_usage()
            rtcname = argv[3]
            for rtcp in rtcps:
                if rtcname == rtcp.getName():
                    sys.stdout.write('Initializing GIT repository in %s\n' % rtcname)
                    sys.stdout.write('Username@github:')
                    user = raw_input()
                    passwd = getpass.getpass()
                    rtc.github_init(user, passwd, rtcp)
        pass

    

