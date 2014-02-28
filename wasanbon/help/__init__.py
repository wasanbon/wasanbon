# Help module for wasanbon
import os, sys, locale, traceback, inspect
import wasanbon


def get_help_dir():
    helpdir = os.path.join(wasanbon.__path__[0],
                           'locale', 'messages',
                           locale.getdefaultlocale()[0])
    if not os.path.isdir(helpdir):
        helpdir = os.path.join(wasanbon.__path__[0],
                           'locale', 'messages',
                            'en_US')
    return helpdir
    
_default_help_message = {'brief' : 'Can not find help message.',
                         'detail' : ['Can not find help message'],
                         'subcommand' : {}}

_invalid_help_message = {'brief' : 'Can not load help message. Your system do not have yaml package',
                         'detail' : ['Can not load help message.', ' Your system do not have yaml package'],
                         'subcommand' : {}}

def get_help_text(path, cmd):
    module_name = 'wasanbon.core.management.' + path + '.' + cmd
    __import__(module_name)
    doc = sys.modules[module_name].__doc__
    loc = locale.getdefaultlocale()[0]
    return doc
    try:
        yaml = __import__('yaml')
        helpdir = get_help_dir()
        filename = os.path.join(helpdir, path, cmd +'.yaml')
        if os.path.isfile(filename):
            return yaml.load(open(filename, 'r'))
        else:
            return _default_help_message
    except:
        traceback.print_exc()
        return _invalid_help_message
    

