#!/usr/bin/env python

import os, sys, subprocess, getpass
import wasanbon
from wasanbon.core import rtc
from wasanbon import util
from wasanbon.core.rtc import git, hg

rtcprofile_filename = 'RTC.xml'


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

    def execute_with_argv(self, argv, verbose, force, clean):
        if len(argv) < 3:
            wasanbon.show_help_description('rtc')
            return

        rtcps = rtc.parse_rtcs()

        if argv[2] == 'list':
            for rtcp in rtcps:
                print_rtc_profile(rtcp)
                pp = rtc.PackageProfile(rtcp)
                print_package_profile(pp)
            return
        elif argv[2] == 'repository':
            url = wasanbon.repositories
            for key, value in url.items():
                print '  ' + key + ' ' * (24-len(key)) + ' : ' + value['description'] 
                if len(argv) >= 4 and argv[3] == '-l':
                    for k, v in value.items():
                        if not k == 'description':
                            print '       ' + k + ' ' * (24-len(k)) + ' : ' + v
            return

        if argv[2] == 'git_init':
            git_init(rtcps, argv)


        if argv[2] == 'clone':
            if len(argv) < 4:
                wasanbon.show_help_description('rtc')
                return

            for i in range(3, len(argv)):
                rtcname = argv[i]
                if rtcname in wasanbon.repositories.keys():
                    repo = wasanbon.repositories[rtcname]
                    if 'git' in repo.keys():
                        url = repo['git']
                        print 'GIT cloning : %s' % url
                        distpath = os.path.join(os.getcwd(), wasanbon.setting['application']['RTC_DIR'], os.path.basename(url)[:-4])
                        cmd = [wasanbon.setting['local']['git'], 'clone', url, distpath]
                        subprocess.call(cmd)
                        return
                    if 'hg' in repo.keys():
                        url = repo['hg']
                        print 'Mercurial cloning : %s' % url
                        distpath = os.path.join(os.getcwd(), wasanbon.setting['application']['RTC_DIR'], rtcname)
                        cmd = [wasanbon.setting['local']['hg'], 'clone', url, distpath]
                        subprocess.call(cmd)
                        return
                        
                    else:
                        pass
            print 'Do not found'
            return
            
        if argv[2] == 'commit':
            if len(argv) < 5:
                print_usage()
            rtcname = argv[3]
            comment = argv[4]
            for rtcp in rtcps:
                if rtcname == rtcp.getName():
                    rtc_dir = os.path.dirname(rtcp.getRTCProfileFileName())
                    if '.hg' in os.listdir(rtc_dir):
                        sys.stdout.write('Commiting Mercurial repository in %s\n' % rtcname)
                        hg.commit(rtcp, comment)
                    elif '.git' in os.listdir(rtc_dir):
                        sys.stdout.write('Commiting GIT repository in %s\n' % rtcname)
                        git.commit(rtcp, comment)

        if argv[2] == 'push':
            if len(argv) < 4:
                print_usage()
            rtcname = argv[3]
            for rtcp in rtcps:
                if rtcname == rtcp.getName():
                    rtc_dir = os.path.dirname(rtcp.getRTCProfileFileName())
                    if '.hg' in os.listdir(rtc_dir):
                        sys.stdout.write('Pushing Mercurial repository in %s\n' % rtcname)
                        hg.push(rtcp)
                    elif '.git' in os.listdir(rtc_dir):
                        sys.stdout.write('Pushing Upstream GIT repository in %s\n' % rtcname)
                        git.push(rtcp)

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

        elif argv[2] == 'build':
            rtcps = rtc.parse_rtcs()

            if '--clean' in argv:
                clean_all = True if 'all' in argv else False
                for i in range(2, len(argv)):
                    rtc_name = argv[i]
                    for rtcp in rtcps:
                        if rtcp.getName() == rtc_name or clean_all:
                            print 'Cleanup RTC(%s).' % rtcp.getName()
                            rtc.clean_rtc(rtcp)
                return
            else:
                build_all = True if 'all' in argv else False
                for i in range(2, len(argv)):
                    rtc_name = argv[i]
                    for rtcp in rtcps:
                        if rtcp.getName() == rtc_name or build_all:
                            print 'Building rtc [%s]' % rtcp.getName()
                            rtc.build_rtc(rtcp)
                return
            

            
            
            pass

    
