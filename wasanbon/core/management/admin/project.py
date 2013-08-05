import os, sys, yaml, getpass, time
import wasanbon
#from wasanbon.core import template
#from wasanbon.core import rtc
#from wasanbon.core.rtc import git
#from wasanbon.core import system

from wasanbon.core import project

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
            proj = project.create_project(argv[3], verbose=verbose)
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
            proj = project.get_project(argv[3], verbose=verbose)
            if proj:
                proj.unregister(verbose=verbose, clean=clean)
            else:
                sys.stdout.write(' - %s project can not find\n' % argv[3])
            return

        elif argv[2] == 'list':
            print ' - Listing projects.'
            projs = project.get_projects(verbose=verbose)
            if not projs:
                sys.stdout.write(' - No project is found.\n')
                return 
            else:
                for proj in projs:
                    sys.stdout.write(' ' + proj.name + ' '*(10-len(proj.name)) + ':' + proj.path + '\n')
            return

        elif argv[2] == 'directory':
            projs = project.get_projects(False)
            if not projs:
                print '.'
            else:
                for proj in projs:
                    if proj.name == argv[3].strip():
                        print proj.path
                        return
                print '.'

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
                installed = system.list_installed_rtcs()
                if not y:
                    print ' - No repository'
                    return 
                for key in y.keys():
                    url = y[key]['git']
                    print ' - Cloning %s' % key
                    rtcp = git.clone(url, verbose=verbose)
                    git.checkout(rtcp, hash=y[key]['hash'], verbose=verbose)
                
                    print ' - Building %s' % key
                    cur = os.getcwd()
                    rtc.build_rtc(rtcp, verbose=verbose)
                    os.chdir(cur)
                    
                    if rtcp.basicInfo.name in installed[rtcp.language.kind]:
                        print ' - Reinstall %s' % key
                        rtc.install(rtcp, verbose=verbose, precreate=False, preload=False)
            else:
                print ' - No repository %s' % repo_name
            pass
        elif argv[2] == 'fork':
            if len(argv) < 4:
                print ' - Give Project Repository Name'
                return
            print ' - Forking Project from Repository'
            sys.stdout.write('Username@github:')
            user = raw_input()
            passwd = getpass.getpass()

            dir = wasanbon.setting[sys.platform]['projects']
            repo_name = argv[3]

            if repo_name in dir.keys():
                url = template.fork_project(repo_name, user, passwd, dir[repo_name]['git'], verbose=verbose)
                if not url:
                    print ' - Can not fork project'
                    return

                template.clone_project(repo_name, url, verbose=verbose)

                os.chdir(repo_name)
                reload(wasanbon)
                y = yaml.load(open('rtc/repository.yaml', 'r'))
                installed = system.list_installed_rtcs()

                if not y:
                    print ' - No repository'
                    return 
                for key in y.keys():
                    url = y[key]['git']
                    print ' - Cloning %s' % key
                    rtcp = git.clone(url, verbose=verbose)
                    git.checkout(rtcp, hash=y[key]['hash'], verbose=verbose)
                
                    print ' - Building %s' % key
                    cur = os.getcwd()
                    rtc.build_rtc(rtcp, verbose=verbose)
                    os.chdir(cur)
                    
                    if rtcp.basicInfo.name in installed[rtcp.language.kind]:
                        print ' - Reinstall %s' % key
                        rtc.install(rtcp, verbose=verbose, precreate=False, preload=False)
            else:
                print ' - No repository %s' % repo_name
            pass
