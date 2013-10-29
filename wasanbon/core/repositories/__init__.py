import os, sys, yaml, shutil
import wasanbon
from wasanbon.util import git



def load_repositories(repo_dir=os.path.join(wasanbon.rtm_home, 'repositories'), verbose=False):
    rtc_repos = {}
    package_repos = {}

    for root, dirs, files in os.walk(repo_dir):

        try:
            if not 'setting.yaml' in files:
                continue

            setting_file = os.path.join(root, 'setting.yaml')
            if verbose:
                sys.stdout.write(' - Loading setting file.\n')
            repo_setting = yaml.load(open(setting_file, 'r'))
            repo_dirs = repo_setting['repositories'][wasanbon.platform]
            for repo_child_dir in repo_dirs:
                dirname = os.path.join(root, repo_child_dir)
                rtc_file_name = os.path.join(dirname, 'rtcs.yaml') 
                pack_file_name = os.path.join(dirname, 'packages.yaml') 
                if os.path.isfile(rtc_file_name):
                    with open(rtc_file_name, 'r') as rtc_file:
                        rtc_repos = dict(rtc_repos, **yaml.load(rtc_file))
                if os.path.isfile(pack_file_name):
                    with open(pack_file_name, 'r') as pack_file:
                        package_repos = dict(package_repos, **yaml.load(pack_file))

        except Exception, ex:
            print ex
            pass
    
    return rtc_repos, package_repos

def download_repositories(verbose=False, force=False):
    file_path = os.path.join(wasanbon.__path__[0], 'settings', 'repository.yaml')
    if verbose:
        sys.stdout.write(' - Downloading Repositories....\n')
        sys.stdout.write(' - Opening setting file in %s\n' % file_path)

    with open(file_path, 'r') as repo_setting:
        for name, value in yaml.load(repo_setting).items():
            if verbose:
                sys.stdout.write(' - Repository : %s\n' % name)
            repository_path = os.path.join(wasanbon.rtm_home, 'repositories', value['url'].split('/')[-2])
            target_path = os.path.join(repository_path, value['url'].split('/')[-1])
            if os.path.isdir(target_path):
                git.git_command(['pull'], verbose=True, path=target_path)
                pass
            else:
                if not os.path.isdir(target_path):
                    os.makedirs(target_path)
                git.git_command(['clone', value['url'], target_path], verbose=verbose)
                pass

    return True
                
def upload_repositories(comment, verbose=False):
    file_path = os.path.join(wasanbon.__path__[0], 'settings', 'repository.yaml')
    if verbose:
        sys.stdout.write(' - Uploading Repositories....\n')
        sys.stdout.write(' - Opening setting file in %s\n' % file_path)

    with open(file_path, 'r') as repo_setting:
        for name, value in yaml.load(repo_setting).items():
            if verbose:
                sys.stdout.write(' - Repository : %s\n' % name)
            target_path = os.path.join(wasanbon.rtm_home, 'repositories', value['url'].split('/')[-2])
            if os.path.isdir(target_path):
                git.git_command(['commit', '-a', '-m', comment], verbose=True, path=target_path)
                git.git_command(['push'], verbose=True, path=target_path)
                pass
            else:
                sys.stdout.write(' - ERROR: Can not find Repository PATH.\n')
    pass
