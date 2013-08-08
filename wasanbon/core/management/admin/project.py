import os, sys, yaml, getpass, time
import wasanbon
#from wasanbon.core import template
#from wasanbon.core import rtc
#from wasanbon.core.rtc import git
#from wasanbon.core import system

import wasanbon.core.project as prj

class Command(object):
    def __init__(self):
        pass
    
    def execute_with_argv(self, argv, verbose, force, clean):

        if argv[2] == 'create':
            if len(argv) < 4:
                print ' - To read help, "%s project -h"' % os.path.basename(argv[0])
                return
            print ' - Creating workspace %s:' % argv[3]
            proj = prj.create_project(argv[3], verbose=verbose)
            if proj:
                print ' - Success'
            else:
                print ' - Failed.'
            return

        elif argv[2] == 'unregister':
            if len(argv) < 4:
                print ' - To read help, "%s project -h"' % os.path.basename(argv[0])
                return
            print ' - Removing workspace %s:' % argv[3]
            proj = prj.get_project(argv[3], verbose=verbose)
            if proj:
                proj.unregister(verbose=verbose, clean=clean)
            else:
                sys.stdout.write(' - %s project can not find\n' % argv[3])
            return

        elif argv[2] == 'list':
            print ' - Listing projects.'
            projs = prj.get_projects(verbose=verbose)
            if not projs:
                sys.stdout.write(' - No project is found.\n')
                return 
            else:
                for proj in projs:
                    sys.stdout.write(' ' + proj.name + ' '*(10-len(proj.name)) + ':' + proj.path + '\n')
            return

        elif argv[2] == 'directory':
            projs = prj.get_projects(False)
            if not projs:
                print '.'
            else:
                for proj in projs:
                    if proj.name == argv[3].strip():
                        print proj.path
                        return
                print '.'

        elif argv[2] == 'repository':
            print ' - Listing Project Repositories'
            repos = prj.get_repositories(verbose=verbose)
            for repo in repos:
                print ' ' + repo.name + ' ' * (24-len(repo.name)) + ' : ' + repo.description
            return

        elif argv[2] == 'clone':
            if len(argv) < 4:
                print ' - Give Project Repository Name'
                return
            print ' - Cloning Project from Repository'
            repo = prj.get_repository(argv[3], verbose=verbose)
            proj = repo.clone(verbose=verbose)
            return

        elif argv[2] == 'fork':
            if len(argv) < 4:
                print ' - Give Project Repository Name'
                return
            print ' - Forking Project from Repository'
            sys.stdout.write('Username@github:')
            user = raw_input()
            passwd = getpass.getpass()
            
            original_repo = prj.get_repository(argv[3], verbose=verbose)
            repo = original_repo.fork(user, passwd, verbose=verbose)
            proj = repo.clone(verbose=verbose)
            

