import sys, os
import wasanbon
from wasanbon.core import package as pack

class Command(object):
    def __init__(self):
        pass

    def alternative(self):
        return ['register', 'git_init', 'github_init', 'commit', 'push', 'setting']

    def execute_with_argv(self, argv, force, verbose, clean):
        wasanbon.arg_check(argv,3)
        _package = pack.Package(os.getcwd())

        if argv[2] == 'register':
            sys.stdout.write(' @ Initializing Package in %s\n' % _package.name)
            _package.register(verbose=verbose)
            
        elif argv[2] == 'git_init':
            sys.stdout.write(' @ Initializing GIT repository in %s\n' % _package.name)
            _package.git_init(verbose=verbose)

        elif argv[2] == 'github_init':
            sys.stdout.write(' @ Initializing github.com repository in %s\n' % _package.name)
            user, passwd = wasanbon.user_pass()
            _package.github_init(user=user, passwd=passwd, verbose=verbose)

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

