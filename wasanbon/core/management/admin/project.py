import os, sys, yaml
import wasanbon
from wasanbon.core import template
from wasanbon.core import rtc
from wasanbon.core.rtc import git

class Command(object):
    def __init__(self):
        pass
    
    def execute_with_argv(self, argv, verbose, force, clean):
        if len(argv) < 3:
            print ' - To read help, "%s project -h"' % os.path.basename(argv[0])
            return

        if argv[2] == 'create':

            if len(argv) < 4:
                print ' - To read help, "%s project -h"' % os.path.basename(argv[0])
                return
            print ' - Creating workspace %s:' % argv[3]
            template.create_project(argv[3], verbose=verbose)

        elif argv[2] == 'list':
            print ' - Listing projects.'
            projs = template.get_projects(verbose)
            if not projs:
                print '\n No project is found.'
            else:
                for key, item in projs.items():
                    print ' ' + key + ' '*(10-len(key)) + ':' + item
            print ''

        elif argv[2] == 'directory':
            projs = template.get_projects(False)
            if not projs:
                print '.'
            else:
                for key, item in projs.items():
                    if key.strip() == argv[3].strip():
                        print item
                        return
                print '.'

        elif argv[2] == 'unregister':
            if len(argv) < 4:
                print ' - To read help, "%s project -h"' % os.path.basename(argv[0])
                return
            template.unregister_project(argv[3], verbose=verbose, clean=clean)

        elif argv[2] == 'repository':
            print ' - Listing Project Repository'
            dir = wasanbon.setting[sys.platform]['projects']
            for key, value in dir.items():
                print ' ' + key + ' ' * (24-len(key)) + ' : ' + value['description']
            pass

        elif argv[2] == 'clone':
            if len(argv) < 4:
                print ' - Give Project Repository Name'
                return
            print ' - Cloning Project from Repository'
            dir = wasanbon.setting[sys.platform]['projects']
            repo_name = argv[3]

            if repo_name in dir.keys():
                template.clone_project(repo_name, dir[repo_name]['git'], verbose=verbose)
                os.chdir(repo_name)
                reload(wasanbon)

                y = yaml.load(open('rtc/repository.yaml', 'r'))
                if not y:
                    print ' - No repository'
                    return 
                for key in y.keys():
                    url = y[key]['git']
                    print ' - Cloning %s' % key
                    rtcp = git.clone(url, verbose=verbose)
                    git.checkout(rtcp, hash=y[key]['hash'], verbose=verbose)
                
                    print ' - Building %s' % key
                    rtc.build_rtc(rtcp, verbose=verbose)
            else:
                print ' - No repository %s' % repo_name
            pass
