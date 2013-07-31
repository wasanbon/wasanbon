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

        elif argv[2] == 'git_init':
            git_init(rtcps, argv)
            return
        elif argv[2] == 'github_fork':
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

                    my_url = rtc.github_fork(user, passwd, url, verbose)
                    if my_url:
                        rtcp = git.clone(my_url, verbose)
                        hash = git.get_hash(rtcp, verbose)
                        rtc.update_repository_yaml(rtcp.basicInfo.name, my_url, protocol='git', hash=hash, verbose=verbose)
                    return
            return

        elif argv[2] == 'github_pullrequest':
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
                    url = repo['git']
                    print ' - Pull Requesting url: %s'  % url
                    if not rtc.github_pullrequest(user, passwd, url, title, body, verbose):
                        print ' - Failed.'
            pass
            
        elif argv[2] == 'clone':
            if len(argv) < 4:
                wasanbon.show_help_description('rtc')
                return

            # if argument is url, then, clone by git command
            if argv[3].startswith('git@') or argv[3].startswith('http'):
                rtcp = git.clone(argv[3], verbose)
                hash  = git.get_hash(rtcp)
                hash = git.get_hash(rtcp, verbose)
                rtc.update_repository_yaml(rtcp.basicInfo.name, argv[3], protocol='git', hash=hash, verbose=verbose)
                return 
                
            for i in range(3, len(argv)):
                rtcname = argv[i]
                if rtcname in wasanbon.repositories.keys():
                    repo = wasanbon.repositories[rtcname]
                    if 'git' in repo.keys():
                        url = repo['git']
                        rtcp = git.clone(url, verbose)
                        hash  = git.get_hash(rtcp, verbose)
                        rtc.update_repository_yaml(rtcp.basicInfo.name, url, protocol='git', hash=hash, verbose=verbose)
                        #return
                    if 'hg' in repo.keys():
                        gitenv = os.environ.copy()
                        if not 'HOME' in gitenv.keys():
                            gitenv['HOME'] = wasanbon.get_home_path()
                            print 'HOME is %s' % gitenv['HOME']
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
                        rtc.delete(rtcp, verbose=verbose, force=force)
                        foundFlag = True
                        rtc.delete_repository_yaml(rtcname, verbose=verbose)
                if not foundFlag:
                    sys.stdout.write(' - %s not found.' % rtcname)
            return
                
            
        elif argv[2] == 'commit':
            if len(argv) < 5:
                print_usage()
            not_found = True
            rtcname = argv[3]
            comment = argv[4]
            for rtcp in rtcps:
                if rtcname == rtcp.basicInfo.name:
                    not_found = False
                    rtc_dir = os.path.dirname(rtcp.getRTCProfileFileName())
                    if '.hg' in os.listdir(rtc_dir):
                        sys.stdout.write('Commiting Mercurial repository in %s\n' % rtcname)
                        hg.commit(rtcp, comment)
                    elif '.git' in os.listdir(rtc_dir):
                        sys.stdout.write('Commiting GIT repository in %s\n' % rtcname)
                        git.commit(rtcp, comment)
                        hash = git.get_hash(rtcp, verbose)
                        rtc.update_repository_yaml(rtcname, protocol='git', hash=hash, verbose=verbose)
            if not_found:
                print ' - RTC(%s) not found.' % rtcname
            return

        elif argv[2] == 'pull':
            if len(argv) < 4:
                print_usage()
            rtcname = argv[3]
            not_found = True
            for rtcp in rtcps:
                if rtcname == rtcp.basicInfo.name:
                    not_found = False
                    rtc_dir = os.path.dirname(rtcp.getRTCProfileFileName())
                    if '.hg' in os.listdir(rtc_dir):
                        sys.stdout.write('Pulling Mercurial repository in %s\n' % rtcname)
                        hg.pull(rtcp)
                    elif '.git' in os.listdir(rtc_dir):
                        sys.stdout.write('Pulling GIT repository in %s\n' % rtcname)
                        git.pull(rtcp)

            if not_found:
                print ' - RTC(%s) not found.' % rtcname
            return

        elif argv[2] == 'checkout':
            if len(argv) < 4:
                print_usage()
            rtcname = argv[3]
            not_found = True
            for rtcp in rtcps:
                if rtcname == rtcp.basicInfo.name:
                    not_found = False
                    rtc_dir = os.path.dirname(rtcp.getRTCProfileFileName())
                    if '.git' in os.listdir(rtc_dir):
                        sys.stdout.write('Rollback GIT repository in %s\n' % rtcname)
                        git.checkout(rtcp, verbose)

            if not_found:
                print ' - RTC(%s) not found.' % rtcname
            return

        elif argv[2] == 'push':
            if len(argv) < 4:
                print_usage()
            rtcname = argv[3]
            not_found = True
            for rtcp in rtcps:
                if rtcname == rtcp.basicInfo.name:
                    not_found = False
                    rtc_dir = os.path.dirname(rtcp.getRTCProfileFileName())
                    if '.hg' in os.listdir(rtc_dir):
                        sys.stdout.write('Pushing Mercurial repository in %s\n' % rtcname)
                        hg.push(rtcp)
                    elif '.git' in os.listdir(rtc_dir):
                        sys.stdout.write('Pushing Upstream GIT repository in %s\n' % rtcname)
                        git.push(rtcp)
            if not_found:
                print ' - RTC(%s) not found.' % rtcname
            return


        elif argv[2] == 'github_init':
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
        elif argv[2] == 'clean':
            rtcps = rtc.parse_rtcs()
            clean_all = True if 'all' in argv else False
            rtcs = argv[2:] if not clean_all else ['all']
            for rtc_name in rtcs:
                for rtcp in rtcps:
                    if rtcp.basicInfo.name == rtc_name or clean_all:
                        print ' - Cleanup build directory of RTC(%s).' % rtcp.basicInfo.name
                        rtc.clean_rtc(rtcp, verbose=verbose)
                
            return
        elif argv[2] == 'build':
            rtcps = rtc.parse_rtcs()
            build_all = True if 'all' in argv else False
            rtcs = argv[2:] if not build_all else ['all']
            for rtc_name in rtcs:
                for rtcp in rtcps:
                    if rtcp.basicInfo.name == rtc_name or build_all:
                        print ' - Building rtc [%s]' % rtcp.basicInfo.name
                        rtc.build_rtc(rtcp, verbose=verbose)
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
            return
        else:
            sys.stdout.write(' - Unknown command [%s]' % argv[2])
            
            pass

    
