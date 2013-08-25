import os, sys
import wasanbon
import wasanbon.core.project as prj

class Command(object):
    def __init__(self):
        pass
    
    def execute_with_argv(self, argv, verbose, force, clean):

        if argv[2] == 'create':
            wasanbon.arg_check(argv, 4)
            sys.stdout.write(' @ Creating workspace %s\n' % argv[3])
            proj = prj.create_project(argv[3], verbose=verbose)

        elif argv[2] == 'unregister':
            wasanbon.arg_check(argv, 4)
            sys.stdout.write(' @ Removing workspace %s\n' % argv[3])
            proj = prj.get_project(argv[3], verbose=verbose)
            proj.unregister(verbose=verbose, clean=clean)

        elif argv[2] == 'list':
            sys.stdout.write(' @ Listing projects.\n')
            projs = prj.get_projects(verbose=verbose)
            for proj in projs:
                sys.stdout.write(' ' + proj.name + ' '*(10-len(proj.name)) + ':' + proj.path + '\n')

        elif argv[2] == 'directory':
            try:
                proj = prj.get_project(argv[3].strip())
                print proj.path
            except:
                print '.'

        elif argv[2] == 'repository':
            sys.stdout.write(' @ Listing Project Repositories\n')
            repos = prj.get_repositories(verbose=verbose)
            for repo in repos:
                sys.stdout.write(' ' + repo.name + ' ' * (24-len(repo.name)) + ' : ' + repo.description + '\n')

        elif argv[2] == 'clone':
            wasanbon.arg_check(argv,4)
            sys.stdout.write(' @ Cloning Project from Repository %s\n' % argv[3])
            repo = prj.get_repository(argv[3], verbose=verbose)
            proj = repo.clone(verbose=verbose)

        elif argv[2] == 'fork':
            wasanbon.arg_check(argv, 4)
            sys.stdout.write(' @ Forking Project from Repository %s\n' % argv[3])
            user, passwd = wasanbon.user_pass()
            original_repo = prj.get_repository(argv[3], verbose=verbose)
            repo = original_repo.fork(user, passwd, verbose=verbose)
            proj = repo.clone(verbose=verbose)

        elif argv[2] == 'diff':
            wasanbon.arg_check(argv, 5)
            sys.stdout.write(' @ Diff between %s and %s\n' % (argv[3], argv[4]))
            repo1 = prj.get_project(argv[3], verbose=verbose)
            repo2 = prj.get_project(argv[4], verbose=verbose)
            diff = prj.diff(repo1, repo2)
            print_diff(diff)

        else:
            raise wasanbon.InvalidUsageException()

        


def print_diff(diff):
    [plus, minus] = diff.rtcs
    sys.stdout.write(' - RTC\n')
    for rtc in plus:
        sys.stdout.write('  + %s\n' % rtc.name)
    for rtc in minus:
        sys.stdout.write('  - %s\n' % rtc.name)

