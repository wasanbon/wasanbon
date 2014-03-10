"""
en_US:
 brief : |
  Local Package administration
 description : |
  Package Administration mainly for version controlling like git.

 subcommands : 
  git_init : |
Initialize git repository for your package
  remote_create : |
Create remote repository in your remote service (github|bitbucket).
eg., $ mgr.py admin remote_create -s [github|bitbucket]
  commit : |
Commit changes in your package into the local version control
  push : |
Push your commits to your remote repository
    
"""


import sys, os
import wasanbon
from wasanbon.core import repositories
from wasanbon.core import package as pack


def alternative(argv=None):
    
    return ['git_init', 'remote_create', 'commit', 'push']


def execute_with_argv(argv, force, verbose=False, clean=False):
    usage = "mgr.py admin [subcommand] ...\n"
    parser = optparse.OptionParser(usage=usage, add_help_option=False)
    parser.add_option('-l', '--long', help='show status in long format', action='store_true', default=False, dest='long_flag')
    parser.add_option('-s', '--service', help='set upstream service',  default='github', metavar='SERVICE', dest='service')
    try:
        options, argv = parser.parse_args(args[:])
    except:
        return

    service_name = options.service

    wasanbon.arg_check(argv,3)
    _package = pack.Package(os.getcwd())
    
    if argv[2] == 'git_init':
        sys.stdout.write(' @ Initializing GIT repository in %s\n' % _package.name)
        _package.git_init(verbose=verbose)
        
    elif argv[2] == 'add':
        sys.stdout.write(' @ Initializing github.com repository in %s\n' % _package.name)
        user, passwd = wasanbon.user_pass()
        if service_name == 'github':
            #_package.github_init(user=user, passwd=passwd, verbose=verbose)
            pack.github_init(_package, user, passwd, verbose=verbose)
        elif service_name == 'bitbucket':
            pack.bitbucket_init(_package, user=user, passwd=passwd, verbose=verbose)
        if repositories.is_local_owner_repository():
            
            pass

    elif argv[2] == 'commit':
        wasanbon.arg_check(argv, 4)
        _package.commit(argv[3], verbose=verbose)

    elif argv[2] == 'push':
        _package.push(verbose=verbose)
    elif argv[2] == 'setting':
        keylist = _package.setting.keys()[:]
        keylist.sort()
        for key in keylist:
            sys.stdout.write(' %s :\n' % key)
            sys.stdout.write('   %s\n' % _package.setting[key])

    raise wasanbon.InvalidUsageException()

