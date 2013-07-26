#!/usr/bin/env python

import os, sys, subprocess, getpass, signal, time
import wasanbon
from wasanbon.core import rtc
from wasanbon import util
from wasanbon.core.rtc import git, hg

rtcprofile_filename = 'RTC.xml'

def signal_action(num, frame):
    pass


def print_rtc_profile(rtcp):
    str = rtcp.basicInfo.name + ' : \n'
    str = str + '    name       : ' + rtcp.basicInfo.name + '\n'
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
        if rtcname == rtcp.basicInfo.name:
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
            return
        if argv[2] == 'github_fork':
            if len(argv) < 4:
                wasanbon.show_help_description('rtc')
                return

            rtcname = argv[3]
            sys.stdout.write(' - Forking GITHUB repository in %s\n' % rtcname)
            sys.stdout.write('Username@github:')
            user = raw_input()
            passwd = getpass.getpass()

            if rtcname in wasanbon.repositories.keys():
                repo = wasanbon.repositories[rtcname]
                if 'git' in repo.keys():
                    url = repo['git']
                    print ' - GIT forking : %s' % url

                    gitenv = os.environ.copy()
                    if not 'HOME' in gitenv.keys():
                        gitenv['HOME'] = wasanbon.get_home_path()
                        print 'HOME is %s' % gitenv['HOME']

                    my_url = rtc.github_fork(user, passwd, url, verbose)
                    if my_url:
                        print ' - GIT cloning : %s' % my_url
                        distpath = os.path.join(os.getcwd(), wasanbon.setting['application']['RTC_DIR'], os.path.basename(url)[:-4])
                        cmd = [wasanbon.setting['local']['git'], 'clone', my_url, distpath]
                        subprocess.call(cmd, env=gitenv)
                        rtc.update_repository_yaml(rtcname, my_url)
                    return
            return

        if argv[2] == 'github_pullrequest':
            if len(argv) < 6:
                print ' - Invalid Usage.'
            rtcname = argv[3]
            title = argv[4]
            body = argv[5]
            sys.stdout.write('Username@github:')
            user = raw_input()
            passwd = getpass.getpass()
            if rtcname in wasanbon.repositories.keys():
                repo = wasanbon.repositories[rtcname]
                if 'git' in repo.keys():
                    print ' - Pull Requesting.' 
                    if not rtc.github_pullrequest(user, passwd, url, title, body, verbose):
                        print ' - Failed.'
            pass
            
        if argv[2] == 'clone':
            if len(argv) < 4:
                wasanbon.show_help_description('rtc')
                return

            gitenv = os.environ.copy()
            if not 'HOME' in gitenv.keys():
                gitenv['HOME'] = wasanbon.get_home_path()
                print 'HOME is %s' % gitenv['HOME']

            if argv[3].startswith('git@') or argv[3].startswith('http'):
                path = os.path.basename(argv[3])
                if path.endswith('.git'):
                    path = path[:-4]
                distpath = os.path.join(wasanbon.setting['application']['RTC_DIR'], path)
                cmd = [wasanbon.setting['local']['git'], 'clone', argv[3], distpath]
                subprocess.call(cmd, env=gitenv)
                rtc.update_repository_yaml(path, argv[3])
                return 
                
            for i in range(3, len(argv)):
                rtcname = argv[i]
                if rtcname in wasanbon.repositories.keys():
                    repo = wasanbon.repositories[rtcname]
                    if 'git' in repo.keys():
                        url = repo['git']
                        print ' - GIT cloning : %s' % url
                        distpath = os.path.join(os.getcwd(), wasanbon.setting['application']['RTC_DIR'], os.path.basename(url)[:-4])
                        cmd = [wasanbon.setting['local']['git'], 'clone', url, distpath]
                        subprocess.call(cmd, env=gitenv)
                        rtc.update_repository_yaml(rtcname, url)
                        #return
                    if 'hg' in repo.keys():
                        url = repo['hg']
                        print ' - Mercurial cloning : %s' % url
                        distpath = os.path.join(os.getcwd(), wasanbon.setting['application']['RTC_DIR'], rtcname)
                        cmd = [wasanbon.setting['local']['hg'], 'clone', url, distpath]
                        subprocess.call(cmd, env=gitenv)
                        #return
                        
                    else:
                        pass
                else:
                    print '%s Do not found' % rtcname
            return

        elif argv[2] == 'delete':
            if len(argv) < 4:
                wasanbon.show_help_description('rtc')
                return

            for i in range(3, len(argv)):
                rtcname = argv[i]
                foundFlag = False
                for rtcp in rtcps:
                    if rtcp.basicInfo.name == rtcname:
                        rtc.delete(rtcp)
                        foundFlag = True
                if not foundFlag:
                    sys.stdout.write(' - %s not found.' % rtcname)
            return
                
            
        if argv[2] == 'commit':
            if len(argv) < 5:
                print_usage()
            rtcname = argv[3]
            comment = argv[4]
            for rtcp in rtcps:
                if rtcname == rtcp.basicInfo.name:
                    rtc_dir = os.path.dirname(rtcp.getRTCProfileFileName())
                    if '.hg' in os.listdir(rtc_dir):
                        sys.stdout.write('Commiting Mercurial repository in %s\n' % rtcname)
                        hg.commit(rtcp, comment)
                    elif '.git' in os.listdir(rtc_dir):
                        sys.stdout.write('Commiting GIT repository in %s\n' % rtcname)
                        git.commit(rtcp, comment)
            return
        if argv[2] == 'pull':
            if len(argv) < 4:
                print_usage()
            rtcname = argv[3]
            for rtcp in rtcps:
                if rtcname == rtcp.basicInfo.name:
                    rtc_dir = os.path.dirname(rtcp.getRTCProfileFileName())
                    if '.hg' in os.listdir(rtc_dir):
                        sys.stdout.write('Pulling Mercurial repository in %s\n' % rtcname)
                        hg.pull(rtcp)
                    elif '.git' in os.listdir(rtc_dir):
                        sys.stdout.write('Pulling GIT repository in %s\n' % rtcname)
                        git.pull(rtcp)

            return
        if argv[2] == 'push':
            if len(argv) < 4:
                print_usage()
            rtcname = argv[3]
            for rtcp in rtcps:
                if rtcname == rtcp.basicInfo.name:
                    rtc_dir = os.path.dirname(rtcp.getRTCProfileFileName())
                    if '.hg' in os.listdir(rtc_dir):
                        sys.stdout.write('Pushing Mercurial repository in %s\n' % rtcname)
                        hg.push(rtcp)
                    elif '.git' in os.listdir(rtc_dir):
                        sys.stdout.write('Pushing Upstream GIT repository in %s\n' % rtcname)
                        git.push(rtcp)

            return
        if argv[2] == 'github_init':
            if len(argv) < 4:
                print_usage()
            rtcname = argv[3]
            for rtcp in rtcps:
                if rtcname == rtcp.basicInfo.name:
                    sys.stdout.write('Initializing GIT repository in %s\n' % rtcname)
                    sys.stdout.write('Username@github:')
                    user = raw_input()
                    passwd = getpass.getpass()
                    rtc.github_init(user, passwd, rtcp)
            return

        elif argv[2] == 'build':
            rtcps = rtc.parse_rtcs()

            if '--clean' in argv:
                clean_all = True if 'all' in argv else False
                for i in range(2, len(argv)):
                    rtc_name = argv[i]
                    for rtcp in rtcps:
                        if rtcp.basicInfo.name == rtc_name or clean_all:
                            print 'Cleanup RTC(%s).' % rtcp.basicInfo.name
                            rtc.clean_rtc(rtcp)
                return
            else:
                build_all = True if 'all' in argv else False
                for i in range(2, len(argv)):
                    rtc_name = argv[i]
                    for rtcp in rtcps:
                        if rtcp.basicInfo.name == rtc_name or build_all:
                            print 'Building rtc [%s]' % rtcp.basicInfo.name
                            rtc.build_rtc(rtcp)
                return
        elif argv[2] == 'edit':
            rtcps = rtc.parse_rtcs()
            for rtcp in rtcps:
                if argv[3] == rtcp.basicInfo.name:
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
        else:
            sys.stdout.write(' - Unknown command [%s]' % argv[2])
            
            pass

    
