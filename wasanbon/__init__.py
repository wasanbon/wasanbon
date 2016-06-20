#!/usr/bin/env python
_version = '1.1.0-0'

import sys, os, locale, getpass, time #, yaml
import platform as plt
import types
import codecs, subprocess
import datetime
#from help import *

def get_version():
    """Get wasanbon version.
    """
    return _version


IDE = 'Visual Studio 12' if sys.platform == 'win32' else 'Makefile'
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)


class WasanbonException(Exception):
    def msg(self):
        return 'Wasanbon Exception'

class PrintAlternativeException(WasanbonException):
    def msg(self):
        return ''
class RemoteLoginException(WasanbonException):
    def msg(self):
        return 'LogIn Failed.'

class BuildSystemException(WasanbonException):
    def msg(self):
        return 'Build System Failed.'

class InvalidUsageException(WasanbonException):
    def msg(self):
        return 'Invalid Usage'

class InvalidMethodException(WasanbonException):
    def msg(self):
        return 'Invalid Method. This function is no longer supported.'

class UnsupportedLanguageException(WasanbonException):
    def msg(self):
        return 'Unsupported Language'

class UnsupportedPlatformException(WasanbonException):
    def __init__(self):
        pass

    def msg(self):
        return 'Unsupported Platform'

class DirectoryAlreadyExistsException(WasanbonException):
    def __init__(self):
        pass
    def msg(self):
        return 'Directory Already Exists.'

class PackageAlreadyExistsException(WasanbonException):
    def msg(self):
        return 'Package Already Exists'

class RepositoryNotFoundException(WasanbonException):
    def msg(self):
        return 'Local Repository Not Found'

class RepositoryAlreadyExistsException(WasanbonException):
    def msg(self):
        return 'Repository Already Exists'

class RTCNotFoundException(WasanbonException):
    def msg(self):
        return 'RTC Not Found'

class RTCBuildFailedException(WasanbonException):
    def msg(self):
        return 'RTC Build Failed'

class NotFoundException(WasanbonException):
    def msg(self):
        return 'RTC Not Found'

class InvalidPackagePathError(WasanbonException):
    def msg(self):
        return 'Invalid Package Path'

class RTCProfileNotFoundException(WasanbonException):
    def msg(self):
        return 'RTCProfile Not Found'

class PackageNotFoundException(WasanbonException):
    def msg(self):
        return 'Package Not Found'

class PluginDependencyNotResolvedException(WasanbonException):
    def msg(self):
        return 'Plugin Dependency can not be resolved.'

class NoSuchFileException(WasanbonException):
    def __init__(self, msg):
        self.msg = msg
    def msg(self):
        return 'No Such File :' + msg

class DownloadFailedException(WasanbonException):
    def msg(self):
        return 'Download Failed'

class InvalidArgumentException(WasanbonException):
    def msg(self):
        return 'Invalid Argument'

def arg_check(argv, num):
    if len(argv) < num:
        raise InvalidUsageException()
    pass

def arg_is_long(argv):
    if '-l' in argv:
        argv.remove('-l')
        return True
    if '--long' in argv:
        argv.remove('--long')
        return True

def get_bin_file_ext():
    if sys.platform == 'win32':
        return '.dll'
    elif sys.platform == 'linux2':
        return '.so'
    elif sys.platform == 'darwin':
        return '.dylib'
    else:
        print '---Unsupported System (%s)' % sys.platform
        raise UnsupportedPlatformException()
    
def user_pass(user=None, passwd=None):
    if not user:
        sys.stdout.write('username:')
        user = raw_input()
    if not passwd:
        passwd = getpass.getpass()
    return (user, passwd)

def timestampstr():
    return datetime.datetime.now().strftime('%Y%m%d%H%M%S')


def get_home_path():
    if sys.platform == 'darwin':
        return os.environ['HOME'] 
    elif sys.platform == 'win32':
        return os.path.join(os.environ['HOMEDRIVE'] , os.environ['HOMEPATH'])
    elif sys.platform == 'linux2':
        return os.environ['HOME'] 
    else:
        print 'Unsupported System %s' % sys.platform
    return ''

tagdict = {'$HOME': get_home_path()}

WASANBON_HOME_ENVKEY = 'WASANBON_HOME'
WASANBON_HOME_DEFAULT = os.path.join(get_home_path(), '.wasanbon')

def get_wasanbon_home():
    env = os.environ
    if WASANBON_HOME_ENVKEY in env.keys():
        return env[WASANBON_HOME_ENVKEY]
    
    return WASANBON_HOME_DEFAULT
    
home_path = get_wasanbon_home()
temp_path = os.path.join(home_path, 'temp')
plugins_path = os.path.join(home_path, 'plugins')
register_file = os.path.join(home_path, 'register.yaml')

username = None
if sys.platform == 'darwin' or sys.platform == 'linux2':
    username = os.environ['USER']
    if username == 'root': # might be launched with sudo
        username = os.environ.get('SUDO_USER', None)

if not os.path.isdir(home_path):
    os.mkdir(home_path)
if not os.path.isdir(temp_path):
    os.mkdir(temp_path)
if not os.path.isdir(plugins_path):
    os.mkdir(plugins_path)
_admin_path = os.path.join(plugins_path, 'admin')
_mgr_path = os.path.join(plugins_path, 'mgr')
if not os.path.isdir(_admin_path):
    os.mkdir(_admin_path)
if not os.path.isdir(_mgr_path):
    os.mkdir(_mgr_path)

if username:
    import pwd
    uid = pwd.getpwnam(username).pw_uid
    gid = pwd.getpwnam(username).pw_gid
    os.chown(home_path, uid, gid)
    os.chown(temp_path, uid, gid)
    os.chown(plugins_path, uid, gid)
    os.chown(_admin_path, uid, gid)
    os.chown(_mgr_path, uid, gid)
        


rtm_temp = ""
rtm_home = ""

def load_settings():
    global rtm_root, rtm_home

    root_dir = os.path.join(__path__[0], 'settings')
    setting = __load_subdir(root_dir)

    pathdict = setting['common']['path']
    if sys.platform == 'win32':
        for key in pathdict.keys():
            pathdict[key] = pathdict[key].replace('/', '\\')

    old_len = len(tagdict)
    while True:
        for key in pathdict:
            pathdict[key] = __replace_tag(pathdict[key])
        __update_tagdict(pathdict)
        if len(tagdict) == old_len:
            break
        old_len = len(tagdict)
    
    __replace_tag_recursive(setting)

    return setting

def __update_tagdict(hash):
    for key in hash.keys():
        if hash[key].find('$') < 0:
            tagdict['$'+key] = hash[key]

def __replace_tag_recursive(hash):
    if type(hash) is types.DictType:
        for key in hash.keys():
            hash[key] = __replace_tag_recursive(hash[key])
        return hash
    elif type(hash) is types.ListType:
        new_hash = []
        for v in hash:
            new_hash.append(__replace_tag_recursive(v))
        return new_hash
    else:
        return __replace_tag(hash)

def __replace_tag(str):
    global tagdict
    for tag in tagdict.keys():
        str = str.replace(tag, tagdict[tag])
    return str

def __parse_yaml(hash):
    for key in hash.keys():
        val = hash[key]
        if type(val) is types.DictType:
            hash[key] = __parse_yaml(val)
        elif type(val) is types.StringType:
            hash[key] = __replace_tags(val)
    return hash

def __load_yaml(file):
    __import__('yaml')
    yaml = sys.modules['yaml']
    dict = yaml.load(open(file, 'r'))
    if type(dict) == types.NoneType:
        return {}
    return dict
    
def __load_subdir(root):
    ret = {}
    for dir in os.listdir(root):
        path = os.path.join(root, dir)
        if os.path.isdir(path):
            ret[dir] = __load_subdir(path)
        elif os.path.isfile(path):
            if dir.endswith('yaml'):
                ret[dir[:len(dir)-5]] = __load_yaml(path)
    return ret


#def __load_repositories():
#    return dict(setting['common']['repository'], **setting[platform]['repository'])

__setting = []
def setting():
    global __setting
    if not __setting:
        __setting =  load_settings()
        __local_setting_file = os.path.join(rtm_home(), 'setting.yaml')
        if os.path.isfile(__local_setting_file):
            __setting['local'] = __load_yaml(__local_setting_file)

        __application_setting_file = os.path.join(os.getcwd(), 'setting.yaml')
        if os.path.isfile(__application_setting_file):
            appsetting = __load_yaml(__application_setting_file)
            if 'application' in appsetting.keys():
                __setting['application'] = appsetting['application']
    return __setting

def rtm_home():
    raise InvalidMethodException()
    #return setting()['common']['path']['RTM_HOME']

#if not os.path.isdir(rtm_home):
#    os.makedirs(rtm_home)

def rtm_temp():
    raise InvalidMethodException()
    #return setting()['common']['path']['RTM_TEMP']


def rtm_plugins():
    raise InvalidMethodException()
    #return setting()['common']['path']['RTM_PLUGINS']


#rtm_temp = setting['common']['path']['RTM_TEMP']
#if not os.path.isdir(rtm_temp):
#    os.makedirs(rtm_temp)

#repositories = __load_repositories()


#__local_repository_file = os.path.join(rtm_home, 'repository.yaml')
#if os.path.isfile(__local_repository_file):
#    setting['local_repo'] = yaml.load(open(__local_repository_file, 'r'))
#    if type(setting['local_repo']) != types.NoneType:
#        repositories = dict(repositories, **setting['local_repo'])


#if 'application' in setting.keys():
#    __application_repository_file = os.path.join(os.getcwd(), setting['application']['RTC_DIR'], 'repository.yaml')
#    if os.path.isfile(__application_repository_file):
#        app_repo = yaml.load(open(__application_repository_file, 'r'))
#        if type(app_repo) != types.NoneType:
#            setting['app_repo'] = app_repo
#            repositories = dict(repositories, **setting['app_repo'])

def xcode_check():
    p = subprocess.Popen(['gcc', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    line = p.stdout.read()
    if line.find('darwin14'):
        return 'xcode6'
    elif line.find('darwin13'):
        return 'xcode5'
    elif line.find('darwin12'):
        return 'xcode4'
    else:
        raise UnsupportedPlatformException()


def platform():
    if sys.platform == 'darwin':
        import platform as plt
        ver = plt.mac_ver()[0]
        if ver.startswith('10.11'):
            _platform = 'osx10.11_' + xcode_check()
        elif ver.startswith('10.10'):
            _platform = 'osx10.10_' + xcode_check()
        elif ver.startswith('10.9'):
            _platform = 'osx10.9_' + xcode_check()
        elif ver.startswith('10.8'):
            _platform = 'osx10.8_' + xcode_check()
        elif ver.startswith('10.7'):
            _platform = 'osx10.7_' + xcode_check()
        else:
            raise wasanbon.UnsupportedPlatformException()
    elif sys.platform == 'win32':
        if sys.getwindowsversion()[1] == 1:
            _platform = 'windows7'
        elif sys.getwindowsversion()[1] == 2:
            _platform = 'windows8'
            
        if os.environ['PROCESSOR_ARCHITEW6432'] == 'AMD64':
            _platform = _platform + '_x64'
        else:
            _platform = _platform + '_x86'
            
    elif sys.platform == 'linux2':
        import platform as plt
        distri = plt.linux_distribution()
        
        if distri[0] == 'Ubuntu':
            _platform = 'ubuntu'
        elif distri[0] == 'debian':
            _platform = 'debian'

            
        #if distri[1] == '12.04':
        #    _platform = _platform + '1204'
            
        if plt.architecture()[0] == '32bit':
            _platform = _platform + '_x86'
        else:
            _platform = _platform + '_x64'
            
    return _platform

import wasanbon.core.plugins
plugins = wasanbon.core.plugins.Loader([plugins_path, wasanbon.core.plugins.__path__[0]])


def sleep(interval, verbose=True):
    times = int(interval * 5)
    #sys.stdout.write(' - Waiting approx. %s seconds\n' % interval)
    for t in range(times):
        percent = float(t) / times
        width = 30
        progress = (int(width*percent)+1)
        sys.stdout.write('\r# [' + '#'*progress + ' '*(width-progress) + ']')
        sys.stdout.flush()
        time.sleep(0.2)

    sys.stdout.write('\n')
    
def get_rtm_root():
    if 'RTM_ROOT' in os.environ.keys():
        return os.environ['RTM_ROOT']
    else:
        for hint in rtm_root_hints:
            if os.path.isfile(os.path.join(hint, 'rtm', 'version.txt')):
                return hint
        return ""
