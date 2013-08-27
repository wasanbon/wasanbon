#!/usr/bin/env python

import os, sys
import wasanbon
from wasanbon.core import project as prj
from wasanbon.util import editor
from wasanbon import util


class Command(object):
    def __init__(self):
        pass

    def execute_with_argv(self, argv, verbose, force, clean):
        wasanbon.arg_check(argv, 3)
        proj = prj.Project(os.getcwd())

        if argv[2] == 'list':
            sys.stdout.write(' @ Listing RTCs in current project\n')
            for rtc in proj.rtcs:
                print_rtc(rtc)

        elif argv[2] == 'repository':
            sys.stdout.write(' @ Listing RTC Repository\n')
            for repo in wasanbon.core.rtc.get_repositories(verbose):
                print_repository(repo)

        elif argv[2] == 'git_init':
            wasanbon.arg_check(argv, 4)
            sys.stdout.write(' @ Initializing RTC %s as GIT repository\n' % argv[3])
            proj.rtc(argv[3]).git_init(verbose=verbose)

        elif argv[2] == 'github_init':
            wasanbon.arg_check(argv, 4)
            sys.stdout.write(' @ Initializing github.com repository in %s\n' % argv[3])
            user, passwd = wasanbon.user_pass()
            rtc_ = proj.rtc(argv[3]).github_init(user, passwd, verbose=verbose)
            sys.stdout.write(' @ Updating repository infomation\n')
            proj.append_rtc_repository(rtc_.repository)

        elif argv[2] == 'github_fork':
            wasanbon.arg_check(argv, 4)
            sys.stdout.write(' @ Forking GITHUB repository in %s\n' % argv[3])
            user, passwd = wasanbon.user_pass()
            original_repo = wasanbon.core.rtc.get_repository(argv[3])
            repo = original_repo.fork(user, passwd, verbose=verbose, path=proj.rtc_path)
            sys.stdout.write(' @ Cloning GITHUB repository in %s\n' % argv[3])            
            rtc_ = repo.clone(verbose=verbose, path=proj.rtc_path)
            proj.update_rtc_repository(repo, verbose=verbose)

        elif argv[2] == 'github_pullrequest':
            wasanbon.arg_check(argv, 6)
            sys.stdout.write(' @ Sending Pullrequest.\n')
            user, passwd = wasanbon.user_pass()
            rtc_ = proj.rtc(argv[3])
            rtc_.github_pullrequest(user, passwd, argv[4], argv[5], verbose=verbose)
            
        elif argv[2] == 'clone':
            wasanbon.arg_check(argv, 4)

            # if argument is url, then, clone by git command
            if argv[3].startswith('git@') or argv[3].startswith('http'):
                url = argv[3]
                name = os.path.basename(url)
                if name.endswith('.git'):
                    name = name[:-4]
                sys.stdout.write(' @ Cloning RTC %s\n' % argv[3])
                rtc_ = wasanbon.core.rtc.RtcRepository(name=name, url=url, desc="").clone(verbose=verbose, path=proj.rtc_path)
                proj.update_rtc_repository(rtc_.repository, verbose=verbose)
                return
                
            #for i in range(3, len(argv)):
            for name in argv[3:]:
                sys.stdout.write(' @ Cloning RTC %s\n' % name)
                rtc_ = wasanbon.core.rtc.get_repository(name).clone(verbose=verbose, path=proj.rtc_path)
                proj.update_rtc_repository(rtc_.repository, verbose=verbose)

        elif argv[2] == 'delete':
            wasanbon.arg_check(argv, 4)
            sys.stdout.write(' @ Deleting RTC %s\n' % argv[3])
            for rtcname in argv[3:]:
                proj.delete_rtc(proj.rtc(rtcname), verbose=verbose)
            
        elif argv[2] == 'commit':
            wasanbon.arg_check(argv, 5)
            sys.stdout.write(' @ Commiting Changes of RTC %s\n' % argv[3])
            rtc_ = proj.rtc(argv[3]).commit(comment=argv[4], verbose=verbose)
            proj.update_rtc_repository(rtc_.repository, verbose=verbose)

        elif argv[2] == 'pull':
            wasanbon.arg_check(argv, 4)
            sys.stdout.write(' @ Pulling the changing upstream RTC repository %s\n' % argv[3])
            rtc_ =proj.rtc(argv[3]).pull(verbose=verbose)
            proj.update_rtc_repository(rtc_.repository, verbose=verbose)

        elif argv[2] == 'checkout':
            wasanbon.arg_check(argv, 4)
            sys.stdout.write(' @ Checkout and overwrite  RTC %s\n' % argv[3])
            proj.rtc(argv[3]).checkout(verbose=verbose)

        elif argv[2] == 'push':
            wasanbon.arg_check(argv, 4)
            sys.stdout.write(' @ Pushing RTC repository  %s to upstream.\n' % argv[3])
            proj.rtc(argv[3]).push(verbose=True) # when pushing always must be verbose 

        elif argv[2] == 'clean':
            wasanbon.arg_check(argv, 4)
            build_all = True if 'all' in argv else False
            for rtc in proj.rtcs:
                if build_all or rtc.name in argv:
                    sys.stdout.write(' @ Cleaning Up RTC %s\n' % rtc.name)
                    rtc.clean(verbose=verbose)

        elif argv[2] == 'build':
            wasanbon.arg_check(argv, 4)
            build_all = True if 'all' in argv else False

            if sys.platform == 'win32':
                verbose=True

            for rtc in proj.rtcs:
                if build_all or rtc.name in argv:
                    sys.stdout.write(' @ Building RTC %s\n' % rtc.name)
                    rtc.build(verbose=verbose)

        elif argv[2] == 'edit':
            wasanbon.arg_check(argv, 4)
            rtc_ = proj.rtc(argv[3])
            if rtc_.is_git_repo():
                if rtc_.git_branch() != 'master':
                    sys.stdout.write(' @ You are not in master branch.\n')
                    if util.yes_no(' @ Do you want to checkout master first?') == 'yes':
                        rtc_.checkout(verbose=verbose)
            editor.edit_rtc(proj.rtc(argv[3]), verbose=verbose)

        else:
            raise wasanbon.InvalidUsageException()

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
