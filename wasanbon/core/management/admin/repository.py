"""
Repository Control.

If you want to check the repository status, use:
  $ wasanbon-admin.py repository status

If you do not have any repositories in your system, use:
  $ wasanbon-admin.py repository setup

If you have your own repository, use:
  $ wasanbon-admin.py repository install YOUR_OWN_REPOSITORY_URL

To update, use:
  $ wasanbon-admin.py repository update
"""

import sys, os, yaml, getpass, types
import wasanbon
from wasanbon.core import repositories
#from wasanbon.core import package as pack
from wasanbon.util import editor, git

def get_repo_name(path):
    return os.path.basename(os.path.split(path)[0])

def alternative(argv=None):
    return ['setup', 'status', 'update', 'install', 'create', 'edit', 'commit', 'push']

def execute_with_argv(argv, force=False, verbose=False, clean=False):
    wasanbon.arg_check(argv, 3)
        
    if '-l' in argv:
        longformat = True
    else:
        longformat = False
    argv = [arg for arg in argv if not arg is '-l']
          
    if argv[2] == 'setup':
        sys.stdout.write(' - Downloading Repositories.\n')
        if not repositories.download_repositories(verbose=True):
            sys.stdout.write(' - Downloading Failed.\n')
            return
        return

    elif argv[2] == 'status':
        sys.stdout.write(' - Checking Repositories.\n')
        paths = repositories.parse_rtc_repo_dir()

        if len(paths) == 0:
            sys.stdout.write(' @ No repository is downloaded. Do wasanbon-admin.py repository setup\n')
            return
        
        for path in paths:
            owner_name = os.path.basename(os.path.dirname(path))
            if owner_name.endswith(repositories.owner_sign):
                owner_name = owner_name[:-len(repositories.owner_sign)]
            sys.stdout.write('  - Repository : %s/%s\n' 
                             % (owner_name, os.path.basename(path)))
            rtcs_dir = os.path.join(path, 'rtcs')
            if os.path.isdir(rtcs_dir):
                sys.stdout.write('   - rtcs : \n')
                for file in os.listdir(rtcs_dir):
                    if file.endswith('.yaml'):
                        sys.stdout.write('     - %s:\n' % file)
                        if longformat:
                            y = yaml.load(open(os.path.join(rtcs_dir, file), 'r'))
                            if type(y) == types.DictType:
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
                            if type(y) == types.DictType:
                                keys = y.keys()
                                keys.sort()
                                for key in keys:
                                    sys.stdout.write('      @ ' + key 
                                                     + ' '*(15-len(key))
                                                     + ': ' + y[key]['description'] + '\n')
    elif argv[2] == 'install':
        if len(argv) == 3:
            sys.stdout.write(' @ Need more argument. See help.\n')
        else:
            __import__('wasanbon.core.package')
            pack = sys.modules['wasanbon.core.package']
            sys.stdout.write(' @ Cloning Package Repositories\n')
            pack.update_repositories(verbose=verbose, url=argv[3])

    elif argv[2] == 'update':
        pack.update_repositories(verbose=verbose)

    elif argv[2] == 'commit':
        wasanbon.arg_check(argv, 4)
        paths = repositories.parse_rtc_repo_dir()
        for path in paths:
            owner_name = os.path.basename(os.path.dirname(path))
            if owner_name.endswith(repositories.owner_sign):
                git.git_command(['commit', '-a', '-m', argv[3]], path=path, verbose=verbose)
                return

    elif argv[2] == 'push':
        paths = repositories.parse_rtc_repo_dir()
        for path in paths:
            owner_name = os.path.basename(os.path.dirname(path))
            if owner_name.endswith(repositories.owner_sign):
                git.git_command(['push'], path=path, verbose=verbose)
                return
        
    elif argv[2] == 'create':
        sys.stdout.write(' - Input Github User Name:')
        username = raw_input()
        passwd = getpass.getpass()
        sys.stdout.write(' - Creating wasanbon_repositories in your github\n')
        repositories.create_local_repository(username, passwd, verbose=verbose)

    elif argv[2] == 'edit':
        paths = repositories.parse_rtc_repo_dir()
        for path in paths:
            owner_name = os.path.basename(os.path.dirname(path))
            if owner_name.endswith(repositories.owner_sign):
                editor.edit_dirs([os.path.join(path, 'rtcs'), os.path.join(path, 'packages')])
                return
