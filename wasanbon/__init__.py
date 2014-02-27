#!/usr/bin/env python

import sys, os, locale, getpass, yaml
import platform as plt
import types
import codecs, subprocess
from help import *

def get_version():
    """Get wasanbon version.
    """
    return "0.8.0"


sys.stdout = codecs.getwriter('utf-8')(sys.stdout)


class WasanbonException(Exception):
    def msg(self):
        return 'Wasanbon Exception'

class GithubLogingException(WasanbonException):
    def msg(self):
        return 'LogIn Failed.'

class BuildSystemException(WasanbonException):
    def msg(self):
        return 'Build System Failed.'

class InvalidUsageException(WasanbonException):
    def msg(self):
        return 'Invalid Usage'

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
        return 'Repository Not Found'

class RepositoryAlreadyExistsException(WasanbonException):
    def msg(self):
        return 'Repository Already Exists'

class RTCNotFoundException(WasanbonException):
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

class NoSuchFileException(WasanbonException):
    def __init__(self, msg):
        self.msg = msg
    def msg(self):
        return 'No Such File :' + msg

class DownloadFailedException(WasanbonException):
    def msg(self):
        return 'Download Failed'

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
    
def user_pass():
    sys.stdout.write('username:')
    user = raw_input()
    passwd = getpass.getpass()
    return (user, passwd)


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

rtm_temp = ""
rtm_home = ""


def load_settings():
    global rtm_root, rtm_home

    root_dir = os.path.join(__path__[0], 'settings')
    setting = __load_subdir(root_dir)

    #print setting
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
            __setting['local'] = yaml.load(open(__local_setting_file, 'r'))

        __application_setting_file = os.path.join(os.getcwd(), 'setting.yaml')
        if os.path.isfile(__application_setting_file):
            appsetting = yaml.load(open(__application_setting_file, 'r'))
            if 'application' in appsetting.keys():
                __setting['application'] = appsetting['application']
    return __setting

def rtm_home():
    return setting()['common']['path']['RTM_HOME']

#if not os.path.isdir(rtm_home):
#    os.makedirs(rtm_home)

def rtm_temp():
    return setting()['common']['path']['RTM_TEMP']


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
    if line.find('darwin13'):
        return 'xcode5'
    elif line.find('darwin12'):
        return 'xcode4'
    else:
        raise UnsupportedPlatformException()


def platform():
    if sys.platform == 'darwin':
        import platform as plt
        ver = plt.mac_ver()[0]
        if ver.startswith('10.9'):
            _platform = 'osx10.9_' + xcode_check()
        elif ver.startswith('10.8'):
            _platform = 'osx10.8_' + xcode_check()
        elif ver.startswith('10.7'):
            _platform = 'osx10.7_' + xcode_check()
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
            
        if distri[1] == '12.04':
            _platform = _platform + '1204'
            
        if plt.architecture()[0] == '32bit':
            _platform = _platform + '_x86'
        else:
            _platform = _platform + '_x64'
            
    return _platform


