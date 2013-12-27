import os, sys, yaml, shutil, traceback, types, github
import wasanbon
from wasanbon import util
from wasanbon.util import git, github_ref

owner_sign = '_owner'

def create_local_repository(user, passwd, repo_name='wasanbon_repositories', repo_dir=os.path.join(wasanbon.rtm_home, 'repositories'), verbose=False):
    if verbose:
        sys.stdout.write(' - Initializing Your Repository\n')
        pass
    target_path = os.path.join(repo_dir, user + owner_sign, repo_name + '.git')
    url = 'https://github.com/' + user + '/' + repo_name + '.git'
    #Check if repository exists...
    github_obj = github_ref.GithubReference(user, passwd)
    if github_obj.exists_repo(repo_name):
        sys.stdout.write(' @ You have already created your own repository.\n')
        sys.stdout.write(' @ wasanbon just clone it.\n')
        download_repository(url=url, target_path=target_path, verbose=verbose)
        return True
    repo_obj = github_obj.fork_repo('sugarsweetrobotics', 
                                    'wasanbon_repositories_template')
    repo_obj.edit(repo_name)
    download_repository(url=url, target_path=target_path, verbose=verbose)

def parse_rtc_repo_dir(repo_dir="", verbose=False):
    if len(repo_dir) == 0:
        repo_dir = os.path.join(wasanbon.rtm_home, 'repositories')
        pass
    paths = []
    for root, dirs, files in os.walk(repo_dir):
        try:
            if not 'setting.yaml' in files:
                continue
            setting_file = os.path.join(root, 'setting.yaml')
            paths.append(root)
        except:
            traceback.print_exc()
    return paths

def load_repositories(repo_dir=os.path.join(wasanbon.rtm_home, 'repositories'), verbose=False):
    rtc_repos = {}
    package_repos = {}

    for root, dirs, files in os.walk(repo_dir):
        try:
            if not 'setting.yaml' in files:
                continue

            setting_file = os.path.join(root, 'setting.yaml')

            """
            if verbose:
                sys.stdout.write(' - Loading setting file (%s)\n' % os.path.join(root, 'setting.yaml'))
            repo_setting = yaml.load(open(setting_file, 'r'))
            try:
                repo_dirs = repo_setting['repositories'][wasanbon.platform]
            except KeyError, ex:
                sys.stdout.write(' @ Error: repository(%s) does not have repository list for %s\n' % (os.path.join(root, 'setting.yaml'), wasanbon.platform))
                continue
                pass
            """
            if verbose:
                sys.stdout.write(' - Loading setting file (%s)\n' % os.path.join(root, 'setting.yaml'))
            repo_setting = yaml.load(open(setting_file, 'r'))

            # process repo_setting file
            
            rtcs_dir = os.path.join(root, 'rtcs')
            if os.path.isdir(rtcs_dir):
                for file in os.listdir(rtcs_dir):
                    if not file.endswith('.yaml'):
                        continue

                    try:
                        with open(os.path.join(rtcs_dir, file), 'r') as f:
                            rtc_repos = dict(rtc_repos, **yaml.load(f))
                    except Exception, ex:
                        if verbose:
                            traceback.print_exc()
                            pass
                        
            pack_dir = os.path.join(root, 'packages')
            if os.path.isdir(pack_dir):
                for file in os.listdir(pack_dir):
                    if not file.endswith('.yaml'):
                        continue
                    try:
                        with open(os.path.join(pack_dir, file), 'r') as f:
                            package_repos = dict(package_repos, **yaml.load(f))
                    except Exception, ex:
                        if verbose:
                            traceback.print_exc()
                            pass
        except Exception, ex:
            traceback.print_exc()
            pass

    filtered_rtc_repos = {}
    for name, repo in rtc_repos.items():
        if not 'platform' in repo.keys():
            filtered_rtc_repos[name] = repo
        elif platform_check(repo['platform'], verbose=verbose):
            filtered_rtc_repos[name] = repo

    filtered_package_repos = {}
    for name, repo in package_repos.items():
        if not 'platform' in repo.keys():
            filtered_package_repos[name] = repo
        elif platform_check(repo['platform'], verbose=verbose):
            filtered_package_repos[name] = repo
    
    return filtered_rtc_repos, filtered_package_repos

def platform_check(args, verbose=False):
    flg = False
    for arg in args:
        flg = flg or (wasanbon.platform.find(arg) >= 0)
    return flg

def download_repository(url, target_path='',verbose=False, force=False):
    if verbose:
        sys.stdout.write(' - Downloading repository %s into %s\n' % (url, target_path))
    repository_path = os.path.join(wasanbon.rtm_home, 'repositories', url.split('/')[-2])
    if not target_path:
        target_path = os.path.join(repository_path, url.split('/')[-1])
        if verbose:
            sys.stdout.write(' - Downloading repository %s into %s\n' % (url, target_path))

    if os.path.isdir(target_path):
        git.git_command(['pull'], verbose=True, path=target_path)
        pass
    else:
        if not os.path.isdir(target_path):
            os.makedirs(target_path)
            pass
        git.git_command(['clone', url, target_path], verbose=verbose)
        pass

    if verbose:
        sys.stdout.write(' - Parsing child repositories\n')
    setting_file_path = os.path.join(target_path, 'setting.yaml')
    if os.path.isfile(setting_file_path):
        with open(setting_file_path, 'r') as setting_file:
            setting = yaml.load(setting_file)
            if type(setting) is types.DictType:
                child_repos = setting.get('child_repositories', [])
                for repo in child_repos:
                    download_repository(repo, verbose=verbose, force=force)
                    
    pass

def download_repositories(verbose=False, force=False, url=None):
    file_path = os.path.join(wasanbon.__path__[0], 'settings', 'repository.yaml')
    if verbose:
        sys.stdout.write(' - Downloading Repositories....\n')
        sys.stdout.write(' - Opening setting file in %s\n' % file_path)

    if url:
        download_repository(url, verbose=verbose, force=force)
        return True
    with open(file_path, 'r') as repo_setting:
        for name, value in yaml.load(repo_setting).items():
            if verbose:
                sys.stdout.write(' - Repository : %s\n' % name)
            download_repository(value['url'], verbose=verbose, force=force)

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
