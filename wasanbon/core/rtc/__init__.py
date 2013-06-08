import os, sys
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

def github_init(user, passwd, rtcp):
    rtc_dir = os.path.split(rtcp.getRTCProfileFileName())[0]
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

    rtc_dir = os.path.split(rtcp.getRTCProfileFileName())[0]
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
    subprocess.Popen(cmd, env=gitenv)
    os.chdir(current_dir)
    
    sys.stdout.write('Updating repository.yaml\n')
    repo_file = os.path.join(os.getcwd(), wasanbon.setting['application']['RTC_DIR'], 'repository.yaml')
    temp_file = os.path.join(os.getcwd(), wasanbon.setting['application']['RTC_DIR'], 'repository.yaml.bak')
    if os.path.isfile(temp_file):
        os.remove(temp_file)
    os.rename(repo_file, temp_file)
    repos = yaml.load(open(temp_file, 'r'))
    repos[repo_name] = 'git@github.com:' + user + '/' + repo_name + '.git'
    fout = open(repo_file, 'w')
    yaml.dump(repos, fout, encoding='utf8', allow_unicode=True)
    fout.close()


def install(rtcp):
    rtcc = RTCConf(wasanbon.setting['application']['conf.' + rtcp.getLanguage()])
    pp = PackageProfile(rtcp)
    if len(pp.getRTCFilePath()) == 0 :
        print '--Executable of RTC (%s) is not found.' % rtcp.getName()
        return

    [path_, file_] = os.path.split(pp.getRTCFilePath())
    if path_.startswith(os.getcwd()):
        path_ = path_[len(os.getcwd())+1:]

    if sys.platform == 'win32':
        path_ = path_.replace('\\', '\\\\')
    rtcc.append('manager.modules.load_path', path_)
    rtcc.append('manager.modules.preload', file_)
    rtcc.append('manager.components.precreate', rtcp.getName())
    rtcc.sync()
    
def uninstall_rtc(rtcp):
    rtcc = RTCConf(settings['application']['conf.' + rtcp.getLanguage()])
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

    if len(pp.getRTCFilePath()) == 0:
        filename = rtcp.getName() + fileext
        print '---Guessing RTCFileName = %s' % filename
    filename = os.path.basename(pp.getRTCFilePath())
    rtcc.remove('manager.components.precreate', rtcp.getName())
    rtcc.remove('manager.modules.preload', filename)
    rtcc.sync()
    

