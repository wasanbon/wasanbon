import sys, os
import wasanbon
from wasanbon.core import rtm, tools
from wasanbon import lib, util

def print_repository(repo):
    sys.stdout.write(' - %s\n' % repo.name)
    sys.stdout.write('    description : %s\n' % repo.description)
    sys.stdout.write('    protocol    : %s\n' % repo.protocol)
    sys.stdout.write('    url         : %s\n' % repo.url)
    pass

class Command(object):
    def __init__(self):
        pass

    def is_admin(self):
        return True

    def execute_with_argv(self, argv, force=False, verbose=False, clean=False):
        wasanbon.arg_check(argv, 3)
        if argv[2] == 'repository':
            sys.stdout.write(' @ Listing Repositories.\n')
            repos = lib.get_repositories(verbose=verbose)
            for repo in repos:
                print_repository(repo)                

        elif argv[2] == 'install':
            wasanbon.arg_check(argv, 4)
            if argv[3] == 'RTno':
                tools.install_rtno(verbose=verbose, force=force)
                return 
            repo = lib.get_repository(argv[3], verbose=verbose)
            sys.stdout.write(' @ Installing %s\n' % argv[3])
            util.download_and_install(repo.url, force=force, verbose=verbose, open_only=True)
            
        else:
            raise wasanbon.InvalidUsageException()
