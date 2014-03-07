"""
en_US:
 brief : |
  RTC's repository control
 description : |

 subcommands:
  list   : List RTC repositories.
  init   : |
   Create local repository in your RTC code directory (current git only)
   ex., $ mgr.py repository init YOUR_RTC_NAME
   This command create .git directory in rtc/YOUR_RTC_DIR/
  fini   : |
   Remove local repository of your RTC
   ex., $ mgr.py repository fini YOUR_RTC_NAME
   This command just remove .git directory in rtc/YOUR_RTC_DIR/
  remote_add : |
   Add remote repository as upstream repository
   ex., $ mgr.py repository remote_add YOUR_RTC_NAME UPSTREAM_URL
  remote_del : |
   Delete remote repository link
   ex., $ mgr.py repository remote_del YOUR_RTC_NAME
  remote_create : |
   Create remote repository in your remote service (currently, github only)
   ex., $ mgr.py repository remote_create YOUR_RTC_NAME [ github | bitbucket ]
  owner_add : |
   Add repository information to your local repository file.
   This command will edit your own local repository file maybe stored in ~/rtm/repositories/*_owner/
   ex., $ mgr.py repository owner_add YOUR_RTC_NAME
  commit : Commit change to local repository.
  push   : Push local commits to upstream repository.
  pull   : Pull from upstream repository to local repository.
"""

import os, sys, optparse
import wasanbon

from wasanbon import util
from wasanbon.core import rtc, package



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
        owner_add(_package, argv[3])
        

    elif argv[2] == 'owner_add':
        owner_add(_package, argv[3])

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



def owner_add(_package, rtc_name, verbose=False):
    from wasanbon.core import repositories
    rtc_obj = _package.rtc(rtc_name)
    users = repositories.get_owner_repository_username_list(verbose=True)
    if len(users) == 1:
        user = users[0]
    else:
        user = raw_input(' - Input User Name:')
    sys.stdout.write(' - Saving to repository data to your own repository.\n')
    if not repositories.is_local_owner_repository(user):
        sys.stdout.write(' @ Can not find your own repository.\n')
        sys.stdout.write(' @ Check by repository command.\n')
        return False
    owner_path = repositories.owner_repository_path(user)
    rtc_path = os.path.join(owner_path, 'rtcs')
    files = [f for f in os.listdir(rtc_path) if f.endswith('.yaml')] + ['Create new file']
    def callback(n):
        file = files[n]
        if n == len(files)-1:
            # Create new file
            file = raw_input(' - filename?:')
            if file:
                try:
                    open(os.path.join(rtc_path, file), 'w').close()
                except:
                    sys.stdout.write(' @ Create file failed.\n')
                    return False
        if not repositories.append_rtc_repo_to_owner(user, file, rtc_obj, verbose=verbose):
            sys.stdout.write(' @ Failed to save repository data to file.\n')
            sys.stdout.write(' @ If you need to add the RTC to your own repository, try ...\n$ mgr.py repository owner_add YOUR_RTC_NAME\n')
            return True
        return True
            
    util.choice(files, callback, msg=' - Choice file to save rtc repo.')


def print_repository(repo, long=False):
    sys.stdout.write(' - %s\n' % repo.name)
    if long:
        sys.stdout.write('    description : %s\n' % repo.description)
        sys.stdout.write('    protocol    : %s\n' % repo.protocol)
        sys.stdout.write('    url         : %s\n' % repo.url)
    pass

            
