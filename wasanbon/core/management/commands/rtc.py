#!/usr/bin/env python

import os, sys, subprocess, getpass, signal, time
import wasanbon
from wasanbon.core import rtc
from wasanbon import util
from wasanbon.core.rtc import git, hg
from wasanbon.core import project

from wasanbon.util import editor

rtcprofile_filename = 'RTC.xml'



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
    filename = pp.getConfFilePath()
    if filename.startswith(os.getcwd()):
        filename = filename[len(os.getcwd()) + 1:]
    str = '    config     : ' + filename + '\n'
    sys.stdout.write(str)

    filename = pp.getRTCFilePath()
    if filename.startswith(os.getcwd()):
        filename = filename[len(os.getcwd()) + 1:]
    str = '    binary     : ' + filename + '\n'
    sys.stdout.write(str)

    filename = pp.getRTCExecutableFilePath()
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

        proj = project.Project(os.getcwd())


        if argv[2] == 'list':
            if verbose:
                sys.stdout.write(' - Listing RTCs in current project\n')
            for rtc in proj.rtcs:
                print_rtc_profile(rtc.rtcprofile)
                print_package_profile(rtc.packageprofile)
            return

        elif argv[2] == 'repository':
            if verbose:
                sys.stdout.write(' - Listing RTC Repository\n')
            for repo in wasanbon.core.rtc.get_repositories(verbose):
                sys.stdout.write(' - %s\n' % repo.name)
                sys.stdout.write('    description : %s\n' % repo.description)
                sys.stdout.write('    protocol    : %s\n' % repo.protocol)
                sys.stdout.write('    url         : %s\n' % repo.url)
            return

        elif argv[2] == 'git_init':
            for rtc in proj.rtcs:
                if rtc.name == argv[3]:
                    rtc.git_init(verbose)
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
            sys.stdout.write(' - Cloning RTC\n')
            if len(argv) < 4:
                wasanbon.show_help_description('rtc')
                return

            # if argument is url, then, clone by git command
            if argv[3].startswith('git@') or argv[3].startswith('http'):
                rtc_ = proj.clone_rtc(argv[3], verbose=verbose)
                return 
                
            #for i in range(3, len(argv)):
            for name in argv[3:]:
                repo = wasanbon.core.rtc.get_repository(name)
                if repo:
                    rtc_ = proj.clone_rtc(repo.url, verbose=verbose)
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
            if len(argv) <= 3:
                sys.stdout.write(' - Invalid Usage. Use --help option\n')
                return
            build_all = True if 'all' in argv else False
            for rtc in proj.rtcs:
                if build_all or rtc.name in argv:
                    if verbose:
                        sys.stdout.write(' - Cleaning Up RTC %s\n' % rtc.name)
                    rtc.clean(verbose=verbose)
            return

        elif argv[2] == 'build':
            if len(argv) <= 3:
                sys.stdout.write(' - Invalid Usage. Use --help option\n')
                return

            build_all = True if 'all' in argv else False
            for rtc in proj.rtcs:
                if build_all or rtc.name in argv:
                    if verbose:
                        sys.stdout.write(' - Building RTC %s\n' % rtc.name)
                    rtc.build(verbose=verbose)
            return

        elif argv[2] == 'edit':
            rtc_obj = proj.rtc(argv[3])
            if rtc_obj:
                editor.edit_rtc(rtc_obj, verbose)
            return


    
