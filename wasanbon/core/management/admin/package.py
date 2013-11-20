import os, sys, optparse, getpass
import wasanbon
import wasanbon.core.package as pack
from  wasanbon.core.package import workspace
from wasanbon.core import repositories

class Command(object):
    def __init__(self):
        pass
    
    def execute_with_argv(self, args, verbose, force, clean):

        usages  = wasanbon.get_help_text(['help', 'admin', 'description', 'package'])
        usage = "wasanbon-admin.py package [subcommand] ...\n\n"
        for line in usages:
            usage = usage + line + '\n'

        parser = optparse.OptionParser(usage=usage, add_help_option=False)
        parser.add_option('-l', '--long', help=wasanbon.get_help_text(['help', 'longformat']), action='store_true', default=False, dest='long_flag')
        try:
            options, argv = parser.parse_args(args[:])
        except:
            return

        wasanbon.arg_check(argv, 3)

        if argv[2] == 'create':
            wasanbon.arg_check(argv, 4)
            sys.stdout.write(' @ Creating workspace %s\n' % argv[3])
            _package = pack.create_package(argv[3], verbose=verbose)

        elif argv[2] == 'unregister':
            wasanbon.arg_check(argv, 4)
            sys.stdout.write(' @ Removing workspace %s\n' % argv[3])
            dic = workspace.load_workspace()
            if not argv[3] in dic.keys():
                sys.stdout.write(' - Can not find package %s\n' % argv[3])
                return
            try:
                _package = pack.get_package(argv[3], verbose=verbose)
                _package.unregister(verbose=verbose, clean=clean)
            except wasanbon.PackageNotFoundException, ex:
                sys.stdout.write(' - Package Not Found (%s).\n' % argv[3])
                from wasanbon import util
                if util.yes_no('Do you want to remove the record?') == 'yes':
                    dic = workspace.load_workspace()
                    dic.pop(argv[3])
                    workspace.save_workspace(dic)
                    sys.stdout.write(' - Removed.\n')


        elif argv[2] == 'list':
            sys.stdout.write(' @ Listing packages.\n')
            _packages = pack.get_packages(verbose=verbose)
            for _package in _packages:
                sys.stdout.write(' ' + _package.name + ' '*(10-len(_package.name)) + ':' + _package.path + '\n')

        elif argv[2] == 'directory':
            try:
                _package = pack.get_package(argv[3].strip())
                print _package.path
            except:
                print '.'

        elif argv[2] == 'repository':

            if len(argv) == 3: # list
                argv.append('list')
                pass

            if argv[3] == 'list':
                sys.stdout.write(' @ Listing Package Repositories\n')
                repos = pack.get_repositories(verbose=verbose)
                for repo in repos:
                    print_repository(repo, long=options.long_flag)
            elif argv[3] == 'create':
                sys.stdout.write('  - Input Github User Name:')
                username = raw_input()
                #sys.stdout.write('  - Input Github Password :')
                passwd = getpass.getpass()
                sys.stdout.write('  - Input repository name :')
                repo_name = raw_input()
                repositories.create_local_repository(username, passwd, repo_name, verbose=verbose)
            elif argv[3] == 'update':
                sys.stdout.write(' @ Updating Package Repositories\n')
                pack.update_repositories(verbose=verbose)
            elif argv[3] == 'clone':
                wasanbon.arg_check(argv,5)
                sys.stdout.write(' @ Cloning Package Repositories\n')
                pack.update_repositories(verbose=verbose, url=argv[4])


        elif argv[2] == 'clone':
            wasanbon.arg_check(argv,4)
            sys.stdout.write(' @ Cloning Package from Repository %s\n' % argv[3])
            repo = pack.get_repository(argv[3], verbose=verbose)
            _package = repo.clone(verbose=verbose)

        elif argv[2] == 'fork':
            wasanbon.arg_check(argv, 4)
            sys.stdout.write(' @ Forking Package from Repository %s\n' % argv[3])
            user, passwd = wasanbon.user_pass()
            original_repo = pack.get_repository(argv[3], verbose=verbose)
            repo = original_repo.fork(user, passwd, verbose=verbose)
            _package = repo.clone(verbose=verbose)

        elif argv[2] == 'diff':
            wasanbon.arg_check(argv, 5)
            sys.stdout.write(' @ Diff between %s and %s\n' % (argv[3], argv[4]))
            repo1 = pack.get_package(argv[3], verbose=verbose)
            repo2 = pack.get_package(argv[4], verbose=verbose)
            diff = pack.diff(repo1, repo2)
            print_diff(diff)

        else:
            raise wasanbon.InvalidUsageException()

def print_repository(repo, long=False):

    if long:
        sys.stdout.write(' - ' + pack + '\n')
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

