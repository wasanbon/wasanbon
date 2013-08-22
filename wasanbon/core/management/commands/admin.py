import sys, os
import wasanbon
from wasanbon.core import project as prj

class Command(object):
    def __init__(self):
        pass

    def execute_with_argv(self, argv, force, verbose, clean):
        wasanbon.arg_check(argv,3)
        proj = prj.Project(os.getcwd())

        if argv[2] == 'register':
            sys.stdout.write(' @ Initializing Project in %s\n' % proj.name)
            proj.register(verbose=verbose)
            
        elif argv[2] == 'git_init':
            sys.stdout.write(' @ Initializing GIT repository in %s\n' % proj.name)
            proj.git_init(verbose=verbose)

        elif argv[2] == 'github_init':
            sys.stdout.write(' @ Initializing github.com repository in %s\n' % proj.name)
            user, passwd = wasanbon.user_pass()
            proj.github_init(user=user, passwd=passwd, verbose=verbose)

        elif argv[2] == 'commit':
            wasanbon.arg_check(argv, 4)
            proj.commit(argv[3], verbose=verbose)

        elif argv[2] == 'push':
            proj.push(verbose=verbose)
        elif argv[2] == 'setting':
            keylist = proj.setting.keys()[:]
            keylist.sort()
            for key in keylist:
                sys.stdout.write(' %s :\n' % key)
                sys.stdout.write('   %s\n' % proj.setting[key])
        else:
            raise wasanbon.InvalidUsageException()

