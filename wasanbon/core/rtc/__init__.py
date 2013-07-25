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
    repo = github_obj.get_user(target_user).get_repo(target_repo[:-4])
    
    github_obj.get_user().create_fork(repo)
    sys.stdout.write('Please wait for 5 seconds to fork...\n')
    time.sleep(5)
    for i in range(0, 5):
        try:
            r = github_obj.get_user().get_repo(target_repo[:-4])
            my_url = 'git@github.com:' + user + '/' + target_repo[:-4]
            sys.stdout.write(' - Success.')
            return my_url
        except:
            sys.stdout.write('Please wait for 1 seconds to fork...\n')
            time.sleep(1)
            pass
    sys.stdout.write(' - Failed to create fork.\n')
    return None

def delete(rtcp, verbose=False):
    rtc_dir = os.path.split(rtcp.filename)[0]
    sys.stdout.write(' - Deleting RTC directory:%s' % rtc_dir)
    if util.no_yes(' OK?') == 'yes':
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

def update_repositoy_yaml(repo_name, url, desc="", erbose=False):
    sys.stdout.write(' - Updating repository.yaml\n')
    repo_file = os.path.join(os.getcwd(), wasanbon.setting['application']['RTC_DIR'], 'repository.yaml')
    temp_file = os.path.join(os.getcwd(), wasanbon.setting['application']['RTC_DIR'], 'repository.yaml.bak')
    if os.path.isfile(temp_file):
        os.remove(temp_file)
    os.rename(repo_file, temp_file)
    repos = yaml.load(open(temp_file, 'r'))
    repos[repo_name] = {}
    repos[repo_name]['description'] = desc
    repos[repo_name]['git'] = url
    fout = open(repo_file, 'w')
    yaml.dump(repos, fout, encoding='utf8', allow_unicode=True)
    fout.close()


def install(rtcp):
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
    rtcc.append('manager.modules.preload', file_)
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
    

