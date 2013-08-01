import os, sys, shutil, time
import wasanbon
from wasanbon import util
from search_rtc import *
from build_rtc import *
from packageprofile import *
from rtcprofile import *
from rtcconf import *
import github


def parse_rtcs():
    rtc_dir = os.path.join(os.getcwd(), 
                           wasanbon.setting['application']['RTC_DIR'])
    rtcprofiles = util.search_file(rtc_dir, 'RTC.xml')
    rtcps = []
    for fullpath in rtcprofiles:
        try:
            rtcp = RTCProfile(fullpath)
            rtcps.append(rtcp)
        except Exception, e:
            print str(e)
            print '-Error Invalid RTCProfile file[%s]' % fullpath
    return rtcps

def github_pullrequest(user, passwd, url, title, body, verbose=False):
    sys.stdout.write(' - Creating Pull Request ')
    github_obj = github.Github(user, passwd)
    git_user = github_obj.get_user()
    try:
        git_user.login
    except:
        print ' - Login Error.'
        return None
    target_user, target_repo = url.split('/')[-2:]
    repo = github_obj.get_user().get_repo(target_repo[:-4])

    owner_url = repo.parent.url
    owner_user, owner_repo = owner_url.split('/')[-2:]
    sys.stdout.write(' (from: %s:%s to %s:%s)\n' % (user, target_repo[:-4], owner_user, target_repo[:-4]))
    parent_repo = github_obj.get_user(owner_user).get_repo(owner_repo)
    parent_repo.create_pull(title=title, body=body, head=user + ':master', base='master')
    return True

def github_fork(user, passwd, url, verbose=False):
    sys.stdout.write(' - Forking URL:: %s\n' % url)
    github_obj = github.Github(user, passwd)
    git_user = github_obj.get_user()
    try:
        git_user.login
    except:
        print ' - Login Error.'
        return None
    target_user, target_repo = url.split('/')[-2:]
    try:
        my_repo = github_obj.get_user().get_repo(target_repo[:-4])
        print ' - Your repository already has the %s repository' % target_repo[:-4]
        print ' - This will be cloned into your space.'
        return 'git@github.com:' + user + '/' + target_repo
    except:
        print ' - Your repository does not have the %s repository' % target_repo[:-4]

        
    repo = github_obj.get_user(target_user).get_repo(target_repo[:-4])

    print ' - Now creating fork of the %s repository' % target_repo[:-4]
    github_obj.get_user().create_fork(repo)
    sys.stdout.write(' - Please wait for 5 seconds to fork...\n')
    time.sleep(5)
    for i in range(0, 5):
        try:
            r = github_obj.get_user().get_repo(target_repo[:-4])
            sys.stdout.write(' - Success\n')
            my_url = 'git@github.com:' + user + '/' + target_repo
            return my_url
        except:
            sys.stdout.write(' - Please wait for 1 more seconds to fork...\n')
            time.sleep(1)
            pass
    sys.stdout.write(' - Failed to create fork.\n')
    return None

def delete(rtcp, verbose=False, force=False):
    rtc_dir = os.path.split(rtcp.filename)[0]

    if not force:
        sys.stdout.write(' - Deleting RTC directory:%s' % rtc_dir)
        if util.no_yes(' OK?') == 'yes':
            force = True

    if force:
        if verbose:
            sys.stdout.write(' - Deleting RTC directory %s' % rtc_dir)
        shutil.rmtree(rtc_dir, ignore_errors=True)
    pass

def github_init(user, passwd, rtcp, verbose=False):
    rtc_dir = os.path.split(rtcp.filename)[0]
    if rtc_dir.endswith('/'): 
        rtc_dir = rtc_dir[:-1]
    repo_name = os.path.basename(rtc_dir)

    github_obj = github.Github(user, passwd)
    git_user = github_obj.get_user()
    try:
        git_user.login
    except:
        print ' - Login Error.'
        return
    github_obj.get_user().create_repo(repo_name)

    rtc_dir = os.path.split(rtcp.filename)[0]
    sys.stdout.write("Connect to GITHUB repository of %s\n" % repo_name)
    current_dir = os.getcwd()
    os.chdir(rtc_dir)

    gitenv = os.environ.copy()
    if not 'HOME' in gitenv.keys():
        gitenv['HOME'] = wasanbon.get_home_path()
    print 'HOME is %s' % gitenv['HOME']

    cmd = [wasanbon.setting['local']['git'], 'remote', 'add', 'origin', 'git@github.com:' + user + '/' + repo_name + '.git']
    subprocess.call(cmd, env=gitenv)
    cmd = [wasanbon.setting['local']['git'], 'push', '-u', 'origin', 'master']
    subprocess.call(cmd, env=gitenv)
    os.chdir(current_dir)

    url = 'git@github.com:' + user + '/' + repo_name + '.git'
    update_repository_yaml(repo_name, url)

def update_repository_yaml(repo_name, url="", protocol="git",  desc="", hash="", verbose=False):
    if verbose:
        sys.stdout.write(' - Updating repository.yaml\n')
    repo_file = os.path.join(os.getcwd(), wasanbon.setting['application']['RTC_DIR'], 'repository.yaml')
    temp_file = os.path.join(os.getcwd(), wasanbon.setting['application']['RTC_DIR'], 'repository.yaml.bak')
    if os.path.isfile(temp_file):
        os.remove(temp_file)
    os.rename(repo_file, temp_file)
    repos = yaml.load(open(temp_file, 'r'))
    if not repos:
        repos = {}
    if verbose:
        sys.stdout.write(' - Adding %s repository\n' % repo_name)
    if url == "":
        url = repos[repo_name][protocol]
    repos[repo_name] = {}
    repos[repo_name]['description'] = desc
    repos[repo_name][protocol] = url
    repos[repo_name]['hash'] = hash
    fout = open(repo_file, 'w')
    yaml.dump(repos, fout, encoding='utf8', allow_unicode=True)
    fout.close()

def delete_repository_yaml(repo_name, verbose=False):
    if verbose:
        sys.stdout.write(' - Updating repository.yaml\n')
    repo_file = os.path.join(os.getcwd(), wasanbon.setting['application']['RTC_DIR'], 'repository.yaml')
    temp_file = os.path.join(os.getcwd(), wasanbon.setting['application']['RTC_DIR'], 'repository.yaml.bak')
    if os.path.isfile(temp_file):
        os.remove(temp_file)
    os.rename(repo_file, temp_file)
    repos = yaml.load(open(temp_file, 'r'))
    if not repos:
        repos = {}
    if repo_name in repos.keys():
        if verbose:
            sys.stdout.write(' - Removing %s repository\n' % repo_name)
        repos.pop(repo_name)
    fout = open(repo_file, 'w')
    yaml.dump(repos, fout, encoding='utf8', allow_unicode=True)
    fout.close()
    

def install(rtcp, verbose=False, precreate=True, preload=True):
    rtcc = RTCConf(wasanbon.setting['application']['conf.' + rtcp.language.kind])
    pp = PackageProfile(rtcp)
    if len(pp.getRTCFilePath()) == 0 :
        print '--Executable of RTC (%s) is not found.' % rtcp.basicInfo.name
        return

    [path_, file_] = os.path.split(pp.getRTCFilePath())
    if path_.startswith(os.getcwd()):
        path_ = path_[len(os.getcwd())+1:]

    if sys.platform == 'win32':
        path_ = path_.replace('\\', '\\\\')
    rtcc.append('manager.modules.load_path', path_)
    if preload:
        rtcc.append('manager.modules.preload', file_)
    if precreate:
        rtcc.append('manager.components.precreate', rtcp.basicInfo.name)
    rtcc.sync()
    
def uninstall(rtcp):
    rtcc = RTCConf(wasanbon.setting['application']['conf.' + rtcp.language.kind])
    pp = PackageProfile(rtcp)
    
    if sys.platform == 'win32':
        fileext = '.dll'
    elif sys.platform == 'linux2':
        fileext = '.so'
    elif sys.platform == 'darwin':
        fileext = '.dylib'
    else:
        print '---Unsupported System (%s)' % sys.platform
        return 

    filename = rtcp.basicInfo.name + fileext
    # filename = os.path.basename(pp.getRTCFilePath())
    rtcc.remove('manager.components.precreate', rtcp.basicInfo.name)
    rtcc.remove('manager.modules.preload', filename)
    rtcc.sync()
    

