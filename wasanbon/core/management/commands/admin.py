# coding: utf-8
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

ja_JP:
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
import sys, os, optparse, traceback

import wasanbon
from wasanbon import util
from wasanbon.core import repositories
from wasanbon.core import package as pack


def alternative(argv=None):
    
    return ['git_init', 'remote_create', 'commit', 'push']


def execute_with_argv(argv, verbose=False, clean=False):
    usage = "mgr.py admin [subcommand] ...\n"
    parser = optparse.OptionParser(usage=usage, add_help_option=False)
    parser.add_option('-l', '--long', help='show status in long format', action='store_true', default=False, dest='long_flag')
    parser.add_option('-s', '--service', help='set upstream service',  default='github', metavar='SERVICE', dest='service')
    try:
        options, argv = parser.parse_args(argv[:])
    except:
        raise wasanbon.InvalidUsageException()

    service_name = options.service

    wasanbon.arg_check(argv,3)
    _package = pack.Package(os.getcwd())
    

    if argv[2] == 'git_init':
        sys.stdout.write(' @ Initializing GIT repository in %s\n' % _package.name)
        _package.git_init(verbose=verbose)
        
    elif argv[2] == 'remote_create':
        sys.stdout.write(' @ Initializing %s repository in %s\n' % (service_name, _package.name))
        user, passwd = wasanbon.user_pass()
        if service_name == 'github':
            #_package.github_init(user=user, passwd=passwd, verbose=verbose)
            pack.github_init(_package, user, passwd, verbose=verbose)
        elif service_name == 'bitbucket':
            pack.bitbucket_init(_package, user=user, passwd=passwd, verbose=verbose)
        owner_add(_package, verbose=False)

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
    else:
        raise wasanbon.InvalidUsageException()

def owner_add(_package, verbose=False):
    from wasanbon.core import repositories
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
    pack_path = os.path.join(owner_path, 'packages')
    files = [f for f in os.listdir(pack_path) if f.endswith('.yaml')] + ['Create new file']
    def callback(n):
        file = files[n]
        if n == len(files)-1:
            # Create new file
            file = raw_input(' - filename?:')
            if file:
                try:
                    open(os.path.join(pack_path, file), 'w').close()
                except:
                    sys.stdout.write(' @ Create file failed.\n')
                    return False
        if not repositories.append_package_repo_to_owner(user, file, _package, verbose=verbose):
            sys.stdout.write(' @ Failed to save repository data to file.\n')
            sys.stdout.write(' @ If you need to add the Package to your own repository, try ...\n$ mgr.py admin owner_add \n')
            return True
        return True
            
    util.choice(files, callback, msg=' - Choice file to save Package repo.')

