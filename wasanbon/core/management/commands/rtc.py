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


def print_rtc(rtc):
    print_rtc_profile(rtc.rtcprofile)
    print_package_profile(rtc.packageprofile)
    pass

def print_repository(repo):
    sys.stdout.write(' - %s\n' % repo.name)
    sys.stdout.write('    description : %s\n' % repo.description)
    sys.stdout.write('    protocol    : %s\n' % repo.protocol)
    sys.stdout.write('    url         : %s\n' % repo.url)
    pass

class Command(object):
    def __init__(self):
        pass

    def execute_with_argv(self, argv, verbose, force, clean):
        proj = project.Project(os.getcwd())

        if argv[2] == 'list':
            if verbose:
                sys.stdout.write(' - Listing RTCs in current project\n')
                return False
            for rtc in proj.rtcs:
                print_rtc(rtc)
            return True

        elif argv[2] == 'repository':
            if verbose:
                sys.stdout.write(' - Listing RTC Repository\n')
                return False
            for repo in wasanbon.core.rtc.get_repositories(verbose):
                print_repository(repo)
            return True

        elif argv[2] == 'git_init':
            if len(argv) < 3:
                sys.stdout.write(' - Invalid Usage. Use --help option.\n')
                return False
            rtc_ = proj.rtc(argv[3])
            if rtc_:
                rtc_.git_init(verbose)
            return True

        elif argv[2] == 'github_fork':
            if len(argv) < 4:
                sys.stdout.write(' - Invalid Usage. Use --help option.\n')
                return False

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
                url = argv[3]
                name = os.path.basename(argv[3])
                if name.endswith('.git'):
                    name = name[:-4]
                repo = rtc.Repository(name=name, url=url, desc="")
                rtc_ = repo.clone(verbose=verbose)
                proj.update_rtc_repository(rtc_.repository, verbose=verbose)
                return 
                
            #for i in range(3, len(argv)):
            for name in argv[3:]:
                repo = wasanbon.core.rtc.get_repository(name)
                if repo:
                    rtc_ = repo.clone(verbose=verbose)
                    proj.update_rtc_repository(rtc_.repository, verbose=verbose)
            return

        elif argv[2] == 'delete':
            if len(argv) < 4:
                sys.stdout.write(' - Invalid Usage. Use --help option.\n')
                return
            for rtcname in argv[3:]:
                foundFlag = False
                rtc_ = proj.rtc(rtcname)
                if rtc_:
                    proj.delete_rtc(rtc_, verbose=verbose)
            return
                
            
        elif argv[2] == 'commit':
            if len(argv) < 5:
                sys.stdout.write(' - Invalid Usage. Use --help option.\n')
                return False

            rtc_ = proj.rtc(argv[3])
            if rtc_:
                rtc_.commit(comment=argv[4], verbose=verbose)
                proj.update_rtc_repository(rtc_.repository, verbose=verbose)
            return

        elif argv[2] == 'pull':
            if len(argv) < 4:
                sys.stdout.write(' - Invalid Usage. Use --help option.\n')
                return False
            rtc_ = proj.rtc(argv[3])
            rtc_.pull(verbose=verbose)
            return True

        elif argv[2] == 'checkout':
            if len(argv) < 4:
                sys.stdout.write(' - Invalid Usage. Use --help option.\n')
                return False
            rtc_ = proj.rtc(argv[3])
            if rtc_:
                rtc_.checkout(verbose=verbose)
            return True

        elif argv[2] == 'push':
            if len(argv) < 4:
                sys.stdout.write(' - Invalid Usage. Use --help option.\n')
                return
            rtc_ = proj.rtc(argv[3])
            if not rtc_:
                sys.stdout.write(' - RTC (%s) not found.\n' % argv[3])
            else:
                rtc_.push(verbose=verbose)
            return

        elif argv[2] == 'github_init':
            if len(argv) < 4:
                sys.stdout.write(' - Invalid Usage. Use --help option.\n')
                return

            rtc_ = proj.rtc(argv[3])
            if rtc_:
                sys.stdout.write(' - Initializing GIT repository in %s\n' % rtc_.name)
                sys.stdout.write(' - Username@github:')
                user = raw_input()
                passwd = getpass.getpass()
                proj.github_init(user, passwd, rtc_, verbose=verbose)
            else:
                sys.stdout.write(' - RTC (%s) not found.\n' % argv[3])
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


        sys.stdout.write(' - Invalid Command %s\n' % argv[2])
