"""
RTC's repository control

$ mgr.py repository [subcommand] YOUR_RTC_NAME ...

subcommands:
 - list   : List RTC repositories.

 - clone  : Clone RTC source code from RTC repository.
  ex., $ mgr.py repository clone YOUR_RTC_REPOSITORY
            This command allows to clone from specific url as well.
  ex., $ mgr.py repository clone YOUR_RTC_URL
 - fork   : Fork RTC source code from RTC repository to your remote repository.
  ex., $ mgr.py repository fork YOUR_RTC_REPOSITORY
            You will asked your remote repository address (Currently github only).

 - init   : Create local repository in your RTC code directory (current git only)
  ex., $ mgr.py repository init YOUR_RTC_NAME
            This command create .git directory in rtc/YOUR_RTC_DIR/
 - fini   : Remove local repository of your RTC
  ex., $ mgr.py repository fini YOUR_RTC_NAME
            This command just remove .git directory in rtc/YOUR_RTC_DIR/

 - remote_add : Add remote repository as upstream repository
  ex., $ mgr.py repository remote_add YOUR_RTC_NAME UPSTREAM_URL
 - remote_del : Delete remote repository link
  ex., $ mgr.py repository remote_del YOUR_RTC_NAME
 - remote_create : Create remote repository in your remote service (currently, github only)
  ex., $ mgr.py repository remote_create YOUR_RTC_NAME [ github | bitbucket ]

 - commit : Commit change to local repository.
 - push   : Push local commits to upstream repository.
 - pull   : Pull from upstream repository to local repository.


"""

import os, sys, optparse
import wasanbon

from wasanbon.core import rtc
from wasanbon.core import package


def alternative(argv=None):
    return_rtc_cmds = ['init', 'fini', 'remote_add', 'remote_del', 'remote_create', 'commit', 'pull', 'push']
    return_repo_cmds = ['clone', 'fork']
    all_cmds = ['list'] + return_rtc_cmds + return_repo_cmds
    if argv and len(argv) >= 3:
        if argv[2] in return_rtc_cmds:
            return [rtc.name for rtc in package.Package(os.getcwd()).rtcs]
        elif argv[2] in return_repo_cmds:
            return [repo.name for repo in wasanbon.core.rtc.get_repositories()]

    return all_cmds

def get_rtc_rtno( _package, name, verbose=False):
    try:
        return _package.rtc(name)
    except wasanbon.RTCNotFoundException, e:
        return tools.get_rtno_package(_package, name, verbose=verbose)

def execute_with_argv(args, verbose, force=False, clean=False):
    usage = "mgr.py repository [subcommand] ...\n"
    parser = optparse.OptionParser(usage=usage, add_help_option=False)
    parser.add_option('-l', '--long', help='show status in long format', action='store_true', default=False, dest='long_flag')
    parser.add_option('-s', '--service', help='set upstream service',  default='github', metavar='SERVICE', dest='service')
    try:
        options, argv = parser.parse_args(args[:])
    except:
        return

    wasanbon.arg_check(argv, 3)
    _package = package.Package(os.getcwd())

    if argv[2] == 'list':
        sys.stdout.write(' @ Listing RTC Repository\n')
        for repo in wasanbon.core.rtc.get_repositories(verbose):
            print_repository(repo, long=options.long_flag)

    elif argv[2] == 'init':
        wasanbon.arg_check(argv, 4)
        sys.stdout.write(' @ Initializing RTC %s as GIT repository\n' % argv[3])
        rtc_ = get_rtc_rtno(_package, argv[3], verbose=verbose)
        rtc_.git_init(verbose=verbose)
        
    elif argv[2] == 'remote_create':
        wasanbon.arg_check(argv, 4)
        sys.stdout.write(' @ Initializing github.com repository in %s\n' % argv[3])
        user, passwd = wasanbon.user_pass()

        rtc_ = get_rtc_rtno(_package, argv[3], verbose=verbose)
        #rtc_.github_init(user, passwd, verbose=verbose)
        if options.service == 'github':
            rtc.github_init(user, passwd, rtc_, verbose=verbose)
        elif options.service == 'bitbucket':
            sys.stdout.write(' - bitbucket service is selected.\n')
            rtc.bitbucket_init(user, passwd, rtc_, verbose=verbose)
        else:
            raise wasanbon.InvalidUsageException()
        sys.stdout.write(' @ Updating repository infomation\n')
        _package.append_rtc_repository(rtc_.repository)
        
    elif argv[2] == 'fork':
        wasanbon.arg_check(argv, 4)
        sys.stdout.write(' @ Forking GITHUB repository in %s\n' % argv[3])
        user, passwd = wasanbon.user_pass()
        original_repo = wasanbon.core.rtc.get_repository(argv[3])
        repo = original_repo.fork(user, passwd, verbose=verbose, path=_package.rtc_path)
        sys.stdout.write(' @ Cloning GITHUB repository in %s\n' % argv[3])            
        rtc_ = repo.clone(verbose=verbose, path=_package.rtc_path)
        _package.update_rtc_repository(repo, verbose=verbose)

    elif argv[2] == 'github_pullrequest':
        wasanbon.arg_check(argv, 6)
        sys.stdout.write(' @ Sending Pullrequest.\n')
        user, passwd = wasanbon.user_pass()
        rtc_ = _package.rtc(argv[3])
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
            try:
                rtc_ = wasanbon.core.rtc.RtcRepository(name=name, url=url, desc="").clone(verbose=verbose, path=_package.rtc_path)
            except wasanbon.RTCProfileNotFoundException, e:
                rtc_ = get_rtc_rtno(_package, name, verbose=verbose)
                    
            _package.update_rtc_repository(rtc_.repository, verbose=verbose)
            return
                
        #for i in range(3, len(argv)):
        for name in argv[3:]:
            sys.stdout.write(' @ Cloning RTC %s\n' % name)
            try:
                rtc_ = wasanbon.core.rtc.get_repository(name).clone(verbose=verbose, path=_package.rtc_path)
            except wasanbon.RTCProfileNotFoundException, e:
                rtc_ = get_rtc_rtno(_package, name, verbose=verbose)

            _package.update_rtc_repository(rtc_.repository, verbose=verbose)

    elif argv[2] == 'checkout':
        wasanbon.arg_check(argv, 4)
        sys.stdout.write(' @ Checkout and overwrite  RTC %s\n' % argv[3])
        get_rtc_rtno(_package, argv[3], verbose=verbose).checkout(verbose=verbose)


def print_repository(repo, long=False):
    sys.stdout.write(' - %s\n' % repo.name)
    if long:
        sys.stdout.write('    description : %s\n' % repo.description)
        sys.stdout.write('    protocol    : %s\n' % repo.protocol)
        sys.stdout.write('    url         : %s\n' % repo.url)
    pass

            
