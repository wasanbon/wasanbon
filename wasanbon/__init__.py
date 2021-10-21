#!/usr/bin/env python
_version = '1.2.0'

import sys
import os
import locale
import getpass
import time  # , yaml
import platform as plt
import types
import codecs
import subprocess
import datetime
#from help import *


def get_version():
    """Get wasanbon version.
    """
    return _version


IDE = 'Visual Studio 16' if sys.platform == 'win32' else 'Makefile'
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


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


class InvalidRTCProfileException(WasanbonException):
    def msg(self):
        return 'Invalid RTCProfile'


def arg_check(argv, num):
    if len(argv) < num:
        raise InvalidUsageException()
    pass


def get_bin_file_ext():
    if sys.platform == 'win32':
        return '.dll'
    elif sys.platform == 'linux':
        return '.so'
    elif sys.platform == 'darwin':
        return '.dylib'
    else:
        print('---Unsupported System (%s)' % sys.platform)
        raise UnsupportedPlatformException()


def user_pass(user=None, passwd=None, token=None, reg=False):
    reg_data = {'github.com': {
        'username': user,
        'password': passwd,
        'token': token},
    }
    if reg == False and user == None and passwd == None and token == None:
        # load from register_file
        if os.path.isfile(register_file):
            reg_data = __load_yaml(register_file)

    if not reg_data['github.com']['username']:
        sys.stdout.write('username:')
        reg_data['github.com']['username'] = input()
    if not reg_data['github.com']['password']:
        reg_data['github.com']['password'] = getpass.getpass()
    if not reg_data['github.com']['token']:
        sys.stdout.write('token:')
        reg_data['github.com']['token'] = input()
    return (reg_data['github.com']['username'], reg_data['github.com']['password'], reg_data['github.com']['token'])


def timestampstr():
    return datetime.datetime.now().strftime('%Y%m%d%H%M%S')


def get_home_path():
    if sys.platform == 'darwin':
        return os.environ['HOME']
    elif sys.platform == 'win32':
        return os.path.join(os.environ['HOMEDRIVE'], os.environ['HOMEPATH'])
    elif sys.platform == 'linux':
        return os.environ['HOME']
    else:
        print('Unsupported System %s' % sys.platform)
    return ''


tagdict = {'$HOME': get_home_path()}

WASANBON_HOME_ENVKEY = 'WASANBON_HOME'
WASANBON_HOME_DEFAULT = os.path.join(get_home_path(), '.wasanbon')


def get_wasanbon_home():
    env = os.environ
    if WASANBON_HOME_ENVKEY in list(env.keys()):
        return env[WASANBON_HOME_ENVKEY]

    return WASANBON_HOME_DEFAULT


home_path = get_wasanbon_home()
temp_path = os.path.join(home_path, 'temp')
plugins_path = os.path.join(home_path, 'plugins')
register_file = os.path.join(home_path, 'register.yaml')
idl_path = os.path.join(home_path, 'idl')

username = None
if sys.platform == 'darwin' or sys.platform == 'linux':
    username = os.environ['USER']
    if username == 'root':  # might be launched with sudo
        username = os.environ.get('SUDO_USER', None)

if not os.path.isdir(home_path):
    os.mkdir(home_path)
if not os.path.isdir(temp_path):
    os.mkdir(temp_path)
if not os.path.isdir(plugins_path):
    os.mkdir(plugins_path)
if not os.path.isdir(idl_path):
    os.mkdir(idl_path)
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


def load_settings():
    root_dir = os.path.join(wasanbon.core.plugins.admin.environment_plugin.__path__[0], 'settings')
    setting = __load_subdir(root_dir)

    pathdict = setting['common']['path']
    if sys.platform == 'win32':
        for key in list(pathdict.keys()):
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
    for key in list(hash.keys()):
        if hash[key].find('$') < 0:
            tagdict['$' + key] = hash[key]


def __replace_tag_recursive(hash):
    if type(hash) is dict:
        for key in list(hash.keys()):
            hash[key] = __replace_tag_recursive(hash[key])
        return hash
    elif type(hash) is list:
        new_hash = []
        for v in hash:
            new_hash.append(__replace_tag_recursive(v))
        return new_hash
    else:
        return __replace_tag(hash)


def __replace_tag(str):
    global tagdict
    for tag in list(tagdict.keys()):
        str = str.replace(tag, tagdict[tag])
    return str


def __parse_yaml(hash):
    for key in list(hash.keys()):
        val = hash[key]
        if type(val) is dict:
            hash[key] = __parse_yaml(val)
        elif type(val) is bytes:
            hash[key] = __replace_tags(val)
    return hash


def __load_yaml(file):
    __import__('yaml')
    yaml = sys.modules['yaml']
    dict = yaml.safe_load(open(file, 'r'))
    if type(dict) == type(None):
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
                ret[dir[:len(dir) - 5]] = __load_yaml(path)
    return ret


# def __load_repositories():
#    return dict(setting['common']['repository'], **setting[platform]['repository'])


def platform():
    if sys.platform == 'darwin':
        _platform = 'macos'
    elif sys.platform == 'win32':
        _platform = 'windows'
    elif sys.platform == 'linux':
        import distro
        distri = distro.linux_distribution()

        if distri[0] == 'Ubuntu':
            _platform = 'ubuntu'
        elif distri[0] == 'debian':
            _platform = 'debian'

    return _platform


import wasanbon.core.plugins
plugins = wasanbon.core.plugins.Loader([plugins_path, wasanbon.core.plugins.__path__[0]])


def sleep(interval, verbose=True):
    times = int(interval * 5)
    #sys.stdout.write(' - Waiting approx. %s seconds\n' % interval)
    for t in range(times):
        percent = float(t) / times
        width = 30
        progress = (int(width * percent) + 1)
        sys.stdout.write('\r# [' + '#' * progress + ' ' * (width - progress) + ']')
        sys.stdout.flush()
        time.sleep(0.2)

    sys.stdout.write('\n')


rtm_root_hints = ['/usr/include/openrtm-1.2', '/usr/local/include/openrtm-1.2', '/opt/local/include/openrtm-1.2']


def get_rtm_root():
    if 'RTM_ROOT' in list(os.environ.keys()):
        return os.environ['RTM_ROOT']
    else:
        for hint in rtm_root_hints:
            if os.path.isfile(os.path.join(hint, 'rtm', 'version.txt')):
                return hint
        return ""
