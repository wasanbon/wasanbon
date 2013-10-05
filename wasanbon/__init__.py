#!/usr/bin/env python

import sys, os, locale, getpass
import yaml, types
import codecs

def get_version():
    """Get wasanbon version.
    """
    return "0.8.0"


sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

platform = ""

if sys.platform == 'darwin':
    import platform as plt
    ver = plt.mac_ver()[0]
    if ver.startswith('10.8'):
        platform = 'darwin108'
    if ver.startswith('10.7'):
        platform = 'darwin107'
elif sys.platform == 'win32':
    if sys.getwindowsversion()[1] == 1:
        platform = 'windows7'
    elif sys.getwindowsversion()[1] == 2:
        platform = 'windows8'

    if os.environ['PROCESSOR_ARCHITEW6432'] == 'AMD64':
        platform = platform + '_x64'
    else:
        platform = platform + '_x86'

elif sys.platform == 'linux2':
    import platform as plt
    distri = plt.linux_distribution()
    print distri
    if distri[0] == 'Ubuntu':
        platform = 'ubuntu'

        if distri[1] == '12.04':
            platform = platform + '1204'

    if plt.architecture()[0] == '32bit':
        platform = platform + '_x86'
    else:
        platform = platform + '_x64'
        


class BuildSystemException(Exception):
    def __init__(self):
        pass

class InvalidUsageException(Exception):
    def __init__(self):
        pass

class UnsupportedPlatformException(Exception):
    def __init__(self):
        pass

class DirectoryAlreadyExistsException(Exception):
    def __init__(self):
        pass

class ProjectAlreadyExistsException(Exception):
    def __init__(self):
        pass

class RepositoryNotFoundException(Exception):
    def __init__(self):
        pass

class RTCNotFoundException(Exception):
    def __init__(self):
        pass

class InvalidProjectPathError(Exception):
    def __init__(self):
        pass

class RTCProfileNotFoundException(Exception):
    def __init__(self):
        pass

class ProjectNotFoundException(Exception):
    def __init__(self):
        pass

class NoSuchFileException(Exception):
    def __init__(self):
        pass

def arg_check(argv, num):
    if len(argv) < num:
        raise InvalidUsageException()
    pass

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

def get_help_text(arg):
    locale_name = locale.getdefaultlocale()[0]
    filename = 'en_US.yaml'
    path = os.path.join(__path__[0], 'locale', 'messages')
    for file in os.listdir(path):
        if file.endswith('.yaml'):
            if file[:len(file)-5] == locale_name:
                filename = locale_name + '.yaml'
    y = data = yaml.load(open(os.path.join(path, filename), 'r'))
    for key in arg:
        if not key in y.keys():
            return data['none']#.encode('utf-8')
        y = y[key]

    #if type(y) is types.ListType:
    #    output = ''
    #    for str in y:
    #        output = output +  str + '\n'
    #    return output

    if not type(y) is types.DictType:
        """
        if type(y) is types.ListType:
            l = []
            for d in y:
                l.append(d.encode('utf-8'))
            y = l
        else:
            y = y#.encode('utf-8')
        """
        return y
    return data['none']#.encode('utf-8')
    

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

def __load_repositories():
    return dict(setting['common']['repository'], **setting[platform]['repository'])

setting = load_settings()

rtm_home = setting['common']['path']['RTM_HOME']
if not os.path.isdir(rtm_home):
    os.makedirs(rtm_home)

rtm_temp = setting['common']['path']['RTM_TEMP']
if not os.path.isdir(rtm_temp):
    os.makedirs(rtm_temp)

repositories = __load_repositories()

__local_setting_file = os.path.join(rtm_home, 'setting.yaml')
if os.path.isfile(__local_setting_file):
    setting['local'] = yaml.load(open(__local_setting_file, 'r'))

__local_repository_file = os.path.join(rtm_home, 'repository.yaml')
if os.path.isfile(__local_repository_file):
    setting['local_repo'] = yaml.load(open(__local_repository_file, 'r'))
    if type(setting['local_repo']) != types.NoneType:
        repositories = dict(repositories, **setting['local_repo'])

__application_setting_file = os.path.join(os.getcwd(), 'setting.yaml')
if os.path.isfile(__application_setting_file):
    appsetting = yaml.load(open(__application_setting_file, 'r'))
    if 'application' in appsetting.keys():
        setting['application'] = appsetting['application']

if 'application' in setting.keys():
    __application_repository_file = os.path.join(os.getcwd(), setting['application']['RTC_DIR'], 'repository.yaml')
    if os.path.isfile(__application_repository_file):
        app_repo = yaml.load(open(__application_repository_file, 'r'))
        if type(app_repo) != types.NoneType:
            setting['app_repo'] = app_repo
            repositories = dict(repositories, **setting['app_repo'])

