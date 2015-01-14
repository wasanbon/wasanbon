import os, sys, yaml, shutil, traceback, types, shutil
import wasanbon
from wasanbon import util
from wasanbon.util import git

owner_sign = '_owner'

default_repo_directory = os.path.join(wasanbon.rtm_home(), 'binder')

def create_local_repository(user, passwd, repo_name='wasanbon_binder', repo_dir=default_repo_directory, verbose=False, service='github'):
    if verbose:
        sys.stdout.write(' - Initializing Your Repository\n')
        pass

    if service=='github':
        import github_api
        target_path = os.path.join(repo_dir, user + owner_sign, repo_name + '.git')
        url = 'https://github.com/' + user + '/' + repo_name + '.git'
        #Check if repository exists...
        github_obj = github_api.GithubReference(user, passwd)
        if github_obj.exists_repo(repo_name):
            sys.stdout.write(' @ You have already created your own repository.\n')
            sys.stdout.write(' @ wasanbon just clone it.\n')
            download_repository(url=url, target_path=target_path, verbose=verbose)
            return True
        repo_obj = github_obj.fork_repo('sugarsweetrobotics', 
                                        'wasanbon_binder_template',
                                        repo_name, verbose=verbose)

    elif service=='bitbucket':
        import bitbucket_api
        target_path = os.path.join(repo_dir, user + owner_sign, repo_name + '.git')
        url = 'https://bitbucket.org/' + user + '/' + repo_name + '.git'
        _obj = bitbucket_api.BitbucketReference(user, passwd)
        if _obj.exists_repo(repo_name):
            sys.stdout.write(' @ You have already created your own repository.\n')
            sys.stdout.write(' @ wasanbon just clone it.\n')
            download_repository(url=url, target_path=target_path, verbose=verbose)
            return True
        repo_obj = _obj.fork_repo('sugarsweetrobotics', 
                                  'wasanbon_binder_template',
                                  repo_name, verbose=verbose)
    else:
        if verbose:
            sys.stdout.write(' @ Error. Unsupported Version Control Service Name %s.' % service)
        return False
    download_repository(url=url, target_path=target_path, verbose=verbose)
    return True


def destroy_local_repository(user, passwd, repo_name='wasanbon_binder', verbose=False, service='github', repo_dir=default_repo_directory):
    if service=='github':
        import github_api

        url = 'https://github.com/' + user + '/' + repo_name + '.git'
        #Check if repository exists...
        github_obj = github_api.GithubReference(user, passwd)
        if github_obj.exists_repo(repo_name):
            github_obj.delete_repo(repo_name)
        #else:
        #    return False

    target_path = os.path.join(repo_dir, user + owner_sign)
    sys.stdout.write(' -remove %s\n' % target_path)
    if not os.path.isdir(target_path):
        sys.stdout.write(' No local repository in %s\n' % target_path)
        return False
    
    shutil.rmtree(target_path)
    return True

def owner_repository_path(user, repo_name='wasanbon_binder'):
    _repository_path = repository_path()
    target_path = os.path.join(_repository_path, user + owner_sign, repo_name + '.git')
    return target_path

def is_local_owner_repository(user, repo_name='wasanbon_binder'):
    target_path = owner_repository_path(user, repo_name)
    return os.path.isdir(target_path)

def get_owner_repository_username_list(verbose=False):
    repo_dir = default_repo_directory
    owner_name_list = []
    for user in os.listdir(repo_dir):
        if user.endswith(owner_sign):
            owner_name_list.append(user[:-len(owner_sign)])
    return owner_name_list

def append_rtc_repo_to_owner(user, filename,  rtc_obj, repo_name='wasanbon_binder', verbose=False):
    if verbose:
        sys.stdout.write(' - Append RTC repository to owner repository to %s\n' % (filename))
    if not is_local_owner_repository(user):
        if verbose:
            sys.stdout.write(' @ Not found owner repository\n')
        return False
    target_path = os.path.join(owner_repository_path(user, repo_name), 'rtcs', filename)
    if not os.path.isfile(target_path):
        if verbose:
            sys.stdout.write(' @ Not found target repository file: %s\n' % target_path)
        return False

    y = yaml.load(open(target_path, 'r'))
    if type(y) == types.DictType:
        if rtc_obj.name in y.keys():
            sys.stdout.write(' @ Your own repository already have repository %s\n' % rtc_obj.name)
            return False
    shutil.copyfile(target_path, target_path + '.bak')
    fin = open(target_path+'.bak', 'r')
    fout = open(target_path, 'w')
    for line in fin:
        fout.write(line)
    
    repo = rtc_obj.repository
    name = rtc_obj.name
    description = rtc_obj.description
    _type = repo.protocol
    url = rtc_obj.repository.url
    platform = wasanbon.platform()
    import datetime
    now = datetime.datetime.now()
    
    fout.write('\n# Added in %s/%s/%s/%s:%s:%s\n' % \
                   (now.year, now.month, now.day, now.hour, now.minute, now.second))
    fout.write(name + ' : \n')
    fout.write('  description : \'' + description + '\'\n')
    fout.write('  type : ' + _type + '\n')
    fout.write('  url : \'' + url + '\'\n')
    fout.write('  platform : ' + platform + '\n')
    
    return True



def parse_rtc_repo_dir(repo_dir="", verbose=False):
    if len(repo_dir) == 0:
        repo_dir = default_repo_directory
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

def load_repositories(repo_dir=default_repo_directory, verbose=False, all_platform=False):
    rtc_repos = {}
    package_repos = {}

    for root, dirs, files in os.walk(repo_dir):
        try:
            if not 'setting.yaml' in files:
                continue

            setting_file = os.path.join(root, 'setting.yaml')
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
                            y = yaml.load(f)
                            if y:
                                rtc_repos = dict(rtc_repos, **y)
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
                            y = yaml.load(f)
                            if y:
                                package_repos = dict(package_repos, **y)
                    except Exception, ex:
                        if verbose:
                            traceback.print_exc()
                            pass
        except Exception, ex:
            traceback.print_exc()
            pass

    if not all_platform:
        for name, repo in rtc_repos.items():
            #if not 'platform' in repo.keys():
            #    filtered_rtc_repos[name] = repo
            #elif platform_check(repo['platform'], verbose=verbose):
            #    filtered_rtc_repos[name] = repo
            if 'platform' in repo.keys():
                if not platform_check(repo['platform'], verbose=verbose):
                    rtc_repos.pop(name, None)

        for name, repo in package_repos.items():
            #if not 'platform' in repo.keys():
            #    filtered_package_repos[name] = repo
            #elif platform_check(repo['platform'], verbose=verbose):
            #    filtered_package_repos[name] = repo
            if 'platform' in repo.keys():
                if not platform_check(repo['platform'], verbose=verbose):
                    package_repos.pop(name, None)

    #return filtered_rtc_repos, filtered_package_repos
    return (rtc_repos, package_repos)

def platform_check(args, verbose=False):
    for arg in args:
        if (wasanbon.platform().find(arg) >= 0):
            return True
    return False


def repository_path(url=None):
    root = default_repo_directory
    if url:
        root = os.path.join(root, url.split('/')[-2])
    return root

def download_repository(url, target_path='',verbose=False, force=False):
    _repository_path = repository_path(url)
    if not target_path:
        target_path = os.path.join(_repository_path, url.split('/')[-1])
    if verbose:
        sys.stdout.write('    - Downloading repository %s\n' % url)
        sys.stdout.write('        into %s\n' % target_path)

    if os.path.isdir(target_path):
        if os.path.isdir(os.path.join(target_path, '.git')):
            git.git_command(['pull'], verbose=True, path=target_path)
        else: # Directory exists but not git repository dir
            git.git_command(['clone', url, target_path], verbose=verbose)
        pass
    else:
        if not os.path.isdir(target_path):
            os.makedirs(target_path)
            pass
        git.git_command(['clone', url, target_path], verbose=verbose)
        pass

    if verbose:
        sys.stdout.write('    - Parsing child Binder\n')
    setting_file_path = os.path.join(target_path, 'setting.yaml')
    if os.path.isfile(setting_file_path):
        with open(setting_file_path, 'r') as setting_file:
            setting = yaml.load(setting_file)
            if type(setting) is types.DictType:
                child_repos = setting.get('child_binder', [])
                for repo in child_repos:
                    download_repository(repo, verbose=verbose, force=force)
    pass




def download_repositories(verbose=False, force=False, url=None):
    file_path = os.path.join(wasanbon.__path__[0], 'settings', 'repository.yaml')
    if verbose:
        sys.stdout.write(' - Downloading Repositories....\n')
        sys.stdout.write('    - Opening setting file in %s\n' % file_path)

    if url:
        download_repository(url, verbose=verbose, force=force)
        return True
    with open(file_path, 'r') as repo_setting:
        for name, value in yaml.load(repo_setting).items():
            if verbose:
                sys.stdout.write('    - Repository : %s\n' % name)
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
            target_path = os.path.join(wasanbon.rtm_home(), 'repositories', value['url'].split('/')[-2])
            if os.path.isdir(target_path):
                git.git_command(['commit', '-a', '-m', comment], verbose=True, path=target_path)
                git.git_command(['push'], verbose=True, path=target_path)
                pass
            else:
                sys.stdout.write(' - ERROR: Can not find Repository PATH.\n')
    pass


def append_package_repo_to_owner(user, filename,  package_obj, repo_name='wasanbon_binder', verbose=False):
    if verbose:
        sys.stdout.write(' - Append Package repository to owner repository\n')
    if not is_local_owner_repository(user):
        if verbose:
            sys.stdout.write(' @ Not found owner repository\n')
        return False
    target_path = os.path.join(owner_repository_path(user, repo_name), 'packages', filename)
    if not os.path.isfile(target_path):
        if verbose:
            sys.stdout.write(' @ Not found target repository file: %s\n' % target_path)
        return False

    y = yaml.load(open(target_path, 'r'))
    if type(y) is types.DictType:
        if package_obj.name in y.keys():
            if verbose:
                sys.stdout.write(' @ Your own repository already have repository %s\n' % package_obj.name)
            return False
    shutil.copyfile(target_path, target_path + '.bak')
    fin = open(target_path+'.bak', 'r')
    fout = open(target_path, 'w')
    for line in fin:
        fout.write(line)
    
    repo = package_obj.repository
    name = package_obj.name
    description = repo.description
    _type = repo.protocol
    url = package_obj.repository.url
    platform = wasanbon.platform()
    import datetime
    now = datetime.datetime.now()
    
    fout.write('\n# Added in %s/%s/%s/%s:%s:%s\n' % \
                   (now.year, now.month, now.day, now.hour, now.minute, now.second))
    fout.write(name + ' : \n')
    fout.write('  description : \'' + description + '\'\n')
    fout.write('  type : ' + _type + '\n')
    fout.write('  url : \'' + url + '\'\n')
    fout.write('  platform : ' + platform + '\n')
    
    return True

