import sys, os, yaml
import wasanbon
from wasanbon.core import repositories
from wasanbon.core import package as pack
class Command(object):
    def __init__(self):
        pass

    def is_admin(self):
        return True

    def execute_with_argv(self, argv, force=False, verbose=False, clean=False):
        wasanbon.arg_check(argv, 3)
        
        if '-l' in argv:
            longformat = True
        else:
            longformat = False

        if argv[2] == 'status':
            sys.stdout.write(' - Checking Repositories.\n')
            paths = repositories.parse_rtc_repo_dir()
            for path in paths:
                sys.stdout.write('  - Repository : %s\n' % (path))
                rtcs_dir = os.path.join(path, 'rtcs')
                if os.path.isdir(rtcs_dir):
                    sys.stdout.write('   - rtcs : \n')
                    for file in os.listdir(rtcs_dir):
                        if file.endswith('.yaml'):
                            sys.stdout.write('     - %s:\n' % file)
                            if longformat:
                                y = yaml.load(open(os.path.join(rtcs_dir, file), 'r'))
                                keys = y.keys()
                                keys.sort()
                                for key in keys:
                                    sys.stdout.write('      @ ' + key 
                                                + ' '*(15-len(key))
                                                + ': ' + y[key]['description'] + '\n')
                packs_dir = os.path.join(path, 'packages')
                if os.path.isdir(packs_dir):
                    sys.stdout.write('   - packages : \n')
                    for file in os.listdir(packs_dir):
                        if file.endswith('.yaml'):
                            sys.stdout.write('     - %s:\n' % file)
                            if longformat:
                                y = yaml.load(open(os.path.join(packs_dir, file), 'r'))
                                keys = y.keys()
                                keys.sort()
                                for key in keys:
                                    sys.stdout.write('      @ ' + key 
                                                + ' '*(15-len(key))
                                                + ': ' + y[key]['description'] + '\n')
        elif argv[2] == 'install':
            wasanbon.arg_check(argv,4)
            sys.stdout.write(' @ Cloning Package Repositories\n')
            pack.update_repositories(verbose=verbose, url=argv[3])

        elif argv[2] == 'update':
            pack.update_repositories(verbose=verbose)
        
        
                    
