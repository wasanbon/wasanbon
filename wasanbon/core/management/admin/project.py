import os, sys, optparse
import wasanbon
import wasanbon.core.project as prj
from  wasanbon.core.project import workspace

class Command(object):
    def __init__(self):
        pass
    
    def execute_with_argv(self, args, verbose, force, clean):

        usages  = wasanbon.get_help_text(['help', 'admin', 'description', 'project'])
        usage = "wasanbon-admin.py project [subcommand] ...\n\n"
        for line in usages:
            usage = usage + line + '\n'

        parser = optparse.OptionParser(usage=usage, add_help_option=False)
        parser.add_option('-l', '--long', help=wasanbon.get_help_text(['help', 'longformat']), action='store_true', default=False, dest='long_flag')
        try:
            options, argv = parser.parse_args(args[:])
        except:
            return

        if argv[2] == 'create':
            wasanbon.arg_check(argv, 4)
            sys.stdout.write(' @ Creating workspace %s\n' % argv[3])
            proj = prj.create_project(argv[3], verbose=verbose)

        elif argv[2] == 'unregister':
            wasanbon.arg_check(argv, 4)
            sys.stdout.write(' @ Removing workspace %s\n' % argv[3])
            dic = workspace.load_workspace()
            if not argv[3] in dic.keys():
                sys.stdout.write(' - Can not find project %s\n' % argv[3])
                return
            try:
                proj = prj.get_project(argv[3], verbose=verbose)
                proj.unregister(verbose=verbose, clean=clean)
            except wasanbon.ProjectNotFoundException, ex:
                sys.stdout.write(' - Project Not Found (%s).\n' % argv[3])
                from wasanbon import util
                if util.yes_no('Do you want to remove the record?') == 'yes':
                    dic = workspace.load_workspace()
                    dic.pop(argv[3])
                    workspace.save_workspace(dic)
                    sys.stdout.write(' - Removed.\n')


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
                print_repository(repo, long=options.long_flag)


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

def print_repository(repo, long=False):

    if long:
        sys.stdout.write(' - ' + repo.name + '\n')
        sys.stdout.write('    - description : ' + repo.description + '\n')
        sys.stdout.write('    - url         : ' + repo.url + '\n')

    else:
        sys.stdout.write(' - ' + repo.name + ' ' * (24-len(repo.name)) + ' : ' + repo.description + '\n')

def print_diff(diff):
    [plus, minus] = diff.rtcs
    sys.stdout.write(' - RTC\n')
    for rtc in plus:
        sys.stdout.write('  + %s\n' % rtc.name)
    for rtc in minus:
        sys.stdout.write('  - %s\n' % rtc.name)

